# HANDS-ON

Master the basics.

```text
HANDS-ON/
├── src/
│   └── __init__.py
│   └── core.py
├── tests/
│   └── __init__.py
│   └── test_monkeypatch.py
│   └── test_performance.py
│   └── test_sistemico.py
│   └── test_unitario.py
├── .pre-commit-config.yaml
├── README.md
├── poetry.lock
└── pyproject.toml
```

**Tools**

isort (isort .)

```bash
isort src/core.py

isort --check-only --diff src/core.py
# Para verificar sem organizar os imports.
```

black (black .)

```bash
black src/core.py

black --check --diff src/core.py
# Para verificar sem formatar o código.
```

ruff (ruff format .)

```bash
ruff format src/core.py

ruff format --check src/core.py
# Para verificar sem formatar o código (complementar ao black).
```

ruff (ruff check --fix .)

```bash
ruff check --fix src/core.py

ruff check src/core.py
# Para verificar sem auto-corrigir os erros (linting).
```

mypy (mypy .)

```bash
mypy src/core.py

mypy --strict src/core.py
# Verifica os tipos de dados com configurações específicas.
```

pydocstyle (pydocstyle .)

```bash
pydocstyle src/core.py

pydocstyle --convention=google src/core.py
# Verifica a documentação com configurações específicas (docstring).
```

pytest (pytest -v)

```bash
pytest tests/test_unitario.py -v

pytest tests/test_unitario.py::test_divisaoporzero -v
# Para testar uma função específica de um dado módulo.
```

---

## Código Sujismundo

```python
"""Módulo principal para divisão de números.  


esta linha tem espaços extras  




e esta também  





"""

import os, sys, math  # imports desorganizados
from typing import Any  

def divisao(a, b):  # sem type hints
    """Divide dois números.  
    
    Args:  
        a: Numerador  
        b: Denominador  
        
    Returns:  
        Resultado da divisão como float  
        
    Raises:  
        ZeroDivisionError: Se o denominador for zero  
    """  
    if b == 0:  
        raise ZeroDivisionError("Denominador não pode ser zero")  
    if a == 0:  
        return 0.0  
    resultado = a / b
    return resultado


def  main (  )  :  # espaços estranhos
    """Função principal que processa entrada e imprime resultado."""  
    data = sys.stdin.read().splitlines(  )

    for  line  in  data  :  # mais espaços
        line = line.strip(  )
        if not line:  
            continue  

        try:  
            x, y = map(int, line.split(  ))  
            resultado = divisao(x, y)  
            print(f"{resultado}")  
        except ZeroDivisionError:  
            print("Erro: Divisão por zero não é permitida")  
        except ValueError:  
            print("Erro: Entrada inválida")  
        except Exception as e:  
            print(f"Erro inesperado: {e}")  

def funcao_nao_usada():  # função nunca usada
    return "inútil"

variavel_global = 42  # variável global não usada

class ClasseInutil:  # classe nunca usada
    def __init__(self):
        self.nada = "nada"

if __name__ == "__main__":  
    main(  )  # espaços extras
    print("fim")  # print desnecessário

```

---

## Backup

```python
"""Módulo principal para divisão de números."""

def divisao(a: int, b: int) -> float:
    """Divide dois números.

    Args:
        a: Numerador
        b: Denominador

    Returns:
        Resultado da divisão como float

    Raises:
        ZeroDivisionError: Se o denominador for zero
    """
    if b == 0:
        raise ZeroDivisionError("Denominador não pode ser zero")
    if a == 0:
        return 0.0
    return a / b


def main() -> None:
    """Função principal que processa entrada e imprime resultado."""
    import sys

    data = sys.stdin.read().splitlines()

    for line in data:
        line = line.strip()
        if not line:
            continue

        try:
            x, y = map(int, line.split())
            resultado = divisao(x, y)
            print(f"{resultado}")
        except ZeroDivisionError:
            print("Erro: Divisão por zero não é permitida")
        except ValueError:
            print("Erro: Entrada inválida")
        except Exception as e:
            print(f"Erro inesperado: {e}")


if __name__ == "__main__":
    main()
```