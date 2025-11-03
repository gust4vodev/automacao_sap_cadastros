# uteis/extrator_documento_tela.py

"""
Módulo com a função especializada para extrair (raspar)
o documento CNPJ ou CPF da tela, com lógica de fallback e retentativas.
"""

import time

# --- Imports de Ferramentas e Assistente ---
from uteis.formatadores import limpar_documento, validar_tamanho_documento
from funcoes.copiar_texto_elemento import copiar_texto_elemento
from uteis.cores import VERDE, VERMELHO, RESET, AMARELO # (Adicionado AMARELO)


def scraping_cnpj_cpf():
    """
    Captura automaticamente o CNPJ ou CPF da tela, alternando entre as duas opções.
    Realiza até 3 tentativas automáticas intercaladas (CNPJ/CPF).
    Caso não consiga identificar nenhum documento válido, solicita ao usuário inserir manualmente.

    Retorna:
        str: Documento limpo (CNPJ com 14 dígitos ou CPF com 11 dígitos).
    """
    
    for tentativa in range(1, 4):
        # --- Tenta capturar CNPJ ---
        try:
            valor_copiado = copiar_texto_elemento("endereco_idfiscais_cnpj")
            if valor_copiado and validar_tamanho_documento(valor_copiado, 14):
                doc_limpo = limpar_documento(valor_copiado)
                print(f"   ✅ CNPJ detectado ({valor_copiado}).")
                return doc_limpo
            
        except Exception as e_cnpj:
            print(f"   {AMARELO}⚠️  Âncora CNPJ não encontrada. Tentando CPF...{RESET}")
        
        # --- Tenta capturar CPF ---
        try:
            time.sleep(1)
            valor_copiado_cpf = copiar_texto_elemento("endereco_idfiscais_cpf")
            if valor_copiado_cpf and validar_tamanho_documento(valor_copiado_cpf, 11):
                doc_limpo = limpar_documento(valor_copiado_cpf)
                print(f"   ✅ CPF detectado ({valor_copiado_cpf}).")
                return doc_limpo
        except Exception as e_cpf:
            print(f"   {AMARELO}⚠️  Âncora CPF não encontrada.{RESET}")

        time.sleep(1)
    # --- Se nenhuma tentativa automática funcionou, aciona input manual ---
    print(f"{VERMELHO}⚠️  Não foi possível capturar automaticamente o CNPJ/CPF após 3 tentativas.{RESET}")
    print(f"{VERMELHO}⚠️  Preencha o valor em sistema e...{RESET}")
    doc_manual = input("    → Informe manualmente o documento e pressione Enter: ")
    return limpar_documento(doc_manual)


# --- Camada de Teste Direto (CORRIGIDA) ---
if __name__ == '__main__':
    """
    Bloco para testar a função 'scraping_cnpj_cpf'.
    Execute a partir da raiz: python -m uteis.extrator_documento_tela
    """
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).resolve().parent.parent))

    from assistente.excecoes import AutomacaoAbortadaPeloUsuario

    print(">>> Iniciando teste da função 'scraping_cnpj_cpf'...") # (Nome corrigido)
    print(">>> Deixe as imagens de CNPJ e CPF visíveis na tela.")
    print(">>> O teste começará em 5 segundos...")
    time.sleep(5)

    try:
        documento = scraping_cnpj_cpf() # (Nome corrigido)
        print("\n--- Teste concluído com SUCESSO! ---")
        print(f"--- Documento obtido: {documento}")

    except AutomacaoAbortadaPeloUsuario:
        print("\n--- Teste ABORTADO pelo usuário. ---")
    except Exception as e:
        print(f"\n--- Teste FALHOU! Erro: {e} ---")