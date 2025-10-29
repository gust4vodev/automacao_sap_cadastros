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
        # 1. Extrai campos (confiando na validação prévia dos campos essenciais)
        rua = linha_endereco.get('Rua', '')
        bairro = linha_endereco.get('Bairro', '')
        cidade = linha_endereco.get('Cidade', '')
        estado = linha_endereco.get('Estado', '')
        
        # 2. Processa o 'Rua nº' (campo opcional)
        # Pega só o número antes de possível letra/complemento
        numero = str(linha_endereco.get('Rua nº', '')).split(' ')[0]

        # 3. Monta uma lista com todas as partes
        #    (Campos essenciais são garantidos; 'numero' pode ser '' (vazio))
        partes_endereco = [rua, numero, bairro, cidade, estado, "Brasil"]
        
        # 4. Filtra a lista para remover quaisquer partes que sejam strings vazias ('')
        #    Isto remove o 'numero' se ele for uma string vazia.
        partes_validas = [parte for parte in partes_endereco if parte]

        # 5. Junta as partes válidas com ", "
        #    Este método garante que não haverá vírgulas duplicadas.
        endereco_formatado = ", ".join(partes_validas)

        print(f"       - Endereço formatado para API: {endereco_formatado}")
        return endereco_formatado

    except KeyError as ke:
            raise KeyError(f"Coluna de endereço essencial não encontrada ao formatar para API: {ke}")
    except Exception as e:
            raise RuntimeError(f"Erro ao formatar endereço para API: {e}")
    
# --- Camada de Teste Direto ---
if __name__ == '__main__':
    """
    Bloco para testar ambas as funções do módulo:
    1. limpar_documento
    2. formatar_endereco_para_api
    
    Execute a partir da raiz: python -m uteis.formatadores
    """
    
    # --- Teste 1: limpar_documento ---
    print(">>> Iniciando teste da função 'limpar_documento'...")
    testes_doc = [
        ("123.456.789-00", "12345678900"),
        ("12.345.678/0001-99", "12345678000199"),
        ("Texto 123 com 456 numeros", "123456"),
        ("", ""),
        (None, "")
    ]

    sucesso_doc = True
    for entrada, esperado in testes_doc:
        resultado = limpar_documento(entrada)
        print(f"--- Testando '{entrada}': R='{resultado}', E='{esperado}'")
        if resultado != esperado:
            print(f"       *** FALHOU! ***")
            sucesso_doc = False

    if sucesso_doc:
        print(">>> Teste 'limpar_documento' concluído com SUCESSO!\n")
    else:
        print(">>> Teste 'limpar_documento' FALHOU!\n")

    
    # --- NOVO: Teste 2: formatar_endereco_para_api ---
    
    # Importa o Pandas APENAS para o teste
    try:
        import pandas as pd
    except ImportError:
        print("--- AVISO: Pandas não instalado. A pular testes de 'formatar_endereco_para_api'. ---")
        pd = None

    if pd:
        print(">>> Iniciando teste da função 'formatar_endereco_para_api'...")
        
        # Cenário 1: Endereço completo (com split de número)
        teste_completo = pd.Series({
            'Rua': 'Rua das Flores',
            'Rua nº': '123 AP 45', # Testa o split(' ')[0]
            'Bairro': 'Centro',
            'Cidade': 'São Paulo',
            'Estado': 'SP'
        })
        # Resultado esperado da sua lógica original:
        esperado_completo = "Rua das Flores, 123, Centro, São Paulo, SP, Brasil"
        
        # Cenário 2: Endereço sem Número (campo opcional)
        teste_sem_numero = pd.Series({
            'Rua': 'Avenida Principal',
            'Rua nº': '', # Testa campo vazio (opcional)
            'Bairro': 'Norte',
            'Cidade': 'Curitiba',
            'Estado': 'PR'
        })
        # Resultado esperado da sua lógica original (gera uma vírgula extra no início):
        # f"Avenida Principal, , Norte, Curitiba, PR, Brasil"
        esperado_sem_numero = "Avenida Principal, Norte, Curitiba, PR, Brasil"

        testes_end = [
            (teste_completo, esperado_completo),
            (teste_sem_numero, esperado_sem_numero),
        ]

        sucesso_end = True
        for entrada_series, esperado in testes_end:
            try:
                # O print da função (com '...') já vai aparecer aqui
                resultado = formatar_endereco_para_api(entrada_series)
                
                print(f"--- Testando: R='{resultado}', E='{esperado}'")
                if resultado.strip() != esperado.strip():
                    print(f"       *** FALHOU! ***")
                    sucesso_end = False
            except Exception as e:
                print(f"       *** FALHOU COM EXCEÇÃO: {e} ***")
                sucesso_end = False

        if sucesso_end:
            print(">>> Teste 'formatar_endereco_para_api' concluído com SUCESSO!\n")
        else:
            print(">>> Teste 'formatar_endereco_para_api' FALHOU!\n")

    # --- Resumo Final ---
    if sucesso_doc and (not pd or sucesso_end):
        print("\n--- Todos os testes do módulo concluídos com SUCESSO! ---")
    else:
        print("\n--- Um ou mais testes FALHARAM! ---")