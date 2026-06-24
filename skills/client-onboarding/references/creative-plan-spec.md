# Creative Plan XLSX, detailed spec

Build with the Python build module (build/creative_plan.py). Three tabs.

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
3. TONE OF VOICE: voice, words to use, words to avoid, emotional direction, and a BANNED IN COPY row (em dashes, en dashes, structure as a noun, framework, exclamation marks, plus the positive-language note).
4. OFFER: offer tiers and pricing, inclusions, payment, exact lead magnet name, funnel, guarantee.
5. BRAND POSITIONING: Core Message, Tagline and support line, positioning statement, unique mechanism, hero story, proof assets, messaging rules, and a Meta compliance row.

## Tab 2, CREATIVE TRACKER
Apply ad-creative principles before writing any cell. Columns left to right:
number, DATE, FORMAT, RESOLUTION, STATUS, PLATFORM, FILE TYPE, AUDIENCE, CONCEPT, HOOK, BEATS, DETAILS, EDITING DIRECTION, FILMING DIRECTION, SCRIPT, FINAL ASSET.

- DATE: today.
- FORMAT: STATIC or VIDEO.
- RESOLUTION: the fixed string "1080 x 1350 (4:5) / 1080 x 1920 (9:16)".
- STATUS: dropdown Briefed, Filmed, In Edit, Signed Off, Live. Default Briefed.
- PLATFORM: dropdown FACEBOOK + INSTAGRAM, FACEBOOK, INSTAGRAM, TIKTOK. Default FACEBOOK + INSTAGRAM.
- FILE TYPE: a formula referencing the FORMAT column on every row, never hardcoded.
- AUDIENCE: one consistent line, identical on every row.
- CONCEPT: the exact concept name. No codes.
- SCRIPT: blank for statics; the Video Ad Scripts filename for video rows after Stage 4.
- FINAL ASSET: blank.

13 rows: 5 statics then 8 videos, concepts in the spec order (Problem to Solution, Incentive, Benefit, Social Proof Review, Social Proof Before and After, then video Problem to Solution, Social Proof, Pattern Interrupt, Storytelling, Benefit, Incentive, Social Proof, Audience Addresser).

Statics follow exact per-concept layouts. Use FILMING DIRECTION to describe the imagery for every static, with three image options, plus an imageless ugly-ad text-only option for Problem to Solution, Incentive and the Review static. For Review and Before and After, the image format stays identical across variations and only the hook changes.

Video HOOK rules: three hooks per row, under 12 words each, at least one statement, never "you" plus a negative attribute, specific to this client. Audience Addresser is the exception: three hooks calling the viewer out by age range, job or role, and daily-life situation; questions are encouraged.

BEATS: statics use Graphic 1, 2, 3; videos use Clip 1 opening, Clip 2 main content, Clip 3 close and CTA.
DETAILS: 4 to 5 dashed bullets, specific to the client.
EDITING DIRECTION and FILMING DIRECTION: bullet format with a dash prefix on every point, per the templates in the System Prompt.

## Tab 3, AD COPY
Apply ads, ad-creative and copywriting before writing. Columns: number, CONCEPT, POST COPY, CHARS. No STATUS column, no CTA column or note.
- Organise by distinct concept only, no duplicate concept rows.
- 5 post copy variations per concept.
- One shared block of 5 headlines and one shared description that cover all concepts.
- CHARS is a live LEN formula on the copy cell.
- Post copy no longer than 125 characters, built to stop the scroll with a clear hook in the first line. Each of the five is unique: a genuinely different angle or approach, not a reworded version of the others. Maximum one rhetorical question per post.
- Headlines no more than 40 characters, ideally 30. Always include one audience-addresser variation and one offer variation, plus a few others on different angles.
- Description one only, no more than 25 characters. Use the client tagline where it fits. It should tie the messaging together, not repeat the offer already carried by the post copy and headlines.
- Emoji and length are fluid and intentional, never a pattern. Add an emoji only where it genuinely fits and leave it out where it does not. Do not pad copy to reach the character limit: if shorter reads stronger, keep it shorter.

These AD COPY rules are the single standard. They also apply to standalone ad-copy requests made outside a full onboarding, which are handled by the `meta-ad-copy` skill and built with `build/ad_copy.py` (it reuses `_build_ad_copy` here, so the format is identical). Keep this section and that skill in sync; this section is the source of truth.
