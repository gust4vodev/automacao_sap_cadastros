# funcoes/digitar_texto.py

"""Módulo para a ação de digitar texto com flexibilidade de deslocamento."""

import pyautogui
import time

# Importa nossa função de base para encontrar a âncora.
from .localizar_elemento import localizar_elemento_por_chave


def digitar_texto(
    nome_chave: str,
    texto_a_digitar: str,
    ajuste_x: int = 0,
    ajuste_y: int = 0
):
    """Digita um texto em um campo, usando uma imagem âncora e um deslocamento.

    Args:
        nome_chave (str): A chave do elemento no JSON a ser usado como âncora.
        texto_a_digitar (str): O texto que será digitado no campo.
        ajuste_x (int, optional): Deslocamento horizontal em pixels. O padrão é 0.
        ajuste_y (int, optional): Deslocamento vertical em pixels. O padrão é 0.

    Raises:
        Exception: Levanta qualquer exceção vinda da localização ou da digitação.
    """
    # 1. Encontra a posição da âncora. Se falhar, levanta uma exceção.
    posicao_ancora = localizar_elemento_por_chave(nome_chave)

    # 2. Calcula a posição final do alvo.
    x_alvo = posicao_ancora.x + ajuste_x
    y_alvo = posicao_ancora.y + ajuste_y

    # 3. Tenta executar a ação no alvo final.
    try:
        pyautogui.click(x_alvo, y_alvo)
        time.sleep(0.5)
        pyautogui.write(str(texto_a_digitar), interval=0.05)
        time.sleep(0.5)
        pyautogui.press('tab') # Pressiona Tab após digitar, um comportamento comum.
    except Exception as e:
        # Se a ação falhar, levanta uma nova exceção com mais contexto.
        raise RuntimeError(f"Falha ao tentar digitar no elemento '{nome_chave}': {e}")


# --- CAMADA EXTRA PARA TESTE DIRETO ---
if __name__ == '__main__':
    """
    Este bloco só é executado quando o arquivo é rodado diretamente
    pelo terminal (ex: python funcoes/digitar_texto.py).
    Ele serve para testar a função 'digitar_texto' de forma isolada.
    """
    print(">>> Iniciando teste da função 'digitar_texto'...")
    print(">>> Por favor, deixe a tela do SAP visível com o campo alvo.")
    print(">>> O teste começará em 5 segundos...")
    time.sleep(5)

    try:
        # --- Exemplo de Teste ---
        # Altere os valores abaixo para corresponder ao seu teste.
        # Supondo que você tenha uma imagem âncora chamada "rotulo_nome"
        # e queira clicar 150 pixels à direita dela para digitar.

        chave_ancora_teste = "C:\\Users\\gustavo.galhaci\\Desktop\\_PROJETOS\\automacao_sap_b1\\imagens\\aba_caracteristicas.png" # Mude para a chave do seu JSON
        texto_teste = "Cliente de Teste LTDA"
        deslocamento_x_teste = 150

        print(f"--- Tentando digitar '{texto_teste}' no campo '{chave_ancora_teste}'")
        digitar_texto(
            nome_chave=chave_ancora_teste,
            texto_a_digitar=texto_teste,
            ajuste_x=deslocamento_x_teste
        )
        print("--- Teste concluído com SUCESSO!")

    except Exception as e:
        print(f"--- Teste FALHOU! Erro: {e}")