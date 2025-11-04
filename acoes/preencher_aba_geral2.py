# acoes/preencher_aba_geral2.py

"""
Módulo para a ação: preenchimento da Aba Geral (Parte 2).

Esta parede é um "Consumidor" de dados do 'gestor_sessao.json'.
Ela preenche:
- Data de Abertura
- Tipo de Pessoa
- Indicador de IE (Regra CC)
- Indicador de Op. Consumidor (Regra CC)
"""

import time
from assistente.executor import executar_acao_assistida
from uteis.cores import AMARELO, VERDE, RESET
from funcoes.colar_texto import colar_texto
from funcoes.selecionar_dropdown import selecionar_dropdown
from uteis.gestor_sessao import ler_dados_sessao
from datetime import datetime
from navegacao.navegacao_abas import ir_para_aba





def preencher_aba_geral2():
    """
    (Orquestradora/Consumidor) Executa o fluxo de preenchimento
    da segunda parte da Aba Geral (Data Abertura, Tipo Pessoa, Regra CC).
    """

    # ============================================================
    # 1. Navega para a aba correta
    # ============================================================
    time.sleep(1)
    executar_acao_assistida(lambda: ir_para_aba("geral"), nome_acao="Navegar para a Aba Geral")
    time.sleep(3)


    # ============================================================
    # 2. Ler Dados da Sessão JSON
    # ============================================================
    dados_sessao = ler_dados_sessao()
    data_abertura = dados_sessao.get("data_abertura", "")
    tipo_pessoa_num = dados_sessao.get("tipo_pessoa", 0)
    status_ie = dados_sessao.get("inscricao_estadual", "Isento")


    # ============================================================
    # 3. Preencher Data de Abertura
    # ============================================================
    if not data_abertura:
        print(f"   {AMARELO}⚠️  Data de Abertura não encontrada no JSON. Pulando passo.{RESET}")
    else:
        try:
            # 1. Converte a string AAAA-MM-DD para um objeto data
            data_obj = datetime.strptime(data_abertura, "%Y-%m-%d")
            # 2. Formata o objeto data para a string DD/MM/AAAA
            data_formatada_br = data_obj.strftime("%d/%m/%Y")
            executar_acao_assistida(lambda: colar_texto("geral2_data_abertura", data_formatada_br), nome_acao=f"Preencher Data de Abertura ({data_formatada_br})")
            time.sleep(1)
        
        except ValueError:
            # Se a data no JSON estiver num formato inesperado (ex: "Isento")
            print(f"   {AMARELO}⚠️  Data de Abertura '{data_abertura}' está em formato inválido (esperado AAAA-MM-DD). Pulando passo.{RESET}")


    # ============================================================
    # 4. Definir Tipo de Pessoa
    # ============================================================
    if tipo_pessoa_num == 0:
        print(f"   {AMARELO}⚠️  Tipo de Pessoa (1 ou 2) não encontrado no JSON. Pulando passo.{RESET}")
    else:
        valor_tipo_pessoa_sap = str(tipo_pessoa_num)
        executar_acao_assistida(lambda: selecionar_dropdown("geral2_tipo_pessoa", valor_tipo_pessoa_sap), nome_acao=f"Selecionar Tipo Pessoa ({valor_tipo_pessoa_sap})")
        time.sleep(1)


    # ============================================================
    # 5. Executar "Regra CC"
    # ============================================================
    if str(status_ie).strip().lower() == "isento":
        valor_ind_ie = "9"
        valor_op_cons = "1"
    else:
        # (Qualquer coisa diferente de 'isento' (um número))
        valor_ind_ie = "1"
        valor_op_cons = "0"
        

    # ============================================================
    # 6. Definir Ind. IE 
    # ============================================================
    executar_acao_assistida(lambda: selecionar_dropdown("geral2_indicador_ie", valor_ind_ie), nome_acao=f"Selecionar Indicador IE ({valor_ind_ie})")
    time.sleep(1)


    # ============================================================
    # 7. Definir Ind. Op Cons
    # ============================================================
    executar_acao_assistida(lambda: selecionar_dropdown("geral2_op_consumidor", valor_op_cons), nome_acao=f"Selecionar Ind. Op. Consumidor ({valor_op_cons})")
    time.sleep(1)
    

# --- Camada de Teste Direto ---
if __name__ == '__main__':
    """
    Bloco para testar esta ação de forma isolada (MODO JSON).
    Execute a partir da raiz: python -m acoes.preencher_aba_geral2
    """
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from assistente.excecoes import AutomacaoAbortadaPeloUsuario
    from uteis.gestor_sessao import iniciar_sessao, escrever_dados_sessao, encerrar_sessao

    # 1. Preparar os dados falsos (Cenário: NÃO Isento)
    dados_falsos_sessao = {
        "data_abertura": "2020-05-10",
        "tipo_pessoa": 2, # CNPJ
        "inscricao_estadual": "123456789" # <-- NÃO ISENTO
    }
    # (Para testar o 'Isento', mude para "inscricao_estadual": "Isento")

    # 2. Iniciar a sessão (Cria o JSON)
    iniciar_sessao()
    # 3. Escrever os dados de teste no JSON
    escrever_dados_sessao(dados_falsos_sessao)
    # ---------------------------

    print(">>> Iniciando teste da ação: preencher_aba_geral2...")
    print(f">>> (JSON de sessão preparado com dados falsos: NÃO Isento)")
    print(">>> ATENÇÃO: O teste tentará COLAR e SELECIONAR dropdowns na tela.")
    print(">>> O teste começará em 5 segundos...")
    time.sleep(5)
    
    try:
        # Chama a função (agora sem parâmetros)
        preencher_aba_geral2()
        print("\n--- Teste da 'parede' (preencher_aba_geral2) concluído com SUCESSO! ---")
    
    except AutomacaoAbortadaPeloUsuario:
        print("\n--- Teste ABORTADO pelo usuário. ---")
    except Exception as e:
        print(f"\n--- Teste da 'parede' FALHOU! Erro: {e} ---")
        
    finally:
        # Limpa o JSON no final do teste
        print("\n--- Encerrando sessão de teste... ---")
        encerrar_sessao()