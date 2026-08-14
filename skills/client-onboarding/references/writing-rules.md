# Global writing rules

Apply to every output without exception, including inside Python or Node build-script strings.

## Banned characters
- No em dashes and no en dashes. Rewrite with a comma, period or colon. Scan every build-script string before saving and replace any that slip in. Zero exceptions.
- No exclamation marks.
- No ellipses for effect, neither the single glyph nor three periods.
- No all-caps words for emphasis inside body copy.

## Banned words
- The word "structure" used as a noun for a programme, plan or approach. Replace with approach, method, process, plan, routine, the way it works.
- The word "framework" in the same sense. Replace with approach, method, way of working.
- These are allowed only inside an explicit rule-statement cell that documents the ban, for example the BANNED IN COPY row.

## Client word bans
Pull the live list from the client Brand memory. Example fitness list: quick fix, miracle, extreme, hack, guaranteed transformation, fear tactics, negative comparisons, unrealistic claims.

## Banned phrases
Here is the truth, the reality is, in today's world, at the end of the day, with that being said, in other words, as you can see, game changer, next level, proven system, done for you, unlock your potential, transform your life, amazing, incredible, powerful, effortless, world class, this means that, it is important to note, in summary, and filler openers like hey guys, so today, let us dive in.

## Banned formula
Never use "it is not a X problem, it is a Y problem" or any close variant. It reads as AI generated. State the idea directly. The validator errors on the literal form and warns on the wider "not X, it is Y" shape (rule `contrastive-correction`).

## AI cadences (Feedback 2026-08-11, Xcelerate Performance)
Liam: "These are obvious Claude AI lines, I've seen them over and over again." None of these are banned words, they are banned SHAPES, and they are the fastest way to make spoken copy sound written.

- **The significance clause.** A clause bolted on the end to explain why what you just said matters: "and that's the whole reason I ended up coaching", "because nobody ever spells this out", "which is exactly why it works", "and that's not nothing". Real people say the thing and stop. Cut the clause and keep the sentence.
- **The neat balanced summary.** A tidy symmetrical phrase where a plain one would do: "coached as one of twenty", "trained, not just supervised". Nobody talks in balanced pairs.
- **The "not X, it is Y" contrast.** See the banned formula above.
- **Stacked subordinate clauses.** A spoken line should carry one idea. If a sentence has two commas and a "which", it was written, not said.
- **Explaining your own joke or point.** If a line lands, the next line must not restate why it landed.

The fix is not a synonym swap. Write the line the way the client would actually say it out loud, then read it back in their voice. If you cannot hear them saying it, it goes.

## Write in the client's actual register
Every onboarding transcribes the client's Instagram videos at Stage 1 (references/instagram-research.md). That transcript is the register, and it is not optional context: mine it for the client's real sentence length, their openers, their tag questions, their filler words, the words they repeat, and the things they genuinely say. Put a "How [name] actually talks" block in the Brand memory AND in the Brand Pack TONE OF VOICE so it travels with the pack, and write every spoken line against it.

Signals worth counting off the transcript: how often they say yeah, mate, look, right, alright, okay, reckon, gonna, gotta. Whether they use tag questions. Whether they repeat for emphasis. How long their average sentence is. A coach who says "as hard as you can, as hard as you can" and "drive, drive, drive" does not then say "which is exactly why the approach works".

### Write to the whole audience, not the half you pictured
Do not narrow an audience's gender, or any other attribute, further than the client and the brief actually did. Check the pronouns in a finished draft against the ICP as agreed, not against the examples that happen to exist in the client's proof. A coach whose filmed clients are all boys still coaches girls, and the parent reading the ad may have either (Feedback 2026-08-13, Xcelerate Performance: the whole pack said "your son" and "he" throughout, which halved the audience on a small budget). Neutral audience-facing language ("your kid", "they") costs nothing and keeps the proof intact, because named real people keep their own pronouns.

### Two registers, and the difference between them
The transcript governs the SHAPE of the client's speech: sentence length, openers, tag questions, cadence, what they repeat, and the technical vocabulary of their craft. Never put a shape in their mouth the transcript does not support.

Audience-facing VOCABULARY is a separate question, and it may legitimately come from the audience's own language rather than the client's transcript. A line that addresses the customer can use the customer's word for something even when the client did not happen to say it in the reels you transcribed, provided the client would plainly say it in life. Xcelerate is the worked example: "footy" appears nowhere in nine transcribed reels, where Zack's on-camera sport vocabulary is all coaching technical (contact, bumpers, post contact metres, play the ball). But every Sydney league parent says "footy", and Liam kept it on exactly that ground (2026-08-11).

