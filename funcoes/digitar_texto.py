# funcoes/digitar_texto.py

"""Módulo para a ação de digitar texto com lógica de ajuste inteligente."""

import pyautogui
import time

# Importa nossa função de base para encontrar a âncora e seus dados.
from .localizar_elemento import localizar_elemento


def digitar_texto(nome_chave: str, texto_a_digitar: str, ajuste_x_override: int = None, ajuste_y_override: int = None):
    """
    Digita um texto em um campo na tela utilizando uma âncora e lógica de ajuste inteligente.

    A função localiza a âncora definida no arquivo `parametros.json`, calcula a posição exata
    onde o texto deve ser inserido aplicando ajustes em X e Y, e executa a digitação por meio
    do PyAutoGUI. Os ajustes são determinados com a seguinte prioridade:

    1. O ajuste de override passado diretamente à função.
    2. O ajuste padrão definido no `parametros.json`.
    3. Zero, se nenhum dos anteriores for especificado.

    Args:
        nome_chave (str): Chave do elemento no arquivo `parametros.json` usada como âncora.
        texto_a_digitar (str): Texto que será digitado no campo alvo.
        ajuste_x_override (int, optional): Deslocamento em X que sobrescreve o valor do JSON.
        ajuste_y_override (int, optional): Deslocamento em Y que sobrescreve o valor do JSON.

    Raises:
        RuntimeError: Se ocorrer falha ao localizar o elemento ou ao executar a digitação.
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
        pyautogui.write(str(texto_a_digitar), interval=0.05)
        time.sleep(0.5)
        pyautogui.press('tab') # Pressiona Tab para confirmar a entrada.
    except Exception as e:
        raise RuntimeError(f"Falha ao tentar digitar no elemento '{nome_chave}': {e}")


# --- Camada de Teste Direto ---
if __name__ == '__main__':
    """
    Bloco para testar a função 'digitar_texto' de forma isolada.
    Execute-o a partir da raiz do projeto com: python -m funcoes.digitar_texto
    """
    print(">>> Iniciando teste da função 'digitar_texto'...")
    print(">>> Deixe a imagem âncora ('geral3_codigo') visível na tela.")
    print(">>> O teste começará em 5 segundos...")
    time.sleep(5)

    try:
        # --- Teste com os dados fornecidos ---
        chave_teste = "geral3_codigo"
        valor_teste = "0123456789"

        print(f"--- Tentando digitar '{valor_teste}' no campo relativo a '{chave_teste}'...")
        digitar_texto(chave_teste, valor_teste)
        print("--- Teste concluído com SUCESSO!")

    except Exception as e:
        print(f"--- Teste FALHOU! Erro: {e}")