"""
Deterministic rule constants for the Maxalding QA gate.

Every banned character is built here with chr() rather than pasted as a literal
glyph, so this module is itself clean ASCII and can be scanned by its own
validator without self-flagging. Do not paste raw em dashes, en dashes or
ellipsis characters into this file.

The rules below are derived from:
  - MAXALDING - Client Onboarding Agent - System Prompt.md (source of truth)
  - MAXALDING - Onboarding Feedback Log.md (live corrections)
and are mirrored in rules/rules.yaml for the agents to load.
"""

# ---------------------------------------------------------------------------
# Banned characters (System Prompt section 3, Feedback rounds 1, 8, 11)
# ---------------------------------------------------------------------------
EM_DASH = chr(0x2014)        # em dash
EN_DASH = chr(0x2013)        # en dash
ELLIPSIS_CHAR = chr(0x2026)  # single-glyph ellipsis
EXCLAMATION = "!"
ELLIPSIS_DOTS = "..."        # three-period ellipsis used for effect

# label -> literal to search for
BANNED_CHARACTERS = {
    "em dash": EM_DASH,
    "en dash": EN_DASH,
    "ellipsis character": ELLIPSIS_CHAR,
    "exclamation mark": EXCLAMATION,
    "ellipsis (three periods)": ELLIPSIS_DOTS,
}

# ---------------------------------------------------------------------------
# Banned words used in the programme/plan sense (System Prompt section 3)
# Whole-word, case-insensitive. Allowed only inside explicit rule-statement
# cells (for example the BANNED IN COPY row), which the scanner exempts.
# ---------------------------------------------------------------------------
BANNED_WORDS = [
    "structure",
    "structures",
    "framework",
    "frameworks",
]

# ---------------------------------------------------------------------------
# Banned phrases (System Prompt section 3). Case-insensitive substring match.
# ---------------------------------------------------------------------------
BANNED_PHRASES = [
    "here's the truth",
    "heres the truth",
    "the reality is",
    "in today's world",
    "in todays world",
    "at the end of the day",
    "with that being said",
    "in other words",
    "as you can see",
    "game changer",
    "next level",
    "proven system",
    "done for you",
    "unlock your potential",
    "transform your life",
    "amazing",
    "incredible",
    "powerful",
    "effortless",
    "world class",
    "this means that",
    "it's important to note",
    "its important to note",
    "in summary",
    "hey guys",
    "so today",
    "let's dive in",
    "lets dive in",
]

# Banned AI-tell formula: "It is not a [X] problem, it is a [Y] problem"
# and close variants. (System Prompt section 3.)
BANNED_FORMULA_PATTERNS = [
    r"it'?s not a[n]?\s+\w+\s+problem,?\s+it'?s a[n]?\s+\w+\s+problem",
    r"it is not a[n]?\s+\w+\s+problem,?\s+it is a[n]?\s+\w+\s+problem",
    r"not a[n]?\s+\w+\s+problem[.,]?\s+(it'?s|it is)\s+a[n]?\s+\w+\s+problem",
]

# ---------------------------------------------------------------------------
# Positive-language rule (System Prompt section 3, Feedback round 4)
# Negative self-framing that puts a failing on the person, even when negated.
# ---------------------------------------------------------------------------
POSITIVE_LANGUAGE_PATTERNS = [
    r"you'?re not lazy",
    r"you are not lazy",
    r"the gym did ?n'?t fail you",
    r"the gym did not fail you",
    r"you have ?n'?t been consistent",
    r"you have not been consistent",
    r"you'?ve not been consistent",
    r"stop making excuses",
    r"you know you should",
]

# ---------------------------------------------------------------------------
# Meta advertising compliance (System Prompt section 4, Feedback 2026-06-18)
# ---------------------------------------------------------------------------
# Specific weight figures anywhere (kg, lbs, pounds), single value or range.
# The range separator class is built from the dash constants to stay clean.
_RANGE = "(?:to|-|" + EN_DASH + "|" + EM_DASH + ")"
META_WEIGHT_PATTERNS = [
    r"\b\d+\s*" + _RANGE + r"\s*\d+\s*kg\b",
    r"\b\d+(?:\.\d+)?\s*kg\b",
    r"\b\d+\s*" + _RANGE + r"\s*\d+\s*lbs?\b",
    r"\b\d+(?:\.\d+)?\s*lbs?\b",
    r"\b\d+\s*pounds\b",
]

