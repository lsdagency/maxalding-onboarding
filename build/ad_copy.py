"""
Standalone Meta Ad Copy XLSX generator.

For ad-copy requests that are NOT part of a full onboarding run (for example,
writing post copy for a batch of filmed videos). It reuses the AD COPY tab
builder from the Creative Plan so the output is byte-for-byte the same format
as the onboarding deliverable: Helvetica Neue, black header row, the
"# | CONCEPT | POST COPY | CHARS" layout, a shared HEADLINES block, one
DESCRIPTION, and live =LEN() formulas on every copy cell.

Single source of truth for the rules: skills/client-onboarding/references/
creative-plan-spec.md (Tab 3) and the meta-ad-copy skill.

Usage:
    python -m build.ad_copy <ad_copy_data>.json --out <dir>

Input JSON shape:
{
  "client_business_name": "FIT Republik",
  "campaign": "Winter Project",   # short campaign name, goes into the filename
  "ad_copy": {
    "concepts": [
      {"concept": "Concept name", "posts": ["p1", "p2", "p3", "p4", "p5"]},
      ...
    ],
    "headlines": ["h1", "h2", "h3", "h4", "h5"],
    "description": "Shared description"
  }
}
"""
from __future__ import annotations

import argparse
import json
import os

import openpyxl

from . import template as T
from .creative_plan import _build_ad_copy

POST_MAX = 125
HEADLINE_MAX = 40
DESCRIPTION_MAX = 25


def validate(data) -> list[str]:
    """Return a list of rule violations (empty means the data is clean)."""
    problems: list[str] = []
    ad = data.get("ad_copy", {})
    concepts = ad.get("concepts", [])
    if not concepts:
        problems.append("ad_copy.concepts is empty")
    for block in concepts:
        name = block.get("concept", "?")
        posts = block.get("posts", [])
        if len(posts) != 5:
            problems.append(f"concept '{name}': {len(posts)} post copies (need exactly 5)")
        for p in posts:
            if len(p) > POST_MAX:
                problems.append(f"post over {POST_MAX} ({len(p)}): {p}")
    headlines = ad.get("headlines", [])
    if len(headlines) != 5:
        problems.append(f"{len(headlines)} headlines (need exactly 5)")
    for h in headlines:
        if len(h) > HEADLINE_MAX:
            problems.append(f"headline over {HEADLINE_MAX} ({len(h)}): {h}")
    desc = ad.get("description", "")
    if not desc:
        problems.append("description is empty")
    if len(desc) > DESCRIPTION_MAX:
        problems.append(f"description over {DESCRIPTION_MAX} ({len(desc)}): {desc}")
    return problems


def build_ad_copy(data, out_dir) -> str:
    """Build a standalone Meta Ad Copy workbook and return the saved path."""
    wb = openpyxl.Workbook()
    default_sheet = wb.active  # the blank sheet openpyxl creates
    _build_ad_copy(wb, data)
    wb.remove(default_sheet)  # leave AD COPY as the only tab
    # Campaign-distinct filename (Feedback 2026-07-15, UBX): a standalone ad
    # copy file is always for a specific campaign, so carry its name.
    filename = T.deliverable_filename(
        data["client_business_name"], "Meta Ad Copy", campaign=data.get("campaign"))
    out_path = os.path.join(out_dir, filename)
    wb.save(out_path)
    return out_path


def main():
    ap = argparse.ArgumentParser(description="Build a standalone Meta Ad Copy XLSX.")
    ap.add_argument("data", help="Path to the ad copy data JSON.")
    ap.add_argument("--out", required=True, help="Output directory.")
    ap.add_argument("--skip-validate", action="store_true",
                    help="Skip the character-limit and structure checks.")
    args = ap.parse_args()

    with open(args.data) as f:
        data = json.load(f)

    if not args.skip_validate:
        problems = validate(data)
        if problems:
            print("Validation failed:")
            for p in problems:
                print("  -", p)
            raise SystemExit(1)

    os.makedirs(args.out, exist_ok=True)
    path = build_ad_copy(data, args.out)
    print("Saved:", path)


if __name__ == "__main__":
    main()
