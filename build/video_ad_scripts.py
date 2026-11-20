"""
Document 1: Video Ad Scripts (.docx) (System Prompt section 9).

Vertical 9:16 social scripts, laid out for the client. 2026-10-22: what we
need, before you film, then per video a plain line on what it is, how to film
and a table of takes. Nothing the client doesn't film or say.

2026-11-20 (Liam, Fisica): "a big document of text is really hard to read".
The doc is now laid out like a shoot sheet: page one is the whole filming plan
as one table, and every video starts on its own page with a title banner, an
at-a-glance strip (on camera, where, what you film, how long the ad runs),
numbered filming steps, the shape of the video where it has one, then the
takes, one sentence per line in larger type, with a box to tick per take.

Driven by data["scripts"]. See evals/cases/sample_client.json for the shape.
"""

from __future__ import annotations

import os
import re

from . import template as T

RECORDING_BEST_PRACTICE = [
    "Film vertical 9:16.",
    "Strong first frame, eyes to the lens immediately.",
    "Shoot at eye level, arm's length, face centred.",
    "Use natural light facing a window.",
    "Quiet room, test a 5 second clip, use a mic.",
    "Clean background with subtle brand cues.",
    "Calm, confident pace, pause after key lines.",
    "Record 3 takes of every line.",
]

# Editing and delivery best practice for paid social / Reels video.
# Research current best practice before each build and pass a refreshed list as
# data["scripts"]["editing_best_practice"]; this is the evergreen fallback.
DEFAULT_EDITING_BEST_PRACTICE = [
    "Win the first 3 seconds: open on the hook with motion and bold on screen text.",
    "Design for sound off and sound on: burned in captions on every line, social font.",
    "Vertical 9:16, keep text and faces inside the safe zones, clear of the top and bottom app UI.",
    "Cut out dead air, change something visual every 1 to 2 seconds to hold attention.",
    "Keep on screen text short, large and high contrast, one idea at a time.",
    "Show a brand cue in the first few seconds, not only at the end.",
    "Keep it feeling native and handheld, not over produced, around 15 to 30 seconds.",
    "End on a clean CTA card with the offer.",
]

# Shoot-sheet palette and sizes (2026-11-20). A4 with 2cm margins: our clients
# are in Australia and the UK, and the extra height keeps each video on one page.
PAGE_WIDTH_CM = 17.0
PAGE_MARGIN_CM = 2.0
FILL_LIGHT = "F2F2F2"
FILL_BLACK = "000000"
WHITE = (255, 255, 255)
LABEL_GREY = (110, 110, 110)
SIZE_SCRIPT = 11.5    # spoken lines in the takes table, read from a distance
SIZE_INTRO = 11       # the one line on what the video is
TICK = "☐"       # ballot box, ticked by hand or in Google Docs


def _shade(cell, hex_fill):
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn

    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_fill)
    tc_pr.append(shd)


def _cell_text(cell, text, bold=False, italic=False, color=None, first=True,
               size=None, center=False, space_after=4, space_before=2, keep=False):
    """Write text into a table cell, one paragraph per line, fonts set on every run.

    keep=True sets keep-with-next, so Word keeps that row with the one below.
    """
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Pt

    lines = text.split("\n") if isinstance(text, str) else [str(text)]
    for i, line in enumerate(lines):
        para = cell.paragraphs[0] if (first and i == 0) else cell.add_paragraph()
        para.paragraph_format.space_before = Pt(space_before)
        if keep:
            para.paragraph_format.keep_with_next = True
        para.paragraph_format.space_after = Pt(space_after)
        if center:
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = para.add_run(line)
        T._set_run_font(run, size=size or T.SIZE_BODY, bold=bold, italic=italic,
                        color=color or T.COLOR_BLACK)


def _tblpr_add(table, el):
    """Add a table property in schema order (before tblLook when present)."""
    from docx.oxml.ns import qn

    tbl_pr = table._tbl.tblPr
    look = tbl_pr.find(qn("w:tblLook"))
    if look is not None:
        look.addprevious(el)
    else:
        tbl_pr.append(el)


