# servicos/api_cnpja_comercial_ie_simples.py

"""
Módulo para consultar a API Comercial do CNPJá (/office/).

Esta API unificada retorna dados cadastrais, sócios (QSA), simples
e inscrições estaduais (IE) em uma única chamada.
"""

import requests
import time
import re
from typing import Dict, Any
from configuracoes.carregar_config import (CNPJA_API_KEY_COMERCIAL, CNPJA_API_URL_COMERCIAL_IE_SIMPLES)

TIMEOUT_REQUISICAO = 15

def _limpar_documento(doc: str) -> str:
    """Remove pontuação de CPF/CNPJ."""
    if not doc:
        return ""
    return re.sub(r"[^\d]", "", str(doc))


def consultar_cnpj_completo(cnpj: str) -> Dict[str, Any]:
    """
    Consulta a API Comercial (/office/) com estratégia de cache escalonada
    para obter os dados completos (Cadastral, QSA, Simples, IE).

    Args:
        cnpj (str): O CNPJ a ser consultado (pode conter pontuação).

    Returns:
        Dict[str, Any]: O JSON bruto retornado pela API em caso de sucesso.

    Raises:
        requests.exceptions.RequestException: Em caso de falha de conexão ou timeout.
        ValueError: Se os dados não forem encontrados (404), chave inválida (401),
                    créditos esgotados (429) ou outro erro da API.
    """
    
    # --- 1. Preparação ---
    cnpj_limpo = _limpar_documento(cnpj)
    
    # URL (do config)
    url = f"{CNPJA_API_URL_COMERCIAL_IE_SIMPLES}{cnpj_limpo}"
    
    # Chave (do config)
    headers = {"Authorization": CNPJA_API_KEY_COMERCIAL}

    # Parâmetros base para feacture de IE e Simples Nascional
    params_base = {
        "simples": "true",
        "registrations": "BR",
    }

    # Estratégias de cache para reduzir o consumo dos creditos de API
    tentativas = [
        {"desc": "Cache até 45 dias",    "strategy": "CACHE", "maxAge": 45},
        {"desc": "Cache até 150 dias",   "strategy": "CACHE", "maxAge": 150},
        {"desc": "Consulta online (paga)","strategy": "CACHE_IF_FRESH", "maxAge": 1},
    ]

    # --- 2. Loop de Tentativas ---
    
    for t in tentativas:
        print(f"     -> Tentando API Comercial: {t['desc']}...") # Log da tentativa

        # Monta parâmetros
        params = params_base.copy()
        params["strategy"] = t["strategy"]
        params["maxAge"] = t["maxAge"]
        
        try:
            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=TIMEOUT_REQUISICAO
            )

            # --- 3. Tratamento de Erros (Error Handling) ---
            
            if response.status_code == 200:
                return response.json() # Sucesso, retorna o JSON
            
            
            elif response.status_code == 404:
                # 404 (Não Encontrado) não é um erro, tenta a próxima estratégia
                print(f"     ⚠️  Dados não encontrados na tentativa: {t['desc']}")
                time.sleep(5) # Pausa antes da próxima requisição
                continue # Continua para a próxima tentativa

            elif response.status_code == 429:
                # 429 (Too Many Requests) nesta API significa "Créditos Esgotados"
                time.sleep(5) # Pausa antes da próxima
                raise ValueError(f"API CNPJá Comercial (/office/): Créditos esgotados ou limite atingido (status 429).")

            elif response.status_code == 401:
                # 401 (Não Autorizado) é um erro grave
                time.sleep(5)
                raise ValueError(f"API CNPJá Comercial (/office/): Chave de API inválida (status 401). Verifique CNPJA_API_KEY_COMERCIAL no .env.")

            else:
                # Outros erros HTTP (5xx, etc.)
                time.sleep(5)
                raise ValueError(f"API CNPJá Comercial (/office/): Erro inesperado (status {response.status_code}): {response.text}")

        except requests.exceptions.Timeout:
             raise requests.exceptions.RequestException(f"API CNPJá Comercial (/office/): Timeout ({TIMEOUT_REQUISICAO}s) excedido na tentativa '{t['desc']}'.")
        except requests.exceptions.RequestException as e:
             # Erros de conexão, DNS, etc.
             raise requests.exceptions.RequestException(f"API CNPJá Comercial (/office/): Falha na conexão na tentativa '{t['desc']}': {e}")
    

    # Se o loop terminar sem sucesso (todos deram 404)
    raise ValueError(f"API CNPJá Comercial (/office/): Nenhuma informação encontrada para CNPJ '{cnpj}' após todas as tentativas.")


# --- Camada de Teste Direto ---
if __name__ == "__main__":
    """
    Bloco para testar esta nova função de forma isolada.
    Execute a partir da raiz: python -m servicos.api_cnpja_comercial_ie_simples
    """
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    import json

    CNPJ_TESTE = "04143008002705" 

    print(f">>> Iniciando teste da função 'consultar_cnpj_completo' com CNPJ: {CNPJ_TESTE}...")
    try:
        resultado = consultar_cnpj_completo(CNPJ_TESTE)
        print("\n--- Teste concluído com SUCESSO! ---")
        print("--- Resultado JSON recebido: ---")
        # Imprime o JSON de forma legível
        print(json.dumps(resultado, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"\n--- Teste FALHOU! Erro: {e} ---")