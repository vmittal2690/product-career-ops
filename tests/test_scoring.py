from pco.scoring import parse_scores, recommendation_for_score, status_for_score, total


def full_scores(value_by_max=False):
    values = {}
    dimensions = [
        ("mandate_authority", 20),
        ("target_alignment", 15),
        ("domain_fit", 15),
        ("leadership_scope", 15),
        ("evidence_match", 10),
        ("career_growth", 10),
        ("product_quality", 5),
        ("commercial_upside", 5),
        ("practical_fit", 5),
    ]
    for key, maximum in dimensions:
        values[key] = {"points": maximum if value_by_max else 0}
    return values


def test_score_totals_to_100():
    assert total(parse_scores(full_scores(True))) == 100


def test_active_threshold():
    assert status_for_score(80) == "Active"
    assert status_for_score(79) == "Archived"


def test_recommendation_tiers():
    assert recommendation_for_score(93) == "Prioritize immediately"
    assert recommendation_for_score(85) == "Pursue"


def test_rejects_points_above_dimension_max():
    raw = full_scores()
    raw["practical_fit"] = {"points": 6}
    try:
        parse_scores(raw)
    except ValueError as exc:
        assert "outside" in str(exc)
    else:
        raise AssertionError("Expected validation error")

