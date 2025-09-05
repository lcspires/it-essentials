from src.math_utils import soma


def test_soma_positivos():
    assert soma(2, 3) == 5


def test_soma_negativos():
    assert soma(-1, -1) == -2
