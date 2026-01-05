## Agent Portfolio Optimizer



### Visão geral

[![Testes CI e CD](https://github.com/Jeferson100/Agent-Portfolio-Optimizer/actions/workflows/testes_ci_cd.yml/badge.svg)](https://github.com/Jeferson100/Agent-Portfolio-Optimizer/actions/workflows/testes_ci_cd.yml)



**Agent Portfolio Optimizer** é um projeto em Python para apoio à tomada de decisão em investimentos, focado em ações brasileiras (B3). Ele combina LLMs com um fluxo de análise fundamentalista automatizado para avaliar empresas, classificar a qualidade dos ativos e apos isso construir uma carteira de ações brasileiras.



# Principais funcionalidades


## Agente Avaliação TICS

O agente [Avaliação TICS](https://github.com/Jeferson100/Agent-Portfolio-Optimizer/blob/main/src/portfolio_optimizer/build_langgraph/graph_avaliacao_tics.py) recebe os dados fundamentais de uma empresa e retorna uma classificação e uma análise textual curta. O fluxo é o seguinte:

![Fluxo do agente](https://github.com/Jeferson100/Agent-Portfolio-Optimizer/raw/main/image/agente_avaliador_tics.png)

- O primeiro node [Coleta fundamentalistas](https://github.com/Jeferson100/Agent-Portfolio-Optimizer/blob/main/src/portfolio_optimizer/build_langgraph/nodes_avaliacao_tics.py) obtem os seguintes dados fundamentais da empresa:

  - Receita líquida
  - EBITDA
  - Lucro por ação
  - Alavancagem financeira
  - Margem líquida
  - P/L
  - P/VPA
  - Fluxo de caixa operacional
  - Divida líquida/EBITDA
  - Variação de caixa equivalentes

- O segundo node [Analise fundamentalista](https://github.com/Jeferson100/Agent-Portfolio-Optimizer/blob/main/src/portfolio_optimizer/build_langgraph/nodes_avaliacao_tics.py) recebe os dados fundamentais e retorna uma classificação e uma análise textual curta indicando por que essa classificação foi dada. O node pode classificar o ativo como `Excellent`, `Good`, `Fair`, `Poor` ou `Very Poor`.

- O terceiro node é chamado de [Avaliação Analise](https://github.com/Jeferson100/Agent-Portfolio-Optimizer/blob/main/src/portfolio_optimizer/build_langgraph/nodes_avaliacao_tics.py), esse node vai avaliar a resposta do node de análise fundamentalista. Ele recebe a classificação e a análise e retorna uma validação booleana indicando se a análise foi adequada.

Esse fluxo é executado até 3 vezes, dependendo da qualidade da análise fundamentalista.


## Agente Criador de Carteira de Ações

 Esse agente [Agente Criador de Carteira de Ações](https://github.com/Jeferson100/Agent-Portfolio-Optimizer/blob/main/src/portfolio_optimizer/build_langgraph/graph_criador_carteira.py) recebe as avaliações do agente de avaliação TICS e cria uma carteira de ações brasileiras. O fluxo é o seguinte:

![Fluxo do agente](https://github.com/Jeferson100/Agent-Portfolio-Optimizer/raw/main/image/agente_criador_carteira.png)

Para diminuir a janela de contexto do agente,só ativos com classificação `Excellent` ou `Good` serão considerados, alem disso é passado para o agente como entrada a correlação entre os ativos.

- O primeiro node [analista_criador_carteira](https://github.com/Jeferson100/Agent-Portfolio-Optimizer/blob/main/src/portfolio_optimizer/build_langgraph/nodes_criador_carteira.py) recebe as avaliações do agente de avaliação TICS e retorna uma sugestão de carteira de ações brasileiras com as seguintes restricoes:

  - Os ativos devem ter classificação `Excellent` ou `Good`.
  - O ativo de maior peso deve ser de 20% da carteira.
  - O ativo de menor peso deve ser de 5% da carteira.
  - O peso total da carteira deve ser de 100%.
  - Deve-se priorizar a diversificação da carteira.

- O segundo node [verify_weight-sum](https://github.com/Jeferson100/Agent-Portfolio-Optimizer/blob/main/src/portfolio_optimizer/build_langgraph/nodes_criador_carteira.py) verifica se o peso total da carteira foi de 100%. Se não for, ele retorna um erro.

- O terceiro node [verifica_tics_selecionados](https://github.com/Jeferson100/Agent-Portfolio-Optimizer/blob/main/src/portfolio_optimizer/build_langgraph/nodes_criador_carteira.py) verifica se os ativos indicados pelo analista criador de carteira de ações existem ou se ele não inventou, indicando uma alucinação. 

- O quarto node [analista_avaliador_peso_carteira](https://github.com/Jeferson100/Agent-Portfolio-Optimizer/blob/main/src/portfolio_optimizer/build_langgraph/nodes_criador_carteira.py)




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