# funcoes/clicar_elemento.py

"""Módulo para a ação de clicar em um elemento com lógica de ajuste inteligente."""

import pyautogui
import time

# Importa nossa função de base para encontrar a âncora e seus dados.
from .localizar_elemento import localizar_elemento


def clicar_elemento(nome_chave: str, ajuste_x_override: int = None, ajuste_y_override: int = None):
    """
    Clica em um elemento, aplicando uma lógica de ajuste flexível.

    A função primeiro localiza a âncora. Em seguida, decide qual ajuste
    usar, com a seguinte prioridade:
    1. O ajuste de override passado diretamente para a função.
    2. O ajuste padrão definido no arquivo parametros.json.
    3. Zero, se nenhum dos anteriores for especificado.

    Args:
        nome_chave (str): A chave do elemento no JSON a ser usado como âncora.
        ajuste_x_override (int, optional): Um deslocamento X que sobrescreve
                                           qualquer valor do JSON.
        ajuste_y_override (int, optional): Um deslocamento Y que sobrescreve
                                           qualquer valor do JSON.

    Raises:
        Exception: Levanta qualquer exceção vinda da localização do elemento
                   ou da própria ação de clique, para ser capturada pelo Assistente executor.
    """
    # 1. Encontra a âncora e seus dados. Se falhar, levanta uma exceção.
    posicao_ancora, dados_elemento = localizar_elemento(nome_chave)

    # 2. Lógica inteligente para decidir o ajuste final em X.
    if ajuste_x_override is not None:
        ajuste_x_final = ajuste_x_override
    else:
        # Tenta pegar o valor do JSON, convertendo para int. Usa 0 se estiver vazio ou ausente.
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
    except Exception as e:
        raise RuntimeError(f"Falha ao tentar clicar no elemento '{nome_chave}': {e}")


# --- Camada de Teste Direto ---
if __name__ == '__main__':
    """
    Bloco para testar a função 'clicar_elemento' de forma isolada.
    Execute-o a partir da raiz do projeto com: python -m funcoes.clicar_elemento
    """
    print(">>> Iniciando teste da função 'clicar_elemento'...")
    print(">>> Deixe a imagem alvo visível na tela.")
    print(">>> O teste começará em 5 segundos...")
    time.sleep(5)

    try:
        # --- Exemplo de Teste ---
        chave_teste = "aba_caracteristicas"

        print(f"--- Tentando clicar no elemento '{chave_teste}'...")
        clicar_elemento(chave_teste)
        print("--- Teste concluído com SUCESSO!")

    except Exception as e:
        print(f"--- Teste FALHOU! Erro: {e}")