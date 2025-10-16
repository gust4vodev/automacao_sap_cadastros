# configuracoes/carregar_config.py

"""Módulo para carregar e disponibilizar as variáveis de ambiente."""

import os
from dotenv import load_dotenv

# Documentação da Função:
# A função load_dotenv() lê o arquivo .env no diretório do projeto
# e carrega as variáveis definidas nele como variáveis de ambiente do sistema.
# Isso permite que os.getenv() possa acessá-las.
load_dotenv()

# --- Chaves de API ---
# Busca o valor associado à chave "GOOGLE_GEOCODE_API_KEY" nas variáveis
# de ambiente e o armazena na constante API_KEY_GOOGLE.
API_KEY_GOOGLE = os.getenv("GOOGLE_GEOCODE_API_KEY")

# Busca o valor da URL base da API do CNPJá.
URL_CNPJA = os.getenv("CNPJA_API_URL")

# --- Configuração de Imagens ---
CONFIANCA_PADRAO_IMAGEM = float(os.getenv("DEFAULT_IMAGE_CONFIDENCE", 0.9))

# --- Validação de Carga ---
# Verifica se a constante API_KEY_GOOGLE está vazia ou nula.
# Se estiver, significa que a variável não foi encontrada no .env,
# e o programa é interrompido com uma mensagem de erro clara.
if not API_KEY_GOOGLE:
    raise ValueError(
        "Erro Crítico: A chave 'GOOGLE_GEOCODE_API_KEY' não foi encontrada no arquivo .env."
    )

# Faz o mesmo para a URL do CNPJá.
if not URL_CNPJA:
    raise ValueError(
        "Erro Crítico: A URL 'CNPJA_API_URL' não foi encontrada no arquivo .env."
    )