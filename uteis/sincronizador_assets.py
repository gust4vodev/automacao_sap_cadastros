# uteis/sincronizador_assets.py

"""
Módulo responsável por sincronizar o arquivo parametros.json com as imagens
reais presentes na pasta de imagens, garantindo consistência.
"""

import json
from pathlib import Path

# 1. Define caminhos absolutos: projeto raiz, `parametros.json` e pasta `imagens`. 
CAMINHO_PROJETO = Path(__file__).resolve().parent.parent
CAMINHO_JSON = CAMINHO_PROJETO / "parametros.json" 
PASTA_IMAGENS = CAMINHO_PROJETO / "imagens"

def sincronizar_json_com_pasta_assets():
    """
    Verifica a pasta de imagens e atualiza o JSON para refletir seu conteúdo.
    - Remove chaves do JSON se a imagem correspondente foi deletada.
    - Adiciona novas chaves ao JSON se novas imagens foram encontradas.
    - Preserva os dados existentes de chaves que não foram alteradas.
    """
    #print("🔄 Iniciando sincronização de assets...")
    alteracoes_feitas = False

# 2. Carrega `parametros.json` ou inicia dicionário vazio se não existir.
    try:
        with open(CAMINHO_JSON, 'r', encoding='utf-8') as f:
            dados_json = json.load(f)
    except FileNotFoundError:
        dados_json = {}

# 3. Coleta todos os caminhos relativos de arquivos `.png` na pasta `imagens` (recursivo).
    caminhos_na_pasta = {
        str(p.relative_to(CAMINHO_PROJETO)).replace('\\', '/')
        for p in PASTA_IMAGENS.rglob('*.png')
    }

# 4. Identifica chaves no JSON cujos caminhos de imagem não existem mais na pasta.  
    chaves_para_remover = []
    for chave, dados in dados_json.items():
        if dados.get("path") not in caminhos_na_pasta:
            chaves_para_remover.append(chave)

# 5. Remove chaves obsoletas do JSON e marca alteração.  
    if chaves_para_remover:
        for chave in chaves_para_remover:
            del dados_json[chave]
        print(f"   - {len(chaves_para_remover)} elemento(s) removido(s) do JSON.")
        alteracoes_feitas = True

# 6. Detecta imagens novas na pasta que não estão no JSON.  
    caminhos_no_json = {v.get("path") for v in dados_json.values()}
    novos_caminhos = caminhos_na_pasta - caminhos_no_json

# 7. Adiciona novas chaves com `path`, `ajuste_x` e `ajuste_y` vazios.  
    if novos_caminhos:
        for caminho in novos_caminhos:
            chave_nova = Path(caminho).stem
            dados_json[chave_nova] = {
                "path": caminho,
                "ajuste_x": "",
                "ajuste_y": ""
            }
        print(f"   - {len(novos_caminhos)} novo(s) elemento(s) adicionado(s) ao JSON.")
        alteracoes_feitas = True

# 8. Salva JSON atualizado com indentação se houve alterações.
    if alteracoes_feitas:
        with open(CAMINHO_JSON, 'w', encoding='utf-8') as f:
            json.dump(dados_json, f, indent=2, ensure_ascii=False)
        print("✅ Sincronização concluída. O arquivo parametros.json foi atualizado.")

# --- Camada de Teste Direto ---
if __name__ == '__main__':
    print(">>> Executando o sincronizador de assets em modo de teste...")
    # O 'parents=True' ainda é útil caso a pasta 'imagens' não exista.
    PASTA_IMAGENS.mkdir(parents=True, exist_ok=True) 
    sincronizar_json_com_pasta_assets()
    print(">>> Teste finalizado.")