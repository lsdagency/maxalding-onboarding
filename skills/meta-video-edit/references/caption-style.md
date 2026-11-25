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
- One font: TikTok Sans Black, one size, balanced line breaks. It does not take the captions' mixed type (Liam, 2026-11-25).
- Highlighted: each line sits on a solid box in the brand paper colour, with ink text (`brand.title_box`). Liam preferred this to plain white type, which got lost over the footage.
- Fully up on frame one (no fade-in), for about 3 seconds through the first spoken line.
- Eight words or fewer, from the `ad-hooks` skill. Two lines above the speaker's head (the largest size that fits two lines), over a soft dark gradient from the top of the frame.

## Framing and caption position on talking heads
- Talking heads and interviews keep one framing for the whole ad (zoom about 1.85 on 4K).
- Captions stay in one area, below the chin, centred (Liam, 2026-11-25: moving them round the face did not work, especially against a bright pillar). The face-aware Placer still sets the line just under the detected face and the QA gate still fails any overlap. Other zones (beside or above the head) are opt-in through `captions.zones`, for shots with dark, even backgrounds.

## Contrast without gradients
- No gradients or scrims behind text (Liam: "a weird gradient effect appears behind the text which just looks clunky"). Readability comes from a stronger soft shadow on every word.
- Never a hard border or outline round captions (Liam). On light clothing use a soft dark glow behind the letters (`captions.shadow_alpha` about 0x18, `shadow_blur` 16, `shadow_glow` 6, offset [0, 2]) together with a highlights grade. When light clothing or a light wall washes the type out, grade the clip instead: `grade.highlights` (for example -0.16) pulls the bright areas down, and `grade.exposure` sets overall exposure.

## Ending
- No end card and no on-screen offer. The ad ends naturally on the client's strongest closing line. Most viewers have gone by then, and the offer belongs in the ad copy and the CTA button (Liam, 2026-11-25). Put an offer on screen only when a brief explicitly asks for it (`cta_required` in the plan turns the QA check back on).
