# funcoes/copiar_texto_elemento.py

"""Módulo para a ação de clicar em um elemento e copiar seu conteúdo."""

import pyautogui
import pyperclip
import time

# Importa nossa função de base para encontrar a âncora e seus dados.
from .localizar_elemento import localizar_elemento


def copiar_texto_elemento(
    nome_chave: str,
    ajuste_x_override: int = None,
    ajuste_y_override: int = None
) -> str:
    """Clica em um elemento e copia seu conteúdo para o clipboard.

    A função primeiro localiza a âncora, calcula a posição de clique,
    limpa o clipboard, clica (o que seleciona o texto no SAP), simula Ctrl+C,
    e então retorna o conteúdo da área de transferência.

    Args:
        nome_chave (str): A chave do elemento no JSON a ser usado como âncora.
        ajuste_x_override (int, optional): Deslocamento X que sobrescreve o JSON.
        ajuste_y_override (int, optional): Deslocamento Y que sobrescreve o JSON.

    Returns:
        str: O texto copiado da área de transferência. Retorna string vazia
             se o campo estiver vazio.

    Raises:
        Exception: Levanta qualquer exceção vinda da localização, clique ou cópia.
                   Inclui ValueError se o clipboard falhar.
    """
    # (Passos 1 a 4: Localizar âncora e calcular alvo - permanecem iguais)
    posicao_ancora, dados_elemento = localizar_elemento(nome_chave)

    if ajuste_x_override is not None:
        ajuste_x_final = ajuste_x_override
    else:
        ajuste_x_final = int(dados_elemento.get("ajuste_x") or 0)

    if ajuste_y_override is not None:
        ajuste_y_final = ajuste_y_override
    else:
        ajuste_y_final = int(dados_elemento.get("ajuste_y") or 0)

    x_alvo = posicao_ancora.x + ajuste_x_final
    y_alvo = posicao_ancora.y + ajuste_y_final

    # 5. Tenta executar a sequência de clique e cópia (com as correções).
    try:
        # CORREÇÃO 1: Limpa o clipboard ANTES de qualquer ação.
        pyperclip.copy('')
        time.sleep(0.1) # Pequena pausa para garantir a limpeza

        pyautogui.click(x_alvo, y_alvo) # Clica para focar (e selecionar no SAP)
        time.sleep(0.3)
        # CORREÇÃO 2: Linha do Ctrl+A removida.
        pyautogui.hotkey('ctrl', 'c') # Copia o texto selecionado
        time.sleep(0.3)

        texto_copiado = pyperclip.paste()
        if texto_copiado is None:
             raise ValueError("Falha ao ler o conteúdo da área de transferência após a cópia.")

        return str(texto_copiado).strip()

    except Exception as e:
        raise RuntimeError(f"Falha ao tentar copiar texto do elemento '{nome_chave}': {e}")


# --- Camada de Teste Direto ---
if __name__ == '__main__':
    """
    Bloco para testar a função 'copiar_texto_elemento' de forma isolada.
    Execute a partir da raiz: python -m funcoes.copiar_texto_elemento
    """
    print(">>> Iniciando teste da função 'copiar_texto_elemento'...")
    print(">>> Deixe a imagem âncora ('endereco_idfiscais_cnpj') visível.")
    print(">>> Certifique-se de que o campo CNPJ tenha algum valor.")
    print(">>> O teste começará em 5 segundos...")
    time.sleep(5)

    try:
        chave_teste = "endereco_idfiscais_cnpj" # Mude se necessário

        print(f"--- Tentando copiar texto do campo '{chave_teste}'...")
        texto_obtido = copiar_texto_elemento(chave_teste)
        print(f"--- Texto copiado: '{texto_obtido}'")
        print("--- Teste concluído com SUCESSO!")

    except Exception as e:
        print(f"--- Teste FALHOU! Erro: {e}")