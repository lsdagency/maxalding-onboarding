# Changelog

All notable changes to the Maxalding Onboarding plugin. Each rule change is traceable to the client and date it came from via rules/rules.yaml and the Onboarding Feedback Log.

## [0.22.1] - 2026-08-11

### Changed
- Refined the v0.21.0 register rule, which was too absolute. The transcript governs the SHAPE of the client's speech (sentence length, openers, tag questions, cadence, repetition, the technical vocabulary of their craft). Audience-facing VOCABULARY is a separate question and may legitimately come from the AUDIENCE's own language, provided the client would plainly say it in life. Evidence the shape from the transcript and the vocabulary from the transcript OR the ICP, and be able to say which; what is never acceptable is reaching for a word because it merely sounds like the region or the trade. Read literally, the old rule would have stripped a correct word. Worked example now in writing-rules: "footy" appears in none of Zack's nine transcribed reels, where his on-camera sport vocabulary is all coaching technical (contact, bumpers, post contact metres, play the ball), but every Sydney league parent says it and Liam kept it on exactly that ground (2026-08-11).

## [0.22.0] - 2026-08-11

### Changed
- The funnel destination deliverable now follows the funnel. New `funnel_type` field (`lead_form` or `landing_page`, default `landing_page`): build.build_all produces Meta Lead Form copy OR Landing Page copy, never the wrong one. The onboarding SKILL.md hard gate now says to ASK at the Stage 2 gate which one the campaign runs, every time, even when the documents imply one. The Xcelerate campaign ran a Meta Instant Form and was handed a landing page (Feedback 2026-08-11).
- landing-page-structure.md: the document covers the LANDING PAGE only and does not automatically include the funnel's second step. If the funnel uses separate pages, the booking page (calendar above the fold, short what-to-expect, reassurance testimonial placeholder) and thank-you page are written as their own clearly titled sections so nobody has to guess whether they were covered. On a lead-form funnel the completion screen is the equivalent second step.

### Removed
- The EDITING BEST PRACTICE section from the Video Ad Scripts document, and the instruction to web-search editing tips before each build. That document is the TALENT'S filming brief: generic Reels editing guidance belongs with the editor, and per-concept editing direction already lives in the Creative Plan EDITING DIRECTION column. From Liam's Xcelerate Performance feedback (2026-08-11).

### Added
- creative-plan-spec.md, post copy: USE THE CEILING WHERE THE IDEA EARNS IT. The variance rule was being read as a licence to write everything short, and a set whose longest post is only 100 characters under-uses the space just as much as one clustered at 125. Expect a couple of posts in the 105 to 125 band in a healthy set. Never pad to reach the limit, never clip to manufacture variety.
- creative-plan-spec.md: EXPLAIN ANY NUMBER A COLD READER CANNOT DECODE. A performance figure carries no meaning alone ("6.4 seconds in week four, 5.19 in week fifteen" tells a stranger nothing about what was measured). Name the test the first time the number appears in any asset. Applies to ad copy, scripts, CRM and the landing page alike.

## [0.21.0] - 2026-08-11

### Added
- writing-rules.md: an AI CADENCES section listing the banned SHAPES rather than banned words. The significance clause bolted on to explain why what you just said matters ("and that's the whole reason I ended up coaching", "because nobody ever spells this out", "which is exactly why it works"); the neat balanced summary ("coached as one of twenty"); the "not X, it is Y" contrast; stacked subordinate clauses in a spoken line; and explaining your own point straight after making it. Liam flagged three of these in the Xcelerate scripts as "obvious Claude AI lines, I've seen them over and over again" (2026-08-11).
- writing-rules.md: a "Write in the client's actual register" section. Every onboarding already transcribes the client's Instagram at Stage 1, and that transcript IS the register. Mine it for sentence length, openers, tag questions, filler words and repeated phrases, and write every spoken line against it.
- instagram-research.md: a "How [name] actually talks" block is now MANDATORY in the Brand memory and in the Brand Pack TONE OF VOICE, written from the transcripts rather than the questionnaire's tone section, with the recurring words counted off the transcript rather than guessed at.

### Why
The Xcelerate run transcribed nine reels at Stage 1 and then wrote the scripts in a generic voice anyway. The research existed and went unused, which is a process failure the rules did not previously catch: the register rule was there but soft, buried in a sentence about hook slang. It is now its own requirement with a named artefact.

## [0.20.0] - 2026-08-11

