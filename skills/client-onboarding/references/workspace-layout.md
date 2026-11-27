# Workspace layout

Every client lives in `workspace/clients/<Client>/` with the same folders. Every phase reads from and writes to these places only. The package itself stays read-only.

```
clients/<Client>/
  CLIENT.md            index: contacts, report recipient, dashboard slug, ad account ID, campaigns, memory files
  memory/              audience.md, brand.md, marketing.md, kpis.md, onboarding.md (+ profile.md,
                       performance-learnings.md and any client-specific extras)
  onboarding/          onboarding document, call transcript, stage-2-gate-decisions.md
  research/            instagram/  website/  competitors/  ads-library/
  brand-assets/        logos and photos the client sends (only when they exist)
  campaigns/<Mon-DD-slug-campaign>/
      ideation/        creative pack, Creative Plan, scripts, CRM, landing page or lead form, data JSON
      production/      statics/, edits/, edit-work/, finals/, feedback-rounds.md
  performance/         reviews/ (audits, quarterly reviews); weekly Meta data and the ad scorecard
  _build/              one-off build scripts and data files not tied to one campaign
  _archive/            superseded drafts, older memory copies, old versions, tool logs
```

## Rules
- **Memory is the client folder.** At the start of every client session read `CLIENT.md` and every file in `memory/`. Write memory updates there. Nothing about a client lives only in the assistant's own memory.
- **One folder per campaign** under `campaigns/`, named `Mon-DD-descriptor-campaign` (for example `Aug-01-anniversary-campaign`). A new campaign always gets a new folder. Deliverables go in its `ideation/`, finished creative in its `production/`.
- **Nothing working-only at the client root.** Drafts that are superseded go to `_archive/`, keeping only the latest beside the campaign. Build scripts and data files go with their campaign's `ideation/`, or `_build/` if they span campaigns. Tool logs (`.err`, `.log`) go to `_archive/logs/`.
- **Client-wide reference never sits in a campaign folder.** Research is client-wide (`research/`), source documents and gate decisions are onboarding (`onboarding/`), audits and reviews are performance (`performance/reviews/`).
- Update `CLIENT.md` whenever a campaign folder is added or a contact, slug or ad account ID becomes known.
- Agency-wide files (logo, feedback log, system prompt, templates) live in `workspace/Maxalding/`, which is also the build `--workspace` path.