So: evidence the shape from the transcript, evidence the vocabulary from the transcript OR the ICP, and be able to say which. What is never acceptable is reaching for a word because it merely sounds like the region or the trade. If you cannot point to either source, it is a guess, and guesses are how the copy ends up sounding like an impression of the client rather than the client.

## The client's physical format (Feedback 2026-06-03, Evolve Fitness Glenhaven)
Establish the client's PHYSICAL FORMAT at Stage 1, before a word is written, and record it in the Brand memory and the Brand Pack. It is one of: outdoor (a park, oval, beach or field), indoor gym, private studio, online only, or a mix. The format is not a detail, it is the thing the reader pictures, and getting it wrong tells them immediately that nobody looked at the business.

Evolve Fitness Glenhaven is an outdoor bootcamp that runs at Glenhaven Oval all year. The copy kept saying "come inside" and describing the business as though it had a building. Every line has to reflect where the training actually happens.

For a client with no indoor space, never write a line that asserts one:
- "come inside", "step inside", "come on in", "through our doors", "on the gym floor", "in our studio", "our facility", "under one roof".
- The generic "at [client name]" is safe and often better than naming a venue at all.
- Naming a competitor's building is still fine, and often the point: "without the intimidation of a traditional gym" is correct copy for an outdoor bootcamp.

For an online-only client the same rule bans any physical venue language at all. For an indoor client, the reverse applies: do not write outdoor scenes into a business that trains under a roof.

The validator warns on indoor-space language via the rule `venue-language`. It is waived automatically when the client data sets `business_format` to an indoor format, so set that field on every client.

## Seasonal and environmental context (Feedback 2026-06-03, Evolve Fitness Glenhaven)
Identify, at Stage 1, the season the campaign runs into and any environmental condition the client trains through, then let it run naturally through the creative. A campaign launching into a Sydney winter for an outdoor bootcamp is not the same campaign as one launching into spring: the real obstacle is getting out of bed in the cold and the rain, and the real proof is that the group does it anyway.

Where to find it: the campaign start date against the client's hemisphere, and anything in the onboarding documents about weather, seasonality, quiet periods or peak periods.

How to use it. Weave it through the concept set where it genuinely belongs, not into every line. It should read as context the writer noticed, never as a theme bolted onto copy that did not need it. On the Evolve pack it belonged in the Problem to Solution angle (why a group keeps you going when it is cold), in the Social Proof concepts (people who turn up anyway) and in the Pattern Interrupt (training in the rain). It did not belong in the Incentive concept, which is the offer and nothing else.

If the campaign has no meaningful seasonal or environmental angle, say so at the Stage 2 gate and leave it out. A forced season is worse than none.

## Positive language rule (critical)
Never frame the problem as a personal failing, even when negating it. Do not write "you are not lazy", "the gym did not fail you", "you have not been consistent", "stop making excuses", "you know you should". Lead with what the person is capable of and what becomes available to them. Replace accusation with understanding. For example, instead of "you are not lazy" use "you have been doing this without the right support"; instead of "you have not been consistent" use "consistency becomes easier when the approach fits your life". Applies to hooks, post copy, scripts, the VSL and the landing page.

## Specificity
If a line could be used by any fitness business in any city, rewrite it with details specific to this client, ICP and offer.

## Never fabricate
Do not invent testimonials, results, numbers, proof, offers, positioning or credentials. Missing items become clearly labelled placeholders. Quantified outcomes such as a specific weight figure may only be used if explicitly present in the client documents.

### Biography is the easiest thing to fabricate and the worst to get wrong
The hero story invites invention, because a vivid origin reads better than a plain one. It is still fabrication. Every biographical claim about the client, what they played, where they trained, what happened to them, how long they have done this, must be traceable to the onboarding documents or their own transcripts. If you cannot point to the line it came from, it does not go in.

Worked example (Feedback 2026-08-13, Xcelerate Performance): the Storytelling concept, the VSL and two ad copy posts were all built on the coach having been "the kid who got stuck on the wing". He had never played rugby. The word rugby appears nowhere in his onboarding document, nor does league, played, team or bench, and none of his nine transcribed reels mention it. It came from the campaign being rugby-flavoured at the time. Liam caught it with one question: "where did you get this from?" That line would have gone into a VSL the client had to read out loud about his own life.

The check, applied to every biographical line before it ships: name the source. Document section, or transcript, or the client said it on a call. "It fits the story" is not a source.
