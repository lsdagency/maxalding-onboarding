# Maxalding Static Design Standard

What makes a Maxalding Meta static. Every rule below came from Liam's feedback on the 1 TO 360 pilot (rounds 1 to 13, 2026-11-24 to 2026-11-26) unless marked otherwise. Newer feedback in the workspace log wins over this file until it is written in here.

## 1. The test: feed, not website
Ask of every layout: "would this look at home in the feed, or on a website?" Liam's first note was "these ads look good as landing page elements but what makes meta best practice?" Website and UI patterns are out:
- No label kickers or sub-headers over the headline (MEET YOUR COACH, YOUR FIRST SESSION, START HERE, THE PROBLEM / THE FIX, MYTH / TRUTH). "Obvious AI slop."
- No icon bullets (tick circles, numbered circles). No hairline-rule lists or card panels as a default.
- No drawn CTA buttons or pills (Meta supplies the button).
- No logos or brand names on the static (on Meta the profile is the logo). No job-title line on Meet the Coach.
- No review counts (a client may have one review).

Social-first means one idea per frame, big type, the photo doing the work, native formats (notes, text thread, captions), and multi-point content in a carousel or the primary text instead of a list on one graphic.

## 2. Layout and safe zones
- Formats: every concept in 4:5 (1080x1350) and 9:16 (1080x1920). Carousels are 1:1 (1080x1080) only (Meta letterboxes them in Stories and Reels).
- 9:16: text only between 14% from the top and 35% from the bottom (the Reels overlay), and clear of the lower-right icon column. The text block ends by y 1248.
- 4:5: key content inside the centre 1080x1080 (the 1:1 crop). CTA bottom at y 1215.
- Headline at the top, or bottom-anchored when the faces are in the top third (Photo Top has Text=Top and Text=Bottom). Text left-aligned except the quote-led Meet the Coach (centred).
- Spacing is generous (auto-layout gaps opened ×1.4 in round 3 after "cramped"). After any spacing change, check fixed-height frames for clipping.
- Type-led 9:16s on ink read as black space (the bottom 670px must stay empty). Put type-led ads on paper or the accent colour, not ink.

## 3. Type
- House font TikTok Sans (free, OFL, native-feeling on Reels): headline Black, body Medium or Regular, CTA Bold. The client serif is an accent on one short word only, never the headline face. Text Thread keeps Inter (phone-native). SF Pro and Neue Haas are not licensed for ads; Poppins reads as Canva.
- Thumbnail test: headlines heavy and 110px or more at 1080 wide; nothing under 36px.
- Headline 8 words or fewer.
- Orphans: no single-word last line, no two-word hanger, never split a place name. Break lines on purpose and re-check.
- Accent colour once per ad, and only on solid backgrounds, never over a photo.
- Problem Solution: the problem line is Bold and smaller, so the solution still carries the most weight (Liam reversed the regular weight in round 13).
- Strikethrough (Myth Buster): a font's strikethrough can't be thinned in Figma and reads too thick. Draw a 3px rule through each line instead (the template has Myth line 1 and Myth line 2).

## 4. Photos, scrims and contrast
- Lift dark phone photos: exposure +0.3, shadows +0.35, highlights -0.1, contrast +0.05.
- The scrim (dark gradient) sits behind the text block only, never the whole frame. It starts about 300px above the first line at 0%, rises to about 60% just above the first line, and holds under the text. On 9:16 it fades to about 25% below the CTA, so the photo fills the Reels zone. Round 13: "too dark and filled with too much black space" at 86 to 94%, then "still a bit too dark" at 80%. 60% was signed off.
- Every line of text over a photo carries a soft shadow: black 45% blur 28 offset y2, plus black 30% blur 6 offset y1. This keeps white type readable on light clothing without darkening the image. It must not read as an outline or a box.
- Support text at full opacity.
- Faces never under text, the sticker or the CTA. Mirror or recrop the photo when they are.
- One photo per ad across a set, and no repeats inside a carousel.
- Meet the Coach shows the coach actually coaching (hands-on cue, demonstrating, talking a client through it), with the face on the upper-third eye line. Never a face-only crop.

## 5. CTA
- Every ad ends on a short text CTA line ("Tap below to enquire ↓"), pinned to the lowest safe line (4:5 bottom 1215, 9:16 bottom 1248), content kept 56px clear above it, in a bottom-anchored CTA Block so it grows upward.
- Text Thread's CTA is a native reply box (a draft reply in the viewer's voice plus a send button).
- The carousel End card is the close: accent background, the offer in mega type, a heavy 68px CTA above a rule.
- Check the CTA colour against its own background every time.

## 6. Concepts
- Each static is a visually distinct concept, not three variations of one.
- Benefit = ONE benefit, photo-led (Photo Top). The rest go in the primary text.
- Offer Sticker: a 380px 22-point burst with a soft shadow, top right outside the text flow (4:5 y150, 9:16 y300), type fitting inside the burst, never over a face.
- Social Proof: a real quote with its source (name, how long they've trained, "Google review"). No review count. Avoid reviews that break Meta rules (weight loss figures).
- Process ads (First Session) say what the customer GETS, not what the gym does.
- Location: drawn (imitated) maps labelled with real neighbouring areas, never real map tiles.
- Audience Addresser: the headline does the addressing (no callout pill).
- Carousel: a sequence follows the client's real path from the transcript (enquiry, quick chat, first session, the rest of the intro block, the offer close). Fewer cards is fine. No phrase repeats across cards. The copy is gain-led. A swipe cue sits bottom right on the Cover. Cards are focal-aware (Step BL / TL / BR puts the copy in the corner clear of faces).
- Price Offer only when the client names the price.

## 7. Copy
- From the approved Creative Plan and ad copy. Every line goes through the copy validator.
- Read back for lists of three (steps, chips, sentences), comma fragments and stock phrases repeated across the set. A verbatim quote that is a triplet is swapped for another real quote, not edited.

## 8. Export
- Figma PNG at 2x, downscaled with Lanczos to 1080 wide, JPG quality 95, full chroma (4:4:4), sRGB.
- Folder: `<campaign>/STATICS FINAL JPG (<Mon-DD>)/` with `4x5 Feed`, `9x16 Stories and Reels`, `1x1 Carousel (upload in order)`.
- Names: `<CLIENT> <NN> <CONCEPT> <4x5|9x16>.jpg`; carousel `<CLIENT> CAROUSEL <n> <CARD>.jpg` in upload order.
- `python -m design.export_statics` does the conversion and checks every size.

## 9. Standing checks (every ad, every round)
1. Safe zones (9:16 top 14%, bottom 35%, Reels icon column; 4:5 centre square).
2. CTA present, on the safe line, not overlapping content, readable on its background.
3. Scrim behind the text only, about 60% peak, faded below the CTA on 9:16; text shadow on every line over a photo; no seams where two scrims meet.
4. No face under text, sticker or CTA.
5. Orphans and wraps; nothing under 36px; nothing clipped.
6. No photo repeats in the set or a carousel.
7. No kickers, icon bullets, buttons, logos or review counts.
8. Copy through the validator and the read-back.
9. Look at the whole set screenshotted together: does it read as a feed of distinct ads, and is any ad a black slab?
