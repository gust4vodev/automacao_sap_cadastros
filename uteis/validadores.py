# uteis/validadores.py

"""
Módulo com funções auxiliares para validação de dados.
"""

import pandas as pd
from typing import List

def validar_tabela_endereco(dataframe: pd.DataFrame):
    """
    Valida se um DataFrame (representando a tabela de endereço copiada)
    contém as colunas essenciais e se elas estão preenchidas na primeira linha.

    Args:
        dataframe (pd.DataFrame): O DataFrame a ser validado.

    Raises:
        ValueError: Se o DataFrame estiver vazio, alguma coluna essencial
                    faltar, ou algum campo essencial estiver vazio/nulo
                    na primeira linha.
    """
    print("      - Iniciando validação da tabela de endereço...")

    # Lista das colunas que NÃO podem estar vazias
    colunas_essenciais = [
        'ID do endereço', 'Tipo de logradouro', 'Rua', 'Rua nº', 'CEP',
        'Bairro', 'Cidade', 'País/região', 'Estado', 'Município'
    ]

    # 1. Verifica se o DataFrame está vazio
    if dataframe.empty:
         raise ValueError("Tabela de endereço (DataFrame) está vazia.")

    # 2. Pega a primeira linha para validação dos dados
    #    Usar .iloc[0] é seguro aqui porque já verificamos que não está vazio.
    primeira_linha = dataframe.iloc[0]

    # 3. Valida colunas e valores
    campos_problematicos = []
    for coluna in colunas_essenciais:
        # Verifica se a coluna existe
        if coluna not in dataframe.columns:
            campos_problematicos.append(f"Coluna ausente: '{coluna}'")
            continue # Pula para próxima coluna se esta não existe

        # Verifica se o valor na primeira linha é Nulo (NaN) ou string vazia
        valor = primeira_linha[coluna]
        if pd.isna(valor) or str(valor).strip() == "":
            campos_problematicos.append(f"Campo vazio: '{coluna}'")

    # 4. Levanta erro se houver problemas
    if campos_problematicos:
        erro_msg = f"Dados essenciais ausentes/vazios na tabela de endereço: {'; '.join(campos_problematicos)}"
        print(f"      ❌ ERRO Validação: {erro_msg}")
        raise ValueError(erro_msg)
    else:
        print("      ✅ Validação da tabela de endereço concluída com sucesso.")


# --- Camada de Teste Direto ---
if __name__ == '__main__':
    """
    Bloco para testar a função 'validar_tabela_endereco'.
    Execute a partir da raiz: python -m uteis.validadores
    """
    print(">>> Iniciando teste da função 'validar_tabela_endereco'...")

    # Teste 1: DataFrame Válido
    print("\n--- Teste 1: DataFrame Válido ---")
    df_valido = pd.DataFrame([{
        'ID do endereço': 'FATURAMENTO', 'Tipo de logradouro': 'RUA', 'Rua': 'TESTE',
        'Rua nº': '123', 'CEP': '12345-678', 'Bairro': 'CENTRO', 'Cidade': 'CIDADE',
        'País/região': 'Brasil', 'Estado': 'SP', 'Município': 'MUNICIPIO', 'Outra Coluna': 'Valor'
    }])
    try:
        validar_tabela_endereco(df_valido)
        print("   -> SUCESSO (Esperado)")
    except ValueError as e:
        print(f"   -> FALHA INESPERADA: {e}")

    # Teste 2: DataFrame com Campo Vazio
    print("\n--- Teste 2: Campo 'Rua' Vazio ---")
    df_rua_vazia = df_valido.copy()
    df_rua_vazia.loc[0, 'Rua'] = ""
    try:
        validar_tabela_endereco(df_rua_vazia)
        print("   -> FALHA (Esperado Erro, mas passou)")
    except ValueError as e:
        print(f"   -> SUCESSO (Erro esperado capturado): {e}")

    # Teste 3: DataFrame com Coluna Ausente
    print("\n--- Teste 3: Coluna 'Estado' Ausente ---")
    df_sem_estado = df_valido.drop(columns=['Estado'])
    try:
        validar_tabela_endereco(df_sem_estado)
        print("   -> FALHA (Esperado Erro, mas passou)")
    except ValueError as e:
        print(f"   -> SUCESSO (Erro esperado capturado): {e}")

    # Teste 4: DataFrame Vazio
    print("\n--- Teste 4: DataFrame Vazio ---")
    df_vazio = pd.DataFrame()
    try:
        validar_tabela_endereco(df_vazio)
        print("   -> FALHA (Esperado Erro, mas passou)")
    except ValueError as e:
        print(f"   -> SUCESSO (Erro esperado capturado): {e}")

    print("\n--- Testes concluídos ---")