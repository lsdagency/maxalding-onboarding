# Video Ad Scripts guidelines

Document 1, built with build/video_ad_scripts.py. Apply ad-creative principles before writing hooks and scripts.

## Typography and header
Helvetica Neue on every run (python-docx falls back to Cambria otherwise; set it explicitly on every run). Main heading size 16 bold; section subheadings size 14 bold; all body, direction notes and script lines size 10. Header labels bold, values unbolded. No date in the header (CLIENT, CAMPAIGN, PREPARED BY only). Logo at the top.

## Context and format
Top context block in bold: the scripts are guidance only and must not be read word for word; the talent says it in their own words, natural and creative, while hitting the key beats and timing. Filming format: filmed vertical 9:16. Do not mention the VSL or 16:9 in this document.

## Recording best practice (8 points)
Vertical 9:16; strong first frame, eyes to lens immediately; eye level, arm's length, face centred; natural light facing a window; quiet room, test a 5 second clip, use a mic; clean background with brand cues; calm confident pace, pause after key lines; record 3 takes.

## No editing best practice section
The document used to carry an EDITING BEST PRACTICE section after RECORDING BEST PRACTICE. It was removed on 2026-08-11 (Feedback, Xcelerate Performance). This document is the TALENT'S filming brief: generic Reels editing guidance belongs with the editor, not with the person holding the phone, and per-concept editing direction already lives in the Creative Plan EDITING DIRECTION column. Do not reinstate it, and do not web-search editing tips for this document.

## The seven concepts
Write all seven video concepts (the VIDEO rows of the Creative Tracker, which follow the seven statics): Problem to Solution, Social Proof (Client Interview), Pattern Interrupt, Storytelling (Full Voiceover B-Roll), Benefit, Incentive, Audience Addresser.

Each concept has a distinct job and they must not bleed into each other (Feedback 2026-08-11, Xcelerate Performance, where the Incentive video had drifted into explaining the offer and left Incentive with nothing of its own):

- **Problem to Solution**: name the exact pain the ICP lives with, then show the coach's answer to it.
- **Social Proof (Client Interview)**: a real client answering a question set, in their own words. See the interview section below.
- **Pattern Interrupt**: break the scroll with something unexpected. Drop this concept first when the plan already carries strong existing-post ads.
- **Storytelling (Full Voiceover B-Roll)**: the COACH'S own story. What made them want to coach, how long they have been doing it and who with, and what they genuinely love about it. Not a client story, and not the offer.
- **Benefit**: explain the OFFER properly. What the client actually gets, what comes as part of the package, and what they can expect from working with this coach. This is the concept that answers "what am I buying".
- **Incentive**: the offer or the price, short and sweet. One clear reason to act now and a CTA. Do not explain what the package contains here, that belongs to Benefit.
- **Audience Addresser**: talk directly to the ICP about what they are trying to achieve. See the Audience Addresser section below.

Where a number belongs in the coach's story (years coaching, athletes worked with) and the client documents do not provide it, leave a clearly labelled placeholder and flag it. Never invent it.

Each block:
- CONCEPT n in caps, then Format, Talent, Audience, Angle.
- A short plain paragraph on what it is and how to film it.
- Hook (the opening line): exactly ONE hook per concept (the Option A/B/C menu is retired as of 0.17.0; Feedback 2026-08-07, BodyShaping). Generate several angles with the ad-hooks skill, pick the strongest, perfect it, and write it as the true first spoken line of the take. The build mirrors this hook into the Creative Plan's HOOK GUIDANCE column; never hand-write that tracker cell separately: build through build.build_all so the two files cannot drift apart. A video hook is the strong, full SPOKEN opening line, a sentence or two (per the ad-hooks skill), not a short static-style fragment; it IS the best line in the concept, the scroll-stopper, not a throwaway before the real opener. Specific, never "you" plus a negative attribute. Three hard requirements on top of that:
  - They must sound like a voicenote. Each hook is the exact thing a real person would say out loud to camera in the first second, in natural spoken English with contractions and a real spoken opener where it fits ("Okay", "Honestly", "Here's the thing", "Don't scroll past this"). Not a written slogan, not a caption, not a headline read aloud.
  - The register must match the ICP's AGE and world, not a generic social-media voice. For an over-30 audience never use under-30 slang ("real talk", "no cap", "lowkey", "vibe"). Pull the register from the client's own transcript and brand voice: slang is only allowed when the coach or the ICP genuinely uses it (for example an Australian client who says "cooked" on the call). When in doubt, plain and direct beats slangy. Invoke the ad-hooks skill EVERY time hooks are written or rewritten, including revision rounds, not only the first pass.
  - The hook and the body must CHAIN, never overlap. The hook opens a thought (a question, a claim, a story lead) and the body's first line advances it; if they say the same thing in different words (hook "One of my clients came to me tired" then body "He came to me tired"), the hook has failed. Write hook plus body as one continuous spoken piece and read them aloud back to back before accepting (Feedback 2026-08-07, BodyShaping: three swappable hooks over one fixed body could not truly chain, hooks either disconnected from the body or duplicated it, which is why scripts moved to one hook).
  - Across the concept set the hooks must span DIFFERENT hook types, never rewordings of one idea. Deliberately mix across question, curiosity gap, urgency, bold statement, empathy or relatable, and pattern interrupt, with at least one statement in the set. When the campaign hangs on an occasion or theme (a birthday, a season, a launch), carry it through the hooks, but do not make every hook sell; let some open on the sentiment and leave the offer to the script body and CTA.
