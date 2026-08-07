# Changelog

All notable changes to the Maxalding Onboarding plugin. Each rule change is traceable to the client and date it came from via rules/rules.yaml and the Onboarding Feedback Log.

## [0.17.0] - 2026-08-07

### Changed
- Video Ad Scripts: ONE hook per concept, and it must CHAIN into the script body. The Option A/B/C menu is retired. The hook is the first spoken line of the take and the body's first line continues the thought, never restates it (hook "One of my clients came to me tired" followed by body "He came to me tired" is the failure). Three swappable hooks over one fixed body could never truly chain: hooks either disconnected from the body (Amir's original flag) or, once tied in, duplicated the body's opening line (Liam's follow-up flag). Write hook plus body as one continuous spoken piece, read aloud back to back before accepting. Updated in agents/scriptwriting.md, skills/client-onboarding/references/script-guidelines.md, rules/rules.yaml (hook_style.video, new hook_body_chaining), build/video_ad_scripts.py (renders "Hook (the opening line)" from the single hook; legacy hook lists fall back to the first entry), build/build_all.py docstring, and the handover email template. The Audience Addresser hook is now one callout built from the strongest of age, role or situation. Creative Tracker HOOK GUIDANCE mirroring is unchanged and now trivially identical to the script hook. From Liam's BodyShaping feedback (2026-08-07).

## [0.16.0] - 2026-08-06

### Changed
- Creative Tracker: the HOOK column is renamed HOOK GUIDANCE and now carries ONE hook on a single line, unlabelled, instead of three labelled variations. In practice only one hook was ever used off the tracker, so the column is now guidance: it shows at a glance how the video is likely to open and set up. Generate several angles with the ad-hooks skill, then pick the strongest and perfect it. From Liam's Kure by Konrad feedback (2026-08-06).
- The Video Ad Scripts document is deliberately UNCHANGED and still carries three spoken hook options (Option A, B, C, all filmed). Option A must now be written as the strongest of the three, because build_all mirrors Option A into the tracker's HOOK GUIDANCE cell.

### Added
- Validator rule `hook-single`: a tracker hook cell holding more than one line, or carrying a legacy "Hook 1:" label, is an error. Uses a new `hook_cell` segment kind for the whole cell, because a per-line segment cannot tell how many hooks a cell holds. Replaces the old `hook-label` rule, which enforced the three-option format.

### Fixed
- build_all._sync_video_hooks assumed the canonical five statics came first (`_STATIC_TRACKER_ROWS = 5`) and mapped script concepts onto tracker rows by that fixed offset. Any plan scoped through `tracker_concepts` with fewer statics, or none, had its hooks written onto the wrong rows. Video rows are now derived from `tracker_concepts`, so the mapping follows the actual plan. Caught by the new hook-single rule on a zero-static plan.
- Tracker and script hooks could silently diverge when a pack was built by calling the generators directly instead of going through `build_all`, which is what happened on the first Kure build. The sync is now documented in script-guidelines as mandatory: never hand-write the tracker hook cell.

## [0.15.0] - 2026-08-06

### Changed
- The Creative Plan is now TWO tabs (BRAND PACK, CREATIVE TRACKER). Ad copy is no longer a tab in it and always ships as its own workbook, built by build/ad_copy.py. build.build_all now builds the Meta Ad Copy workbook alongside the Creative Plan whenever ad_copy.concepts is present, so a full onboarding run still produces the copy. From Liam's Kure by Konrad feedback (2026-08-06).

### Added
- Deterministic post copy LENGTH VARIANCE rule (validator rule `post-copy-variance`). The character limit is a ceiling, not a target: a set of posts all written to roughly the same length reads machine-made whether it clusters at 125 or at 65. Across a file, post copy must span at least 45 characters end to end and at least one post must be 50 characters or under. Waive with `--skip-rules post-copy-variance`.
- First SET-LEVEL check in the validator (checks.run_set_checks, wired into validate.scan_file). Every previous check judged one cell at a time, which is why this failure was invisible to the QA gate: each cell was individually legal and only the whole set was wrong.
- Set-level evals in evals/run_evals.py covering both clustering modes (at the limit and mid-range), the no-short-post case, a healthy spread, and a below-threshold set.

### Fixed
- The canonical AD COPY example in evals/cases/sample_client.json was itself clustered (35 posts spanning 40 to 85 characters), so it taught the very pattern the fluidity rule forbids. Rewritten with a genuine spread (18 to 104 characters, 19 posts at or under 50). This was the root cause of the rule being missed repeatedly.
- The length-variance guidance was buried inside a long emoji bullet in creative-plan-spec.md. It now has its own explicit, measurable bullet, and the meta-ad-copy skill carries the same wording.

