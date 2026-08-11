# Creative Plan XLSX, detailed spec

Build with the Python build module (build/creative_plan.py). TWO tabs: BRAND PACK and CREATIVE TRACKER.

Ad copy is NOT a tab in the Creative Plan. It always ships as its own workbook, built with build/ad_copy.py and named "MAXALDING - [Client] - [Campaign] - Meta Ad Copy.xlsx" (Feedback 2026-08-06, Kure by Konrad). The AD COPY section below is the content spec for that separate workbook, and remains the single source of truth for the ad copy rules.

## XLSX formatting (mandatory)
- Font: Helvetica Neue throughout, not Arial, not Calibri.
- Header rows: black background (000000), white bold text, size 8.
- Body rows: white background, text colour 434343, size 8, wrap text on, top-aligned.
- Column widths generous; all content readable without horizontal scrolling.
- Row heights: minimum 45pt for short rows; 120 to 150pt for Creative Tracker data rows.
- Freeze the top row on the Creative Tracker and Ad Copy tabs.

## Tab 1, BRAND PACK (label and value, black section headers)
Sections in order. Do NOT include a KPIs section.
1. CHANNELS: platforms in use, website, socials.
2. AUDIENCE: ICP summary, demographics, psychographics, pain points, locations, exclusions.
3. TONE OF VOICE: voice, words to use, words to avoid, emotional direction, an Emoji palette row (a short per-client emoji set chosen to fit the ICP, see the emoji rule under Tab 3), and a BANNED IN COPY row (em dashes, en dashes, structure as a noun, framework, exclamation marks, plus the positive-language note).
4. OFFER: offer tiers and pricing, inclusions, payment, exact lead magnet name, funnel, guarantee.
5. BRAND POSITIONING: Core Message, Tagline and support line, positioning statement, unique mechanism, hero story, proof assets, messaging rules, and a Meta compliance row.

## Tab 2, CREATIVE TRACKER
Apply ad-creative principles before writing any cell. Columns left to right:
number, DATE, FORMAT, RESOLUTION, STATUS, PLATFORM, FILE TYPE, AUDIENCE, CONCEPT, HOOK GUIDANCE, BEATS, DETAILS, EDITING DIRECTION, FILMING DIRECTION, SCRIPT, FINAL ASSET.

- DATE: leave blank. The agency does not stamp a date on deliverables, to avoid implying deadlines we cannot meet. The team fills this per row when a creative is actually briefed. Do not write "today" or an actual calendar date into this column.
- FORMAT: STATIC or VIDEO.
- RESOLUTION: the fixed string "1080 x 1350 (4:5) / 1080 x 1920 (9:16)".
- STATUS: dropdown Briefed, Filmed, In Edit, Signed Off, Live. Default Briefed.
- PLATFORM: dropdown FACEBOOK + INSTAGRAM, FACEBOOK, INSTAGRAM, TIKTOK. Default FACEBOOK + INSTAGRAM.
- FILE TYPE: a formula referencing the FORMAT column on every row, never hardcoded.
- AUDIENCE: one consistent line, identical on every row.
- CONCEPT: the exact concept name. No codes.
- SCRIPT: blank for statics; the Video Ad Scripts filename for video rows after Stage 4.
- FINAL ASSET: blank.

14 rows: 7 statics then 7 videos, concepts in the spec order (static Problem to Solution, Incentive, Benefit, Social Proof Review, Social Proof Progress, Location, Audience Addresser, then video Problem to Solution, Social Proof (Client Interview), Pattern Interrupt, Storytelling (Full Voiceover B-Roll), Benefit, Incentive, Audience Addresser).

There is ONE social proof video concept, in the client-interview format (see script-guidelines). The client records the same question set with a few different clients or members, and each interview becomes its own ad variant; do not add a second social proof video concept. Storytelling runs as the full voiceover B-Roll concept by default (one per plan, see script-guidelines); its FILMING DIRECTION is a concrete B-Roll shot list that doubles as the client's filming brief. Pattern Interrupt stays canonical but drop it via tracker_concepts when it does not serve the plan (Fisica, 2026-07-16). It is the first concept to drop when the client has strong existing-post ads in the plan, because a proven organic post interrupts the scroll better than a concept written to do it (Feedback 2026-08-11, Xcelerate Performance).

