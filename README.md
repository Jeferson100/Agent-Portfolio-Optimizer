## Agent Portfolio Optimizer



### Visão geral



**Agent Portfolio Optimizer** é um projeto em Python para apoio à tomada de decisão em investimentos, focado em ações brasileiras (B3). Ele combina um **roteador de modelos de linguagem (LLM)** com um fluxo de análise fundamentalista automatizado para avaliar empresas, classificar a qualidade dos ativos e gerar insumos para otimização de carteiras.



O projeto integra múltiplos provedores de LLM (NVIDIA, Groq, HuggingFace, Cerebras) com fallback automático, utilizando dados fundamentalistas históricos para construir uma análise estruturada e revisada por um "analista sênior" virtual.



### Principais funcionalidades



- **Roteador de LLMs com fallback (`LlmRouter`)**:

  - Tenta sequencialmente diferentes provedores/modelos (NVIDIA, Cerebras, Groq, HuggingFace).

  - Suporta **saída estruturada com Pydantic** (classificações, textos de análise, flags de validação etc.).

  - Trata respostas em múltiplos formatos (string, dict, objetos) e normaliza para dicionário.



- **Análise fundamentalista automatizada**:

  - Coleta dados fundamentalistas de ações brasileiras (por ticker, intervalo de datas) via módulos em `src/portfolio_optimizer`.

  - Constrói tabelas em formato markdown com indicadores como **receita líquida, EBITDA, lucro por ação, alavancagem financeira, margem líquida, P/L, P/VP**, entre outros.

  - Usa um LLM para gerar, para cada ticker, uma **classificação** (`Excellent`, `Good`, `Fair`, `Poor`, `Very Poor`) e uma **análise textual curta**.



- **Validação por analista sênior virtual**:

  - Um segundo agente LLM revisa a classificação e a análise do primeiro analista.

  - Retorna um campo booleano de validação e um texto explicando se a análise é consistente e o que pode ser melhorado.

  - Possibilidade de iterações sucessivas até que a análise seja considerada adequada ou até um número máximo de interações.



- **Orquestração com LangGraph**:

  - Usa `StateGraph` para compor o fluxo:

    - coleta de dados fundamentalistas,

    - análise fundamentalista,

    - avaliação do analista,

    - decisão condicional de encerrar ou refazer a análise.

  - Permite executar o grafo para **um ticker** ou **listas de tickers** em paralelo (por exemplo, VALE3, PETR4, ITUB4, etc.).



- **Segundo fluxo: construção de carteira de ações brasileiras**:

  - A partir das classificações e análises fundamentalistas, o projeto executa um segundo fluxo que **seleciona e monta uma carteira de ações da B3**.

  - Esse fluxo considera um conjunto de tickers elegíveis, aplica filtros de qualidade (classificação mínima, consistência de análise, período de dados) e pode integrar métricas de risco/retorno.

  - O resultado é uma **carteira sugerida**, com lista de ativos e pesos/participações, que pode ser ajustada conforme o perfil do investidor e restrições adicionais (número máximo de ativos, limites por setor, etc.).



### Detalhes dos agentes



- **Agente de coleta de dados**:

  - Recebe como estado os campos `tic`, `data_inicio` e `data_fim`.

  - Usa classes de tratamento de dados (por exemplo, `TratatandoDadosFundamentalistasComparacao`) para buscar e consolidar a série histórica do ticker.

  - Retorna o estado enriquecido com `dados_fundamentalistas` em formato markdown (tabela de indicadores).



- **Agente analista fundamentalista**:

  - Lê `dados_fundamentalistas` e, opcionalmente, um feedback anterior (`description_avaliacao_analise`).

  - Monta um prompt rico com a tabela de fundamentos e instruções de classificação.

  - Chama o `LlmRouter` com um modelo de saída estruturada `TickerLevel` (campos `classification` e `analysis`).

  - Normaliza a resposta (independente do provedor) via função de tratamento para garantir um dicionário padrão.



- **Agente avaliador sênior**:

  - Recebe o mesmo `dados_fundamentalistas`, mais `classification` e `analysis` vindos do agente anterior.

  - Usa o `LlmRouter` com o modelo `SeniorAvaliador`, que retorna:

    - `avaliacao_analise` (True/False),

    - `description_avaliacao_analise` (feedback curto, em inglês),

    - além de atualizar o contador de interações (`interacao`).

  - Esse feedback alimenta a próxima rodada de análise, caso o grafo decida continuar.



- **Função de decisão (`should_continue`)** (análise fundamentalista):

  - Lê `avaliacao_analise` e `interacao` do estado global.

  - Se a análise foi aprovada ou o número máximo de interações foi atingido, retorna `END`.

  - Caso contrário, direciona o fluxo de volta para o agente analista, permitindo refinamento iterativo.



- **Agente de construção de carteira (segundo fluxo)**:

  - Consome o conjunto de estados finais por ticker (classificação, análise, validação, indicadores).

  - Aplica regras como:

    - filtrar apenas tickers com classificação mínima (por exemplo, `Good` ou `Excellent`),

    - excluir ativos reprovados pelo avaliador sênior,

    - limitar concentração por ativo/setor.

  - Produz uma sugestão de **lista de ativos e pesos** que pode ser usada como ponto de partida para otimização quantitativa adicional.



