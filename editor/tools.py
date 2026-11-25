"""
ffmpeg plumbing: find the binary, probe media, measure loudness and run jobs.

There is no ffprobe on every machine, so probing parses `ffmpeg -i` output.
The binary is found in this order: $FFMPEG, ffmpeg on PATH, the imageio-ffmpeg
bundled binary, the static-ffmpeg package.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from dataclasses import dataclass, field

_FFMPEG = None


class EditError(RuntimeError):
    pass


def ffmpeg() -> str:
    global _FFMPEG
    if _FFMPEG:
        return _FFMPEG
    cands = [os.environ.get("FFMPEG"), shutil.which("ffmpeg")]
    try:
        import imageio_ffmpeg  # type: ignore
        cands.append(imageio_ffmpeg.get_ffmpeg_exe())
    except Exception:
        pass
    try:
        import static_ffmpeg  # type: ignore
        static_ffmpeg.add_paths()
        cands.append(shutil.which("ffmpeg"))
    except Exception:
        pass
    for c in cands:
        if c and os.path.exists(c):
            _FFMPEG = c
            return c
    raise EditError("ffmpeg not found. pip install imageio-ffmpeg, or set FFMPEG to the binary.")


def available() -> bool:
    try:
        ffmpeg()
        return True
    except EditError:
        return False


RECONNECT = ["-reconnect", "1", "-reconnect_at_eof", "1", "-reconnect_delay_max", "2"]


def _with_reconnect(args: list) -> list:
    """Remote inputs read in chunks (see driveproxy), so ffmpeg must reconnect as it reads on."""
    out = []
    for i, a in enumerate(args):
        if a == "-i" and i + 1 < len(args) and is_remote(args[i + 1]):
            out += RECONNECT
        out.append(a)
    return out


def run(args, *, capture=True, check=True) -> subprocess.CompletedProcess:
    cmd = [ffmpeg(), "-hide_banner", "-nostdin"] + _with_reconnect(list(args))
    p = subprocess.run(cmd, capture_output=capture, text=True)
    if check and p.returncode != 0:
        tail = (p.stderr or "")[-3000:]
        raise EditError(f"ffmpeg failed ({p.returncode}):\n{tail}")
    return p


@dataclass
class MediaInfo:
    path: str
    duration: float = 0.0
    width: int = 0
    height: int = 0
    fps: float = 0.0
    vcodec: str = ""
    pix_fmt: str = ""
    rotation: int = 0
    has_audio: bool = False
    acodec: str = ""
    sample_rate: int = 0
    extra: dict = field(default_factory=dict)

    @property
    def display_size(self):
        """Width and height as the viewer sees them (phone footage is often rotated)."""
        if self.rotation in (90, 270, -90, -270):
            return self.height, self.width
        return self.width, self.height

    def to_dict(self):
        d = dict(self.__dict__)
        d["display_w"], d["display_h"] = self.display_size
        return d


def is_remote(path: str) -> bool:
    return isinstance(path, str) and path.startswith(("http://", "https://"))


_PROBE_CACHE_FILE = os.path.expanduser("~/.cache/maxalding/probe.json")


def _probe_cache() -> dict:
    try:
        with open(_PROBE_CACHE_FILE) as f:
            return json.load(f)
    except Exception:
        return {}


def probe(path: str) -> MediaInfo:
    remote = is_remote(path)
    if not remote and not os.path.exists(path):
        raise EditError(f"No such file: {path}")
    if remote:
        # asking Drive for a file's header takes ~25 s; remember the answer
        cached = _probe_cache().get(path)
        if cached:
            info = MediaInfo(path=path)
            info.__dict__.update({k: v for k, v in cached.items() if k in info.__dict__})
            return info
    p = run(["-i", path], check=False)
    err = p.stderr or ""
    info = MediaInfo(path=path)
    m = re.search(r"Duration: (\d+):(\d+):(\d+(?:\.\d+)?)", err)
    if m:
        info.duration = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))
    v = re.search(r"Stream #\S+?: Video: (\w+)[^,\n]*(?:\([^)]*\))*,\s*(\w+)[^\n]*?, (\d{2,5})x(\d{2,5})", err)
    if v:
        info.vcodec, info.pix_fmt = v.group(1), v.group(2)
        info.width, info.height = int(v.group(3)), int(v.group(4))
    f = re.search(r"Video:[^\n]*?, (\d+(?:\.\d+)?) fps", err) or re.search(r"Video:[^\n]*?, (\d+(?:\.\d+)?) tbr", err)
    if f:
        info.fps = float(f.group(1))
    r = re.search(r"rotation of (-?\d+(?:\.\d+)?) degrees", err) or re.search(r"rotate\s*:\s*(-?\d+)", err)
    if r:
        info.rotation = int(float(r.group(1))) % 360
    a = re.search(r"Stream #\S+?: Audio: (\w+)[^\n]*?, (\d+) Hz", err)
    if a:
        info.has_audio = True
        info.acodec, info.sample_rate = a.group(1), int(a.group(2))
    if remote and info.duration:
        c = _probe_cache()
        c[path] = {k: v for k, v in info.__dict__.items() if k != "extra"}
        os.makedirs(os.path.dirname(_PROBE_CACHE_FILE), exist_ok=True)
        with open(_PROBE_CACHE_FILE, "w") as f:
            json.dump(c, f)
    return info


def loudness(path: str) -> dict:
    """Integrated loudness (LUFS), true peak (dBTP) and LRA via loudnorm's analysis pass."""
    p = run(["-i", path, "-vn", "-af", "loudnorm=I=-14:TP=-1:LRA=11:print_format=json", "-f", "null", "-"], check=False)
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", p.stderr or "", re.S)
    if not m:
        return {}
    d = json.loads(m.group(0))
    return {k: float(v) for k, v in d.items() if _isnum(v)} | {"raw": d}


