"""
Creative Plan XLSX generator (System Prompt section 8).

Two tabs:
  1. BRAND PACK       label/value with black section headers, NO KPIs section
  2. CREATIVE TRACKER dropdowns, live formulas, no DATE column

Ad copy is NOT a tab here. It ships as its own workbook, built by
build/ad_copy.py (Feedback 2026-08-06, Kure by Konrad). The AD COPY tab builder
below (_build_ad_copy) is retained because build/ad_copy.py reuses it, so the
standalone workbook keeps byte-for-byte identical layout and styling.

The generator takes a structured `data` dict (the campaign content the agents
produce) and lays it out to spec. See evals/cases/sample_client.json for the
exact shape. Styling comes from build/template.py.
"""

from __future__ import annotations

from . import template as T

RESOLUTION_STRING = "1080 x 1350 (4:5) / 1080 x 1920 (9:16)"

STATUS_OPTIONS = ["Briefed", "Filmed", "In Edit", "Signed Off", "Live"]
PLATFORM_OPTIONS = ["FACEBOOK + INSTAGRAM", "FACEBOOK", "INSTAGRAM", "TIKTOK"]
DEFAULT_PLATFORM = "FACEBOOK + INSTAGRAM"
DEFAULT_STATUS = "Briefed"

# Canonical 14-row tracker template: seven statics then seven videos.
# The static set is the coach template (Feedback 2026-08-11, Xcelerate
# Performance). Gyms are likely to differ; scope either half through
# tracker_concepts.
CANONICAL_TRACKER = [
    ("STATIC", "Problem > Solution"),
    ("STATIC", "Incentive"),
    ("STATIC", "Benefit"),
    ("STATIC", "Social Proof (Review)"),
    ("STATIC", "Social Proof (Progress)"),
    ("STATIC", "Location"),
    ("STATIC", "Audience Addresser"),
    ("VIDEO", "Problem > Solution"),
    ("VIDEO", "Social Proof (Client Interview)"),
    ("VIDEO", "Pattern Interrupt"),
    ("VIDEO", "Storytelling (Full Voiceover B-Roll)"),
    ("VIDEO", "Benefit"),
    ("VIDEO", "Incentive"),
    ("VIDEO", "Audience Addresser"),
]

TRACKER_COLUMNS = [
    "#", "FORMAT", "RESOLUTION", "STATUS", "PLATFORM", "FILE TYPE",
    "AUDIENCE", "CONCEPT", "HOOK GUIDANCE", "BEATS", "DETAILS",
    "EDITING DIRECTION", "FILMING DIRECTION", "SCRIPT", "FINAL ASSET",
]

# No DATE column (Liam, 2026-10-22): the tracker starts #, FORMAT.
TRACKER_WIDTHS = {
    "A": 5, "B": 10, "C": 28, "D": 12, "E": 22, "F": 10, "G": 30,
    "H": 18, "I": 38, "J": 34, "K": 40, "L": 34, "M": 34, "N": 30, "O": 16,
}


def _write_row(ws, row, values):
    for i, value in enumerate(values, start=1):
        cell = ws.cell(row=row, column=i, value=value)
        T.plan_align(cell, i)
    return row


# ---------------------------------------------------------------------------
# Tab 1: BRAND PACK
# ---------------------------------------------------------------------------
def _build_brand_pack(wb, data):
    ws = wb.active
    ws.title = "BRAND PACK"
    T.set_column_widths(ws, {"A": 34, "B": 90})

    bp = data["brand_pack"]
    # Section order is fixed. No KPIs section (Feedback 2026-06-18).
    sections = [
        ("CHANNELS", bp.get("channels", [])),
        ("AUDIENCE", bp.get("audience", [])),
        ("TONE OF VOICE", bp.get("tone_of_voice", [])),
        ("OFFER", bp.get("offer", [])),
        ("BRAND POSITIONING", bp.get("brand_positioning", [])),
    ]

    row = 1
    for title, rows in sections:
        # Black section header spanning both columns.
        ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=2)
        cell = ws.cell(row=row, column=1, value=title)
        T.style_header_cell(cell, vertical=T.PLAN_VERTICAL)
        ws.row_dimensions[row].height = T.XLSX_MIN_ROW_HEIGHT
        row += 1
        for label, value in rows:
            lab = ws.cell(row=row, column=1, value=label)
            T.style_body_cell(lab, vertical=T.PLAN_VERTICAL)
            lab.font = T.xlsx_font(bold=True)
            val = ws.cell(row=row, column=2, value=value)
            T.style_body_cell(val, vertical=T.PLAN_VERTICAL)
            ws.row_dimensions[row].height = T.XLSX_MIN_ROW_HEIGHT
            row += 1
    return ws


