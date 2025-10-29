# funcoes/localizar_elemento.py

"""
Módulo para a função de mais baixo nível: localizar um elemento na tela.
"""

import json
import pyautogui
from pathlib import Path
from typing import Tuple, Dict, Any
from configuracoes.carregar_config import CONFIANCA_PADRAO_IMAGEM

# 1. Define constantes de caminho: projeto raiz e localização do `parametros.json`.
CAMINHO_PROJETO = Path(__file__).resolve().parent.parent
CAMINHO_JSON = CAMINHO_PROJETO / "parametros.json"

def localizar_elemento(nome_chave: str, confianca_override: float = None) -> Tuple[pyautogui.Point, Dict[str, Any]]:
    """
    Localiza um elemento na tela com base em seu nome de chave e retorna sua posição e metadados.

    A função busca as informações do elemento no arquivo `parametros.json`, carrega o caminho da
    imagem associada e utiliza o PyAutoGUI para localizar o centro dessa imagem na tela. Caso a
    imagem não seja encontrada ou os dados estejam inconsistentes, uma exceção é levantada.

    Args:
        nome_chave (str): Nome da chave do elemento no arquivo `parametros.json`.
        confianca_override (float, optional): Valor de confiança (entre 0 e 1) que substitui
        o padrão definido em `CONFIANCA_PADRAO_IMAGEM`.

    Returns:
        Tuple[pyautogui.Point, Dict[str, Any]]:
            Um par contendo:
            - A posição central do elemento localizado na tela.
            - O dicionário de dados correspondentes à chave no JSON.

    Raises:
        FileNotFoundError: Se o arquivo `parametros.json` ou a imagem do elemento não existirem.
        KeyError: Se a chave ou propriedades esperadas não forem encontradas no JSON.
        pyautogui.ImageNotFoundException: Se o elemento não for localizado na tela."""

    # 2. Abre e carrega o arquivo JSON com todos os elementos definidos.
    try:
        with open(CAMINHO_JSON, 'r', encoding='utf-8') as f:
            dados_json_completo = json.load(f)

    # 3. Levanta erro se o arquivo `parametros.json` não for encontrado.
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo de elementos não encontrado: {CAMINHO_JSON}")

    # 4. Busca os dados do elemento pela chave informada; levanta KeyError se não existir.
    dados_elemento = dados_json_completo.get(nome_chave)
    if not dados_elemento:
        raise KeyError(f"Chave '{nome_chave}' não encontrada no parametros.json.")

    # 5. Extrai o caminho relativo da imagem do elemento; levanta erro se ausente.
    caminho_imagem_relativo = dados_elemento.get("path")
    if not caminho_imagem_relativo:
        raise KeyError(f"Propriedade 'path' não encontrada para a chave '{nome_chave}'.")

    # 6. Constrói o caminho absoluto da imagem e verifica se o arquivo existe.
    caminho_imagem_absoluto = CAMINHO_PROJETO / caminho_imagem_relativo
    if not caminho_imagem_absoluto.exists():
        raise FileNotFoundError(f"Arquivo de imagem não encontrado: {caminho_imagem_absoluto}")

    # 7. Determina o nível de confiança a usar: override ou valor padrão da configuração.
    confianca_a_usar = confianca_override if confianca_override is not None else CONFIANCA_PADRAO_IMAGEM

    # 8. Tenta localizar o centro da imagem na tela com `pyautogui.locateCenterOnScreen`.
    try:
        posicao = pyautogui.locateCenterOnScreen(str(caminho_imagem_absoluto), confidence=confianca_a_usar)

    # 9. Se a posição for `None`, força uma exceção `ImageNotFoundException`.
        if posicao is None:
            raise pyautogui.ImageNotFoundException

    # 10. Captura `ImageNotFoundException` e relança com mensagem clara, incluindo nome e caminho da imagem.
    except pyautogui.ImageNotFoundException:
        raise pyautogui.ImageNotFoundException(
            f"Elemento '{nome_chave}' (imagem: {caminho_imagem_relativo}) não foi encontrado na tela."
        )
    
    # 11. Retorna a posição (Point) e os dados completos do elemento do JSON.
    return posicao, dados_elemento

# --- Camada de Teste Direto ---
if __name__ == '__main__':
    """
    Bloco para testar a função localizar_elemento de forma isolada.
    Execute-o a partir da raiz do projeto com: python -m funcoes.localizar_elemento
    """
    import time
    
    # --- AJUSTE AQUI ---
    # Coloque o nome exato de uma chave que existe no seu parametros.json
    CHAVE_PARA_TESTAR = "tela_cadastro_parceirodeneg" 
    # ------------------

    print(">>> Iniciando teste da função localizar_elemento...")
    print(f">>> Tentando localizar a chave: '{CHAVE_PARA_TESTAR}'")
    print(">>> ATENÇÃO: Garanta que a imagem correspondente a esta chave esteja VISÍVEL na tela e devidamente registrada no parametros.json.")
    print(">>> O teste começará em 5 segundos...")
    time.sleep(5)

    try:
        print(f"--- Tentando localizar o elemento '{CHAVE_PARA_TESTAR}' na tela...")
        
        # A função é chamada com a CHAVE
        posicao, dados = localizar_elemento(CHAVE_PARA_TESTAR)
        
        print("--- Teste concluído com SUCESSO! ---")
        print(f"Posição encontrada: {posicao}")
        print(f"Dados do elemento: {dados}")

    except FileNotFoundError as e:
        print(f"--- Teste FALHOU! Arquivo não encontrado: {e}")
    except KeyError as e:
        print(f"--- Teste FALHOU! Erro na chave ou parâmetro do JSON: {e}")
    except pyautogui.ImageNotFoundException as e:
        # A exceção da sua função (Passo 10) será capturada aqui
        print(f"--- Teste FALHOU! Imagem não encontrada na tela: {e}")
    except Exception as e:
        print(f"--- Teste FALHOU! Erro inesperado: {type(e).__name__}: {e}")