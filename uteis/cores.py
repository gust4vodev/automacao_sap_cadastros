# uteis/cores.py

"""
Módulo central para armazenar constantes de cores e estilos ANSI para o terminal.

Isso permite a padronização da saída em toda a aplicação.
Uso: print(f"{VERDE}{NEGRITO}Texto em negrito e verde{RESET}")
"""

# --- Estilos de Texto ---
RESET = "\033[0m"       # Reseta todas as formatações
NEGRITO = "\033[1m"      # Texto em negrito
SUBLINHADO = "\033[4m"   # Texto sublinhado

# --- Cores de Texto (Cores Vivas/Brilhantes) ---
PRETO = "\033[90m"
VERMELHO = "\033[91m"
VERDE = "\033[92m"
AMARELO = "\033[93m"
AZUL = "\033[94m"
MAGENTA = "\033[95m"
CIANO = "\033[96m"
BRANCO = "\033[97m"

# --- Camada de Teste Direto / Demonstração ---
if __name__ == '__main__':
    """
    Bloco para demonstrar visualmente as cores e estilos definidos neste módulo.
    
    Execute-o a partir da raiz do projeto (ex: pasta 'automacao_sap_b1') com:
    python -m uteis.cores
    """
    
    print(">>> Iniciando demonstração de Cores e Estilos ANSI <<<")
    
    # --- 1. Demonstração de Estilos ---
    print(f"\n{NEGRITO}--- Demonstração de Estilos ---{RESET}")
    print(f"Texto Normal (padrão)")
    print(f"{NEGRITO}Texto em Negrito{RESET}")
    print(f"{SUBLINHADO}Texto Sublinhado{RESET}")
    print(f"{NEGRITO}{SUBLINHADO}Negrito e Sublinhado{RESET}")

    # --- 2. Demonstração de Cores Vivas ---
    print(f"\n{NEGRITO}--- Demonstração de Cores ---{RESET}")
    print(f"{PRETO}Texto em Preto{RESET}")
    print(f"{VERMELHO}Texto em Vermelho{RESET}")
    print(f"{VERDE}Texto em Verde{RESET}")
    print(f"{AMARELO}Texto em Amarelo{RESET}")
    print(f"{AZUL}Texto em Azul{RESET}")
    print(f"{MAGENTA}Texto em Magenta{RESET}")
    print(f"{CIANO}Texto em Ciano{RESET}")
    print(f"{BRANCO}Texto em Branco{RESET}")

    # --- 3. Demonstração de Combinações ---
    print(f"\n{NEGRITO}--- Demonstração de Combinações ---{RESET}")
    print(f"{VERDE}{NEGRITO}Sucesso: Ação concluída! (Verde, Negrito){RESET}")
    print(f"{AMARELO}{NEGRITO}Aviso: Atenção necessária! (Amarelo, Negrito){RESET}")
    print(f"{VERMELHO}{NEGRITO}{SUBLINHADO}Erro: Falha crítica! (Vermelho, Negrito, Sublinhado){RESET}")
    
    print("\n>>> Demonstração concluída! <<<")