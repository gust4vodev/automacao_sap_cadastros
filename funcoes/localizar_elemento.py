# funcoes/localizar_elemento.py

"""
Módulo para a função de mais baixo nível: localizar um elemento na tela.
"""

import json
import pyautogui
from pathlib import Path
from typing import Tuple, Dict, Any

from configuracoes.carregar_config import CONFIANCA_PADRAO_IMAGEM

# --- Constantes de Caminho ---
CAMINHO_PROJETO = Path(__file__).resolve().parent.parent
CAMINHO_JSON = CAMINHO_PROJETO / "parametros.json"


def localizar_elemento(
    nome_chave: str,
    confianca_override: float = None
) -> Tuple[pyautogui.Point, Dict[str, Any]]:
    """Localiza um elemento e retorna sua posição e dados do JSON."""

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

    confianca_a_usar = confianca_override if confianca_override is not None else CONFIANCA_PADRAO_IMAGEM

    # --- AQUI ESTÁ A CORREÇÃO ---
    try:
        # Tenta localizar a imagem na tela.
        posicao = pyautogui.locateCenterOnScreen(str(caminho_imagem_absoluto), confidence=confianca_a_usar)

        if posicao is None:
            # Se o PyAutoGUI retornar None (em vez de um erro), forçamos um erro.
            raise pyautogui.ImageNotFoundException

    except pyautogui.ImageNotFoundException:
        # Captura a exceção (seja a nossa ou a do PyAutoGUI) e a
        # re-levanta com uma mensagem de erro clara e descritiva.
        raise pyautogui.ImageNotFoundException(
            f"Elemento '{nome_chave}' (imagem: {caminho_imagem_relativo}) não foi encontrado na tela."
        )
    # -------------------------------

    return posicao, dados_elemento