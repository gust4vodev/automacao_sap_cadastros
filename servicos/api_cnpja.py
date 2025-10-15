# servicos/api_cnpja.py

"""Módulo para interagir com a API do CNPJá."""

import requests
from typing import Dict, Any

# Import absoluto para carregar a URL da API do nosso módulo de configurações.
from configuracoes.carregar_config import URL_CNPJA

def consultar_cnpj(cnpj: str) -> Dict[str, Any]:
    """
    Realiza uma consulta de CNPJ na API CNPJá.

    Args:
        cnpj (str): O número do CNPJ a ser consultado, sem pontuação.

    Returns:
        Dict[str, Any]: Um dicionário com os dados da empresa se a consulta
                        for bem-sucedida.

    Raises:
        requests.exceptions.RequestException: Em caso de falha na comunicação
                                              com a API (ex: erro de rede).
        ValueError: Se o CNPJ não for encontrado ou a resposta da API
                    indicar um erro (ex: status code 404).
    """
    # 1. Monta a URL completa para a requisição.
    # Ex: "https://open.cnpja.com/office/" + "07526557011659"
    url_completa = f"{URL_CNPJA}{cnpj}"

    try:
        # 2. Executa a requisição GET para a API.
        # O timeout define um limite de 10 segundos para a resposta.
        response = requests.get(url_completa, timeout=10)

        # 3. Lança um erro HTTP se a resposta for um código de falha (4xx ou 5xx).
        # Isso garante que o programa pare se a API estiver fora do ar, por exemplo.
        response.raise_for_status()

        # 4. Se a requisição foi bem-sucedida (código 200), retorna os dados em formato JSON.
        return response.json()

    except requests.exceptions.HTTPError as http_err:
        # Captura especificamente erros de status HTTP.
        if response.status_code == 404:
            raise ValueError(f"CNPJ '{cnpj}' não encontrado na base de dados.")
        else:
            raise ValueError(f"Erro HTTP ao consultar o CNPJ '{cnpj}': {http_err}")

    except requests.exceptions.RequestException as req_err:
        # Captura outros erros de requisição (falha de conexão, timeout, etc.).
        raise requests.exceptions.RequestException(
            f"Erro de conexão ao consultar o CNPJ '{cnpj}': {req_err}"
        )