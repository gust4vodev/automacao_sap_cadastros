# uteis/logica_vendedores.py

"""
Módulo para centralizar a lógica de negócio, como a lista de vendedores.
"""

import json
from pathlib import Path

# --- Constantes de Caminho ---
CAMINHO_PROJETO = Path(__file__).resolve().parent.parent
CAMINHO_JSON_VENDEDORES = CAMINHO_PROJETO / "vendedores_pet7.json"

# --- Cache da Lista ---
# Para evitar ler o arquivo do disco toda hora, carregamos a lista uma vez
# e a armazenamos em um 'set' (conjunto) para buscas rápidas.
VENDEDORES_PET7_SET = set()

def _carregar_lista_vendedores() -> set:
    """
    Função interna para carregar o JSON e convertê-lo em um 'set' (conjunto)
    de nomes em maiúsculas para performance e robustez na comparação.
    """
    global VENDEDORES_PET7_SET
    if VENDEDORES_PET7_SET:
        # Se a lista já foi carregada, não faz nada.
        return VENDEDORES_PET7_SET

    try:
        with open(CAMINHO_JSON_VENDEDORES, 'r', encoding='utf-8') as f:
            lista_json = json.load(f)

        # Converte a lista em um 'set' com todos os nomes em maiúsculo.
        VENDEDORES_PET7_SET = {str(nome).strip().upper() for nome in lista_json}
        return VENDEDORES_PET7_SET

    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo de vendedores não encontrado: {CAMINHO_JSON_VENDEDORES}")
    except Exception as e:
        raise RuntimeError(f"Falha ao carregar ou processar o JSON de vendedores: {e}")


def obter_codigo_divisao_por_usuario(codigo_usuario: str) -> int:
    """
    Verifica se um usuário pertence à lista de Vendedores PET7 carregada do JSON.

    Args:
        codigo_usuario (str): O código do usuário (ex: 'JONATHAN.FREITAS').

    Returns:
        int: Retorna 4 se o usuário ESTIVER na lista, 2 se NÃO ESTIVER.
    """
    # Garante que a lista esteja carregada em memória.
    lista_vendedores = _carregar_lista_vendedores()

    if not codigo_usuario:
        return 2 # Usuário nulo ou vazio

    # Compara em maiúsculas com a lista (que já está em maiúsculas).
    if codigo_usuario.strip().upper() in lista_vendedores:
        return 4  # Usuário é da PET7
    else:
        return 2  # Usuário não é da PET7


# --- Camada de Teste Direto ---
if __name__ == '__main__':
    """
    Bloco para testar a lógica de vendedores.
    Execute-o a partir da raiz do projeto com: python -m uteis.logica_vendedores
    """
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).resolve().parent.parent))

    print(">>> Iniciando teste da função 'obter_codigo_divisao_por_usuario'...")

    # Teste 1: Usuário que ESTÁ na lista
    usuario_teste_pet = "JONATHAN.FREITAS"
    resultado_pet = obter_codigo_divisao_por_usuario(usuario_teste_pet)
    print(f"--- Testando usuário: '{usuario_teste_pet}' -> Resultado: {resultado_pet} (Esperado: 4)")
    assert resultado_pet == 4, "Teste 1 Falhou"

    # Teste 2: Usuário que NÃO ESTÁ na lista
    usuario_teste_outro = "USUARIO.COMUM"
    resultado_outro = obter_codigo_divisao_por_usuario(usuario_teste_outro)
    print(f"--- Testando usuário: '{usuario_teste_outro}' -> Resultado: {resultado_outro} (Esperado: 2)")
    assert resultado_outro == 2, "Teste 2 Falhou"

    print("\n--- Teste concluído com SUCESSO! ---")