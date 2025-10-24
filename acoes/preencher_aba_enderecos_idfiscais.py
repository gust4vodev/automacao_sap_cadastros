# acoes/preencher_aba_enderecos_idfiscais.py

"""
Módulo para a "parede" de ações: preenchimento dos IDs Fiscais na Aba Endereços.
"""

import time

# --- Imports de Módulos do Projeto ---
from navegacao.navegacao_abas import ir_para_aba
from funcoes.clicar_elemento import clicar_elemento
from funcoes.digitar_texto import digitar_texto
from uteis.formatadores import limpar_documento
from uteis.extrator_documento_tela import obter_documento_tela_com_fallback
from servicos.consulta_cnpj import obter_dados_cnpj
from assistente.executor import executar_acao_assistida


def preencher_aba_enderecos_idfiscais():
    """(Orquestradora) Executa o fluxo para IDs Fiscais na Aba Endereços."""
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
    # Passo 3: Obter Documento
    # ============================================================
    try:
        documento_copiado = obter_documento_tela_com_fallback()
    except Exception as e:
        raise RuntimeError(f"Falha crítica ao obter documento da tela: {e}")
    documento_limpo = limpar_documento(documento_copiado)
    time.sleep(1)

    # ============================================================
    # Passo 4: Consultar Documento via API / Obter IE
    # ============================================================
    inscricao_estadual_final = "Isento"
    if len(documento_limpo) == 14: # É CNPJ
        dados_cnpj_unificados = executar_acao_assistida(lambda: obter_dados_cnpj(documento_limpo),nome_acao=f"Obter dados unificados para CNPJ {documento_limpo}")
        inscricao_estadual_final = dados_cnpj_unificados.get("inscricao_estadual", "Isento")
        time.sleep(1)
    elif len(documento_limpo) == 11: # É CPF
        time.sleep(1)
    else:
        print(f"   - Documento '{documento_copiado}' não reconhecido. Definindo IE como 'Isento'.")
        time.sleep(1)

    # ============================================================
    # Passo 5: Escrever IE
    # ============================================================
    print(f"   - Inscrição Estadual {inscricao_estadual_final}. Digitando...")
    executar_acao_assistida(lambda: digitar_texto("endereco_idfiscais_ie", inscricao_estadual_final), nome_acao=f"Digitar Inscrição Estadual '{inscricao_estadual_final}'")
    time.sleep(1)

    # ============================================================
    # Passo 6: Clicar Atualizar e OK
    # ============================================================
    executar_acao_assistida(lambda: clicar_elemento("endereco_idfiscais_atualizar"), nome_acao="Clicar 'Atualizar'")
    time.sleep(1)
    executar_acao_assistida(lambda: clicar_elemento("endereco_idfiscais_ok"), nome_acao="Clicar 'OK'")
    time.sleep(1)


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