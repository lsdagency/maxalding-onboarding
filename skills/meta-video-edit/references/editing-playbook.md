# Editing playbook: what makes a Meta ad edit work

The standard every Maxalding edit is held to. Sources are listed at the end. The Learned from feedback section at the bottom is where Liam's corrections become standing rules; it outranks everything above it.

## The principles
1. **The first frame and the first words are the ad.** Meta's own research is that most of a video ad's value is delivered in the first three seconds. Open on the strongest line, with the speaker's face on screen and the on-screen hook text up from frame one. Never open on a breath, a "so", a logo, a wide shot of nothing, or black.
2. **Sound off is the default viewer.** Burned-in captions on every spoken word, plus a hook title that says the point without audio. Someone watching muted must get the whole ad.
3. **Cut the air, keep the person.** Remove pauses, false starts, fillers and repeated words (jump cuts). Keep the natural rhythm of the speaker: do not cut so tight that breaths vanish and it sounds robotic. The engine's tightening keeps a short breath either side of every cut.
4. **Hide jump cuts with punch-ins.** Alternate the framing between a mid shot and a closer crop (about 8 to 12 percent) on each cut, so the cut reads as an edit choice, not a glitch. 4K source makes the punch-in clean.
5. **Something changes every three to five seconds.** A cut, a punch-in, a B-roll insert or a caption beat. Long unbroken shots lose people.
6. **B-roll shows what is being said.** When the speaker mentions training, the coach, the studio or a result, cut to footage of exactly that. Keep the voice running underneath. B-roll that does not match the words is wallpaper; leave it out.
7. **One idea per ad.** Every line has to serve the concept in the Creative Plan. Good lines that belong to another concept go in that concept's cut.
8. **End on the strongest line, not a slate.** The ad ends naturally on a line that lands. The offer and the instruction live in the ad copy, the headline and the CTA button, which work together with the video.
9. **Native, not produced.** Authentic beats polished on Reels. Light colour correction for consistency, clean audio, no flashy transitions, no stock swooshes, no other platform's watermark.
10. **Audio is half the ad.** Voice clear and even, delivered at -14 LUFS with peaks under -1 dBTP. Music, if used, sits well under the voice (around -22 dB) and ducks when anyone speaks.
11. **Both formats, framed for each.** 9x16 for Reels and Stories, 4x5 for Feed. Reframe per format with a focus point on the face; never letterbox. Keep all text inside the safe zone (specs-and-safe-zones.md).
12. **Creative diversity beats volume.** Meta's ranking favours genuinely different ads (different hooks, angles, people), not ten near copies. Hook variants share an identical body so the hook is the only variable.

## Recipes by concept

### Client interview (testimonial)
- Questions are cut out; only the client's answers remain, and the story must make sense without them.
- Open on the client's single strongest line (the one that would stop a scroll on its own), or their intro line if it is strong. If the strongest line opens, the intro ("I'm Kevin, I've trained with Sergio for 18 months") comes second.
- Shape: hook line, who they are and how long, why they started, what training is like, what changed, the line that points at the viewer ("if you're thinking about it, just try it"), then the offer close.
- Singles 30 to 45 seconds unless the plan says otherwise. Mixes (several clients) cut on a theme: one answer per person per beat, alternating faces.
- Hook title: the strongest line paraphrased to a few words, or the theme ("What 18 months with Sergio changed").
- Never splice words from different answers into a new claim. Cut weight figures, kilos and measurements (Meta). Flag health conditions to Liam before anything runs.
- Close on the offer end card with one line of the coach's CTA audio under it.

### Audience Addresser
- Hook names the audience in the first line ("Women 40 to 55 in South Kensington"). Hook title says the same thing in a few words.
- Body tight, CTA on screen at the end. 15 to 45 seconds.
- Hook variants: identical body and CTA, only the first line changes.

### Incentive
- The offer is the hook, said and shown in the first two seconds. Short: 10 to 30 seconds.
- End on the offer card.

### Story / Meet the coach
- Open on the most human line, not the CV. Credentials appear as on-screen text, not a spoken list.

### B-roll montage
- Cut on the beat of the track. Strongest shot first. Text carries the message (three to five short beats), ending on the offer. 8 to 30 seconds.

