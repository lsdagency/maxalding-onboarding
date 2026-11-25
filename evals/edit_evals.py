"""
Regression evals for the video edit engine (editor/).

Unit layer (always runs): tightening, caption chunking, safe-zone layout and
the edit QA gate's manifest checks, on synthetic words, no media needed.
Render layer (runs when ffmpeg is available): a synthetic clip is rendered
end to end at 9x16 and the edit QA gate must pass it with zero errors.
"""

from __future__ import annotations

import json
import os
import shutil
import tempfile


def _words(text: str, start: float = 0.3, step: float = 0.32, gaps=None) -> list:
    out, t = [], start
    gaps = gaps or {}
    for i, w in enumerate(text.split()):
        t += gaps.get(i, 0.0)
        out.append({"w": w, "start": round(t, 3), "end": round(t + step - 0.04, 3), "p": 0.99})
        t += step
    return out


def run_unit_evals() -> list:
    from editor import captions, plan as planmod, qa, specs
    fails = []

    # tighten: a long pause and a filler are cut, speech is kept
    ws = _words("Start with um four sessions", gaps={3: 1.2})
    spans = planmod.tighten(ws, 0.0, 6.0)
    kept = sum(b - a for a, b in spans)
    if len(spans) < 2:
        fails.append(f"edit tighten: expected a jump cut at the 1.2s pause, got {spans}")
    if kept > 2.2:
        fails.append(f"edit tighten: kept {kept:.2f}s, dead air not removed")
    um = next(w for w in ws if w["w"] == "um")
    if any(a <= um["start"] and um["end"] <= b for a, b in spans):
        fails.append("edit tighten: filler 'um' survived")

    # chunking: never end a chunk on 'the', keep named phrases whole
    ws = _words("Start with four sessions for the price of three")
    chunks = [" ".join(w["w"] for w in c) for c in captions.chunk_words(ws, 3, 22, 0.3, ["price of three"])]
    if any(c.split()[-1].lower() in ("the", "for", "of") for c in chunks):
        fails.append(f"edit captions: chunk ends on a leaning word: {chunks}")
    if not any("price of three" in c for c in chunks):
        fails.append(f"edit captions: keep-together phrase was split: {chunks}")

    # layout: default titles, captions and cards land inside the safe zone in both formats
    plan = {"client": "Eval", "ad": "EVAL", "clips": [], "captions": {"on": True},
            "titles": [{"text": "Aged 40 to 55 and living in South Kensington?", "start": 0, "end": 3, "style": "hook"},
                       {"text": "Tap below to book in", "start": 5, "end": 8, "style": "cta"}]}
    piece = planmod.Piece(src="x", t_in=0, t_out=5, words=_words("If you are forty to fifty five listen to this"))
    card = planmod.Piece(src="", t_in=0, t_out=0, card={"text": "Start with four sessions for the price of three", "duration": 3})
    for fmt in specs.FORMATS:
        _, events = captions.build(plan, [piece, card], fmt)
        x0, y0, x1, y1 = specs.safe_box(fmt)
        for e in events:
            bx0, by0, bx1, by1 = e["box"]
            if bx0 < x0 or by0 < y0 or bx1 > x1 or by1 > y1:
                fails.append(f"edit layout {fmt}: {e['kind']} '{e['text']}' outside safe zone {e['box']}")
        caps = [e for e in events if e["kind"] == "caption"]
        if any(c["end"] > 5.0 + 1e-6 for c in caps):
            fails.append(f"edit layout {fmt}: a caption hangs over the end card")

    # QA manifest checks catch what they should
    base = {"format": "9x16", "duration": 10, "concept": "default", "pieces": [{"dur": 10}],
            "words": [{"w": "Hi", "start": 0.2, "end": 0.4}],
            "fonts": [{"requested": "TikTok Sans 900", "used": "TikTokSans900-Brand", "fallback": False}]}
    good = dict(base, events=[
        {"kind": "hook", "text": "Aged 40 to 55?", "start": 0, "end": 3, "lines": ["Aged 40 to 55?"], "size": 84, "box": [200, 300, 880, 420]},
        {"kind": "caption", "text": "Hi there", "start": 0.2, "end": 0.9, "lines": ["Hi there"], "size": 80, "box": [300, 1100, 780, 1200]},
        {"kind": "cta", "text": "Tap below to book in", "start": 8, "end": 10, "lines": ["Tap below to book in"], "size": 84, "box": [100, 1100, 980, 1220]},
    ])
    errs = [f for f in qa.check_manifest(good, "9x16") if f.level == qa.ERROR]
    if errs:
        fails.append(f"edit qa: clean manifest flagged: {[str(e) for e in errs]}")
    bad_cases = [
        ("safe-zone", {"kind": "hook", "text": "Too high", "start": 0, "end": 3, "lines": ["Too high"], "size": 84, "box": [200, 40, 880, 160]}),
        ("copy:banned-character", {"kind": "caption", "text": "Book now" + chr(33), "start": 1, "end": 2, "lines": ["Book now" + chr(33)], "size": 80, "box": [300, 1100, 780, 1200]}),
        ("copy:premium-framing", {"kind": "caption", "text": "Your free session", "start": 1, "end": 2, "lines": ["Your free session"], "size": 80, "box": [300, 1100, 780, 1200]}),
        ("text-size", {"kind": "caption", "text": "tiny", "start": 1, "end": 2, "lines": ["tiny"], "size": 30, "box": [400, 1100, 680, 1150]}),
    ]
    for rule, ev in bad_cases:
        m = dict(good, events=good["events"] + [ev])
        rules = {f.rule for f in qa.check_manifest(m, "9x16") if f.level == qa.ERROR}
        if not any(r == rule or r.startswith(rule) for r in rules):
            fails.append(f"edit qa: expected {rule}, got {sorted(rules)}")
    fb = dict(good, fonts=[{"requested": "TikTok Sans 700", "used": "Helvetica-Bold", "fallback": True}])
    if "font-fallback" not in {f.rule for f in qa.check_manifest(fb, "9x16")}:
        fails.append("edit qa: font fallback to Helvetica not caught")
    return fails


