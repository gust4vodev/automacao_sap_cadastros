# funcoes/rolar_mouse.py

"""Módulo para a ação de rolar (scroll) o mouse várias vezes."""

import pyautogui
import time

def rolar_mouse_linhas(numero_de_linhas: int, direcao: str = 'baixo'):
    """
    Executa rolagens da roda do mouse para simular a rolagem de linhas.

    Args:
        numero_de_linhas (int): Quantas linhas rolar.
        direcao (str, optional): A direção da rolagem ('cima' ou 'baixo').
                                 O padrão é 'baixo'.

    Raises:
        ValueError: Se a direção for inválida.
        RuntimeError: Se a ação do PyAutoGUI falhar.
    """
    if direcao == 'baixo':
        # PyAutoGUI usa valor negativo para rolar para baixo.
        # O valor '-1' simula um "clique" da roda.
        clique_por_linha = -1
    elif direcao == 'cima':
        clique_por_linha = 1
    else:
        raise ValueError("Direção da rolagem inválida. Use 'cima' ou 'baixo'.")

    try:
        # Executa o scroll N vezes, uma linha de cada vez.
        for _ in range(abs(numero_de_linhas)): # abs() garante que funcione mesmo se passar número negativo
            pyautogui.scroll(clique_por_linha)
            # Pequena pausa entre cada rolagem para o sistema processar.
            # Ajuste este valor se necessário.
            time.sleep(0.05)
    except Exception as e:
        raise RuntimeError(f"Falha ao tentar rolar o mouse: {e}")


# --- Camada de Teste Direto ---
if __name__ == '__main__':
    """
    Bloco para testar a função 'rolar_mouse_linhas'.
    Execute-o a partir da raiz do projeto com: python -m funcoes.rolar_mouse
    """
    print(">>> Iniciando teste da função 'rolar_mouse_linhas'...")
    print(">>> ATENÇÃO: O teste irá rolar a tela ativa.")
    print(">>> Abra uma página web ou editor de texto para ver o resultado.")
    print(">>> O teste começará em 5 segundos...")
    time.sleep(5)

    try:
        # Simula rolar 5 linhas para baixo
        linhas_teste_baixo = 5

        print(f"--- Testando rolagem para BAIXO ({linhas_teste_baixo} linhas)...")
        rolar_mouse_linhas(linhas_teste_baixo, direcao='baixo')
        print("--- Rolagem para baixo concluída.")

        time.sleep(2)

        # Simula rolar 3 linhas para cima
        linhas_teste_cima = 3
        print(f"--- Testando rolagem para CIMA ({linhas_teste_cima} linhas)...")
        rolar_mouse_linhas(linhas_teste_cima, direcao='cima')
        print("--- Rolagem para cima concluída.")

        print("\n--- Teste concluído com SUCESSO! ---")

    except Exception as e:
        print(f"\n--- Teste FALHOU! Erro: {e} ---")