def _borders(table, color="BFBFBF", size=4):
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn

    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}")
        if color is None:
            el.set(qn("w:val"), "nil")
        else:
            el.set(qn("w:val"), "single")
            el.set(qn("w:sz"), str(size))
            el.set(qn("w:color"), color)
        borders.append(el)
    _tblpr_add(table, borders)


def _fixed(table):
    # Fixed layout, so a short table keeps the same column widths as a long one
    # instead of the label column collapsing to fit its text.
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn

    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    _tblpr_add(table, layout)


def _margins(table, top=50, bottom=50, left=120, right=120):
    """Cell padding in twips, so text never sits on the cell edge."""
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn

    mar = OxmlElement("w:tblCellMar")
    for side, value in (("top", top), ("left", left), ("bottom", bottom), ("right", right)):
        el = OxmlElement(f"w:{side}")
        el.set(qn("w:w"), str(value))
        el.set(qn("w:type"), "dxa")
        mar.append(el)
    _tblpr_add(table, mar)


def _widths(table, widths_cm):
    from docx.shared import Cm

    for i, w in enumerate(widths_cm):
        table.columns[i].width = Cm(w)
    for row in table.rows:
        for i, w in enumerate(widths_cm):
            row.cells[i].width = Cm(w)


def _keep_row(row, header=False):
    """Never split a row across a page; repeat header rows on a new page."""
    from docx.oxml import OxmlElement

    tr_pr = row._tr.get_or_add_trPr()
    tr_pr.append(OxmlElement("w:cantSplit"))
    if header:
        tr_pr.append(OxmlElement("w:tblHeader"))


def _middle(cell):
    from docx.enum.table import WD_ALIGN_VERTICAL

    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER


def _grid(doc, cols, border="BFBFBF", border_size=4):
    table = doc.add_table(rows=0, cols=cols)
    table.autofit = False
    _borders(table, border, border_size)
    _fixed(table)
    _margins(table)
    return table


def _header_row(table, headers):
    row = table.add_row()
    _keep_row(row, header=True)
    for cell, h in zip(row.cells, headers):
        _shade(cell, FILL_BLACK)
        _middle(cell)
        _cell_text(cell, h, bold=True, color=WHITE, size=9)
    return row


def _table(doc, headers, rows, widths_cm):
    """A simple two or three column table: black header row, script text in grey.

    rows: list of lists of (text, style) where style is "label", "script" or "note".
    Also used by the Landing Page Copy wireframe blocks.
    """
    table = _grid(doc, len(headers))
    _header_row(table, headers)
    for row in rows:
        r = table.add_row()
        _keep_row(r)
        for i, (text, style) in enumerate(row):
            if style == "label":
                _cell_text(r.cells[i], text, bold=True)
            elif style == "script":
                _cell_text(r.cells[i], text, color=T.COLOR_SCRIPT_GREY)
            else:
                _cell_text(r.cells[i], text, italic=True, color=T.COLOR_DIRECTION_GREY)
    _widths(table, widths_cm)
    return table


def _gap(doc, pt=6):
    from docx.shared import Pt

    para = doc.add_paragraph()
    para.paragraph_format.space_before = Pt(0)
    para.paragraph_format.space_after = Pt(0)
    run = para.add_run("")
    T._set_run_font(run, size=pt)
    return para


def _section(doc, text):
    """A small bold caps label above each block of a video page."""
    from docx.shared import Pt

    para = doc.add_paragraph()
    para.paragraph_format.space_before = Pt(8)
    para.paragraph_format.space_after = Pt(4)
    para.paragraph_format.keep_with_next = True
    run = para.add_run(text.upper())
    T._set_run_font(run, size=11, bold=True, color=T.COLOR_BLACK)
    return para


def _banner(doc, kicker, title):
    table = _grid(doc, 1, border=None)
    cell = table.add_row().cells[0]
    _shade(cell, FILL_BLACK)
    _cell_text(cell, kicker, bold=True, color=(191, 191, 191), size=9, space_after=0)
    _cell_text(cell, title, bold=True, color=WHITE, size=18, first=False, space_after=6)
    _widths(table, [PAGE_WIDTH_CM])