# Body-attribute and body-shaming phrasing that asserts the viewer's body,
# weight or health. Case-insensitive substring match.
META_BODY_PHRASES = [
    "feel confident in your body",
    "confident in your body again",
    "problem areas",
    "belly fat",
    "beach body",
    "hate what you see in the mirror",
    "ashamed",
    "embarrassed",
    "disgusted",
    "lose weight",
    "are you overweight",
    "your body fat",
    "tone up those",
    "get rid of your",
]

# "you" plus a negative physical trait (a representative, extensible set).
META_YOU_NEGATIVE_PATTERNS = [
    r"\byou'?re\s+(?:over\s?weight|fat|unfit|out of shape)\b",
    r"\byou are\s+(?:over\s?weight|fat|unfit|out of shape)\b",
    r"\byour\s+(?:belly|gut|love handles)\b",
]

# ---------------------------------------------------------------------------
# Premium framing of the lead magnet (System Prompt section 5, Feedback 06-18)
# Discount language banned in audience-facing copy.
# ---------------------------------------------------------------------------
PREMIUM_FRAMING_BANNED = [
    r"\bfree\b",
    r"\bno cost\b",
    r"\bno pressure\b",
    r"\bcosts nothing\b",
    r"\bno obligation\b",
    r"\bfor free\b",
    r"\b100% free\b",
    r"\bzero cost\b",
]

# ---------------------------------------------------------------------------
# Length limits (System Prompt section 8, AD COPY tab)
# ---------------------------------------------------------------------------
POST_COPY_MAX = 125
HEADLINE_MAX = 40
DESCRIPTION_MAX = 25

# Hook word-count limits (System Prompt section 8; Feedback 2026-07-07 UBX).
# A video hook is a SPOKEN opening line and may be a full sentence or two (per
# the ad-hooks skill), so it is capped generously, not clipped to a short
# fragment. A static hook is an on-screen overlay and stays short.
VIDEO_HOOK_MAX_WORDS = 25        # a spoken hook can be a sentence or two
STATIC_HOOK_MIN_WORDS = 5        # 5 to 10 words
STATIC_HOOK_MAX_WORDS = 10

# ---------------------------------------------------------------------------
# Naming convention (System Prompt section 6, Feedback 2026-06-18)
# Pattern: MAXALDING - [Client Business Name] - [Deliverable].[ext]
# ---------------------------------------------------------------------------
DELIVERABLES = {
    "Creative Plan": "xlsx",
    "Meta Ad Copy": "xlsx",
    "Meta Lead Form Copy": "xlsx",
    "Meta Ad & Lead Form Copy": "xlsx",
    "Video Ad Scripts": "docx",
    "VSL Script": "docx",
    "Landing Page Copy": "docx",
    "CRM Automation": "docx",
}
NAMING_PREFIX = "MAXALDING - "
# Group 1 = client business name, group 2 = deliverable, group 3 = extension
NAMING_REGEX = (
    r"^MAXALDING - (.+) - "
    r"(Creative Plan|Meta Ad Copy|Meta Lead Form Copy|Meta Ad & Lead Form Copy"
    r"|Video Ad Scripts|VSL Script|Landing Page Copy|CRM Automation)"
    r"\.(xlsx|docx)$"
)

# ---------------------------------------------------------------------------
# No date in document header (System Prompt sections 9 to 12, Feedback 06-18)
# Header carries CLIENT, CAMPAIGN, PREPARED BY only. Scan the header region.
# ---------------------------------------------------------------------------
HEADER_SCAN_PARAGRAPHS = 12  # first N paragraphs treated as the header region
DATE_PATTERNS = [
    r"\bdate\s*:",                                   # an explicit DATE: label
    r"\b\d{1,2}[/\-.]\d{1,2}[/\-.]\d{2,4}\b",        # 19/06/2026 etc.
    r"\b\d{4}[/\-.]\d{1,2}[/\-.]\d{1,2}\b",          # 2026-06-19 etc.
    r"\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{1,2},?\s+\d{4}\b",
    r"\b\d{1,2}\s+(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{4}\b",
]

# ---------------------------------------------------------------------------
# Markers that identify a rule-statement cell or paragraph. Word, premium and
# Meta checks are skipped on these (they document the bans by quoting them),
# but character checks (dashes, exclamation, ellipsis) still apply.
# ---------------------------------------------------------------------------
RULE_STATEMENT_MARKERS = [
    "banned in copy",
    "words to avoid",
    "do not use",
    "meta compliance",
    "positive language",
    "never use",
    "avoid:",
]

# SMS limits (System Prompt section 12)
SMS_PREFERRED_MAX = 160
SMS_HARD_MAX = 320
