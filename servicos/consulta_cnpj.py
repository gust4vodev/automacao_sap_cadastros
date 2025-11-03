# ============================================================
# 📦 servicos/consulta_cnpj.py
# ============================================================
"""
Módulo responsável por unificar e padronizar consultas de dados de CNPJ,
utilizando a API Comercial unificada (/office/) e escrevendo os dados
no ficheiro de sessão JSON.
"""

from typing import Dict, Any, List
from uteis.extrator_json import extrair_dado_json
from uteis.cores import VERDE, RESET, AMARELO
from uteis.formatadores import limpar_documento, limpar_cep, separar_tipo_logradouro
from servicos.api_cnpja_comercial_ie_simples import consultar_cnpj_completo
from uteis.gestor_sessao import ler_dados_sessao, escrever_dados_sessao

# ============================================================
# 🚀 Função Principal
# ============================================================
def obter_dados_cnpj(cnpj: str) -> Dict[str, Any]:
    """
    Obtém dados de um CNPJ, usando o cache da sessão JSON e a API Comercial.
    Escreve o resultado no dados_sessao.json e retorna o dicionário padronizado.
    """
    
    cnpj_chave = limpar_documento(cnpj)

    # --- Verificação de Cache (Lendo do JSON) ---
    dados_sessao_atuais = ler_dados_sessao()
    if dados_sessao_atuais.get("documento_consultado") == cnpj_chave:
        return dados_sessao_atuais
    

    # --- Inicialização ---
    # (Obtém o template VAZIO da sessão para preencher)
    # (Isto garante que não estamos a misturar dados de um CNPJ antigo)
    dados_padronizados = ler_dados_sessao() # <-- Começa com o template
    
    # (Mantém apenas os dados do template, limpa dados antigos se houver)
    dados_padronizados = {
        "status_cnpj": "", "razao_social": "", "data_abertura": "",
        "inscricao_estadual": "Isento", "simples_nacional": None,
        "socios": [],
        "endereco": {
            "tipo_logradouro": "", "logradouro": "", "numero": "",
            "complemento": "", "bairro": "", "cep": "",
            "cidade": "", "estado": ""
        },
        "tipo_pessoa": dados_sessao_atuais.get("tipo_pessoa", 0) # Mantém o tipo_pessoa
    }


    # ============================================================
    # 🧩 Etapa 1 — Consulta Unificada
    # ============================================================
    dados_brutos = {} # O JSON que vem da API
    try:
        dados_brutos = consultar_cnpj_completo(cnpj_chave)
        
    except Exception as e:
        print(f"⚠️ Aviso: Falha crítica ao consultar a API Comercial (/office/): {e}")
        raise e

    # ============================================================
    # 🧩 Etapa 2 — Mapeamento dos Dados Cadastrais
    # ============================================================
    try:
        dados_padronizados["razao_social"] = extrair_dado_json(dados_brutos, "company.name")
        dados_padronizados["data_abertura"] = extrair_dado_json(dados_brutos, "founded")
        dados_padronizados["status_cnpj"] = extrair_dado_json(dados_brutos, "status.text")
        dados_padronizados["simples_nacional"] = extrair_dado_json(
            dados_brutos, "company.simples.optant", padrao=None
        )

        # Endereço
        logradouro_completo = extrair_dado_json(dados_brutos, "address.street")
        tipo_log, nome_log = separar_tipo_logradouro(logradouro_completo)
        endereco = dados_padronizados["endereco"]
        endereco["tipo_logradouro"] = tipo_log or ""
        endereco["logradouro"] = nome_log or ""
        endereco["numero"] = extrair_dado_json(dados_brutos, "address.number")
        endereco["complemento"] = extrair_dado_json(dados_brutos, "address.details")
        endereco["bairro"] = extrair_dado_json(dados_brutos, "address.district")
        endereco["cep"] = limpar_cep(extrair_dado_json(dados_brutos, "address.zip"))
        endereco["cidade"] = extrair_dado_json(dados_brutos, "address.city")
        endereco["estado"] = extrair_dado_json(dados_brutos, "address.state")

        # Sócios
        socios_brutos = dados_brutos.get("company", {}).get("members", [])
        dados_padronizados["socios"] = [m["person"]["name"] for m in socios_brutos]
    except Exception as e:
        print(f"⚠️ Aviso: Falha ao mapear dados cadastrais (Razão, Endereço, Sócios): {e}")
    
    # ============================================================
    # 🧩 Etapa 3 — [REGRA: CANDIDATO A SUFRAMA]
    # ============================================================
    try:
        uf = dados_padronizados["endereco"].get("estado", "").upper()
        cidade = dados_padronizados["endereco"].get("cidade", "").strip().lower()
        status_cnpj = (dados_padronizados.get("status_cnpj") or "").lower()

        estados_suframa = {"AM", "AC", "AP", "RO", "RR"}
        municipios_alc = {
            "cruzeiro do sul", "epitaciolandia", "brasileia",
            "macapa", "santana", "guajara-mirim", "boa vista", "bonfim", "tabatinga"
        }
        cnaes_candidatos = [
            "comércio", "industr", "import", "export", "transformação", "produção"
        ]
        cnae_texto = (dados_brutos.get("mainActivity", {}).get("text", "") or "").lower()

        if (
            status_cnpj == "ativa"
            and uf in estados_suframa
            and (
                any(palavra in cnae_texto for palavra in cnaes_candidatos)
                or cidade in municipios_alc
            )
        ):
            print(f"\n{AMARELO}🚩 Possível empresa com benefício SUFRAMA detectada.{RESET}")
            print(f"{AMARELO}→ {dados_padronizados['razao_social']} ({uf} - {cidade.title()}){RESET}")
            print(f"{AMARELO}⚠️ Interrompendo o fluxo para verificação manual da inscrição SUFRAMA.{RESET}\n")
            input("Pressione ENTER para continuar após verificar manualmente no site da SUFRAMA...")
    except Exception as e:
        print(f"⚠️ Falha ao avaliar regra SUFRAMA: {e}")

    # ============================================================
    # 🧩 Etapa 4 — Mapeamento da Inscrição Estadual
    # ============================================================
    try:
        estado_empresa = dados_padronizados["endereco"]["estado"]
        inscricao_estadual_valida = "Isento"
        registrations: List[Dict] = extrair_dado_json(dados_brutos, "registrations", padrao=[])
        
        if estado_empresa:
            for registro in registrations:
                ie_numero = extrair_dado_json(registro, "number")
                ie_estado = extrair_dado_json(registro, "state")
                ie_ativa = extrair_dado_json(registro, "enabled", padrao=False)

                if ie_numero and ie_estado and ie_ativa and ie_estado.upper() == estado_empresa.upper():
                    print(f"     -> IE encontrada: {VERDE}{ie_numero}/{ie_estado} (Ativa){RESET}")
                    inscricao_estadual_valida = ie_numero
                    break
        else:
            print("   - Não foi possível validar a IE (estado da empresa não encontrado nos dados gerais).")

        dados_padronizados["inscricao_estadual"] = inscricao_estadual_valida

    except Exception as e:
        print(f"⚠️ Aviso: falha ao mapear inscrição estadual: {e}")


    # ============================================================
    # 🕒 Finalização (ESCREVENDO NO JSON)
    # ============================================================
    # (Adiciona o CNPJ consultado para a verificação de cache)
    dados_padronizados["documento_consultado"] = cnpj_chave
    escrever_dados_sessao(dados_padronizados) 
    return dados_padronizados


