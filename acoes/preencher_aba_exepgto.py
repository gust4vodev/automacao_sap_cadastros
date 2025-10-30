# acoes/preencher_aba_exepgto.py

"""
Módulo para preenchimento da aba Execução de Pagamentos.
"""

import time
from navegacao.navegacao_abas import ir_para_aba
from funcoes.clicar_elemento import clicar_elemento
from funcoes.rolar_mouse import rolar_mouse_linhas
from assistente.executor import executar_acao_assistida

def preencher_aba_exepgto(divisao_pn: int):
    """(Orquestradora) Executa o fluxo completo para a Aba Execução de Pagamentos.
    Cada passo é executado individualmente pelo 'assistente.executor'.
    """
    # ============================================================
    # 1. Navegar para a aba.
    # ============================================================
    executar_acao_assistida(lambda: ir_para_aba("exepgto"), nome_acao="Navegar para a Aba Execução de Pagamentos")
    time.sleep(1)


    # ============================================================
    # 2. Abrir janela de formas de pgto.
    # ============================================================
    executar_acao_assistida(lambda: clicar_elemento("exepgto_abrirformas"), nome_acao="Abrir janela de Formas de Pagamento")
    time.sleep(1)


    # ============================================================
    # 3. Selecionar forma de pgto 'Bonificação'.
    # ============================================================
    executar_acao_assistida(lambda: clicar_elemento("exepgto_bonif"), nome_acao="Selecionar forma de pgto 'Bonificação'")
    time.sleep(0.5)


    if divisao_pn != 4:
    # ============================================================
    # 4. Clicar nas formas de pgto 'Crédito'.
    # ============================================================ 
        executar_acao_assistida(lambda: clicar_elemento("exepgto_cred"), nome_acao="Selecionar forma de pgto 'Crédito'")
        time.sleep(0.5)


    # ============================================================
    # 5. Clicar na forma de pgto 'Depósito'.
    # ============================================================
    executar_acao_assistida(lambda: clicar_elemento("exepgto_deposito"), nome_acao="Selecionar forma de pgto 'Depósito'")
    time.sleep(0.5)


    # ============================================================
    # 6. Rolar a lista para baixo.
    # ============================================================
    executar_acao_assistida(lambda: rolar_mouse_linhas(11, direcao='baixo'), nome_acao="Rolar 8 linhas para baixo na lista de formas de pgto")
    time.sleep(0.5)


    # ============================================================
    # 7. Clicar na forma de pgto 'Misto'.
    # ============================================================
    executar_acao_assistida(lambda: clicar_elemento("exepgto_misto"), nome_acao="Selecionar forma de pgto 'Misto'")
    time.sleep(0.5)


    # ============================================================
    # 8. Clicar para fechar a janela.
    # ============================================================
    executar_acao_assistida(lambda: clicar_elemento("exepgto_fecharformas"), nome_acao="Fechar janela de Formas de Pagamento")
    time.sleep(1) # Pausa para a janela fechar


# --- Camada de Teste Direto ---
if __name__ == '__main__':
    """
    Bloco para testar esta "parede" de forma isolada.
    Execute-o a partir da raiz do projeto com: python -m acoes.preencher_aba_exepgto
    """
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).resolve().parent.parent))

    from assistente.excecoes import AutomacaoAbortadaPeloUsuario

    print(">>> Iniciando teste da 'parede': preencher_aba_exepgto...")
    print(">>> Testando o fluxo COMPLETO (Passos 1 a 6)...")
    print(">>> O teste começará em 5 segundos...")
    time.sleep(1)

    try:
        preencher_aba_exepgto(2)
        print("\n--- Teste da 'parede' (Passos 1 a 6) concluído com SUCESSO! ---")

    except AutomacaoAbortadaPeloUsuario:
        print("\n--- Teste ABORTADO pelo usuário. ---")
    except Exception as e:
        print(f"\n--- Teste da 'parede' FALHOU! Erro: {e} ---")