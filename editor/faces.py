"""
Face boxes, so captions can move around the frame without ever covering a face.

The largest frontal face in a source frame is found with OpenCV's Haar cascade
(fast, no model download) and returned as fractions of the source frame. The
crop maths (`crop`) is shared with the renderer, so the box can be mapped into
the finished frame exactly where the viewer sees it.
"""

from __future__ import annotations

import functools

from . import specs, tools


@functools.lru_cache(maxsize=512)
def detect(src: str, t: float):
    """(x0, y0, x1, y1) of the largest face as fractions of the source frame, or None."""
    try:
        import cv2  # type: ignore
    except ImportError:
        return None
    try:
        g = tools.frame_gray(src, t, width=480)
    except tools.EditError:
        return None
    casc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    h, w = g.shape
    found = casc.detectMultiScale(g, scaleFactor=1.08, minNeighbors=6, minSize=(int(w * 0.08), int(w * 0.08)))
    if len(found) == 0:
        return None
    x, y, fw, fh = max(found, key=lambda r: r[2] * r[3])
    # the cascade box sits on brow-to-mouth; extend to hair and chin
    y0 = max(0.0, (y - fh * 0.30) / h)
    y1 = min(1.0, (y + fh * 1.18) / h)
    x0 = max(0.0, (x - fw * 0.06) / w)
    x1 = min(1.0, (x + fw * 1.06) / w)
    return (x0, y0, x1, y1)


def crop(W, H, sw, sh, zoom, fx, fy, fmt="9x16", layout="center"):
    """The renderer's crop: returns (scaled_w, scaled_h, crop_x, crop_y)."""
    from .render import LAYOUT_FRAME
    lx, lz = LAYOUT_FRAME.get(layout, (0.5, 1.0))
    s = max(W / sw, H / sh) * zoom * lz
    zw, zh = int(round(sw * s / 2) * 2), int(round(sh * s / 2) * 2)
    _, ty = specs.EYE_LINE.get(fmt, (0.5, 0.36))
    cx = min(max(fx * zw - lx * W, 0), zw - W)
    cy = min(max(fy * zh - ty * H, 0), zh - H)
    return zw, zh, int(cx), int(cy)


def to_frame(box, geo, W, H):
    """Map a source-fraction box into finished-frame pixels."""
    zw, zh, cx, cy = geo
    x0, y0, x1, y1 = box
    return (max(0, x0 * zw - cx), max(0, y0 * zh - cy), min(W, x1 * zw - cx), min(H, y1 * zh - cy))


def to_source(box_px, geo):
    """Map a finished-frame pixel box back to source fractions (for sampling brightness)."""
    zw, zh, cx, cy = geo
    x0, y0, x1, y1 = box_px
    return ((x0 + cx) / zw, (y0 + cy) / zh, (x1 + cx) / zw, (y1 + cy) / zh)


def brightness(src: str, t: float, frac_box) -> float:
    """Mean luminance (0 to 255) of a source-fraction box: can white type sit there?"""
    try:
        g = tools.frame_gray(src, t, width=160)
    except tools.EditError:
        return 128.0
    h, w = g.shape
    x0, y0, x1, y1 = frac_box
    a, b = max(0, int(y0 * h)), min(h, max(int(y0 * h) + 1, int(y1 * h)))
    c, d = max(0, int(x0 * w)), min(w, max(int(x0 * w) + 1, int(x1 * w)))
    return float(g[a:b, c:d].mean())


def focus_for(piece, fmt: str = "9x16"):
    """The eye point for a piece: the plan's focus, or from the detected face when the plan says "auto"."""
    f = piece.focus
    if isinstance(f, dict):
        f = f.get(fmt) or f.get("default") or "auto"
    if f == "auto" or f is None:
        box = detect(piece.src, round((piece.t_in + piece.t_out) / 2, 1))
        if box:
            x0, y0, x1, y1 = box
            return ((x0 + x1) / 2, y0 + (y1 - y0) * 0.45)
        return (0.5, 0.35)
    return (float(f[0]), float(f[1]))
