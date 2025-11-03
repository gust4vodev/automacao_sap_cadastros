# funcoes/selecionar_dropdown.py

"""Módulo para a ação de selecionar um valor em um dropdown."""

import pyautogui
import time

# Importa nossa função de base para encontrar a âncora e seus dados.
from .localizar_elemento import localizar_elemento


def selecionar_dropdown(nome_chave: str, valor_a_selecionar: str, ajuste_x_override: int = None, ajuste_y_override: int = None):
    """
    Seleciona um valor em um dropdown usando uma âncora e lógica de ajuste.

    A função localiza uma imagem que serve como âncora e, a partir dela, determina
    qual ajuste aplicar (os ajustes são coordenadas X e Y somadas às coordenadas
    da imagem). A prioridade para definir o ajuste é a seguinte:

    1. O ajuste de override passado diretamente para a função.
    2. O ajuste padrão definido no arquivo parametros.json.
    3. Zero, se nenhum dos anteriores for especificado.

    Args:
        nome_chave (str): Chave do elemento no JSON usada como referência de âncora.
        valor_a_selecionar (str): Texto que será digitado para selecionar a opção desejada.
        ajuste_x_override (int, optional): Deslocamento em X que sobrescreve qualquer valor do JSON.
        ajuste_y_override (int, optional): Deslocamento em Y que sobrescreve qualquer valor do JSON.

    Raises:
        Exception: Propaga exceções originadas da localização do elemento
                   ou da interação com o dropdown.
    """

    # 1. Encontra a âncora e seus dados. Se falhar, levanta uma exceção.
    posicao_ancora, dados_elemento = localizar_elemento(nome_chave)

    # 2. Lógica inteligente para decidir o ajuste final em X.
    if ajuste_x_override is not None:
        ajuste_x_final = ajuste_x_override
    else:
        ajuste_x_final = int(dados_elemento.get("ajuste_x") or 0)

    # 3. Lógica inteligente para decidir o ajuste final em Y.
    if ajuste_y_override is not None:
        ajuste_y_final = ajuste_y_override
    else:
        ajuste_y_final = int(dados_elemento.get("ajuste_y") or 0)

    # 4. Calcula a posição final do alvo (o clique para abrir o dropdown).
    x_alvo = posicao_ancora.x + ajuste_x_final
    y_alvo = posicao_ancora.y + ajuste_y_final

    # 5. Tenta executar a sequência de ações no alvo final.
    try:
        pyautogui.click(x_alvo, y_alvo)
        time.sleep(0.8) # Pausa um pouco maior para o dropdown abrir.
        pyautogui.write(str(valor_a_selecionar), interval=0.05)
        time.sleep(0.5)
        pyautogui.press('enter') # Enter para confirmar a seleção.
    except Exception as e:
        raise RuntimeError(f"Falha ao interagir com o dropdown '{nome_chave}': {e}")


# --- Camada de Teste Direto ---
if __name__ == '__main__':
    """
    Bloco para testar a função 'selecionar_dropdown' de forma isolada.
    Execute-o a partir da raiz do projeto com: python -m funcoes.selecionar_dropdown
    """
    print(">>> Iniciando teste da função 'selecionar_dropdown'...")
    print(">>> Deixe a imagem âncora ('geral1_tipopn.png') visível na tela.")
    print(">>> O teste começará em 5 segundos...")
    time.sleep(5)

    try:
        # --- Teste ---
        chave_teste = "geral1_tipopn.png"
        valor_teste = "Cliente"

        print(f"--- Tentando selecionar '{valor_teste}' no dropdown '{chave_teste}'...")
        selecionar_dropdown(chave_teste, valor_teste)
        print("--- Teste concluído com SUCESSO!")

    except Exception as e:
        print(f"--- Teste FALHOU! Erro: {e}")