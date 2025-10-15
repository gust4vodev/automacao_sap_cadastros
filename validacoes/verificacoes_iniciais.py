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
    """Verificação de conexão com as APIs."""
    """
    Executa testes de chamada nas APIs externas. Em caso de falha, imprime
    um erro detalhado e levanta uma exceção para o motor assistente.
    """
    print("⚙️  Verificando conexões com APIs externas...")

    try:
        # Tenta executar todas as verificações em sequência.
        cnpja.consultar_cnpj("04143008002705")
        google.consultar_coordenadas("Avenida Paulista, 1578, São Paulo, SP")

        # Se chegou até aqui, todas as conexões foram bem-sucedidas.
        print(f"    {VERDE}✔ Conexões com as APIs estabelecidas com sucesso.{RESET}")

    except Exception as e:
        # Se QUALQUER uma das chamadas acima falhar, o código pula para cá.
        print(f"    {VERMELHO}✖ Falha na verificação das APIs.{RESET}")
        print(f"    {VERMELHO}  -> Detalhe do erro: {e}{RESET}")

        # Sinaliza a falha para o motor.
        raise