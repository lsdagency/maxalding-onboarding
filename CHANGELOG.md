# Changelog

All notable changes to the Maxalding Onboarding plugin. Each rule change is traceable to the client and date it came from via rules/rules.yaml and the Onboarding Feedback Log.

## [0.11.1] - 2026-06-26

### Added
- Per-client `premium_lead_magnet` flag (client data, default true). For a low-ticket, local, in-person client whose genuine front end is a free trial or session (for example a $50 to $60 per session PT offering a free starter session), set it to false. build/build_all then waives the premium-framing QA rule for that client so a legitimately named free offer passes the gate, and the standalone validator can waive it with `python -m validator.cli ... --skip-rules premium-framing`. High-ticket clients are unaffected (default true keeps the premium "no free" framing). From the Peak with Hamza run (2026-06-26).

### Changed
- validator/validate.py: `validate_paths` gains an optional `skip_rules` argument that drops violations of the named rules from the result. validator/cli.py gains `--skip-rules`. rules/rules.yaml and references/premium-positioning.md document the flag and that premium framing is scoped to high-ticket offers only.

### Reaffirmed
- No KPIs anywhere in the client-facing Creative Plan (section, tab or rows). Already enforced (references/creative-plan-spec.md, rules.yaml brand_pack_no_kpis), recorded as a deliberate standing rule (Peak with Hamza, 2026-06-26).

## [0.11.0] - 2026-06-26

### Changed
- CRM Automation deliverable now produces the fixed funnel: four workflows in a set order every time (Lead Follow Up, Booked Call Confirmation, No Show Rebook, Long Term Nurture), with the timing and message type of every step locked to the funnel spec. Replaces the old flexible menu that let the agent pick and rename workflows, which was producing the wrong automation copy. Updated in agents/lifecycle-crm.md and references/automation-copy-guidelines.md.
- CRM Automation deliverable drops the OVERVIEW section: no overview, no instructions or prompt and no booking-link preamble at the start, just the automation copy. build/crm_automation.py renders straight into AUTOMATION COPY.

### Folded in from the funnel spec
- Standard funnel automations defined by the Automation Workflow doc: Lead Follow Up (12 steps), Booked Call Confirmation (8 steps), No Show Rebook (6 steps), Long Term Nurture (6 fortnightly emails) (2026-06-26).

## [0.10.2] - 2026-06-24

### Changed
- Ad copy rules: post copy must not end with a full stop (it reads unnatural in an ad), and lean a little more into emoji (a few across the set where they fit, some posts with none, never one-per-row). Updated in the meta-ad-copy skill and the Creative Plan AD COPY spec.

### Added
- Validator: post copy ending with a full stop is now flagged as a warning (rule post-copy-punctuation), scoped to the AD COPY POST COPY column.

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
