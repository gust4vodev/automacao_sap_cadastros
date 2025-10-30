# servicos/api_cnpja_comercial_ie.py

"""Módulo para consultar Inscrições Estaduais (IE) na API CNPJá Comercial (/ccc)."""

import requests
import time
from typing import Dict, Any

# --- Imports de Configuração ---
# CORREÇÃO AQUI:
from configuracoes.carregar_config import CNPJA_API_KEY_COMERCIAL, CNPJA_API_URL_COMERCIAL_IE

# --- Constantes ---
HEADERS = {"Authorization": CNPJA_API_KEY_COMERCIAL}
TIMEOUT_REQUISICAO = 15 # Timeout em segundos

def consultar_ie_por_cnpj(cnpj: str, estado: str = "BR") -> Dict[str, Any]:
    """
    Consulta o Cadastro Centralizado de Contribuintes (CCC) com estratégia escalonada.

    Estratégia: Cache 90d -> Cache 150d -> Online (pago).

    Args:
        cnpj (str): O CNPJ a ser consultado (apenas números).
        estado (str, optional): A sigla do estado para filtrar (ex: "SP").
                                 Padrão é "BR" para buscar em todos.

    Returns:
        Dict[str, Any]: O JSON bruto retornado pela API em caso de sucesso.

    Raises:
        requests.exceptions.RequestException: Em caso de falha de conexão ou timeout.
        ValueError: Se os dados não forem encontrados, chave inválida,
                    créditos esgotados ou outro erro da API.
    """
    # Define as diferentes tentativas (estratégias)
    tentativas = [
        {"desc": "Cache até 90 dias", "params": {"taxId": cnpj, "states": estado, "strategy": "CACHE", "maxAge": 90}},
        {"desc": "Cache até 150 dias", "params": {"taxId": cnpj, "states": estado, "strategy": "CACHE", "maxAge": 150}},
        {"desc": "Consulta online (paga)", "params": {"taxId": cnpj, "states": estado, "strategy": "ONLINE", "maxAge": 1}},
    ]
    
    for tentativa in tentativas:
        print(f"     -> Tentando: {tentativa['desc']}...") # Log da tentativa
        try:
            response = requests.get(
                CNPJA_API_URL_COMERCIAL_IE,
                headers=HEADERS,
                params=tentativa["params"],
                timeout=TIMEOUT_REQUISICAO
            )

            # Verifica o status code da resposta
            if response.status_code == 200:
                return response.json() # Sucesso, retorna o JSON

            elif response.status_code == 404:
                print(f"     ⚠️ Dados não encontrados na tentativa: {tentativa['desc']}")
                time.sleep(1) # Pausa antes da próxima
                continue # Continua para a próxima tentativa

            elif response.status_code == 429:
                raise ValueError(f"API CNPJá Comercial (/ccc): Créditos esgotados ou limite atingido (status {response.status_code}).")

            elif response.status_code == 401:
                raise ValueError(f"API CNPJá Comercial (/ccc): Chave de API inválida (status {response.status_code}). Verifique CNPJA_API_KEY_COMERCIAL_IE no .env.")

            else:
                # Outros erros HTTP (5xx, etc.)
                raise ValueError(f"API CNPJá Comercial (/ccc): Erro inesperado (status {response.status_code}): {response.text}")

        except requests.exceptions.Timeout:
             raise requests.exceptions.RequestException(f"API CNPJá Comercial (/ccc): Timeout ({TIMEOUT_REQUISICAO}s) excedido na tentativa '{tentativa['desc']}'.")
        except requests.exceptions.RequestException as e:
             # Erros de conexão, DNS, etc.
             raise requests.exceptions.RequestException(f"API CNPJá Comercial (/ccc): Falha na conexão na tentativa '{tentativa['desc']}': {e}")

    # Se o loop terminar sem sucesso (todos deram 404)
    raise ValueError(f"API CNPJá Comercial (/ccc): Nenhuma IE encontrada para CNPJ '{cnpj}' (Estado: {estado}) após todas as tentativas.")


# --- Camada de Teste Direto ---
if __name__ == "__main__":
    """
    Bloco para testar a função de consulta de IE.
    Execute a partir da raiz: python -m servicos.api_cnpja_comercial_ie
    """
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    import json

    CNPJ_TESTE = "04143008002705"

    print(f">>> Iniciando teste da função 'consultar_ie_por_cnpj' com CNPJ: {CNPJ_TESTE}...")
    try:
        resultado = consultar_ie_por_cnpj(CNPJ_TESTE)
        print("\n--- Teste concluído com SUCESSO! ---")
        print("--- Resultado JSON recebido: ---")
        # Imprime o JSON de forma legível
        print(json.dumps(resultado, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"\n--- Teste FALHOU! Erro: {e} ---")