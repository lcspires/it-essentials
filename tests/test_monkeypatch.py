# Integration Tests: I/O Tests ou Input/Output Tests.
# Smoke Tests and Mock Tests (Testes com Mock Objects)

from io import StringIO
import sys
from src.core import main


def test_main_com_multiplas_entradas(monkeypatch, capsys):
    # Simula a entrada padrão com múltiplas linhas
    entrada_multilinha = """10 5
-100 10
0 2
10 0
10 abc"""

    # Monkeypatch do sys.stdin para simular múltiplas entradas
    monkeypatch.setattr('sys.stdin', StringIO(entrada_multilinha))

    # Executa a main uma única vez (ela processa todas as linhas)
    main()

    # Captura a saída completa
    captured = capsys.readouterr()

    # Verifica todas as saídas de uma vez
    saidas = captured.out.strip().split('\n')

    assert saidas == [
        "2.0",
        "-10.0",
        "0.0",
        "Erro: Divisão por zero não é permitida",
        "Erro: Entrada inválida"
    ]


def test_main_entrada_vazia(monkeypatch, capsys):
    # Testa com entrada vazia
    monkeypatch.setattr('sys.stdin', StringIO(""))

    main()

    captured = capsys.readouterr()
    assert captured.out.strip() == ""  # Nenhuma saída


def test_main_com_linhas_vazias(monkeypatch, capsys):
    # Testa com linhas vazias no meio
    entrada_com_vazios = """10 5

-100 10

0 2"""

    monkeypatch.setattr('sys.stdin', StringIO(entrada_com_vazios))

    main()

    captured = capsys.readouterr()
    saidas = captured.out.strip().split('\n')

    assert saidas == [
        "2.0",
        "-10.0",
        "0.0"
    ]