def _glance(doc, items):
    """One shaded strip: ON CAMERA | WHERE | YOU FILM | FINISHED AD."""
    table = _grid(doc, len(items), border="FFFFFF", border_size=24)
    cells = table.add_row().cells
    for cell, (label, value) in zip(cells, items):
        _shade(cell, FILL_LIGHT)
        _cell_text(cell, label.upper(), bold=True, color=LABEL_GREY, size=8, space_after=1)
        _cell_text(cell, value, bold=True, size=10, first=False)
    _widths(table, [PAGE_WIDTH_CM / len(items)] * len(items))


def _steps(doc, steps):
    """Numbered filming steps, one per row, number in a black square."""
    table = _grid(doc, 2, border="FFFFFF", border_size=12)
    for i, step in enumerate(steps, start=1):
        row = table.add_row()
        _keep_row(row)
        num, text = row.cells
        _shade(num, FILL_BLACK)
        _middle(num)
        _cell_text(num, str(i), bold=True, color=WHITE, size=11, center=True)
        _shade(text, FILL_LIGHT)
        _middle(text)
        _cell_text(text, step, size=10, space_after=0, space_before=0)
    _widths(table, [1.0, PAGE_WIDTH_CM - 1.0])


def _flow(doc, labels):
    """The shape of the video as a strip of numbered steps, left to right."""
    table = _grid(doc, len(labels), border="FFFFFF", border_size=24)
    cells = table.add_row().cells
    for i, (cell, label) in enumerate(zip(cells, labels), start=1):
        _shade(cell, FILL_LIGHT)
        _cell_text(cell, str(i), bold=True, size=12, center=True, space_after=0, space_before=0)
        _cell_text(cell, label, bold=True, size=8.5, center=True, first=False, space_after=1)
    _widths(table, [PAGE_WIDTH_CM / len(labels)] * len(labels))


def _sentences(text):
    """One sentence per line, so a take reads like a prompter, not a paragraph."""
    parts = re.split(r"(?<=[.?])\s+(?=[\"\[A-Z])", (text or "").strip())
    return [p for p in parts if p]


def _takes(doc, rows, whole=None):
    """TAKE | WHAT TO SAY | LENGTH, one take per row with a box to tick."""
    table = _grid(doc, 3)
    _header_row(table, ["TAKE", "WHAT TO SAY", "LENGTH"])
    for r in rows:
        row = table.add_row()
        _keep_row(row)
        take, say, length = row.cells
        _shade(take, FILL_LIGHT)
        _cell_text(take, r["label"], bold=True, size=10, space_before=0, space_after=1)
        _cell_text(take, f"{TICK} Filmed", color=LABEL_GREY, size=8.5, first=False, space_after=0, space_before=0)
        for i, sentence in enumerate(_sentences(r["line"])):
            _cell_text(say, sentence, color=T.COLOR_SCRIPT_GREY, size=SIZE_SCRIPT,
                       first=(i == 0), space_after=1, space_before=0)
        if r.get("note"):
            _cell_text(say, r["note"], italic=True, color=T.COLOR_DIRECTION_GREY,
                       size=9.5, first=False, space_before=1, space_after=0)
        _cell_text(length, r["length"], italic=True, color=T.COLOR_DIRECTION_GREY, size=9,
                   space_before=0, space_after=0)
    if whole:
        label, text, length = whole
        row = table.add_row()
        _keep_row(row)
        a, b, c = row.cells
        for cell in (a, b, c):
            _shade(cell, FILL_LIGHT)
        _cell_text(a, label, bold=True)
        _cell_text(b, text, italic=True, color=T.COLOR_DIRECTION_GREY)
        _cell_text(c, length, bold=True, size=9)
    _widths(table, [3.4, 11.2, 2.4])


