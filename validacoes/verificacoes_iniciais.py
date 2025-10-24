# validacoes/verificacoes_iniciais.py

"""
Módulo responsável por executar todas as verificações de "prontidão"
do ambiente antes do início da automação principal.
"""

# --- Imports de Módulos do Projeto ---
import servicos.api_cnpja_publica as cnpja_publica
import servicos.api_google as google
from uteis.sincronizador_assets import sincronizar_json_com_pasta_assets
from uteis.cores import VERDE, VERMELHO, RESET


def executar_verificacoes_iniciais():
    """Verificações iniciais do ambiente de automação."""
    """
    Orquestra todas as checagens necessárias para garantir que a automação
    possa ser executada com segurança. Isso inclui:
    1. Sincronizar os assets (JSON e imagens).
    2. Verificar a conexão com as APIs externas.

    Levanta uma exceção em caso de qualquer falha.
    """
    print("⚙️  Executando verificações iniciais do ambiente...")

    try:
        # ETAPA 1: Sincroniza o JSON com a pasta de imagens.
        sincronizar_json_com_pasta_assets()

        # ETAPA 2: Verifica a conexão com as APIs externas.
        #cnpja_publica.consultar_cnpj("04143008002705")
        google.consultar_coordenadas("Avenida Paulista, 1578, São Paulo, SP")

        # Se chegou até aqui, todas as verificações passaram.
        print(f"    {VERDE}✔ Ambiente verificado e pronto para execução.{RESET}")

    except Exception as e:
        # Se QUALQUER etapa falhar, o código pula para cá.
        print(f"    {VERMELHO}✖ Falha nas verificações iniciais.{RESET}")
        print(f"    {VERMELHO}  -> Detalhe do erro: {e}{RESET}")

        # Sinaliza a falha para o motor assistente.
        raise