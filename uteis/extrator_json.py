# uteis/extrator_json.py

"""
Módulo com funções utilitárias para extrair dados de respostas JSON complexas.
Usado para extrair dados de forma rapida e dinamica do retorno de APIs.
"""

from typing import Any, Dict, List, Union
import re

def extrair_dado_json(dados_json: Union[Dict, List], caminho: str, padrao: Any = "") -> Any:
    """
    Navega em um dicionário ou lista JSON usando um caminho de chaves/índices
    e retorna o valor encontrado ou um valor padrão.

    Args:
        dados_json (Union[Dict, List]): O dicionário ou lista JSON (já convertido para Python).
        caminho (str): O caminho para o dado desejado, usando pontos para separar
        chaves e colchetes para índices de listas. Ex: "estabelecimento.inscricoes_estaduais[0].inscricao_estadual"
        padrao (Any, optional): O valor a ser retornado se o caminho não for encontrado ou for inválido. O padrão é "".

    Returns:
        Any: O valor encontrado no caminho especificado ou o valor padrão.
    """

    # 1. Verifica se JSON ou caminho são vazios e retorna valor padrão se necessário. 
    if not dados_json or not caminho:
        return padrao

    # 2. Divide o caminho por pontos e colchetes usando regex para separar chaves e índices. 
    partes = re.split(r'\.|(\[\d+\])', caminho)

    # 3. Filtra partes vazias geradas pelo split, garantindo lista limpa de tokens.  
    partes_limpas = [p for p in partes if p and p.strip()]

    # 4. Inicia navegação a partir da estrutura JSON com valor atual como raiz.  
    valor_atual = dados_json

    # 5. Para cada parte: se for índice `[n]`, converte e acessa lista se válido.  
    for parte in partes_limpas:
        match_indice = re.fullmatch(r'\[(\d+)\]', parte) 
        if match_indice: # Verifica se é um índice de lista (ex: '[0]')
            try:
                indice = int(match_indice.group(1))
                if isinstance(valor_atual, list) and 0 <= indice < len(valor_atual):
                    valor_atual = valor_atual[indice]
                else:
                    return padrao # Índice inválido ou o valor atual não é uma lista
            except (ValueError, IndexError):
                return padrao
            
    # 6. Se não for índice, trata como chave de dicionário e usa `.get()` para acesso seguro.
        elif isinstance(valor_atual, dict):
            valor_atual = valor_atual.get(parte)

    # 7. Retorna valor padrão se tipo incompatível, índice fora do limite ou chave ausente.         
            if valor_atual is None: # Chave não encontrada
                return padrao
        else: # Tentou acessar uma chave em algo que não é dicionário
            return padrao

    # 8. Após navegação completa, retorna valor encontrado ou padrão se `None`. 
    return valor_atual if valor_atual is not None else padrao


# --- Camada de Teste Direto ---
if __name__ == '__main__':
    """
    Bloco para testar a função 'extrair_dado_json'.
    Execute a partir da raiz: python -m uteis.extrator_json
    """
    print(">>> Iniciando teste da função 'extrair_dado_json'...")

    # Exemplo de JSON similar à resposta da API CNPJ
    json_teste = {
        "estabelecimento": {
            "cnpj": "123456",
            "inscricoes_estaduais": [
                {
                    "estado": "SP",
                    "inscricao_estadual": "111222333"
                },
                {
                    "estado": "PR",
                    "inscricao_estadual": "999888777"
                }
            ]
        },
        "nome": "Empresa Teste"
    }

    # Teste 1: Caminho válido e existente
    print('\n')
    caminho1 = "estabelecimento.inscricoes_estaduais[0].inscricao_estadual"
    resultado1 = extrair_dado_json(json_teste, caminho1)
    print(f"--- Teste 1 ('{caminho1}'): {resultado1} (Esperado: '111222333')")
    assert resultado1 == "111222333", "Teste 1 Falhou"

    # Teste 2: Caminho válido, segundo item da lista
    print('\n')
    caminho2 = "estabelecimento.inscricoes_estaduais[1].estado"
    resultado2 = extrair_dado_json(json_teste, caminho2)
    print(f"--- Teste 2 ('{caminho2}'): {resultado2} (Esperado: 'PR')")
    assert resultado2 == "PR", "Teste 2 Falhou"

    # Teste 3: Chave de nível superior
    print('\n')
    caminho3 = "nome"
    resultado3 = extrair_dado_json(json_teste, caminho3)
    print(f"--- Teste 3 ('{caminho3}'): {resultado3} (Esperado: 'Empresa Teste')")
    assert resultado3 == "Empresa Teste", "Teste 3 Falhou"

    # Teste 4: Caminho inválido (chave não existe)
    print('\n')
    caminho4 = "estabelecimento.cidade"
    resultado4 = extrair_dado_json(json_teste, caminho4)
    print(f"--- Teste 4 ('{caminho4}'): '{resultado4}' (Esperado: '')")
    assert resultado4 == "", "Teste 4 Falhou"

    # Teste 5: Caminho inválido (índice fora do limite)
    print('\n')
    caminho5 = "estabelecimento.inscricoes_estaduais[2].estado"
    resultado5 = extrair_dado_json(json_teste, caminho5)
    print(f"--- Teste 5 ('{caminho5}'): '{resultado5}' (Esperado: '')")
    assert resultado5 == "", "Teste 5 Falhou"

    # Teste 6: Usando valor padrão diferente
    print('\n')
    caminho6 = "chave_inexistente"
    resultado6 = extrair_dado_json(json_teste, caminho6, padrao=None)
    print(f"--- Teste 6 ('{caminho6}', padrao=None): {resultado6} (Esperado: None)")
    assert resultado6 is None, "Teste 6 Falhou"

    print("\n--- Teste concluído com SUCESSO! ---")