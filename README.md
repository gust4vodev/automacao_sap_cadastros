# Assistente de Automação SAP


Este repositório contém o código-fonte de um assistente de automação (robô) focado no processo de **Cadastro de Parceiros de Negócios (PN)** no SAP B1.

O objetivo deste projeto é eliminar a entrada manual de dados, garantir a consistência da informação através de consultas a APIs externas e lidar de forma inteligente com falhas de execução.

## 1. Tecnologias Utilizadas

Para construir este robô, utilizámos as seguintes tecnologias principais:

* **Python 3:** A linguagem de programação central.
* **PyAutoGUI (Automação de UI):** Usado para a "visão computacional" — encontrar imagens na tela (âncoras), clicar e digitar.
* **Requests:** A biblioteca usada para comunicar com APIs externas (consultar CNPJs).
* **Pandas:** Usado para tarefas de manipulação de dados, especificamente para ler e escrever dados de/para a área de transferência do SAP.

## 2. Atenção: Um Projeto "Sob Medida"

Antes de executar este robô, é fundamental entender que ele **não** é uma solução genérica "plug-and-play".

Este projeto foi desenvolvido e afinado para funcionar num ambiente de SAP B1 **altamente específico e personalizado**.

A estratégia central do robô é a **Visão Computacional**: ele "enxerga" a tela e procura por imagens exatas (âncoras) para saber onde clicar e digitar. Estas imagens de referência (guardadas na pasta `imagens/` e mapeadas no `parametros.json`) foram capturadas usando as preferências visuais exatas do ambiente de desenvolvimento original, tais como:

* **Tema de Cores** (ex: Dark/Light Mode, cores personalizadas do SAP)
* **Tamanho da Fonte**
* **Resolução do Monitor**
* **Versão Específica** do SAP

### Aviso Crítico de Implantação

Qualquer tentativa de executar este robô num ambiente (computador ou servidor) que tenha uma **configuração visual diferente** (outro tema, fonte, ou resolução de ecrã) irá **causar falhas críticas**.

O robô não conseguirá "enxergar" os botões e abas, resultando em erros (`ImageNotFoundException`) que irão parar a automação.

**Para reproduzir este projeto, será necessário:**
1.  **Recapturar todas** as imagens de âncora (`.png`) no ambiente de destino.
2.  **Atualizar** o ficheiro `parametros.json` para que ele aponte para as novas imagens.

### Estratégia 1: Visão Computacional (Âncoras)

O robô não clica em coordenadas fixas (ex: X:100, Y:250). Em vez disso, ele "enxerga" a tela.

* **Como:** Usamos um ficheiro central, o `parametros.json`, que funciona como os "olhos" do robô.
* **Exemplo:** Para clicar na aba "Endereços", o robô procura a imagem `aba_enderecos.png` (definida no JSON) e clica no centro dela, não importa onde a janela do SAP esteja na tela.
* **Vantagem:** O robô não "quebra" se a resolução do monitor mudar ou se a janela for movida.

### Estratégia 2: O "Cérebro de Sessão" (Ficheiro JSON)

Para que as diferentes etapas da automação comuniquem entre si, utilizámos um "cérebro" central.

* **Como:** Em vez de passar variáveis complexas (como a lista de sócios) do `main.py` para as funções, o robô usa um ficheiro de "estado" temporário: `temp/dados_sessao.json`.
* **Fluxo de Dados:**
    1.  **Início:** O robô cria o `dados_sessao.json` com chaves vazias.
    2.  **"Gatilho" (`idfiscais.py`):** Esta etapa captura o CPF/CNPJ da tela. Se for um CNPJ, ela chama a API.
    3.  **"Produtor" (`consulta_cnpj.py`):** Esta etapa (o "Gerente da API") **escreve** os dados (Sócios, IE, Endereço, etc.) no `dados_sessao.json`.
    4.  **"Consumidores" (`preencher_socios.py`):** As etapas seguintes (como "Preencher Sócios" ou "Preencher Geral 2") **leem** os dados de que precisam diretamente deste JSON.
* **Vantagem:** O `main.py` (orquestrador) fica limpo. As "paredes" (ações) tornam-se independentes e auto-suficientes. Se o robô falhar, o ficheiro JSON fica guardado, permitindo uma depuração (debug) muito fácil.

### Estratégia 3: O "Motor" de Automação Assistida (Resiliência)

Esta é a estratégia mais importante para a robustez. O robô nunca executa uma ação "sensível" (como um clique ou uma chamada de API) diretamente.

* **Como:** Todas as ações são "embrulhadas" pelo `assistente/executor.py` (o nosso "Motor").
* **Lógica 1 (Retentativas):** O Motor tenta executar cada ação (ex: `clicar_elemento`) 3 vezes (com pausas) antes de desistir. Isto resolve 90% das falhas comuns de *timing* (ex: o SAP demorou a responder).
* **Lógica 2 (Assistência):** Se as 3 tentativas falharem, o Motor **não pára o robô**. Em vez disso, ele abre um menu de interface para o utilizador, perguntando o que fazer ("Tentar Novamente", "Ignorar Etapa" ou "Abortar"). Isto é "Automação Assistida".

### Estratégia 4: Regras de Negócio Embutidas

O robô não apenas move dados; ele toma decisões de negócio que implementámos:

1.  **Validação de Status (em `idfiscais.py`):** O robô verifica se o `status_cnpj` retornado pela API é "Ativa". Se o CNPJ estiver "Baixada" ou "Inapta", o robô é programado para **abortar a execução** (usando a exceção `AutomacaoAbortadaPeloUsuario`), impedindo o cadastro de um PN irregular.
2.  **Pausa para SUFRAMA (em `consulta_cnpj.py`):** O robô analisa o Estado (UF), Município e CNAE. Se detetar um candidato a SUFRAMA, ele **pausa** a automação (`input()`) e pede ao utilizador para fazer a verificação manual, antes de continuar.
3.  **Regra CC (em `preencher_aba_geral2.py`):** O robô lê o status da IE (`Isento` ou um número) do JSON e aplica a sua regra de negócio para preencher os campos "Ind. IE" (1 ou 9) e "Op. Consumidor" (0 ou 1).

## 3. Estrutura das Pastas

Este é um mapa simples do projeto, focado nos "porquês" de cada pasta.

automacao_sap_b1

-- acoes/             (As "Paredes": O que fazer? Etapas de negócio)

-- assistente/        (O "Motor": A lógica de Retentativas e Menu de Falha)

-- configuracoes/     (Carrega as chaves do ficheiro .env)

-- funcoes/           (As "Ferramentas": Como fazer? (ex: clicar, digitar))

-- servicos/          (As "Fontes de Dados": Onde buscar informação? (APIs))

-- uteis/             (Lógica Pura: Funções que não tocam na tela (ex: formatar, gerir o JSON))

-- validacoes/        (O "Check-in": O que verificar antes de começar?)

-- temp/              (Pasta temporária onde o "Cérebro" (JSON) é guardado)

-- parametros.json    (Os "Olhos": Onde estão as imagens (âncoras)?)

-- main.py            (O "Maestro": O orquestrador que chama as "paredes" na ordem correta)
