## APIs Externas e Estratégia de Consulta

Para garantir a validade dos dados de cadastro, o robô consome APIs externas. A forma como o robô consome estas APIs foi desenhada especificamente para **maximizar a performance e economizar custos/créditos**.

### 1. APIs Utilizadas

O robô utiliza **duas** fontes de dados externas principais:

1.  **API Comercial CNPJá (Unificada)**
    * **Endpoint:** `https://api.cnpja.com/office/[CNPJ]`
    * **Ficheiro:** `servicos/api_cnpja_comercial_ie_simples.py`
    * **Autenticação:** Chave (`Authorization`) lida do ficheiro `.env`.
    * **Propósito:** Esta é a nossa API principal. Numa única chamada, ela fornece todos os dados necessários para o cadastro:
        * Dados Cadastrais (Razão Social, Data de Abertura, Status)
        * Endereço Completo
        * QSA (Lista de Sócios)
        * Status do Simples Nacional
        * Inscrições Estaduais (IEs)

2.  **API Google Maps Geocoding**
    * **Endpoint:** `https://maps.googleapis.com/maps/api/geocode/json`
    * **Ficheiro "Trabalhador":** `servicos/api_google.py`
    * **Propósito:** Utilizada pela "ação" `processar_endereco_faturamento` para obter as coordenadas (Latitude e Longitude) do endereço lido do SAP.

### A Lógica para Economia de Créditos (em Camadas)

Como a API Comercial (`/office/`) é paga (cobra por consulta "online"), implementámos **duas camadas** de cache para garantir que o robô só gasta créditos quando é absolutamente necessário.

#### Cache Escalonado (A Estratégia da API)

O robô chama a API, de forma "inteligente", usando a estratégia de 3 passos `api_cnpja_comercial_ie_simples.py`:

1.  **Tentativa 1 (Cache Rápido - 90 dias):**
    O robô pede à API os dados, mas *apenas* se eles estiverem no cache do servidor e tiverem sido atualizados nos últimos 90 dias (`strategy: CACHE, maxAge: 90`). Se o servidor não os tiver (erro 404), o robô avança.

2.  **Tentativa 2 (Cache Antigo - 150 dias):**
    O robô tenta de novo, agora aceitando um cache "mais velho", de até 150 dias (`strategy: CACHE, maxAge: 150`).

3.  **Tentativa 3 (Consulta Online - Paga):**
    Apenas se as duas tentativas de cache falharem, o robô faz a consulta "Online" (`strategy: CACHE_IF_FRESH`), que gasta um crédito e obtém os dados mais recentes do governo.

* **Vantagem:** Esta estratégia garante que 90% das consultas (para empresas que não mudam de dados frequentemente) sejam resolvidas usando o cache gratuito da API, **economizando drasticamente os créditos pagos** e encontrando resultados **que não é possivel obter com a versão gratuita**