"""
Maxalding video edit engine: raw footage to finished Meta ads.

Modules:
    specs       delivery specs, safe zones, loudness, caption sizes (one source)
    tools       ffmpeg plumbing: find, probe, loudness, detection filters
    transcribe  word-level transcripts (mlx-whisper)
    footage     index a footage folder into a log
    plan        the edit plan (EDL) and the timeline it expands to
    captions    captions, hook titles and card text as ASS
    render      plan to finished 9x16 and 4x5 files
    qa          the edit QA gate
    review      contact sheets and first frames for the eye check

The craft and the process live in skills/meta-video-edit. This package only
does what can be made deterministic.
"""

__version__ = "0.43.0"
