"""
Document 3: Landing Page Copy (.docx) (System Prompt section 11).

Substantial, social-proof-led conversion copy modelled on premium coaching sales
pages. Recommended sections in order, one consistent premium CTA throughout,
missing assets listed as clearly labelled client-action placeholders. No internal
production notes in the client-facing sections.

Driven by data["landing_page"].
"""

from __future__ import annotations

import os

from . import template as T

# Recommended section order (System Prompt section 11). The agent supplies the
# copy per section; this is the default scaffold when an order is not given.
DEFAULT_SECTION_ORDER = [
    "Top bar",
    "Hero",
    "Social proof strip",
    "The reality",
    "Why a real coach makes the difference",
    "Real results / transformations",
    "Meet the coach",
    "Testimonials grid",
    "Who this is for",
    "How the consultation works",
    "FAQ and objections",
    "Guarantee",
    "Final CTA",
    "Footer",
]


def _wireframe_block(doc, heading, section):
    """One block of the page laid out like a wireframe: the heading, a line on
    how the block looks, then every piece of copy labelled by the element it
    sits in (Headline, Button, Card 1 and so on). Opt in per section with
    "layout" and "elements": [[label, text], ...] (Liam, 2026-11-19: the page
    was hard to picture from a run of plain paragraphs)."""
    from .video_ad_scripts import _table

    T.add_subheading(doc, heading)
    if section.get("layout"):
        T.add_direction(doc, f"How it looks: {section['layout']}")
    rows = [[(label, "label"), (text, "script")] for label, text in section["elements"]]
    for placeholder in section.get("placeholders", []):
        rows.append([("Client to provide", "label"), (placeholder, "note")])
    _table(doc, ["ELEMENT", "COPY"], rows, [4.0, 12.5])


def build_landing_page(data, out_dir, workspace=None):
    doc = T.new_document()
    lp = data.get("landing_page", {})

    T.add_header_block(
        doc,
        client=data.get("client_business_name", ""),
        campaign=data.get("campaign", ""),
        prepared_by=data.get("prepared_by", "Maxalding Agency"),
        workspace=workspace,
    )

    doc.add_paragraph()
    T.add_subheading(doc, "LANDING PAGE COPY")

    sections = lp.get("sections")
    if not sections:
        sections = [{"title": title, "lines": []} for title in DEFAULT_SECTION_ORDER]

    # The page at a glance: a numbered run of the blocks top to bottom, so the
    # reader can picture the page before reading any copy (Liam, 2026-11-19).
    if lp.get("overview"):
        doc.add_paragraph()
        T.add_subheading(doc, "THE PAGE AT A GLANCE")
        for i, line in enumerate(lp["overview"], start=1):
            T.add_body(doc, f"{i}. {line}")

    block = 0
    for section in sections:
        doc.add_paragraph()
        if section.get("elements"):
            block += 1
            _wireframe_block(doc, f"BLOCK {block}: {section.get('title', '').upper()}", section)
            continue
        T.add_subheading(doc, section.get("title", "").upper())
        for line in section.get("lines", []):
            T.add_body(doc, line)
        for placeholder in section.get("placeholders", []):
            T.add_body(doc, f"[CLIENT ACTION: {placeholder}]", bold=True)

    # Optional separate booking and thank-you pages.
    for extra_key, heading in (("booking_page", "BOOKING PAGE"),
                               ("thank_you_page", "THANK YOU PAGE")):
        extra = lp.get(extra_key)
        if extra:
            doc.add_paragraph()
            if extra.get("elements"):
                _wireframe_block(doc, heading, extra)
                continue
            T.add_subheading(doc, heading)
            for line in extra.get("lines", []):
                T.add_body(doc, line)
            for placeholder in extra.get("placeholders", []):
                T.add_body(doc, f"[CLIENT ACTION: {placeholder}]", bold=True)

    filename = T.deliverable_filename(data["client_business_name"], "Landing Page Copy", campaign=data.get("campaign"))
    out_path = os.path.join(out_dir, filename)
    doc.save(out_path)
    return out_path
