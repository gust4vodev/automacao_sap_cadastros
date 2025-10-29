# funcoes/rolar_mouse.py

"""Módulo para a ação de rolar (scroll) o mouse várias vezes."""

import pyautogui
import time

def rolar_mouse_linhas(numero_de_linhas: int, direcao: str = 'baixo'):
    """
     Executa rolagens da roda do mouse para simular a rolagem de linhas na tela.

    A função utiliza a roda do mouse para rolar o conteúdo exibido, permitindo simular
    movimentos de scroll controlados em uma direção específica.

    Args:
        numero_de_linhas (int): Número de linhas a rolar.
        direcao (str, optional): Direção da rolagem, podendo ser 'cima' ou 'baixo'.
                                 O padrão é 'baixo'.

    Raises:
        ValueError: Se a direção informada não for 'cima' nem 'baixo'.
        RuntimeError: Se ocorrer uma falha ao executar a ação com o PyAutoGUI.
    """

    # 1. Verifica a direção da rolagem e define o valor do clique da roda.
    if direcao == 'baixo': # PyAutoGUI usa valor negativo para rolar para baixo.
        clique_por_linha = -100

    elif direcao == 'cima': # PyAutoGUI usa valor positivo para rolar para cima.
        clique_por_linha = 100

    # 2. Levanta erro se a direção informada não for 'cima' ou 'baixo'.
    else:
        raise ValueError("Direção da rolagem inválida. Use 'cima' ou 'baixo'.")

    # 3. Itera pelo número absoluto de linhas, garantindo funcionamento com valores negativos.
    try:
        for _ in range(abs(numero_de_linhas)):
            pyautogui.scroll(clique_por_linha)

    # 4. Executa uma rolagem por vez com pyautogui.scroll() e pausa de 0.30s entre cada uma.
            time.sleep(0.30)

    # 5. Captura exceções do PyAutoGUI e relança como RuntimeError com mensagem clara.
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