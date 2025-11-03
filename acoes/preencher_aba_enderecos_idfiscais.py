# acoes/preencher_aba_enderecos_idfiscais.py

"""
Módulo para preenchimento dos IDs Fiscais na Aba Endereços.
"""

import time
from navegacao.navegacao_abas import ir_para_aba
from funcoes.clicar_elemento import clicar_elemento
from funcoes.digitar_texto import digitar_texto
from uteis.formatadores import contar_caracteres, limpar_documento
from uteis.extrator_documento_tela import scraping_cnpj_cpf
from servicos.consulta_cnpj import obter_dados_cnpj
from assistente.executor import executar_acao_assistida
from uteis.cores import AMARELO, VERDE, VERMELHO, RESET
from funcoes.selecionar_dropdown import selecionar_dropdown
from uteis.gestor_sessao import ler_dados_sessao, escrever_dados_sessao


def preencher_aba_enderecos_idfiscais():
    """
    (Orquestradora) Executa o fluxo para IDs Fiscais.
    É o "Gatilho" (Trigger) que preenche o dados_sessao.json.
    """
    
    # ============================================================
    # Passo 1: Navegar para Aba Endereços
    # ============================================================
    executar_acao_assistida(lambda: ir_para_aba("enderecos"), nome_acao="Navegar para a Aba Endereços")
    time.sleep(1)


    # ============================================================
    # Passo 2: Abrir IDs Fiscais
    # ============================================================
    executar_acao_assistida(lambda: clicar_elemento("enderecos_idfiscais"), nome_acao="Abrir IDs Fiscais")
    time.sleep(1)


    # ============================================================
    # Passo 3: Obter, Validar e SALVAR 'tipo_pessoa'
    # ============================================================
    documento_copiado = scraping_cnpj_cpf()
    documento_limpo = limpar_documento(documento_copiado)
    tipo_pessoa = 0 # 0 = Desconhecido/Inválido, 1 = CPF, 2 = CNPJ
    
    if contar_caracteres(documento_limpo) == 14: # É CNPJ
        tipo_pessoa = 2
    elif contar_caracteres(documento_limpo) == 11: # É CPF
        tipo_pessoa = 1
        escrever_dados_sessao({"documento_consultado": documento_limpo})
        

    # Escreve o tipo_pessoa no JSON para que outras ações saibam
    escrever_dados_sessao({"tipo_pessoa": tipo_pessoa})
    

    # ============================================================
    # Passo 4: Consultar API e Validar status (se CNPJ) (Gatilho do JSON)
    # ============================================================
    inscricao_estadual_final = "Isento" # Padrão
    status_simples = None # Padrão
    if tipo_pessoa == 2: # Somente para CNPJ
        
        executar_acao_assistida(lambda: obter_dados_cnpj(documento_copiado), nome_acao=f"Obter dados unificados para CNPJ {documento_copiado}")
        dados_sessao = ler_dados_sessao()
        #captura status do CNPJ no arquivo JSON que foi enriquecido pela consulta API.
        status_cnpj = dados_sessao.get("status_cnpj", "N/A").strip().lower()

        if status_cnpj != "ativa":
            # Se não estiver "Ativa" (Pode ser "Baixada", "Inapta", "Suspensa", etc.)
            erro_msg = f"CNPJ {documento_copiado} não está com status 'Ativa'. Status encontrado: '{status_cnpj.title()}'."
            print(f"   {VERMELHO}❌ CNPJ IRREGULAR: {erro_msg}{RESET}")
            # Levanta um erro que o 'executor_acao_assistida' (no main.py) vai apanhar
            raise ValueError(erro_msg)
        print(f"   {VERDE}✔ Status do CNPJ validado: Ativa.{RESET}")
    

    # ============================================================
    # Passo 5: Obter IE(do JSON) e Preencher 
    # ============================================================
        inscricao_estadual_final = dados_sessao.get("inscricao_estadual", "Isento")

    else: # Se for CPF (tipo_pessoa == 1)
        print(f"   - Documento é CPF: {VERDE}{documento_copiado}{RESET}. Definindo IE como 'Isento'.")
    time.sleep(1.5)

    executar_acao_assistida(lambda: digitar_texto("enderecos_idfiscais_ie", inscricao_estadual_final), nome_acao=f"Digitar Inscrição Estadual ('{inscricao_estadual_final}')")
    time.sleep(0.5)


    # ============================================================
    # Passo 7: Clicar Atualizar e OK
    # ============================================================
    executar_acao_assistida(lambda: clicar_elemento("enderecos_idfiscais_atualizar"), nome_acao="Clicar 'Atualizar'")
    time.sleep(2)
    executar_acao_assistida(lambda: clicar_elemento("enderecos_idfiscais_ok"), nome_acao="Clicar 'OK'")
    time.sleep(1)


    # ============================================================
    # Passo 8: Preencher Simples Nacional
    # ============================================================
    if tipo_pessoa == 2:
        status_simples = dados_sessao.get("simples_nacional", None)
        if status_simples is True:
            valor_dropdown_simples = '1' # Sim
            nome_opcao = "Sim"
        else: # False ou None
            valor_dropdown_simples = '2' # Não
            nome_opcao = "Não"

        print(f"   - Status Simples Nacional: ({VERDE}{status_simples}{RESET}). Selecionando '{nome_opcao}'...")
        executar_acao_assistida(lambda: selecionar_dropdown("enderecos_simplesnac", valor_dropdown_simples), nome_acao=f"Selecionar Simples Nacional como '{nome_opcao}'")
        time.sleep(0.5)
    else:
        print("   - Documento é CPF. Pulando etapa do Simples Nacional.")


# --- Camada de Teste Direto ---
if __name__ == '__main__':
    """
    Bloco para testar esta ação de forma isolada.
    """
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from assistente.excecoes import AutomacaoAbortadaPeloUsuario
    
    # Para testar este módulo, o 'gestor_sessao' deve ser iniciado
    from uteis.gestor_sessao import iniciar_sessao, encerrar_sessao
    iniciar_sessao()

    print(">>> Iniciando teste da ação: preencher_aba_enderecos_idfiscais...")
    print(">>> (Teste agora usa o 'dados_sessao.json')")
    print(">>> O teste começará em 5 segundos...")
    time.sleep(5)
    
    try:
        preencher_aba_enderecos_idfiscais()
        print("\n--- Teste da ação concluído com SUCESSO! ---")
    
    except AutomacaoAbortadaPeloUsuario:
        print("\n--- Teste ABORTADO pelo usuário. ---")
    except Exception as e:
        print(f"\n--- Teste da ação FALHOU! Erro: {e}")
        
    finally:
        print("\n--- Encerrando sessão de teste... ---")
        encerrar_sessao()