## What we never do
- Open on black, a logo or a title card.
- Leave a caption word that does not match the audio.
- Put text outside the safe zone, or under 54 px at 1080 wide.
- Use a commercial music track, or another platform's watermark.
- Present a result from another business (for example a coach's previous gym) as the client's result.
- Name or show another Maxalding client.

## Sources
- Meta Business Help Centre and Meta creative guidance on the first three seconds, sound off viewing and 9:16 Reels (Nielsen research commissioned by Meta: viewers under three seconds account for up to 47 percent of campaign value).
- Reels and Stories safe zone guides (14 percent top, 35 percent bottom, 6 percent sides): Coinis, AdNova, Billo (2026).
- Andromeda creative diversity guidance (2025 to 2026): benly.ai, V8 Media, dojoai.
- UGC and testimonial editing practice: Billo, Influencer Marketing Hub (jump cuts, removing dead air, B-roll that shows what is said).

## Learned from feedback
Dated entries promoted from the workspace feedback log. Newest first.

- 2026-11-25 (Liam, preview round 7): no on-screen hook text on interviews (`titles: []`, `hook_text: false`); the spoken hook carries it. Keep the caption glow soft (shadow_alpha about 0x40, blur 10, glow 3 on light clothing). B-roll is training footage only (never coach intros or interviews), worked out line by line from what's being said: a cutaway of 2 to 2.5 s on the words it illustrates, three to five per ad, hooks and endings on the face. Use that client's own training first; if none fits a beat, another client's training is fine, preferring shots where the person isn't the focus (hands, bar, coaching).

- 2026-11-25 (Liam, preview round 6, "nearly there, the scripts are a lot better"): captions back in one area below the chin, with the same editorial style; the hook title is highlighted (ink on a paper box). On light clothing, use a soft glow shadow plus a highlights grade, never a border.

- 2026-11-25 (Liam, preview round 5): the opening still had an "ummm" (his false start "uh, the private, the" was hidden by the transcript); one result was built from parts of different sentences and lost the viewer after 0:29; "give you a goal / gym will try something different" came from a cut landing on the tail of another word; captions sat on the face; client 2 had an outline. Standing fixes: verbatim transcripts, `refine` on every used span, `verify` on every cut-in before rendering, never join parts of different sentences, captions placed around the detected face (QA fails overlaps), no caption borders (grade the clip instead).

- 2026-11-25 (Liam, preview round 4): (1) a stutter at the start came from splicing words out of the middle of the hook sentence; hooks are whole sentences. (2) No gradients behind text. (3) Talking heads keep one framing; no side reframes. (4) Cuts landed before sentences finished; modules are whole sentences and jump cuts only remove pauses over 0.6 s (TIGHTEN_GAP), so the speaker's rhythm stays. (5) No end card and no on-screen offer: let the video end on the client's best closing line and put the offer in the ad copy. When asked what is best for social, think about the whole ad (video, primary text, headline, CTA button), not the video alone.

- 2026-11-25 (Liam): one finished ad per interview, built on the best hook from the scored script evaluation, not three hook variants (only make variants when asked for a hook test). The hook title is one font (TikTok Sans Black). Captions must interact with the video: the layout director reframes the subject off-centre and sets the captions in the open space, changing at sentence boundaries. The default close is the offer over a muted listening beat, not a solid end card.

- 2026-11-25 (Liam's caption references): captions and hook titles are editorial (mixed TikTok Sans with a serif-italic key word, small connecting words, words fading in as spoken, soft shadow and scrim). See caption-style.md. Frame for the title: eyes about 38 percent down so a two-line title fits above the head. Tighter framing (chest up, zoom about 2.1 on 4K) with 1.15 punch-ins.

- 2026-11-25 (Liam): "if you do that stupid copper box caption thing I'm going to go mad, that's such AI slop". Captions are clean: plain white TikTok Sans Bold with a soft shadow. Never the boxed or karaoke word-highlight caption-tool looks. Vendor "best caption style" lists describe what caption tools sell, not what a good editor does for a premium brand.

- 2026-11-25 (Liam, "a poor first attempt"): the first 1 TO 360 cut was one version per client, opening on the first decent line, with captions designed to pass checks rather than grab attention. Standing fix: every edit starts with a scored script evaluation, modules and three hook variants over one shared body. Captions are big and clean (see the next entry: no box styles). Chase B-roll of the speaker doing the thing (training) before cutting a talking head with nothing to cut to.

- 2026-11-25 (Liam): preview first, final once. Feedback rounds run on quick half-size previews; the full-quality 9x16 and 4x5 render happens once, after sign-off.
- 2026-11-25 (first edit, 1 TO 360): camera footage shot upright carries a rotation flag that ffmpeg passed into the output, so the first preview played sideways. The renderer now clears it and QA fails any rotation flag. Client words that hit a house banned phrase ("at the end of the day") are cut at a natural break rather than left on screen.

- 2026-11-25 (Liam, setup): captions and all on-screen text in TikTok Sans, same as the statics. Titles, CTA and cards in Black, captions in Bold.
- 2026-11-25 (Liam): never use a client's existing or previously delivered videos as reference or source material. Each edit is built from the raw footage, the Creative Plan and this playbook only.
- 2026-11-26 (Liam, 1 TO 360 round 8): interviews need more B-roll held longer. Cutaways run about 3.5 to 4 s each and cover roughly a third or more of the body. The hook, the name intro and the closing line stay on the face. Don't flash a cutaway for under 2 s before the next one, don't use a soft (focus-hunting) shot, don't repeat the same angle in one ad, and never put another interviewee's own set into someone else's testimonial. A cutaway must show the line, not filler (a strap being fastened, an empty machine): pick the moment where the coach is visibly coaching or the client is visibly working.
- 2026-11-26 (Liam): don't grade to fix captions. A highlights curve to stop captions washing out on a light jumper darkened the whole ad. Measure the sources first (mean and face-band luma); match the interviews across a set; leave caption contrast to the caption glow.
- 2026-11-26 (Liam, 1 TO 360 round 9): B-roll runs back to back. Chain cutaways into one run and only cut back to the face on key moments (the hook, the line that lands the testimonial, the close), never in, out, in. Plans chain a cutaway onto the previous one ("+" in build_plans), and the renderer holds each cutaway's last frame to the end of its window so a chain never flashes the face between clips. Caption glow eased again: default shadow alpha 0x68 for a dark top, 0x58 with glow 2 on a light top.