- **Agentes de criação e validação de pesos da carteira** (fluxo `graph_weights`):

  - O estado desse fluxo é descrito por `StateCarteira`, contendo pesos por ticker, justificativa, correlações, erros de soma/tickers e contador de iterações.

  - O grafo é construído com `StateGraph(StateCarteira)` e os seguintes nós:

    - `analista_criador_carteira`: usa o LLM com o prompt de otimização para propor uma nova alocação (`tickers_weights` + `justification`), a partir das classificações fundamentalistas, correlações e feedback anterior.

    - `verify_weight_sum`: verifica e normaliza a soma dos pesos para 100%, ajustando proporcionalmente e registrando mensagens de erro em `soma_weights_error`, se necessário.

    - `verifica_tics_selecionados`: garante que todos os tickers alocados pertencem à lista de tickers válidos (`tics`), registrando eventuais erros em `tics_error`.

    - `analista_avaliador_peso_carteira`: agente avaliador de carteira que analisa a alocação proposta, gera um relatório detalhado de riscos/violação de restrições e atualiza `analise_avaliador_weights` e `interacao`.

  - O fluxo é definido da seguinte forma:

    - ponto de entrada em `analista_criador_carteira`;

    - `analista_criador_carteira` → `verify_weight_sum` → `verifica_tics_selecionados`;

    - uma função de decisão (`should_continue`, específica desse fluxo) avalia `tics_error` e `interacao` para decidir entre encerrar (`END`) ou enviar o estado para `analista_avaliador_peso_carteira`;

    - se houver nova iteração, `analista_avaliador_peso_carteira` → `analista_criador_carteira`, criando um ciclo de refinamento até que os pesos estejam corretos e os tickers sejam válidos ou o limite de interações seja atingido.



### Tecnologias e bibliotecas



- **Python 3.11+** (ver `pyproject.toml`).

- **Pydantic / Pydantic AI** para modelos de saída estruturada.

- **LangGraph** para orquestração do fluxo de agentes/tools.

- **Clientes de LLM**:

  - `langchain-nvidia-ai-endpoints` (NVIDIA),

  - `groq` (Groq),

  - `cerebras.cloud.sdk` (Cerebras),

  - modelos HuggingFace via `pydantic_ai`.

- **Pandas / NumPy** para manipulação de dados financeiros.

- **dotenv** para gerenciamento de variáveis de ambiente.



### Estrutura do projeto (resumo)



- `notebooks/create_agent_portfolio_optmizer.ipynb`: notebook principal de experimentação, onde são definidos:

  - o roteador de LLMs,

  - os prompts de análise e validação,

  - o grafo de LangGraph para análise fundamentalista,

  - o fluxo de construção de carteira com base nas avaliações dos tickers,

  - exemplos de execução para múltiplos tickers.

- `src/portfolio_optimizer/`: módulos de **coleta** e **tratamento** de dados (fundamentalistas, técnicos, valuation, notícias etc.) utilizados como base para as análises.



### Como o fluxo funciona (alto nível)



1. **Entrada do usuário**: ticker(s) de ações, data inicial e final.

2. **Coleta de dados**: o agente busca e consolida os dados fundamentalistas dos tickers no período solicitado.

3. **Análise inicial**: um LLM avalia cada empresa e produz uma classificação de qualidade com justificativa.

4. **Revisão sênior**: outro LLM verifica se a análise faz sentido à luz dos indicadores e aponta ajustes se necessário.

5. **Iteração / encerramento**: dependendo da avaliação, o fluxo encerra ou refaz a análise até atingir um limite de interações.

6. **Saída**: um dicionário/estado final com classificação, análise, feedback e metadados por ticker, pronto para ser usado em estratégias de **otimização de carteiras**.

7. **Construção de carteira** (segundo fluxo): a partir das saídas do passo 6, o notebook pode selecionar os melhores ativos e construir uma carteira de ações brasileiras, atribuindo pesos e aplicando regras de diversificação.



### Pré-requisitos e configuração (resumo)



- Ter Python instalado e as dependências do projeto (via `uv`, `poetry` ou `pip` conforme seu fluxo).

- Configurar no arquivo `.env` (veja `.env_example`, se existir) as chaves dos provedores de LLM, por exemplo:

  - `CEREBRAS_API_KEY`

  - chaves da NVIDIA, Groq, HuggingFace, etc.



### Uso básico



- Abrir o notebook `notebooks/create_agent_portfolio_optmizer.ipynb`.

- Garantir que o diretório `src` esteja no `PYTHONPATH` (o próprio notebook já faz isso com `sys.path.insert`).

- Executar as células na ordem, ajustando:

  - lista de tickers (`tics` ou `list_tics`),

  - datas `data_inicio` e `data_fim`,

  - provedores/modelos preferidos no `LlmRouter`.



A partir desse fluxo, você obtém uma **camada de análise fundamentalista assistida por LLMs**, bem como um **segundo fluxo de construção de carteira de ações brasileiras**, que juntos podem ser usados para montar carteiras de investimento mais robustas e alinhadas ao seu perfil de risco.