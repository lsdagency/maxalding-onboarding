# Caption and on-screen text style

The house style for every burned-in word. The engine (`editor/captions.py`) implements it; this file is the reason behind each choice.

## Font
- TikTok Sans for all clients, matching the statics (Liam, 2026-11-25).
- Hook titles, CTA text and end cards: TikTok Sans Black (900).
- Captions: TikTok Sans Bold (700).
- The renderer cuts a static instance of each weight from the variable font so the caption renderer cannot fall back to Helvetica. The edit QA gate fails any render where it did.

## Captions: editorial (house default)
From Liam's four caption references, 2026-11-25. They're saved in the workspace at video-references/captions/ with contact sheets. What they share, and what the engine does:
- **Mixed type.** Words are TikTok Sans Bold. Connecting words ("the", "to", "with", "is", "in") are smaller and lighter (TikTok Sans Medium, about 74 percent size). The one word per phrase that carries the meaning is large (about 1.5 times) in the brand's serif italic (1 TO 360: Cormorant Italic, matching the statics' serif accent). The plan's `captions.emphasis` list picks the serif words. Use restraint: roughly one every two or three phrases, never one per line.
- **Small over big.** If the serif word isn't first, it starts the second line ("until the / *end*", "something / *different*").
- **Words arrive as spoken.** Each word fades and sharpens in over about 140 ms. The whole phrase is laid out from its first word, so nothing jumps. No bounce, no pop, no karaoke colour, no box.
- **White with a soft shadow,** no outline. A soft dark band sits behind the caption area while anyone is speaking. It's about 34 percent by default; raise `captions.scrim` for light clothing or bright walls (client 2's grey hoodie needed 0xA0). This is the video version of the statics' contrast scrims.
- **Size.** 104 px base on 9x16, 88 px on 4x5. A phrase that won't fit two lines scales down rather than spilling to a third. A phrase made only of connecting words shows at full size.
- **Placement.** 61 percent down on 9x16, below the face. A taller phrase lifts to stay in the safe zone.
- Chunks run up to four words and break at pauses and punctuation. Names, places and offer lines are held together with `keep_together`.
- Every caption word matches the audio. Captions stop at the end card.
- **Never** boxed or karaoke active-word highlights, bouncing pops or emoji captions (Liam: "AI slop"). `captions.style: "clean"` (plain white phrases) is the fallback.

## Hook title
- Fully up on frame one (no fade-in), for about 3 seconds through the first spoken line.
- A few words, the point of the ad: the audience, the offer or the client's strongest line paraphrased. Eight words or fewer, from the `ad-hooks` skill.
- The same editorial type as the captions, with no box: TikTok Sans Black, connecting words smaller, one serif-italic word (`emphasis` on the title). Up to three lines above the speaker's head, at the top of the safe zone, over a soft dark gradient from the top of the frame.

## CTA and end card
- The CTA line sits at the bottom of the safe zone, or on the end card.
- End card mirrors the static End card: brand accent background, the offer as the biggest thing on screen, a support line, then the CTA line (for 1 TO 360: "4 for 3", "Start with four sessions for the price of three.", "Tap below and Sergio will call you").
- 2.5 to 4 seconds, long enough to read twice.

## Copy rules still apply
On-screen text runs through the same validator as every other deliverable: no exclamation marks, em dashes or ellipses, no banned words, no weight figures, premium framing ("never free" for high-ticket clients).
