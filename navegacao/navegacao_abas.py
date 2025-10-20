# navegacao/navegacao_abas.py

"""Módulo central e genérico para navegação entre abas do SAP."""

import time

# Importa a nossa ferramenta de baixo nível para clicar.
from funcoes.clicar_elemento import clicar_elemento
# Importa o motor executor.
from assistente.executor import executar_acao_assistida


def ir_para_aba(nome_da_aba: str):
    """Navega para qualquer aba especificada, clicando em seu ícone.

    Esta função constrói a chave do elemento dinamicamente (ex: 'aba_geral')
    e passa a ação de clique para o motor de execução assistida.

    Args:
        nome_da_aba (str): O nome da aba para a qual navegar (ex: 'geral', 'socios').
    """
    # Constrói o nome da chave do JSON dinamicamente, seguindo nosso padrão.
    chave_da_aba = f"aba_{nome_da_aba}"

    # A docstring da ação será a própria chave, tornando o log do motor claro.
    executar_acao_assistida(
        lambda: clicar_elemento(chave_da_aba),
        nome_acao=f"Navegar para a aba '{nome_da_aba.capitalize()}'"
    )
    time.sleep(1) # Pausa de segurança para a aba renderizar.


# --- Camada de Teste Direto ---
if __name__ == '__main__':
    """
    Bloco para testar a função genérica de navegação.
    Execute-o a partir da raiz do projeto com: python -m navegacao.navegacao_abas
    """
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).resolve().parent.parent))

    from assistente.excecoes import AutomacaoAbortadaPeloUsuario

    print(">>> Iniciando teste de navegação genérica...")
    print(">>> O teste tentará navegar para a aba 'geral'.")
    print(">>> Deixe a imagem da aba visível na tela.")
    print(">>> O teste começará em 5 segundos...")
    time.sleep(5)

    try:
        # Testamos a função genérica chamando-a com o nome da aba desejada.
        ir_para_aba("geral")
        print("\n--- Teste de navegação concluído com SUCESSO! ---")

        print("\n>>> Testando agora a aba 'caracteristicas' em 3 segundos...")
        time.sleep(3)
        ir_para_aba("caracteristicas")
        print("\n--- Teste de navegação concluído com SUCESSO! ---")


    except AutomacaoAbortadaPeloUsuario:
        print("\n--- Teste ABORTADO pelo usuário. ---")
    except Exception as e:
        print(f"\n--- Teste de navegação FALHOU! Erro: {e} ---")