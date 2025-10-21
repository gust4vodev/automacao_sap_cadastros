# acoes/preencher_aba_caracteristicas.py

"""
Módulo para a "parede" de ações: preenchimento da aba Características.
"""

import time

# --- Imports de Módulos do Projeto ---
from navegacao.navegacao_abas import ir_para_aba
from funcoes.pressionar_teclas import pressionar_atalho_combinado, pressionar_tecla_unica
from funcoes.clicar_com_botao_direito import clicar_com_botao_direito
from funcoes.processar_log_clipboard import obter_ultimo_usuario_do_log
from funcoes.clicar_elemento import clicar_elemento
from uteis.logica_vendedores import obter_codigo_divisao_por_usuario
from assistente.executor import executar_acao_assistida


def preencher_aba_caracteristicas():
    """(Orquestradora) Executa o fluxo completo para a Aba Características."""

    # 1. Navegar para a aba Características
    executar_acao_assistida(lambda: ir_para_aba("caracteristicas"), nome_acao="Navegar para a Aba Características")
    time.sleep(1)

    # 2. pressionar o atalho para abrir o log de modificações Alt + F + L
    executar_acao_assistida(lambda: pressionar_atalho_combinado('alt', 'f'), nome_acao="Pressionar atalho 'Alt+F'")
    time.sleep(1)
    executar_acao_assistida(lambda: pressionar_tecla_unica('l'), nome_acao="Pressionar tecla 'L' para abrir o Log")
    time.sleep(1)

    # 3. Copia tabela do log de modificações para a área de transferência e fecha janela do log.
    executar_acao_assistida(lambda: clicar_com_botao_direito("caracteristicas_logmodif", ajuste_x_override=-50, ajuste_y_override=30), nome_acao="Clicar com botão direito no log para copiar")
    time.sleep(1)
    executar_acao_assistida(lambda: pressionar_tecla_unica('t'), nome_acao="Pressionar tecla 'T' para Copiar Tudo")
    time.sleep(1)
    executar_acao_assistida(lambda: pressionar_tecla_unica('esc'), nome_acao="Pressionar tecla 'Esc' para Fechar o Log")
    time.sleep(1)

    # 4. Processar o log e obter o ultimo usuário.
    ultimo_usuario = executar_acao_assistida(obter_ultimo_usuario_do_log,nome_acao="Processar log da área de transferência")

    # 5. Definir a divisão com base no último usuário.
    codigo_divisao = obter_codigo_divisao_por_usuario(ultimo_usuario)

    # 6. Clicar na divisão correta.
    if codigo_divisao == 4: # Usuário é PET7, clica em X.
        executar_acao_assistida(lambda: clicar_elemento("caracteristicas_pet7"),nome_acao=f"Definir divisão como PET7 (Usuário: {ultimo_usuario})")
    else: # Usuário é SERILON (ou outro), clica em Y.
        executar_acao_assistida(lambda: clicar_elemento("caracteristicas_serilon"),nome_acao=f"Definir divisão como SERILON (Usuário: {ultimo_usuario})")
    time.sleep(0.5)

# --- Camada de Teste Direto ---
if __name__ == '__main__':
    """
    Bloco para testar esta "parede" de forma isolada.
    Execute-o a partir da raiz do projeto com: python -m acoes.preencher_aba_caracteristicas
    """
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).resolve().parent.parent))

    from assistente.excecoes import AutomacaoAbortadaPeloUsuario

    print(">>> Iniciando teste da 'parede': preencher_aba_caracteristicas...")
    print(">>> Testando o fluxo COMPLETO (Passos 1 a 6)...")
    print(">>> O teste começará em 5 segundos...")
    time.sleep(5)

    try:
        preencher_aba_caracteristicas()
        print("\n--- Teste da 'parede' concluído com SUCESSO! ---")

    except AutomacaoAbortadaPeloUsuario:
        print("\n--- Teste ABORTADO pelo usuário. ---")
    except Exception as e:
        print(f"\n--- Teste da 'parede' FALHOU! Erro: {e} ---")