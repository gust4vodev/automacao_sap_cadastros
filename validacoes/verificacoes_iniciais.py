# validacoes/verificacoes_iniciais.py

"""
Módulo responsável por executar verificações essenciais do ambiente
antes do início da automação principal.
"""

# --- Imports de Módulos do Projeto ---

import time
from funcoes.localizar_elemento import localizar_elemento
from uteis.sincronizador_assets import sincronizar_json_com_pasta_assets
from uteis.cores import VERDE, VERMELHO, RESET
from uteis.gestor_sessao import iniciar_sessao


def executar_verificacoes_iniciais():
    """Verificações iniciais do ambiente de automação."""
    """
    Orquestra as checagens essenciais:
    1. Sincroniza os assets (JSON e imagens).
    2. Verifica se a tela inicial do Cadastro de PN está visível.

    Levanta uma exceção em caso de qualquer falha.
    """
    try:
        # ETAPA 1: Sincroniza o JSON com a pasta de imagens.
        iniciar_sessao()
        print(f"    {VERDE}✔ Sessão iniciada.{RESET}")

        # ETAPA 2: Sincroniza o JSON com a pasta de imagens.
        sincronizar_json_com_pasta_assets()
        print(f"    {VERDE}✔ Assets sincronizados.{RESET}")

        # ETAPA 3: Verifica se a tela inicial está visível.
        chave_tela_inicial = "tela_cadastro_parceirodeneg"
        localizar_elemento(chave_tela_inicial)
        print(f"    {VERDE}✔ Tela inicial encontrada.{RESET}")

        # Se chegou até aqui, todas as verificações passaram.
        print(f"    {VERDE}✔ Ambiente verificado e pronto para execução.{RESET}")

    except FileNotFoundError as fnf_err:
         # Erro específico se o JSON ou imagem não for encontrado durante a localização
         print(f"    {VERMELHO}✖ Falha na verificação: Arquivo essencial não encontrado.{RESET}")
         print(f"    {VERMELHO}  -> Detalhe: {fnf_err}{RESET}")
         raise # Re-levanta para o Assistente executor executor

    except KeyError as key_err:
         # Erro específico se a chave da tela inicial não estiver no JSON
         print(f"    {VERMELHO}✖ Falha na verificação: Chave da tela inicial não encontrada no JSON.{RESET}")
         print(f"    {VERMELHO}  -> Detalhe: {key_err}{RESET}")
         raise # Re-levanta para o Assistente executor executor

    except pyautogui.ImageNotFoundException as img_err: # Import pyautogui if needed at top
         # Erro específico se a imagem da tela inicial não for encontrada na tela
         print(f"    {VERMELHO}✖ Falha na verificação: Tela inicial do cadastro NÃO encontrada.{RESET}")
         print(f"    {VERMELHO}  -> Detalhe: {img_err}{RESET}")
         print(f"    {VERMELHO}  -> Certifique-se que a janela correta do SAP está aberta e visível.{RESET}")
         raise # Re-levanta para o Assistente executor executor

    except Exception as e:
        # Captura qualquer outro erro inesperado
        print(f"    {VERMELHO}✖ Falha inesperada nas verificações iniciais.{RESET}")
        print(f"    {VERMELHO}  -> Detalhe do erro: {e}{RESET}")
        raise # Re-levanta para o Assistente executor executor

# (O bloco de teste __main__ pode ser ajustado para refletir a nova lógica, se necessário)
if __name__ == '__main__':
    import sys, pyautogui # Adicionado pyautogui para o except
    from pathlib import Path
    sys.path.append(str(Path(__file__).resolve().parent.parent))

    print(">>> Iniciando teste das verificações iniciais...")
    print(">>> O teste começará em 3 segundos...")
    time.sleep(3)
    try:
        executar_verificacoes_iniciais()
        print("\n--- Teste concluído com SUCESSO! ---")
    except Exception as e:
        print(f"\n--- Teste FALHOU! Erro: {e} ---")