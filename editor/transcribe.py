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
        audio, path_or_hf_repo=model, word_timestamps=True, initial_prompt=prompt,
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
