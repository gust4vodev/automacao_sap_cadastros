# servicos/api_cnpja_publica.py
"""
Módulo responsável por consultar a API pública do CNPJá
para obtenção de dados cadastrais de empresas.
"""
import requests
from typing import Dict, Any
from configuracoes.carregar_config import CNPJA_API_URL_PUBLICA

# --- Constantes ---
TIMEOUT_REQUISICAO = 10 # Timeout em segundos

# Função principal: consultar_cnpj
def consultar_cnpj(cnpj: str) -> Dict[str, Any]:
    """Consulta os dados de um CNPJ na API pública do CNPJá.
    Args:
        cnpj (str): Número do CNPJ a ser consultado (somente dígitos).
    Returns:
        Dict[str, Any]: Dados da empresa retornados pela API.
    Raises:
        requests.exceptions.Timeout: Se a requisição exceder o tempo limite.
        requests.exceptions.ConnectionError: Se houver problemas de rede.
        ValueError: Se o CNPJ não for encontrado (404) ou ocorrer outro erro HTTP (4xx, 5xx).
        requests.exceptions.RequestException: Para outros erros inesperados.
    """

    url = f"{CNPJA_API_URL_PUBLICA}{cnpj}"

    try:
        response = requests.get(url, timeout=TIMEOUT_REQUISICAO)

        # Lança uma exceção HTTPError para respostas 4xx ou 5xx.
        response.raise_for_status()

        # Se chegou aqui, a resposta foi 2xx (sucesso).
        print("     ✅ Sucesso na consulta.") # Log de Sucesso
        return response.json()

    except requests.exceptions.Timeout:
        # Log e raise para Timeout
        print(f"     ❌ Falha: Timeout ({TIMEOUT_REQUISICAO}s) excedido.")
        raise requests.exceptions.Timeout(
            f"API Pública CNPJá: Tempo limite ({TIMEOUT_REQUISICAO}s) excedido ao consultar CNPJ '{cnpj}'."
        )

    except requests.exceptions.ConnectionError as conn_err:
        # Log e raise para ConnectionError
        print(f"     ❌ Falha: Erro de conexão ({conn_err}).")
        raise requests.exceptions.ConnectionError(
            f"API Pública CNPJá: Erro de conexão ao consultar CNPJ '{cnpj}': {conn_err}"
        )

    except requests.exceptions.HTTPError as http_err:
        # Log e raise para HTTPError
        status_code = http_err.response.status_code
        print(f"     ❌ Falha: Erro HTTP {status_code}.")
        if status_code == 404:
            # Trata o 404 especificamente
            print("     ⚠️  CNPJ não encontrado na base pública do CNPJá.") # Log específico 404
            raise ValueError(f"API Pública CNPJá: CNPJ '{cnpj}' não encontrado (status {status_code}).")
        # Adicione elif para outros códigos 4xx/5xx se precisar de tratamento especial
        # elif status_code == 429: etc...
        else:
            # Trata outros erros HTTP (ex: 500, 503)
            raise ValueError(
                f"API Pública CNPJá: Erro HTTP {status_code} inesperado ao consultar CNPJ '{cnpj}': {http_err}"
            )

    except requests.exceptions.RequestException as req_err:
        # Log e raise para outros RequestException
        print(f"     ❌ Falha: Erro inesperado na requisição ({req_err}).")
        raise requests.exceptions.RequestException(
            f"API Pública CNPJá: Erro inesperado ao consultar CNPJ '{cnpj}': {req_err}"
        )

# testando a função diretamente
if __name__ == "__main__":
    """
    Bloco para testar a função de consulta de CNPJ.
    Execute a partir da raiz: python -m servicos.api_cnpja_publica
    """
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    import json # Para imprimir o JSON formatado

    CNPJ_TESTE = "04143008002705"
    print(f">>> Testando função com CNPJ: {CNPJ_TESTE}")

    try:
        resultado = consultar_cnpj(CNPJ_TESTE)
        print("\n--- Teste concluído com SUCESSO! ---")
        print("--- Resultado JSON recebido: ---")
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
    except Exception as e:
        print("\n--- Teste FALHOU! Erro: ---")
        print(e)