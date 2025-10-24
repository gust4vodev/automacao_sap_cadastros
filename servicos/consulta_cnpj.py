# ============================================================
# 📦 servicos/consulta_cnpj.py
# ============================================================
"""
Módulo de interface/abstração para consulta de dados de CNPJ
com cache simplificado (apenas o último resultado).
"""

from typing import Dict, Any, List
import re
import time  # Adicionado para logs de cache

# --- Imports ---
from .api_cnpja_publica import consultar_cnpj as consultar_cnpj_publica
from .api_cnpja_comercial_ie import consultar_ie_por_cnpj
from configuracoes.carregar_config import API_CNPJ_SELECIONADA
from uteis.extrator_json import extrair_dado_json


# ============================================================
# 🧠 Cache Simplificado
# ============================================================
_ultimo_cnpj_consultado: str = None
_ultimo_resultado: Dict[str, Any] = None

# ============================================================
# 🔧 Funções Auxiliares
# ============================================================
def _limpar_cep(cep: str) -> str:
    """Remove pontuação do CEP."""
    return re.sub(r"[^\d]", "", str(cep))


def _limpar_documento(doc: str) -> str:
    """Remove pontuação de CPF/CNPJ."""
    if not doc:
        return ""
    return re.sub(r"[^\d]", "", str(doc))


def separar_tipo_logradouro(logradouro_completo: str):
    """Divide o logradouro completo em tipo e nome."""
    if not logradouro_completo:
        return None, None
    partes = logradouro_completo.strip().split(" ", 1)
    return (partes[0], partes[1]) if len(partes) == 2 else (None, partes[0])


