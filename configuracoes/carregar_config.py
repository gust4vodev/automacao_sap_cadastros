# ============================================================
# 🔑 CARREGAMENTO DE CONFIGURAÇÕES E CHAVES DE API
# ============================================================

# 🌱 Carrega variáveis do arquivo .env
import os
from dotenv import load_dotenv
load_dotenv()

# Nível de confiança padrão para busca de imagens (0.0 a 1.0)
CONFIANCA_PADRAO_IMAGEM = float(os.getenv("DEFAULT_IMAGE_CONFIDENCE", 0.9))

# ============================================================
# 🔑 CHAVES E CONFIGURAÇÕES DE APIS EXTERNAS
# ============================================================

# 🌍 Google Geocode API — Coordenadas geográficas
GOOGLE_GEOCODE_API_KEY = os.getenv("GOOGLE_GEOCODE_API_KEY")

# 🏢 APIs de Consulta de CNPJ — CNPJá
CNPJA_API_URL_PUBLICA = os.getenv("CNPJA_API_URL_PUBLICA")           # Consulta pública geral (dados básicos)
CNPJA_API_URL_COMERCIAL_IE = os.getenv("CNPJA_API_URL_COMERCIAL_IE") # Consulta comercial de Inscrição Estadual (CCC)

# Chave de autenticação para o endpoint comercial (/ccc)
CNPJA_API_KEY_COMERCIAL = os.getenv("CNPJA_API_KEY_COMERCIAL")
CNPJA_API_URL_COMERCIAL_IE_SIMPLES = os.getenv("CNPJA_API_URL_COMERCIAL_IE_SIMPLES")

# ⚙️ Seleção da API principal de CNPJ
# Define qual API será usada como fonte primária de dados.
# Outras APIs podem ser utilizadas para complementar as informações.
# Opções disponíveis:
# 1 → CNPJá (implementada)
# 2 → CnpjWS (a implementar)
# 3 → ReceitaWS (a implementar)
try:
    API_CNPJ_SELECIONADA = int(os.getenv("API_CNPJ_SELECIONADA", "1"))
except ValueError:
    raise ValueError("Valor inválido para API_CNPJ_SELECIONADA no .env. Deve ser um número inteiro.")

# ============================================================
# ⚠️ VALIDAÇÕES ESSENCIAIS
# ============================================================

if not GOOGLE_GEOCODE_API_KEY:
    raise ValueError("A chave GOOGLE_GEOCODE_API_KEY não foi encontrada no .env")

if not CNPJA_API_URL_PUBLICA:
    raise ValueError("A URL CNPJA_API_URL_PUBLICA não foi encontrada no .env")

if not CNPJA_API_URL_COMERCIAL_IE:
    raise ValueError("A URL CNPJA_API_URL_COMERCIAL_IE não foi encontrada no .env")

if not CNPJA_API_KEY_COMERCIAL:
    raise ValueError("A chave CNPJA_API_KEY_COMERCIAL não foi encontrada no .env")

# Valida se a API principal selecionada está entre as suportadas
APIS_SUPORTADAS = {1}  # Por enquanto, só suportamos a API 1 (CNPJá Pública)
if API_CNPJ_SELECIONADA not in APIS_SUPORTADAS:
    raise ValueError(f"API_CNPJ_SELECIONADA ({API_CNPJ_SELECIONADA}) não é suportada. APIs válidas: {APIS_SUPORTADAS}")
