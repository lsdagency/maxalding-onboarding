---
name: meta-ad-copy
description: Write Meta (Facebook and Instagram) ad copy for an existing Maxalding client, as a standalone task outside a full onboarding. Triggers include "write ad copy", "ad copy for these videos", "Meta ad copy", "post copy and headlines", "more ad variations", "ad copy for [client]", or any request to produce post copy, headlines, or a description for paid social. Produces the AD COPY spreadsheet, never a chat list, using the same format and rules as the onboarding Creative Plan.
---

# Maxalding Meta Ad Copy

This skill produces Meta ad copy for a client who has already been onboarded, when ad copy is requested on its own rather than as part of a full onboarding run (for example, post copy for a batch of filmed videos). It exists because these requests kept arriving outside onboarding, where the AD COPY rules were not being triggered, and the copy came back as a patterned chat list instead of the spreadsheet. See the Onboarding Feedback Log entry dated 2026-06-24.

The rules here are the single AD COPY standard, identical to the onboarding deliverable. The authoritative spec is `../client-onboarding/references/creative-plan-spec.md` (Tab 3). Writing craft lives in `../client-onboarding/references/writing-rules.md`. If anything here ever conflicts with those files, those files win, and update this skill to match.

## Read first, every time
Read the shared Onboarding Feedback Log in full before writing anything. It lives in the workspace folder, not in this package (resolve with the `MAXALDING_WORKSPACE` env var, default `./maxalding-workspace`). Apply every instruction in it. The most recent feedback wins on conflict. Then read the client's memory files (Audience, Brand, Marketing, KPIs) so the copy uses the real ICP, offer, tagline, words-to-use and banned-copy list. If a client tagline was not defined at onboarding, define a short one now and use it for the description.

## Delivering the file (do not hand-encode binaries)
Build the XLSX and save it into the session outputs directory, then let the user open it with Google Drive (the Cowork native upload moves the real bytes). Never hand-encode the workbook as base64 into a Drive create-file call: reproducing thousands of base64 characters corrupts the xlsx and it will not open. If the user wants it in a specific Drive folder, ask which one, but the file still travels via the outputs directory and the open-with-Google-Drive step, not a pasted blob.

## Read-only package, writable workspace
This package is read-only at runtime. Save the generated XLSX into the client's workspace folder (or alongside the client's other deliverables), then upload it to the location the user provided.

## What you produce
One AD COPY spreadsheet, built with the deterministic build module. Never a chat list, never hand-formatted. Layout, columns and styling are fixed by the builder:

- Columns: `# | CONCEPT | POST COPY | CHARS`. No STATUS column, no CTA column or note.
- Organise by distinct concept only, no duplicate concept rows. For a batch of videos, each video maps to one concept (use the video's subject or angle as the concept name).
- 5 post copy variations per concept.
- One shared block of 5 headlines and one shared description that cover all concepts.
- CHARS is a live `=LEN()` formula on every copy cell. Never hardcode a count.

## The rules (apply before writing a single cell)
Apply the `marketing-skills:ads`, `marketing-skills:ad-creative` and `marketing-skills:copywriting` principles. Then:

Post copy
- No longer than 125 characters, with a clear hook in the first line that stops the scroll.
- Each of the five is genuinely unique: a different angle or approach, not a reword of the others.
- One rhetorical question per post maximum.
- Speak to a pain point or desire the ICP already holds. No generic hooks.

Headlines
- Exactly 5, shared across all concepts. No more than 40 characters, ideally around 30.
- Always include one audience-addresser variation and one offer variation, plus a few on other angles.

Description
- One only, no more than 25 characters. Use the client tagline where it fits.
- Tie the messaging together. Do not repeat the offer already carried by the post copy and headlines.

Fluid, not patterned (this is the rule that gets missed)
- Vary length on purpose. Do NOT pad toward 125. Short often reads stronger. The set of lengths across the five should look hand-written, not clustered near the limit.
- Emoji are optional and intentional. Add one only where it genuinely fits and leave it out everywhere else. Never one-per-row as a pattern. Match the brand tone (no hype emoji for a calm, grounded brand).

Banned copy (zero exceptions, scan every cell including build-script strings)
- No em dashes or en dashes anywhere. No exclamation marks.
- The client's own banned list from the Brand memory always applies (for fitness clients this typically includes: structure as a noun, framework, weight-loss-as-headline, burn calories, shred, tone up, bikini/summer body, no pain no gain, beast mode, hack, shortcut, quick fix, game changer, next level, proven system).
- No negative framing of the person, even when negated (no "you are not lazy", "you have not been consistent"). Lead with what becomes available to them. Understanding, not accusation.
- Check every hook, headline and post against Meta's Personal Attributes policy: do not assert or imply the viewer's body, weight or health. Name the offer, not the viewer's flaw.

## Build it deterministically
Assemble the `ad_copy` data dict and build with the module. This guarantees the format, styling and live formulas without hand-formatting:

    python -m build.ad_copy "<ad copy data>.json" --out "<workspace client folder>"

The JSON shape:

    {
      "client_business_name": "FIT Republik",
      "ad_copy": {
        "concepts": [
          {"concept": "Concept or video name", "posts": ["p1", "p2", "p3", "p4", "p5"]}
        ],
        "headlines": ["h1", "h2", "h3", "h4", "h5"],
        "description": "Shared description"
      }
    }

The builder reuses the Creative Plan AD COPY tab generator, names the file `MAXALDING - [Client] - Meta Ad Copy.xlsx`, and runs a structure and character-limit check (5 posts per concept, post <=125, headline <=40, description <=25) before saving. If the client already has a Creative Plan, the same copy can instead be pasted into that file's AD COPY tab.

## Run the QA gate (mandatory)
After building, run the deterministic validator over the file and fix every error before handing over:

    python -m validator.cli "<output file>.xlsx"

It checks banned characters, banned words, positive-language, Meta personal-attributes compliance, the length limits, and the naming convention. The gate must pass with 0 errors.

## Before you hand over
Run this scan and fix anything that fails:
- Output is the XLSX, not a chat list.
- Lengths are genuinely varied, not clustered near the limit. Emoji is intentional, not one-per-row.
- Each post is a distinct angle. Each concept has exactly 5.
- Headlines: exactly 5, one audience-addresser, one offer, all <=40 (ideally ~30).
- Description: one, <=25, uses the tagline, does not repeat the offer.
- Zero em dashes, en dashes or exclamation marks. Client banned list clear. Meta personal-attributes clear.

Tell the user the file name and remind them to upload it to the client's Google Drive folder.
