# uteis/processador_tabela_clipboard.py

"""
Módulo para ler e processar dados tabulados da área de transferência
usando a biblioteca pandas.
"""

import pyperclip
import pandas as pd
import io # Para ler string como arquivo
import time

def ler_tabela_clipboard_para_dataframe() -> pd.DataFrame:
    """
    Lê o conteúdo da área de transferência, assumindo que é uma tabela
    separada por tabulações (TABs), e a retorna como um DataFrame pandas.

    Returns:
        pd.DataFrame: Um DataFrame contendo os dados da tabela. As colunas serão nomeadas com base na primeira linha do clipboard.
    Raises:
        ValueError: Se a área de transferência estiver vazia ou os dados não puderem ser lidos como uma tabela tabulada.
        Exception: Para outros erros inesperados durante o processamento.
    """
    try:
        dados_clipboard = pyperclip.paste()
        if not dados_clipboard:
            raise ValueError("A área de transferência está vazia. Não há tabela para processar.")

        # Usa io.StringIO para que o pandas leia a string como se fosse um arquivo.
        # 'sep=\t' indica que o separador de colunas é TAB.
        # 'header=0' usa a primeira linha como cabeçalho (nomes das colunas).
        dataframe = pd.read_csv(io.StringIO(dados_clipboard), sep='\t', header=0)

        if dataframe.empty:
            raise ValueError("Os dados no clipboard estão vazios ou não formam uma tabela válida.")

        print("   - Tabela lida do clipboard com sucesso.")
        return dataframe

    except Exception as e:
        # Captura erros do pandas ou outros e os relança com contexto.
        raise RuntimeError(f"Falha ao ler ou processar a tabela do clipboard: {e}")

def converter_dataframe_para_string_tabulada(dataframe: pd.DataFrame) -> str:
    """
    Converte um DataFrame pandas em uma string formatada com TABs
    entre as colunas e newlines entre as linhas, incluindo o cabeçalho.

    Args:
        dataframe (pd.DataFrame): O DataFrame a ser convertido.

    Returns:
        str: A string formatada representando a tabela.

    Raises:
        TypeError: Se a entrada não for um DataFrame pandas.
        Exception: Para outros erros inesperados durante a conversão.
    """
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("Entrada inválida. Espera-se um DataFrame pandas.")

    try:
        buffer_string = io.StringIO()
        dataframe.to_csv(buffer_string, sep='\t', index=False, header=True, lineterminator='\n')
        string_tabulada = buffer_string.getvalue()
        buffer_string.close()

        print("   - DataFrame convertido para string tabulada com sucesso.")
        return string_tabulada

    except Exception as e:
        raise RuntimeError(f"Falha ao converter DataFrame para string tabulada: {e}")
    

    
# --- Bloco de Teste Direto ---
if __name__ == '__main__':
    """
    Bloco para testar AMBAS as funções do módulo.
    Execute a partir da raiz: python -m uteis.processador_tabela_clipboard
    """
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).resolve().parent.parent))

    # --- Teste da Leitura ---
    print(">>> Iniciando teste de LEITURA ('ler_tabela_clipboard_para_dataframe')...")
    print(">>> Lendo dados REAIS do clipboard em 5 segundos...")
    print(">>> (Copie a tabela do SAP para a área de transferência AGORA!)")
    time.sleep(5)
    df_lido = None
    try:
        df_lido = ler_tabela_clipboard_para_dataframe()
        print("\n--- Leitura concluída com SUCESSO! ---")
        print("--- DataFrame Lido (head): ---")
        print(df_lido.head().to_markdown(index=False))
    except Exception as e:
        print(f"\n--- Teste de LEITURA FALHOU! Erro: {e} ---")
        sys.exit(1) # Aborta se a leitura falhar

    # --- Teste da Formatação ---
    print("\n>>> Iniciando teste de FORMATAÇÃO ('converter_dataframe_para_string_tabulada')...")
    print(">>> Usando o DataFrame lido anteriormente...")
    try:
        string_formatada = converter_dataframe_para_string_tabulada(df_lido)
        print("\n--- Formatação concluída com SUCESSO! ---")
        print("--- String Tabulada Resultante (preview): ---")
        print(repr(string_formatada[:300]) + "...") # Mostra os primeiros 300 chars com \t, \n

        # Validação básica
        assert '\t' in string_formatada
        assert '\n' in string_formatada

    except Exception as e:
        print(f"\n--- Teste de FORMATAÇÃO FALHOU! Erro: {e} ---")