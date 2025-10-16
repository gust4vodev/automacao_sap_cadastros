# main.py

"""
Ponto de entrada principal da aplicação de automação SAP B1.
"""

# --- Imports ---
from configuracoes import carregar_config
# MUDANÇA 1: Importa a nova função, mais completa.
from validacoes.verificacoes_iniciais import executar_verificacoes_iniciais
from assistente.executor import executar_acao_assistida
from assistente.excecoes import AutomacaoAbortadaPeloUsuario
from uteis.cores import AMARELO, VERMELHO, RESET


def principal():
    """Função que contém a lógica principal e orquestração da automação."""

    print(f"{AMARELO}🚀 Automação SAP B1 iniciada...{RESET}\n")

    try:
        # Antes de qualquer coisa, testa todas as dependencias externas
        executar_acao_assistida(executar_verificacoes_iniciais)

    except AutomacaoAbortadaPeloUsuario:
        # Se o usuário abortar, o motor levanta uma exceção que é
        # capturada aqui para encerrar o programa de forma limpa.
        print(f"{VERMELHO}🚀 Automação encerrada pelo usuário.{RESET}")
        return # Encerra a função principal.

    print(f"\n{AMARELO}🚀 Automação SAP B1 concluída com sucesso!{RESET}")


if __name__ == "__main__":
    principal()