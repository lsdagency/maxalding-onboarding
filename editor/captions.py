"""
Captions, hook titles and card text as one ASS subtitle file per format.

House caption style (skills/meta-video-edit/references/caption-style.md):
short chunks of up to three words, the word being spoken lit in the brand
highlight colour, bold brand font, white with a dark outline, sat in the
safe zone just below centre. Titles echo the spoken hook in a box at the
top of the safe zone. Everything is positioned with \\pos so the QA gate
can check every event's box against the safe zone.
"""

from __future__ import annotations

from . import specs

DEFAULT_BRAND = {
    # House font for every client, matching the statics (Liam, 2026-11-25):
    # titles, CTA and cards in TikTok Sans Black like the static headlines,
    # captions in TikTok Sans Bold like the static labels.
    "font": "TikTok Sans",
    "title_weight": 900,
    "caption_weight": 700,
    "caption_color": "#FFFFFF",
    "highlight": "#FFE14D",
    "outline": "#000000",
    "title_color": "#111111",
    "title_box": "#FFFFFF",
    "caption_box": "#111111",
    "caption_style": "editorial",
    "cta_color": "#FFFFFF",
    "cta_box": "#111111",
    "card_bg": "#111111",
    "card_fg": "#FFFFFF",
    "case": "sentence",
}

CHAR_W = 0.56   # average glyph width as a fraction of font size, bold sans
LINE_H = 1.18


def brand_for(plan: dict) -> dict:
    b = dict(DEFAULT_BRAND)
    b.update(plan.get("brand") or {})
    return b


def face(brand: dict, role: str) -> str:
    """The family name a role renders in: one static instance per weight (see fonts.py)."""
    dflt = {"title": 900, "caption": 700, "small": 500, "accent": 600}[role]
    w = int(brand.get(f"{role}_weight", dflt))
    fam = brand.get("accent_font") if role == "accent" else brand["font"]
    return f"{fam} {w}"


SMALL_WORDS = {"a", "an", "the", "to", "of", "for", "in", "on", "at", "with", "and", "or", "but", "so",
               "is", "it", "it's", "i", "i'm", "i've", "i'll", "me", "my", "you", "your", "we", "was", "be",
               "that", "this", "as", "by", "from", "which", "just", "like", "do", "had", "have", "been", "are"}


def _emph_set(words: list, phrases: list) -> set:
    """Indexes of words that take the serif accent, from the plan's emphasis list."""
    out = set()
    bare = [_bare(w["w"]) for w in words]
    for ph in phrases or []:
        toks = [_bare(t) for t in ph.split()]
        for i in range(len(words) - len(toks) + 1):
            if bare[i:i + len(toks)] == toks:
                out.update(range(i, i + len(toks)))
    return out


def editorial_chunk(texts: list, emph: list, size: int, fmt: str, brand: dict, title: bool = False,
                    max_lines: int = 2, maxw: float | None = None):
    """Lay out a chunk, scaling it down in steps until it fits max_lines (never a third line)."""
    for scale in (1.0, 0.9, 0.8, 0.72, 0.65):
        lines, w, h = _editorial_layout(texts, emph, int(size * scale), fmt, brand, title, maxw)
        if len(lines) <= max_lines:
            break
    return lines, w, h


def _editorial_layout(texts: list, emph: list, size: int, fmt: str, brand: dict, title: bool = False,
                      maxw: float | None = None):
    """Lay out one chunk editorially. Returns (lines of (text, role, px) tuples, box w, box h).

    Connecting words small and lighter, the rest Bold, emphasis words large in the
    serif italic. If an emphasis word sits after the first word it starts the second
    line, so the phrase reads small-over-big ("until the / end").
    """
    acc = bool(brand.get("accent_font"))
    items = []
    # a phrase made only of connecting words ("to", "is the") shows at full size, never tiny
    all_small = all(_bare(t) in SMALL_WORDS for t in texts)
    for t, e in zip(texts, emph):
        if all_small and not (e and acc):
            items.append((t, "caption", size))
            continue
        if e and acc:
            items.append((t, "accent", int(size * 1.5)))
        elif _bare(t) in SMALL_WORDS:
            items.append((t, "small", int(size * 0.74)))
        else:
            items.append((t, "caption", size))

    def width(it):
        t, role, px = it
        k = {"accent": 0.40, "small": 0.52, "caption": 0.56}[role]
        return len(t) * px * k

    x0, _, x1, _ = specs.safe_box(fmt)
    maxw = maxw or (x1 - x0) * 0.92
    first_e = next((i for i, it in enumerate(items) if it[1] == "accent"), None)
    gap = 0.3 * size
    lines, cur, cw = [], [], 0.0
    for i, it in enumerate(items):
        wi = width(it)
        # break before the first emphasis word (small-over-big), or when the line is full
        if cur and ((i == first_e and not title) or cw + gap + wi > maxw):
            lines.append(cur)
            cur, cw = [], 0.0
        cur.append(it)
        cw += (gap if len(cur) > 1 else 0) + wi
    if cur:
        lines.append(cur)
    w = max(sum(width(i) for i in ln) + 0.3 * size * (len(ln) - 1) for ln in lines)
    h = sum(max(px for _, _, px in ln) * 1.05 for ln in lines)
    return lines, w, h


