"""
Command-line entry point for the Maxalding QA gate.

Usage:
    python -m validator.cli PATH [PATH ...] [--no-names] [--quiet]

Exits non-zero if any error-severity violation is found, so it can be wired as
a QA step and as a git pre-commit hook.
"""

from __future__ import annotations

import argparse
import sys

from .validate import validate_paths


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="maxalding-validate",
        description="Deterministic QA gate for Maxalding onboarding outputs.",
    )
    parser.add_argument("paths", nargs="+", help="Files or directories to scan.")
    parser.add_argument(
        "--no-names",
        action="store_true",
        help="Skip the filename naming-convention check.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Only print the summary line.",
    )
    parser.add_argument(
        "--skip-rules",
        default="",
        help=(
            "Comma-separated rule ids to waive, for example premium-framing for a "
            "low-ticket free-trial client that legitimately names a free offer."
        ),
    )
    args = parser.parse_args(argv)

    skip_rules = {r.strip() for r in args.skip_rules.split(",") if r.strip()}
    result = validate_paths(
        args.paths, check_names=not args.no_names, skip_rules=skip_rules
    )

    if not args.quiet:
        for v in result.errors:
            line = f"  ERROR  [{v.rule}] {v.message}\n         at {v.location}"
            if v.snippet:
                line += f'\n         near: "{v.snippet}"'
            print(line)
        for v in result.warnings:
            print(f"  WARN   [{v.rule}] {v.message}\n         at {v.location}")

    n_err = len(result.errors)
    n_warn = len(result.warnings)
    if result.ok:
        print(f"QA gate passed. 0 errors, {n_warn} warnings.")
        return 0
    print(f"QA gate FAILED. {n_err} errors, {n_warn} warnings.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