- A timestamped script. The first script beat is the hook beat: a short direction note, no repeated line, telling the talent the hook above is the first spoken line of the take and the script continues straight from it. The body then starts at the next timestamp and chains from the hook. Add a direction note elsewhere only where genuinely needed. Content beats are the timestamp, the section label and the spoken line. Spoken lines are wrapped in quotation marks and rendered in grey; any direction note is italic and grey.
- Write it the way the coach would actually say it to camera: like a voicenote to a mate, not a list of slogans. Full, flowing sentences in plain spoken English, contractions and all (you are saying it out loud, so "it is" can be "it's", "we will" can be "we'll"). Each beat is the timestamp, the section label, and one or two natural spoken sentences that connect to each other. Do NOT chop the script into clipped 6 to 10 word lines, and do not pad or trim to hit a line or word count. Keep it on message and hitting the beats, roughly 20 to 45 seconds spoken, but it must sound like a real person talking. The banned characters, banned words, positive-language and Meta rules still apply.
- CTA (film this ending): one firm CTA per concept, not three options. A single spoken line that names the offer AND conveys its value tied to the pain point named in this ad's angle: say what they get from it and why it matters to them, not just a bare instruction to come in. For example, tie a free session to the time-pressure angle with "grab a free session and we'll build a plan that finally fits your week". No clicking or booking verbs anywhere except this final line, no invented results or deadlines, no marketing terminology.
- Separate concepts with a dash line.

Each of the eight uses a meaningfully different angle, pain context and objection (time, confidence, intimidation, consistency, support, accountability, commitment). For a beginner-intimidating niche, confidence and "this is for normal people" leads. A strong optional ninth angle for any client whose ICP has bought the service before: a "tried it before and it didn't stick" concept that validates the past attempt, names why generic plans fail, and presents the difference (proven buyers convert best).

Multi-location clients: never name two distant locations in the same spoken script or VSL. Pick ONE launch location per script set (decided with the client at the confirm gate, weighing where they are best known against demographics and any local sponsorships), write every location mention to that one place, and clone the campaign for the second location later. The Creative Plan brand pack still records all locations as fact.

## Social Proof concept, client-interview format (coaches and gyms)
The social proof video is an interview, never a monologue and never a script the client reads. The brand (the coach) asks the questions off camera and the client answers in their own words. This applies to every coach and gym client (Fisica, 2026-07-16).

- The script block is a QUESTION SET with guided responses: each beat is a direction note carrying the question the coach asks and what to guide the client to mention in that answer (for example, get them to mention how long they had been dealing with it and what they had already tried). No spoken lines are written for the client.
- Hooks: one of the three is ALWAYS the client's introduction line, for example "Hi, I'm [NAME] and I've been training at [Client] for the past year." The other two are pulled from the strongest moments in the client's actual answers during the edit; write them as example pull-lines and say so in the intro and the hook direction note.
- One interview concept per plan. The client records the same question set with a few different clients or members, and each interview becomes its own ad variant. Do not write a second social proof video concept.
- All the usual rules apply to the questions and guidance: positive language, no invented specifics, Meta compliance, and results framed as one person's real experience.

## Full voiceover B-Roll concept, one per plan
Exactly one video concept per plan runs as a full voiceover over B-Roll with no talking head. Storytelling is the default choice because continuous narration carries it best. The talent records the narration clean on a mic and the whole edit is cut to it. The concept's FILMING DIRECTION in the Creative Plan is a concrete B-Roll shot list, specific to the client's spaces and coaching moments, and doubles as the client's filming brief. Clients are typically short on B-Roll; this concept deliberately pushes them to film it, so make the shot list practical and specific.

The shot list must map to the script beats: for each line or beat of the voiceover, name the footage that could sit under it, and tell the client to go through the script line by line filming or supplying existing footage to match (including archival footage from their own history where the story calls for it). When handing the pack to the client, point them at a shared content upload folder for everything they film or supply, and push B-Roll volume hard: short 10 to 20 second phone clips, unpolished over staged, no such thing as too much, spare footage feeds every future edit. Do not tell them work starts on partial uploads; the edit starts once the full set is in. The handover email itself follows references/handover-email.md.

## Audience Addresser concept, specific rules
A direct-to-camera format with a four-beat structure: hook (direct callout, statement, names a lived experience not a demographic), understand them (2 to 3 lines naming specific daily situations), pain point (1 to 2 lines on the emotional cost, positive-language rule applies), present the solution (2 to 3 lines on the coaching approach), CTA (one clear instruction, offer named exactly).

The hook calls out the audience directly, built from the ICP's age range, job or role, or daily situation, whichever lens is strongest for this client (combining two is fine, for example age plus situation). Questions are allowed and encouraged here. The viewer should feel recognised, not targeted.
