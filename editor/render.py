"""
Render an edit plan to finished ads, one file per format.

Pipeline per format:
  1. each piece trimmed from source, reframed to the format (cover scale, crop
     on the plan's focus point, optional punch-in), cards drawn as colour frames
  2. pieces concatenated; tiny audio fades at every cut so jump cuts never click
  3. B-roll laid over the timeline (main audio keeps running underneath)
  4. captions, hook titles and card text burned in from one ASS file
  5. music bed under the voice, ducked by the voice (sidechain)
  6. two-pass loudness normalisation to -14 LUFS, true peak under -1 dBTP

Output: <out_dir>/<AD> <fmt>.mp4, plus <AD> <fmt>.render.json (the timeline
and every text event with its box) that the QA gate reads.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import tempfile

from . import captions, fonts as fontmod, plan as planmod, specs, tools

PRESET = os.environ.get("MAXALDING_X264_PRESET", "medium")


def _focus(obj, fmt):
    f = obj.get("focus") if isinstance(obj, dict) else obj
    if isinstance(f, dict):
        f = f.get(fmt) or f.get("default") or (0.5, 0.5)
    f = f or (0.5, 0.5)
    return float(f[0]), float(f[1])


_SIZE_CACHE = {}


def _src_size(path):
    if path not in _SIZE_CACHE:
        _SIZE_CACHE[path] = tools.probe(path).display_size
    return _SIZE_CACHE[path]


LAYOUT_FRAME = {  # where the eyes sit across the frame, and zoom, per layout
    "center": (0.50, 1.00), "punch": (0.50, 1.15), "left": (0.68, 0.94), "right": (0.32, 0.94)}


def _reframe(W, H, zoom, fx, fy, src=None, fmt="9x16", layout="center"):
    """Scale to cover the frame (times zoom) and crop so the focus point lands on the eye line.

    focus (fx, fy) is where the eyes are in the source, as fractions of its width and
    height. The crop puts that point at specs.EYE_LINE for the format, clamped so the
    crop never leaves the picture.
    """
    from .faces import crop
    sw, sh = _src_size(src) if src else (W, H)
    zw, zh, cx, cy = crop(W, H, sw, sh, zoom, fx, fy, fmt, layout)
    return (f"scale={zw}:{zh},crop={W}:{H}:{int(cx)}:{int(cy)},setsar=1,fps={specs.FPS},format={specs.PIX_FMT}")


def _grade(plan: dict) -> str:
    """Optional light grade on every piece: exposure (+/- stops, roughly) and highlights
    (negative pulls bright areas down, e.g. a light jumper washing out white captions)."""
    g = plan.get("grade") or {}
    out = []
    ex = float(g.get("exposure", 0))
    if ex:
        out.append(f"eq=gamma={2 ** ex:.3f}")
    hl = float(g.get("highlights", 0))
    if hl:
        top = max(0.5, min(1.0, 1 + hl))
        out.append(f"curves=all='0/0 0.5/{0.5 + hl * 0.15:.3f} 1/{top:.3f}'")
    return ("," + ",".join(out)) if out else ""


def _hex(c):
    return "0x" + c.lstrip("#")


def _filter_path(p: str) -> str:
    return p.replace("\\", "\\\\").replace("'", "\\'").replace(":", "\\:")


def _proxy_dir(plan: dict) -> str:
    d = plan.get("proxy_dir") or os.path.join(plan.get("_base", "."), "..", "proxies")
    d = planmod.resolve(plan, d) if not os.path.isabs(d) else d
    os.makedirs(d, exist_ok=True)
    return d


def proxies(plan: dict) -> list:
    """Decode each clip's span once into an upright 1080x1920 30 fps proxy for previews.

    Camera originals (4K 10-bit 4:2:2) take minutes to decode; every preview, hook
    variant and feedback round after the first reads these instead. Returns a list of
    (src, start, end, proxy_path). Proxies are reused across plans that share spans.
    """
    out = []
    d = _proxy_dir(plan)
    for c in plan.get("clips", []):
        if "src" not in c:
            continue
        src = planmod.resolve(plan, c["src"])
        a = max(0.0, float(c.get("in", 0)) - 0.5)
        b = float(c["out"]) + 0.5 if c.get("out") is not None else tools.probe(src).duration
        if any(s == src and pa <= a and b <= pb for s, pa, pb, _ in out):
            continue
        base = os.path.splitext(os.path.basename(src))[0]
        path = os.path.join(d, f"{base}_{a:.2f}_{b:.2f}.mp4")
        # reuse any existing proxy of this source that already covers the span
        cover = None
        for f in os.listdir(d):
            if f.startswith(base + "_") and f.endswith(".mp4"):
                try:
                    pa, pb = (float(x) for x in f[len(base) + 1:-4].split("_"))
                except ValueError:
                    continue
                if pa <= a and b <= pb:
                    cover = (pa, pb, os.path.join(d, f))
                    break
        if cover:
            out.append((src, cover[0], cover[1], cover[2]))
            continue
        sw, sh = _src_size(src)
        vf = "scale=-2:1920" if sh >= sw else "scale=1920:-2"
        tools.run(["-y", "-ss", f"{a:.3f}", "-t", f"{b - a:.3f}", "-i", src, "-vf", f"{vf},fps={specs.FPS},format={specs.PIX_FMT}",
                   "-c:v", "libx264", "-preset", "ultrafast", "-crf", "16", "-c:a", "pcm_s16le", "-ar", str(specs.AUDIO_RATE),
                   path.replace(".mp4", ".tmp.mov")])
        # frames are upright now; strip the camera's rotation flag that ffmpeg carries over
        tools.run(["-y", "-display_rotation", "0", "-i", path.replace(".mp4", ".tmp.mov"), "-c", "copy", "-f", "mov", path])
        os.remove(path.replace(".mp4", ".tmp.mov"))
        out.append((src, a, b, path))
    return out


def render_format(plan: dict, fmt: str, out_dir: str, pieces=None, preview: bool = False) -> dict:
    """Render one format. preview=True is the quick look for feedback: half resolution,
    fastest encode, faster decode, same cut, captions and audio. Named '<AD> <fmt> PREVIEW'."""
    W, H = specs.frame_size(fmt)
    if preview:
        W, H = W // 2, H // 2  # the ASS keeps full-size coordinates; libass scales it to the frame
    pieces = pieces if pieces is not None else planmod.timeline(plan)
    total = planmod.duration(pieces)
    os.makedirs(out_dir, exist_ok=True)
    name = f"{plan['ad']} {fmt}" + (" PREVIEW" if preview else "")
    fast_in = []
    prox = proxies(plan) if preview else []
    work = tempfile.mkdtemp(prefix="mx_edit_")
    inputs, graph, cat = [], [], []
    brand = captions.brand_for(plan)

    for k, p in enumerate(pieces):
        if p.card:
            bg = p.card.get("bg", brand["card_bg"])
            graph.append(f"color=c={_hex(bg)}:s={W}x{H}:r={specs.FPS}:d={p.dur:.3f},format={specs.PIX_FMT},setsar=1[v{k}]")
            ca = p.card.get("audio")
            if ca:
                # a line of voice under the card (e.g. the coach's CTA), faded so it never clicks
                idx = _count_inputs(inputs)
                a_in, a_out = float(ca.get("in", 0)), float(ca["out"])
                inputs += ["-ss", f"{a_in:.3f}", "-t", f"{a_out - a_in:.3f}", "-i", planmod.resolve(plan, ca["src"])]
                fo = max(0.0, (a_out - a_in) - 0.08)
                delay = int(float(ca.get("at", 0.15)) * 1000)
                graph.append(f"[{idx}:a]aresample={specs.AUDIO_RATE},aformat=channel_layouts=stereo,asetpts=PTS-STARTPTS,"
                             f"volume={float(ca.get('gain_db', 0))}dB,afade=t=in:d=0.03,afade=t=out:st={fo:.3f}:d=0.08,"
                             f"adelay={delay}|{delay},apad=whole_dur={p.dur:.3f},atrim=duration={p.dur:.3f}[a{k}]")
            else:
                graph.append(f"aevalsrc=0|0:d={p.dur:.3f}:s={specs.AUDIO_RATE}[a{k}]")
        else:
            idx = _count_inputs(inputs)
            src_path, t_in = p.src, p.t_in
            if preview:
                for s0, pa, pb, px in prox:
                    if s0 == p.src and pa <= p.t_in and p.t_out <= pb:
                        src_path, t_in = px, p.t_in - pa
                        break
            inputs += fast_in + ["-ss", f"{t_in:.3f}", "-t", f"{p.dur:.3f}", "-i", src_path]
            from .faces import focus_for
            fx, fy = focus_for(p, fmt)
            graph.append(f"[{idx}:v]{_reframe(W, H, p.zoom, fx, fy, src_path, fmt, p.layout)}{_grade(plan)},trim=duration={p.dur:.3f},setpts=PTS-STARTPTS[v{k}]")
            info = tools.probe(src_path)
            if info.has_audio and not p.mute:
                fo = max(0.0, p.dur - 0.015)
                graph.append(f"[{idx}:a]aresample={specs.AUDIO_RATE},aformat=channel_layouts=stereo,atrim=duration={p.dur:.3f},"
                             f"asetpts=PTS-STARTPTS,afade=t=in:d=0.012,afade=t=out:st={fo:.3f}:d=0.015,apad=whole_dur={p.dur:.3f}[a{k}]")
            else:
                graph.append(f"aevalsrc=0|0:d={p.dur:.3f}:s={specs.AUDIO_RATE}[a{k}]")
        cat.append(f"[v{k}][a{k}]")
    graph.append("".join(cat) + f"concat=n={len(pieces)}:v=1:a=1[vc][ac]")
    vlast, alast = "vc", "ac"

    for j, b in enumerate(plan.get("broll", [])):
        if b.get("formats") and fmt not in b["formats"]:
            continue
        src = planmod.resolve(plan, b["src"])
        dur = float(b.get("dur", 2.0))
        at = float(b["at"])
        idx = _count_inputs(inputs)
        inputs += fast_in + ["-ss", f"{float(b.get('in', 0)):.3f}", "-t", f"{dur:.3f}", "-i", src]
        fx, fy = _focus(b, fmt)
        graph.append(f"[{idx}:v]{_reframe(W, H, float(b.get('zoom', 1.0)), fx, fy, src, fmt)},trim=duration={dur:.3f},setpts=PTS-STARTPTS+{at:.3f}/TB[b{j}]")
        graph.append(f"[{vlast}][b{j}]overlay=enable='between(t,{at:.3f},{at + dur:.3f})':eof_action=pass[vb{j}]")
        vlast = f"vb{j}"

    ass_text, events = captions.build(plan, pieces, fmt)
    ass_path = os.path.join(work, "text.ass")
    with open(ass_path, "w") as f:
        f.write(ass_text)
    font_dir = os.path.join(work, "fonts")
    prepared = fontmod.prepare_all(brand, font_dir, plan.get("_base", "."))
    fd = f":fontsdir='{_filter_path(font_dir)}'"
    font_report, seen = [], set()
    probe_times = sorted({min(e["start"] for e in events if e["kind"] == k) + 0.05 for k in {e["kind"] for e in events}})
    found = [r for t in probe_times for r in fontmod.used_fonts(_filter_path(ass_path), _filter_path(font_dir), W, H, at=t)]
    for fam, _w, used in found:
        if fam in seen:
            continue
        seen.add(fam)
        ours = {v for f in prepared["faces"].values() if f for v in (f["file"], os.path.splitext(os.path.basename(f["file"]))[0])}
        font_report.append({"requested": fam, "used": used, "fallback": used not in ours and not used.startswith(font_dir)})
    graph.append(f"[{vlast}]ass=filename='{_filter_path(ass_path)}'{fd}[vout]")

    m = plan.get("music")
    if m:
        idx = _count_inputs(inputs)
        inputs += ["-stream_loop", "-1", "-i", planmod.resolve(plan, m["src"])]
        gain = float(m.get("gain_db", specs.MUSIC_BED_DB))
        st = float(m.get("start", 0))
        fade = max(0.0, total - 1.2)
        graph.append(f"[{idx}:a]aresample={specs.AUDIO_RATE},aformat=channel_layouts=stereo,atrim={st:.3f}:{st + total:.3f},asetpts=PTS-STARTPTS,"
                     f"volume={gain}dB,afade=t=in:d=0.3,afade=t=out:st={fade:.3f}:d=1.2[mus]")
        if m.get("duck", True):
            graph.append(f"[{alast}]asplit=2[voice][sc]")
            graph.append("[mus][sc]sidechaincompress=threshold=0.03:ratio=6:attack=15:release=350[musd]")
            graph.append("[voice][musd]amix=inputs=2:duration=first:normalize=0[aout]")
        else:
            graph.append(f"[{alast}][mus]amix=inputs=2:duration=first:normalize=0[aout]")
    else:
        graph.append(f"[{alast}]anull[aout]")

    script = os.path.join(work, "graph.txt")
    with open(script, "w") as f:
        f.write(";\n".join(graph))
    tmp = os.path.join(work, "pass1.mp4")
    tools.run(["-y"] + inputs + ["-filter_complex_script", script, "-map", "[vout]", "-map", "[aout]",
               "-t", f"{total:.3f}", "-c:v", specs.VIDEO_CODEC, "-preset", "ultrafast" if preview else PRESET,
               "-crf", "28" if preview else str(specs.CRF),
               "-profile:v", "high", "-pix_fmt", specs.PIX_FMT, "-r", str(specs.FPS),
               "-c:a", "aac", "-b:a", "320k", "-ar", str(specs.AUDIO_RATE), tmp])

    out = os.path.join(out_dir, name + ".mp4")
    meas = tools.loudness(tmp).get("raw", {})
    if meas and _finite(meas.get("input_i")):
        ln = (f"loudnorm=I={specs.LOUDNESS_TARGET}:TP=-1.5:LRA=11:measured_I={meas['input_i']}:measured_TP={meas['input_tp']}:"
              f"measured_LRA={meas['input_lra']}:measured_thresh={meas['input_thresh']}:offset={meas['target_offset']}:linear=true")
        afilter = ["-af", ln]
    else:
        afilter = []  # silent track, nothing to normalise
    # -display_rotation 0: the frames are already upright; drop the camera's rotation
    # flag, which ffmpeg carries through from phone or camera footage and which would
    # make players turn the finished ad sideways
    tools.run(["-y", "-display_rotation", "0", "-i", tmp, "-c:v", "copy"] + afilter + ["-ar", str(specs.AUDIO_RATE), "-c:a", "aac",
               "-b:a", specs.AUDIO_BITRATE, "-movflags", "+faststart", out])

    manifest = {
        "plan": plan.get("_path"), "ad": plan["ad"], "client": plan.get("client"), "concept": plan.get("concept"),
        "format": fmt, "file": out, "duration": total, "preview": preview,
        "pieces": [{"src": p.src, "in": p.t_in, "out": p.t_out, "dur": round(p.dur, 3), "role": p.role,
                    "card": p.card, "zoom": p.zoom, "layout": p.layout} for p in pieces],
        "events": events, "words": planmod.all_words(pieces),
        "has_music": bool(m), "max_seconds": plan.get("max_seconds"), "cta_required": bool(plan.get("cta_required")),
        "fonts": font_report,
        "font_sources": {r: (f or {}).get("source") for r, f in prepared["faces"].items()},
    }
    with open(os.path.join(out_dir, name + ".render.json"), "w") as f:
        json.dump(manifest, f, indent=1)
    shutil.copy(ass_path, os.path.join(out_dir, name + ".ass"))
    shutil.rmtree(work, ignore_errors=True)
    return manifest


def _finite(v) -> bool:
    try:
        x = float(v)
        return x == x and abs(x) != float("inf")
    except (TypeError, ValueError):
        return False


def _count_inputs(inputs: list) -> int:
    return sum(1 for a in inputs if a == "-i")


def render(plan: dict, out_dir: str, formats=None, preview: bool = False) -> list:
    errs = planmod.check(plan)
    if errs:
        raise tools.EditError("Plan cannot render:\n  " + "\n  ".join(errs))
    pieces = planmod.timeline(plan)
    if preview and not formats:
        formats = ["9x16"]  # one format is enough to judge the cut
    fmts = formats or plan.get("formats") or list(specs.FORMATS)
    return [render_format(plan, fmt, out_dir, pieces, preview=preview) for fmt in fmts]