## [0.14.0] - 2026-07-16

### Added
- Client handover email template (references/handover-email.md), used at Stage 5 when the user asks to "draft me the email". Always a Gmail draft for review, never sent; To the client contact, CC chad@maxaldingagency.com; WhatsApp ("drop me a WhatsApp") as the questions channel, never "call me"; keeps the this-week push on the part 1 assets; points everything at one content upload folder and pushes B-Roll volume hard with client-specific categories and voiceover script-beat pairings (archival footage ask where the client's history offers one). From Liam's Fisica handover email review (2026-07-16).

### Changed
- Corrected the previous commit's guidance: never tell the client to upload as they go or that work starts with whatever lands first. Work starts once the full content set is in (script-guidelines.md, handover-email.md).

## [0.13.1] - 2026-07-16

### Fixed
- rules/rules.yaml version string had sat on 0.9.0 since the first packaged release while plugin.json was bumped each release (flagged by Liam). Both now read 0.13.1, and a new version eval in evals/run_evals.py fails whenever the two version strings differ, so a future bump cannot miss one.

## [0.13.0] - 2026-07-16

### Changed
- Social Proof video is now ONE concept in the client-interview format, for all coach and gym clients: the brand asks questions off camera, the script is a question set with guided responses (what to get the client to mention per answer), Hook 1 is always the client's introduction line ("Hi, I'm [NAME] and I've been training at [Client] for the past year"), Hooks 2 and 3 are pulled from the strongest answer moments in the edit (written as example pull-lines). The client records the same question set with several different clients or members, each interview becoming its own ad variant; the second Social Proof video concept is removed from the canonical set. From Liam's Fisica creative plan review (2026-07-16).
- One video concept per plan runs as a full voiceover over B-Roll with no talking head, Storytelling by default. Its FILMING DIRECTION is a concrete B-Roll shot list that doubles as the client's filming brief, deliberately pushing clients to supply B-Roll.
- Canonical tracker is now 12 rows (5 statics + 7 videos): build/creative_plan.py CANONICAL_TRACKER, references/creative-plan-spec.md and references/script-guidelines.md updated, evals/cases/sample_client.json restructured to match (interview-format social proof, voiceover storytelling, second social proof removed).
- Pattern Interrupt stays canonical but may be dropped via tracker_concepts when it does not serve the plan (dropped for Fisica).

## [0.12.0] - 2026-07-16

### Added
- Compulsory Instagram research step in Stage 1 (new references/instagram-research.md). The client's Instagram handle or profile URL is now a hard-gate input alongside the Brand Campaign Document / Creative Strategy Brief (waivable only by the user explicitly stating the client has no Instagram). intake-research scans the profile, captions and metadata, downloads and transcribes the five most recent videos (yt-dlp + ffmpeg + mlx_whisper), reads the visual style from extracted frames, saves everything under workspace/clients/[Client]/research/instagram/, and feeds real voice, recurring phrases, content formats and visual grammar into the Brand memory. An empty or "Music" transcript is recorded as a text-overlay-led reel, not a failure. Never log in or use credentials; if anonymous access fails, ask the user for the videos. Requested by Liam at the start of the Fisca onboarding (2026-07-16).
- Preflight checklist item: Instagram scan completed (or explicitly waived) with findings fed into the Brand memory.
- requirements.txt gains yt-dlp and static-ffmpeg for the research step; ffmpeg/ffprobe are symlinked into .venv/bin from the static-ffmpeg package.

### Changed
- SKILL.md hard input gate, Stage 1, preflight and reference list; agents/onboarding-orchestrator.md gate and Stage 1; agents/intake-research.md gains the scan procedure and prefers demonstrated Instagram language in the Brand "words to use".

## [0.11.2] - 2026-06-26

### Changed
- Ad copy emoji guidance strengthened: lean further into emoji (around a third of posts carry one, varied, never one-per-row, some left bare) and make them premium and on-brand (sparkle, white heart, warm heart, leaf, location pin, house, sun), never hype or loud ones (no fire, 100, rocket, heart-eyes). Updated in rules/rules.yaml, skills/meta-ad-copy/SKILL.md and references/creative-plan-spec.md. Liam had given this before and it was being lost, so it is now codified in all three places plus the feedback log. From the Peak with Hamza run (2026-06-26).
- Document logo width set to at least 1 inch (build/template.py DEFAULT_LOGO_WIDTH_CM 1.0 to 3.0, about 1.18 inches).

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

## [0.10.3] - 2026-06-24

### Fixed
- meta-ad-copy and meta-lead-form skills now say to save the built file into the client's campaign subfolder (clients/<Client>/<Mon-DD>-<slug>-campaign/), not just the outputs directory, so standalone deliverables follow the campaign-subfolder rule.

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
