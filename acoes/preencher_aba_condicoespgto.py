# acoes/preencher_aba_condicoespgto.py

"""
Módulo para a "parede" de ações: preenchimento da aba Condições de Pagamento.
"""

import time

# --- Imports de Módulos do Projeto ---
from navegacao.navegacao_abas import ir_para_aba
from funcoes.clicar_elemento import clicar_elemento
from assistente.executor import executar_acao_assistida


def preencher_aba_condicoespgto():
    """(Orquestradora) Executa o fluxo completo para a Aba Condições de Pagamento.

    Cada passo é executado individualmente pelo motor.
    """
    # Passo 1: Navegar para a aba.
    # CORREÇÃO: Usar a chave correta 'aba_condicoespgto'
    executar_acao_assistida(
        lambda: ir_para_aba("condicoespgto"),
        nome_acao="Navegar para a Aba Condições de Pagamento"
    )
    time.sleep(1)

    # Passo 2: Clicar no elemento de entrega parcial.
    executar_acao_assistida(
        # A chave segue o nosso padrão: [aba]_[elemento]
        lambda: clicar_elemento("condicoespgto_entregparcial"),
        nome_acao="Marcar/Desmarcar 'Permitir Entrega Parcial'"
    )
    time.sleep(0.5)

    # Próximos passos (se houver) serão adicionados aqui.


# --- Camada de Teste Direto ---
if __name__ == '__main__':
    """
    Bloco para testar esta "parede" de forma isolada.
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