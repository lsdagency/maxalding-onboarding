"""
Maxalding QA gate: a deterministic validator for onboarding outputs.

Public API:
    validate_paths(paths)          scan files or directories, return a Result
    validate_text(text, kind=...)  scan a single string (tests, eval harness)
    Result, Violation, Segment     data containers
"""

from .checks import Result, Violation, Segment
from .validate import validate_paths, validate_text, scan_file

__all__ = [
    "Result",
    "Violation",
    "Segment",
    "validate_paths",
    "validate_text",
    "scan_file",
]

__version__ = "0.9.0"
