---
name: meta-static-design
description: Design a Maxalding client's Meta static ads in Figma and export them as final JPGs. Triggers include "do the statics", "design the statics", "build the static ads", "statics for [client]", "feedback on the statics", "export the statics", "make the static JPGs", or any request to turn a campaign's STATICS rows into finished image ads. Produces 4x5 and 9x16 statics (plus 1x1 carousel cards) in the Maxalding Figma ad system, checked against the static design standard, exported as 1080px JPGs foldered by placement, with every correction logged so the design improves client to client.
---

# Maxalding Meta Static Design

The statics arm. Liam moved statics from the editor to Claude in Figma on 2026-11-24 and ran the 1 TO 360 pilot through 13 rounds of feedback. Those rounds are now the standard in `references/static-design-standard.md`. The Figma mechanics (file, variables, templates, gotchas, scripts) are in `references/figma-system.md`. Final JPGs come out of `design/export_statics.py`.

## Read first, every time
1. The Onboarding Feedback Log in the workspace (`MAXALDING_WORKSPACE`), in full. Statics entries are tagged "Statics". The most recent feedback wins.
2. `references/static-design-standard.md`: the whole standard. Every rule there came from Liam.
3. `references/figma-system.md`: how the Figma file is built and the scripts for scrims, shadows, photos and exports.
4. The client's memory files (Brand, Audience, Marketing, the "How [name] talks" block) and Meta rules for this client (no weight figures, banned words, premium framing, youth safeguards).
5. The campaign's Creative Plan STATICS rows and the approved ad copy. The copy, offer line and CTA are decided there. Do not invent a new campaign on a static.

## The process
1. **Client theme.** In the Figma file, add the client as a new mode on the Brand variable collection: ink, paper, accent, on-accent and muted colours from their brand guidelines or website, and the fonts (TikTok Sans by default; the client serif only as a one-word accent). Never copy a past client's or the editor's designs.
2. **Photos.** Get the client's photos as local files (the Drive connector can't pass images through). Make a contact sheet, map every photo (who, what's happening, where the faces are) and pick per ad. One photo per ad across the whole set: never repeat a photo inside a set or a carousel. Prefer the coach mid-cue (hands-on, talking, demonstrating) over posed or face-only crops. If the set needs more photos of the right people than exist, say so and ask for the shoot's raw photos rather than force a repeat or a wrong-audience photo.
3. **Build.** One page per client campaign. Each concept is an instance of a Meta template (Size=4:5 and Size=9:16; carousels 1:1), with copy set through component properties. Pick the template by concept, not by habit: one idea per frame, the photo doing the work.
4. **Fit the photo.** Crop each photo per format so faces sit clear of the text block and the sticker. Lift dark phone photos (exposure +0.3, shadows +0.35, highlights -0.1). Set the scrim to the text block only and add the text shadow (the standard, section 4; scripts in figma-system.md).
5. **Check.** Run the standing checks in the standard (section 9) on every ad, every round: safe zones, CTA line, scrim and contrast, orphans, 36px minimum, no repeats, copy through the validator. Screenshot the whole set and look at it as a feed, not as a page.
6. **Show Liam.** Send the overview screenshot and say what changed. Every round of notes is applied in Figma, re-screenshotted and checked again.
7. **Export.** Once Liam signs off (or asks for files): export each ad from Figma at 2x PNG, then `python -m design.export_statics <png folder> <campaign folder>` builds `STATICS FINAL JPG (<Mon-DD>)/` with `4x5 Feed`, `9x16 Stories and Reels` and `1x1 Carousel (upload in order)`, every file 1080 wide, JPG quality 95, full chroma, named `<CLIENT> <NN> <CONCEPT> <size>.jpg`. Re-exports after a change replace only the files that changed.
8. **Feedback loop.** Every note Liam gives is (a) applied in Figma and re-exported if files exist, (b) logged as a dated "Statics" entry in the workspace feedback log, and (c) if it should bind future statics, written into `references/static-design-standard.md` (and the template, when it is a template change), with the version bumped. A correction is not closed until all three happen.

## Hard rules
- Social-first, never landing-page elements: no label kickers, no icon bullets, no drawn CTA buttons, no logos (the profile is the logo), no review counts.
- Copy comes from the approved Creative Plan and ad copy, and passes the copy validator. Never fabricate a quote, result or credential.
- No other client's name, photos or footage on any static.
- Exports are JPG at 1080 wide unless Liam asks for another format. Upload to Drive or ClickUp only when he asks, to the folder he names.
- The plugin rules win over any skill on conflict.

## Skills to use alongside
- `ad-hooks` for headline options when a concept needs a new hook.
- `social-media-skills:quote-cards-and-text-graphics`, `social-media-skills:carousel-writer` and `social-media-skills:social-proof-and-testimonials` for craft reference.
