# funcoes/clicar_com_botao_direito.py

"""Módulo para a ação de clicar com o botão direito do mouse."""

import pyautogui
import time

# Importa nossa função de base para encontrar a âncora e seus dados.
from .localizar_elemento import localizar_elemento


def clicar_com_botao_direito(nome_chave: str, ajuste_x_override: int = None, ajuste_y_override: int = None):
    """
    Clica com o BOTÃO DIREITO em um elemento, usando uma âncora e lógica de ajuste.

    A função primeiro localiza a âncora e então decide qual ajuste
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
                   ou da própria ação de clique.
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
        # AQUI ESTÁ A DIFERENÇA: Usa pyautogui.rightClick()
        pyautogui.rightClick(x_alvo, y_alvo)
    except Exception as e:
        raise RuntimeError(f"Falha ao tentar clicar com botão direito no elemento '{nome_chave}': {e}")


# --- Camada de Teste Direto ---
if __name__ == '__main__':
    """
    Bloco para testar a função 'clicar_com_botao_direito' de forma isolada.
    Execute-o a partir da raiz do projeto com: python -m funcoes.clicar_com_botao_direito
    """
    print(">>> Iniciando teste da função 'clicar_com_botao_direito'...")
    print(">>> Deixe a imagem âncora ('caracteristicas_logmodif') visível.")
    print(">>> O teste começará em 5 segundos...")
    time.sleep(5)

    try:
        # --- Teste com os dados fornecidos ---
        # Você mencionou que precisamos testar o ponto exato de clique.
        # Comece com ajustes pequenos e vá aumentando.
        chave_teste = "caracteristicas_logmodif"
        ajuste_x_teste = -50  # Mude aqui para testar (para direita)
        ajuste_y_teste = 30  # Mude aqui para testar (para baixo)

        print(f"--- Tentando clicar com botão direito em '{chave_teste}' com ajuste X={ajuste_x_teste}, Y={ajuste_y_teste}...")
        clicar_com_botao_direito(chave_teste, ajuste_x_teste, ajuste_y_teste)
        print("--- Teste concluído com SUCESSO!")

    except Exception as e:
        print(f"--- Teste FALHOU! Erro: {e}")