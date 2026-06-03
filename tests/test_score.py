from qapitol.evals.score import Score


def test_passed_threshold_maximize() -> None:
    s = Score(
        score=0.8,
        name="coherence",
        label="coherent",
        kind="llm",
        direction="maximize",
    )
    assert s.passed_threshold(0.7)
    assert not s.passed_threshold(0.85)


def test_passed_threshold_low_score_fails_high_bar() -> None:
    s = Score(
        score=0.1,
        name="coherence",
        label="incoherent",
        kind="llm",
        direction="maximize",
    )
    assert not s.passed_threshold(0.7)
