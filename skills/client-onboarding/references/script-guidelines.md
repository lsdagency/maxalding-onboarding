# Video Ad Scripts guidelines

Document 1, built with build/video_ad_scripts.py. Apply ad-creative principles before writing hooks and scripts.

## Typography and header
Helvetica Neue on every run (python-docx falls back to Cambria otherwise; set it explicitly on every run). Main heading size 16 bold; section subheadings size 14 bold; all body, direction notes and script lines size 10. Header labels bold, values unbolded. No date in the header (CLIENT, CAMPAIGN, PREPARED BY only). Logo at the top.

## Context and format
Top context block in bold: the scripts are guidance only and must not be read word for word; the talent says it in their own words, natural and creative, while hitting the key beats and timing. Filming format: filmed vertical 9:16. Do not mention the VSL or 16:9 in this document.

## Recording best practice (8 points)
Vertical 9:16; strong first frame, eyes to lens immediately; eye level, arm's length, face centred; natural light facing a window; quiet room, test a 5 second clip, use a mic; clean background with brand cues; calm confident pace, pause after key lines; record 3 takes.

## Editing best practice (research it every run)
The document carries an EDITING BEST PRACTICE section after RECORDING BEST PRACTICE, so the editor has current paid-social / Reels guidance in the same file. Before each build, RESEARCH current best-practice editing tips for Instagram Reels and Meta video ads (web search) and pass the refreshed list as `data["scripts"]["editing_best_practice"]`; the builder falls back to a sensible evergreen default if none is supplied. Keep it in the same dashed bullet format. Typical points: win the first 3 seconds on the hook, burned-in captions for sound-off, 9:16 safe zones, cut dead air and change something visual every 1 to 2 seconds, short high-contrast on-screen text, brand cue early, native and handheld feel around 15 to 30 seconds, end on a clean CTA card. Add any campaign-specific editing notes here too (for example seasonal or birthday motion like a confetti burst).

## The eight concepts
Write all eight video concepts (Creative Tracker rows 6 to 13). Each block:
- CONCEPT n in caps, then Format, Talent, Audience, Angle.
- A short plain paragraph on what it is and how to film it.
- Hook Options (film all three): Option A, B, C. All three are filmed and tested; never tell the client to choose one. Hooks under 12 words, specific, never "you" plus a negative attribute. Two hard requirements on top of that:
  - They must sound like a voicenote. Each hook is the exact thing a real person would say out loud to camera in the first second, in natural spoken English with contractions and a real spoken opener where it fits ("Okay", "Real quick", "Honestly", "Here's the thing", "Don't scroll past this"). Not a written slogan, not a caption, not a headline read aloud.
  - The three must span DIFFERENT hook types, never three wordings of one idea. Deliberately mix across question, curiosity gap, urgency, bold statement, empathy or relatable, and pattern interrupt, with at least one statement in the set. When the campaign hangs on an occasion or theme (a birthday, a season, a launch), carry it through the hooks, but do not make all three sell; let some open on the sentiment and leave the offer to the script body and CTA.
- A timestamped script. Add a direction note only where genuinely needed, for example the hook. Content beats are just the timestamp, the section label and the spoken line. Spoken lines are wrapped in quotation marks and rendered in grey; any direction note is italic and grey.
- Write it the way the coach would actually say it to camera: like a voicenote to a mate, not a list of slogans. Full, flowing sentences in plain spoken English, contractions and all (you are saying it out loud, so "it is" can be "it's", "we will" can be "we'll"). Each beat is the timestamp, the section label, and one or two natural spoken sentences that connect to each other. Do NOT chop the script into clipped 6 to 10 word lines, and do not pad or trim to hit a line or word count. Keep it on message and hitting the beats, roughly 20 to 45 seconds spoken, but it must sound like a real person talking. The banned characters, banned words, positive-language and Meta rules still apply.
- CTA (film this ending): one firm CTA per concept, not three options. A single spoken line that names the offer AND conveys its value tied to the pain point named in this ad's angle: say what they get from it and why it matters to them, not just a bare instruction to come in. For example, tie a free session to the time-pressure angle with "grab a free session and we'll build a plan that finally fits your week". No clicking or booking verbs anywhere except this final line, no invented results or deadlines, no marketing terminology.
- Separate concepts with a dash line.

Each of the eight uses a meaningfully different angle, pain context and objection (time, confidence, intimidation, consistency, support, accountability, commitment). For a beginner-intimidating niche, confidence and "this is for normal people" leads.

## Audience Addresser concept, specific rules
A direct-to-camera format with a four-beat structure: hook (direct callout, statement, names a lived experience not a demographic), understand them (2 to 3 lines naming specific daily situations), pain point (1 to 2 lines on the emotional cost, positive-language rule applies), present the solution (2 to 3 lines on the coaching approach), CTA (one clear instruction, offer named exactly).

The three hooks must each call out the audience in a distinct way: one names the age range (from the ICP), one the job or role, one the daily situation. Questions are allowed and encouraged here. The viewer should feel recognised, not targeted.
