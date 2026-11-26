"""
Turn Figma 2x PNG exports into final Meta static JPGs, foldered by placement.

    python -m design.export_statics "<png folder>" "<campaign folder>" --client 1TO360 [--date Nov-26]

PNG names: "<NN> <CONCEPT> <4x5|9x16>.png" or "CAROUSEL <n> <CARD>.png".
Output: <campaign>/STATICS FINAL JPG (<Mon-DD>)/ with "4x5 Feed", "9x16 Stories and Reels" and
"1x1 Carousel (upload in order)"; every file 1080 wide, Lanczos-downscaled, JPG quality 95,
full chroma, named "<CLIENT> <PNG name>.jpg". Existing files with the same name are replaced,
so a re-export after a change only needs the changed PNGs.
"""

from __future__ import annotations

import argparse
import datetime
import glob
import os
import sys

FOLDERS = {"4x5": "4x5 Feed", "9x16": "9x16 Stories and Reels", "1x1": "1x1 Carousel (upload in order)"}
SIZES = {"4x5": (1080, 1350), "9x16": (1080, 1920), "1x1": (1080, 1080)}
QUALITY = 95


class ExportError(ValueError):
    pass


def placement(name: str) -> str:
    """The placement a PNG belongs to, from its name."""
    if name.upper().startswith("CAROUSEL"):
        return "1x1"
    last = name.split()[-1] if name.split() else ""
    if last in ("4x5", "9x16"):
        return last
    raise ExportError(f"can't tell the size of '{name}': end the name with 4x5 or 9x16, or start it with CAROUSEL")


def out_dir(campaign: str, date: str | None = None) -> str:
    date = date or datetime.date.today().strftime("%b-%d")
    return os.path.join(campaign, f"STATICS FINAL JPG ({date})")


def export(png_dir: str, campaign: str, client: str, date: str | None = None) -> list:
    """Convert every PNG in png_dir. Returns the written JPG paths."""
    from PIL import Image

    pngs = sorted(glob.glob(os.path.join(png_dir, "*.png")))
    if not pngs:
        raise ExportError(f"no PNGs in {png_dir}")
    root = out_dir(campaign, date)
    written = []
    for path in pngs:
        name = os.path.splitext(os.path.basename(path))[0]
        kind = placement(name)
        w, h = SIZES[kind]
        im = Image.open(path).convert("RGB")
        if abs(im.width / im.height - w / h) > 0.01:
            raise ExportError(f"{name}: {im.width}x{im.height} is not {kind}")
        if im.width < w:
            raise ExportError(f"{name}: {im.width} wide, export at 2x so it is at least {w}")
        if im.size != (w, h):
            im = im.resize((w, h), Image.LANCZOS)
        folder = os.path.join(root, FOLDERS[kind])
        os.makedirs(folder, exist_ok=True)
        dest = os.path.join(folder, f"{client} {name}.jpg")
        im.save(dest, "JPEG", quality=QUALITY, subsampling=0, optimize=True)
        written.append(dest)
    return written


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    ap.add_argument("png_dir")
    ap.add_argument("campaign")
    ap.add_argument("--client", required=True, help="file name prefix, for example 1TO360")
    ap.add_argument("--date", help="folder date, Mon-DD (default today)")
    a = ap.parse_args(argv)
    try:
        files = export(a.png_dir, a.campaign, a.client, a.date)
    except ExportError as e:
        print("export failed:", e)
        return 1
    for f in files:
        print(os.path.relpath(f, a.campaign))
    print(f"{len(files)} JPGs in {out_dir(a.campaign, a.date)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
