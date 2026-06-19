"""
Document 1: Video Ad Scripts (.docx) (System Prompt section 9).

Vertical 9:16 social scripts for the eight video concepts (Creative Tracker rows
6 to 13). Guidance-only context block, recording best practice, hook A/B/C per
concept (all three filmed), timestamped script with direction notes only where
needed, and one firm CTA per concept.

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


def build_video_ad_scripts(data, out_dir, workspace=None):
    doc = T.new_document()
    meta = data.get("scripts", {})

    T.add_header_block(
        doc,
        client=data.get("client_business_name", ""),
        campaign=data.get("campaign", ""),
        prepared_by=data.get("prepared_by", "Maxalding Agency"),
        workspace=workspace,
    )

    # Context block, in bold: scripts are guidance only.
    doc.add_paragraph()
    T.add_body(
        doc,
        "These scripts are guidance only and must not be read word for word. "
        "Say it in your own words. Be natural and creative while hitting the key "
        "beats and timing.",
        bold=True,
    )

    # Filming format. Vertical only. No mention of the VSL or 16:9 here.
    doc.add_paragraph()
    T.add_body(doc, "Filming format: these are filmed vertical 9:16.", bold=True)

    doc.add_paragraph()
    T.add_subheading(doc, "RECORDING BEST PRACTICE")
    for point in RECORDING_BEST_PRACTICE:
        T.add_body(doc, f"- {point}")

    for i, concept in enumerate(meta.get("concepts", []), start=1):
        doc.add_paragraph()
        T.add_subheading(doc, f"CONCEPT {i}: {concept.get('name', '').upper()}")
        T.add_label_line(doc, "Format", concept.get("format", "Vertical 9:16"))
        T.add_label_line(doc, "Talent", concept.get("talent", ""))
        T.add_label_line(doc, "Audience", concept.get("audience", ""))
        T.add_label_line(doc, "Angle", concept.get("angle", ""))

        if concept.get("intro"):
            doc.add_paragraph()
            T.add_body(doc, concept["intro"])

        doc.add_paragraph()
        T.add_body(doc, "Hook Options (film all three):", bold=True)
        for letter, hook in zip("ABC", concept.get("hooks", [])):
            T.add_body(doc, f"Option {letter}:")
            T.add_script_line(doc, hook)

        doc.add_paragraph()
        T.add_body(doc, "Script:", bold=True)
        for beat in concept.get("script", []):
            # beat = {timestamp, label, line, direction(optional)}
            T.add_timestamp(doc, f"{beat.get('timestamp', '')}  {beat.get('label', '')}".strip())
            if beat.get("direction"):
                T.add_direction(doc, beat["direction"])
            if beat.get("line"):
                T.add_script_line(doc, beat["line"])

        doc.add_paragraph()
        T.add_body(doc, "CTA (film this ending):", bold=True)
        if concept.get("cta"):
            T.add_script_line(doc, concept["cta"])

        T.add_divider(doc)

    filename = T.deliverable_filename(data["client_business_name"], "Video Ad Scripts")
    out_path = os.path.join(out_dir, filename)
    doc.save(out_path)
    return out_path
