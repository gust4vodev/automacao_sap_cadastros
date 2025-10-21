# funcoes/pressionar_teclas.py

"""Módulo para ações de teclado (atalhos e teclas únicas)."""

import pyautogui
import time

def pressionar_atalho_combinado(*teclas: str):
    """Pressiona uma combinação de teclas simultaneamente (ex: Ctrl+F).

    Args:
        *teclas (str): As teclas a serem pressionadas em conjunto.
                       Ex: 'ctrl', 'f'

    Raises:
        RuntimeError: Se a ação do PyAutoGUI falhar.
    """
    try:
        pyautogui.hotkey(*teclas)
    except Exception as e:
        raise RuntimeError(f"Falha ao pressionar o atalho '{teclas}': {e}")


def pressionar_tecla_unica(tecla: str):
    """Pressiona uma única tecla (ex: 'L', 'enter', 'tab').

    Args:
        tecla (str): A tecla a ser pressionada.

    Raises:
        RuntimeError: Se a ação do PyAutoGUI falhar.
    """
    try:
        pyautogui.press(tecla)
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
        print("--- Testando: pressionar_atalho_combinado('alt', 'f')")
        pressionar_atalho_combinado('alt', 'f')
        time.sleep(1)

        print("--- Testando: pressionar_tecla_unica('l')")
        pressionar_tecla_unica('l')
        print("--- Teste concluído com SUCESSO!")

    except Exception as e:
        print(f"--- Teste FALHOU! Erro: {e}")