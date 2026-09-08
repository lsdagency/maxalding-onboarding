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

## Length in short-form conversion copy (Feedback 2026-09-07, Oliver Bird)
Liam, on a lead form intro: "This needs to be punchy, why should someone leave their details, what value are they getting?", and on the habit generally, "i've noticed you do this a lot".

Long is the default failure mode in every asset the reader meets mid-scroll: the lead form intro, a static's on-screen copy, a completion screen, a CTA. Explanation feels thorough and reads as friction. The fix is to decide what the ONE job of the line is, write that, and delete the rest. A 437 character lead form intro that answered five questions became 212 characters answering two, and it converted the point better.

Where the rule applies: lead form intro and completion copy, static overlay lines, headlines, descriptions, SMS. Where it does not: spoken scripts and the VSL, where full flowing sentences are correct because a person is talking, and nurture emails, where the reader has already opted in and value-first length is the point. Know which of the two a given asset is before choosing a length.

## Sell the gain, not only the absence of the problem (Feedback 2026-09-07, Oliver Bird)
Liam, on a finished pack: "your angle is quite negative, it's a lot of your running is bad Oli can fix it. What about the flip side, get faster, run for longer, improve your times, run better... All of these positive benefits have been left out? It sounds much more appealing if we're talking to our audience about how they can improve their times instead of calling them out for their running stalling."

This is the failure the positive-language rule below does NOT catch, and the two must be read together. That rule bans putting a negative on the person. It is possible to obey it completely and still produce a campaign built entirely on what is wrong, because "your running has stalled" accuses nobody and is still a whole campaign about a deficit. On the Oliver Bird pack the measured result was stark: of 35 post copy variations, eight were deficit-framed, twenty seven described the testing mechanism, and ZERO led on an upside. The campaign had two registers, something is wrong and here is what the machine does, and it never once said get faster, run further, run more easily, keep running for years.

The customer buys the gain. The problem is context that earns attention; it is never the whole proposition.

**The mechanical check, run before the pack is saved.** Classify every post, headline, hook and on-screen overlay line as gain-led, deficit-led or neutral mechanism. If nothing in the set leads on the gain, or if deficit plus mechanism accounts for the whole set, the copy is not finished. Aim for the gain to lead a clear share of the set and to own the spine, with deficit framing kept to the concepts whose job it genuinely is (Problem to Solution, Audience Addresser) and even there written as available potential rather than present failure ("you have put the miles in, now find the speed" rather than "training hard and the progress has stalled").

**The positive rule extends to the things the audience LOVES, not just to the audience.** A gain-led angle can still be written as a put-down, and the most likely target is whatever the customer is already enthusiastic about: their app, their club, their kit, their current routine. On the Oliver Bird pack the Strava angle was written as "Strava tracks every run you do. What it cannot tell you is which part of your strength would make them quicker", which sets the offer up against a hobby the reader enjoys. Liam: "you've kinda shat on Strava with that line, it's a bit negative again." The fix is to treat the thing they love as a given worth adding to: "The strength work you do this winter shows up on your Strava in spring." Same angle, same offer, and the reader is not asked to accept that something they like is failing them.

**Do not overclaim the client's discipline over the customer's sport.** A support discipline (strength work, mobility, nutrition, physio) makes the main thing better. It is not where the main thing comes from, and a customer who actually does the sport spots the overclaim instantly. On the Oliver Bird pack the line "A quicker parkrun starts in the gym" was flatly wrong to any runner, and it also contradicted the client's own content, where he says speed is a skill you have to go and practise with intervals. Two more had slipped in the same way: "a quicker 5K is mostly about how much force you put into the ground", and a script line dismissing added mileage as moving things "a little" before naming strength as "the thing that actually makes you quicker".

The credibility cost is highest for exactly the clients who trade on evidence, because the overclaim contradicts the positioning that is meant to be selling. Write the support discipline as ADDITIVE and respect the work the customer already does: "Keep doing the intervals. Strength is what makes the same pace feel easier." Check every causal claim against the client's own transcripts before it ships; on this client the correcting evidence was sitting in a reel that had already been transcribed at Stage 1.

**Find the gains at intake.** They are almost always sitting in the onboarding document already and get skipped because the pain points are more vivid. For a running client: faster times, running further, better running economy so the same pace costs less, staying on the road, still running properly in ten years. Oli's own tagline, "run stronger for longer", was the gain the entire time and the campaign had been built past it.

Keep Meta compliance in view while doing this: sell capability and performance, never promise injury prevention or a medical outcome, and never attach an invented number to a time or a result.

## Specificity
If a line could be used by any fitness business in any city, rewrite it with details specific to this client, ICP and offer.

## Never fabricate
Do not invent testimonials, results, numbers, proof, offers, positioning or credentials. Missing items become clearly labelled placeholders. Quantified outcomes such as a specific weight figure may only be used if explicitly present in the client documents.

### Biography is the easiest thing to fabricate and the worst to get wrong
The hero story invites invention, because a vivid origin reads better than a plain one. It is still fabrication. Every biographical claim about the client, what they played, where they trained, what happened to them, how long they have done this, must be traceable to the onboarding documents or their own transcripts. If you cannot point to the line it came from, it does not go in.

Worked example (Feedback 2026-08-13, Xcelerate Performance): the Storytelling concept, the VSL and two ad copy posts were all built on the coach having been "the kid who got stuck on the wing". He had never played rugby. The word rugby appears nowhere in his onboarding document, nor does league, played, team or bench, and none of his nine transcribed reels mention it. It came from the campaign being rugby-flavoured at the time. Liam caught it with one question: "where did you get this from?" That line would have gone into a VSL the client had to read out loud about his own life.

The check, applied to every biographical line before it ships: name the source. Document section, or transcript, or the client said it on a call. "It fits the story" is not a source.
