# main.py

"""
Ponto de entrada principal da aplicação de automação SAP B1.
(Refatorado para arquitetura de Sessão JSON)
"""

from validacoes.verificacoes_iniciais import executar_verificacoes_iniciais
from assistente.executor import executar_acao_assistida
from assistente.excecoes import AutomacaoAbortadaPeloUsuario
from uteis.cores import AMARELO, VERMELHO, RESET
from acoes.preencher_aba_geral1 import processar_aba_geral_parte1
from acoes.preencher_aba_caracteristicas import preencher_aba_caracteristicas
from acoes.preencher_aba_exepgto import preencher_aba_exepgto
from acoes.preencher_aba_enderecos_idfiscais import preencher_aba_enderecos_idfiscais
from acoes.processar_endereco_faturamento import processar_endereco_faturamento
from acoes.preencher_socios import preencher_aba_socios
from uteis.gestor_sessao import encerrar_sessao
from acoes.preencher_aba_geral2 import preencher_aba_geral2


def principal():
    """Função que contém a lógica principal e orquestração da automação."""

    print(f"{AMARELO}🚀 Automação SAP B1 iniciada...{RESET}\n")

    try:
        # ETAPA 1: Verificações iniciais do ambiente.
        print("⚙️   Executando verificações iniciais do ambiente...")
        executar_acao_assistida(executar_verificacoes_iniciais)

        # ETAPA 2: Preenchimento da Aba Geral (Parte 1)
        print(f"\n{AMARELO}--- Iniciando Etapa: Aba Geral (Parte 1) ---{RESET}")
        executar_acao_assistida(processar_aba_geral_parte1)

        # ETAPA 3: Preenchimento da Aba Características
        print(f"\n{AMARELO}--- Iniciando Etapa: Aba Características ---{RESET}")
        divisao_pn = executar_acao_assistida(preencher_aba_caracteristicas)

        # ETAPA 4: Preenchimento da Aba Execução de Pagamentos
        print(f"\n{AMARELO}--- Iniciando Etapa: Aba Execução de Pagamentos ---{RESET}")
        executar_acao_assistida(lambda: preencher_aba_exepgto(divisao_pn), nome_acao="Preencher Aba Execução de Pagamentos")
            
        # ETAPA 5: Preenchimento dos IDs Fiscais (O "GATILHO" da Sessão JSON)
        print(f"\n{AMARELO}--- Iniciando Etapa: Aba Endereços - IDs Fiscais ---{RESET}")
        executar_acao_assistida(preencher_aba_enderecos_idfiscais)

        # ETAPA 6: Processamento de Endereço de Faturamento
        print(f"\n{AMARELO}--- Iniciando Etapa: Aba Endereços - Faturamento ---{RESET}")
        executar_acao_assistida(processar_endereco_faturamento)
        
        # ETAPA 7: Preenchimento dos Socios
        print(f"\n{AMARELO}--- Iniciando Etapa: Aba Pessoas de Contato (Sócios) ---{RESET}")
        executar_acao_assistida(preencher_aba_socios, nome_acao="Preencher Aba Pessoas de Contato (Sócios)")

        # ETAPA 8: Preenchimento Geral 2
        print(f"\n{AMARELO}--- Iniciando Etapa: Aba Pessoas de Contato (Sócios) ---{RESET}")
        executar_acao_assistida(preencher_aba_geral2, nome_acao="Preencher Aba Geral 2")

        # ETAPA 9: Finalização
        print(f"\n{AMARELO}🚀 Automação SAP B1 concluída com sucesso!{RESET}")


    except AutomacaoAbortadaPeloUsuario:
        # Se o usuário abortar em qualquer etapa, a execução é encerrada aqui.
        print(f"{VERMELHO}🚀 Automação encerrada pelo usuário.{RESET}")

    except Exception as e:
        print(f"{VERMELHO}🚀 Automação FALHOU com erro crítico: {e}{RESET}")

    finally:
        input('SESSÃO SERA ENCERRADA............................................')
        # Esta etapa SEMPRE será executada (sucesso, aborto ou falha).
        # Limpa o 'dados_sessao.json' de volta ao template vazio.
        print(f"\n{AMARELO}--- Encerrando sessão... ---{RESET}")
        encerrar_sessao()
        print(f"{AMARELO}🚀 Execução finalizada.{RESET}")


if __name__ == "__main__":
    principal()