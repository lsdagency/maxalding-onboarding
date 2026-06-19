"""
Document 2: VSL Script (.docx) (System Prompt section 10).

A landing-page video, horizontal 16:9. Five-step formula in order: what it is,
why they need it, what they get, why to trust you, next step. No price, no
jargon, no marketing terminology. Transformation focus. Direction note in italics
then spoken line in grey, same timestamp format as Document 1.

Driven by data["vsl"].
"""

from __future__ import annotations

import os

from . import template as T

RECORDING_BEST_PRACTICE = [
    "Film horizontal 16:9.",
    "Camera on a tripod, framed wide enough for shoulders and above.",
    "Eyes to the lens, calm and conversational.",
    "Natural light facing a window.",
    "Quiet room, test a 5 second clip, use a mic.",
    "Clean, on-brand background.",
    "Steady pace, pause after key lines.",
]

STEP_LABELS = [
    "STEP 1: WHAT IT IS",
    "STEP 2: WHY THEY NEED IT",
    "STEP 3: WHAT THEY GET",
    "STEP 4: WHY TO TRUST YOU",
    "STEP 5: NEXT STEP",
]


def build_vsl_script(data, out_dir, workspace=None):
    doc = T.new_document()
    vsl = data.get("vsl", {})

    T.add_header_block(
        doc,
        client=data.get("client_business_name", ""),
        campaign=data.get("campaign", ""),
        prepared_by=data.get("prepared_by", "Maxalding Agency"),
        workspace=workspace,
    )

    doc.add_paragraph()
    T.add_body(doc, "Filming format: this is a landing-page video, filmed horizontal 16:9.", bold=True)

    doc.add_paragraph()
    T.add_subheading(doc, "RECORDING BEST PRACTICE")
    for point in RECORDING_BEST_PRACTICE:
        T.add_body(doc, f"- {point}")

    doc.add_paragraph()
    T.add_subheading(doc, "VSL SCRIPT")

    steps = vsl.get("steps", [])
    for i, step in enumerate(steps):
        label = step.get("label") or (STEP_LABELS[i] if i < len(STEP_LABELS) else f"STEP {i + 1}")
        timestamp = step.get("timestamp", "")
        doc.add_paragraph()
        T.add_timestamp(doc, f"{timestamp}  {label}".strip())
        if step.get("direction"):
            T.add_direction(doc, step["direction"])
        for line in step.get("lines", []):
            T.add_script_line(doc, line)

    filename = T.deliverable_filename(data["client_business_name"], "VSL Script")
    out_path = os.path.join(out_dir, filename)
    doc.save(out_path)
    return out_path
