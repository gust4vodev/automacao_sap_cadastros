# funcoes/localizar_elemento.py

"""
Módulo para a função de mais baixo nível: localizar um elemento na tela.
"""

import json
import pyautogui
from pathlib import Path
from typing import Tuple, Dict, Any

# --- Imports de Módulos do Projeto ---
from configuracoes.carregar_config import CONFIANCA_PADRAO_IMAGEM

# --- Constantes de Caminho ---
CAMINHO_PROJETO = Path(__file__).resolve().parent.parent
CAMINHO_JSON = CAMINHO_PROJETO / "assets" / "parametros.json"


def localizar_elemento(
    nome_chave: str,
    confianca_override: float = None
) -> Tuple[pyautogui.Point, Dict[str, Any]]:
    """Localiza um elemento e retorna sua posição e dados do JSON.

    Esta é a função de base para todas as interações. Ela encontra a âncora
    na tela e retorna tanto sua posição quanto os metadados associados
    (como ajustes padrão) do arquivo JSON.

    Args:
        nome_chave (str): A chave do elemento a ser procurado no JSON.
        confianca_override (float, optional): Um valor de confiança específico
                                             para esta busca, que sobrescreve
                                             o padrão global.

    Returns:
        Tuple[pyautogui.Point, Dict[str, Any]]: Uma tupla contendo:
            - A posição (x, y) do centro da âncora encontrada.
            - O dicionário de dados do JSON para aquela chave.

    Raises:
        FileNotFoundError: Se o arquivo JSON ou a imagem não forem encontrados.
        KeyError: Se a chave do elemento não for encontrada no JSON.
        pyautogui.ImageNotFoundException: Se a imagem não for encontrada na tela.
    """
    try:
        with open(CAMINHO_JSON, 'r', encoding='utf-8') as f:
            dados_json_completo = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo de elementos não encontrado: {CAMINHO_JSON}")

    dados_elemento = dados_json_completo.get(nome_chave)
    if not dados_elemento:
        raise KeyError(f"Chave '{nome_chave}' não encontrada no parametros.json.")

    caminho_imagem_relativo = dados_elemento.get("path")
    if not caminho_imagem_relativo:
        raise KeyError(f"Propriedade 'path' não encontrada para a chave '{nome_chave}'.")

    caminho_imagem_absoluto = CAMINHO_PROJETO / caminho_imagem_relativo
    if not caminho_imagem_absoluto.exists():
        raise FileNotFoundError(f"Arquivo de imagem não encontrado: {caminho_imagem_absoluto}")

    # Define a confiança a ser usada: o override, se existir, ou o padrão global.
    confianca_a_usar = confianca_override if confianca_override is not None else CONFIANCA_PADRAO_IMAGEM

    posicao = pyautogui.locateCenterOnScreen(str(caminho_imagem_absoluto), confidence=confianca_a_usar)

    if posicao is None:
        raise pyautogui.ImageNotFoundException(f"Elemento '{nome_chave}' não foi encontrado na tela.")

    return posicao, dados_elemento