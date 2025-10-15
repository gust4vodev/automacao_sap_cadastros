# servicos/api_google.py

"""Módulo para interagir com a API Google Geocode."""

import requests
from typing import Tuple

# Import absoluto para carregar a chave da API do nosso módulo de configurações.
from configuracoes.carregar_config import API_KEY_GOOGLE

def consultar_coordenadas(endereco: str) -> Tuple[float, float]:
    """
    Consulta as coordenadas geográficas (latitude e longitude) de um endereço.

    Args:
        endereco (str): O endereço completo a ser consultado.

    Returns:
        Tuple[float, float]: Uma tupla contendo (latitude, longitude).

    Raises:
        requests.exceptions.RequestException: Em caso de falha na comunicação
                                              com a API.
        ValueError: Se o endereço não for encontrado ou a API retornar um
                    erro (ex: chave inválida, zero resultados).
    """
    # 1. URL base da API de Geocodificação do Google.
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"

    # 2. Dicionário com os parâmetros que serão enviados na URL.
    params = {
        'address': endereco,
        'key': API_KEY_GOOGLE
    }

    try:
        # 3. Executa a requisição GET com os parâmetros.
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()  # Lança erro para status HTTP 4xx ou 5xx.

        data = response.json()

        # 4. A API do Google tem um campo 'status' próprio no JSON.
        #    É preciso verificá-lo para saber se a consulta teve sucesso.
        if data['status'] == 'OK':
            # Extrai a localização do primeiro resultado encontrado.
            location = data['results'][0]['geometry']['location']
            latitude = location['lat']
            longitude = location['lng']
            return latitude, longitude

        elif data['status'] == 'ZERO_RESULTS':
            raise ValueError(f"O endereço '{endereco}' não retornou resultados.")

        else:
            # Trata outros erros possíveis da API (chave inválida, etc.).
            error_message = data.get('error_message', 'Erro não especificado pela API.')
            raise ValueError(f"Erro da API Google ({data['status']}): {error_message}")

    except requests.exceptions.RequestException as req_err:
        # Captura erros de conexão, timeout, etc.
        raise requests.exceptions.RequestException(
            f"Erro de conexão ao consultar o endereço: {req_err}"
        )