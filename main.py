# main.py

"""
Ponto de entrada principal da aplicação de automação SAP B1.
Este script inicializa a aplicação, carrega as configurações e, futuramente,
dará início ao fluxo de automação selecionado pelo usuário.
"""

# --- Imports ---
# Importa os módulos de serviço para que suas funções possam ser utilizadas.
# Damos um apelido (alias) para facilitar a chamada (ex: cnpja.consultar_cnpj).
import servicos.api_cnpja as cnpja
import servicos.api_google as google

# Importa o módulo de configuração para garantir que as variáveis de ambiente
# sejam carregadas assim que a aplicação iniciar.
from configuracoes import carregar_config


def principal():
    """Função que contém a lógica principal e orquestração da automação."""

    print(">>> [INFO] Automação SAP B1 iniciada.")
    print("=" * 40)

    # Etapa 1: Validação de Carga das Configurações
    # Apenas por ter importado 'carregar_config', o .env já foi lido.
    # A linha abaixo serve como um teste para confirmar que a URL foi carregada.
    print(f"[OK] Módulo de configuração carregado. URL do CNPJá: {carregar_config.URL_CNPJA}")

    # Etapa 2: Teste de Conexão com as APIs (bloco de verificação)
    # Este bloco serve para garantir que as funções de serviço estão operacionais.
    try:
        print("\n>>> [TESTE] Realizando chamada de verificação na API CNPJá...")
        # Usamos um CNPJ conhecido apenas para o teste.
        dados = cnpja.consultar_cnpj("04143008002705")
        print(f"[OK] Teste CNPJá bem-sucedido. Razão Social: {dados.get('alias')}")

    except Exception as e:
        print(f"[FALHA] Erro no teste da API CNPJá: {e}")

    print("=" * 40)
    print(">>> [INFO] Estrutura principal pronta. Aguardando implementação do fluxo de automação.")


# --- Ponto de Entrada do Script ---
# A expressão `if __name__ == "__main__":` é um padrão em Python que define
# o ponto de início da execução. O código dentro deste bloco só roda quando
# o arquivo 'main.py' é executado diretamente pelo terminal.
if __name__ == "__main__":
    principal()