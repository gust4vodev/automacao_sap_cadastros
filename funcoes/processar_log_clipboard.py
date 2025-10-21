# funcoes/processar_log_clipboard.py

"""Módulo para ler e processar a tabela de log da área de transferência."""

import pyperclip
import pandas as pd
import io
import time

def obter_ultimo_usuario_do_log() -> str:
    """Obtém a tabela da área de transferência e retorna o último usuário.

    Esta função lê a tabela copiada (que está em formato de abas),
    a processa usando pandas, encontra a última linha e retorna o
    'Código do usuário' que fez a última atualização.

    Returns:
        str: O 'Atualizado por - Código do usuário' da última entrada do log.

    Raises:
        ValueError: Se a área de transferência estiver vazia ou o log for inválido.
        RuntimeError: Se houver um erro no processamento com pandas.
        KeyError: Se a coluna esperada não for encontrada no log.
    """
    try:
        dados_clipboard = pyperclip.paste()
        if not dados_clipboard:
            raise ValueError("A área de transferência está vazia. Não há log para processar.")

        # 'io.StringIO' permite que o pandas leia uma string como se fosse um arquivo.
        # 'sep=\t' informa ao pandas que as colunas são separadas por TABS.
        df = pd.read_csv(io.StringIO(dados_clipboard), sep='\t')

        if df.empty:
            raise ValueError("Os dados do log no clipboard estão vazios ou em formato inválido.")

        # Pega a última linha do log. O pandas 'iloc[-1]' faz isso.
        ultima_modificacao = df.iloc[-1]

        # Pega o valor da coluna 'Atualizado por - Código do usuário'.
        # O nome da coluna deve ser exato, como no exemplo que você forneceu.
        nome_usuario = ultima_modificacao['Atualizado por - Código do usuário']

        return str(nome_usuario).strip()

    except KeyError:
        # Este erro ocorre se a coluna esperada não for encontrada.
        raise KeyError("A coluna 'Atualizado por - Código do usuário' não foi encontrada no log.")
    except Exception as e:
        # Captura outros erros (ex: falha no pandas) e os relança.
        raise RuntimeError(f"Falha ao processar o log do clipboard: {e}")


# --- Camada de Teste Direto ---
if __name__ == '__main__':
    """
    Bloco para testar a função de processamento de log.
    Execute-o a partir da raiz do projeto com: python -m funcoes.processar_log_clipboard
    """
    print(">>> Iniciando teste da função 'obter_ultimo_usuario_do_log'...")

    # --- SIMULAÇÃO DE DADOS NO CLIPBOARD (PARA TESTE) ---
    # Para um teste 100% automático, podemos injetar dados falsos no clipboard.
    # Basta descomentar as 6 linhas abaixo.

    # dados_falsos = (
    #     "Instância\tCódigo do objeto\tAtualizado\tAtualizado por - Código do usuário\tAtualizado por - Nome do usuário\n"
    #     "1\tC056202\t20/10/2025\tJONATHAN.FREITAS\tJONATHAN EDUARDO FREITAS\n"
    #     "2\tC056202\t20/10/2025\tTESTE_USUARIO_FINAL\tTESTE USUARIO FINAL"
    # )
    # pyperclip.copy(dados_falsos)
    # print(">>> (Dados de teste 'TESTE_USUARIO_FINAL' foram injetados no clipboard.)")

    print(">>> Lendo dados REAIS do clipboard em 3 segundos...")
    print(">>> (Para testar com dados reais, copie a tabela do SAP agora!)")
    time.sleep(3)

    try:
        ultimo_usuario = obter_ultimo_usuario_do_log()
        print(f"\n--- Teste concluído com SUCESSO! ---")
        print(f"--- Último usuário encontrado: {ultimo_usuario}")

    except Exception as e:
        print(f"\n--- Teste FALHOU! Erro: {e} ---")