### Changed
- Statics now leave the HOOK GUIDANCE cell BLANK. All of a static's on-screen copy, hook line included, already lives in BEATS alongside the subline or bullets and the CTA, so carrying the hook in both columns just repeated it and read as confusing. HOOK GUIDANCE is effectively a video-only column now: it exists to show at a glance how a VIDEO opens, which a static does not need because its whole copy is written out in BEATS. From Liam's Xcelerate Performance feedback (2026-08-11), raised as a forward-looking rule, so no existing deliverable was rebuilt.
- The static overlay hook is still written to the 5 to 10 word rule, it just lives as the first line of BEATS rather than in its own column.
- evals/cases/sample_client.json: the seven static hooks are blanked and their hook lines folded into BEATS, so the canonical example teaches the new shape.

### Added
- Validator rule `static-hook-blank` (WARNING): a populated static HOOK GUIDANCE cell is flagged with a pointer to put the line in BEATS. A warning rather than an error so older packs still build.

### Removed
- The static hook length check. A blank static hook cell used to fail `hook-length` for being under five words, which would have made the new rule unusable. Video hooks are unaffected and still capped at 25 words.

### Fixed
- creative-plan-spec.md still said "the canonical 13 rows" and "the build mirrors the script's Option A hook", both stale since 0.18.0 and 0.17.0 respectively.

## [0.19.0] - 2026-08-11

### Added
- Validator rule `contrastive-correction` (WARNING, not an error): flags the wider "not X, it is Y" shape that the banned formula belongs to, for example "the bit I love isn't the sprint times, it's the week he turns up early" or "not just a group plan, an actual program". The existing `banned-formula` rule only ever matched the literal "X problem / Y problem" wording, so writing round that one while reaching for the same rhythm went completely unflagged: four instances survived into a finished Xcelerate Performance build on 2026-08-11 and were only caught by reading. Deliberately a warning, because plenty of legitimate copy contrasts two things and an error would block good work; the warning exists to make the author look at the line. Verified at 6 of 6 on real failures with 0 false positives across 12 legitimate negatives, and locked in with three bad cases and three good cases in the evals.

## [0.18.0] - 2026-08-11

### Changed
- Statics: ONE graphic per static row, never three variations. The tracker moved to a single perfected hook in 0.16.0 but the BEATS column was never brought in line and kept suggesting Graphic 1 / Graphic 2 / Graphic 3. BEATS now describes the elements on that one graphic, each on its own line, and must say what the static IS rather than reciting a generic layout. From Liam's Xcelerate Performance feedback (2026-08-11).
- The canonical static set is now the COACH template, seven statics rather than five: Problem > Solution (two lines, the pain point and the solution, plus a CTA), Incentive (hook line and a clear CTA to the offer, no subline), Benefit (hook line, a checklist of three to four bullets on what comes in the package, then a CTA), Social Proof Review (five star rating, who it is from, one key quote pulled from the review), Social Proof Progress (50:50 split, before and after from a client or the coach himself), Location (annotated map of the catchment, a hook asking the local question, clear CTA) and Audience Addresser (hook calls the audience out directly). Gyms are likely to differ, so adapt rather than force. Statics carry B-Roll imagery by default. CANONICAL_TRACKER is now 14 rows, seven statics then seven videos.
- Social Proof (Before & After) renamed Social Proof (Progress) and specified as a 50:50 split graphic.
- Video concept purposes are now written down, because they had bled into each other: Storytelling is the COACH'S own story (why they started coaching, how long, what they love about it), Benefit explains the OFFER and what comes in the package, and Incentive is the offer or price short and sweet with no explanation of the package. From the same feedback round, where the Incentive video had drifted into explaining the offer and left Incentive with nothing of its own.
- Pattern Interrupt is now explicitly the first concept to drop when the plan already carries strong existing-post ads, because a proven organic post interrupts the scroll better than a concept written to do it.

### Added
- Child-safety rule for any client whose end user is a minor: never run a body before-and-after on the Progress static. Use the coach's own transformation or a documented performance figure instead. Recorded in creative-plan-spec.md and rules/rules.yaml.

### Fixed
- rules/rules.yaml `tracker_rows` said "5 statics then 8 videos (13 total)", which had been stale since the tracker dropped to 12 rows. Now correct at 14.
- plugin.json and rules/rules.yaml were both still on 0.16.0 despite a 0.17.0 changelog entry. Both bumped to 0.18.0.

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
