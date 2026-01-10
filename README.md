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
|        |   preco_inicial(2026-01-02) |   preco_atual(2026-01-09) |   pesos_carteira |   diferenca_inicio_atual |   diferenca_inicio_atual(em %) |   valor_inicial_investido_1000 |   valor_atual_investido_1000 |
|:-------|----------------------------:|--------------------------:|-----------------:|-------------------------:|-------------------------------:|-------------------------------:|-----------------------------:|
| MULT3  |                       27.04 |                     28.69 |             0.18 |                     1.65 |                         0.061  |                            180 |                       190.98 |
| BMOB3  |                       22    |                     22.21 |             0.09 |                     0.21 |                         0.0095 |                             90 |                        90.86 |
| ALOS3  |                       28.55 |                     29.24 |             0.09 |                     0.69 |                         0.0242 |                             90 |                        92.18 |
| CLSC4  |                      124.95 |                    129.5  |             0.07 |                     4.55 |                         0.0364 |                             70 |                        72.55 |
| CGRA4  |                       27.3  |                     26.6  |             0.07 |                    -0.7  |                        -0.0256 |                             70 |                        68.21 |
| WEGE3  |                       48.25 |                     46.1  |             0.07 |                    -2.15 |                        -0.0446 |                             70 |                        66.88 |
| ALPA3  |                       10.38 |                     10.56 |             0.07 |                     0.18 |                         0.0173 |                             70 |                        71.21 |
| ENEV3  |                       20.02 |                     20.76 |             0.07 |                     0.74 |                         0.037  |                             70 |                        72.59 |
| FIQE3  |                        4.89 |                      4.93 |             0.07 |                     0.04 |                         0.0082 |                             70 |                        70.57 |
| SBSP3  |                      133.07 |                    131.5  |             0.07 |                    -1.57 |                        -0.0118 |                             70 |                        69.17 |
| IGTI11 |                       25.31 |                     26.55 |             0.05 |                     1.24 |                         0.049  |                             50 |                        52.45 |
| CMIG4  |                       11.16 |                     10.96 |             0.05 |                    -0.2  |                        -0.0179 |                             50 |                        49.1  |
| PRIO3  |                       41.76 |                     42.68 |             0.05 |                     0.92 |                         0.022  |                             50 |                        51.1  |
### Comentário sobre a carteira
O desempenho geral da carteira de investimentos apresentada para o trimestre atual indica uma rentabilidade positiva, embora com variações entre os ativos que a compõem. Ao analisar os dados fornecidos, podemos observar que a carteira teve um investimento inicial de R$ 1000 em cada ativo, totalizando R$ 13.000,00, considerando as 13 ações listadas.

A variação no valor dos investimentos entre o preço inicial (em 2026-01-02) e o preço atual (em 2026-01-09) é um indicador chave para avaliar o desempenho. A tabela fornece a diferença absoluta e percentual entre esses dois preços para cada ação, bem como o valor inicial e atual do investimento de R$ 1000 em cada ativo, ponderado pela participação de cada ação na carteira (`pesos_carteira`).

Entre os destaques positivos, as ações MULT3, IGTI11 e ENEV3 apresentaram as maiores valorizações percentuais, com 6,1%, 4,9% e 3,7%, respectivamente. Essas ações contribuíram significativamente para o desempenho geral positivo da carteira. Outros ativos, como ALOS3, CLSC4, ALPA3, PRIO3 e FIQE3, também apresentaram valorizações, embora em menor magnitude.

Por outro lado, algumas ações registraram perdas. WEGE3 e CGRA4 apresentaram desvalorizações de 4,46% e 2,56%, respectivamente, sendo as principais contribuições negativas para o desempenho da carteira. Outras ações com perdas, embora menores, foram CMIG4 e SBSP3.

Para avaliar a performance geral da carteira, é necessário considerar o peso de cada ação na composição total. A carteira é diversificada entre 13 ativos, com MULT3 tendo a maior participação (18%), seguida por BMOB3, ALOS3, CLSC4, CGRA4, WEGE3, ALPA3, ENEV3, FIQE3 e SBSP3, todas com 7%, e IGTI11, CMIG4 e PRIO3 com 5% cada.

Dada a distribuição dos pesos e as variações nos preços, o valor total investido inicialmente de R$ 13.000,00 passou para aproximadamente R$ 13.222,93, representando uma valorização de cerca de 1,71% no período. Embora o período de análise seja curto (uma semana), essa valorização é um indicador inicial positivo.

Considerando as valorizações e desvalorizações observadas, a carteira apresenta um desempenho satisfatório no período analisado, com as ações mais representativas contribuindo positivamente para o resultado. No entanto, é importante monitorar a tendência dos ativos que apresentaram desvalorização para avaliar se essas perdas são pontuais ou se indicam uma tendência de queda.

Além disso, é fundamental considerar outros fatores, como o contexto econômico, setorial e as perspectivas futuras para os ativos componentes da carteira, para uma avaliação mais completa e precisa de seu desempenho. A diversificação da carteira é um ponto positivo, pois ajuda a mitigar riscos específicos associados a ações individuais.

Em resumo, o desempenho da carteira no período é considerado satisfatório, com uma valorização de 1,71%. A manutenção de uma estratégia de diversificação e o monitoramento contínuo dos ativos são recomendados para garantir a sustentabilidade do desempenho positivo.


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