# ============================================================
# 🚀 Função Principal
# ============================================================
def obter_dados_cnpj(cnpj: str) -> Dict[str, Any]:
    """
    Obtém dados de um CNPJ, usando cache do último resultado e orquestrando APIs.
    Retorna um dicionário padronizado.
    """
    global _ultimo_cnpj_consultado, _ultimo_resultado

    cnpj_chave = _limpar_documento(cnpj)

    # --- Verificação de Cache ---
    if cnpj_chave == _ultimo_cnpj_consultado and _ultimo_resultado is not None:
        return _ultimo_resultado
    start_time = time.time()

    # --- Inicialização ---
    dados_padronizados = {
        "status_cnpj": "",
        "razao_social": "",
        "data_abertura": "",
        "inscricao_estadual": "Isento",
        "simples_nacional": None,
        "suframa_valido": False,
        "suframa_numero": "",
        "socios": [],
        "endereco": {
            "tipo_logradouro": "",
            "logradouro": "",
            "numero": "",
            "complemento": "",
            "bairro": "",
            "cep": "",
            "cidade": "",
            "estado": ""
        }
    }

    # ============================================================
    # 🧩 Etapa 1 — Dados Gerais
    # ============================================================
    dados_gerais_brutos = {}
    if API_CNPJ_SELECIONADA == 1:  # CNPJá Pública
        try:
            dados_gerais_brutos = consultar_cnpj_publica(cnpj_chave)
        except Exception as e:
                print(f"⚠️ Aviso: Falha ao obter dados gerais da API principal (CNPJá Pública): {e}")
                # --- ADICIONAR ESTA LINHA ---
                # Re-levanta a exceção para sinalizar a falha ao motor executor
                raise e
        try:
            # Mapeamento principal
            dados_padronizados["razao_social"] = extrair_dado_json(dados_gerais_brutos, "company.name")
            dados_padronizados["data_abertura"] = extrair_dado_json(dados_gerais_brutos, "founded")
            dados_padronizados["status_cnpj"] = extrair_dado_json(dados_gerais_brutos, "status.text")
            dados_padronizados["simples_nacional"] = extrair_dado_json(
                dados_gerais_brutos, "company.simples.optant", padrao=None
            )

            # Endereço
            logradouro_completo = extrair_dado_json(dados_gerais_brutos, "address.street")
            tipo_log, nome_log = separar_tipo_logradouro(logradouro_completo)
            endereco = dados_padronizados["endereco"]
            endereco["tipo_logradouro"] = tipo_log or ""
            endereco["logradouro"] = nome_log or ""
            endereco["numero"] = extrair_dado_json(dados_gerais_brutos, "address.number")
            endereco["complemento"] = extrair_dado_json(dados_gerais_brutos, "address.details")
            endereco["bairro"] = extrair_dado_json(dados_gerais_brutos, "address.district")
            endereco["cep"] = _limpar_cep(extrair_dado_json(dados_gerais_brutos, "address.zip"))
            endereco["cidade"] = extrair_dado_json(dados_gerais_brutos, "address.city")
            endereco["estado"] = extrair_dado_json(dados_gerais_brutos, "address.state")

            # Sócios
            socios_brutos = dados_gerais_brutos.get("company", {}).get("members", [])
            dados_padronizados["socios"] = [m["person"]["name"] for m in socios_brutos]
        except Exception as e:
            print(f"⚠️ Aviso: Falha ao obter dados gerais da API principal (CNPJá Pública): {e}")

    # ============================================================
    # 🔎 Etapa 2 — Suframa
    # ============================================================
    try:
        suframa_lista = extrair_dado_json(dados_gerais_brutos, "suframa", padrao=[])
        if suframa_lista: # Procede somente se a lista não for vazia
            primeiro_suframa = suframa_lista[0] # Pega o primeiro registro
            suframa_aprovado = extrair_dado_json(primeiro_suframa, "approved", padrao=False)
            suframa_numero = extrair_dado_json(primeiro_suframa, "number", padrao="")
            if suframa_aprovado and suframa_numero:
                dados_padronizados["suframa_valido"] = True
                dados_padronizados["suframa_numero"] = suframa_numero
        else:
            dados_padronizados["suframa_valido"] = False
            dados_padronizados["suframa_numero"] = ""

    except Exception as e:
        # Em caso de erro inesperado ao processar Suframa
        print(f"⚠️ Aviso: Falha ao processar dados de Suframa: {e}")
        dados_padronizados["suframa_valido"] = False
        dados_padronizados["suframa_numero"] = ""

    # ============================================================
    # 🧩 Etapa 3 — Inscrição Estadual
    # ============================================================
    try:
        dados_ie_brutos = consultar_ie_por_cnpj(cnpj_chave)
        estado_empresa = dados_padronizados["endereco"]["estado"]
        inscricao_estadual_valida = "Isento"
        registrations: List[Dict] = extrair_dado_json(dados_ie_brutos, "registrations", padrao=[])
        if estado_empresa:
            print(f"   - Validando {len(registrations)} IE(s) encontradas para o estado {estado_empresa}...")
            for registro in registrations:
                ie_numero = extrair_dado_json(registro, "number")
                ie_estado = extrair_dado_json(registro, "state")
                ie_ativa = extrair_dado_json(registro, "enabled", padrao=False)

                if ie_numero and ie_estado and ie_ativa and ie_estado.upper() == estado_empresa.upper():
                    print(f"     -> IE válida encontrada: {ie_numero}/{ie_estado} (Ativa)")
                    inscricao_estadual_valida = ie_numero
                    break
                elif ie_numero and ie_estado:
                    if not ie_ativa:
                        print(f"     -> IE {ie_numero}/{ie_estado} ignorada (inativa).")
                    elif ie_estado.upper() != estado_empresa.upper():
                        print(f"     -> IE {ie_numero}/{ie_estado} ignorada (estado diferente de {estado_empresa}).")
                    else:
                        print(f"     -> IE {ie_numero}/{ie_estado} ignorada (dados incompletos).")
        else:
            print("   - Não foi possível validar a IE (estado da empresa não encontrado nos dados gerais).")

        dados_padronizados["inscricao_estadual"] = inscricao_estadual_valida

    except Exception as e:
        print(f"⚠️ Aviso: falha ao consultar inscrição estadual: {e}")


    # ============================================================
    # 🕒 Finalização
    # ============================================================
    end_time = time.time()
    print(f"   - Consultas APIs concluídas em {end_time - start_time:.2f} segundos.")

    _ultimo_cnpj_consultado = cnpj_chave
    _ultimo_resultado = dados_padronizados

    return dados_padronizados
# ============================================================
# 🧪 Bloco de Teste Direto
# ============================================================
if __name__ == "__main__":
    """
    Bloco para testar a função de consulta unificada.
    Execute a partir da raiz: python -m servicos.consulta_cnpj
    """
    import sys
    from pathlib import Path
    import json

    sys.path.append(str(Path(__file__).resolve().parent.parent))

    CNPJ_TESTE = "04143008002705"

    print(f">>> Iniciando teste da função 'obter_dados_cnpj' com CNPJ: {CNPJ_TESTE}...")
    try:
        resultado_padronizado = obter_dados_cnpj(CNPJ_TESTE)
        print("\n--- Teste concluído com SUCESSO! ---")
        print("--- Resultado Padronizado: ---")
        print(json.dumps(resultado_padronizado, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"\n--- Teste FALHOU! Erro: {e} ---")
