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
A carteira de investimentos apresentou uma variação de 1,79% no período analisado, considerando um investimento inicial de R$1.000,00. Este desempenho pode ser considerado moderado, especialmente se levarmos em conta o contexto de mercado durante o período de 02 de janeiro de 2026 a 09 de janeiro de 2026.

Uma análise detalhada dos ativos que compõem a carteira revela que os investimentos estão distribuídos entre diferentes ações e um fundo imobiliário (IGTI11), com pesos variados na carteira. Observa-se que os ativos com maior peso são MULT3 (18%), BMOB3 (9%) e ALOS3 (9%), indicando uma concentração moderada nos três principais ativos.

Os destaques positivos na carteira incluem MULT3, com uma valorização de 6,1% no período, contribuindo significativamente para o desempenho geral devido ao seu peso na carteira. Outros ativos que apresentaram desempenho positivo incluem IGTI11 (4,9%), ENEV3 (3,7%), CLSC4 (3,64%), e ALOS3 (2,42%). Estes ativos, juntos, ajudaram a impulsionar o desempenho da carteira.

Por outro lado, alguns ativos apresentaram desempenho negativo, como WEGE3 (-4,46%), CGRA4 (-2,56%), e SBSP3 (-1,18%). Embora esses desempenhos individuais negativos tenham sido parcialmente compensados pelos ganhos em outros ativos, é importante monitorar esses ativos para entender as causas subjacentes de suas quedas e decidir se ajustes são necessários.

A diversificação da carteira entre diferentes setores e ativos parece ter contribuído para mitigar perdas potenciais, uma vez que a variação negativa em alguns ativos foi compensada pela valorização em outros. No entanto, é crucial avaliar se essa diversificação está alinhada com os objetivos de investimento e o perfil de risco do investidor.

Considerando o desempenho geral e a composição da carteira, pode-se dizer que a performance é satisfatória, dado o contexto. A valorização de 1,79% no período é um resultado razoável, especialmente se considerarmos que o mercado pode ter apresentado volatilidade durante o período.

No entanto, é fundamental continuar monitorando a carteira e realizar análises periódicas para garantir que ela permaneça alinhada com os objetivos do investidor e que os ativos continuem a apresentar potencial de crescimento. Ajustes na composição da carteira podem ser necessários à medida que as condições de mercado mudam e novos dados se tornam disponíveis.

Além disso, uma análise mais aprofundada dos ativos com desempenho negativo, bem como uma avaliação das perspectivas futuras para esses e outros ativos na carteira, é recomendada para otimizar o desempenho da carteira nos próximos períodos.


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
