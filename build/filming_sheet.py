"""
Filming Sheet: the client-facing shoot doc for a SMALL ask, a handful of
takes rather than a full concept batch (the canonical case is a hook test:
five new openings and a fresh CTA against a winning ad's reused body).

The full Video Ad Scripts document earns its structure when every concept
carries its own body and directions. When the ask is six short takes, that
structure buries the ask (Feedback 2026-09-18, Fisica: Liam asked for the
hook-test doc to be radically simpler for the client). This sheet is the
simple form: what we need, how to film it, then the takes, one line each.

Editor instructions never go on this sheet. They belong in the designer
ticket, this doc is for the person standing in front of the camera.

Usage:
    python -m build.filming_sheet CLIENT_DATA.json --out OUT_DIR [--workspace WS]

Data shape (filming_sheet key):
    {
      "client_business_name": "Fisica",
      "campaign": "Incentive Hook Test",
      "prepared_by": "Maxalding Agency",
      "filming_sheet": {
        "what": ["short paragraph lines on what we need and why"],
        "how": ["dashed bullet lines on how to film every take"],
        "takes": [
          {"label": "Take 1 of 6", "note": "optional short italic note", "line": "the spoken line"}
        ],
        "close": "optional final line (upload folder reminder etc.)"
      }
    }
"""

from __future__ import annotations

import argparse
import json
import os

from . import template as T


def build_filming_sheet(data, out_dir, workspace=None):
    sheet = data["filming_sheet"]
    doc = T.new_document()
    T.add_header_block(
        doc,
        data["client_business_name"],
        data.get("campaign", ""),
        data.get("prepared_by", "Maxalding Agency"),
        workspace=workspace,
    )

    T.add_subheading(doc, "WHAT WE NEED FROM YOU")
    for line in sheet.get("what", []):
        T.add_body(doc, line)

    T.add_subheading(doc, "HOW TO FILM EVERY TAKE")
    for line in sheet.get("how", []):
        T.add_body(doc, line)

    for take in sheet.get("takes", []):
        T.add_subheading(doc, take["label"].upper())
        if take.get("note"):
            T.add_direction(doc, take["note"])
        T.add_script_line(doc, take["line"])

    if sheet.get("close"):
        T.add_divider(doc)
        T.add_body(doc, sheet["close"])

    filename = T.deliverable_filename(
        data["client_business_name"], "Filming Sheet", campaign=data.get("campaign")
    )
    out_path = os.path.join(out_dir, filename)
    doc.save(out_path)
    return out_path


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Build a Maxalding Filming Sheet.")
    parser.add_argument("data", help="Path to the client data JSON file.")
    parser.add_argument("--out", default=".", help="Output directory (default: cwd).")
    parser.add_argument("--workspace", default=None, help="Workspace folder for the logo.")
    args = parser.parse_args(argv)

    with open(args.data, "r", encoding="utf-8") as fh:
        data = json.load(fh)

    path = build_filming_sheet(data, args.out, workspace=args.workspace)
    print(f"Saved: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
