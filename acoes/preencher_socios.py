# acoes/preencher_socios.py

"""
Módulo para a "parede" de ações: preenchimento dos Sócios
na aba Pessoas de Contato.
"""

import time

# --- Imports de Módulos do Projeto ---
from navegacao.navegacao_abas import ir_para_aba
from funcoes.clicar_elemento import clicar_elemento
from funcoes.pressionar_teclas import pressionar_atalho_combinado, pressionar_tecla_unica
from funcoes.colar_texto import colar_texto
from assistente.executor import executar_acao_assistida
from uteis.cores import AMARELO, VERDE, VERMELHO, RESET
    

def preencher_aba_socios(lista_de_socios: list):
    """
    (Orquestradora) Executa o fluxo completo para preencher MÚLTIPLOS sócios
    na aba Pessoas de Contato.
    """
    
    # ============================================================
    # Passo 1: Navegar para Aba Pessoas de Contato
    # ============================================================
    executar_acao_assistida(lambda: ir_para_aba("socio"), nome_acao="Navegar para a Aba Pessoas de Contato (Sócios)")
    time.sleep(3)
    print(f"   - Iniciando o preenchimento de {len(lista_de_socios)} sócio(s)...")


    # ============================================================
    # Passo 2: Clicar novo Socio, e Colar valor
    # ============================================================
    for socio in lista_de_socios:
        try:
            print(f"     - Preenchendo sócio: {VERDE}{socio}{RESET}")
            try:
                colar_texto("pessoascontato_novosocio", socio)
            except Exception:
                colar_texto("pessoascontato_novosocio2", socio)
            time.sleep(1)

    # ============================================================
    # Passo 4: Preencher Sócio ativo SIM
    # ============================================================       
            executar_acao_assistida(lambda: pressionar_atalho_combinado('shift', 'tab', 'tab'), nome_acao="Sair do campo (Shift+Tab)")
            time.sleep(1)
            
            executar_acao_assistida(lambda: pressionar_tecla_unica('y'), nome_acao="Selecionar 'Y' (Sim) para Sócio")
            time.sleep(1)
        
        except Exception as e:
            # (Captura do 'try' EXTERNO)
            # Se AMBOS os cliques falharem, ou se 'colar' falhar, etc.
            print(f"   {VERMELHO}❌ Falha ao preencher o sócio '{socio}': {e}{RESET}")

    print(f"   {VERDE}✅ Preenchimento de sócios concluído.{RESET}")


# --- Camada de Teste Direto ---
if __name__ == '__main__':
    """
    Bloco para testar esta "parede" de forma isolada.
    Execute-a partir da raiz: python -m acoes.preencher_socios
    """
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from assistente.excecoes import AutomacaoAbortadaPeloUsuario

    # --- Lista de Sócios Falsa (para teste) ---
    socios_para_teste = [
        "Gustavo Galhaci (Socio Teste 1)",
        "Socio de Teste 2 (Com Parenteses)",
    ]

    print(">>> Iniciando teste da 'parede': preencher_socios...")
    print(f">>> Testando com {len(socios_para_teste)} sócios FALSOS (LÓGICA REAL).")
    print(">>> ATENÇÃO: O teste tentará NAVEGAR e DIGITAR na tela.")
    print(">>> Garanta que a aba 'Pessoas de Contato' esteja acessível.")
    print(">>> O teste começará em 5 segundos...")
    time.sleep(5)
    
    try:
        # Chama a função orquestradora com os dados falsos
        preencher_aba_socios(socios_para_teste)
        print("\n--- Teste da 'parede' (preencher_socios) concluído com SUCESSO! ---")
    
    except AutomacaoAbortadaPeloUsuario:
        print("\n--- Teste ABORTADO pelo usuário. ---")
    except Exception as e:
        print(f"\n--- Teste da 'parede' FALHOU! Erro: {e} ---")