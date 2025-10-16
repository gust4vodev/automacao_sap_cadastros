# uteis/sincronizador_assets.py

"""
Módulo responsável por sincronizar o arquivo parametros.json com as imagens
reais presentes na pasta de imagens, garantindo consistência.
"""

import json
from pathlib import Path

# --- Constantes de Caminho (VERSÃO ATUALIZADA) ---
CAMINHO_PROJETO = Path(__file__).resolve().parent.parent

# Assumindo que o JSON também ficará na raiz para consistência.
CAMINHO_JSON = CAMINHO_PROJETO / "parametros.json" 

# AQUI ESTÁ A CORREÇÃO: O caminho agora aponta diretamente para a pasta 'imagens' na raiz.
PASTA_IMAGENS = CAMINHO_PROJETO / "imagens"
# --- Fim das Constantes ---


def sincronizar_json_com_pasta_assets():
    """
    Verifica a pasta de imagens e atualiza o JSON para refletir seu conteúdo.
    - Remove chaves do JSON se a imagem correspondente foi deletada.
    - Adiciona novas chaves ao JSON se novas imagens foram encontradas.
    - Preserva os dados existentes de chaves que não foram alteradas.
    """
    #print("🔄 Iniciando sincronização de assets...")
    alteracoes_feitas = False

    try:
        with open(CAMINHO_JSON, 'r', encoding='utf-8') as f:
            dados_json = json.load(f)
    except FileNotFoundError:
        dados_json = {}

    caminhos_na_pasta = {
        str(p.relative_to(CAMINHO_PROJETO)).replace('\\', '/')
        for p in PASTA_IMAGENS.rglob('*.png')
    }

    chaves_para_remover = []
    for chave, dados in dados_json.items():
        if dados.get("path") not in caminhos_na_pasta:
            chaves_para_remover.append(chave)

    if chaves_para_remover:
        for chave in chaves_para_remover:
            del dados_json[chave]
        print(f"   - {len(chaves_para_remover)} elemento(s) removido(s) do JSON.")
        alteracoes_feitas = True

    caminhos_no_json = {v.get("path") for v in dados_json.values()}
    novos_caminhos = caminhos_na_pasta - caminhos_no_json

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

    if alteracoes_feitas:
        with open(CAMINHO_JSON, 'w', encoding='utf-8') as f:
            json.dump(dados_json, f, indent=2, ensure_ascii=False)
        print("✅ Sincronização concluída. O arquivo parametros.json foi atualizado.")
    else:
        pass
        #print("✅ Sincronização concluída. Nenhum ajuste foi necessário.")


# --- Camada de Teste Direto ---
if __name__ == '__main__':
    print(">>> Executando o sincronizador de assets em modo de teste...")
    # O 'parents=True' ainda é útil caso a pasta 'imagens' não exista.
    PASTA_IMAGENS.mkdir(parents=True, exist_ok=True) 
    sincronizar_json_com_pasta_assets()
    print(">>> Teste finalizado.")