# funcoes/colar_texto.py

"""Módulo para a ação de colar texto com lógica de ajuste inteligente."""

import pyautogui
import pyperclip
import time

# Importa nossa função de base para encontrar a âncora e seus dados.
from .localizar_elemento import localizar_elemento


def colar_texto(nome_chave: str, texto_a_colar: str, ajuste_x_override: int = None, ajuste_y_override: int = None):
    """
    Cola um texto em um campo, usando uma âncora e lógica de ajuste.

    A função primeiro localiza a âncora e então decide qual ajuste
    usar, com a seguinte prioridade:
    1. O ajuste de override passado diretamente para a função.
    2. O ajuste padrão definido no arquivo parametros.json.
    3. Zero, se nenhum dos anteriores for especificado.

    Args:
        nome_chave (str): A chave do elemento no JSON a ser usado como âncora.
        texto_a_colar (str): O texto que será colado no campo.
        ajuste_x_override (int, optional): Um deslocamento X que sobrescreve
                                           qualquer valor do JSON.
        ajuste_y_override (int, optional): Um deslocamento Y que sobrescreve
                                           qualquer valor do JSON.

    Raises:
        Exception: Levanta qualquer exceção vinda da localização do elemento
                   ou da própria ação de colar.
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

    # 4. Calcula a posição final do alvo.
    x_alvo = posicao_ancora.x + ajuste_x_final
    y_alvo = posicao_ancora.y + ajuste_y_final

    # 5. Tenta executar a ação no alvo final.
    try:
        pyautogui.click(x_alvo, y_alvo)
        time.sleep(0.5)
        # Limpa o campo antes de colar
        pyautogui.press('backspace')

        # Ação de colar
        pyperclip.copy(str(texto_a_colar))
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)
        pyautogui.press('tab') # Pressiona Tab para confirmar a entrada.
    except Exception as e:
        raise RuntimeError(f"Falha ao tentar colar no elemento '{nome_chave}': {e}")


# --- Camada de Teste Direto ---
if __name__ == '__main__':
    """
    Bloco para testar a função 'colar_texto' de forma isolada.
    Execute-o a partir da raiz do projeto com: python -m funcoes.colar_texto
    """
    print(">>> Iniciando teste da função 'colar_texto'...")
    print(">>> Deixe a imagem âncora ('geral3_codigo') visível na tela.")
    print(">>> O teste começará em 5 segundos...")
    time.sleep(5)

    try:
        # --- Teste ---
        chave_teste = "geral3_codigo"
        valor_teste = "0123456789"

        print(f"--- Tentando colar '{valor_teste}' no campo relativo a '{chave_teste}'...")
        colar_texto(chave_teste, valor_teste)
        print("--- Teste concluído com SUCESSO!")

    except Exception as e:
        print(f"--- Teste FALHOU! Erro: {e}")