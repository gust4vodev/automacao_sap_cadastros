# funcoes/processar_log_clipboard.py

"""Módulo para ler e processar a tabela de log da área de transferência."""

import pyperclip
import pandas as pd
import io
import time

def obter_ultimo_usuario_do_log() -> str:
    """
    Lê a tabela de log copiada para a área de transferência e retorna o último usuário registrado.

    A função obtém os dados da área de transferência (esperados no formato tabulado por TABS),
    processa-os com pandas, identifica a última linha do log e extrai o valor da coluna
    'Atualizado por - Código do usuário', retornando-o como string.

    Returns:
        str: Código do usuário responsável pela última atualização registrada no log.

    Raises:
        ValueError: Se a área de transferência estiver vazia ou o conteúdo for inválido.
        KeyError: Se a coluna 'Atualizado por - Código do usuário' não estiver presente no log.
        RuntimeError: Se ocorrer qualquer erro durante o processamento com pandas.
    """

    # 1. Lê o conteúdo da área de transferência usando pyperclip.
    try:
        dados_clipboard = pyperclip.paste()

    # 2. Verifica se o clipboard está vazio e levanta erro se não houver dados.
        if not dados_clipboard:
            raise ValueError("A área de transferência está vazia. Não há log para processar.")
        
    # 3. Usa io.StringIO para tratar a string do clipboard como um arquivo CSV com separador de tabulação (\t).
        df = pd.read_csv(io.StringIO(dados_clipboard), sep='\t')

    # 4. Verifica se o DataFrame gerado está vazio e levanta erro se não houver linhas válidas.
        if df.empty:
            raise ValueError("Os dados do log no clipboard estão vazios ou em formato inválido.")

    # 5. Obtém a última linha do log com iloc[-1].
        ultima_modificacao = df.iloc[-1]

    # 6. Extrai o valor da coluna específica 'Atualizado por - Código do usuário'.
        nome_usuario = ultima_modificacao['Atualizado por - Código do usuário']

    # 7. Converte o valor para string, remove espaços extras e retorna.
        return str(nome_usuario).strip()

    # 8. Captura KeyError se a coluna não existir e relança com mensagem clara.
    except KeyError:
        raise KeyError("A coluna 'Atualizado por - Código do usuário' não foi encontrada no log.")
    
    # 9. Captura qualquer outra exceção e relança como RuntimeError com detalhes do erro.
    except Exception as e:
        raise RuntimeError(f"Falha ao processar o log do clipboard: {e}")


# --- Camada de Teste Direto ---
if __name__ == '__main__':
    """
    Bloco para testar a função de processamento de log.
    Execute-o a partir da raiz do projeto com: python -m funcoes.processar_log_clipboard
    """
    print(">>> Iniciando teste da função 'obter_ultimo_usuario_do_log'...")

    # --- SIMULAÇÃO DE DADOS NO CLIPBOARD (PARA TESTE) ---
    # Para um teste 100% automático, podemos injetar dados ficticios no clipboard.

    dados_falsos = (
        "Instância\tCódigo do objeto\tAtualizado\tAtualizado por - Código do usuário\tAtualizado por - Nome do usuário\n"
        "1\tC056202\t20/10/2025\tJONATHAN.FREITAS\tJONATHAN EDUARDO FREITAS\n"
        "2\tC056202\t20/10/2025\tTESTE_USUARIO_FINAL\tTESTE USUARIO FINAL"
    )
    pyperclip.copy(dados_falsos)
    time.sleep(3)

    try:
        ultimo_usuario = obter_ultimo_usuario_do_log()
        print(f"\n--- Teste concluído com SUCESSO! ---")
        print(f"--- Último usuário encontrado: {ultimo_usuario}")

    except Exception as e:
        print(f"\n--- Teste FALHOU! Erro: {e} ---")