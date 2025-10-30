# acoes/preencher_aba_condicoespgto.py

"""
Módulo para preenchimento da aba Condições de Pagamento.
"""

import time
from navegacao.navegacao_abas import ir_para_aba
from funcoes.clicar_elemento import clicar_elemento
from assistente.executor import executar_acao_assistida


def preencher_aba_condicoespgto():
    """(Orquestradora) Executa o fluxo completo para a Aba Condições de Pagamento..
    """
# ============================================================
# Passo 1: Navegar para a aba.
# ============================================================
    time.sleep(1)
    executar_acao_assistida(lambda: ir_para_aba("condicoespgto"), nome_acao="Navegar para a Aba Condições de Pagamento")
    time.sleep(1)

# ============================================================
# Passo 2: Clicar no elemento de entrega parcial.
# ============================================================
    executar_acao_assistida(lambda: clicar_elemento("condicoespgto_entregparcial"), nome_acao="Marcar/Desmarcar 'Permitir Entrega Parcial'")
    time.sleep(0.5)


# --- Camada de Teste Direto ---
if __name__ == '__main__':
    """
    Bloco para testar de forma isolada.
    Execute-o a partir da raiz do projeto com: python -m acoes.preencher_aba_condicoespgto
    """
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).resolve().parent.parent))

    from assistente.excecoes import AutomacaoAbortadaPeloUsuario

    print(">>> Iniciando teste da 'parede': preencher_aba_condicoespgto...")
    print(">>> Testando Passos 1 e 2 (Navegação, Clique Entrega Parcial)...")
    print(">>> O teste começará em 5 segundos...")
    time.sleep(5)

    try:
        preencher_aba_condicoespgto()
        print("\n--- Teste da 'parede' (Passos 1 e 2) concluído com SUCESSO! ---")

    except AutomacaoAbortadaPeloUsuario:
        print("\n--- Teste ABORTADO pelo usuário. ---")
    except Exception as e:
        print(f"\n--- Teste da 'parede' FALHOU! Erro: {e} ---")