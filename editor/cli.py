"""
Maxalding video edit command line.

    python -m editor.cli index <footage folder> --work <work folder> [--prompt "offer words"]
    python -m editor.cli transcribe <clip> [--work <folder>] [--prompt "names"]
    python -m editor.cli refine <clip> <start> <end> --work <folder>   re-time one span verbatim
    python -m editor.cli verify <plan.json>            listen to every cut-in for stray words or fillers
    python -m editor.cli timeline <plan.json>          print the cut, words and length
    python -m editor.cli render <plan.json> --out <folder> [--formats 9x16 4x5]
    python -m editor.cli qa <video or folder>    the edit QA gate (exit 1 on any error)
    python -m editor.cli sheet <video>                 contact sheet + first frame for review
    python -m editor.cli build <plan.json> --out <folder>   render, QA and sheets in one go
    python -m editor.cli build <plan.json> --out <folder> --preview   quick half-size 9x16 for feedback

Run from the plugin root (the folder with editor/ and validator/).
"""

from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from editor import footage, plan as planmod, qa, render, review, transcribe  # noqa: E402


def _print_findings(results: dict) -> int:
    errors = 0
    for path, finds in results.items():
        e = [f for f in finds if f.level == qa.ERROR]
        w = [f for f in finds if f.level == qa.WARN]
        errors += len(e)
        print(f"\n{os.path.basename(path)}: {len(e)} error(s), {len(w)} warning(s)")
        for f in e + w:
            print(f"  {f}")
    print(f"\nEdit QA gate: {'PASSED' if errors == 0 else 'FAILED'} ({errors} error(s)).")
    return 0 if errors == 0 else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="editor")
    sub = ap.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("index"); a.add_argument("folder"); a.add_argument("--work", required=True)
    a.add_argument("--prompt"); a.add_argument("--no-transcribe", action="store_true")
    a = sub.add_parser("transcribe"); a.add_argument("clip"); a.add_argument("--work"); a.add_argument("--prompt")
    a = sub.add_parser("refine"); a.add_argument("clip"); a.add_argument("start", type=float); a.add_argument("end", type=float)
    a.add_argument("--work"); a.add_argument("--prompt")
    a = sub.add_parser("verify"); a.add_argument("plan")
    a = sub.add_parser("timeline"); a.add_argument("plan")
    a = sub.add_parser("render"); a.add_argument("plan"); a.add_argument("--out", required=True); a.add_argument("--formats", nargs="*")
    a.add_argument("--preview", action="store_true")
    a = sub.add_parser("qa"); a.add_argument("paths", nargs="+")
    a = sub.add_parser("sheet"); a.add_argument("video"); a.add_argument("--every", type=float)
    a = sub.add_parser("build"); a.add_argument("plan"); a.add_argument("--out", required=True); a.add_argument("--formats", nargs="*")
    a.add_argument("--preview", action="store_true", help="quick half-size 9x16 look for feedback")
    args = ap.parse_args(argv)

    if args.cmd == "index":
        idx = footage.index(args.folder, args.work, prompt=args.prompt, do_transcribe=not args.no_transcribe)
        print(f"Indexed {len(idx['clips'])} clip(s). Log: {os.path.join(args.work, 'FOOTAGE LOG.md')}")
        return 0
    if args.cmd == "transcribe":
        data = transcribe.load_or_transcribe(args.clip, args.work, prompt=args.prompt)
        print(data["text"])
        unsure = transcribe.low_confidence(data["words"])
        if unsure:
            print("\nCheck these words against the footage: " + ", ".join(f"{w['w']} ({w['start']:.1f}s)" for w in unsure))
        return 0
    if args.cmd == "refine":
        new = transcribe.refine(args.clip, args.start, args.end, args.work, args.prompt)
        print(" ".join(f"{w['w']}({w['start']:.2f})" for w in new))
        return 0
    if args.cmd == "verify":
        finds = qa.verify_cuts(args.plan)
        for f in finds:
            print(" ", f)
        print(f"Cut check: {len(finds)} cut(s) to look at." if finds else "Cut check: every cut starts on its word.")
        return 0
    if args.cmd == "timeline":
        p = planmod.load(args.plan)
        errs = planmod.check(p)
        for e in errs:
            print("PLAN ERROR:", e)
        pieces = planmod.timeline(p)
        t = 0.0
        for pc in pieces:
            label = f"CARD '{pc.card.get('text', '')}'" if pc.card else f"{os.path.basename(pc.src)} {pc.t_in:.2f}-{pc.t_out:.2f}"
            said = " ".join(w["w"] for w in pc.words)
            print(f"{t:6.2f}s  {pc.dur:5.2f}s  {pc.role:8s} {label}  {said}")
            t += pc.dur
        print(f"\nLength: {planmod.duration(pieces):.2f}s across {len(pieces)} piece(s)")
        return 1 if errs else 0
    if args.cmd in ("render", "build"):
        p = planmod.load(args.plan)
        mans = render.render(p, args.out, args.formats, preview=args.preview)
        for m in mans:
            print(f"Rendered {m['file']} ({m['duration']:.2f}s)")
        if args.cmd == "render":
            return 0
        rc = _print_findings({m["file"]: qa.check_file(m["file"]) for m in mans})
        for m in mans:
            print("Sheet:", review.contact_sheet(m["file"]))
            print("Frame 1:", review.first_frame(m["file"]))
        return rc
    if args.cmd == "qa":
        return _print_findings(qa.check(args.paths))
    if args.cmd == "sheet":
        print(review.contact_sheet(args.video, every=args.every))
        print(review.first_frame(args.video))
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
