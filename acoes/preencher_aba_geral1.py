# acoes/preencher_aba_geral.py

"""
Módulo de preenchimento da primeira parte da Aba Geral,
com cada passo executado individualmente pelo 'assistente.executor'.
"""

import time
from datetime import date
from navegacao.navegacao_abas import ir_para_aba
from funcoes.selecionar_dropdown import selecionar_dropdown
from funcoes.digitar_texto import digitar_texto
from assistente.executor import executar_acao_assistida


def processar_aba_geral_parte1():
    """(Orquestradora) Executa o fluxo completo para a Aba Geral.

    Esta função de alto nível orquestra a sequência de ações, passando
    cada passo individualmente pelo motor de execução assistida para
    controle granular de falhas e retentativas.
    """
    
    # ============================================================
    # 1. Navega para a aba correta
    # ============================================================
    executar_acao_assistida(lambda: ir_para_aba("geral"), nome_acao="Navegar para a Aba Geral")
    time.sleep(1)


    # ============================================================
    # 2. Define o tipo do PN.
    # ============================================================
    executar_acao_assistida(lambda: selecionar_dropdown("geral1_tipopn", "Cliente"),nome_acao="Definir Tipo do PN como 'Cliente'")
    time.sleep(2)


    # ============================================================
    # 3. Define a Moeda.
    # ============================================================
    executar_acao_assistida(lambda: selecionar_dropdown("geral1_moeda", "Real", ajuste_x_override=150),nome_acao="Definir Moeda como 'Real'")
    time.sleep(1)


    # ============================================================
    # 4. Define o Tipo de envio.
    # ============================================================
    executar_acao_assistida(lambda: selecionar_dropdown("geral1_tipoenvio", "sem", ajuste_x_override=150),nome_acao="Definir Tipo de Envio como 'Sem-frete'")
    time.sleep(1)


    # ============================================================
    # 5. Define a Data de início.
    # ============================================================
    data_hoje = date.today().strftime("%d/%m/%Y")
    executar_acao_assistida(lambda: digitar_texto("geral1_datainicio", "H", ajuste_x_override=150),nome_acao=f"Definir Data de Início como 'Hoje' ({data_hoje})")
    time.sleep(1)


    # ============================================================
    # 6. Define o Uso-principal.
    # ============================================================
    executar_acao_assistida(lambda: selecionar_dropdown("geral1_usoprincipal", "s-venda", ajuste_x_override=120),nome_acao="Definir Uso Principal como 'S-Vendas'")
    time.sleep(1)


    # ============================================================
    # 7. Define Enviar p/revisão.
    # ============================================================
    executar_acao_assistida(lambda: selecionar_dropdown("geral1_enviarrevisao", "N", ajuste_x_override=120),nome_acao="Definir 'Enviar p/ Revisão' como 'Não'")
    time.sleep(1)

# --- Camada de Teste Direto ---
if __name__ == '__main__':
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).resolve().parent.parent))

    from assistente.excecoes import AutomacaoAbortadaPeloUsuario

    print(">>> Iniciando teste da 'parede' granular: processar_aba_geral_parte1...")
    print(">>> O teste começará em 5 segundos...")
    time.sleep(5)

    try:
        processar_aba_geral_parte1()
        print("\n--- Teste da 'parede' concluído com SUCESSO! ---")

    except AutomacaoAbortadaPeloUsuario:
        print("\n--- Teste ABORTADO pelo usuário. ---")
    except Exception as e:
        print(f"\n--- Teste da 'parede' FALHOU! Erro: {e} ---")