The canonical 14 rows are the default, not a cage. A client may scope or extend the set through the `tracker_concepts` data list ([FORMAT, CONCEPT] pairs, statics first), for example adding an extra objection-angle video such as a "Tried PT Before" concept aimed at the same ICP who has bought personal training before and had it not stick (proven buyers, a strong warm angle). Every video concept in the tracker must have a matching concept block, in the same order, in the Video Ad Scripts document; the build mirrors the script's single hook into the tracker HOOK GUIDANCE cell (video rows only, statics stay blank).

Existing post ads. If the client has a proven organic post to run as a paid ad (Meta's Use Existing Post), add it as an extra tracker row through the `existing_posts` data list, numbered after the canonical rows. Set FORMAT to EXISTING POST, STATUS to Signed Off, put the post URL in FINAL ASSET, describe it in DETAILS (a proven organic post to boost, run as is, do not re-edit) with the beats and editing notes saying no filming or editing is required, and leave SCRIPT blank. The hook lives in the existing post, so keep the HOOK GUIDANCE cell a short reference, not new copy; the validator does not apply the single-hook or hook-length rules to non STATIC or VIDEO rows. When the client shares a link to a post that performed well, that is the signal to add an existing-post-ad row.

## Statics, the coach template

ONE graphic per static row, not three variations (Feedback 2026-08-11, Xcelerate Performance: the tracker moved to a single perfected hook, and the BEATS column has to match it). BEATS describes the elements that appear on that one graphic, each on its own line. Do not write Graphic 1 / Graphic 2 / Graphic 3, and do not list hook variations anywhere.

**Statics leave HOOK GUIDANCE BLANK.** All of a static's on-screen copy, the hook line included, lives in BEATS alongside the subline or bullets and the CTA. Putting the hook line in both columns just repeats it and reads as confusing (Feedback 2026-08-11, Xcelerate Performance). HOOK GUIDANCE is effectively a video-only column: it exists to show at a glance how a VIDEO opens, which a static does not need because its entire copy is already written out in BEATS. The validator warns on a populated static hook cell (rule `static-hook-blank`).

BEATS must say what the static IS, not just recite a generic layout. Use these per-concept layouts. They are written for coaches; gyms are likely to differ, so adapt rather than force them.

- **Problem > Solution**: two lines, the exact pain point the ICP is facing and the coach's solution to it, then a clear CTA. B-Roll imagery behind.
- **Incentive**: a clear ad hook line and a clear CTA pointing at the offer or incentive the coach has available. No subline. B-Roll imagery.
- **Benefit**: a hook line at the top, then a checklist of three to four bullets maximum covering what comes in the package and the standout benefits a client can expect, then a CTA. B-Roll imagery.
- **Social Proof (Review)**: literally a review. A five star rating, who it is from, and one key quote pulled out of that review. Client supplies the review and any client photo.
- **Social Proof (Progress)**: a 50:50 split graphic showing before on one side and after on the other, from a client or from the coach himself, with a hook naming the change ("X went from this to this", or whatever suits the brief and coach). Client supplies the transformation photos.
- **Location**: an annotated map of the area the coach serves, a hook that asks the local question ("Are you looking for a coach in Sydney?" or similar), and a clear CTA. B-Roll imagery with the map graphic over the top.
- **Audience Addresser**: the hook calls the audience out directly, with a clear CTA. B-Roll of the ICP audience.

Use FILMING DIRECTION to describe the imagery for every static, matched to the concept above. An imageless ugly-ad text-only treatment is still worth offering on Problem to Solution and Incentive.

Where the client's end user is a MINOR, do not run a body before-and-after on the Progress static. Use the coach's own transformation, or a documented performance figure instead (Feedback 2026-08-11, Xcelerate Performance).

HOOK GUIDANCE column format: ONE hook per row, on a single line, with NO label. Do not write "Hook 1:"/"Hook 2:"/"Hook 3:" and do not list variations; the column name already says what it is, and the QA gate rejects a multi-line cell (rule `hook-single`). This column is GUIDANCE: it shows the team at a glance how the video is likely to open and set up, not a menu to choose from. Write the single strongest hook and perfect it. Because the Video Ad Scripts still carry three spoken options, the tracker line is the script's Option A, so write Option A as the best of the three and let the build mirror it. A static hook is an on-screen overlay: keep it 5 to 10 words. A video hook is a SPOKEN opening line and may be a full sentence or two, up to about 25 words, not a short fragment. Apply the ad-creative and ad-hooks craft before writing: generate several angles (problem callout, question, empathy, social proof, bold statement, pattern interrupt, curiosity gap), then pick the strongest and sharpen it rather than shipping the set.

Video hook rules: one hook per row, specific to this client. It must sound like a voicenote said out loud to camera, not a written slogan: natural spoken English, contractions, a real spoken opener where it fits ("Okay", "Real quick", "Here's the thing", "Don't scroll past this"). Never "you" plus a negative attribute. Static hook rules: the HOOK GUIDANCE cell is left blank; write the overlay hook line as the first line of BEATS instead, keeping it to 5 to 10 words. Audience Addresser: one hook that calls the viewer out, by age range, job or role, or daily-life situation, whichever lands hardest for this ICP; a question is encouraged.

BEATS: statics describe the ONE graphic using the per-concept layout above; videos use Clip 1 opening, Clip 2 main content, Clip 3 close and CTA. Put every element on its OWN line inside the cell (line breaks, not a single run-on line). Any Subline, Quote, checklist bullet or CTA note also goes on its own line.
DETAILS: 4 to 5 dashed bullets, specific to the client.
EDITING DIRECTION and FILMING DIRECTION: bullet format with a dash prefix on every point, per the templates in the System Prompt.

## AD COPY (separate workbook, build/ad_copy.py)
Apply ads, ad-creative and copywriting before writing. Columns: number, CONCEPT, POST COPY, CHARS. No STATUS column, no CTA column or note.
- Organise by distinct concept only, no duplicate concept rows.
- 5 post copy variations per concept.
- One shared block of 5 headlines and one shared description that cover all concepts.
- CHARS is a live LEN formula on the copy cell.
- Post copy no longer than 125 characters, built to stop the scroll with a clear hook in the first line. Each of the five is unique: a genuinely different angle or approach, not a reworded version of the others. Maximum one rhetorical question per post. Do not end a post copy with a full stop, it reads unnatural in an ad.
- LENGTH VARIANCE (enforced by the QA gate, rule `post-copy-variance`). 125 is a CEILING, not a target, and neither is any other number. The repeated failure here is writing every post to roughly the same length: first everything near 125, then later everything near 65. Both read machine-made. Write each post at the length its idea needs and let the set land unevenly. Concretely, across the whole set: the shortest and longest must differ by at least 45 characters, and at least one post must be 50 characters or under. A healthy set mixes genuinely short punchy lines (roughly 20 to 40 characters, often the strongest) with mid-length lines and a few longer ones near the limit. Check the spread before saving; if the lengths look like a flat line, rewrite rather than trim.
- Headlines no more than 40 characters, ideally 30. Always include one audience-addresser variation and one offer variation, plus a few others on different angles.
- Description one only, no more than 25 characters. Use the client tagline where it fits. It should tie the messaging together, not repeat the offer already carried by the post copy and headlines.
- Emoji and length are fluid and intentional, never a pattern. Lean into emoji: aim for around a third of the posts to carry one, varied and never one-per-row, with some left bare. Prefer premium, on-brand emoji (sparkle, white heart, warm heart, leaf, location pin, house, sun) over hype or loud ones (no fire, 100, rocket, heart-eyes), subject to brand tone. Match the emoji to the AUDIENCE, not only the brand: for a male or masculine audience (for example men over 30), avoid soft or feminine-coded emoji such as white heart, warm heart, leaf or sun; use a neutral, relevant emoji like a location pin sparingly, or none. The set above is a menu, not a mandate, and fewer emoji often reads better for a masculine audience. Draw the emoji from the client's emoji palette (defined at intake from the ICP and shown in the Brand Pack TONE OF VOICE), matched to each post's angle (for example a time emoji on a no-time post, a location pin on a local post). Do not pad copy to reach the character limit: if shorter reads stronger, keep it shorter.

These AD COPY rules are the single standard. They also apply to standalone ad-copy requests made outside a full onboarding, which are handled by the `meta-ad-copy` skill and built with `build/ad_copy.py` (it reuses `_build_ad_copy` here, so the format is identical). Keep this section and that skill in sync; this section is the source of truth.
