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