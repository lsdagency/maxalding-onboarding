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

    for section in sections:
        doc.add_paragraph()
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
            T.add_subheading(doc, heading)
            for line in extra.get("lines", []):
                T.add_body(doc, line)
            for placeholder in extra.get("placeholders", []):
                T.add_body(doc, f"[CLIENT ACTION: {placeholder}]", bold=True)

    filename = T.deliverable_filename(data["client_business_name"], "Landing Page Copy")
    out_path = os.path.join(out_dir, filename)
    doc.save(out_path)
    return out_path
