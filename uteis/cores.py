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