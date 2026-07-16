"""
Build orchestrator: produce all five Maxalding deliverables from one data file,
then run the QA gate over the outputs.

Usage:
    python -m build.build_all CLIENT_DATA.json [--out OUT_DIR] [--workspace WS]

The Video Ad Scripts filename is resolved up front and written into the Creative
Plan SCRIPT column for the video rows (System Prompt sections 2 and 8), so the
tracker references the script file even though both are produced in one pass.
"""

from __future__ import annotations

import argparse
import json
import os
import sys

from . import template as T
from .creative_plan import build_creative_plan
from .video_ad_scripts import build_video_ad_scripts
from .vsl_script import build_vsl_script
from .landing_page import build_landing_page
from .crm_automation import build_crm_automation


_STATIC_TRACKER_ROWS = 5
_ADDRESSER_TAGS = ["(age)", "(role)", "(situation)"]


def _sync_video_hooks(data):
    """Single source of truth for video hooks. The Video Ad Script hook options
    ARE the hooks; mirror them into the Creative Tracker video HOOK cells so the
    tracker and the scripts can never show different hooks. Static rows are left
    untouched. The Audience Addresser keeps its age/role/situation labels."""
    concepts = data.get("scripts", {}).get("concepts", [])
    tracker = data.get("tracker", [])
    for j, concept in enumerate(concepts):
        idx = _STATIC_TRACKER_ROWS + j
        if idx >= len(tracker):
            break
        hooks = [h for h in concept.get("hooks", []) if h][:3]
        if not hooks:
            continue
        addresser = "addresser" in concept.get("name", "").lower()
        lines = []
        for k, hook in enumerate(hooks):
            if addresser and k < len(_ADDRESSER_TAGS):
                lines.append(f"Hook {k + 1} {_ADDRESSER_TAGS[k]}: {hook}")
            else:
                lines.append(f"Hook {k + 1}: {hook}")
        tracker[idx]["hook"] = "\n".join(lines)


def build_all(data, out_dir, workspace=None):
    os.makedirs(out_dir, exist_ok=True)

    # Resolve the Video Ad Scripts filename first so the Creative Plan SCRIPT
    # column can reference it on the video rows.
    client = data["client_business_name"]
    data.setdefault(
        "video_scripts_filename",
        T.deliverable_filename(client, "Video Ad Scripts", campaign=data.get("campaign")),
    )

    # Mirror the script hook options into the tracker video hook cells.
    _sync_video_hooks(data)

    outputs = {}
    outputs["Creative Plan"] = build_creative_plan(data, out_dir)
    outputs["Video Ad Scripts"] = build_video_ad_scripts(data, out_dir, workspace=workspace)
    outputs["VSL Script"] = build_vsl_script(data, out_dir, workspace=workspace)
    outputs["Landing Page Copy"] = build_landing_page(data, out_dir, workspace=workspace)
    outputs["CRM Automation"] = build_crm_automation(data, out_dir, workspace=workspace)
    return outputs


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Build all Maxalding deliverables.")
    parser.add_argument("data", help="Path to the client data JSON file.")
    parser.add_argument("--out", default=".", help="Output directory (default: cwd).")
    parser.add_argument("--workspace", default=None, help="Workspace folder for the logo.")
    parser.add_argument("--no-validate", action="store_true", help="Skip the QA gate.")
    args = parser.parse_args(argv)

    with open(args.data, "r", encoding="utf-8") as fh:
        data = json.load(fh)

    outputs = build_all(data, args.out, workspace=args.workspace)
    for name, path in outputs.items():
        print(f"  built {name}: {path}")

    if args.no_validate:
        return 0

    # Run the QA gate over the produced files.
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from validator.validate import validate_paths

    # Per-client waiver: a low-ticket free-trial client (premium_lead_magnet
    # false) may name a "free" offer in audience copy, which waives the
    # premium-framing rule. Default is True (premium framing enforced).
    skip_rules = set()
    if not data.get("premium_lead_magnet", True):
        skip_rules.add("premium-framing")
        print("  note: premium_lead_magnet is false, waiving premium-framing for this client")
    result = validate_paths(list(outputs.values()), skip_rules=skip_rules)
    if result.ok:
        print(f"QA gate passed. 0 errors, {len(result.warnings)} warnings.")
        return 0
    for v in result.errors:
        print(f"  ERROR [{v.rule}] {v.message} at {v.location}")
    print(f"QA gate FAILED. {len(result.errors)} errors.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
