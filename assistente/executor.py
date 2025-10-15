# assistente/executor.py

"""Módulo executor que gerencia a execução, captura exceções e repassa o retorno."""

import time
from typing import Callable, Any

from interface.menu_de_erro import exibir_menu_de_falha
from uteis.cores import VERDE, VERMELHO, CIANO, RESET
from assistente.excecoes import AutomacaoAbortadaPeloUsuario

def executar_acao_assistida(
    funcao_acao: Callable[..., Any],
    nome_acao: str = None
) -> Any:
    """
    Executa uma ação, captura exceções e, em caso de sucesso, repassa o retorno.
    """

    # --- MUDANÇA 2: LÓGICA PARA LER A DOCSTRING ---
    # Se um nome_acao não foi fornecido explicitamente...
    if nome_acao is None:
        # ...tenta extrair a primeira linha da docstring da função.
        if funcao_acao.__doc__:
            nome_acao = funcao_acao.__doc__.strip().split('\n')[0]
        else:
            # Caso a função não tenha docstring, usa um nome genérico.
            nome_acao = "Ação sem nome definido"
    # -----------------------------------------------

    # O resto do código da função permanece exatamente o mesmo.
    ultimo_erro = None

    while True:
        for tentativa in range(1, 4):
            try:
                resultado = funcao_acao()
                return resultado

            except Exception as e:
                print(f"{CIANO}🦾 Executando: {nome_acao}...{RESET}")
                ultimo_erro = e
                print(f"{VERMELHO}   ✖ Falha na tentativa {tentativa}/3.{RESET}")
                time.sleep(0.5)

        escolha = exibir_menu_de_falha(nome_acao, ultimo_erro)

        if escolha == 'tentar':
            print(f"{CIANO}🦾 Ok, tentando a ação '{nome_acao}' novamente...{RESET}")
            continue
        elif escolha == 'ignorar':
            print(f"{CIANO}🦾 Ação '{nome_acao}' ignorada. Continuando...{RESET}")
            return None
        elif escolha == 'abortar':
            print(f"{VERMELHO}🦾 Automação abortada pelo usuário.{RESET}")
            raise AutomacaoAbortadaPeloUsuario("O usuário decidiu encerrar o processo.")