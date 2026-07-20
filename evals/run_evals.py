"""
Regression evals for the Maxalding onboarding plugin.

Two layers:
  1. Rule evals: known-bad strings MUST be caught with the right rule id, and
     known-good strings MUST pass. This locks the validator behaviour so the
     prompt and rules can change without silently regressing.
  2. Build eval: build every deliverable from evals/cases/sample_client.json,
     then run the QA gate over the outputs and assert zero errors. Skipped with
     a clear message if openpyxl / python-docx are not installed.

Run:
    python -m evals.run_evals
Exit code is non-zero if any eval fails.
"""

from __future__ import annotations

import json
import os
import sys
import tempfile

# Make the package importable when run from the repo root.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from validator import validate_text, validate_paths  # noqa: E402

DASH = chr(0x2014)
ELLIPSIS = chr(0x2026)

# (description, text, kind, expected_rule_id)
BAD_CASES = [
    ("em dash", "Strength" + DASH + "that lasts", "content", "banned-character"),
    ("exclamation", "Book now!", "content", "banned-character"),
    ("ellipsis glyph", "Wait for it" + ELLIPSIS, "content", "banned-character"),
    ("ellipsis dots", "Wait for it...", "content", "banned-character"),
    ("banned word structure", "Our structure keeps you on track", "content", "banned-word"),
    ("banned word framework", "A framework for busy people", "content", "banned-word"),
    ("banned phrase", "Here's the truth about training", "content", "banned-phrase"),
    ("ai formula", "It is not a time problem, it is a focus problem", "content", "banned-formula"),
    ("positive language", "You are not lazy, you just need a plan", "content", "positive-language"),
    ("meta weight kg", "Lose 5 to 10kg for good", "content", "meta-weight-figure"),
    ("meta body phrasing", "Feel confident in your body again", "content", "meta-body-phrasing"),
    ("premium framing free", "Book your free consultation today", "content", "premium-framing"),
    ("post copy too long", "x" * 130, "post_copy", "length-limit"),
    ("headline too long", "x" * 45, "headline", "length-limit"),
    ("description too long", "x" * 30, "description", "length-limit"),
    ("video hook too long", "Hook 1: this spoken video hook is written to run well beyond twenty five words on purpose so the length check still fires for an overlong opening line today", "video_hook", "hook-length"),
    ("static hook too short", "too short", "static_hook", "hook-length"),
    ("date in header", "DATE: 19/06/2026", "header", "no-date-in-header"),
    ("unlabelled video hook", "You start strong then a big week", "video_hook", "hook-label"),
    ("unlabelled static hook", "Home by six and too cooked", "static_hook", "hook-label"),
    ("tracker date stamped", "today", "tracker_date", "tracker-date-blank"),
]

# (description, text, kind) that must produce zero violations
GOOD_CASES = [
    ("clean content", "Strength that fits the life you already lead", "content"),
    ("structure exempt in rule cell", "Avoid the words structure and framework", "rule_statement"),
    ("clean post copy", "A plan built around your week, so progress finally holds.", "post_copy"),
    ("clean headline", "Strength built around your week", "headline"),
    ("clean description", "Strength that lasts", "description"),
    ("clean video hook", "Hook 1: Training keeps falling off your week", "video_hook"),
    ("clean static hook", "Hook 1: Strength that fits a packed week", "static_hook"),
    ("clean header", "CLIENT: Northside Strength Co", "header"),
]


def run_rule_evals():
    failures = []
    for desc, text, kind, expected in BAD_CASES:
        result = validate_text(text, kind=kind)
        rules_hit = {v.rule for v in result.violations}
        if expected not in rules_hit:
            failures.append(f"BAD  [{desc}] expected '{expected}', got {sorted(rules_hit) or 'none'}")
    for desc, text, kind in GOOD_CASES:
        result = validate_text(text, kind=kind)
        if not result.ok:
            hit = [(v.rule, v.message) for v in result.errors]
            failures.append(f"GOOD [{desc}] expected clean, got {hit}")
    return failures


def run_build_eval():
    try:
        import openpyxl  # noqa: F401
        import docx  # noqa: F401
    except Exception as exc:
        print(f"  build eval SKIPPED (missing dependency: {exc})")
        return []

    from build.build_all import build_all

    case_path = os.path.join(ROOT, "evals", "cases", "sample_client.json")
    with open(case_path, "r", encoding="utf-8") as fh:
        data = json.load(fh)

    failures = []
    with tempfile.TemporaryDirectory() as out_dir:
        outputs = build_all(data, out_dir, workspace=out_dir)  # no logo present, fine
        result = validate_paths(list(outputs.values()))
        if not result.ok:
            for v in result.errors:
                failures.append(f"BUILD [{v.rule}] {v.message} at {v.location}")
    return failures


def run_version_eval():
    """The plugin has two version strings (plugin.json and rules/rules.yaml).
    They drifted once (rules.yaml sat on 0.9.0 until 0.13.1); this locks them
    together so a bump cannot miss one."""
    try:
        import yaml
    except Exception as exc:
        print(f"  version eval SKIPPED (missing dependency: {exc})")
        return []
    with open(os.path.join(ROOT, ".claude-plugin", "plugin.json"), encoding="utf-8") as fh:
        plugin_version = json.load(fh)["version"]
    with open(os.path.join(ROOT, "rules", "rules.yaml"), encoding="utf-8") as fh:
        rules_version = yaml.safe_load(fh).get("version")
    if plugin_version != rules_version:
        return [
            f"VERSION plugin.json is {plugin_version} but rules/rules.yaml is "
            f"{rules_version}; bump both together"
        ]
    return []


def main():
    print("Running rule evals...")
    failures = run_rule_evals()
    print("Running build eval...")
    failures += run_build_eval()
    print("Running version eval...")
    failures += run_version_eval()

    if failures:
        print(f"\n{len(failures)} eval failure(s):")
        for f in failures:
            print(f"  {f}")
        return 1
    print("\nAll evals passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
