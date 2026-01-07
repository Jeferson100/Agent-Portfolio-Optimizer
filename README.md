# Agent Portfolio Optimizer

|||
|-----------|-----------|
| **Testing**  | [![Testes CI e CD](https://github.com/Jeferson100/Agent-Portfolio-Optimizer/actions/workflows/testes_ci_cd.yml/badge.svg)](https://github.com/Jeferson100/Agent-Portfolio-Optimizer/actions/workflows/testes_ci_cd.yml) ||
| **Tecnologias**  | ![Python](https://img.shields.io/badge/Python-3.12%2B-blue?style=flat&logo=python) [![LangGraph](https://img.shields.io/badge/LangGraph-gray?style=flat&logo=langgraph&logoColor=white)](https://langchain-ai.github.io/langgraph/) [![LangChain](https://img.shields.io/badge/LangChain-gray?style=flat&logo=langchain&logoColor=white)](https://www.langchain.com/)  ![Pydantic](https://img.shields.io/badge/Pydantic-gray?style=flat&logo=pydantic&logoColor=purple) [![HuggingFace](https://img.shields.io/badge/HuggingFace-gray?style=flat&logo=huggingface)](https://huggingface.co/)  ![NVIDIA](https://img.shields.io/badge/-NVIDIA-gray?logo=nvidia) [![Cerebras](https://img.shields.io/badge/-Cerebras-gray?logo=cerebras/)](https://www.cerebras.ai/) [![Groq](https://img.shields.io/badge/Groq-gray?style=flat&logo=groq&logoColor=white)](https://groq.com/) ![Pandas](https://img.shields.io/badge/pandas-gray?style=flat&logo=pandas&logoColor=150458)
||

## Visão geral

**Agent Portfolio Optimizer** é uma solução inteligente em Python que automatiza a análise fundamentalista de ações brasileiras (B3) utilizando Large Language Models (LLMs). O sistema avalia empresas, classifica ativos por qualidade e constrói carteiras otimizadas através de uma arquitetura multi-agente baseada em **LangGraph**, onde cada agente especializado contribui para decisões de investimento fundamentadas e diversificadas. 

Primero um agente avalia os ativos classificando-os por qualidade atraves dos dados fundamentais, essa classificacao pode ser `Excellent`, `Good`, `Fair`, `Poor` ou `Very Poor`, depois outro agente cria uma carteira de ações com os ativos com qualidade `Excellent` e `Good` tendo como restrição que ativos de maior peso devem ser de 20% da carteira e ativos de menor peso devem ser de 5% da carteira.


## Carteria de ações para o trimestre
### Tabela Resultados
|        |   preco_inicial(2026-01-02) |   preco_atual(2026-01-06) |   pesos_carteira |   diferenca_inicio_atual |   diferenca_inicio_atual(em %) |   valor_inicial_investido_1000 |   valor_atual_investido_1000 |
|:-------|----------------------------:|--------------------------:|-----------------:|-------------------------:|-------------------------------:|-------------------------------:|-----------------------------:|
| MULT3  |                       27.04 |                     27.71 |             0.18 |                     0.67 |                         0.0248 |                            180 |                       184.46 |
| BMOB3  |                       22    |                     22.45 |             0.09 |                     0.45 |                         0.0205 |                             90 |                        91.84 |
| ALOS3  |                       28.55 |                     29.07 |             0.09 |                     0.52 |                         0.0182 |                             90 |                        91.64 |
| CLSC4  |                      124.95 |                    125.65 |             0.07 |                     0.7  |                         0.0056 |                             70 |                        70.39 |
| CGRA4  |                       27.3  |                     27.15 |             0.07 |                    -0.15 |                        -0.0055 |                             70 |                        69.62 |
| WEGE3  |                       48.25 |                     48.17 |             0.07 |                    -0.08 |                        -0.0017 |                             70 |                        69.88 |
| ALPA3  |                       10.38 |                     10.55 |             0.07 |                     0.17 |                         0.0164 |                             70 |                        71.15 |
| ENEV3  |                       20.02 |                     20.37 |             0.07 |                     0.35 |                         0.0175 |                             70 |                        71.23 |
| FIQE3  |                        4.89 |                      4.94 |             0.07 |                     0.05 |                         0.0102 |                             70 |                        70.71 |
| SBSP3  |                      133.07 |                    130.48 |             0.07 |                    -2.59 |                        -0.0195 |                             70 |                        68.64 |
| IGTI11 |                       25.31 |                     25.76 |             0.05 |                     0.45 |                         0.0178 |                             50 |                        50.89 |
| CMIG4  |                       11.16 |                     11.12 |             0.05 |                    -0.04 |                        -0.0036 |                             50 |                        49.82 |
| PRIO3  |                       41.76 |                     40.82 |             0.05 |                    -0.94 |                        -0.0225 |                             50 |                        48.88 |
### Comentário sobre a carteira
O desempenho geral da carteira de ações no período de 02/01/2026 a 06/01/2026 apresentou uma variação positiva, embora moderada. Considerando um investimento inicial de R$ 1.000,00 em cada ação proporcionalmente à sua participação na carteira, o valor total investido foi de R$ 1.000,00.

A análise dos dados revela que a carteira apresentou uma variação positiva de 0,43% no período, passando de R$ 1.000,00 para R$ 1.004,30. Embora seja um aumento modesto, é importante considerar a composição da carteira e o desempenho individual das ações.

As ações que mais contribuíram positivamente para o desempenho da carteira foram MULT3 (0,18% de participação, com variação de 2,48%), BMOB3 (0,09% de participação, com variação de 2,05%) e ALOS3 (0,09% de participação, com variação de 1,82%). Essas ações juntas representam 36% da carteira e contribuíram com uma variação positiva média de 2,22%.

Por outro lado, as ações que apresentaram desempenho negativo foram CGRA4 (-0,55%), WEGE3 (-0,17%), SBSP3 (-1,95%), CMIG4 (-0,36%) e PRIO3 (-2,25%). Essas ações juntas representam 31% da carteira e contribuíram com uma variação negativa média de -1,06%.

É notável que as ações com maior peso na carteira (MULT3, BMOB3 e ALOS3) apresentaram desempenho positivo, o que ajudou a compensar as perdas das ações com desempenho negativo. Além disso, a diversificação da carteira, com ações de diferentes setores, contribuiu para reduzir o impacto das variações negativas.

Considerando o contexto atual, o desempenho da carteira pode ser considerado satisfatório, uma vez que apresentou uma variação positiva no período. No entanto, é fundamental monitorar o desempenho das ações individuais e ajustar a carteira conforme necessário para garantir que continue a atender aos objetivos de investimento.

Em resumo, o desempenho da carteira de ações no período analisado foi moderadamente positivo, com uma variação de 0,43%. As ações MULT3, BMOB3 e ALOS3 foram as principais contribuintes para o desempenho positivo, enquanto as ações CGRA4, WEGE3, SBSP3, CMIG4 e PRIO3 apresentaram desempenho negativo. A diversificação da carteira e o monitoramento contínuo das ações individuais são fundamentais para garantir um desempenho satisfatório no longo prazo.

É recomendável continuar a monitorar o desempenho da carteira e realizar ajustes periódicos para garantir que a composição da carteira continue a atender aos objetivos de investimento. Além disso, é importante considerar a realização de análises mais aprofundadas das ações individuais para identificar oportunidades de melhoria do desempenho da carteira.


## Fluxo geral

### Agente Avaliação TICS

O agente [Avaliação TICS](https://github.com/Jeferson100/Agent-Portfolio-Optimizer/blob/main/src/portfolio_optimizer/build_langgraph/graph_avaliacao_tics.py) recebe os dados fundamentais de uma empresa e retorna uma classificação e uma análise textual curta. O fluxo é o seguinte:

![Fluxo do agente](https://github.com/Jeferson100/Agent-Portfolio-Optimizer/raw/main/image/agente_avaliador_tics.png)

- O primeiro node [Coleta fundamentalistas](https://github.com/Jeferson100/Agent-Portfolio-Optimizer/blob/main/src/portfolio_optimizer/build_langgraph/nodes_avaliacao_tics.py) obtém os seguintes dados fundamentais da empresa:

  - Receita líquida
  - EBITDA
  - Lucro por ação
  - Alavancagem financeira
  - Margem líquida
  - P/L
  - P/VPA
  - Fluxo de caixa operacional
  - Dívida líquida/EBITDA
  - Variação de caixa equivalentes

  Além disso, são obtidos os dados fundamentais de 8 trimestres anteriores.

- O segundo node [Analise fundamentalista](https://github.com/Jeferson100/Agent-Portfolio-Optimizer/blob/main/src/portfolio_optimizer/build_langgraph/nodes_avaliacao_tics.py) recebe os dados fundamentais e retorna uma classificação e uma análise textual curta indicando por que essa classificação foi dada. O node pode classificar o ativo como `Excellent`, `Good`, `Fair`, `Poor` ou `Very Poor`.

- O terceiro node é chamado de [Avaliação Analise](https://github.com/Jeferson100/Agent-Portfolio-Optimizer/blob/main/src/portfolio_optimizer/build_langgraph/nodes_avaliacao_tics.py), esse node vai avaliar a resposta do node de análise fundamentalista. Ele recebe a classificação e a análise e retorna uma validação booleana indicando se a análise foi adequada.

Esse fluxo é executado até 3 vezes, dependendo da qualidade da análise fundamentalista.

### Agente Criador de Carteira de Ações

Esse agente [Agente Criador de Carteira de Ações](https://github.com/Jeferson100/Agent-Portfolio-Optimizer/blob/main/src/portfolio_optimizer/build_langgraph/graph_criador_carteira.py) recebe as avaliações do agente de avaliação TICS e cria uma carteira de ações brasileiras. O fluxo é o seguinte:

![Fluxo do agente](https://github.com/Jeferson100/Agent-Portfolio-Optimizer/raw/main/image/agente_criador_carteira.png)

Para diminuir a janela de contexto do agente, só ativos com classificação `Excellent` ou `Good` serão considerados, além disso é passado para o agente como entrada a correlação entre os ativos.

- O primeiro node [analista_criador_carteira](https://github.com/Jeferson100/Agent-Portfolio-Optimizer/blob/main/src/portfolio_optimizer/build_langgraph/nodes_criador_carteira.py) recebe as avaliações do agente de avaliação TICS e retorna uma sugestão de carteira de ações brasileiras com as seguintes restrições:

  - Os ativos devem ter classificação `Excellent` ou `Good`.
  - O ativo de maior peso deve ser de 20% da carteira.
  - O ativo de menor peso deve ser de 5% da carteira.
  - O peso total da carteira deve ser de 100%.
  - Deve-se priorizar a diversificação da carteira.

- O segundo node [verify_weight_sum](https://github.com/Jeferson100/Agent-Portfolio-Optimizer/blob/main/src/portfolio_optimizer/build_langgraph/nodes_criador_carteira.py) verifica se o peso total da carteira foi de 100%. Se não for, ele retorna um erro.

- O terceiro node [verifica_tics_selecionados](https://github.com/Jeferson100/Agent-Portfolio-Optimizer/blob/main/src/portfolio_optimizer/build_langgraph/nodes_criador_carteira.py) verifica se os ativos indicados pelo analista criador de carteira de ações existem ou se ele não inventou, indicando uma alucinação.

- O quarto node [analista_avaliador_peso_carteira](https://github.com/Jeferson100/Agent-Portfolio-Optimizer/blob/main/src/portfolio_optimizer/build_langgraph/nodes_criador_carteira.py) recebe a carteira e retorna uma avaliação de qualidade da carteira. Ele retorna um campo booleano de validação e um texto explicando se a carteira é consistente e o que pode ser melhorado.

O fluxo é executado até 3 vezes, tentando melhorar a qualidade da carteira.

## Tecnologias e bibliotecas

- **Python 3.12+** (ver `pyproject.toml`)
- **Pydantic / Pydantic AI** para modelos de saída estruturada
- **LangGraph** para orquestração do fluxo de agentes/tools
- **Clientes de LLM**:
  - `langchain-nvidia-ai-endpoints` (NVIDIA)
  - `groq` (Groq)
  - `cerebras.cloud.sdk` (Cerebras)
  - modelos HuggingFace via `pydantic_ai`
- **Pandas / NumPy** para manipulação de dados financeiros
- **yfinance** para coleta de dados de mercado
- **dotenv** para gerenciamento de variáveis de ambiente
- **Arize Phoenix** para observabilidade e rastreamento de LLMs

## Estrutura do projeto

```
Agent-Portfolio-Optimizer/
├── src/
│   └── portfolio_optimizer/
│       ├── build_langgraph/          # Grafos LangGraph dos agentes
│       │   ├── graph_avaliacao_tics.py
│       │   ├── graph_criador_carteira.py
│       │   ├── nodes_avaliacao_tics.py
│       │   └── nodes_criador_carteira.py
│       ├── coleta_dados/             # Módulos de coleta de dados
│       │   ├── dados_fundamentalistas.py
│       │   ├── dados_indicadores_tecnicos.py
│       │   └── ...
│       ├── roteador_llms/            # Sistema de roteamento de LLMs
│       │   ├── roteador_llms.py
│       │   ├── roteador_nvidia.py
│       │   ├── roteador_groq.py
│       │   ├── roteador_cerebras.py
│       │   └── roteador_huggingface.py
│       ├── prompts/                  # Prompts dos agentes
│       │   ├── prompts_avaliador_tics.py
│       │   └── prompts_criador_carteira.py
│       ├── state_otputs/             # Modelos Pydantic de saída
│       │   ├── output_classicacao_tics.py
│       │   └── output_criador_carteira.py
│       ├── tratando_dados/           # Tratamento e processamento de dados
│       └── utils/                    # Funções utilitárias
├── notebooks/                        # Notebooks de experimentação
│   ├── create_agent_portfolio_optmizer.ipynb
│   └── chamando_agentes.ipynb
├── codigos_rodando/                 # Scripts prontos para execução
│   ├── rodando_avaliacao_tics.py
│   ├── rodando_criando_carteira.py
│   └── ...
├── tests/                            # Testes automatizados
│   ├── test_build_langgraph/
│   ├── test_roteador_llms/
│   └── ...
├── data/                             # Dados e resultados
│   ├── avaliacao_tics_historico.json
│   └── carteira_resultado.json
└── pyproject.toml                    # Configuração do projeto
```
## Licença

Este projeto está licenciado sob a licença especificada no arquivo [LICENSE](LICENSE).

## Avisos importantes

⚠️ **Este projeto é para fins educacionais e de pesquisa. Não constitui aconselhamento financeiro.**

- As análises geradas por LLMs podem conter erros ou alucinações
- Sempre valide os resultados antes de tomar decisões de investimento
- O desempenho passado não garante resultados futuros
- Consulte um profissional de investimentos qualificado antes de investir
