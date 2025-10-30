# acoes/preencher_aba_enderecos_idfiscais.py

"""
Módulo para preenchimento dos IDs Fiscais na Aba Endereços.
"""

import time
from navegacao.navegacao_abas import ir_para_aba
from funcoes.clicar_elemento import clicar_elemento
from funcoes.digitar_texto import digitar_texto
from uteis.formatadores import limpar_documento
from uteis.extrator_documento_tela import obter_documento_tela_com_fallback
from servicos.consulta_cnpj import obter_dados_cnpj
from assistente.executor import executar_acao_assistida
from uteis.cores import AMARELO, VERDE, VERMELHO, RESET
from funcoes.selecionar_dropdown import selecionar_dropdown


def preencher_aba_enderecos_idfiscais() -> tuple[int, str, str, list]:
    """(Orquestradora) Executa o fluxo para IDs Fiscais e retorna tipo_pessoa, status_suframa, status_ie e a lista_socios."""
    
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
    # Passo 3: Obter e Validar Documento (com Loop e Correção Manual)
    # ============================================================
    documento_limpo = ""
    tipo_pessoa = 0 # 0 = Desconhecido/Inválido, 1 = CPF, 2 = CNPJ
    while True:
        documento_copiado = obter_documento_tela_com_fallback() #AQUIII
        documento_limpo = limpar_documento(documento_copiado)
        if len(documento_limpo) == 14: # É CNPJ
            tipo_pessoa = 2
            break
        elif len(documento_limpo) == 11: # É CPF
            tipo_pessoa = 1
            break
        else: # Documento Inválido
            documento_copiado = input(
                f"\n{VERMELHO}*** ATENÇÃO: DOCUMENTO INVÁLIDO ***{RESET}\n"
                f"{VERMELHO}   - Obtido: '{documento_copiado}' (Limpo: '{documento_limpo}'). Não é CPF/CNPJ.{RESET}\n"
                f"{AMARELO}   - Por favor, digite o documento correto (apenas números) e pressione Enter: {RESET}"
            )
            print(f"{AMARELO}   - Ok, tentando validar o documento digitado...{RESET}")
            # Loop continua para re-limpar e re-validar


    # ============================================================
    # Passo 4: Consultar API(se CNPJ) e obter Socios
    # ============================================================
    inscricao_estadual_final = "Isento" # Padrão
    suframa = "N"
    lista_socios = []
    dados_cnpj_unificados = {}

    if tipo_pessoa == 2: # Somente para CNPJ
        dados_cnpj_unificados = executar_acao_assistida(lambda: obter_dados_cnpj(documento_limpo), nome_acao=f"Obter dados unificados para CNPJ {documento_limpo}")
        lista_socios = dados_cnpj_unificados.get("socios", [])


    # ============================================================
    # Passo 5: obter IE e Suframa
    # ============================================================
        inscricao_estadual_final = dados_cnpj_unificados.get("inscricao_estadual", "Isento")
        if dados_cnpj_unificados.get("suframa_valido"):
            suframa_numero = dados_cnpj_unificados.get("suframa_numero", "")

            if suframa_numero:
                suframa = "Y"
                print(f"   - Suframa Aprovado ({VERDE}{suframa_numero}{RESET}). Preenchendo campo...")
                executar_acao_assistida(lambda: digitar_texto("enderecos_idfiscais_suframa", suframa_numero), nome_acao=f"Preencher Suframa '{suframa_numero}'")
            else:
                print("   - Suframa válido, mas número não encontrado.")
                
        else:
            print("   - Suframa não aplicável ou não encontrado.")
    else: # Se for CPF (tipo_pessoa == 1)
        print(f"   - Documento é CPF: {VERDE}{documento_copiado}{RESET}. Definindo IE como 'Isento'.")
    time.sleep(1.5)


    # ============================================================
    # Passo 6: Escrever IE (Sempre executa após definir o valor final)
    # ============================================================
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
    # Passo 8: Preencher Simples Nacional (SE CNPJ)
    # ============================================================
    if tipo_pessoa == 2: # Repete a verificação, pois só se aplica a CNPJ
        # Verifica o status do Simples Nacional obtido na consulta API (Passo 4)
        status_simples = dados_cnpj_unificados.get("simples_nacional", None)

        if status_simples is True:
            valor_dropdown_simples = '1' # Sim
            nome_opcao = "Sim"
        else: # False ou None
            valor_dropdown_simples = '2' # Não
            nome_opcao = "Não"

        print(f"   - Status Simples Nacional: Verde ({VERDE}{status_simples}{RESET}). Selecionando '{nome_opcao}'...")
        executar_acao_assistida(lambda: selecionar_dropdown("enderecos_simplesnac", valor_dropdown_simples), nome_acao=f"Selecionar Simples Nacional como '{nome_opcao}'")
        time.sleep(0.5)
    else:
        # Se for CPF, não faz nada para o Simples Nacional
        print("   - Documento é CPF. Pulando etapa do Simples Nacional.")
 

    # ============================================================
    # Finalização e Retorno
    # ============================================================
    return tipo_pessoa, suframa, inscricao_estadual_final, lista_socios




# --- Camada de Teste Direto ---
if __name__ == '__main__':
    """
    Bloco para testar esta "parede" de forma isolada.
    Execute-o a partir da raiz do projeto com: python -m acoes.preencher_aba_enderecos_idfiscais
    """
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from assistente.excecoes import AutomacaoAbortadaPeloUsuario

    print(">>> Iniciando teste da 'parede': preencher_aba_enderecos_idfiscais...")
    print(">>> Testando o fluxo COMPLETO (Passos 1 a 5)...")
    print(">>> O teste começará em 5 segundos...")
    time.sleep(5)
    try:
        preencher_aba_enderecos_idfiscais()
        print("\n--- Teste da 'parede' concluído com SUCESSO! ---")
    except AutomacaoAbortadaPeloUsuario:
        print("\n--- Teste ABORTADO pelo usuário. ---")
    except Exception as e:
        print(f"\n--- Teste da 'parede' FALHOU! Erro: {e} ---")