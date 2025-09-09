# System Tests ou End-to-End Tests (E2E).

import subprocess
import pytest
from pathlib import Path

dir_tests = Path(__file__).parent
dir_src = dir_tests.parent / 'src'
caminho_core_py = dir_src / 'core.py'

def executar_caso_teste(entrada):
    processo = subprocess.run(
        ['python', str(caminho_core_py)],
        input=entrada,
        text=True,
        capture_output=True
    )
    return processo.stdout.strip()

@pytest.mark.parametrize("entrada,esperado", [
    ("10 5", "2.0"),
    ("0 5", "0.0"),
    ("100 25", "4.0"),
    ("-10 2", "-5.0"),
])
def test_casos_competicao(entrada, esperado):
    resultado = executar_caso_teste(entrada)
    assert resultado == esperado