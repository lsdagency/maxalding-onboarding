---
name: meta-lead-form
description: Write Meta (Facebook and Instagram) Lead Form (Instant Form) copy for a Maxalding client, as a standalone task. Triggers include "lead form copy", "instant form copy", "Meta lead form", "lead gen form", "write a lead form", or any request to produce the intro, questions, and completion screen copy for a Meta lead ad. Produces the branded LEAD FORM spreadsheet, never a chat list, and can sit alongside the ad copy in one workbook.
---

# Maxalding Meta Lead Form Copy

This skill writes the copy for a Meta Instant Form (lead form) for an onboarded client. It produces a branded spreadsheet tab, the same format family as the AD COPY and Creative Plan deliverables, and can be built into a combined workbook alongside the ad copy.

## Read first, every time
Read the shared Onboarding Feedback Log in full before writing (workspace folder, resolve with `MAXALDING_WORKSPACE`, default `./maxalding-workspace`). Apply every instruction in it. Then read the client's memory files (Audience, Brand, Marketing, KPIs) so the form uses the real ICP, offer, tagline, words-to-use and banned-copy list.

## Confirm the funnel first
A lead form is not always the right tool. If the client's funnel is a landing page that sells or books directly (no instant forms), say so and confirm with the user before writing. A lead form fits an enquiry or interest-capture step, where a person is handed to the client to follow up, not a direct book-and-pay offer.

## Delivering the file (do not hand-encode binaries)
Build the XLSX and save it into the session outputs directory, then let the user open it with Google Drive (the Cowork native upload moves the real bytes). Never hand-encode the workbook as base64 into a Drive create-file call: reproducing thousands of base64 characters corrupts the xlsx and it will not open. If the user wants it in a specific Drive folder, ask which one, but the file still travels via the outputs directory and the open-with-Google-Drive step. This applies to ad copy and lead form copy both.

## Read-only package, writable workspace
This package is read-only at runtime. Save the generated XLSX into the client workspace folder and upload it to the location the user provided.

## What you produce
One branded LEAD FORM spreadsheet tab (optionally combined with the AD COPY tab in the same workbook), built with the deterministic build module. Never a chat list, never hand-formatted. The tab is laid out as FIELD | COPY | CHARS under black section headers, with live =LEN() formulas on the length-limited fields.

## Lead form best practices (apply before writing)
Sourced from Meta's own guidance and current best practice. Keep the experience short and aligned with the ad.

Form type
- Prefer Higher intent (it adds a review step so the lead confirms before submitting), which improves lead quality. Use More volume only when the priority is raw volume and the follow-up can handle lower intent.

Keep it short
- Prefilled fields (name, email, phone) plus one or two qualifying questions outperform long forms. Do not ask more than you genuinely need. Every extra question lowers completion.

Intro
- Intro headline: state plainly what they get or what this is. No more than 60 characters.
- Intro description: set expectations. Say what the program is, who it is for, and what happens after they submit (for example, the team will be in touch to confirm). This is where alignment with the ad is won or lost: the form must deliver what the ad promised.

Questions
- List the prefilled fields, then one or two custom qualifying questions. Multiple choice qualifies better than free text and is easier to complete. Keep each question clear and under about 80 characters. Phrase questions to qualify (goal, timeframe, suburb), never to interrogate.

Privacy
- Include a short privacy line and the client's privacy policy URL. If the URL is not confirmed, flag it as a placeholder to confirm before launch.

Completion screen
- Completion headline: confirm they are in and reassure. No more than 60 characters.
- Completion description: tell them exactly what happens next (who will contact them and when, or to check email).
- CTA button: one clear next step (visit website, call the studio, download). Button text no more than 30 characters.

## Writing rules (same standard as all Maxalding copy)
- No em dashes, no en dashes, no exclamation marks anywhere.
- Apply the client's banned-copy list from the Brand memory. No weight-loss-as-headline or other client-specific bans.
- No negative framing of the person, even when negated. Lead with what becomes available to them.
- Check every line against Meta's Personal Attributes policy: do not assert or imply the viewer's body, weight or health.
- Match the client's tone and use their tagline where it fits (for example on the completion screen).

## Build it deterministically
Assemble the `lead_form` data dict (and the `ad_copy` dict if building the combined file) and build with the module:

    # combined ad copy + lead form in one workbook (default)
    python -m build.lead_form "<data>.json" --out "<dir>"
    # lead form tab only
    python -m build.lead_form "<data>.json" --out "<dir>" --lead-form-only

The JSON shape (lead_form is a list of sections, each with FIELD/COPY rows; add "limit" to a row to get a live =LEN and a build-time character check):

    {
      "client_business_name": "FIT Republik",
      "ad_copy": { "concepts": [...], "headlines": [...], "description": "..." },
      "lead_form": {
        "sections": [
          {"name": "FORM SETUP", "rows": [
            {"field": "Form name", "copy": "..."},
            {"field": "Form type", "copy": "..."}
          ]},
          {"name": "INTRO", "rows": [
            {"field": "Intro headline", "copy": "...", "limit": 60},
            {"field": "Intro description", "copy": "..."}
          ]},
          {"name": "QUESTIONS", "rows": [...]},
          {"name": "PRIVACY", "rows": [...]},
          {"name": "COMPLETION SCREEN", "rows": [
            {"field": "Completion headline", "copy": "...", "limit": 60},
            {"field": "Completion description", "copy": "..."},
            {"field": "CTA button text", "copy": "...", "limit": 30}
          ]}
        ]
      }
    }

The builder names the file `MAXALDING - [Client] - Meta Ad & Lead Form Copy.xlsx` (or `Meta Lead Form Copy` for lead-form-only) and checks every limited field against its Meta character limit before saving.

## Run the QA gate (mandatory)
After building, run the deterministic validator over the file and fix every error before handing over:

    python -m validator.cli "<output file>.xlsx"

It checks banned characters, banned words, positive-language, Meta personal-attributes compliance, the length limits, and the naming convention. The gate must pass with 0 errors.

## Before you hand over
- Output is the XLSX, not a chat list.
- Form is short: prefill plus one or two qualifying questions only.
- Intro says what they get and what happens next. Completion says who contacts them and when, with one CTA.
- Headlines and CTA within Meta limits (intro 60, completion 60, CTA 30).
- Zero em dashes, en dashes or exclamation marks. Client banned list clear. Meta personal-attributes clear.
- Confirm the upload location with the user, then upload.
