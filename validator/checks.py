"""
Individual deterministic checks for the Maxalding QA gate.

Each check operates on Segment objects and returns a list of Violation objects.
A Segment carries its text, a human-readable location, and a kind that controls
which checks apply. Character checks apply to every kind. Word, phrase, Meta and
premium-framing checks skip rule-statement and code-definition segments, because
those legitimately quote the banned items in order to document them.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from . import rules


# ---------------------------------------------------------------------------
# Data containers
# ---------------------------------------------------------------------------
# Segment kinds:
#   content       general audience-facing copy (all checks apply)
#   rule_statement a cell/paragraph that documents a rule (char checks only)
#   code_string   a Python string literal from a build script (char checks only)
#   post_copy     an AD COPY post-copy cell (adds 125 char limit)
#   headline      an AD COPY headline cell (adds 40 char limit)
#   description   the AD COPY description cell (adds 25 char limit)
#   video_hook    a video hook cell (adds < 12 word limit)
#   static_hook   a static hook cell (adds 5 to 10 word limit)
#   header        a document header paragraph (adds no-date check)

CONTENT_KINDS = {
    "content",
    "post_copy",
    "headline",
    "description",
    "video_hook",
    "static_hook",
    "header",
}


@dataclass
class Segment:
    text: str
    location: str
    kind: str = "content"


@dataclass
class Violation:
    rule: str
    message: str
    location: str
    severity: str = "error"   # "error" or "warn"
    snippet: str = ""


@dataclass
class Result:
    violations: list = field(default_factory=list)

    @property
    def errors(self):
        return [v for v in self.violations if v.severity == "error"]

    @property
    def warnings(self):
        return [v for v in self.violations if v.severity == "warn"]

    @property
    def ok(self):
        return len(self.errors) == 0


def _snippet(text: str, idx: int, width: int = 40) -> str:
    start = max(0, idx - width)
    end = min(len(text), idx + width)
    return text[start:end].replace("\n", " ").strip()


def _word_count(text: str) -> int:
    return len([w for w in re.split(r"\s+", text.strip()) if w])


# ---------------------------------------------------------------------------
# Character checks (apply to every segment, including rule statements and code)
# ---------------------------------------------------------------------------
def check_characters(seg: Segment) -> list:
    out = []
    for label, literal in rules.BANNED_CHARACTERS.items():
        idx = seg.text.find(literal)
        if idx != -1:
            out.append(
                Violation(
                    rule="banned-character",
                    message=f"Contains a {label}",
                    location=seg.location,
                    snippet=_snippet(seg.text, idx),
                )
            )
    return out


# ---------------------------------------------------------------------------
# Word and phrase checks (content only)
# ---------------------------------------------------------------------------
def check_banned_words(seg: Segment) -> list:
    if seg.kind not in CONTENT_KINDS:
        return []
    out = []
    lowered = seg.text.lower()
    for word in rules.BANNED_WORDS:
        for m in re.finditer(r"\b" + re.escape(word) + r"\b", lowered):
            out.append(
                Violation(
                    rule="banned-word",
                    message=f'Banned word "{word}" used in a programme or plan sense',
                    location=seg.location,
                    snippet=_snippet(seg.text, m.start()),
                )
            )
            break  # one report per word per segment is enough
    return out


def check_banned_phrases(seg: Segment) -> list:
    if seg.kind not in CONTENT_KINDS:
        return []
    out = []
    lowered = seg.text.lower()
    for phrase in rules.BANNED_PHRASES:
        idx = lowered.find(phrase)
        if idx != -1:
            out.append(
                Violation(
                    rule="banned-phrase",
                    message=f'Banned phrase "{phrase}"',
                    location=seg.location,
                    snippet=_snippet(seg.text, idx),
                )
            )
    return out


def check_banned_formula(seg: Segment) -> list:
    if seg.kind not in CONTENT_KINDS:
        return []
    out = []
    for pat in rules.BANNED_FORMULA_PATTERNS:
        m = re.search(pat, seg.text, re.IGNORECASE)
        if m:
            out.append(
                Violation(
                    rule="banned-formula",
                    message='AI-tell "it is not a X problem, it is a Y problem" construction',
                    location=seg.location,
                    snippet=_snippet(seg.text, m.start()),
                )
            )
    return out


def check_positive_language(seg: Segment) -> list:
    if seg.kind not in CONTENT_KINDS:
        return []
    out = []
    for pat in rules.POSITIVE_LANGUAGE_PATTERNS:
        m = re.search(pat, seg.text, re.IGNORECASE)
        if m:
            out.append(
                Violation(
                    rule="positive-language",
                    message="Frames the problem as a personal failing (positive-language rule)",
                    location=seg.location,
                    snippet=_snippet(seg.text, m.start()),
                )
            )
    return out


# ---------------------------------------------------------------------------
# Meta compliance (content only)
# ---------------------------------------------------------------------------
def check_meta(seg: Segment) -> list:
    if seg.kind not in CONTENT_KINDS:
        return []
    out = []
    for pat in rules.META_WEIGHT_PATTERNS:
        m = re.search(pat, seg.text, re.IGNORECASE)
        if m:
            out.append(
                Violation(
                    rule="meta-weight-figure",
                    message="Specific weight figure (Meta personal-attributes risk)",
                    location=seg.location,
                    snippet=_snippet(seg.text, m.start()),
                )
            )
    lowered = seg.text.lower()
    for phrase in rules.META_BODY_PHRASES:
        idx = lowered.find(phrase)
        if idx != -1:
            out.append(
                Violation(
                    rule="meta-body-phrasing",
                    message=f'Body-attribute phrasing "{phrase}" (Meta personal-attributes risk)',
                    location=seg.location,
                    snippet=_snippet(seg.text, idx),
                )
            )
    for pat in rules.META_YOU_NEGATIVE_PATTERNS:
        m = re.search(pat, seg.text, re.IGNORECASE)
        if m:
            out.append(
                Violation(
                    rule="meta-you-negative",
                    message='"you" plus a negative physical trait (Meta personal-attributes risk)',
                    location=seg.location,
                    snippet=_snippet(seg.text, m.start()),
                )
            )
    return out


# ---------------------------------------------------------------------------
# Premium framing (content only)
# ---------------------------------------------------------------------------
def check_premium_framing(seg: Segment) -> list:
    if seg.kind not in CONTENT_KINDS:
        return []
    out = []
    for pat in rules.PREMIUM_FRAMING_BANNED:
        m = re.search(pat, seg.text, re.IGNORECASE)
        if m:
            out.append(
                Violation(
                    rule="premium-framing",
                    message="Discount language in audience-facing copy (premium-framing rule)",
                    location=seg.location,
                    snippet=_snippet(seg.text, m.start()),
                )
            )
    return out


# ---------------------------------------------------------------------------
# Length and word-count checks (kind-specific)
# ---------------------------------------------------------------------------
def check_lengths(seg: Segment) -> list:
    out = []
    limits = {
        "post_copy": (rules.POST_COPY_MAX, "post copy"),
        "headline": (rules.HEADLINE_MAX, "headline"),
        "description": (rules.DESCRIPTION_MAX, "description"),
    }
    if seg.kind in limits:
        limit, label = limits[seg.kind]
        n = len(seg.text)
        if n > limit:
            out.append(
                Violation(
                    rule="length-limit",
                    message=f"{label} is {n} characters, limit is {limit}",
                    location=seg.location,
                    snippet=seg.text[:60],
                )
            )
    return out


def check_hooks(seg: Segment) -> list:
    out = []
    if seg.kind == "video_hook":
        n = _word_count(seg.text)
        if n >= rules.VIDEO_HOOK_MAX_WORDS:
            out.append(
                Violation(
                    rule="hook-length",
                    message=f"video hook is {n} words, must be under {rules.VIDEO_HOOK_MAX_WORDS}",
                    location=seg.location,
                    snippet=seg.text[:60],
                )
            )
    elif seg.kind == "static_hook":
        n = _word_count(seg.text)
        if n < rules.STATIC_HOOK_MIN_WORDS or n > rules.STATIC_HOOK_MAX_WORDS:
            out.append(
                Violation(
                    rule="hook-length",
                    message=(
                        f"static hook is {n} words, must be "
                        f"{rules.STATIC_HOOK_MIN_WORDS} to {rules.STATIC_HOOK_MAX_WORDS}"
                    ),
                    location=seg.location,
                    snippet=seg.text[:60],
                )
            )
    return out


# ---------------------------------------------------------------------------
# No date in header (header segments only)
# ---------------------------------------------------------------------------
def check_no_date(seg: Segment) -> list:
    if seg.kind != "header":
        return []
    out = []
    for pat in rules.DATE_PATTERNS:
        m = re.search(pat, seg.text, re.IGNORECASE)
        if m:
            out.append(
                Violation(
                    rule="no-date-in-header",
                    message="Date or DATE label found in the document header",
                    location=seg.location,
                    snippet=_snippet(seg.text, m.start()),
                )
            )
    return out


# ---------------------------------------------------------------------------
# Filename naming convention (operates on a filename string)
# ---------------------------------------------------------------------------
def check_naming(filename: str) -> list:
    out = []
    m = re.match(rules.NAMING_REGEX, filename)
    if not m:
        out.append(
            Violation(
                rule="naming-convention",
                message=(
                    "Filename does not match MAXALDING - [Client] - [Deliverable].[ext] "
                    "with the approved deliverable names"
                ),
                location=filename,
            )
        )
        return out
    deliverable, ext = m.group(2), m.group(3)
    expected_ext = rules.DELIVERABLES.get(deliverable)
    if expected_ext and ext != expected_ext:
        out.append(
            Violation(
                rule="naming-convention",
                message=f'"{deliverable}" must be a .{expected_ext} file, found .{ext}',
                location=filename,
            )
        )
    return out


# ---------------------------------------------------------------------------
# Segment runner: applies the right checks based on kind
# ---------------------------------------------------------------------------
def check_post_copy_punctuation(seg: Segment) -> list:
    """Post copy should not end with a full stop; it reads unnatural in an ad.
    Ellipsis is handled by the banned-character check, so a trailing '..' is
    left for that check to flag."""
    if seg.kind != "post_copy":
        return []
    stripped = seg.text.rstrip()
    if stripped.endswith(".") and not stripped.endswith(".."):
        return [
            Violation(
                rule="post-copy-punctuation",
                message="post copy should not end with a full stop",
                location=seg.location,
                snippet=seg.text[-60:],
                severity="warn",
            )
        ]
    return []


SEGMENT_CHECKS = [
    check_characters,
    check_banned_words,
    check_banned_phrases,
    check_banned_formula,
    check_positive_language,
    check_meta,
    check_premium_framing,
    check_lengths,
    check_hooks,
    check_no_date,
    check_post_copy_punctuation,
]


def run_segment_checks(segments) -> list:
    violations = []
    for seg in segments:
        for check in SEGMENT_CHECKS:
            violations.extend(check(seg))
    return violations


def is_rule_statement(text: str) -> bool:
    lowered = text.lower()
    return any(marker in lowered for marker in rules.RULE_STATEMENT_MARKERS)
