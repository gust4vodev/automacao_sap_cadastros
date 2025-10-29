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
    """
    Clica em um elemento na tela e copia seu conteúdo para a área de transferência.

    A função localiza a âncora definida no arquivo `parametros.json`, calcula a posição exata
    de clique aplicando ajustes em X e Y, limpa o clipboard, executa o clique e envia o atalho
    Ctrl+C para copiar o texto do campo. O conteúdo copiado é então retornado como string.

    Args:
        nome_chave (str): Chave do elemento no arquivo `parametros.json` usada como âncora.
        ajuste_x_override (int, optional): Deslocamento em X que sobrescreve o valor do JSON.
        ajuste_y_override (int, optional): Deslocamento em Y que sobrescreve o valor do JSON.

    Returns:
        str: Texto copiado da área de transferência. Retorna uma string vazia se o campo estiver vazio.

    Raises:
        RuntimeError: Se ocorrer falha ao localizar o elemento, clicar ou copiar o texto.
        ValueError: Se houver erro ao acessar o conteúdo da área de transferência.
    """
    # 1. Localiza a âncora na tela e obtém seus dados do JSON via `localizar_elemento`.  
    posicao_ancora, dados_elemento = localizar_elemento(nome_chave)

    # 2. Define o ajuste final em X: usa override se fornecido, senão pega do JSON ou zero.
    if ajuste_x_override is not None:
        ajuste_x_final = ajuste_x_override
    else:
        ajuste_x_final = int(dados_elemento.get("ajuste_x") or 0)

    # 3. Define o ajuste final em Y: usa override se fornecido, senão pega do JSON ou zero.  
    if ajuste_y_override is not None:
        ajuste_y_final = ajuste_y_override
    else:
        ajuste_y_final = int(dados_elemento.get("ajuste_y") or 0)

    # 4. Calcula a posição final do clique com base na âncora e nos ajustes determinados.
    x_alvo = posicao_ancora.x + ajuste_x_final
    y_alvo = posicao_ancora.y + ajuste_y_final

    # 5. Limpa a área de transferência com `pyperclip.copy('')` antes de qualquer ação.  
    try:
        pyperclip.copy('')
        time.sleep(0.1)

    # 6. Clica no campo para focar e selecionar o conteúdo (comportamento SAP).
        pyautogui.click(x_alvo, y_alvo)
        time.sleep(0.3)

    # 7. Executa Ctrl+C para copiar o texto selecionado.
        pyautogui.hotkey('ctrl', 'c') # Copia o texto selecionado
        time.sleep(0.3)
    
    # 8. Lê o conteúdo do clipboard com `pyperclip.paste()`.
        texto_copiado = pyperclip.paste()

    # 9. Levanta erro se o clipboard estiver vazio ou inacessível.  
        if texto_copiado is None:
             raise ValueError("Falha ao ler o conteúdo da área de transferência após a cópia.")

    # 10. Retorna o texto copiado, removendo espaços extras. 
        return str(texto_copiado).strip()
    
    # 11. Captura exceções e relança como `RuntimeError` com contexto.  
    except Exception as e:
        raise RuntimeError(f"Falha ao tentar copiar texto do elemento '{nome_chave}': {e}")


# --- Camada de Teste Direto ---
if __name__ == '__main__':
    """
    Bloco para testar a função 'copiar_texto_elemento' de forma isolada.
    Execute a partir da raiz: python -m funcoes.copiar_texto_elemento
    """
    print(">>> Iniciando teste da função 'copiar_texto_elemento'...")
    print(">>> Deixe a imagem âncora ('geral3_telefone') visível.")
    print(">>> Certifique-se de que o campo CNPJ tenha algum valor.")
    print(">>> O teste começará em 5 segundos...")
    time.sleep(5)

    try:
        chave_teste = "geral3_telefone"

        print(f"--- Tentando copiar texto do campo '{chave_teste}'...")
        texto_obtido = copiar_texto_elemento(chave_teste)
        print(f"--- Texto copiado: '{texto_obtido}'")
        print("--- Teste concluído com SUCESSO!")

    except Exception as e:
        print(f"--- Teste FALHOU! Erro: {e}")