def run_render_eval() -> list:
    from editor import qa, render, tools, plan as planmod
    if not tools.available():
        print("  (skipped render eval: ffmpeg not found)")
        return []
    try:
        import fontTools  # noqa: F401
    except ImportError:
        print("  (skipped render eval: fontTools not installed)")
        return []
    fails = []
    work = tempfile.mkdtemp(prefix="mx_edit_eval_")
    try:
        src = os.path.join(work, "TALK.mp4")
        # camera footage shot upright carries a rotation flag; the render must come out upright and unflagged
        raw = os.path.join(work, "RAW.mp4")
        tools.run(["-y", "-f", "lavfi", "-i", "testsrc2=s=1920x1080:r=25", "-f", "lavfi",
                   "-i", "sine=frequency=220:sample_rate=48000", "-t", "5", "-c:v", "libx264", "-preset", "ultrafast",
                   "-c:a", "aac", "-shortest", raw])
        tools.run(["-y", "-display_rotation", "90", "-i", raw, "-c", "copy", src])
        words = _words("If you are forty to fifty five this is for you", start=0.4, step=0.35, gaps={6: 0.9})
        plan = {"client": "Eval Client", "ad": "EVAL HOOK 1", "concept": "default", "formats": ["9x16"],
                "clips": [{"src": src, "in": 0, "out": 5, "tighten": True, "words": words},
                          {"card": {"text": "Tap below to book in", "duration": 2}}],
                "titles": [{"text": "Aged 40 to 55?", "start": 0, "end": 2.5, "style": "hook"}],
                "captions": {"on": True}}
        path = os.path.join(work, "plan.json")
        with open(path, "w") as f:
            json.dump(plan, f)
        os.environ.setdefault("MAXALDING_X264_PRESET", "ultrafast")
        render.PRESET = os.environ["MAXALDING_X264_PRESET"]
        mans = render.render(planmod.load(path), os.path.join(work, "out"))
        for m in mans:
            errs = [f for f in qa.check_file(m["file"]) if f.level == qa.ERROR]
            if errs:
                fails.append(f"edit render: QA errors on a clean render: {[str(e) for e in errs]}")
            if m["duration"] > 6.5:
                fails.append(f"edit render: tightening did not shorten the clip ({m['duration']}s)")
    except Exception as e:  # report, do not crash the eval run
        fails.append(f"edit render: {type(e).__name__}: {str(e)[-600:]}")
    finally:
        shutil.rmtree(work, ignore_errors=True)
    return fails