def _questions(doc, rows):
    """Numbered interview questions with what to get them talking about."""
    table = _grid(doc, 3)
    _header_row(table, ["#", "ASK", "GET THEM TALKING ABOUT"])
    for i, (question, steer) in enumerate(rows, start=1):
        row = table.add_row()
        _keep_row(row)
        num, ask, listen = row.cells
        _shade(num, FILL_LIGHT)
        _cell_text(num, str(i), bold=True, size=11, center=True)
        _cell_text(ask, question, bold=True, size=11)
        _cell_text(listen, steer or "", italic=True, color=T.COLOR_DIRECTION_GREY, size=10)
    _widths(table, [1.0, 6.6, 9.4])


# Spoken length of a take, worked out from its words at a calm talking pace
# (about 150 words a minute). Liam, 2026-11-03: the client should see how long
# every take and the whole video runs, in the table of what to say.
WORDS_PER_SECOND = 2.5


def _seconds(text):
    import math
    words = len(re.findall(r"[A-Za-z0-9']+", text or ""))
    return max(2, math.ceil(words / WORDS_PER_SECOND))


def _about(low, high=None):
    r = lambda x: max(5, 5 * round(x / 5))  # noqa: E731
    high = low if high is None else high
    if r(low) == r(high):
        return f"About {r(low)} sec"
    return f"About {r(low)} to {r(high)} sec"


def _kind(concept):
    if concept.get("organic"):
        return "organic"
    if concept.get("kind"):
        return concept["kind"]
    beats = concept.get("script", [])
    if beats and not any(b.get("line") for b in beats):
        return "interview"
    return "script"


def _script_plan(concept):
    """The takes of a scripted video: rows, the whole-video row and flow labels.

    Labelled beats (a single-problem video's steps: the problem, how people
    notice it, why it keeps coming back, what we do, proof) get a numbered row
    each and a flow strip, so the client sees the shape (Liam, 2026-11-19).
    """
    hooks = [h for h in concept.get("hooks", []) if h]
    beats = concept.get("script", [])
    test = bool(concept.get("hook_test")) and len(hooks) > 1
    used = hooks if test else hooks[:1]
    spoken = [b for b in beats if b.get("line")]
    labelled = bool(spoken) and any(b.get("label") for b in spoken)
    opening = concept.get("opening_label", "Opening line")
    carry = concept.get("carry_on")

    rows = []
    for i, hook in enumerate(used, start=1):
        label = f"Hook {i}" if test else (f"1. {opening}" if labelled else opening)
        note = f'Then carry straight on: "{carry}" and stop.' if carry else None
        rows.append({"label": label, "line": hook, "note": note,
                     "length": _about(_seconds(hook))})
    middle = "\n".join(b["line"] for b in spoken)
    mid_s = _seconds(middle) if middle else 0
    if labelled:
        for j, b in enumerate(spoken, start=2):
            rows.append({"label": f"{j}. {b.get('label') or 'Middle'}", "line": b["line"],
                         "length": _about(_seconds(b["line"]))})
    elif middle:
        rows.append({"label": "Middle" + (" (same after every hook)" if test else ""),
                     "line": " ".join(b["line"] for b in spoken), "length": _about(mid_s)})
    end_s = _seconds(concept["cta"]) if concept.get("cta") else 0
    if concept.get("cta"):
        label = f"{len(spoken) + 2}. Ending" if labelled else "Ending"
        rows.append({"label": label, "line": concept["cta"], "length": _about(end_s)})

    hook_s = [_seconds(h) for h in used] or [0]
    if test and not middle:
        # The middle is reused from a running ad, so the honest total is what
        # the client films: every opening plus the ending.
        whole = ("Total to film", "Every opening plus the ending",
                 _about(sum(hook_s) + end_s))
        finished = None
    else:
        whole_len = _about(min(hook_s) + mid_s + end_s, max(hook_s) + mid_s + end_s)
        whole = ("Whole video",
                 "Each video, opening line to ending" if test else "Opening line to ending",
                 whole_len)
        finished = whole_len
    flow = [opening] + [b.get("label") or "Middle" for b in spoken] + (
        ["Ending"] if concept.get("cta") else []) if labelled else None
    return rows, whole, flow, finished


