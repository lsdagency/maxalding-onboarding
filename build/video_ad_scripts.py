"""
Document 1: Video Ad Scripts (.docx) (System Prompt section 9).

Vertical 9:16 social scripts, laid out for the client (2026-10-22): what we
need, before you film, then per video a plain line on what it is, how to film
and a table of takes. Nothing the client doesn't film or say.

Driven by data["scripts"]. See evals/cases/sample_client.json for the shape.
"""

from __future__ import annotations

import os

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


def _shade(cell, hex_fill):
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn

    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_fill)
    tc_pr.append(shd)


def _cell_text(cell, text, bold=False, italic=False, color=None, first=True):
    """Write text into a table cell, one paragraph per line, fonts set on every run."""
    from docx.shared import Pt

    lines = text.split("\n") if isinstance(text, str) else [str(text)]
    for i, line in enumerate(lines):
        para = cell.paragraphs[0] if (first and i == 0) else cell.add_paragraph()
        para.paragraph_format.space_before = Pt(2)
        para.paragraph_format.space_after = Pt(4)
        run = para.add_run(line)
        T._set_run_font(run, size=T.SIZE_BODY, bold=bold, italic=italic,
                        color=color or T.COLOR_BLACK)


def _table(doc, headers, rows, widths_cm):
    """A simple two or three column table: black header row, script text in grey.

    rows: list of lists of (text, style) where style is "label", "script" or "note".
    """
    from docx.shared import Cm

    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn

    table = doc.add_table(rows=1, cols=len(headers))
    table.autofit = False
    # Light grey borders, set explicitly: the default template has no grid style.
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), "4")
        el.set(qn("w:color"), "BFBFBF")
        borders.append(el)
    table._tbl.tblPr.append(borders)
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        _shade(cell, "000000")
        _cell_text(cell, h, bold=True, color=(255, 255, 255))
    for row in rows:
        cells = table.add_row().cells
        for i, (text, style) in enumerate(row):
            if style == "label":
                _cell_text(cells[i], text, bold=True)
            elif style == "script":
                _cell_text(cells[i], text, color=T.COLOR_SCRIPT_GREY)
            else:
                _cell_text(cells[i], text, italic=True, color=T.COLOR_DIRECTION_GREY)
    for i, w in enumerate(widths_cm):
        table.columns[i].width = Cm(w)
    for row in table.rows:
        for i, w in enumerate(widths_cm):
            row.cells[i].width = Cm(w)
    return table


def _kind(concept):
    if concept.get("organic"):
        return "organic"
    if concept.get("kind"):
        return concept["kind"]
    beats = concept.get("script", [])
    if beats and not any(b.get("line") for b in beats):
        return "interview"
    return "script"


