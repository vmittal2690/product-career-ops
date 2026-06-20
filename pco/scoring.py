from __future__ import annotations

from .config import ACTIVE_THRESHOLD, SCORE_DIMENSIONS
from .schema import Score


def parse_scores(raw: dict) -> list[Score]:
    result = []
    for key, label, maximum in SCORE_DIMENSIONS:
        item = raw.get(key)
        if item is None:
            raise ValueError(f"Missing score dimension: {key}")
        points = int(item["points"] if isinstance(item, dict) else item)
        score = Score(
            key=key,
            label=label,
            maximum=maximum,
            points=points,
            rationale=item.get("rationale", "") if isinstance(item, dict) else "",
            evidence=item.get("evidence", "") if isinstance(item, dict) else "",
            unknowns=item.get("unknowns", "") if isinstance(item, dict) else "",
        )
        score.validate()
        result.append(score)
    return result


def total(scores: list[Score]) -> int:
    return sum(item.points for item in scores)


def status_for_score(value: int) -> str:
    return "Active" if value >= ACTIVE_THRESHOLD else "Archived"


def recommendation_for_score(value: int) -> str:
    if value >= 90:
        return "Prioritize immediately"
    if value >= 80:
        return "Pursue"
    if value >= 70:
        return "Explore only with a specific strategic reason"
    return "Pass"

