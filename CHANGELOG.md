# Changelog

All notable changes to the Maxalding Onboarding plugin. Each rule change is traceable to the client and date it came from via rules/rules.yaml and the Onboarding Feedback Log.

## [0.10.1] - 2026-06-24

### Added
- meta-lead-form: the lead form QUESTIONS section now includes the Meta data-use description, the small box that sits with the form fields and tells people how their information will be used or shared.

## [0.10.0] - 2026-06-24

### Added
- meta-ad-copy skill: standalone Meta ad copy requests (outside a full onboarding) now trigger the AD COPY rules and produce the spreadsheet directly. build/ad_copy.py reuses the Creative Plan AD COPY builder, so the format and live =LEN formulas are identical to the onboarding deliverable.
- meta-lead-form skill: standalone Meta Lead Form (Instant Form) copy, with best practices folded in (higher-intent form type, prefilled fields plus one or two qualifying questions, an expectation-setting intro aligned with the ad, and a completion screen with one CTA). build/lead_form.py builds a branded LEAD FORM tab and a combined Ad & Lead Form workbook.
- Mandatory QA gate step in both new skills, plus an ask-for-the-upload-location step before any file is uploaded to Google Drive.

### Changed
- Registered the new deliverables (Meta Ad Copy, Meta Lead Form Copy, Meta Ad & Lead Form Copy) in the filename helper, validator/rules.py and rules/rules.yaml so the QA gate accepts and checks them.

### Folded in from the feedback log
- Standalone ad copy must be delivered as the AD COPY spreadsheet (never a chat list) and the variations must be fluid, not length-clustered near the limit. Ask for the upload location before uploading (2026-06-24).

## [0.9.0] - 2026-06-19

First packaged release as an installable Claude Code plugin. Consolidates every rule and correction to date into one read-only package with writable state held in the workspace folder.

### Added
- Plugin manifest and loadable structure (agents and skills auto-discovered).
- Orchestrator agent that runs the four-stage workflow, the hard input gate, the Stage 2 confirm step and the QA approval gate.
- Six specialist subagents: intake-research, creative-plan, scriptwriting, conversion-copy, lifecycle-crm, and a separate compliance-qa reviewer.
- Python build module with one shared template (fonts, header, logo, styling) plus generators for the Creative Plan XLSX and the four .docx documents, implementing every formatting and content rule in the System Prompt.
- Deterministic validator (the QA gate): scans outputs and build-script strings for em and en dashes, exclamation marks, ellipses, banned words, Meta risk patterns (weight figures, body-attribute phrasing), length limits (post copy 125, headline 40, description 25), the naming convention, no date in the header, and the premium-framing check. Wired as the QA step and as a git pre-commit hook.
- Machine-readable rules file (rules/rules.yaml) derived from the feedback log, with provenance.
- Regression eval set so the prompt can change without regressions.
- README, this changelog, and .gitignore that keeps writable state out of the package.

### Folded in from the feedback log
- File naming convention MAXALDING - [Client] - [Deliverable] with spaces and standard hyphens, superseding the older em-dash Brand Pack convention (2026-06-18).
- Brand Pack KPIs section removed; CAMPAIGN column removed from the Creative Tracker; FILE TYPE formula references the FORMAT column (2026-06-18).
- Static per-concept layouts and imagery direction, including the imageless ugly-ad option (2026-06-18).
- Meta compliance standing pass for all paid creative (2026-06-18).
- Video Ad Scripts refinements: vertical 9:16 only, one firm CTA per concept, direction notes only where needed, guidance-only context block (2026-06-18).
- AD COPY tab restructure: distinct concepts, 5 posts each, shared headlines and one description, no STATUS or CTA columns (2026-06-18).
- Documents: no date in headers, premium positioning of the lead magnet, social-proof-led landing page, CRM reduced to overview plus automation copy, logo from the workspace folder (2026-06-18).
- Audience Addresser concept and its age, role and situation hooks (2026-05-21).
- Helvetica Neue set explicitly on every run (2026-05-20).
- Positive-language rule and the document gate (2026-05-19).
- Feedback log moved to the workspace folder (2026-05-19).