# ---------------------------------------------------------------------------
# Tab 2: CREATIVE TRACKER
# ---------------------------------------------------------------------------
def _build_tracker(wb, data):
    ws = wb.create_sheet("CREATIVE TRACKER")
    T.set_column_widths(ws, TRACKER_WIDTHS)

    # Header row.
    for i, name in enumerate(TRACKER_COLUMNS, start=1):
        cell = ws.cell(row=1, column=i, value=name)
        T.plan_align(cell, i, header=True)
    ws.row_dimensions[1].height = T.XLSX_MIN_ROW_HEIGHT
    ws.freeze_panes = "A2"

    audience_line = data.get("audience_line", "")
    rows = data.get("tracker", [])
    video_scripts_file = data.get("video_scripts_filename", "")

    # The canonical 13 rows are the default. A client may scope or extend the
    # set with tracker_concepts: a list of [FORMAT, CONCEPT] pairs (statics
    # first), for example adding an extra objection-angle video concept.
    concept_rows = data.get("tracker_concepts") or CANONICAL_TRACKER

    for idx, (fmt, concept) in enumerate(concept_rows):
        r = idx + 2
        content = rows[idx] if idx < len(rows) else {}
        is_static = fmt == "STATIC"
        script_value = "" if is_static else (content.get("script") or video_scripts_file)
        values = [
            idx + 1,                                   # A #
            fmt,                                       # B FORMAT
            RESOLUTION_STRING,                         # C RESOLUTION
            content.get("status", DEFAULT_STATUS),     # D STATUS
            content.get("platform", DEFAULT_PLATFORM), # E PLATFORM
            None,                                      # F FILE TYPE (formula)
            audience_line,                             # G AUDIENCE (identical)
            concept,                                   # H CONCEPT
            content.get("hook", ""),                   # I HOOK
            content.get("beats", ""),                  # J BEATS
            content.get("details", ""),                # K DETAILS
            content.get("editing", ""),                # L EDITING DIRECTION
            content.get("filming", ""),                # M FILMING DIRECTION
            script_value,                              # N SCRIPT
            content.get("final_asset", ""),            # O FINAL ASSET
        ]
        _write_row(ws, r, values)
        # FILE TYPE is always a formula referencing the FORMAT column (B).
        ws.cell(row=r, column=6, value=f'=IF(B{r}="STATIC","JPG","MP4")')
        T.plan_align(ws.cell(row=r, column=6), 6)
        ws.row_dimensions[r].height = T.XLSX_TRACKER_ROW_HEIGHT

    # Existing post ads: proven organic posts to run as ads (Use Existing Post).
    # Appended after the canonical rows. Each is a dict of tracker fields.
    n_canon = len(concept_rows)
    existing = data.get("existing_posts", [])
    for j, post in enumerate(existing):
        idx = n_canon + j
        r = idx + 2
        values = [
            idx + 1,                                       # A #
            post.get("format", "EXISTING POST"),           # B FORMAT
            post.get("resolution", "As posted"),           # C RESOLUTION
            post.get("status", "Signed Off"),              # D STATUS
            post.get("platform", DEFAULT_PLATFORM),        # E PLATFORM
            None,                                          # F FILE TYPE (formula)
            audience_line,                                 # G AUDIENCE
            post.get("concept", "Existing Post Ad"),       # H CONCEPT
            post.get("hook", ""),                          # I HOOK
            post.get("beats", ""),                         # J BEATS
            post.get("details", ""),                       # K DETAILS
            post.get("editing", ""),                       # L EDITING DIRECTION
            post.get("filming", ""),                       # M FILMING DIRECTION
            "",                                            # N SCRIPT (blank)
            post.get("final_asset", ""),                   # O FINAL ASSET (post URL)
        ]
        _write_row(ws, r, values)
        ws.cell(row=r, column=6, value=f'=IF(B{r}="STATIC","JPG","MP4")')
        T.plan_align(ws.cell(row=r, column=6), 6)
        ws.row_dimensions[r].height = T.XLSX_TRACKER_ROW_HEIGHT

    last = n_canon + len(existing) + 1
    # Dropdowns on STATUS (D) and PLATFORM (E).
    T.add_dropdown(ws, f"D2:D{last}", STATUS_OPTIONS)
    T.add_dropdown(ws, f"E2:E{last}", PLATFORM_OPTIONS)
    return ws


