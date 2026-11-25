"""
Footage intake: index a folder of raw clips so the edit starts from a log,
not from scrubbing.

For every clip: specs (size, rotation, length, audio), a frame strip, and for
clips with speech a word-level transcript. Writes footage_index.json and
FOOTAGE LOG.md into the work folder. The editor reads the log to match takes
to script lines and to find B-roll, then writes the selects.
"""

from __future__ import annotations

import json
import os

from . import review, tools, transcribe

VIDEO_EXT = {".mp4", ".mov", ".m4v", ".mxf", ".mts", ".avi"}


def find_clips(folder: str) -> list:
    out = []
    for root, _, files in os.walk(folder):
        for f in sorted(files):
            if os.path.splitext(f)[1].lower() in VIDEO_EXT and not f.startswith("._"):
                out.append(os.path.join(root, f))
    return out


def index(folder: str, work: str, prompt: str | None = None, do_transcribe: bool = True,
          strips: bool = True) -> dict:
    os.makedirs(work, exist_ok=True)
    tdir = os.path.join(work, "transcripts")
    sdir = os.path.join(work, "strips")
    os.makedirs(tdir, exist_ok=True)
    os.makedirs(sdir, exist_ok=True)
    clips = []
    for path in find_clips(folder):
        info = tools.probe(path)
        rec = {"file": os.path.relpath(path, folder), "path": path, **info.to_dict()}
        rec.pop("extra", None)
        if strips:
            strip = os.path.join(sdir, os.path.splitext(os.path.basename(path))[0] + ".png")
            try:
                review.footage_sheet(path, strip)
                rec["strip"] = strip
            except tools.EditError:
                rec["strip"] = None
        if do_transcribe and info.has_audio:
            data = transcribe.load_or_transcribe(path, tdir, prompt=prompt)
            rec["words"] = len(data["words"])
            rec["text"] = data["text"]
            rec["talking"] = len(data["words"]) >= max(4, info.duration * 0.6)
            rec["unsure"] = [w["w"] for w in transcribe.low_confidence(data["words"])][:20]
        clips.append(rec)
    idx = {"folder": os.path.abspath(folder), "transcripts_dir": tdir, "clips": clips}
    with open(os.path.join(work, "footage_index.json"), "w") as f:
        json.dump(idx, f, indent=1)
    with open(os.path.join(work, "FOOTAGE LOG.md"), "w") as f:
        f.write(log_markdown(idx))
    return idx


def log_markdown(idx: dict) -> str:
    lines = ["# Footage log", "", f"Source: {idx['folder']}", "",
             "| Clip | Length | Frame | Audio | Talking | Opening words |", "|---|---|---|---|---|---|"]
    for c in idx["clips"]:
        txt = (c.get("text") or "").replace("|", "/")
        lines.append(f"| {c['file']} | {c['duration']:.1f}s | {c['display_w']}x{c['display_h']} | "
                     f"{'yes' if c['has_audio'] else 'no'} | {'yes' if c.get('talking') else 'no'} | {txt[:90]} |")
    lines += ["", "Talking clips are matched to script lines in SELECTS.md. Clips without speech are B-roll candidates.", ""]
    return "\n".join(lines)
