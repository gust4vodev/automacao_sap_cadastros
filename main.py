# main.py

"""
Ponto de entrada principal da aplicação de automação SAP B1.
"""

# --- Imports ---
import configuracoes.carregar_config
from validacoes.verificacoes_iniciais import executar_verificacoes_iniciais
from assistente.executor import executar_acao_assistida
from assistente.excecoes import AutomacaoAbortadaPeloUsuario
from uteis.cores import AMARELO, VERMELHO, RESET
# --- Imports das "Paredes" de Ações ---
from acoes.preencher_aba_geral1 import processar_aba_geral_parte1
from acoes.preencher_aba_caracteristicas import preencher_aba_caracteristicas
from acoes.preencher_aba_exepgto import preencher_aba_exepgto
from acoes.preencher_aba_condicoespgto import preencher_aba_condicoespgto
from acoes.preencher_aba_enderecos_idfiscais import preencher_aba_enderecos_idfiscais


def principal():
    """Função que contém a lógica principal e orquestração da automação."""

    print(f"{AMARELO}🚀 Automação SAP B1 iniciada...{RESET}\n")

    try:
        # ETAPA 1: Verificações iniciais do ambiente.
        print("⚙️  Executando verificações iniciais do ambiente...")
        executar_acao_assistida(executar_verificacoes_iniciais)

        # ETAPA 2: Preenchimento da Aba Geral (Parte 1)
        print(f"\n{AMARELO}--- Iniciando Etapa: Aba Geral (Parte 1) ---{RESET}")
        executar_acao_assistida(processar_aba_geral_parte1)

        # ETAPA 3: Preenchimento da Aba Características
        print(f"\n{AMARELO}--- Iniciando Etapa: Aba Características ---{RESET}")
        divisao_pn = executar_acao_assistida(preencher_aba_caracteristicas)
        print(f"divisao_pn: {divisao_pn}")

        # ETAPA 4: Preenchimento da Aba Execução de Pagamentos
        print(f"\n{AMARELO}--- Iniciando Etapa: Aba Execução de Pagamentos ---{RESET}")
        executar_acao_assistida(lambda: preencher_aba_exepgto(divisao_pn), nome_acao="Preencher Aba Execução de Pagamentos")

        """ Houve uma alteração onde o flag de preenchimento da Aba Condições de Pagamento
            foi removido. Portanto, a etapa 5 foi comentada temporariamente."""
        # ETAPA 5: Preenchimento da Aba Condições de Pagamento
        #print(f"\n{AMARELO}--- Iniciando Etapa: Aba Condições de Pagamento ---{RESET}")
        #executar_acao_assistida(preencher_aba_condicoespgto)

        # --- NOVA ETAPA 6: Preenchimento dos IDs Fiscais na Aba Endereços ---
        print(f"\n{AMARELO}--- Iniciando Etapa: Aba Endereços - IDs Fiscais ---{RESET}")
        tipo_pessoa, suframa = executar_acao_assistida(preencher_aba_enderecos_idfiscais)

        
       


        # Futuramente, as próximas "paredes" (outras abas) serão chamadas aqui.


    except AutomacaoAbortadaPeloUsuario:
        # Se o usuário abortar em qualquer etapa, a execução é encerrada aqui.
        print(f"{VERMELHO}🚀 Automação encerrada pelo usuário.{RESET}")
        return # Encerra a função principal.

    print(f"\n{AMARELO}🚀 Automação SAP B1 concluída com sucesso!{RESET}")


if __name__ == "__main__":
    principal()