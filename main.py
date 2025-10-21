# main.py

"""
Ponto de entrada principal da aplicação de automação SAP B1.
"""

# --- Imports ---
from configuracoes import carregar_config
from validacoes.verificacoes_iniciais import executar_verificacoes_iniciais
from assistente.executor import executar_acao_assistida
from assistente.excecoes import AutomacaoAbortadaPeloUsuario
from uteis.cores import AMARELO, VERMELHO, RESET

# --- Imports das "Paredes" de Ações ---
from acoes.preencher_aba_geral1 import processar_aba_geral_parte1
from acoes.preencher_aba_caracteristicas import preencher_aba_caracteristicas
# NOVO IMPORT: Importa a nossa terceira "parede".
from acoes.preencher_aba_exepgto import preencher_aba_exepgto


def principal():
    """Função que contém a lógica principal e orquestração da automação."""

    print(f"{AMARELO}🚀 Automação SAP B1 iniciada...{RESET}\n")

    try:
        # ETAPA 1: Verificações iniciais do ambiente.
        executar_acao_assistida(executar_verificacoes_iniciais)

        # ETAPA 2: Preenchimento da Aba Geral (Parte 1)
        print(f"\n{AMARELO}--- Iniciando Etapa: Aba Geral (Parte 1) ---{RESET}")
        executar_acao_assistida(processar_aba_geral_parte1)

        # ETAPA 3: Preenchimento da Aba Características
        print(f"\n{AMARELO}--- Iniciando Etapa: Aba Características ---{RESET}")
        executar_acao_assistida(preencher_aba_caracteristicas)

        # --- NOVA ETAPA 4: Preenchimento da Aba Execução de Pagamentos ---
        print(f"\n{AMARELO}--- Iniciando Etapa: Aba Execução de Pagamentos ---{RESET}")
        executar_acao_assistida(preencher_aba_exepgto)
        # -------------------------------------------------------------

        # Futuramente, as próximas "paredes" (outras abas) serão chamadas aqui.


    except AutomacaoAbortadaPeloUsuario:
        # Se o usuário abortar em qualquer etapa, a execução é encerrada aqui.
        print(f"{VERMELHO}🚀 Automação encerrada pelo usuário.{RESET}")
        return # Encerra a função principal.

    print(f"\n{AMARELO}🚀 Automação SAP B1 concluída com sucesso!{RESET}")


if __name__ == "__main__":
    principal()