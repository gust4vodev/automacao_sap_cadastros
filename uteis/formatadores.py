# uteis/formatadores.py

"""
Módulo com funções auxiliares para formatação e limpeza de dados.
"""

import re

def limpar_documento(doc: str) -> str:
    """Remove pontuação e caracteres não numéricos de CPF/CNPJ."""
    # Retorna uma string vazia se a entrada for None ou vazia
    if not doc:
        return ""
    # Usa expressão regular para encontrar e remover tudo que NÃO for dígito (\d)
    return re.sub(r'[^\d]', '', str(doc))

# --- Camada de Teste Direto ---
if __name__ == '__main__':
    """
    Bloco para testar a função 'limpar_documento'.
    Execute a partir da raiz: python -m uteis.formatadores
    """
    print(">>> Iniciando teste da função 'limpar_documento'...")

    testes = [
        ("123.456.789-00", "12345678900"),
        ("12.345.678/0001-99", "12345678000199"),
        ("Texto 123 com 456 numeros", "123456"),
        ("", ""),
        (None, "")
    ]

    sucesso = True
    for entrada, esperado in testes:
        resultado = limpar_documento(entrada)
        print(f"--- Testando '{entrada}': Resultado='{resultado}', Esperado='{esperado}'")
        if resultado != esperado:
            print(f"    *** FALHOU! ***")
            sucesso = False

    if sucesso:
        print("\n--- Teste concluído com SUCESSO! ---")
    else:
        print("\n--- Teste FALHOU! ---")