def build_video_ad_scripts(data, out_dir, workspace=None):
    """Video Ad Scripts, client-friendly layout (Liam, 2026-10-22: "a lot easier
    to understand and way less AI commentary, whilst keeping good guidance").

    Per video: who is on camera, one plain line on what it is, how to film, and a
    table of takes. No timestamps, no beat labels, no audience or angle lines.
    """
    doc = T.new_document()
    meta = data.get("scripts", {})

    T.add_header_block(
        doc,
        client=data.get("client_business_name", ""),
        campaign=data.get("campaign", ""),
        prepared_by=data.get("prepared_by", "Maxalding Agency"),
        workspace=workspace,
    )

    if meta.get("summary"):
        doc.add_paragraph()
        T.add_subheading(doc, "WHAT WE NEED FROM YOU")
        for point in meta["summary"]:
            T.add_body(doc, f"- {point}")

    # Guidance only, vertical only. No mention of the VSL or 16:9 here.
    doc.add_paragraph()
    T.add_subheading(doc, "BEFORE YOU FILM")
    T.add_body(doc, "These are guides, not lines to learn. Say it your way and hit the "
                    "main points.", bold=True)
    # The default list assumes an indoor room with a window. Outdoor clients
    # (a pitch, an oval, a park) pass their own list in
    # scripts.recording_best_practice (Relentless Generation, 2026-10-22).
    for point in meta.get("recording_best_practice") or RECORDING_BEST_PRACTICE:
        T.add_body(doc, f"- {point}")

    for n, concept in enumerate(meta.get("concepts", []), start=1):
        kind = _kind(concept)
        name = concept.get("name", "")
        hooks = [h for h in concept.get("hooks", []) if h]
        beats = concept.get("script", [])

        doc.add_paragraph()
        # A plain client-facing title ("The parent video") can stand in for the
        # agency concept name ("Audience Addresser").
        T.add_subheading(doc, f"{n}. {concept.get('title', name).upper()}")
        if concept.get("talent"):
            T.add_label_line(doc, "On camera", concept["talent"])
        what = concept.get("what") or concept.get("intro")
        if what:
            T.add_body(doc, what)
        if kind == "organic":
            T.add_body(doc, "ORGANIC CONTENT, NOT AN AD SCRIPT.", bold=True)

        # How to film: the concept's own bullets plus any direction-only beats
        # (props, which hook needs what) on a scripted video.
        how = list(concept.get("how_to_film", []))
        if kind == "script":
            how += [b["direction"] for b in beats if b.get("direction") and not b.get("line")]
        if how:
            doc.add_paragraph()
            T.add_body(doc, "How to film", bold=True)
            for point in how:
                T.add_body(doc, f"- {point}")
        doc.add_paragraph()

        if kind == "script":
            rows = []
            test = concept.get("hook_test") and len(hooks) > 1
            for i, hook in enumerate(hooks if test else hooks[:1], start=1):
                rows.append([(f"Hook {i}" if test else "Opening line", "label"), (hook, "script")])
            middle = "\n".join(b["line"] for b in beats if b.get("line"))
            if middle:
                rows.append([("Middle" + (" (same after every hook)" if test else ""), "label"),
                             (middle, "script")])
            if concept.get("cta"):
                rows.append([("Ending", "label"), (concept["cta"], "script")])
            _table(doc, ["TAKE", "WHAT TO SAY"], rows, [3.5, 13.0])

        elif kind == "interview":
            rows = []
            # The opening line only gets its own row when the first question
            # does not already ask for it.
            if hooks and not (beats and beats[0].get("question")):
                rows.append([("Opening line", "label"),
                             ("Get it as one full sentence: " + hooks[0], "script")])
            for b in beats:
                q = b.get("question")
                steer = b.get("steer")
                if not q:
                    q, steer = b.get("label", ""), b.get("direction", "")
                rows.append([(q, "label"), (steer or "", "note")])
            _table(doc, ["QUESTION", "GET THEM TALKING ABOUT"], rows, [6.5, 10.0])
            # The end card and CTA audio are edit notes, not something the
            # client films, so they stay out of this doc (Liam, 2026-10-22).

        else:  # organic
            labels = concept.get("hook_labels", [])
            rows = []
            for i, hook in enumerate(hooks):
                idea = beats[i]["direction"] if i < len(beats) else ""
                rows.append([(labels[i] if i < len(labels) else f"Pillar {i + 1}", "label"),
                             (hook, "script"), (idea, "note")])
            _table(doc, ["PILLAR", "EXAMPLE OPENING LINE", "MORE IDEAS"], rows, [3.5, 5.0, 8.0])
            # Only the pillars table. Extra notes and "when a post runs as an
            # ad" read as commentary to the client (Liam, 2026-10-22).

    # No take checklist: Liam removed it as AI commentary (2026-10-22).

    filename = T.deliverable_filename(data["client_business_name"], "Video Ad Scripts", campaign=data.get("campaign"))
    out_path = os.path.join(out_dir, filename)
    doc.save(out_path)
    return out_path
