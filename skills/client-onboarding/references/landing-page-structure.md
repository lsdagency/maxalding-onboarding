# Landing Page Copy structure

Document 3, built with build/landing_page.py. Apply copywriting principles. Same typography and header, no date, logo at top. Use "you" language, plain English in the client's voice, clear within 5 seconds on mobile, one consistent CTA throughout.

This is conversion copy and must be substantial and social-proof led, not a thin "what we offer" page. Use a premium, proof-heavy structure modelled on high-end coaching sales pages.

## Sections in order
1. Top bar: premium positioning line plus a real constraint if one exists (for example limited consultations each month).
2. Hero: outcome headline, supporting subheadline, single premium CTA (for example "Book My Consultation"), support line, and a social-proof bar placeholder (rating, client count, any "as featured in").
3. Social proof strip directly under the hero: star rating and a few one-line client quotes (placeholders if not supplied).
4. The reality: short problem section in the ICP's language, framed with understanding (positive-language rule).
5. Why a real coach makes the difference: authority section, value framed around the human and expert difference (built around your life, expert eyes weekly, accountability, efficient by design), not feature lists.
6. Real results and transformations: lead with proof. Realistic, modest before-and-after placeholders with first name and a one-line result.
7. Meet the coach: authority and story; credentials placeholder.
8. Testimonials grid: aim for six, with name, role or age, specific result and how it felt (placeholders if not supplied).
9. Who this is for: four lines that let the right person self-select.
10. How the consultation works: the lead magnet reframed premium, a private one-to-one consultation, three simple steps, a value line that it is a genuine working session, not a sales pitch.
11. FAQ and objections: busy or time, tried before, what it costs (complimentary, leaves with a plan), how soon results.
12. Guarantee: the client's real risk reversal.
13. Final CTA: recap value, repeat the one CTA.
14. Footer: business name, privacy policy placeholder, unsubscribe note.

This document covers the LANDING PAGE only. It does not automatically include the second step of the funnel, so decide explicitly and say which pages are in scope.

If the funnel uses separate pages, also provide a **booking page** (calendar above the fold, a short what-to-expect list, a reassurance testimonial placeholder, and nothing else competing with the calendar) and a **thank-you page** (confirmation, what happens next and when, a warm trust line). Write them as their own sections in the same document, clearly titled, so nobody has to guess whether they were covered.

Only produce this document at all when `funnel_type` is `landing_page`. A lead-form funnel gets Meta Lead Form copy instead (skills/meta-lead-form), where the completion screen is the equivalent second step.

## Lay the document out like the page (Liam, 2026-11-19, Fisica)
A run of section headings and paragraphs is hard to picture. Write the document so the reader can see the page:
- Open with THE PAGE AT A GLANCE (`landing_page.overview`): the blocks top to bottom, one line each on what the block is for.
- Write each section as a numbered BLOCK with a `layout` line (how it looks: full-width video, three cards in a row that stack on mobile, a two-column photo and text, a sticky button) and its copy in `elements`, labelled by the element it sits in (Headline, Subheadline, Body, Card 1, Quote, Button). build/landing_page.py renders each block as a labelled table. The booking and thank-you pages take the same shape.
- Where the page is being rebuilt or is hard to explain in words, also send a quick visual mockup (a single HTML page) built from the same copy, so the account lead and the page builder see the intended layout.

## Missing information
List required social proof, transformations, reviews, credentials, privacy policy and booking link as clearly labelled client-action placeholders. Never invent them. Do not include internal production checklists or direction notes in the client-facing sections.

Also open the document with a prominent, consolidated "Client to provide before this page can go live" section that lists every missing asset in one place (rating and client count, quotes, testimonials, before and after photos, credentials, booking link, privacy policy and unsubscribe). This makes it unmistakable that the client must supply these before the page can go live. Keep the per-section CLIENT ACTION placeholders as well, so each gap is marked both in the summary and where it belongs.