def ass_color(hex_rgb: str, alpha: int = 0) -> str:
    h = hex_rgb.lstrip("#")
    r, g, b = h[0:2], h[2:4], h[4:6]
    return f"&H{alpha:02X}{b}{g}{r}".upper().replace("&H", "&H", 1)


def ts(t: float) -> str:
    t = max(0.0, t)
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = t % 60
    cs = int(round((s - int(s)) * 100))
    si = int(s)
    if cs == 100:
        si, cs = si + 1, 0
    return f"{h}:{m:02d}:{si:02d}.{cs:02d}"


def _esc(text: str) -> str:
    return text.replace("\\", "/").replace("{", "(").replace("}", ")")


def _case(text: str, brand: dict) -> str:
    return text.upper() if brand.get("case") == "upper" else text


def wrap(text: str, max_chars: int, max_lines: int = 2) -> list:
    words = text.split()
    if len(text) <= max_chars or len(words) < 2:
        return [text]
    best, best_score = [text], 10 ** 9
    for i in range(1, len(words)):
        a, b = " ".join(words[:i]), " ".join(words[i:])
        score = max(len(a), len(b)) * 10 + (len(a) > len(b))  # balanced, top line not longer
        if score < best_score:
            best, best_score = [a, b], score
    if max_lines > 2 and max(len(x) for x in best) > max_chars:
        out, line = [], ""
        for w in words:
            if line and len(line) + 1 + len(w) > max_chars:
                out.append(line)
                line = w
            else:
                line = f"{line} {w}".strip()
        out.append(line)
        return out[:max_lines]
    return best


# Words that should not end a caption chunk: they lean on the next word, so a
# chunk ending on one reads as a broken phrase ("We plan every / session").
LEANING = {"a", "an", "the", "to", "of", "for", "in", "on", "at", "with", "and", "or", "but",
           "your", "my", "our", "their", "his", "her", "every", "each", "by", "from", "into"}


def _bare(w: str) -> str:
    return w.lower().strip(specs.PUNCT)


def _glue(words: list, phrases: list) -> list:
    """glued[i] is True when word i must stay on screen with word i-1 (a keep-together phrase)."""
    glued = [False] * len(words)
    bare = [_bare(w["w"]) for w in words]
    for ph in phrases or []:
        toks = [_bare(t) for t in ph.split()]
        n = len(toks)
        for i in range(len(words) - n + 1):
            if bare[i:i + n] == toks:
                for k in range(i + 1, i + n):
                    glued[k] = True
    return glued


def balanced(text: str, max_chars: int, max_lines: int = 3) -> list:
    """Break text into the fewest lines that fit, with line lengths as even as possible."""
    words = text.split()
    for n in range(1, max_lines + 1):
        best = None

        def rec(i, k, acc):
            nonlocal best
            if k == 1:
                line = " ".join(words[i:])
                cand = acc + [line]
                if len(line) <= max_chars:
                    sc = max(len(x) for x in cand) - min(len(x) for x in cand)
                    if best is None or sc < best[0]:
                        best = (sc, cand)
                return
            for j in range(i + 1, len(words) - k + 2):
                line = " ".join(words[i:j])
                if len(line) <= max_chars:
                    rec(j, k - 1, acc + [line])

        if len(words) >= n:
            rec(0, n, [])
        if best:
            return best[1]
    return wrap(text, max_chars, max_lines)


