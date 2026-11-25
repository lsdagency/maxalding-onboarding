"""
The edit plan (EDL): one JSON file per ad, the single source of truth for a cut.

The editor writes the plan, the renderer turns it into files, the QA gate
checks the render against it. Nothing about a cut lives anywhere else, so a
feedback note ("cut the pause after the hook", "hold the end card longer")
is a plan edit and a re-render.

Shape (see skills/meta-video-edit/references/edit-plan-format.md):

{
  "client": "1 TO 360 Strength and Fitness",
  "ad": "AA HOOK 1",
  "concept": "audience_addresser",
  "formats": ["9x16", "4x5"],
  "transcripts_dir": "work/transcripts",
  "brand": {"font": "TikTok Sans", "highlight": "#E4FF3A"},
  "punch_in": 1.08,
  "clips": [
    {"src": "footage/C4862.MP4", "in": 3.2, "out": 9.8, "focus": [0.5, 0.35],
     "zoom": 1.0, "role": "hook", "tighten": true},
    {"card": {"text": "Tap below to book in", "duration": 2.5}}
  ],
  "broll": [{"src": "footage/C4901.MP4", "in": 12.0, "at": 4.2, "dur": 2.4}],
  "titles": [{"text": "Women 40 to 55 in South Ken", "start": 0, "end": 2.8, "style": "hook"}],
  "captions": {"on": true, "fixes": {"free": "three"}},
  "music": {"src": "music/track.mp3", "gain_db": -22, "duck": true}
}
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field

from . import specs, transcribe


@dataclass
class Piece:
    """One continuous run of source footage on the output timeline."""
    src: str
    t_in: float
    t_out: float
    focus: object = (0.5, 0.5)  # [x, y] or {"9x16": [x, y], "4x5": [x, y]}
    zoom: float = 1.0
    role: str = ""
    mute: bool = False
    card: dict | None = None
    words: list = field(default_factory=list)  # output-timeline words

    @property
    def dur(self) -> float:
        if self.card:
            return float(self.card.get("duration", 2.5))
        return max(0.0, self.t_out - self.t_in)


def load(path: str) -> dict:
    with open(path) as f:
        plan = json.load(f)
    plan["_path"] = os.path.abspath(path)
    plan["_base"] = os.path.dirname(plan["_path"])
    return plan


def resolve(plan: dict, p: str) -> str:
    if not p:
        return p
    p = os.path.expanduser(p)
    return p if os.path.isabs(p) else os.path.normpath(os.path.join(plan.get("_base", "."), p))


def check(plan: dict) -> list:
    """Structural problems with a plan, as strings. Empty list means it can render."""
    errs = []
    for k in ("client", "ad", "clips"):
        if not plan.get(k):
            errs.append(f"plan is missing '{k}'")
    for fmt in plan.get("formats", ["9x16", "4x5"]):
        if fmt not in specs.FORMATS:
            errs.append(f"unknown format {fmt}")
    for i, c in enumerate(plan.get("clips", [])):
        if "card" in c:
            ca = c["card"].get("audio")
            if ca and not os.path.exists(resolve(plan, ca.get("src", ""))):
                errs.append(f"clip {i}: card audio not found: {ca.get('src')}")
            continue
        src = resolve(plan, c.get("src", ""))
        if not src or not os.path.exists(src):
            errs.append(f"clip {i}: source not found: {c.get('src')}")
        if c.get("out") is not None and c.get("in") is not None and c["out"] <= c["in"]:
            errs.append(f"clip {i}: out ({c['out']}) is not after in ({c['in']})")
    for i, b in enumerate(plan.get("broll", [])):
        if not os.path.exists(resolve(plan, b.get("src", ""))):
            errs.append(f"broll {i}: source not found: {b.get('src')}")
    m = plan.get("music")
    if m and not os.path.exists(resolve(plan, m.get("src", ""))):
        errs.append(f"music source not found: {m.get('src')}")
    return errs


def clip_words(plan: dict, clip: dict) -> list:
    """Source-time words for a clip, from its words file or the transcripts folder."""
    if isinstance(clip.get("words"), list):
        return clip["words"]
    wp = clip.get("words")
    if wp:
        wp = resolve(plan, wp)
    else:
        tdir = resolve(plan, plan.get("transcripts_dir", "")) or None
        wp = transcribe.words_path(resolve(plan, clip["src"]), tdir)
    if os.path.exists(wp):
        with open(wp) as f:
            return json.load(f).get("words", [])
    return []


def _is_filler(w: dict) -> bool:
    return w["w"].lower().strip(specs.PUNCT) in specs.FILLER_WORDS


def tighten(words: list, t_in: float, t_out: float, gap: float = specs.TIGHTEN_GAP,
            pad: float = specs.TIGHTEN_PAD, drop_fillers: bool = True) -> list:
    """Split [t_in, t_out] into spans that keep the speech and cut the dead air.

    Pauses longer than `gap` between words are removed (a jump cut), fillers
    (um, erm) are dropped, and the head and tail are trimmed to the speech.
    Returns a list of (in, out) in source time.
    """
    ws = [w for w in words if w["start"] >= t_in - 0.05 and w["end"] <= t_out + 0.05]
    if drop_fillers:
        ws = [w for w in ws if not _is_filler(w)]
    if not ws:
        return [(t_in, t_out)]
    spans = []
    s = max(t_in, ws[0]["start"] - pad)
    for a, b in zip(ws, ws[1:]):
        if b["start"] - a["end"] > gap:
            spans.append((s, min(a["end"] + pad, t_out)))
            s = max(b["start"] - pad, t_in)
    spans.append((s, min(ws[-1]["end"] + pad + 0.06, t_out)))
    merged = []
    for a, b in spans:
        if merged and a - merged[-1][1] < 0.04:
            merged[-1] = (merged[-1][0], b)
        else:
            merged.append((a, b))
    return [(round(a, 3), round(b, 3)) for a, b in merged if b - a > 0.12]


_ENV = {}


def envelope(src: str, hop: float = 0.02):
    """Audio level in dB per 20 ms frame, cached per source (and on disk beside the transcripts)."""
    if src in _ENV:
        return _ENV[src]
    import numpy as np
    from . import tools
    a = tools.audio_array(src, sr=16000)
    n = int(16000 * hop)
    frames = len(a) // n
    rms = np.sqrt(np.mean(a[: frames * n].reshape(frames, n) ** 2, axis=1) + 1e-12)
    db = 20 * np.log10(rms + 1e-9)
    _ENV[src] = (db, hop)
    return _ENV[src]


def split_on_silence(src: str, spans: list, gap: float = specs.TIGHTEN_GAP, pad: float = specs.TIGHTEN_PAD) -> list:
    """Cut silent runs inside spans using the audio itself.

    Whisper stretches a word over the pause that follows it, so word gaps miss
    many pauses. Speech level is taken from the loud frames of the span; a run
    more than 24 dB under it for longer than `gap` is cut, keeping `pad`.
    """
    import numpy as np
    db, hop = envelope(src)
    out = []
    for a, b in spans:
        i0, i1 = int(a / hop), max(int(a / hop) + 1, int(b / hop))
        seg = db[i0:i1]
        if len(seg) < 3:
            out.append((a, b))
            continue
        speech = np.percentile(seg, 90)
        quiet = seg < speech - 24
        start = a
        k = 0
        while k < len(seg):
            if quiet[k]:
                j = k
                while j < len(seg) and quiet[j]:
                    j += 1
                ta, tb = a + k * hop, a + j * hop
                if tb - ta > gap and ta > a + 0.05 and tb < b - 0.05:
                    out.append((start, ta + pad))
                    start = tb - pad
                k = j
            else:
                k += 1
        out.append((start, b))
    return [(round(x, 3), round(y, 3)) for x, y in out if y - x > 0.12]


def snap_edges(src: str, spans: list, reach: float = 0.10) -> list:
    """Move every cut point to the quietest 20 ms frame within `reach`, so cuts land
    between sounds and never on half a syllable."""
    import numpy as np
    db, hop = envelope(src)

    def quiet(t):
        i0, i1 = max(0, int((t - reach) / hop)), min(len(db), int((t + reach) / hop) + 1)
        if i1 <= i0:
            return t
        k = int(np.argmin(db[i0:i1]))
        return (i0 + k) * hop + hop / 2

    out = [(quiet(a), quiet(b)) for a, b in spans]
    return [(round(a, 3), round(b, 3)) for a, b in out if b - a > 0.12]


def timeline(plan: dict) -> list:
    """Expand the plan's clips into Pieces on the output timeline, with words mapped across."""
    pieces = []
    t = 0.0
    punch = float(plan.get("punch_in", 0) or 0)
    fixes = {k.lower(): v for k, v in (plan.get("captions", {}).get("fixes") or {}).items()}
    for clip in plan.get("clips", []):
        if "card" in clip:
            p = Piece(src="", t_in=0, t_out=0, card=clip["card"], role=clip.get("role", "cta"))
            pieces.append(p)
            t += p.dur
            continue
        src = resolve(plan, clip["src"])
        words = clip_words(plan, clip)
        t_in = float(clip.get("in", 0))
        t_out = float(clip["out"]) if clip.get("out") is not None else None
        if t_out is None:
            from . import tools
            t_out = tools.probe(src).duration
        spans = tighten(words, t_in, t_out) if clip.get("tighten") and words else [(t_in, t_out)]
        if clip.get("tighten") and plan.get("audio_tighten", True):
            try:
                spans = split_on_silence(src, spans)
                spans = snap_edges(src, spans)
            except Exception:
                pass  # no audio or undecodable: keep the word-based spans
        base_zoom = float(clip.get("zoom", 1.0))
        # each word goes to the span it overlaps most (whisper stretches words over
        # pauses, so a word can straddle a cut); words outside every span are dropped
        best = {}
        for wi, w in enumerate(words):
            # a word belongs to this clip only if it starts inside it: whisper stretches a
            # word over the pause after it, so its sound is at its start, not its end
            if w["start"] < t_in - 0.03 or w["start"] > t_out - 0.08:
                continue
            ov = [(min(b, w["end"]) - max(a, w["start"]), j) for j, (a, b) in enumerate(spans)]
            o, j = max(ov) if ov else (0, -1)
            if o >= min(0.03, 0.5 * (w["end"] - w["start"])):
                best[wi] = j
        for j, (a, b) in enumerate(spans):
            z = base_zoom * (punch if (punch and j % 2 == 1) else 1.0)
            p = Piece(src=src, t_in=a, t_out=b, focus=clip.get("focus", (0.5, 0.5)),
                      zoom=z, role=clip.get("role", ""), mute=bool(clip.get("mute")))
            for wi, w in enumerate(words):
                if best.get(wi) == j and not (clip.get("tighten") and _is_filler(w)):
                    txt = fixes.get(w["w"].lower().strip(specs.PUNCT), None)
                    word = dict(w)
                    if txt is not None:
                        trail = w["w"][len(w["w"].rstrip(specs.PUNCT)):]
                        word["w"] = txt + trail
                    word["start"] = round(max(0.0, w["start"] - a) + t, 3)
                    word["end"] = round(max(min(b - a, w["end"] - a), max(0.0, w["start"] - a) + 0.05) + t, 3)
                    p.words.append(word)
            pieces.append(p)
            t += p.dur
        if clip.get("cap_first"):
            first = next((pc for pc in pieces[len(pieces) - len(spans):] if pc.words), None)
            if first:
                w0 = first.words[0]["w"]
                first.words[0]["w"] = w0[:1].upper() + w0[1:]
    for pc in pieces:
        for w in pc.words:
            low = w["w"].lower()
            if low.rstrip(specs.PUNCT) in ("i", "i'm", "i've", "i'll", "i'd"):
                w["w"] = "I" + w["w"][1:]
    return pieces


def duration(pieces: list) -> float:
    return round(sum(p.dur for p in pieces), 3)


def all_words(pieces: list) -> list:
    return [w for p in pieces for w in p.words]


def save(plan: dict, path: str) -> None:
    clean = {k: v for k, v in plan.items() if not k.startswith("_")}
    with open(path, "w") as f:
        json.dump(clean, f, indent=2)
