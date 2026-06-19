---
name: client-onboarding
description: Onboard a new Maxalding Agency fitness client. Triggers include "onboard new client", "run onboarding", "set up client", "process onboarding docs", "new client setup", or when the user uploads a Brand Campaign Document or Creative Strategy Brief. Runs the four-stage workflow: read documents, build memory and the campaign spine, build the Creative Plan XLSX, and produce the four deliverable documents, all gated by the deterministic QA validator.
---

# Maxalding Client Onboarding

This skill runs the full onboarding for a new fitness client and produces a complete, ready-to-use campaign asset set: a Creative Plan spreadsheet and four campaign documents, every one looking and reading like it came from the same agency on the same campaign.

The work is split across an orchestrator and specialist subagents (see the agents folder). The orchestrator owns the workflow and the gates; the specialists own one craft each; a separate compliance and QA reviewer holds the final line. This file is the operating spec. The reference files carry the detailed rules.

## Read first, every time
Read the shared Onboarding Feedback Log in full before doing anything. It lives in the workspace folder, not in this package. Resolve the workspace with the MAXALDING_WORKSPACE environment variable (default ./maxalding-workspace). Apply every instruction in it. The most recent feedback wins on any conflict. If you cannot read it, stop and tell the user.

## Read-only package, writable workspace
This package is read-only at runtime. All writable state lives in the workspace folder: the logo (Maxalding Logo.png), the feedback log, per-client brand kits, and the generated client outputs. Never write into the package.

## Hard input gate
Required: at least one of the Brand Campaign Document or the Creative Strategy Brief. If neither is present, stop and say: "To run the onboarding I need at least one of the following: the Brand Campaign Document or the Creative Strategy Brief. Please upload one or both and I will get started." Do not work from memory. If only one is present, proceed but flag what is missing and recommend a human creative review. If the funnel goal is not stated anywhere, ask before proceeding.

## The four stages
1. Read everything (intake-research): the feedback log, every document, any transcript. Mine a transcript for the real voice, the genuine offer focus, real objections and authentic story. Reconcile conflicts.
2. Extract and confirm (intake-research): extract the five categories (Audience, Onboarding, Brand, Marketing, KPIs), save the memory files, and define the campaign spine: a single Core Message, a short Tagline, one support line. Then PAUSE and confirm the spine, ICP, offer, funnel and any conflicts with the user before building.
3. Build the Creative Plan XLSX (creative-plan): three tabs, using the Python build module.
4. Produce the four documents (scriptwriting, conversion-copy, lifecycle-crm): Video Ad Scripts, VSL Script, Landing Page Copy, CRM Automation, using the Python build module. After the Video Ad Scripts file is named, the Creative Plan SCRIPT column references it on the video rows.

Then run the QA gate (compliance-qa) over every output, fix anything it flags, and only then hand over.

## Building the files
Do not hand-format documents or spreadsheets. Assemble the structured data dict (see evals/cases/sample_client.json for the shape) and call the build module:

    python -m build.build_all "<client data>.json" --out "<workspace client folder>" --workspace "<workspace>"

The build module enforces Helvetica Neue on every run, the no-date header, the logo, grey script colour, the XLSX styling, dropdowns and live formulas. Tell the user to upload the Creative Plan to Google Drive manually (a Drive MCP cannot write Sheets).

## The QA gate
Run the deterministic validator before delivery:

    python -m validator.cli "<output dir>"

It enforces, with zero tolerance: no em or en dashes, exclamation marks or ellipses anywhere including build-script strings; no banned words outside rule-statement cells; no Meta risk patterns; length limits (post copy 125, headline 40, description 25); hook word counts; the naming convention; no date in headers; and premium framing. Fix every error and re-scan before sharing.

## Naming convention
MAXALDING - [Client Business Name] - [Deliverable], with spaces and standard hyphens with a space either side. Deliverables: Creative Plan (xlsx), Video Ad Scripts, VSL Script, Landing Page Copy, CRM Automation (docx).

## Feedback loop
If the user gave any correction during the session, append a dated entry to the workspace feedback log:

    ## [YYYY-MM-DD] - [Client name] - [brief summary]
    [What the feedback was, in plain language]
    [How to apply it in future runs]

If no feedback was given, append nothing. Confirm what was logged.

## Reference files
- references/writing-rules.md: global writing rules, banned characters, words, phrases, the positive-language rule.
- references/meta-compliance.md: Meta advertising policy pass for all paid creative.
- references/premium-positioning.md: premium framing of the lead magnet.
- references/creative-plan-spec.md: the Creative Plan XLSX detailed spec.
- references/script-guidelines.md: Video Ad Scripts and the Audience Addresser concept.
- references/vsl-guidelines.md: the VSL five-step formula.
- references/landing-page-structure.md: the conversion landing page structure.
- references/automation-copy-guidelines.md: CRM email and SMS copy rules.

## Skill invocations (mandatory points)
Apply the relevant expertise before writing each asset: ad-creative before any Creative Tracker content; ads, ad-creative and copywriting before Ad Copy; ad-creative before Video Ad Scripts; ads (funnel-stage thinking) before the VSL; copywriting before Landing Page Copy; email-sequence before any CRM email copy.
