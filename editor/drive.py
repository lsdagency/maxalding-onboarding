"""
Footage straight from Google Drive, without downloading whole camera files.

Drive serves byte ranges, so ffmpeg can jump into a 4K file and read only the
seconds an edit uses. Plans name a Drive clip as "drive:<file id>"; the file
(or its folder) must be shared "anyone with the link can view". Reads are slow
per request (each jump is a fresh request), so:
  - logging a shoot uses Drive's own thumbnails first (one small image per clip),
    then samples a few frames only from the clips worth a closer look;
  - previews read each used span once into the local span cache (render.proxies);
  - the final render pulls only the seconds in the cut from the 4K originals.

For private folders, mount Drive with rclone (read-only) and use local paths.
"""

from __future__ import annotations

import concurrent.futures as cf
import json
import os
import subprocess


def url(file_id: str) -> str:
    """Read through the local relay, which only asks Drive for bounded ranges (Drive's
    anonymous quota blocks open-ended range requests on busy files)."""
    from .driveproxy import ensure_running
    return f"{ensure_running()}/{file_id}"


def direct_url(file_id: str) -> str:
    return f"https://drive.usercontent.google.com/download?id={file_id}&export=download&confirm=t"


def thumbnail_url(file_id: str, width: int = 320) -> str:
    return f"https://drive.google.com/thumbnail?id={file_id}&sz=w{width}"


def thumbnails(files: list, out_dir: str, width: int = 320, workers: int = 12) -> list:
    """Fetch Drive's thumbnail for each {"name", "id"} file. Returns local paths."""
    os.makedirs(out_dir, exist_ok=True)

    def get(f):
        out = os.path.join(out_dir, os.path.splitext(f["name"])[0] + ".jpg")
        if not os.path.exists(out):
            subprocess.run(["curl", "-s", "-L", "-o", out, thumbnail_url(f["id"], width)], timeout=120)
        return out

    with cf.ThreadPoolExecutor(workers) as ex:
        return list(ex.map(get, files))


def sample_frames(files: list, out_dir: str, fracs=(0.2, 0.5, 0.8), bitrate_bps: float = 211e6,
                  workers: int = 8) -> dict:
    """A few frames from each Drive clip (read by range request). Duration is estimated from
    file size and bitrate so no slow probe is needed. Returns {name: [paths]}."""
    from . import tools
    os.makedirs(out_dir, exist_ok=True)
    ff = tools.ffmpeg()

    def job(args):
        f, frac = args
        dur = f["size"] * 8 / bitrate_bps
        out = os.path.join(out_dir, f"{os.path.splitext(f['name'])[0]}_{int(frac * 100)}.jpg")
        if not os.path.exists(out):
            subprocess.run([ff, "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{max(0.5, dur * frac):.2f}",
                            ] + tools.RECONNECT + ["-i", url(f["id"]), "-frames:v", "1", "-vf", "scale=240:-2", out], timeout=900)
        return f["name"], out

    res: dict = {}
    with cf.ThreadPoolExecutor(workers) as ex:
        for name, path in ex.map(job, [(f, fr) for f in files for fr in fracs]):
            res.setdefault(name, []).append(path)
    return res


def save_index(files: list, path: str) -> None:
    with open(path, "w") as f:
        json.dump(files, f, indent=1)
