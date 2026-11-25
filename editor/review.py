"""
Review aids: a contact sheet of the cut with the safe zone drawn on, and the
first frame on its own (it is the thumbnail and the hook frame).

The editor reads these images before handing anything over. They are how a
cut gets looked at, not just measured.
"""

from __future__ import annotations

import math
import os

from . import specs, tools


def _font():
    for f in ("~/Library/Fonts/Helvetica.ttf", "/System/Library/Fonts/Helvetica.ttc",
              "/System/Library/Fonts/Supplemental/Arial.ttf", "/Library/Fonts/Arial.ttf"):
        p = os.path.expanduser(f)
        if os.path.exists(p):
            return p
    return None


def contact_sheet(video: str, out: str | None = None, every: float | None = None,
                  cols: int = 6, thumb_w: int = 270) -> str:
    info = tools.probe(video)
    w, h = info.display_size
    fmt = "9x16" if h / max(w, 1) > 1.5 else "4x5"
    z = specs.SAFE_ZONES[fmt]
    dur = max(info.duration, 0.1)
    every = every or max(0.5, round(dur / 24, 2))
    n = max(1, int(math.floor(dur / every)))
    rows = math.ceil(n / cols)
    out = out or os.path.splitext(video)[0] + " sheet.png"
    vf = [f"fps=1/{every}", f"scale={thumb_w}:-2",
          f"drawbox=x=iw*{z['left']}:y=ih*{z['top']}:w=iw*{1 - z['left'] - z['right']:.3f}:h=ih*{1 - z['top'] - z['bottom']:.3f}:color=red@0.7:t=2"]
    font = _font()
    if font:
        ff = font.replace(":", "\\:")
        vf.append(f"drawtext=fontfile='{ff}':text='%{{pts\\:hms}}':x=6:y=6:fontsize=18:fontcolor=white:box=1:boxcolor=black@0.6")
    vf.append(f"tile={cols}x{rows}:padding=4:margin=4")
    tools.run(["-y", "-i", video, "-vf", ",".join(vf), "-frames:v", "1", "-update", "1", out])
    return out


def first_frame(video: str, out: str | None = None) -> str:
    out = out or os.path.splitext(video)[0] + " frame1.png"
    return tools.frame_png(video, 0.0, out, width=540)


def footage_sheet(video: str, out: str, n: int = 8, thumb_w: int = 240) -> str:
    """A strip of n frames across a raw clip, for logging footage.

    Seeks to each frame rather than decoding the whole clip, so a long 4K
    10-bit interview takes seconds, not minutes.
    """
    info = tools.probe(video)
    dur = max(info.duration, 0.1)
    args, graph = ["-y"], []
    for i in range(n):
        t = dur * (i + 0.5) / n
        args += ["-ss", f"{t:.2f}", "-i", video]
        graph.append(f"[{i}:v]scale={thumb_w}:-2,setsar=1[t{i}]")
    graph.append("".join(f"[t{i}]" for i in range(n)) + f"hstack=inputs={n}[out]")
    tools.run(args + ["-filter_complex", ";".join(graph), "-map", "[out]", "-frames:v", "1", "-update", "1", out])
    return out
