"""Evals for the statics arm: the export script and the static design standard."""

from __future__ import annotations

import os
import tempfile


def run_static_evals() -> list:
    failures = []
    try:
        from PIL import Image
    except ImportError:
        print("  (Pillow not installed, static export evals skipped)")
        return failures
    from design.export_statics import export, placement, ExportError

    # placement from names
    for name, want in [("01 OFFER BIG TYPE 4x5", "4x5"), ("12 MEET THE COACH 9x16", "9x16"), ("CAROUSEL 1 COVER", "1x1")]:
        if placement(name) != want:
            failures.append(f"static export: '{name}' read as {placement(name)}, want {want}")
    try:
        placement("05 BENEFIT")
        failures.append("static export: a name without a size should be refused")
    except ExportError:
        pass

    with tempfile.TemporaryDirectory() as td:
        src = os.path.join(td, "png"); os.makedirs(src)
        Image.new("RGB", (2160, 2700), (200, 100, 70)).save(os.path.join(src, "01 OFFER 4x5.png"))
        Image.new("RGB", (2160, 3840), (20, 20, 20)).save(os.path.join(src, "01 OFFER 9x16.png"))
        Image.new("RGB", (2160, 2160), (240, 240, 230)).save(os.path.join(src, "CAROUSEL 1 COVER.png"))
        files = export(src, td, "TEST", "Jan-01")
        want = {"4x5 Feed/TEST 01 OFFER 4x5.jpg": (1080, 1350),
                "9x16 Stories and Reels/TEST 01 OFFER 9x16.jpg": (1080, 1920),
                "1x1 Carousel (upload in order)/TEST CAROUSEL 1 COVER.jpg": (1080, 1080)}
        root = os.path.join(td, "STATICS FINAL JPG (Jan-01)")
        for rel, size in want.items():
            p = os.path.join(root, rel)
            if not os.path.exists(p):
                failures.append(f"static export: missing {rel}")
                continue
            im = Image.open(p)
            if im.size != size or im.format != "JPEG":
                failures.append(f"static export: {rel} is {im.format} {im.size}, want JPEG {size}")
        if len(files) != 3:
            failures.append(f"static export: wrote {len(files)} files, want 3")
        # wrong aspect and 1x exports are refused
        bad = os.path.join(td, "bad"); os.makedirs(bad)
        Image.new("RGB", (2160, 2160), 0).save(os.path.join(bad, "02 WRONG 4x5.png"))
        try:
            export(bad, td, "TEST", "Jan-01")
            failures.append("static export: a square PNG named 4x5 should be refused")
        except ExportError:
            pass
        small = os.path.join(td, "small"); os.makedirs(small)
        Image.new("RGB", (540, 675), 0).save(os.path.join(small, "03 SMALL 4x5.png"))
        try:
            export(small, td, "TEST", "Jan-01")
            failures.append("static export: an undersized PNG should be refused")
        except ExportError:
            pass

    # the standard keeps the rules Liam signed off
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    std = open(os.path.join(here, "skills/meta-static-design/references/static-design-standard.md")).read()
    for must in ["about 60%", "soft shadow", "No label kickers", "No icon bullets", "One photo per ad",
                 "actually coaching", "3px rule", "quality 95"]:
        if must not in std:
            failures.append(f"static standard: missing '{must}'")
    return failures
