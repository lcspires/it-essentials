# Performance Tests ou Benchmark Tests
# Tempo de execução, uso de memória, throughput

import subprocess
import pytest
import time
from pathlib import Path

dir_tests = Path(__file__).parent
dir_src = dir_tests.parent / 'src'
caminho_core_py = dir_src / 'core.py'


def executar_caso_teste(entrada):
    processo = subprocess.run(
        ['python', str(caminho_core_py)],
        input=entrada,
        text=True,
        capture_output=True,
        timeout=10  # Timeout para evitar travamentos
    )
    return processo.stdout.strip(), processo.stderr.strip(), processo.returncode


def test_performance_entrada_unica():
    """Testa performance de uma única execução"""
    entrada = "1000000 1"

    inicio = time.time()
    stdout, stderr, returncode = executar_caso_teste(entrada)
    tempo_execucao = time.time() - inicio

    assert returncode == 0
    assert stdout == "1000000.0"
    assert tempo_execucao < 0.1  # Máximo 100ms por execução


def test_performance_operacao_complexa():
    """Testa performance com operação mais complexa"""
    entrada = "999999 3"

    inicio = time.time()
    stdout, stderr, returncode = executar_caso_teste(entrada)
    tempo_execucao = time.time() - inicio

    assert returncode == 0
    assert stdout == "333333.0"
    assert tempo_execucao < 0.1  # Máximo 100ms

# Regression Tests (Testes de Regressão)
@pytest.mark.parametrize("entrada,esperado", [
    ("1000000 1", "1000000.0"),
    ("999999999 1", "999999999.0"),
    ("123456789 1", "123456789.0"),
    ("999999 3", "333333.0"),
    ("888888 4", "222222.0"),
])
def test_performance_varios_casos(entrada, esperado):
    """Testa performance com vários casos individuais"""
    inicio = time.time()
    stdout, stderr, returncode = executar_caso_teste(entrada)
    tempo_execucao = time.time() - inicio

    assert returncode == 0
    assert stdout == esperado
    assert tempo_execucao < 0.1  # Máximo 100ms por caso


def test_sistema_multiplas_entradas_em_lote():
    """Testa múltiplas entradas em um único processo"""
    # Cria um arquivo de entrada com múltiplos casos
    entradas_multiplas = """10 5
100 10
7 2
0 5
-12 3
999999 3"""

    inicio = time.time()
    stdout, stderr, returncode = executar_caso_teste(entradas_multiplas)
    tempo_total = time.time() - inicio

    assert returncode == 0
    # Verifica se todas as saídas estão presentes
    saidas = stdout.split('\n')
    assert len(saidas) == 6  # 6 entradas = 6 saídas
    assert tempo_total < 0.5  # Máximo 500ms para o lote


def test_stress_entradas_muito_grandes():
    """Testa com números no limite máximo"""
    # Valores próximos ao limite do int
    entradas_grandes = """2147483647 1
2147483646 2
1000000000 1000000000
999999999 333333333"""

    inicio = time.time()
    stdout, stderr, returncode = executar_caso_teste(entradas_grandes)
    tempo_total = time.time() - inicio

    assert returncode == 0
    assert tempo_total < 1.0  # Máximo 1 segundo para o lote


def test_nao_deve_travar():
    """Garante que o programa não entra em loop infinito"""
    # Testa com entrada válida mas que poderia causar problemas
    entrada = "1000000000 1"

    # Usa timeout no subprocess
    processo = subprocess.run(
        ['python', str(caminho_core_py)],
        input=entrada,
        text=True,
        capture_output=True,
        timeout=5  # 5 segundos de timeout
    )

    assert processo.returncode == 0
    assert processo.stdout.strip() == "1000000000.0"