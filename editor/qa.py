"""
Edit QA gate: deterministic checks on a rendered ad before anyone sees it.

Reads the render and its .render.json manifest (timeline and every text
event with its box). Errors block delivery; warnings go in the review note
with a reason. This covers the mechanical rules only. The craft review
(references/edit-qa-checklist.md) is still done by eye on the contact sheet.

    python -m editor.cli qa "<AD> 9x16.mp4"
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass

from . import specs, tools

ERROR, WARN = "error", "warning"


@dataclass
class Finding:
    level: str
    rule: str
    msg: str
    t: float | None = None

    def __str__(self):
        at = f" @ {self.t:.2f}s" if self.t is not None else ""
        return f"[{self.level.upper()}] {self.rule}{at}: {self.msg}"


def _manifest_for(video: str):
    mp = os.path.splitext(video)[0] + ".render.json"
    if os.path.exists(mp):
        with open(mp) as f:
            return json.load(f)
    return None


def _fmt_from_size(w, h):
    for k, v in specs.FORMATS.items():
        if (v["w"], v["h"]) == (w, h):
            return k
    return None


def check_file(video: str) -> list:
    out = []
    man = _manifest_for(video)
    info = tools.probe(video)
    w, h = info.display_size
    fmt = _fmt_from_size(w, h)
    if info.rotation:
        out.append(Finding(ERROR, "rotation-flag", f"the file carries a {info.rotation} degree rotation flag; players will show it sideways"))
    if man and man.get("preview"):
        # a preview is half size and fast-encoded on purpose: check the edit, not the delivery spec
        out.append(Finding(WARN, "preview", "preview render, not for delivery"))
        if info.has_audio:
            ld = tools.loudness(video)
            if ld.get("input_i") is not None and abs(ld["input_i"] - specs.LOUDNESS_TARGET) > specs.LOUDNESS_TOLERANCE:
                out.append(Finding(ERROR, "loudness", f"{ld['input_i']:.1f} LUFS"))
        return out + check_manifest(man, man["format"], info.duration)
    if not fmt:
        out.append(Finding(ERROR, "frame-size", f"{w}x{h} is not a delivery size (1080x1920 or 1080x1350)"))
    if man and fmt and man.get("format") != fmt:
        out.append(Finding(ERROR, "frame-size", f"file is {fmt} but the plan rendered {man.get('format')}"))
    name = os.path.basename(video)
    m = re.match(r"^(.+) (9x16|4x5)\.mp4$", name)
    if not m:
        out.append(Finding(ERROR, "file-name", f"'{name}' should be '<AD NAME> 9x16.mp4' or '<AD NAME> 4x5.mp4'"))
    elif fmt and m.group(2) != fmt:
        out.append(Finding(ERROR, "file-name", f"name says {m.group(2)} but the frame is {fmt}"))
    if abs(info.fps - specs.FPS) > 0.2:
        out.append(Finding(ERROR, "frame-rate", f"{info.fps} fps, deliver at {specs.FPS}"))
    if info.vcodec != "h264" or info.pix_fmt != "yuv420p":
        out.append(Finding(ERROR, "codec", f"{info.vcodec}/{info.pix_fmt}, deliver h264/yuv420p"))
    if not info.has_audio:
        out.append(Finding(ERROR, "audio-missing", "no audio track"))
    elif info.acodec != "aac" or info.sample_rate != specs.AUDIO_RATE:
        out.append(Finding(ERROR, "audio-format", f"{info.acodec} {info.sample_rate} Hz, deliver AAC 48 kHz"))

    # Loudness
    if info.has_audio:
        ld = tools.loudness(video)
        li, tp = ld.get("input_i"), ld.get("input_tp")
        if li is None or li < -70:
            out.append(Finding(ERROR, "loudness", "the audio is silent"))
        else:
            if abs(li - specs.LOUDNESS_TARGET) > specs.LOUDNESS_TOLERANCE:
                out.append(Finding(ERROR, "loudness", f"{li:.1f} LUFS, target {specs.LOUDNESS_TARGET} plus or minus {specs.LOUDNESS_TOLERANCE}"))
            if tp is not None and tp > specs.TRUE_PEAK_MAX:
                out.append(Finding(ERROR, "true-peak", f"{tp:.1f} dBTP, keep under {specs.TRUE_PEAK_MAX}"))

    # Black frames, outside cards
    card_spans = []
    if man:
        t = 0.0
        for p in man.get("pieces", []):
            if p.get("card"):
                card_spans.append((t, t + p["dur"]))
            t += p["dur"]
    for a, b in tools.black_frames(video):
        if any(a >= s - 0.05 and b <= e + 0.05 for s, e in card_spans):
            continue
        if a < 0.3:
            out.append(Finding(ERROR, "black-open", "the ad opens on black; frame one has to carry the hook", a))
        elif b - a > 0.3:
            out.append(Finding(WARN, "black-frames", f"{b - a:.2f}s of black", a))

    # Dead air (speech gaps), outside cards and the last second
    dur = info.duration
    if info.has_audio and man and not man.get("has_music"):
        for a, b in tools.silences(video, min_dur=specs.DEAD_AIR_MAX):
            b = b if b is not None else dur
            if b > dur - 1.0 or any(a >= s - 0.1 and b <= e + 0.1 for s, e in card_spans):
                continue
            out.append(Finding(WARN, "dead-air", f"{b - a:.2f}s of silence mid-ad", a))

    if man and fmt:
        out += check_manifest(man, fmt, dur)
    return out


def check_manifest(man: dict, fmt: str, dur: float | None = None) -> list:
    from validator import validate_text  # the same copy rules as every other deliverable
    out = []
    W, H = specs.frame_size(fmt)
    x0, y0, x1, y1 = specs.safe_box(fmt)
    dur = dur if dur is not None else man.get("duration", 0)
    events = man.get("events", [])

    for e in events:
        bx0, by0, bx1, by1 = e["box"]
        if bx0 < x0 or by0 < y0 or bx1 > x1 or by1 > y1:
            out.append(Finding(ERROR, "safe-zone", f"{e['kind']} '{e['text'][:40]}' sits outside the {fmt} safe zone "
                               f"(box {e['box']}, safe {[x0, y0, x1, y1]})", e["start"]))
        if e["size"] < specs.CAPTION["min_size"]:
            out.append(Finding(ERROR, "text-size", f"{e['kind']} at {e['size']}px, minimum {specs.CAPTION['min_size']}", e["start"]))
        fbox = e.get("face")
        if fbox:
            ix = min(e["box"][2], fbox[2]) - max(e["box"][0], fbox[0])
            iy = min(e["box"][3], fbox[3]) - max(e["box"][1], fbox[1])
            if ix > 4 and iy > 4:
                out.append(Finding(ERROR, "caption-over-face", f"'{e['text'][:40]}' overlaps the face", e["start"]))
        if e["kind"] == "caption":
            if len(e["lines"]) > e.get("max_lines", specs.CAPTION["max_lines"]):
                out.append(Finding(ERROR, "caption-lines", f"'{e['text']}' runs to {len(e['lines'])} lines", e["start"]))
            if e["end"] - e["start"] < specs.CAPTION["min_event"] - 0.01:
                out.append(Finding(WARN, "caption-flash", f"'{e['text']}' is up for {e['end'] - e['start']:.2f}s", e["start"]))
        elif e["kind"] in ("hook", "cta", "label"):
            if e["end"] - e["start"] < specs.TITLE["min_on_screen"]:
                out.append(Finding(WARN, "title-short", f"'{e['text']}' is up for {e['end'] - e['start']:.2f}s, under {specs.TITLE['min_on_screen']}s", e["start"]))
        if e["start"] > dur + 0.05:
            out.append(Finding(WARN, "text-after-end", f"'{e['text']}' starts after the ad ends", e["start"]))
        kind = "content"
        for v in validate_text(e["text"], kind=kind, location=f"{fmt} {e['kind']} @ {e['start']:.2f}s").violations:
            lvl = ERROR if v.severity == "error" else WARN
            out.append(Finding(lvl, f"copy:{v.rule}", f"'{e['text']}': {v.message}", e["start"]))

    for fr in man.get("fonts", []):
        if fr.get("fallback"):
            out.append(Finding(ERROR, "font-fallback", f"'{fr['requested']}' was not found; the text rendered in {os.path.basename(fr['used'])}"))
    if events and not man.get("fonts"):
        out.append(Finding(WARN, "font-unchecked", "the render did not record which font was used"))

    words = man.get("words", [])
    pieces = man.get("pieces", [])
    opens_on_card = bool(pieces and pieces[0].get("card"))
    if words and not opens_on_card and words[0]["start"] > specs.HOOK_SPEECH_START_MAX:
        out.append(Finding(WARN, "slow-open", f"first word at {words[0]['start']:.2f}s; the hook should start by {specs.HOOK_SPEECH_START_MAX}s", 0))
    if not any(e["kind"] == "hook" and e["start"] <= 0.5 for e in events):
        out.append(Finding(WARN, "no-hook-text", "no on-screen hook text in the first half second (sound-off viewers get nothing)"))
    if words and not any(e["kind"] == "caption" for e in events):
        out.append(Finding(ERROR, "no-captions", "the ad has speech but no captions"))
    # the offer lives in the ad copy and the CTA button; the video ends naturally
    # (Liam, 2026-11-25), so a missing on-screen CTA is only flagged when the plan asks for one
    if man.get("cta_required") and not any(e["kind"] in ("cta", "card") and e["end"] >= dur - 0.5 for e in events):
        out.append(Finding(WARN, "no-cta", "the plan asks for an on-screen CTA and there is none at the close"))

    concept = (man.get("concept") or "default").lower()
    lo, hi = specs.LENGTH.get(concept, specs.LENGTH["default"])
    if man.get("max_seconds"):
        hi = float(man["max_seconds"])
    if dur > hi + 0.5:
        out.append(Finding(WARN, "length", f"{dur:.1f}s is over the {hi:.0f}s guide for {concept}"))
    if dur < lo - 0.5:
        out.append(Finding(WARN, "length", f"{dur:.1f}s is under the {lo:.0f}s guide for {concept}"))
    return out


def check(paths: list) -> dict:
    res = {}
    for p in paths:
        if os.path.isdir(p):
            for f in sorted(os.listdir(p)):
                if f.endswith(".mp4"):
                    res[os.path.join(p, f)] = check_file(os.path.join(p, f))
        else:
            res[p] = check_file(p)
    return res


def verify_cuts(plan_path: str) -> list:
    """Listen to the first moment after every cut and check it starts on the expected word.

    A cut a few hundredths too early carries the tail of a filler, a false start or the
    previous word ("uh", "So", "there's") and reads as a stutter. Each piece's first
    1.6 s is transcribed on its own (no prompt, so nothing is suggested) and compared with
    the first caption word the plan expects. Slow, so it runs on demand: editor.cli verify.
    """
    import mlx_whisper  # type: ignore
    from . import plan as planmod, transcribe
    p = planmod.load(plan_path)
    out = []
    cache = {}
    t = 0.0
    for pc in planmod.timeline(p):
        if pc.card or pc.mute or not pc.words:
            t += pc.dur
            continue
        if pc.src not in cache:
            cache[pc.src] = tools.audio_array(pc.src)
        a = cache[pc.src]
        seg = a[int(pc.t_in * 16000):int(min(pc.t_out, pc.t_in + 1.6) * 16000)]
        r = mlx_whisper.transcribe(seg, path_or_hf_repo=transcribe.DEFAULT_MODEL, language="en",
                                   condition_on_previous_text=False)
        heard = r.get("text", "").strip().split()
        want = pc.words[0]["w"].strip(specs.PUNCT).lower()
        got = heard[0].strip(specs.PUNCT).lower() if heard else ""
        if got and got != want and not (len(heard) > 1 and heard[1].strip(specs.PUNCT).lower() == want and got in specs.FILLER_WORDS):
            fix = clean_start(a, want, pc.t_in, pc.t_out)
            hint = f"; starts cleanly at {fix:.2f}s" if fix is not None else "; no clean start found nearby"
            out.append(Finding(WARN, "cut-in", f"cut at {pc.t_in:.2f}s should start on '{want}' but starts '{' '.join(heard[:3])}'{hint}", t))
        elif got in specs.FILLER_WORDS:
            out.append(Finding(WARN, "cut-in", f"cut at {pc.t_in:.2f}s starts on a filler '{got}'", t))
        t += pc.dur
    return out


def clean_start(audio, want: str, t_in: float, t_out: float, before: float = 0.3, after: float = 0.5, step: float = 0.03):
    """Scan around a cut-in for the earliest point whose first heard word is `want`."""
    import mlx_whisper  # type: ignore
    from . import transcribe
    t = max(0.0, t_in - before)
    while t <= t_in + after:
        seg = audio[int(t * 16000):int(min(t_out, t + 1.6) * 16000)]
        r = mlx_whisper.transcribe(seg, path_or_hf_repo=transcribe.DEFAULT_MODEL, language="en",
                                   condition_on_previous_text=False)
        heard = r.get("text", "").strip().split()
        if heard and heard[0].strip(specs.PUNCT).lower() == want:
            return round(t, 2)
        t += step
    return None
