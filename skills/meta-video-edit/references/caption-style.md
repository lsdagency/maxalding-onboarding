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
- One font: TikTok Sans Black, white, one size, with balanced line breaks. It does not take the captions' mixed type (Liam, 2026-11-25). No box.
- Fully up on frame one (no fade-in), for about 3 seconds through the first spoken line.
- Eight words or fewer, from the `ad-hooks` skill. Two lines above the speaker's head (the largest size that fits two lines), over a soft dark gradient from the top of the frame.

## Captions that move with the edit (layout director)
What made Liam's references work is that the captions change position and interact with the shot, so the eye keeps getting pulled back. The engine's director gives each piece a layout at sentence or module boundaries, roughly every three to six seconds:
- **centre:** subject centred, captions below the face.
- **side:** the subject is reframed off-centre and the caption stacks big in the open space beside them, left or right aligned. The 4K source gives the room.
- **punch:** a tighter crop, captions below.
- The rhythm is side, centre, side, punch. The hook stays centred under the title.
- Side text only goes where the background is dark enough for white type. The director samples the frame and never puts text on a bright wall or light pillar.
- A phrase always breaks where the framing changes.
- Inside a run of one layout, alternate pieces step the zoom by 6 percent, so jump cuts still read as cuts.
- A plan can pin layouts with `layouts` or limit sides with `sides`.

## CTA close (no end card by default)
- The ad closes on a short muted beat of the client listening (2.5 to 3 seconds), with the offer set over the footage in the hook's plain TikTok Sans Black at the bottom of the safe zone (1 TO 360: "4 sessions for the price of 3"). The Meta CTA button and the primary text do the "tap below". A solid branded slate reads as an ad and invites the swipe, so use one only when Liam or the brief asks for it.
- End card mirrors the static End card: brand accent background, the offer as the biggest thing on screen, a support line, then the CTA line (for 1 TO 360: "4 for 3", "Start with four sessions for the price of three.", "Tap below and Sergio will call you").
- 2.5 to 4 seconds, long enough to read twice.

## Copy rules still apply
On-screen text runs through the same validator as every other deliverable: no exclamation marks, em dashes or ellipses, no banned words, no weight figures, premium framing ("never free" for high-ticket clients).
