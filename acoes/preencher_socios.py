# acoes/preencher_socios.py

"""
Módulo para a ação de ações: preenchimento dos Sócios
na aba Pessoas de Contato.
(Refatorado para consumir dados do 'gestor_sessao.json')
"""

import time
from navegacao.navegacao_abas import ir_para_aba
from funcoes.clicar_elemento import clicar_elemento
from funcoes.pressionar_teclas import pressionar_atalho_combinado, pressionar_tecla_unica
from funcoes.colar_texto import colar_texto
from assistente.executor import executar_acao_assistida
from uteis.cores import AMARELO, VERDE, VERMELHO, RESET
from uteis.gestor_sessao import ler_dados_sessao


def preencher_aba_socios():
    """
    (Orquestradora/Consumidor) Executa o fluxo para preencher MÚLTIPLOS sócios.
    
    Lê o 'dados_sessao.json' para verificar se é CNPJ e se há sócios
    antes de executar a navegação e o preenchimento.
    """
    
    # ============================================================
    # Passo 1: Ler Sessão e Validar Lógica
    # ============================================================
    dados_sessao = ler_dados_sessao()
    
    tipo_pessoa = dados_sessao.get("tipo_pessoa", 0)
    lista_de_socios = dados_sessao.get("socios", [])

    if tipo_pessoa != 2 or not lista_de_socios:
        if tipo_pessoa != 2:
            print(f"   {AMARELO}Documento não é CNPJ).{RESET}")
        else:
            print(f"   {AMARELO}Nenhum sócio (QSA) encontrado.{RESET}")
        return # Encerra esta ação
    

    # ============================================================
    # Passo 2: Navegar para Aba Pessoas de Contato
    # ============================================================
    executar_acao_assistida(lambda: ir_para_aba("socio"), nome_acao="Navegar para a Aba Pessoas de Contato (Sócios)")
    time.sleep(1)
    print(f"   - Iniciando o preenchimento de {len(lista_de_socios)} sócio(s)...")


    # ============================================================
    # Passo 3: Loop de Preenchimento
    # ============================================================
    for socio in lista_de_socios:
        try:
            print(f"     - Preenchendo sócio: {VERDE}{socio}{RESET}")
            
            # --- Bloco do Clique - (DENIFIR NOVO)---
            try:
                clicar_elemento("pessoascontato_novosocio")
                time.sleep(1)
            except Exception:
                clicar_elemento("pessoascontato_novosocio2")
                time.sleep(1)
            
            # --- Passo 2: Colar ---
            executar_acao_assistida(lambda: colar_texto('pessoascontato_idsocio', socio), nome_acao=f"Colar nome '{socio}'")
            time.sleep(1)
            
            # --- Passo 3: Shift+Tab ---
            executar_acao_assistida(lambda: pressionar_atalho_combinado('shift', 'tab'), nome_acao="Sair do campo (Shift+Tab)")
            time.sleep(1)

             # --- Passo 4: Shift+Tab novamente---
            executar_acao_assistida(lambda: pressionar_atalho_combinado('shift', 'tab'), nome_acao="Sair do campo (Shift+Tab)")
            time.sleep(1)
            
            # --- Passo 4: 'y' ---
            executar_acao_assistida(lambda: pressionar_tecla_unica('y'), nome_acao="Selecionar 'Y' (Sim) para Sócio")
            time.sleep(1)
        
        except Exception as e:
            print(f"   {VERMELHO}❌ Falha ao preencher o sócio '{socio}': {e}{RESET}")
            time.sleep(1) # Pausa e continua o loop


# --- Camada de Teste Direto
if __name__ == '__main__':
    """
    Bloco para testar esta ação de forma isolada (MODO JSON).
    Execute a partir da raiz: python -m acoes.preencher_socios
    """
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from assistente.excecoes import AutomacaoAbortadaPeloUsuario
    
    # Para testar este módulo, o 'gestor_sessao' deve ser iniciado
    # e o JSON deve ser "preparado" com dados de testes.
    from uteis.gestor_sessao import iniciar_sessao, escrever_dados_sessao, encerrar_sessao

    # 1. Preparar os dados falsos
    socios_para_teste = [
        "Gustavo Galhaci (Socio Teste 1)",
        "Socio de Teste 2 (Com Parenteses)",
    ]
    dados_falsos_sessao = {
        "tipo_pessoa": 2, # Simula um CNPJ
        "socios": socios_para_teste
    }

    # 2. Iniciar a sessão (Cria o JSON)
    iniciar_sessao()
    # 3. Escrever os dados falsos no JSON
    escrever_dados_sessao(dados_falsos_sessao)
    # ---------------------------

    print(">>> Iniciando teste da ação: preencher_socios...")
    print(f">>> (JSON de sessão preparado com {len(socios_para_teste)} sócios de testes)")
    print(">>> ATENÇÃO: O teste tentará NAVEGAR e DIGITAR na tela.")
    print(">>> Garanta que a aba 'Pessoas de Contato' esteja acessível.")
    print(">>> O teste começará em 5 segundos...")
    time.sleep(5)
    
    try:
        # Chama a função (agora sem parâmetros)
        preencher_aba_socios()
        print("\n--- Teste da ação (preencher_socios) concluído com SUCESSO! ---")
    
    except AutomacaoAbortadaPeloUsuario:
        print("\n--- Teste ABORTADO pelo usuário. ---")
    except Exception as e:
        print(f"\n--- Teste da ação FALHOU! Erro: {e} ---")
        
    finally:
        # Limpa o JSON no final do teste
        print("\n--- Encerrando sessão de teste... ---")
        encerrar_sessao()