def chunk_words(words: list, max_words: int, max_chars: int, gap: float, keep_together=(), breaks=()) -> list:
    chunks, cur = [], []
    glued = _glue(words, keep_together)
    breaks = set(breaks)
    for i, w in enumerate(words):
        if cur and i in breaks:
            # a new framing starts here: the phrase never carries across it
            chunks.append(cur)
            cur = []
        if cur and glued[i] and w["start"] - cur[-1]["end"] <= gap:
            cur.append(w)
            continue
        if cur and i + 1 < len(words) and glued[i + 1] and len(cur) >= 2 and _bare(cur[-1]["w"]) not in LEANING:
            # a keep-together phrase starts here: open a fresh chunk for it
            chunks.append(cur)
            cur = []
        if cur:
            prev = cur[-1]
            text_len = len(" ".join(x["w"] for x in cur + [w]))
            hard = (w["start"] - prev["end"] > gap or prev["w"].rstrip()[-1:] in specs.END_PUNCT)
            full = len(cur) >= max_words or text_len > max_chars
            if hard:
                chunks.append(cur)
                cur = []
            elif full:
                starts_phrase = i + 1 < len(words) and glued[i + 1]
                if _bare(prev["w"]) in LEANING and len(cur) <= max_words and text_len <= max_chars and not starts_phrase:
                    # "for the" would hang: take the next word in and close there
                    cur.append(w)
                    chunks.append(cur)
                    cur = []
                    continue
                carry = []
                while len(cur) > 1 and _bare(cur[-1]["w"]) in LEANING:
                    carry.insert(0, cur.pop())
                chunks.append(cur)
                cur = carry
        cur.append(w)
    if cur:
        chunks.append(cur)
    return chunks


def fit_chars(fmt: str, size: int) -> int:
    """Most characters per line that fit the safe width at this size."""
    x0, _, x1, _ = specs.safe_box(fmt)
    return max(8, int((x1 - x0) * 0.92 / (size * CHAR_W)))


def box_for(text_lines: list, size: int, cx: float, cy: float, pad: float = 0.0):
    w = max(len(l) for l in text_lines) * size * CHAR_W + 2 * pad
    h = len(text_lines) * size * LINE_H + 2 * pad
    return (round(cx - w / 2), round(cy - h / 2), round(cx + w / 2), round(cy + h / 2))


