# Unit Tests: rápidos e isolados.

import pytest
from src.core import divisao

@pytest.mark.parametrize("a,b,esperado", [
    (10, 5, 2.0),
    (0, 5, 0.0),
    (7, 2, 7/2),
    (-100, 10, -10),
])
def test_divisao(a, b, esperado):
    assert divisao(a, b) == esperado

@pytest.mark.parametrize("a,b", [
    (10, 0),
    (0, 0),
])
def test_divisaoporzero(a, b):
    with pytest.raises(ZeroDivisionError):
        divisao(a, b)