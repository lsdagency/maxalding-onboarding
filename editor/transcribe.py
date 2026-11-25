"""
Word-level transcription for raw footage (mlx-whisper on Apple Silicon).

Output JSON, saved next to the edit work as <clip>.words.json:
    {"source": path, "model": "<model>", "duration": s,
     "words": [{"w": "Four", "start": 1.02, "end": 1.31, "p": 0.97}],
     "text": "full transcript"}

Captions and tightening both run off these word timings, so the transcript
must be checked by eye before captions ship. Whisper mishears offer words
(it heard Sergio's "three" as "free"), so pass the client's offer and
vocabulary as the prompt, and fix what is left in the plan's caption fixes.
"""

from __future__ import annotations

import json
import os

from . import tools

DEFAULT_MODEL = os.environ.get("MAXALDING_WHISPER_MODEL", "mlx-community/whisper-large-v3-turbo")


# Whisper drops fillers and false starts unless the prompt shows it some. A verbatim
# transcript is what lets the edit cut around "uh, the private, the..." instead of
# starting a hook on it (Liam, 2026-11-25: "still a stutter at the start").
VERBATIM = "Umm, uh, so, I mean, like, you know, erm, the, the."


def transcribe(path: str, prompt: str | None = None, model: str = DEFAULT_MODEL, language: str = "en") -> dict:
    try:
        import mlx_whisper  # type: ignore
    except ImportError as e:
        raise tools.EditError("mlx_whisper is not installed (pip install mlx-whisper).") from e
    info = tools.probe(path)
    if not info.has_audio:
        return {"source": path, "model": model, "duration": info.duration, "words": [], "text": ""}
    audio = tools.audio_array(path)
    res = mlx_whisper.transcribe(
        audio, path_or_hf_repo=model, word_timestamps=True, initial_prompt=(VERBATIM + " " + (prompt or "")).strip(),
        language=language, condition_on_previous_text=False,
        hallucination_silence_threshold=2.0,
    )
    words = []
    for seg in res.get("segments", []):
        for w in seg.get("words", []):
            txt = w.get("word", "").strip()
            if txt:
                words.append({"w": txt, "start": round(float(w["start"]), 3),
                              "end": round(float(w["end"]), 3), "p": round(float(w.get("probability", 1)), 3)})
    return {"source": os.path.abspath(path), "model": model, "duration": info.duration,
            "words": words, "text": " ".join(x["w"] for x in words)}


def words_path(src: str, work_dir: str | None = None) -> str:
    base = os.path.splitext(os.path.basename(src))[0] + ".words.json"
    return os.path.join(work_dir or os.path.dirname(src), base)


def load_or_transcribe(src: str, work_dir: str | None = None, prompt: str | None = None) -> dict:
    wp = words_path(src, work_dir)
    if os.path.exists(wp):
        with open(wp) as f:
            return json.load(f)
    data = transcribe(src, prompt=prompt)
    os.makedirs(os.path.dirname(wp) or ".", exist_ok=True)
    with open(wp, "w") as f:
        json.dump(data, f, indent=1)
    return data


def low_confidence(words: list, threshold: float = 0.6) -> list:
    """Words the model was unsure of. Check every one against the footage before captions ship."""
    return [w for w in words if w.get("p", 1) < threshold]


def refine(src: str, t0: float, t1: float, work_dir: str | None = None, prompt: str | None = None,
           model: str = DEFAULT_MODEL) -> list:
    """Re-transcribe one short span on its own and patch it into the clip's words file.

    Whole-file transcripts smear word timings around false starts and fillers (the
    "uh, the private, the personal" at the top of Gianluigi's hook came out as one
    stretched "personal"). A short span transcribed alone, verbatim, times them
    properly. Run it on every span an edit actually uses. Returns the new words.
    """
    import mlx_whisper  # type: ignore
    a = tools.audio_array(src)
    seg = a[int(t0 * 16000):int(t1 * 16000)]
    r = mlx_whisper.transcribe(seg, path_or_hf_repo=model, word_timestamps=True,
                               initial_prompt=(VERBATIM + " " + (prompt or "")).strip(),
                               language="en", condition_on_previous_text=False)
    new = [{"w": w["word"].strip(), "start": round(float(w["start"]) + t0, 3), "end": round(float(w["end"]) + t0, 3),
            "p": round(float(w.get("probability", 1)), 3)}
           for sg in r.get("segments", []) for w in sg.get("words", []) if w["word"].strip()]
    wp = words_path(src, work_dir)
    with open(wp) as f:
        data = json.load(f)
    # keep words outside the span, and inside it only from the refined pass (trim the
    # span edges by a hair so a word cut in half at the boundary is not duplicated)
    lo, hi = t0 + 0.15, t1 - 0.15
    kept = [w for w in data["words"] if w["start"] < lo or w["start"] > hi]
    new = [w for w in new if lo <= w["start"] <= hi]
    data["words"] = sorted(kept + new, key=lambda w: w["start"])
    data["text"] = " ".join(w["w"] for w in data["words"])
    data.setdefault("refined", []).append([t0, t1])
    with open(wp, "w") as f:
        json.dump(data, f, indent=1)
    return new
