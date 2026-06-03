from qapitol.evals.cli import doctor


def test_doctor_runs() -> None:
    assert doctor() == 0
