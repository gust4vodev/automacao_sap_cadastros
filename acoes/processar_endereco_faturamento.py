# acoes/processar_endereco_faturamento.py

"""
Módulo para a "parede" de ações: processar o endereço de faturamento,
obter coordenadas e atualizar a tabela.
"""

import time
import pandas as pd
import re
import pyperclip

# --- Imports de Módulos do Projeto ---
from funcoes.clicar_com_botao_direito import clicar_com_botao_direito
from funcoes.pressionar_teclas import pressionar_tecla_unica, pressionar_atalho_combinado
from funcoes.clicar_elemento import clicar_elemento
from uteis.processador_tabela_clipboard import ler_tabela_clipboard_para_dataframe, converter_dataframe_para_string_tabulada
from servicos.api_google import consultar_coordenadas
# NOVOS IMPORTS: Funções auxiliares extraídas
from uteis.validadores import validar_tabela_endereco           
from uteis.formatadores import formatar_endereco_para_api # <- Nova função
from assistente.executor import executar_acao_assistida
from uteis.cores import VERMELHO, RESET, AMARELO


def processar_endereco_faturamento():
    """(Orquestradora) Executa o fluxo completo para processar o Endereço Faturamento."""

    # ============================================================
    # Passo 1: Copiar Tabela de Endereço
    # ============================================================
    executar_acao_assistida(lambda: clicar_com_botao_direito("enderecos_tabela"), nome_acao="Clicar com botão direito na Tabela de Endereços")
    time.sleep(1)
    executar_acao_assistida(lambda: pressionar_tecla_unica('t'), nome_acao="Pressionar tecla 'T' para Copiar Tabela de Endereço")
    time.sleep(1)

    # ============================================================
    # Passo 2: Ler Tabela do Clipboard
    # ============================================================
    df_endereco: pd.DataFrame = executar_acao_assistida(
        ler_tabela_clipboard_para_dataframe,
        nome_acao="Ler tabela de endereço do clipboard"
    )

    # ============================================================
    # Passo 3: Validar Campos Essenciais (USA FUNÇÃO AUXILIAR)
    # ============================================================
    try:
        validar_tabela_endereco(df_endereco) # Chama a função de uteis/validadores.py
    except ValueError as val_err:
         raise val_err # Re-levanta para o motor executor

    # ============================================================
    # Passo 4: Extrair Endereço para API (USA FUNÇÃO AUXILIAR)
    # ============================================================
    try:
        primeira_linha = df_endereco.iloc[0]
        endereco_para_api = formatar_endereco_para_api(primeira_linha) # Chama a função de uteis/formatadores.py
    except Exception as e:
        raise RuntimeError(f"Erro ao preparar endereço para API: {e}")

    # ============================================================
    # Passo 5: Consultar Coordenadas
    # ============================================================
    latitude = None
    longitude = None
    try:
        lat, lon = executar_acao_assistida(
            lambda: consultar_coordenadas(endereco_para_api),
            nome_acao=f"Consultar coordenadas para '{endereco_para_api}'"
        )
        latitude = lat; longitude = lon
        print(f"    ✅ Coordenadas obtidas: Lat={latitude}, Lon={longitude}")
    except Exception as e:
        print(f"    {AMARELO}⚠️ Aviso: Falha ao obter coordenadas: {e}{RESET}")

    # ============================================================
    # Passo 6: Formatar Coordenadas e Atualizar DataFrame
    # ============================================================

    lat_formatada = ""; lon_formatada = ""
    try:
        if latitude is not None and longitude is not None:
            
            # --- NOVO PASSO: Truncar os valores para 5 casas decimais ---
            # Ex: -15.7534813 -> -15.75348
            # Ex: -47.7791001 -> -47.7791 (ou -47.77910)
            
            # 1. Multiplica por 100_000 (move 5 casas decimais)
            # 2. Converte para int() (corta/ignora o resto)
            # 3. Divide por 100_000.0 (retorna as 5 casas decimais)
            lat_truncada = int(latitude * 100_000) / 100_000.0
            lon_truncada = int(longitude * 100_000) / 100_000.0
            
            # --- FIM DO NOVO PASSO ---

            # 1. Cria as strings formatadas (com vírgula)
            #    Usamos :.5f para garantir que valores como ,7791 sejam impressos como ,77910
            lat_formatada = f"{lat_truncada:.5f}".replace('.', ',')
            lon_formatada = f"{lon_truncada:.5f}".replace('.', ',')

        # 2. Guarda os NÚMEROS (floats) TRUNCADOS no DataFrame
        #    (Isto resolve o FutureWarning e usa os 5 decimais)
        df_endereco.loc[0, 'Latitude'] = lat_truncada
        df_endereco.loc[0, 'Longitude'] = lon_truncada

        # 3. O print usa as strings formatadas (com 5 casas)
        print(f"     ✅ DataFrame atualizado: Lat='{lat_formatada}', Lon='{lon_formatada}'")
        
    except Exception as e:
            raise RuntimeError(f"Erro ao atualizar DataFrame com coordenadas: {e}")
   # ============================================================
    # Passo 7: Reformatar DataFrame para String Tabulada
    # ============================================================
    print("   - Convertendo tabela atualizada de volta para formato de clipboard...")
    try:
        # --- CORREÇÃO AQUI ---
        # Chama a função correta: converter_dataframe_para_string_tabulada
        # Passa o DataFrame modificado (df_endereco) como argumento
        tabela_formatada_string: str = executar_acao_assistida(
            lambda: converter_dataframe_para_string_tabulada(df_endereco),
            nome_acao="Formatar tabela de endereço para área de transferência"
        )
        # --- FIM DA CORREÇÃO ---

        # Verifica se a conversão retornou uma string válida
        if not tabela_formatada_string:
             raise ValueError("Função de formatação retornou string vazia.")

        print("    ✅ Tabela reformatada com sucesso.")

    except Exception as e:
        # Captura erros da conversão ou se a string for vazia
        erro_msg = f"Erro ao reformatar a tabela para colar: {e}"
        print(f"    {VERMELHO}❌ ERRO: {erro_msg}{RESET}")
        raise RuntimeError(erro_msg) # Levanta erro para o motor
    # ============================================================
    # Passo 8: Colar Tabela de Volta no SAP
    # ============================================================
    print("   - Preparando para colar a tabela no SAP...")
    try:
        pyperclip.copy(tabela_formatada_string)
        time.sleep(0.3)
        print("    - Tabela copiada para clipboard.")
        executar_acao_assistida(lambda: clicar_elemento("enderecos_idfaturamento"), nome_acao="Clicar na área da tabela para colar")
        time.sleep(0.5)
        executar_acao_assistida(lambda: pressionar_atalho_combinado('ctrl', 'v'), nome_acao="Colar tabela atualizada (Ctrl+V)")
        time.sleep(1)
        executar_acao_assistida(lambda: pressionar_atalho_combinado('enter'), nome_acao="Colar tabela atualizada (Ctrl+V)")
        time.sleep(1)
        print("    ✅ Tabela colada.")
    except Exception as e:
        raise RuntimeError(f"Erro ao colar a tabela de volta no SAP: {e}")


# --- Camada de Teste Direto ---
if __name__ == '__main__':
    # ... (imports sys, Path, excecoes) ...
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from assistente.excecoes import AutomacaoAbortadaPeloUsuario

    print(">>> Iniciando teste da 'parede': processar_endereco_faturamento...")
    print(">>> Testando Passos 1 a 3 (Copiar, Ler, Validar)...") # Mensagem atualizada
    print(">>> Certifique-se de que a âncora 'enderecos_tabela' esteja visível.")
    print(">>> O teste começará em 5 segundos...")
    time.sleep(5)

    try:
        processar_endereco_faturamento()
        print("\n--- Teste da 'parede' (Passos 1 a 3) concluído com SUCESSO! ---")
        # (Opcional: Verificar DataFrame lido)

    except AutomacaoAbortadaPeloUsuario:
        print("\n--- Teste ABORTADO pelo usuário. ---")
    except Exception as e:
        print(f"\n--- Teste da 'parede' FALHOU! Erro: {e} ---")