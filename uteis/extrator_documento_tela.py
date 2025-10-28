# uteis/extrator_documento_tela.py

"""
Módulo com a função especializada para extrair (raspar)
o documento CNPJ ou CPF da tela, com lógica de fallback e retentativas.
"""

import time

# --- Imports de Ferramentas e Assistente ---
from funcoes.copiar_texto_elemento import copiar_texto_elemento
from assistente.executor import executar_acao_assistida
from uteis.cores import VERDE, VERMELHO, RESET # Para logs de erro internos


def obter_documento_tela_com_fallback() -> str:
    """
    Tenta obter CNPJ ou CPF da tela, com 3 tentativas gerais.

    Ordem de tentativa: CNPJ -> CPF.
    Cada tentativa de cópia individual é gerenciada pelo motor executor.

    Returns:
        str: O documento (CNPJ ou CPF) encontrado e copiado.

    Raises:
        ValueError: Se nenhum documento puder ser obtido após 3 tentativas gerais.
        Exception: Propaga exceções do motor se o usuário abortar.
    """
    documento_encontrado = ""
    for tentativa_geral in range(1, 4):  # 3 tentativas gerais
        try:
            # Tenta CNPJ
            doc = executar_acao_assistida(
                lambda: copiar_texto_elemento("endereco_idfiscais_cnpj"),
                nome_acao=f"[Tentativa {tentativa_geral}] Copiar CNPJ"
            )
            # Verifica se o motor retornou algo (não None e não vazio)
            if doc:
                documento_encontrado = doc
                break # Sucesso, sai do loop for
        except Exception as e_cnpj:
             # Se executar_acao_assistida levantou erro (ex: usuário abortou),
             # ou se copiar_texto_elemento levantou erro inesperado.
            print(f"   {VERMELHO}- Falha crítica ao tentar obter CNPJ (detalhe: {e_cnpj}). Tentando CPF...{RESET}")
            # Não relança o erro aqui, permite tentar o CPF

        # Só tenta CPF se o CNPJ falhou OU se o motor retornou None (usuário ignorou)
        if not documento_encontrado:
            try:
                # Tenta CPF
                doc = executar_acao_assistida(
                    lambda: copiar_texto_elemento("endereco_idfiscais_cpf"),
                    nome_acao=f"[Tentativa {tentativa_geral}] Copiar CPF"
                )
                if doc:
                     documento_encontrado = doc
                     break # Sucesso, sai do loop for
            except Exception as e_cpf:
                print(f"   {VERMELHO}- Falha crítica ao tentar obter CPF (detalhe: {e_cpf}).{RESET}")
                # Não relança, permite próxima tentativa geral

        # Se encontrou documento (CNPJ ou CPF), sai do loop
        if documento_encontrado:
            break

        # Se não encontrou, imprime aviso e continua para próxima tentativa geral
        print(f"   - Nenhum documento encontrado na Tentativa Geral {tentativa_geral}.")
        if tentativa_geral < 3:
            time.sleep(1) # Pausa antes da próxima tentativa geral

    # Se após 3 TENTATIVAS GERAIS nenhum documento foi encontrado, falha.
    if not documento_encontrado:
        raise ValueError("Não foi possível obter CNPJ ou CPF da tela após 3 tentativas gerais.")

    print(f"   - Documento obtido da tela: '{VERDE}{documento_encontrado}{RESET}'.")
    return documento_encontrado


# --- Camada de Teste Direto ---
if __name__ == '__main__':
    """
    Bloco para testar a função 'obter_documento_tela_com_fallback'.
    Execute a partir da raiz: python -m uteis.extrator_documento_tela
    """
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).resolve().parent.parent))

    from assistente.excecoes import AutomacaoAbortadaPeloUsuario

    print(">>> Iniciando teste da função 'obter_documento_tela_com_fallback'...")
    print(">>> Deixe as imagens de CNPJ e CPF visíveis na tela.")
    print(">>> O teste começará em 5 segundos...")
    time.sleep(5)

    try:
        documento = obter_documento_tela_com_fallback()
        print("\n--- Teste concluído com SUCESSO! ---")
        print(f"--- Documento obtido: {documento}")

    except AutomacaoAbortadaPeloUsuario:
        print("\n--- Teste ABORTADO pelo usuário. ---")
    except Exception as e:
        print(f"\n--- Teste FALHOU! Erro: {e} ---")