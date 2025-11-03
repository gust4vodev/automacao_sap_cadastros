# uteis/gestor_sessao.py

"""
Módulo Gestor de Sessão (JSON).

Responsável por criar, ler, atualizar e limpar o ficheiro de estado
(dados_sessao.json) que persiste os dados durante uma única
execução do robô.

Isto permite que as (ações) sejam "desacopladas" e
consumam dados (como dados da API CNPJ) sem dependerem
do main.py para passar parâmetros.
"""

import json
from pathlib import Path
from typing import Dict, Any, List

# 1. Define o caminho do projeto (a pasta raiz 'automacao_sap_b1')
CAMINHO_PROJETO = Path(__file__).resolve().parent.parent

# 2. Define onde o ficheiro de sessão será guardado
CAMINHO_SESSAO_JSON = CAMINHO_PROJETO / "temp" / "dados_sessao.json"

# 3. Define o "Template" inicial (com chaves vazias que posteriormente é atualizada com os dados de retorno da API)
TEMPLATE_SESSAO_VAZIA = {
    "tipo_pessoa": 0, # 0=Desconhecido, 1=CPF, 2=CNPJ
    "status_cnpj": "",
    "razao_social": "",
    "data_abertura": "",
    "inscricao_estadual": "Isento",
    "simples_nacional": None,
    "socios": [],
    "endereco": {
        "tipo_logradouro": "", "logradouro": "", "numero": "",
        "complemento": "", "bairro": "", "cep": "",
        "cidade": "", "estado": ""
    }
}

# --- Funções Públicas de Gestão ---

def iniciar_sessao():
    """
    (Passo 1) Cria/Limpa o ficheiro dados_sessao.json.
    Garante que o robô comece com um estado limpo.
    """
    try:
        # Garante que a pasta 'temp' exista
        CAMINHO_SESSAO_JSON.parent.mkdir(parents=True, exist_ok=True)
        
        # Escreve o template vazio no ficheiro
        with open(CAMINHO_SESSAO_JSON, 'w', encoding='utf-8') as f:
            json.dump(TEMPLATE_SESSAO_VAZIA, f, indent=4, ensure_ascii=False)
        print("   - (Gestor de Sessão: 'dados_sessao.json' iniciado/limpo.)")
        
    except Exception as e:
        print(f"❌ Erro crítico ao iniciar a sessão JSON: {e}")
        raise IOError(f"Falha ao criar/limpar o dados_sessao.json: {e}")

def escrever_dados_sessao(novos_dados: Dict[str, Any]):
    """
    (Passo 2) Atualiza o JSON de sessão com novos dados.
    Lê o ficheiro atual, junta os novos dados e reescreve.
    
    Args:
        novos_dados (Dict[str, Any]): Um dicionário com os dados a serem adicionados ou sobrescritos.
    """
    try:
        # 1. Lê os dados que já existem no JSON
        dados_atuais = ler_dados_sessao()
        
        # 2. Atualiza (mescla) os dados atuais com os novos dados
        dados_atuais.update(novos_dados)
        
        # 3. Reescreve o ficheiro completo
        with open(CAMINHO_SESSAO_JSON, 'w', encoding='utf-8') as f:
            json.dump(dados_atuais, f, indent=4, ensure_ascii=False)
            
    except Exception as e:
        print(f"❌ Erro crítico ao escrever no dados_sessao.json: {e}")
        # (Não levanta erro para não parar o robô, mas avisa)


def ler_dados_sessao() -> Dict[str, Any]:
    """
    Lê o conteúdo completo do JSON de sessão.
    
    Returns:
        Dict[str, Any]: O dicionário com o estado atual da sessão.
    """
    try:
        if not CAMINHO_SESSAO_JSON.exists():
            # Segurança: se o JSON não existir, inicia um novo
            print("⚠️ Aviso: dados_sessao.json não encontrado. Iniciando um novo.")
            iniciar_sessao()
        
        with open(CAMINHO_SESSAO_JSON, 'r', encoding='utf-8') as f:
            return json.load(f)
            
    except Exception as e:
        print(f"❌ Erro crítico ao ler o dados_sessao.json: {e}")
        # Retorna o template vazio em caso de falha de leitura
        return TEMPLATE_SESSAO_VAZIA.copy()

def encerrar_sessao():
    """
    Limpa o ficheiro de sessão (reescreve o template vazio).
    """
    try:
        # Por segurança, em vez de apagar, reescrevemos o template vazio
        iniciar_sessao()
        print("   - (Gestor de Sessão: 'dados_sessao.json' limpo.)")
    except Exception as e:
        print(f"⚠️ Aviso: Falha ao limpar o dados_sessao.json: {e}")