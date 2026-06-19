"""
Document 4: CRM Automation (.docx) (System Prompt section 12).

A short OVERVIEW (booking link stated once), then straight into AUTOMATION COPY.
No ClickUp brief, no process steps, no quality-control checklist, no Master Copy
Prompt. The deliverable is the email and SMS copy for each requested workflow.

Emails: numbered, bold subject, Delay, an italic direction note, then Subject /
Body / single CTA, with body and CTA in grey. SMS: numbered, Delay, italic note,
then the SMS copy in grey. Premium positioning of the consultation throughout.

Driven by data["crm"].
"""

from __future__ import annotations

import os

from . import template as T


def build_crm_automation(data, out_dir, workspace=None):
    doc = T.new_document()
    crm = data.get("crm", {})

    T.add_header_block(
        doc,
        client=data.get("client_business_name", ""),
        campaign=data.get("campaign", ""),
        prepared_by=data.get("prepared_by", "Maxalding Agency"),
        workspace=workspace,
    )

    doc.add_paragraph()
    T.add_subheading(doc, "OVERVIEW")
    for line in crm.get("overview", []):
        T.add_body(doc, line)
    if crm.get("booking_link"):
        T.add_label_line(doc, "Booking link", crm["booking_link"])

    doc.add_paragraph()
    T.add_subheading(doc, "AUTOMATION COPY")

    for workflow in crm.get("workflows", []):
        doc.add_paragraph()
        T.add_subheading(doc, workflow.get("name", "").upper())
        T.add_label_line(doc, "TRIGGER", workflow.get("trigger", ""))

        for n, message in enumerate(workflow.get("messages", []), start=1):
            mtype = message.get("type", "email").lower()
            doc.add_paragraph()
            if mtype == "sms":
                head = doc.add_paragraph()
                run = head.add_run(f"{n}. SMS")
                T._set_run_font(run, size=T.SIZE_BODY, bold=True, color=T.COLOR_BLACK)
                T.add_label_line(doc, "Delay", message.get("delay", ""))
                if message.get("note"):
                    T.add_direction(doc, message["note"])
                if message.get("body"):
                    T.add_script_line(doc, message["body"])
            else:
                head = doc.add_paragraph()
                run = head.add_run(f"{n}. {message.get('subject', '')}")
                T._set_run_font(run, size=T.SIZE_BODY, bold=True, color=T.COLOR_BLACK)
                T.add_label_line(doc, "Delay", message.get("delay", ""))
                if message.get("note"):
                    T.add_direction(doc, message["note"])
                if message.get("subject"):
                    T.add_label_line(doc, "Subject", message["subject"])
                if message.get("body"):
                    T.add_script_line(doc, message["body"])
                if message.get("cta"):
                    T.add_script_line(doc, message["cta"])

    filename = T.deliverable_filename(data["client_business_name"], "CRM Automation")
    out_path = os.path.join(out_dir, filename)
    doc.save(out_path)
    return out_path
