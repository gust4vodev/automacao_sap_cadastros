# main.py

"""
Ponto de entrada principal da aplicação de automação SAP B1.
"""

# --- Imports ---
from validacoes.verificacoes_iniciais import testar_conexoes_api
from configuracoes import carregar_config

# Importa as cores necessárias do nosso módulo central de utilitários.
from uteis.cores import AMARELO, RESET


def principal():
    """Função que contém a lógica principal e orquestração da automação."""

    # INICIO
    print(f"{AMARELO}🚀 Automação SAP B1 iniciada...{RESET}")

    # 1. Delega a execução das verificações de sistema.
    testar_conexoes_api()



    # FIM
    print(f"\n{AMARELO}🚀 Automação SAP B1 concluída com sucesso!{RESET}")


if __name__ == "__main__":
    principal()