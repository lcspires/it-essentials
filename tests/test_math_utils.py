from src.math_utils import soma, subtracao


def test_soma() -> None:
    assert soma(2, 3) == 5
    assert soma(-1, 1) == 0


def test_subtracao() -> None:
    assert subtracao(5, 2) == 3
    assert subtracao(0, 3) == -3
