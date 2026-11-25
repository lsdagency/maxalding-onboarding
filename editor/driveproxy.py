"""
A local relay between ffmpeg and Google Drive that only ever asks Drive for
bounded byte ranges.

Drive's anonymous quota blocks open-ended requests ("Range: bytes=N-") on a busy
file with a "Quota exceeded" page, but still serves bounded ranges
("bytes=N-M"). ffmpeg always asks open-ended, so it reads through this relay:
each request is answered with one bounded chunk (206, Content-Range), and ffmpeg
reconnects for the next chunk as it reads on.

    python -m editor.driveproxy            # serves on 127.0.0.1:8765
    ffmpeg -reconnect 1 -reconnect_at_eof 1 -i http://127.0.0.1:8765/<drive file id>
"""

from __future__ import annotations

import http.server
import os
import re
import time
import socketserver
import threading
import urllib.request

CHUNK = 8 * 1024 * 1024
PORT = 8765
_SIZES: dict = {}


def _drive(file_id: str) -> str:
    return f"https://drive.usercontent.google.com/download?id={file_id}&export=download&confirm=t"


CACHE = os.path.expanduser("~/.cache/maxalding/drive")


SUB = 2 * 1024 * 1024  # Drive's quota page kicks in above ~2 MB per request on a busy file


def _fetch_raw(file_id: str, start: int, end: int):
    """A bounded range, fetched as requests of at most SUB bytes."""
    if end - start + 1 <= SUB:
        return _fetch_one(file_id, start, end)
    parts = []
    pos = start
    while pos <= end:
        stop = min(end, pos + SUB - 1)
        parts.append(_fetch_one(file_id, pos, stop))
        pos = stop + 1
    return b"".join(parts)


def _fetch_one(file_id: str, start: int, end: int):
    """One bounded range from Drive, retried with back-off when Drive answers with a page
    (its quota or virus-scan HTML) instead of the video bytes."""
    delay = 2.0
    last = None
    for _ in range(8):
        try:
            req = urllib.request.Request(_drive(file_id), headers={"Range": f"bytes={start}-{end}",
                                                                   "User-Agent": "curl/8.4.0"})
            with urllib.request.urlopen(req, timeout=180) as r:
                ctype = r.headers.get("Content-Type", "")
                cr = r.headers.get("Content-Range", "")
                data = r.read()
                m = re.search(r"/(\d+)$", cr)
                if r.status == 206 and "html" not in ctype and m:
                    _SIZES[file_id] = int(m.group(1))
                    return data
                last = f"{r.status} {ctype}"
        except Exception as e:  # network drop: try again
            last = repr(e)
        time.sleep(delay)
        delay = min(delay * 2, 60)
    raise IOError(f"Drive would not serve {file_id} bytes {start}-{end}: {last}")


def _chunk(file_id: str, idx: int) -> bytes:
    """Chunk idx (CHUNK-aligned) of a file, from the disk cache or Drive."""
    path = os.path.join(CACHE, file_id, f"{idx}.bin")
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f.read()
    start = idx * CHUNK
    size = _SIZES.get(file_id)
    end = start + CHUNK - 1 if size is None else min(size - 1, start + CHUNK - 1)
    data = _fetch_raw(file_id, start, end)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".part"
    with open(tmp, "wb") as f:
        f.write(data)
    os.replace(tmp, path)
    return data


def _size(file_id: str) -> int:
    if file_id not in _SIZES:
        meta = os.path.join(CACHE, file_id, "size")
        if os.path.exists(meta):
            _SIZES[file_id] = int(open(meta).read())
        else:
            _fetch_raw(file_id, 0, 0)
            os.makedirs(os.path.dirname(meta), exist_ok=True)
            with open(meta, "w") as f:
                f.write(str(_SIZES[file_id]))
    return _SIZES[file_id]


def prefetch(file_id: str, patience: int = 20) -> int:
    """Pull every chunk of a (small) Drive file into the disk cache before rendering, so
    the render never waits on Drive. Each chunk gets `patience` rounds of retries.
    Returns the number of chunks now cached."""
    size = _size(file_id)
    n = (size + CHUNK - 1) // CHUNK
    for idx in range(n):
        for attempt in range(patience):
            try:
                _chunk(file_id, idx)
                break
            except IOError:
                time.sleep(min(60, 5 * (attempt + 1)))
    return sum(1 for i in range(n) if os.path.exists(os.path.join(CACHE, file_id, f"{i}.bin")))


class Handler(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *a):
        pass

    def _serve(self, head_only=False):
        file_id = self.path.strip("/").split("?")[0]
        rng = self.headers.get("Range", "bytes=0-")
        m = re.match(r"bytes=(\d+)-(\d*)", rng)
        start = int(m.group(1)) if m else 0
        want_end = int(m.group(2)) if m and m.group(2) else None
        size = _size(file_id)
        if start >= size:
            self.send_response(416)
            self.send_header("Content-Range", f"bytes */{size}")
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        idx = start // CHUNK
        data = b"" if head_only else _chunk(file_id, idx)
        off = start - idx * CHUNK
        chunk_end = min(size - 1, idx * CHUNK + CHUNK - 1)
        end = chunk_end if want_end is None else min(chunk_end, want_end)
        body = data[off:off + (end - start + 1)]
        self.send_response(206)
        self.send_header("Content-Type", "video/mp4")
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.send_header("Content-Length", str(end - start + 1))
        self.end_headers()
        if not head_only:
            self.wfile.write(body)

    def do_GET(self):
        try:
            self._serve()
        except (BrokenPipeError, ConnectionResetError):
            pass

    def do_HEAD(self):
        self._serve(head_only=True)


class Server(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


_server = None


def ensure_running(port: int = PORT) -> str:
    """Start the relay in a background thread if it isn't running; return its base URL."""
    global _server
    if _server is None:
        try:
            _server = Server(("127.0.0.1", port), Handler)
            threading.Thread(target=_server.serve_forever, daemon=True).start()
        except OSError:
            pass  # already running in another process
    return f"http://127.0.0.1:{port}"


if __name__ == "__main__":
    print("Drive relay on", ensure_running())
    threading.Event().wait()