class Placer:
    """Moves captions around a fixed frame, phrase by phrase, never over the face.

    Zones come from the face box in the finished frame: below the chin, left and right
    of the head, above it (after the hook title). The position changes at sentence
    breaks (or after three phrases), cycling below, left, below, right, above, and only
    into a zone the phrase fits and whose background is dark enough for white type.
    """

    CYCLE = ["below", "left", "below_l", "above", "below_r", "right"]

    def __init__(self, plan, pieces, fmt, brand, size):
        self.plan, self.pieces, self.fmt, self.brand, self.size = plan, pieces, fmt, brand, size
        self.W, self.H = specs.frame_size(fmt)
        self.cur, self.held, self.k = "below", 0, 0
        self.prev_end_sentence = True
        self.hook_end = max((float(t["end"]) for t in plan.get("titles", []) if t.get("style", "hook") == "hook"),
                            default=0.0)
        self.zones_allowed = (plan.get("captions") or {}).get("zones") or self.CYCLE

    def _piece(self, t):
        acc = 0.0
        for p in self.pieces:
            if acc - 0.01 <= t < acc + p.dur:
                return p
            acc += p.dur
        return self.pieces[-1]

    def zones(self, p):
        from . import faces, tools as _t
        W, H = self.W, self.H
        sx0, sy0, sx1, sy1 = specs.safe_box(self.fmt)
        if p.card or not p.src:
            return {"below": (sx0, H * 0.55, sx1, sy1)}, None, None, None
        sw, sh = _t.probe(p.src).display_size
        fx, fy = faces.focus_for(p, self.fmt)
        geo = faces.crop(W, H, sw, sh, p.zoom, fx, fy, self.fmt, getattr(p, "layout", "center"))
        fb = faces.detect(p.src, round((p.t_in + p.t_out) / 2, 1))
        if fb:
            face = faces.to_frame(fb, geo, W, H)
        else:
            ey = specs.EYE_LINE.get(self.fmt, (0.5, 0.38))[1] * H
            face = (W * 0.33, ey - H * 0.14, W * 0.67, ey + H * 0.16)
        m = H * 0.022
        fx0, fy0, fx1, fy1 = face
        z = {"below": (sx0, fy1 + m, sx1, sy1),
             "below_l": (sx0, fy1 + m, sx1, sy1),
             "below_r": (sx0, fy1 + m, sx1, sy1),
             "above": (sx0, sy0, sx1, fy0 - m),
             "left": (sx0, max(sy0, fy0 - H * 0.04), fx0 - m * 0.6, min(sy1, fy1 + H * 0.10)),
             "right": (fx1 + m * 0.6, max(sy0, fy0 - H * 0.04), sx1, min(sy1, fy1 + H * 0.10))}
        return z, face, geo, p

    def fit(self, zone, texts, emph, max_lines):
        x0, y0, x1, y1 = zone
        zw, zh = x1 - x0, y1 - y0
        if zw < self.W * 0.18 or zh < self.size * 0.7:
            return None
        for scale in (1.0, 0.9, 0.8, 0.72):
            lay, bw, bh = editorial_chunk(texts, emph, int(self.size * scale), self.fmt, self.brand,
                                          max_lines=max_lines, maxw=zw * 0.96)
            if len(lay) <= max_lines and bh <= zh and bw <= zw:
                return lay, bw, bh
        return None

    def readable(self, name, zone, geo, p):
        if name.startswith("below") or geo is None:
            return True
        from . import faces
        frac = faces.to_source(zone, geo)
        return faces.brightness(p.src, round((p.t_in + p.t_out) / 2, 1), frac) < 165

    def place(self, texts, emph, t, chunk):
        zones, face, geo, p = self.zones(self._piece(t))
        change = (self.held >= 3) or (self.held >= 1 and self.prev_end_sentence)
        order = []
        if change:
            for i in range(len(self.CYCLE)):
                order.append(self.CYCLE[(self.k + i) % len(self.CYCLE)])
        order = ([self.cur] if not change else []) + order + ["below", "below_l", "below_r", "left", "right", "above"]
        chosen = None
        for name in order:
            if name not in zones or name not in self.zones_allowed and name != "below":
                continue
            if name == "above" and t < self.hook_end + 0.2:
                continue
            res = self.fit(zones[name], texts, emph, 4 if name in ("left", "right") else 2)
            if res and name in ("below_l", "below_r") and res[1] > (zones[name][2] - zones[name][0]) * 0.7:
                res = None  # an off-centre line only reads as moved when it is short
            if not res or not self.readable(name, zones[name], geo, p):
                continue
            chosen = (name, res)
            break
        if chosen is None:  # last resort: below, as small as it needs
            name = "below"
            lay, bw, bh = editorial_chunk(texts, emph, int(self.size * 0.65), self.fmt, self.brand, max_lines=3)
            chosen = (name, (lay, bw, bh))
        name, (lay, bw, bh) = chosen
        if change and name in self.CYCLE:
            self.k = (self.CYCLE.index(name) + 1) % len(self.CYCLE)  # move the cycle on every change point
        if name != self.cur:
            self.cur, self.held = name, 0
        self.held += 1
        self.prev_end_sentence = chunk[-1]["w"].rstrip()[-1:] in ".?" + chr(33)
        x0, y0, x1, y1 = zones[name]
        cxm = self.W / 2
        if name == "below":
            an, x, y = 5, cxm, min(y0 + bh / 2 + self.H * 0.005, y1 - bh / 2)
            box = (cxm - bw / 2, y - bh / 2, cxm + bw / 2, y + bh / 2)
        elif name in ("below_l", "below_r"):
            y = min(y0 + bh / 2 + self.H * 0.005, y1 - bh / 2)
            if name == "below_l":
                an, x = 4, x0
                box = (x0, y - bh / 2, x0 + bw, y + bh / 2)
            else:
                an, x = 6, x1
                box = (x1 - bw, y - bh / 2, x1, y + bh / 2)
        elif name == "above":
            an, x, y = 5, cxm, y1 - bh / 2
            box = (cxm - bw / 2, y - bh / 2, cxm + bw / 2, y + bh / 2)
        elif name == "left":
            mid = (face[1] + face[3]) / 2 if face else (y0 + y1) / 2
            y = min(max(mid, y0 + bh / 2), y1 - bh / 2)
            an, x = 4, x0
            box = (x0, y - bh / 2, x0 + bw, y + bh / 2)
        else:
            mid = (face[1] + face[3]) / 2 if face else (y0 + y1) / 2
            y = min(max(mid, y0 + bh / 2), y1 - bh / 2)
            an, x = 6, x1
            box = (x1 - bw, y - bh / 2, x1, y + bh / 2)
        box = tuple(round(v) for v in box)
        return {"an": an, "x": x, "y": y, "lay": lay, "w": bw, "h": bh, "box": box, "zone": name,
                "face": tuple(round(v) for v in face) if face else None}