# ============================================================
# 🧪 Bloco de Teste Direto
# ============================================================
if __name__ == "__main__":
    """
    Bloco para testar a função de consulta unificada (VERSÃO COMERCIAL).
    Execute a partir da raiz: python -m servicos.consulta_cnpj
    """
    import sys
    from pathlib import Path
    import json
    # (Importa o gestor de sessão para o teste)
    from uteis.gestor_sessao import iniciar_sessao, ler_dados_sessao, encerrar_sessao

    sys.path.append(str(Path(__file__).resolve().parent.parent))

    CNPJ_TESTE = "04143008002705" # CNPJ com dados completos
    
    # Inicia a sessão (cria o JSON)
    iniciar_sessao()

    print(f">>> Iniciando teste da função 'obter_dados_cnpj' (Nova Versão JSON) com CNPJ: {CNPJ_TESTE}...")
    try:
        resultado_padronizado = obter_dados_cnpj(CNPJ_TESTE)
        print("\n--- Teste concluído com SUCESSO! ---")
        print("--- Resultado Padronizado (Mapeado): ---")
        print(json.dumps(resultado_padronizado, indent=2, ensure_ascii=False))

        print("\n--- Teste da função 'ler_dados_sessao' ---")
        dados_do_json = ler_dados_sessao()
        socios_do_cache = dados_do_json.get("socios")
        print(f"Sócios obtidos do JSON: {socios_do_cache}")

    except Exception as e:
        print(f"\n--- Teste FALHOU! Erro: {e}")
    
    finally:
        # Limpa o JSON no final do teste
        encerrar_sessao()