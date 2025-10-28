# uteis/formatadores.py

"""
Módulo com funções auxiliares para formatação e limpeza de dados.
"""

import re
import pandas as pd

def limpar_documento(doc: str) -> str:
    """Remove pontuação e caracteres não numéricos de CPF/CNPJ."""
    # Retorna uma string vazia se a entrada for None ou vazia
    if not doc:
        return ""
    # Usa expressão regular para encontrar e remover tudo que NÃO for dígito (\d)
    return re.sub(r'[^\d]', '', str(doc))

# --- Camada de Teste Direto ---
if __name__ == '__main__':
    """
    Bloco para testar a função 'limpar_documento'.
    Execute a partir da raiz: python -m uteis.formatadores
    """
    print(">>> Iniciando teste da função 'limpar_documento'...")

    testes = [
        ("123.456.789-00", "12345678900"),
        ("12.345.678/0001-99", "12345678000199"),
        ("Texto 123 com 456 numeros", "123456"),
        ("", ""),
        (None, "")
    ]

    sucesso = True
    for entrada, esperado in testes:
        resultado = limpar_documento(entrada)
        print(f"--- Testando '{entrada}': Resultado='{resultado}', Esperado='{esperado}'")
        if resultado != esperado:
            print(f"    *** FALHOU! ***")
            sucesso = False

    if sucesso:
        print("\n--- Teste concluído com SUCESSO! ---")
    else:
        print("\n--- Teste FALHOU! ---")


def formatar_endereco_para_api(linha_endereco: pd.Series) -> str:
    """
    Extrai os componentes de endereço de uma linha de DataFrame (Series)
    e os formata em uma string única para a API de Geocodificação.

    Args:
        linha_endereco (pd.Series): A linha do DataFrame contendo os dados do endereço.

    Returns:
        str: A string de endereço formatada (ex: "Rua, Numero, Bairro, Cidade, Estado").

    Raises:
        KeyError: Se alguma coluna essencial do endereço não for encontrada na Series.
        Exception: Para outros erros inesperados.
    """
    try:
        # Acessa os valores diretamente (assume que a validação prévia foi feita)
        # Usa .get() como segurança extra, mas idealmente as colunas existem
        rua = linha_endereco.get('Rua', '')
        # Pega só o número antes de possível letra/complemento
        numero = str(linha_endereco.get('Rua nº', '')).split(' ')[0]
        bairro = linha_endereco.get('Bairro', '')
        cidade = linha_endereco.get('Cidade', '')
        estado = linha_endereco.get('Estado', '')

        # Monta a string de endereço (adicionando "Brasil" para robustez)
        endereco_formatado = f"{rua}, {numero}, {bairro}, {cidade}, {estado}, Brasil"

        # Remove vírgulas duplicadas ou espaços extras
        endereco_formatado = re.sub(r'\s*,\s*', ', ', endereco_formatado).strip(', ')

        print(f"      - Endereço formatado para API: {endereco_formatado}")
        return endereco_formatado

    except KeyError as ke:
         raise KeyError(f"Coluna de endereço essencial não encontrada ao formatar para API: {ke}")
    except Exception as e:
        raise RuntimeError(f"Erro ao formatar endereço para API: {e}")