# ---------------------------------------------------------------------------
# Tab 3: AD COPY
# ---------------------------------------------------------------------------
def _build_ad_copy(wb, data):
    ws = wb.create_sheet("AD COPY")
    T.set_column_widths(ws, {"A": 5, "B": 22, "C": 90, "D": 10})

    # Header row: # | CONCEPT | POST COPY | CHARS. No STATUS, no CTA columns.
    for i, name in enumerate(["#", "CONCEPT", "POST COPY", "CHARS"], start=1):
        cell = ws.cell(row=1, column=i, value=name)
        T.style_header_cell(cell)
    ws.row_dimensions[1].height = T.XLSX_MIN_ROW_HEIGHT
    ws.freeze_panes = "A2"

    ad = data.get("ad_copy", {})
    row = 2
    n = 1
    for block in ad.get("concepts", []):
        concept = block.get("concept", "")
        for post in block.get("posts", []):
            ws.cell(row=row, column=1, value=n)
            ws.cell(row=row, column=2, value=concept)
            ws.cell(row=row, column=3, value=post)
            ws.cell(row=row, column=4, value=f"=LEN(C{row})")
            for c in range(1, 5):
                T.style_body_cell(ws.cell(row=row, column=c))
            ws.row_dimensions[row].height = T.XLSX_MIN_ROW_HEIGHT
            row += 1
            n += 1

    # Blank spacer row.
    row += 1

    # Shared HEADLINES block (label cell drives the validator's headline tag).
    hcell = ws.cell(row=row, column=2, value="HEADLINES")
    T.style_body_cell(hcell)
    hcell.font = T.xlsx_font(bold=True)
    row += 1
    for headline in ad.get("headlines", []):
        ws.cell(row=row, column=2, value=headline)
        ws.cell(row=row, column=4, value=f"=LEN(B{row})")
        T.style_body_cell(ws.cell(row=row, column=2))
        T.style_body_cell(ws.cell(row=row, column=4))
        ws.row_dimensions[row].height = T.XLSX_MIN_ROW_HEIGHT
        row += 1

    row += 1

    # One DESCRIPTION.
    dcell = ws.cell(row=row, column=2, value="DESCRIPTION")
    T.style_body_cell(dcell)
    dcell.font = T.xlsx_font(bold=True)
    row += 1
    description = ad.get("description", "")
    ws.cell(row=row, column=2, value=description)
    ws.cell(row=row, column=4, value=f"=LEN(B{row})")
    T.style_body_cell(ws.cell(row=row, column=2))
    T.style_body_cell(ws.cell(row=row, column=4))
    return ws


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# B-ROLL LIST (Liam, 2026-10-22): a worksheet of specific clips for the client
# to film, each one tied to the ads it feeds, so B-Roll stops being a vague ask.
# Built whenever data["broll"] has rows. Per-client Creative Plan scripts call
# build_broll_sheet directly.
# ---------------------------------------------------------------------------
BROLL_COLUMNS = ["#", "CLIP", "WHERE AND WHEN", "HOW TO FILM", "LENGTH",
                 "USED IN", "WHO'S IN SHOT", "STATUS", "FINAL ASSET"]
BROLL_WIDTHS = {"A": 5, "B": 34, "C": 26, "D": 40, "E": 10, "F": 30,
                "G": 26, "H": 12, "I": 16}
BROLL_STATUS_OPTIONS = ["To film", "Filmed", "Uploaded"]


def build_broll_sheet(wb, rows, title="B-ROLL LIST"):
    """rows: list of dicts with clip, where, how, length, used_in, who."""
    ws = wb.create_sheet(title)
    T.set_column_widths(ws, BROLL_WIDTHS)
    for i, name in enumerate(BROLL_COLUMNS, start=1):
        T.plan_align(ws.cell(row=1, column=i, value=name), i, header=True)
    ws.row_dimensions[1].height = T.XLSX_MIN_ROW_HEIGHT
    ws.freeze_panes = "A2"
    for idx, b in enumerate(rows):
        r = idx + 2
        values = [idx + 1, b.get("clip", ""), b.get("where", ""), b.get("how", ""),
                  b.get("length", ""), b.get("used_in", ""), b.get("who", ""),
                  b.get("status", "To film"), b.get("final_asset", "")]
        for c, value in enumerate(values, start=1):
            T.plan_align(ws.cell(row=r, column=c, value=value), c)
        ws.row_dimensions[r].height = 75
    if rows:
        T.add_dropdown(ws, f"H2:H{len(rows) + 1}", BROLL_STATUS_OPTIONS)
    return ws


def build_creative_plan(data, out_dir):
    import os
    import openpyxl

    wb = openpyxl.Workbook()
    _build_brand_pack(wb, data)
    _build_tracker(wb, data)
    if data.get("broll"):
        build_broll_sheet(wb, data["broll"])
    # No AD COPY tab: ad copy ships as its own workbook via build/ad_copy.py.

    filename = T.deliverable_filename(data["client_business_name"], "Creative Plan", campaign=data.get("campaign"))
    out_path = os.path.join(out_dir, filename)
    wb.save(out_path)
    return out_path
