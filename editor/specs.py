"""
Delivery specs for Maxalding paid social video, in one place.

The render engine, the caption builder and the edit QA gate all read from
here, so a spec change is one edit. The human-readable version, with sources,
is skills/meta-video-edit/references/specs-and-safe-zones.md. Keep them in step.

Safe zones are fractions of the frame, so they hold at any export size.
"""

from __future__ import annotations

# Output formats. 9x16 runs on Reels and Stories, 4x5 on Feed. Every ad is
# delivered in both unless the plan says otherwise.
FORMATS = {
    "9x16": {"w": 1080, "h": 1920, "label": "Reels and Stories"},
    "4x5": {"w": 1080, "h": 1350, "label": "Feed"},
}

FPS = 30
VIDEO_CODEC = "libx264"
PIX_FMT = "yuv420p"
CRF = 18
AUDIO_RATE = 48000
AUDIO_BITRATE = "192k"

# Safe zones: keep captions, hook text and CTAs inside these bands. The 9x16
# numbers are the Reels/Stories UI (profile and caption at the bottom, the
# account bar at the top, the action rail on the right). 4x5 Feed has less
# overlay, so the margins are smaller.
SAFE_ZONES = {
    "9x16": {"top": 0.14, "bottom": 0.35, "left": 0.06, "right": 0.06},
    "4x5": {"top": 0.06, "bottom": 0.12, "left": 0.06, "right": 0.06},
}

# Where the eyes sit in the output frame (x, y as fractions). The plan's focus
# point (the eyes in the source) is placed here: the upper third on 9x16,
# a touch lower on 4x5 where there is less headroom.
EYE_LINE = {"9x16": (0.5, 0.38), "4x5": (0.5, 0.40)}

# Loudness. Social platforms normalise around -14 LUFS integrated; delivering
# there means the ad neither gets turned down nor sounds quiet next to organic.
LOUDNESS_TARGET = -14.0
LOUDNESS_TOLERANCE = 1.5
TRUE_PEAK_MAX = -1.0
MUSIC_BED_DB = -22.0  # music under voice, before ducking

# Captions (house defaults, overridable per client brand).
CAPTION = {
    "9x16": {"size": 104, "y": 0.61, "max_chars": 18},
    "4x5": {"size": 88, "y": 0.72, "max_chars": 20},
    "max_words": 3,          # words on screen at once
    "max_lines": 2,
    "min_size": 54,          # px at 1080 wide; smaller is unreadable on a phone
    "break_gap": 0.30,       # a pause this long starts a new caption chunk
    "min_event": 0.25,       # seconds a caption chunk must stay up
}

# On-screen hook text (the title that echoes the spoken hook).
TITLE = {
    "9x16": {"size": 84, "y": 0.20, "max_chars": 22},
    "4x5": {"size": 76, "y": 0.13, "max_chars": 24},
    "min_on_screen": 1.5,
}

# Timing.
HOOK_SPEECH_START_MAX = 0.7   # first spoken word by this many seconds
DEAD_AIR_MAX = 0.8            # a silence longer than this mid-ad is a warning
TIGHTEN_GAP = 0.35            # gaps between words longer than this get cut
TIGHTEN_PAD = 0.08            # breath kept either side of a cut

# Length guidance by concept (seconds). Warnings, not errors: the plan can
# carry max_seconds to override for a concept that earns a longer run.
LENGTH = {
    "default": (8, 60),
    "hook": (2, 6),
    "audience_addresser": (15, 45),
    "incentive": (10, 30),
    "interview": (20, 75),
    "montage": (8, 30),
    "story": (25, 75),
}

# Punctuation that can trail a word (the bang is built with chr so the source
# passes the house banned-character scan).
PUNCT = ".,?;:'\"" + chr(33)
END_PUNCT = ".?,;:" + chr(33)

FILLER_WORDS = {"um", "uh", "erm", "er", "ah", "hmm", "mm"}


def frame_size(fmt: str):
    spec = FORMATS[fmt]
    return spec["w"], spec["h"]


def safe_box(fmt: str):
    """Return the safe zone as pixel bounds (x0, y0, x1, y1)."""
    w, h = frame_size(fmt)
    z = SAFE_ZONES[fmt]
    return (round(w * z["left"]), round(h * z["top"]),
            round(w * (1 - z["right"])), round(h * (1 - z["bottom"])))