def _isnum(v) -> bool:
    try:
        float(v)
        return True
    except (TypeError, ValueError):
        return False


def detect(path: str, filt: str, pattern: str, audio=False) -> list:
    """Run a detection filter (blackdetect, silencedetect, freezedetect) and return regex matches."""
    args = ["-i", path]
    args += (["-vn", "-af", filt] if audio else ["-an", "-vf", filt])
    args += ["-f", "null", "-"]
    p = run(args, check=False)
    return re.findall(pattern, p.stderr or "")


def silences(path: str, noise_db=-35, min_dur=0.5) -> list:
    out, start = [], None
    for kind, val in detect(path, f"silencedetect=noise={noise_db}dB:d={min_dur}",
                            r"silence_(start|end): (-?\d+(?:\.\d+)?)", audio=True):
        if kind == "start":
            start = float(val)
        elif start is not None:
            out.append((start, float(val)))
            start = None
    if start is not None:
        out.append((start, None))
    return out


def black_frames(path: str, min_dur=0.1) -> list:
    return [(float(a), float(b)) for a, b in detect(
        path, f"blackdetect=d={min_dur}:pix_th=0.10", r"black_start:(\d+(?:\.\d+)?) black_end:(\d+(?:\.\d+)?)")]


def scene_cuts(path: str, threshold=10.0) -> list:
    return [float(t) for t in detect(path, f"scdet=threshold={threshold}", r"lavfi\.scd\.time: (\d+(?:\.\d+)?)")]


def frame_png(path: str, t: float, out: str, width: int = 540) -> str:
    run(["-y", "-ss", f"{t:.3f}", "-i", path, "-frames:v", "1", "-vf", f"scale={width}:-2", out])
    return out


def audio_array(path: str, sr: int = 16000):
    """Decode audio to a mono float32 numpy array (for transcription)."""
    import numpy as np  # local import, only needed for transcription
    cmd = [ffmpeg(), "-hide_banner", "-nostdin", "-i", path, "-vn", "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"]
    p = subprocess.run(cmd, capture_output=True)
    if p.returncode != 0:
        raise EditError(p.stderr.decode(errors="ignore")[-2000:])
    return np.frombuffer(p.stdout, dtype=np.float32).copy()


def frame_gray(path: str, t: float, width: int = 96):
    """One frame as a small greyscale numpy array (rows, cols), upright, for layout decisions."""
    import numpy as np
    info = probe(path)
    w, h = info.display_size
    height = max(2, int(round(width * h / max(w, 1) / 2) * 2))
    cmd = [ffmpeg(), "-hide_banner", "-nostdin", "-ss", f"{t:.2f}"] + (RECONNECT if is_remote(path) else []) + ["-i", path, "-frames:v", "1",
           "-vf", f"scale={width}:{height}", "-f", "rawvideo", "-pix_fmt", "gray", "-"]
    p = subprocess.run(cmd, capture_output=True)
    if p.returncode != 0 or len(p.stdout) < width * height:
        raise EditError("could not read a frame from " + path)
    return np.frombuffer(p.stdout[: width * height], dtype=np.uint8).reshape(height, width)
