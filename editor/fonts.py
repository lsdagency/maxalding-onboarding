"""
Brand fonts for burned-in text.

libass (the caption renderer) cannot pick a weight out of a variable font and
silently falls back to Helvetica when it cannot match the family. That is how
a client's brand font goes missing without anyone noticing. So before every
render the brand font is resolved to a real file, a variable font is cut to a
static instance at the brand weight with the family renamed to the brand
name, and the result goes in a private fonts folder that is the only one the
renderer looks in. After the render the font libass actually used is checked
(fontselect in the log); a fallback is a QA error.
"""

from __future__ import annotations

import os
import re

from . import tools

SEARCH_DIRS = ["~/Library/Fonts", "/Library/Fonts", "/System/Library/Fonts", "/System/Library/Fonts/Supplemental"]
FONT_EXT = (".ttf", ".otf")


def _names(path: str):
    from fontTools.ttLib import TTFont
    try:
        f = TTFont(path, lazy=True, fontNumber=0)
    except Exception:
        return None
    n = f["name"]
    fam = (n.getDebugName(16) or n.getDebugName(1) or "").strip()
    sub = (n.getDebugName(17) or n.getDebugName(2) or "").strip()
    weight = f["OS/2"].usWeightClass if "OS/2" in f else 400
    axes = {a.axisTag: (a.minValue, a.defaultValue, a.maxValue) for a in f["fvar"].axes} if "fvar" in f else {}
    return {"path": path, "family": fam, "sub": sub, "weight": weight, "axes": axes}


def find(family: str, weight: int, extra_dirs=()) -> dict | None:
    """Best file for family+weight: an exact static weight, else a variable font with a wght axis."""
    want = family.lower().replace(" ", "")
    best, best_score = None, None
    for d in list(extra_dirs) + SEARCH_DIRS:
        d = os.path.expanduser(d)
        if not os.path.isdir(d):
            continue
        for f in os.listdir(d):
            if not f.lower().endswith(FONT_EXT):
                continue
            p = os.path.join(d, f)
            meta = _names(p)
            if not meta:
                continue
            fam = meta["family"].lower().replace(" ", "")
            fname = f.lower().replace(" ", "").replace("-", "")
            if not (fam.startswith(want) or fname.startswith(want)):
                continue
            if "wght" in meta["axes"]:
                lo, _, hi = meta["axes"]["wght"]
                score = 0 if lo <= weight <= hi else 500
                score += 1  # a matching static beats a variable instance
            else:
                score = abs(meta["weight"] - weight) * 2 + (50 if "italic" in meta["sub"].lower() else 0)
            if best_score is None or score < best_score:
                best, best_score = meta, score
    return best


def prepare_all(brand: dict, out_dir: str, plan_base: str = ".") -> dict:
    """One static instance per role, each named '<font> <weight>': title (Black),
    caption (Bold), small (Medium, for connecting words) and, when the brand has
    one, accent (the serif italic used on one key word)."""
    out = {"dir": out_dir, "faces": {}}
    base = brand.get("font", "TikTok Sans")
    roles = [("title", base, 900), ("caption", base, 700), ("small", base, 500)]
    if brand.get("accent_font"):
        roles.append(("accent", brand["accent_font"], 600))
    for role, fam, dflt in roles:
        w = int(brand.get(f"{role}_weight", dflt))
        out["faces"][role] = prepare(brand, out_dir, plan_base, weight=w, family_as=f"{fam} {w}", family=fam)
    return out


def prepare(brand: dict, out_dir: str, plan_base: str = ".", weight: int = 900, family_as: str | None = None,
            family: str | None = None) -> dict:
    """Make a fonts folder holding the brand font at `weight` as a static file named `family_as`.

    Returns {"dir", "family", "source", "variable", "file"} or {} if the font cannot
    be found (the render then uses whatever libass falls back to, and QA fails it).
    """
    family = family or brand.get("font", "TikTok Sans")
    os.makedirs(out_dir, exist_ok=True)
    extra = []
    if brand.get("fonts_dir"):
        extra.append(brand["fonts_dir"] if os.path.isabs(brand["fonts_dir"]) else os.path.join(plan_base, brand["fonts_dir"]))
    src = None
    if brand.get("font_file") and family == brand.get("font"):
        ff = brand["font_file"]
        ff = ff if os.path.isabs(ff) else os.path.join(plan_base, ff)
        src = _names(os.path.expanduser(ff))
    src = src or find(family, weight, extra)
    if not src:
        return {}
    from fontTools.ttLib import TTFont
    font = TTFont(src["path"], fontNumber=0)
    variable = "fvar" in font
    if variable:
        from fontTools.varLib import instancer
        loc = {}
        for tag, (lo, dflt, hi) in src["axes"].items():
            if tag == "wght":
                loc[tag] = max(lo, min(hi, weight))
            elif tag == "wdth":
                loc[tag] = max(lo, min(hi, 100))
            elif tag == "opsz":
                loc[tag] = hi  # display size for big on-screen text
            elif tag in ("slnt", "ital"):
                loc[tag] = 0 if lo <= 0 <= hi else dflt
            else:
                loc[tag] = dflt
        font = instancer.instantiateVariableFont(font, loc)
    # Rename so the family is exactly the brand name and the weight is honest.
    name = font["name"]
    for rec in list(name.names):
        if rec.nameID in (1, 2, 4, 6, 16, 17, 21, 22, 25):
            name.removeNames(nameID=rec.nameID)
    alias = family_as or family
    ps = re.sub(r"[^A-Za-z0-9]", "", alias) + "-Brand"
    name.setName(alias, 1, 3, 1, 0x409)
    name.setName("Regular", 2, 3, 1, 0x409)
    name.setName(alias, 4, 3, 1, 0x409)
    name.setName(ps, 6, 3, 1, 0x409)
    if "OS/2" in font:
        font["OS/2"].usWeightClass = 400
        font["OS/2"].fsSelection = (font["OS/2"].fsSelection & ~0b100001) | 0b1000000  # REGULAR bit
    if "head" in font:
        font["head"].macStyle = 0
    out = os.path.join(out_dir, ps + ".ttf")
    font.save(out)
    return {"dir": out_dir, "family": alias, "source": src["path"], "variable": variable, "file": out}


def used_fonts(ass_path: str, fonts_dir: str | None, W: int, H: int, at: float = 0.5) -> list:
    """Ask libass which font file it picks for each requested family (from its fontselect log)."""
    fd = f":fontsdir='{fonts_dir}'" if fonts_dir else ""
    p = tools.run(["-loglevel", "debug", "-f", "lavfi", "-i", f"color=c=gray:s={W}x{H}:d=600",
                   "-vf", f"ass=filename='{ass_path}'{fd}", "-ss", f"{at:.2f}", "-frames:v", "1", "-f", "null", "-"], check=False)
    return re.findall(r"fontselect: \(([^,]+), (\d+), \d+\) -> ([^,]+),", p.stderr or "")
