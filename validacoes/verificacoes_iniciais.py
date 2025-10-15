# validacoes/verificacoes_iniciais.py

"""
Módulo responsável por executar verificações de ambiente e conectividade
antes do início da automação principal.
"""

# --- Imports de Serviços ---
import servicos.api_cnpja as cnpja
import servicos.api_google as google

# --- Imports de Utilitários ---
from uteis.cores import VERDE, VERMELHO, RESET


def testar_conexoes_api():
    """
    Executa testes de chamada nas APIs externas para validar a conexão.
    Imprime o resultado em verde (sucesso) ou vermelho (falha).
    """
    # Emoji ⚙️ identifica que esta mensagem vem do módulo de validações.
    print("\n⚙️  Verificando conexões com APIs externas...")

    # --- Teste 1: API CNPJá ---
    try:
        cnpja.consultar_cnpj("04143008002705") # CNPJ de exemplo
        print(f"    {VERDE}✔ API CNPJá: Conectada{RESET}")

    except Exception as e:
        print(f"    {VERMELHO}✖ API CNPJá: Falha na conexão{RESET}")
        print(f"    {VERMELHO}  -> Detalhe: {e}{RESET}")

    # --- Teste 2: API Google Geocode ---
    try:
        endereco_teste = "Avenida Paulista, 1578, São Paulo, SP"
        google.consultar_coordenadas(endereco_teste)
        print(f"    {VERDE}✔ API Google Geocode: Conectada{RESET}")

    except Exception as e:
        print(f"    {VERMELHO}✖ API Google Geocode: Falha na conexão{RESET}")
        print(f"    {VERMELHO}  -> Detalhe: {e}{RESET}")