def _you_film(concept, kind, rows=None):
    if concept.get("you_film"):
        return concept["you_film"]
    if kind == "script" and rows is not None:
        n = len(rows)
        return f"{n} short take{'s' if n != 1 else ''}"
    if kind == "interview":
        n = len([b for b in concept.get("script", []) if b.get("question") or b.get("label")])
        return f"{n} questions per person"
    if kind == "brief":
        return "Leave the phone recording"
    if kind == "organic":
        return f"{len(concept.get('hooks', []))} post ideas"
    return ""


def build_video_ad_scripts(data, out_dir, workspace=None):
    """Video Ad Scripts, laid out as a shoot sheet (Liam, 2026-11-20).

    Page one: the header, WHAT WE NEED FROM YOU as one table of every video
    (where, what you film, a box to tick), then BEFORE YOU FILM as a grid of
    tips. Then one page per video: a title banner, an at-a-glance strip, the
    one line on what it is, numbered HOW TO FILM steps, THE SHAPE OF THIS VIDEO
    where it has labelled steps, and the takes or questions.
    """
    doc = T.new_document()
    from docx.shared import Cm
    section = doc.sections[0]
    section.page_width, section.page_height = Cm(21.0), Cm(29.7)
    for side in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
        setattr(section, side, Cm(PAGE_MARGIN_CM))
    meta = data.get("scripts", {})
    concepts = meta.get("concepts", [])

    T.add_header_block(
        doc,
        client=data.get("client_business_name", ""),
        campaign=data.get("campaign", ""),
        prepared_by=data.get("prepared_by", "Maxalding Agency"),
        workspace=workspace,
    )

    plans = {}
    for n, concept in enumerate(concepts, start=1):
        if _kind(concept) == "script":
            plans[n] = _script_plan(concept)

    # WHAT WE NEED FROM YOU: the whole shoot on one table, then the plain lines.
    doc.add_paragraph()
    T.add_subheading(doc, "WHAT WE NEED FROM YOU")
    if concepts:
        table = _grid(doc, 5)
        _header_row(table, ["#", "VIDEO", "WHERE", "WHAT YOU FILM", "DONE"])
        for n, concept in enumerate(concepts, start=1):
            kind = _kind(concept)
            row = table.add_row()
            _keep_row(row)
            c = row.cells
            _shade(c[0], FILL_LIGHT)
            _cell_text(c[0], str(n), bold=True, center=True)
            _cell_text(c[1], concept.get("title", concept.get("name", "")), bold=True)
            _cell_text(c[2], concept.get("where", ""))
            _cell_text(c[3], _you_film(concept, kind, plans.get(n, (None,))[0]))
            _cell_text(c[4], TICK, size=14, center=True)
        _widths(table, [0.9, 4.4, 4.6, 5.5, 1.6])
        _gap(doc)
    for point in meta.get("summary", []):
        T.add_body(doc, f"- {point}")

    # BEFORE YOU FILM: guidance only, vertical only, as a grid of tips. No
    # mention of the VSL or 16:9 here. Outdoor clients (a pitch, an oval, a
    # park) pass their own list in scripts.recording_best_practice
    # (Relentless Generation, 2026-10-22).
    # The heading, the bold line and the tips grid stay together, so the tips
    # never split across pages.
    doc.add_paragraph()
    T.add_subheading(doc, "BEFORE YOU FILM").paragraph_format.keep_with_next = True
    T.add_body(doc, "These are guides, not lines to learn. Say it your way and hit the "
                    "main points.", bold=True).paragraph_format.keep_with_next = True
    tips = list(meta.get("recording_best_practice") or RECORDING_BEST_PRACTICE)
    table = _grid(doc, 2, border="FFFFFF", border_size=24)
    pairs = range(0, len(tips), 2)
    for i in pairs:
        row = table.add_row()
        _keep_row(row)
        last = i == pairs[-1]
        for cell, tip in zip(row.cells, tips[i:i + 2] + [""]):
            if tip:
                _shade(cell, FILL_LIGHT)
            _cell_text(cell, tip, size=10, keep=not last)
    _widths(table, [PAGE_WIDTH_CM / 2] * 2)

    total = len(concepts)
    for n, concept in enumerate(concepts, start=1):
        kind = _kind(concept)
        name = concept.get("name", "")
        hooks = [h for h in concept.get("hooks", []) if h]
        beats = concept.get("script", [])
        rows, whole, flow, finished = plans.get(n, (None, None, None, None))

        # Every video on its own page, opened by a banner. A plain
        # client-facing title ("The parent video") stands in for the agency
        # concept name ("Audience Addresser").
        doc.add_page_break()
        _banner(doc, f"VIDEO {n} OF {total}", concept.get("title", name).upper())
        _gap(doc)

        glance = []
        if concept.get("talent"):
            glance.append(("On camera", concept["talent"]))
        if concept.get("where"):
            glance.append(("Where", concept["where"]))
        you_film = _you_film(concept, kind, rows)
        if you_film:
            glance.append(("You film", you_film))
        ad_length = concept.get("ad_length") or finished
        if ad_length:
            glance.append(("Finished ad", ad_length))
        if glance:
            _glance(doc, glance)

        what = concept.get("what") or concept.get("intro")
        if what:
            from docx.shared import Pt
            para = doc.add_paragraph()
            para.paragraph_format.space_before = Pt(8)
            para.paragraph_format.space_after = Pt(2)
            run = para.add_run(what)
            T._set_run_font(run, size=SIZE_INTRO, color=T.COLOR_BLACK)
        if kind == "organic":
            T.add_body(doc, "ORGANIC CONTENT, NOT AN AD SCRIPT.", bold=True)

        # How to film: the concept's own steps plus any direction-only beats
        # (props, which hook needs what) on a scripted video.
        how = list(concept.get("how_to_film", []))
        if kind == "script":
            how += [b["direction"] for b in beats if b.get("direction") and not b.get("line")]
        if how:
            _section(doc, "How to film")
            _steps(doc, how)

        if kind == "script":
            if flow:
                _section(doc, "The shape of this video")
                _flow(doc, flow)
            _section(doc, "What to say")
            # The whole-video length already sits in the at-a-glance strip as
            # FINISHED AD, so the row only stays when it says something new:
            # the total to film on a hook test (Liam, 2026-11-20).
            _takes(doc, rows, None if ad_length == whole[2] else whole)

        elif kind == "interview":
            qs = []
            # The opening line only gets its own row when the first question
            # does not already ask for it.
            if hooks and not (beats and beats[0].get("question")):
                qs.append(("Opening line", "Get it as one full sentence: " + hooks[0]))
            for b in beats:
                q, steer = b.get("question"), b.get("steer")
                if not q:
                    q, steer = b.get("label", ""), b.get("direction", "")
                qs.append((q, steer))
            _section(doc, "The questions")
            _questions(doc, qs)
            # The end card and CTA audio are edit notes, not something the
            # client films, so they stay out of this doc (Liam, 2026-10-22).

        elif kind == "brief":
            # A filming brief with nothing to say on camera, for example
            # recording whole sessions for B-Roll: the steps are the page
            # (Liam, 2026-11-19).
            pass

        else:  # organic
            labels = concept.get("hook_labels", [])
            org = []
            for i, hook in enumerate(hooks):
                idea = beats[i]["direction"] if i < len(beats) else ""
                org.append([(labels[i] if i < len(labels) else f"Pillar {i + 1}", "label"),
                            (hook, "script"), (idea, "note")])
            _section(doc, "Post ideas")
            _table(doc, ["PILLAR", "EXAMPLE OPENING LINE", "MORE IDEAS"], org, [3.5, 5.0, 8.0])
            # Only the pillars table. Extra notes and "when a post runs as an
            # ad" read as commentary to the client (Liam, 2026-10-22).

    # No take checklist: Liam removed it as AI commentary (2026-10-22). The
    # per-take tick box is part of the takes table, not a separate list.

    filename = T.deliverable_filename(data["client_business_name"], "Video Ad Scripts", campaign=data.get("campaign"))
    out_path = os.path.join(out_dir, filename)
    doc.save(out_path)
    return out_path
