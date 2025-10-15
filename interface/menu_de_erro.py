# interface/menu_de_erro.py

"""Módulo para exibir o menu de interação com o usuário em caso de falha."""

from uteis.cores import VERMELHO, RESET

def exibir_menu_de_falha(nome_processo: str, ultimo_erro: Exception) -> str:
    """
    Exibe um menu de opções para o usuário após falhas consecutivas.

    Args:
        nome_processo (str): O nome amigável da ação que falhou.
        ultimo_erro (Exception): A última exceção capturada que causou a falha.

    Returns:
        str: A escolha do usuário ('tentar', 'ignorar', ou 'abortar').
    """
    # Emoji 💬 para identificar o módulo de interface com o usuário.
    # Mensagem de erro principal em VERMELHO.
    print(f"\n{VERMELHO}💬 [ERRO] Não foi possível executar '{nome_processo}' após 3 tentativas.{RESET}")
    print(f"{VERMELHO}   -> Motivo: {ultimo_erro}{RESET}")

    while True:
        # Descrições e perguntas ao usuário sem cor, como definido no padrão.
        print("\nO que você deseja fazer?")
        print("  1 - Tentar novamente a mesma etapa")
        print("  2 - Ignorar esta etapa e continuar a automação")
        print("  3 - Abortar toda a automação")

        escolha = input("\nDigite o número da sua escolha: ").strip()

        if escolha == '1':
            return 'tentar'
        elif escolha == '2':
            return 'ignorar'
        elif escolha == '3':
            return 'abortar'
        else:
            # Mensagem de erro de opção inválida em VERMELHO.
            print(f"{VERMELHO}Opção inválida. Por favor, digite 1, 2 ou 3.{RESET}")