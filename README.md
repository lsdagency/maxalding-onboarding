# Maxalding Onboarding

A Claude Code plugin that automates Maxalding Agency's fitness client onboarding. It takes a new client's onboarding documents and produces a complete, ready-to-use campaign asset set: a Creative Plan spreadsheet and four campaign documents, every output looking and reading like it came from the same agency on the same campaign.

Version 0.9.0.

## What it does

An orchestrator agent runs the four-stage workflow and the approval gates. Specialist subagents own one craft each. A separate compliance and QA reviewer holds the final line, and a deterministic validator makes the house style and Meta compliance rules code, not vibes.

- onboarding-orchestrator: owns the workflow, the hard input gate, the Stage 2 confirm step and the QA gate.
- intake-research: reads everything, extracts the five categories, defines the campaign spine.
- creative-plan: builds the Creative Plan XLSX.
- scriptwriting: Video Ad Scripts and the VSL Script.
- conversion-copy: the Landing Page.
- lifecycle-crm: the CRM email and SMS copy.
- compliance-qa: runs the validator and a Meta policy read before anything is delivered.

## Read-only package, writable workspace

The package is read-only at runtime. All writable, per-agency and per-client state lives OUTSIDE the package, in a workspace folder:

- Maxalding Logo.png (inserted at the top of every document)
- the Onboarding Feedback Log (the live source of truth, read at the start of every session, appended to at the end)
- per-client brand kits
- the generated client outputs

Point the plugin at the workspace with the MAXALDING_WORKSPACE environment variable. If it is not set, the default is ./maxalding-workspace under the current directory.

```
export MAXALDING_WORKSPACE="/path/to/your/agency workspace"
```

A suggested workspace layout:

```
maxalding-workspace/
  Maxalding Logo.png
  MAXALDING - Onboarding Feedback Log.md
  brand-kits/
    <client>/   (colours, fonts, proof, approved testimonials)
  clients/
    <client>/   (the five deliverables land here)
```

Nothing writable is ever committed into this repo. The .gitignore guards against accidental commits of the logo, the feedback log and generated .xlsx or .docx files.

## Install

```
pip install -r requirements.txt
```

As a Claude Code plugin, load the repo as a plugin and the agents and the client-onboarding skill become available. Trigger it with "onboard new client" or by uploading a Brand Campaign Document or Creative Strategy Brief.

## Build the deliverables

The agents assemble a structured data dict (see evals/cases/sample_client.json for the shape) and call the build module. To build all five from a data file:

```
python -m build.build_all "client-data.json" --out "/path/to/workspace/clients/<client>" --workspace "$MAXALDING_WORKSPACE"
```

One shared template module (build/template.py) defines the font (Helvetica Neue on every run), the no-date header, the logo insertion and all styling, so a brand change is a single edit. The generators implement every formatting and content rule in the System Prompt: the Creative Plan XLSX (three tabs, dropdowns, live formulas, freeze panes) and the four .docx documents.

Upload the Creative Plan to Google Drive manually; a Drive MCP cannot write Sheets.

## The QA gate (the validator)

The validator is the deterministic quality gate. It scans every output and every build-script string for:

- em dashes, en dashes, exclamation marks and ellipses (zero tolerance, everywhere)
- banned words (structure or framework as nouns) outside rule-statement cells
- Meta risk patterns: specific weight figures, body-attribute phrasing, "you" plus a negative trait
- length limits: post copy 125, headlines 40, description 25, and hook word counts
- the naming convention and the SCRIPT-column reference
- a date in any document header
- discount language in audience-facing copy (the premium-framing check)

Run it directly:

```
python -m validator.cli "/path/to/output dir"
```

It exits non-zero on any error, so it works as a QA step and as a git pre-commit hook.

## Pre-commit hook

Install the QA gate as a git pre-commit hook so a rule violation cannot be committed:

```
scripts/install-hooks.sh
```

The hook scans the in-repo source for banned characters and runs the evals.

## Rules and evals

- rules/rules.yaml is the machine-readable ruleset derived from the feedback log, with provenance on every rule. The agents load it; validator/rules.py mirrors it for enforcement.
- evals/ holds a small regression set. Run it after any prompt or rule change:

```
python -m evals.run_evals
```

The evals check that known-bad copy is caught with the right rule and that the sample client builds clean through the QA gate.

## Repository layout

```
.claude-plugin/plugin.json   plugin manifest
agents/                      orchestrator and six specialists
skills/client-onboarding/    the user-facing skill and reference files
build/                       Python build module (template + 5 generators)
validator/                   deterministic QA gate
rules/rules.yaml             machine-readable rules
evals/                       regression eval set
hooks/pre-commit             QA gate as a git hook
scripts/install-hooks.sh     hook installer
```

## Provenance

Behaviour is governed by the Maxalding Client Onboarding Agent System Prompt (the source of truth) and the Onboarding Feedback Log (live corrections). No rule in the System Prompt is changed here; it is implemented faithfully.
