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

    # 1. Inicia loop de 3 tentativas gerais para obter CNPJ ou CPF da tela. 
    for tentativa_geral in range(1, 4): 

    # 2. Tenta copiar CNPJ via `copiar_texto_elemento` com `executar_acao_assistida`.
        try:
            doc = executar_acao_assistida(lambda: copiar_texto_elemento("endereco_idfiscais_cnpj"),nome_acao=f"[Tentativa {tentativa_geral}] Copiar CNPJ")

    # 3. Se CNPJ for obtido e válido, armazena e interrompe o loop. 
            if doc:
                documento_encontrado = doc
                break # Sucesso, sai do loop for
        except Exception as e_cnpj: # Não relança o erro aqui, permite tentar o CPF
            print(f"   {VERMELHO}- Falha crítica ao tentar obter CNPJ (detalhe: {e_cnpj}). Tentando CPF...{RESET}")


    # 4. Em caso de falha no CNPJ, tenta copiar CPF da mesma forma. 
        if not documento_encontrado:

    # 5. Se CPF for obtido e válido, armazena e interrompe o loop.        
            try:
                doc = executar_acao_assistida(lambda: copiar_texto_elemento("endereco_idfiscais_cpf"), nome_acao=f"[Tentativa {tentativa_geral}] Copiar CPF")
                if doc:
                     documento_encontrado = doc
                     break # Sucesso, sai do loop for
                
    # 6. Registra falha crítica com cor vermelha se ambas as tentativas falharem.             
            except Exception as e_cpf: # Não relança, permite próxima tentativa geral
                print(f"   {VERMELHO}- Falha crítica ao tentar obter CPF (detalhe: {e_cpf}).{RESET}")
                
        # Se encontrou documento (CNPJ ou CPF), sai do loop
        if documento_encontrado:
            break

    # 7. Se não encontrou, imprime aviso e continua para próxima tentativa geral
        print(f"   - Nenhum documento encontrado na Tentativa Geral {tentativa_geral}.")
        if tentativa_geral < 3:
            time.sleep(1) # Pausa antes da próxima tentativa geral

    # 8. Após 3 tentativas sem sucesso, levanta `ValueError`. 
    if not documento_encontrado:
        raise ValueError("Não foi possível obter CNPJ ou CPF da tela após 3 tentativas gerais.")

    # 9. Ao obter documento, exibe com cor verde e retorna o valor.  
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