def _layout_at(pieces, t):
    acc = 0.0
    for p in pieces:
        if acc - 0.01 <= t < acc + p.dur:
            return getattr(p, "layout", "center")
        acc += p.dur
    return "center"


def _starts(pieces):
    t = 0.0
    for p in pieces:
        yield t, p
        t += p.dur


def _merge(spans, gap=0.3):
    out = []
    for a, b in sorted(spans):
        if out and a - out[-1][1] <= gap:
            out[-1] = (out[-1][0], max(out[-1][1], b))
        else:
            out.append((a, b))
    return out


def build(plan: dict, pieces: list, fmt: str) -> tuple:
    """Return (ass_text, events). Events carry layout boxes for the QA gate."""
    W, H = specs.frame_size(fmt)
    brand = brand_for(plan)
    cap_font = face(brand, "caption")
    title_font = face(brand, "title")
    cap = specs.CAPTION[fmt]
    cap_size = int((plan.get("captions") or {}).get("size", cap["size"]))
    title = specs.TITLE[fmt]
    t_size = int(title["size"])
    head = [
        "[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}",
        "WrapStyle: 2", "ScaledBorderAndShadow: yes", "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        f"Style: Caption,{cap_font},{cap_size},{ass_color(brand['caption_color'])},{ass_color(brand['highlight'])},{ass_color(brand['outline'])},{ass_color('#000000', 0x80)},0,0,0,0,100,100,0,0,1,{max(4, cap_size // 14)},2,5,0,0,0,1",
        f"Style: CapBox,{cap_font},{cap_size},{ass_color(brand['caption_color'])},{ass_color(brand['caption_color'])},{ass_color(brand['caption_box'])},{ass_color(brand['caption_box'])},0,0,0,0,100,100,0,0,3,{max(8, cap_size // 7)},0,5,0,0,0,1",
        f"Style: CapClean,{cap_font},{cap_size},{ass_color(brand['caption_color'])},{ass_color(brand['caption_color'])},{ass_color(brand['outline'], 0x60)},{ass_color('#000000', 0x70)},0,0,0,0,100,100,0,0,1,1.5,4,5,0,0,0,1",
        f"Style: CapEd,{cap_font},{cap_size},{ass_color(brand['caption_color'])},{ass_color(brand['caption_color'])},&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1",
        f"Style: Title,{title_font},{t_size},{ass_color(brand['title_color'])},{ass_color(brand['title_color'])},{ass_color(brand['title_box'])},{ass_color(brand['title_box'])},0,0,0,0,100,100,0,0,3,{t_size // 4},0,5,0,0,0,1",
        f"Style: CTA,{title_font},{t_size},{ass_color(brand['cta_color'])},{ass_color(brand['cta_color'])},{ass_color(brand['cta_box'])},{ass_color(brand['cta_box'])},0,0,0,0,100,100,0,0,3,{t_size // 4},0,5,0,0,0,1",
        f"Style: Card,{title_font},{int(t_size * 1.1)},{ass_color(brand['card_fg'])},{ass_color(brand['card_fg'])},{ass_color(brand['card_bg'])},{ass_color(brand['card_bg'])},0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1",
        "", "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]
    lines, events = [], []
    wtag = ""  # weights come from static font instances, never faux bold
    cx = W / 2

    # Captions
    cfg = plan.get("captions") or {}
    if cfg.get("on", True):
        words = [w for p in pieces if not p.card for w in p.words]
        cap_chars = min(cap["max_chars"], fit_chars(fmt, cap_size))
        lay_breaks, prev_lay = [], None
        for wi, w in enumerate(words):
            lw = _layout_at(pieces, w["start"])
            if prev_lay is not None and lw != prev_lay:
                lay_breaks.append(wi)
            prev_lay = lw
        chunks = chunk_words(words, int(cfg.get("max_words", specs.CAPTION["max_words"])),
                             cap_chars, specs.CAPTION["break_gap"], cfg.get("keep_together", []), lay_breaks)
        bounds, acc = [], 0.0
        for p in pieces:
            acc += p.dur
            bounds.append((acc, bool(p.card)))
        cy = H * float(cfg.get("y", cap["y"]))
        placer = Placer(plan, pieces, fmt, brand, cap_size)
        for ci, ch in enumerate(chunks):
            c_start = ch[0]["start"]
            nxt = chunks[ci + 1][0]["start"] if ci + 1 < len(chunks) else None
            c_end = min(nxt, ch[-1]["end"] + 0.35) if nxt else ch[-1]["end"] + 0.35
            c_end = max(c_end, c_start + specs.CAPTION["min_event"])
            if nxt:
                c_end = min(c_end, nxt)
            # never hang over into a card or the next framing: stop at the end of the piece the words are in
            for b_end, _ in bounds:
                if b_end >= ch[-1]["end"] - 0.01:
                    c_end = min(c_end, b_end)
                    break
            texts = [_esc(_case(w["w"], brand)) for w in ch]
            full = " ".join(texts)
            wrapped = wrap(full, cap_chars, specs.CAPTION["max_lines"])
            box = box_for(wrapped, cap_size, cx, cy)
            events.append({"kind": "caption", "text": full, "start": c_start, "end": c_end,
                           "lines": wrapped, "size": cap_size, "box": box})
            # one event per word. "box" (house default): the word being said sits in a
            # solid brand-colour box (accent on a solid background, never bare accent text
            # over footage); "color": the word is lit in the highlight colour.
            mode = cfg.get("style", brand.get("caption_style", "editorial"))
            if mode == "editorial":
                # house default: words arrive as spoken (fade and sharpen in), connecting
                # words small, the plan's emphasis words large in the brand serif italic,
                # white with a soft shadow. The whole phrase is laid out from the first
                # word so nothing jumps.
                emph_all = _emph_set(ch, cfg.get("emphasis", []))
                emph = [k in emph_all for k in range(len(ch))]
                # where this phrase sits depends on the layout of the shot it is in:
                # centre below the face, or set into the open side when the subject is off-centre
                pl = placer.place(texts, emph, c_start, ch)
                an, ax, ccy, lay, bw, bh, box, layout = pl["an"], pl["x"], pl["y"], pl["lay"], pl["w"], pl["h"], pl["box"], pl["zone"]
                events[-1]["face"] = pl["face"]
                events[-1]["lines"] = [" ".join(t for t, _, _ in ln) for ln in lay]
                events[-1]["box"] = box
                events[-1]["layout"] = layout
                events[-1]["max_lines"] = 4 if an in (4, 6) else 3  # side columns stack
                if brand.get("scrims", False):
                    strength = int(cfg.get("scrim", 0x57))
                    pad = H * 0.06
                    if an == 4:
                        rx0, rx1 = -100, box[2] + W * 0.12
                    elif an == 6:
                        rx0, rx1 = box[0] - W * 0.12, W + 100
                    else:
                        rx0, rx1 = -100, W + 100
                    lines.append(f"Dialogue: 0,{ts(c_start)},{ts(c_end)},CapEd,,0,0,0,,{{\\an7\\pos(0,0)\\p1\\bord0\\shad0\\c&H000000&"
                                 f"\\alpha&H{255 - strength:02X}&\\blur90}}m {rx0:.0f} {box[1] - pad:.0f} l {rx1:.0f} {box[1] - pad:.0f} "
                                 f"{rx1:.0f} {box[3] + pad:.0f} {rx0:.0f} {box[3] + pad:.0f}{{\\p0}}")
                flat = [it for ln in lay for it in ln]
                for wi, w in enumerate(ch):
                    ws = c_start if wi == 0 else w["start"]
                    we = ch[wi + 1]["start"] if wi + 1 < len(ch) else c_end
                    if we <= ws:
                        continue
                    for layer, shadow in ((1, True), (2, False)):
                        parts, k = [], 0
                        for li, ln in enumerate(lay):
                            seg = []
                            for (t, role, px) in ln:
                                fn = face(brand, role)
                                ital = "\\i1" if role == "accent" else "\\i0"
                                if shadow:
                                    vis, show = "&H50&", "&HFF&"
                                    look = f"\\c&H000000&\\blur7"
                                else:
                                    vis, show = "&H00&", "&HFF&"
                                    ol = float(cfg.get("outline", 0))  # thin ink outline for light clothing or walls
                                    look = f"\\c{ass_color(brand['caption_color'])}\\blur0"
                                    if ol:
                                        look += f"\\bord{ol:g}\\3c{ass_color(brand.get('outline', '#181B1E'))}"
                                if k < wi:
                                    a = f"\\alpha{vis}"
                                elif k == wi:
                                    a = f"\\alpha{show}\\t(0,140,\\alpha{vis})"
                                else:
                                    a = f"\\alpha{show}"
                                seg.append(f"{{\\fn{fn}\\fs{px}{ital}{look}{a}}}{t}")
                                k += 1
                            parts.append(" ".join(seg))
                        off = "\\pos({:.0f},{:.0f})".format(ax + (3 if shadow else 0), ccy + (5 if shadow else 0))
                        lines.append(f"Dialogue: {layer},{ts(ws)},{ts(we)},CapEd,,0,0,0,,{{\\an{an}{off}\\bord0\\shad0\\q2}}" + "\\N".join(parts))
                continue
            if mode == "clean":
                # house default: the phrase as one plain block, white with a soft shadow,
                # no per-word highlight, no box, no animation
                body = "\\N".join(wrapped)
                lines.append(f"Dialogue: 1,{ts(c_start)},{ts(c_end)},CapClean,,0,0,0,,{{\\an5\\pos({cx:.0f},{cy:.0f})}}{body}")
                continue
            bord = max(4, cap_size // 14)
            n_top = len(wrapped[0].split()) if len(wrapped) == 2 else None

            def _join(toks):
                if n_top:
                    return " ".join(toks[:n_top]) + "\\N" + " ".join(toks[n_top:])
                return " ".join(toks)

            for wi, w in enumerate(ch):
                ws = c_start if wi == 0 else w["start"]
                we = ch[wi + 1]["start"] if wi + 1 < len(ch) else c_end
                if we <= ws:
                    continue
                # the phrase pops in on its first word
                pop = "\\fscx86\\fscy86\\t(0,90,\\fscx100\\fscy100)" if wi == 0 else ""
                pos = f"\\an5\\pos({cx:.0f},{cy:.0f}){pop}"
                if mode == "box":
                    boxed = [(f"{{\\alpha&HFF&\\3a&H00&}}{t}" if k == wi else f"{{\\alpha&HFF&\\3a&HFF&}}{t}")
                             for k, t in enumerate(texts)]
                    lines.append(f"Dialogue: 1,{ts(ws)},{ts(we)},CapBox,,0,0,0,,{{{pos}}}{_join(boxed)}")
                    plain = [(f"{{\\bord0\\shad0}}{t}" if k == wi else f"{{\\bord{bord}\\shad2}}{t}")
                             for k, t in enumerate(texts)]
                    lines.append(f"Dialogue: 2,{ts(ws)},{ts(we)},Caption,,0,0,0,,{{{pos}}}{_join(plain)}")
                else:
                    parts = [f"{{\\c{ass_color(brand['highlight'] if k == wi else brand['caption_color'])}}}{t}"
                             for k, t in enumerate(texts)]
                    lines.append(f"Dialogue: 1,{ts(ws)},{ts(we)},Caption,,0,0,0,,{{{pos}}}{_join(parts)}")

    # Titles (hook text, CTA text, labels). A title with from_end counts its times
    # back from the end of the ad (the CTA over the closing beat).
    total = sum(p.dur for p in pieces)
    titles = []
    for t in plan.get("titles", []):
        if t.get("from_end"):
            t = dict(t, start=total + float(t["start"]), end=total + float(t["end"]))
        titles.append(t)
    for t in titles:
        if t.get("formats") and fmt not in t["formats"]:
            continue
        if t.get("style", "hook") in ("hook", "cta") and brand.get("title_style", "plain") == "plain":
            # one font, TikTok Sans Black, white, balanced lines, no box (Liam, 2026-11-25:
            # the hook does not take the caption's mixed type)
            txt = _esc(_case(t["text"], brand))
            # the largest size that sets the hook on two lines (it has to sit above the head)
            size, wrapped = int(t.get("size", t_size)), None
            if "\n" in txt:
                wrapped = txt.split("\n")
            elif "size" not in t:
                for sz in (96, 88, 80, 74):
                    cand = balanced(txt, fit_chars(fmt, sz), 2)
                    if len(cand) <= 2 and max(len(x) for x in cand) <= fit_chars(fmt, sz):
                        size, wrapped = sz, cand
                        break
            if wrapped is None:
                wrapped = balanced(txt, fit_chars(fmt, size), 3)
            bh = len(wrapped) * size * 1.12
            _, sy0, _, sy1 = specs.safe_box(fmt)
            if "y" in t:
                y = H * float(t["y"])
            elif t.get("style", "hook") == "hook":
                y = sy0 + H * 0.02 + bh / 2
            else:
                y = sy1 - H * 0.02 - bh / 2
            box = box_for(wrapped, size, cx, y)
            events.append({"kind": t.get("style", "hook"), "text": t["text"], "start": float(t["start"]),
                           "end": float(t["end"]), "lines": wrapped, "size": size, "box": box})
            if brand.get("scrims", False):
                if t.get("style", "hook") == "hook":
                    ry0, ry1 = -100, int(box[3] + H * 0.07)
                else:
                    ry0, ry1 = int(box[1] - H * 0.07), H + 100
                lines.append(f"Dialogue: 0,{ts(float(t['start']))},{ts(float(t['end']))},CapEd,,0,0,0,,"
                             f"{{\\an7\\pos(0,0)\\p1\\bord0\\shad0\\c&H000000&\\alpha&H78&\\blur70\\fad(0,120)}}"
                             f"m -100 {ry0} l {W + 100} {ry0} {W + 100} {ry1} -100 {ry1}{{\\p0}}")
            body = "\\N".join(wrapped)
            fn = face(brand, "title")
            lines.append(f"Dialogue: 4,{ts(float(t['start']))},{ts(float(t['end']))},CapEd,,0,0,0,,"
                         f"{{\\an5\\pos({cx + 3:.0f},{y + 5:.0f})\\fn{fn}\\fs{size}\\c&H000000&\\alpha&H50&\\blur8\\q2\\fad(0,120)}}{body}")
            lines.append(f"Dialogue: 5,{ts(float(t['start']))},{ts(float(t['end']))},CapEd,,0,0,0,,"
                         f"{{\\an5\\pos({cx:.0f},{y:.0f})\\fn{fn}\\fs{size}\\c{ass_color(brand['caption_color'])}\\q2\\fad(0,120)}}{body}")
            continue
        style = {"cta": "CTA"}.get(t.get("style", "hook"), "Title")
        size = int(t.get("size", t_size))
        txt = _esc(_case(t["text"], brand))
        chars = min(title["max_chars"], fit_chars(fmt, size))
        wrapped = wrap(txt, chars, 3) if "\n" not in txt else txt.split("\n")
        pad = size // 4
        _, sy0, _, sy1 = specs.safe_box(fmt)
        bh = len(wrapped) * size * LINE_H + 2 * pad
        if "y" in t:
            y = H * float(t["y"])
        elif style == "Title":
            y = sy0 + H * 0.015 + bh / 2          # top of the safe zone
        else:
            y = sy1 - H * 0.015 - bh / 2          # CTA sits at the bottom of the safe zone
        box = box_for(wrapped, size, cx, y, pad)
        events.append({"kind": t.get("style", "hook"), "text": t["text"], "start": float(t["start"]),
                       "end": float(t["end"]), "lines": wrapped, "size": size, "box": box})
        lines.append(f"Dialogue: 2,{ts(float(t['start']))},{ts(float(t['end']))},{style},,0,0,0,,{{\\an5\\pos({cx:.0f},{y:.0f})\\fad(120,0)}}{wtag}" + "\\N".join(wrapped))

    # Card text. A card takes one "text", or "lines": a stack of
    # {"text", "size", "y", "face": "title"|"caption", "color"} for an end card
    # built like the static End card (mega offer, support line, CTA line).
    t = 0.0
    for p in pieces:
        if p.card:
            stack = p.card.get("lines") or ([{"text": p.card["text"], "size": p.card.get("size", int(t_size * 1.1)),
                                              "y": p.card.get("y", 0.45)}] if p.card.get("text") else [])
            for item in stack:
                txt = _esc(_case(item["text"], brand))
                size = int(item.get("size", t_size))
                wrapped = txt.split("\n") if "\n" in txt else wrap(txt, fit_chars(fmt, size), 3)
                y = H * float(item.get("y", 0.45))
                box = box_for(wrapped, size, cx, y)
                events.append({"kind": "card", "text": item["text"], "start": t, "end": t + p.dur,
                               "lines": wrapped, "size": size, "box": box})
                fam = face(brand, item.get("face", "title"))
                col = item.get("color", p.card.get("fg", brand["card_fg"]))
                lines.append(f"Dialogue: 3,{ts(t)},{ts(t + p.dur)},Card,,0,0,0,,{{\\an5\\pos({cx:.0f},{y:.0f})\\fn{fam}\\fs{size}"
                             f"\\c{ass_color(col)}\\fad(150,0)}}" + "\\N".join(wrapped))
        t += p.dur

    return "\n".join(head + lines) + "\n", events
