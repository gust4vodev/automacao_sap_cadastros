# funcoes/pressionar_teclas.py

"""Módulo para ações de teclado (atalhos e teclas únicas)."""
import pyautogui
import time

# 1. Define a função pressionar_atalho_combinado que aceita múltiplas teclas como argumentos variáveis.
def pressionar_atalho_combinado(*teclas: str):
    """
    Pressiona uma combinação de teclas simultaneamente (por exemplo, Ctrl+F).

    A função utiliza o PyAutoGUI para acionar atalhos compostos, enviando
    todas as teclas informadas em conjunto.

    Args:
        *teclas (str): Sequência de teclas a serem pressionadas simultaneamente.
                       Exemplo: 'ctrl', 'f'.

    Raises:
        RuntimeError: Se ocorrer falha ao executar o atalho via PyAutoGUI.
    """

# 2. Usa pyautogui.hotkey() para pressionar todas as teclas simultaneamente (ex: Ctrl + F).
    try:
        pyautogui.hotkey(*teclas)

# 3. Captura qualquer exceção do PyAutoGUI e relança como RuntimeError com mensagem clara incluindo as teclas.
    except Exception as e:
        raise RuntimeError(f"Falha ao pressionar o atalho '{teclas}': {e}")
    
#=========================================================================================================

# 1. Define a função pressionar_tecla_unica que aceita uma única tecla como string.
def pressionar_tecla_unica(tecla: str):
    """  Pressiona uma única tecla (por exemplo, 'L', 'enter' ou 'tab').

    A função envia um único comando de tecla através do PyAutoGUI, simulando
    uma digitação simples.

    Args:
        tecla (str): Nome da tecla a ser pressionada.

    Raises:
        RuntimeError: Se ocorrer falha ao pressionar a tecla via PyAutoGUI.
    """

# 2. Usa pyautogui.press() para simular o pressionamento de uma tecla individual.
    try:
        pyautogui.press(tecla)

# 3. Captura exceções do PyAutoGUI e relança como RuntimeError com a tecla envolvida na falha.
    except Exception as e:
        raise RuntimeError(f"Falha ao pressionar a tecla '{tecla}': {e}")


# --- Camada de Teste Direto ---
if __name__ == '__main__':
    """
    Bloco para testar as funções de teclado de forma isolada.
    Execute-o a partir da raiz do projeto com: python -m funcoes.pressionar_teclas
    """
    print(">>> Iniciando teste das funções de teclado...")
    print(">>> ATENÇÃO: O teste simulará pressionamentos de teclas.")
    print(">>> Abra um editor de texto (Bloco de Notas) para ver o resultado.")
    print(">>> O teste começará em 5 segundos...")
    time.sleep(5)

    try:
        print("--- Testando: pressionar_atalho_combinado('shift', 'tab')")
        pressionar_atalho_combinado('shift', 'tab')
        time.sleep(1)

        #print("--- Testando: pressionar_tecla_unica('l')")
        #pressionar_tecla_unica('l')
        #print("--- Teste concluído com SUCESSO!")

    except Exception as e:
        print(f"--- Teste FALHOU! Erro: {e}")