from __future__ import annotations

from datetime import datetime, timezone

PREFIXES = {
    "Opportunities": "OPP",
    "Companies": "CO",
    "Scorecards": "SC",
    "Applications": "APP",
    "Interviews": "INT",
    "Documents": "DOC",
    "Outcomes": "OUT",
    "Evidence": "EVD",
    "Competencies": "CMP",
    "Coaching_Sessions": "COACH",
    "Decisions": "DEC",
    "Weekly_Reviews": "WK",
    "Quarterly_Reviews": "QTR",
    "Development_Experiments": "EXP",
    "Prompt_Lessons": "PL",
    "Feedback": "FB",
    "History": "EVT",
    "Career_Thesis": "TH",
    "Research_Principles": "RP",
}


def next_id(existing: list[str], sheet: str) -> str:
    prefix = PREFIXES[sheet]
    highest = 0
    for value in existing:
        if not isinstance(value, str) or not value.startswith(prefix + "-"):
            continue
        tail = value[len(prefix) + 1 :]
        if tail.isdigit():
            highest = max(highest, int(tail))
    return f"{prefix}-{highest + 1:04d}"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

