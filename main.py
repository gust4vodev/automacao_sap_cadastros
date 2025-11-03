# main.py

"""
Ponto de entrada principal da aplicação de automação SAP B1.
(Refatorado para arquitetura de Sessão JSON)
"""

# --- Imports ---
from validacoes.verificacoes_iniciais import executar_verificacoes_iniciais
from assistente.executor import executar_acao_assistida
from assistente.excecoes import AutomacaoAbortadaPeloUsuario
from uteis.cores import AMARELO, VERMELHO, RESET
from acoes.preencher_aba_geral1 import processar_aba_geral_parte1
from acoes.preencher_aba_caracteristicas import preencher_aba_caracteristicas
from acoes.preencher_aba_exepgto import preencher_aba_exepgto
# (condicoespgto está comentado, mantido)
# from acoes.preencher_aba_condicoespgto import preencher_aba_condicoespgto
from acoes.preencher_aba_enderecos_idfiscais import preencher_aba_enderecos_idfiscais
from acoes.processar_endereco_faturamento import processar_endereco_faturamento
from acoes.preencher_socios import preencher_aba_socios
from uteis.gestor_sessao import encerrar_sessao


def principal():
    """Função que contém a lógica principal e orquestração da automação."""

    print(f"{AMARELO}🚀 Automação SAP B1 iniciada...{RESET}\n")

    try:
        # ETAPA 1: Verificações iniciais do ambiente.
        # (Esta etapa agora chama 'iniciar_sessao()')
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
            
        # ETAPA 5: (Comentada)
        # ...

        # ============================================================
        # ETAPA 6: Preenchimento dos IDs Fiscais (O "GATILHO" do JSON)
        # ============================================================
        print(f"\n{AMARELO}--- Iniciando Etapa: Aba Endereços - IDs Fiscais ---{RESET}")
        # (Esta função agora escreve no JSON e não retorna nada)
        executar_acao_assistida(preencher_aba_enderecos_idfiscais)

        # ============================================================
        # ETAPA 7: Processamento de Endereço de Faturamento (Consumidor)
        # ============================================================
        print(f"\n{AMARELO}--- Iniciando Etapa: Aba Endereços - Faturamento ---{RESET}")
        # (Esta chamada está desacoplada e correta)
        executar_acao_assistida(processar_endereco_faturamento)
        
        # ============================================================
        # ETAPA 8: Preenchimento dos Socios (Consumidor)
        # ============================================================
        print(f"\n{AMARELO}--- Iniciando Etapa: Aba Pessoas de Contato (Sócios) ---{RESET}")
        # (Esta chamada está desacoplada e correta)
        executar_acao_assistida(preencher_aba_socios, nome_acao="Preencher Aba Pessoas de Contato (Sócios)")

        print(f"\n{AMARELO}🚀 Automação SAP B1 concluída com sucesso!{RESET}")


    except AutomacaoAbortadaPeloUsuario:
        # Se o usuário abortar em qualquer etapa, a execução é encerrada aqui.
        print(f"{VERMELHO}🚀 Automação encerrada pelo usuário.{RESET}")
        # O 'finally' será chamado automaticamente após isto.

    except Exception as e:
        # Captura qualquer outra falha crítica
        print(f"{VERMELHO}🚀 Automação FALHOU com erro crítico: {e}{RESET}")
        # O 'finally' será chamado automaticamente após isto.

    finally:
        input('SESSÃO SERA ENCERRADA............................................')
        # Esta etapa SEMPRE será executada (sucesso, aborto ou falha).
        # Limpa o 'dados_sessao.json' de volta ao template vazio.
        print(f"\n{AMARELO}--- Encerrando sessão... ---{RESET}")
        encerrar_sessao()
        print(f"{AMARELO}🚀 Execução finalizada.{RESET}")


if __name__ == "__main__":
    principal()