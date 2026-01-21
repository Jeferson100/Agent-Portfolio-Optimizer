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
|        |   preco_inicial(2026-01-02) |   preco_atual(2026-01-19) |   pesos_carteira |   diferenca_inicio_atual |   diferenca_inicio_atual(em %) |   valor_inicial_investido_1000 |   valor_atual_investido_1000 |
|:-------|----------------------------:|--------------------------:|-----------------:|-------------------------:|-------------------------------:|-------------------------------:|-----------------------------:|
| MULT3  |                       27.04 |                     29.25 |             0.18 |                     2.21 |                         0.0817 |                            180 |                       194.71 |
| BMOB3  |                       22    |                     23.02 |             0.09 |                     1.02 |                         0.0464 |                             90 |                        94.18 |
| ALOS3  |                       28.55 |                     28.44 |             0.09 |                    -0.11 |                        -0.0039 |                             90 |                        89.65 |
| CLSC4  |                      124.95 |                    132.97 |             0.07 |                     8.02 |                         0.0642 |                             70 |                        74.49 |
| CGRA4  |                       27.3  |                     26.39 |             0.07 |                    -0.91 |                        -0.0333 |                             70 |                        67.67 |
| WEGE3  |                       48.25 |                     46.22 |             0.07 |                    -2.03 |                        -0.0421 |                             70 |                        67.05 |
| ALPA3  |                       10.38 |                     10.28 |             0.07 |                    -0.1  |                        -0.0096 |                             70 |                        69.33 |
| ENEV3  |                       20.02 |                     20.85 |             0.07 |                     0.83 |                         0.0415 |                             70 |                        72.9  |
| FIQE3  |                        4.89 |                      4.95 |             0.07 |                     0.06 |                         0.0123 |                             70 |                        70.86 |
| SBSP3  |                      133.07 |                    124    |             0.07 |                    -9.07 |                        -0.0682 |                             70 |                        65.23 |
| IGTI11 |                       25.31 |                     26.74 |             0.05 |                     1.43 |                         0.0565 |                             50 |                        52.82 |
| CMIG4  |                       11.16 |                     10.79 |             0.05 |                    -0.37 |                        -0.0332 |                             50 |                        48.34 |
| PRIO3  |                       41.76 |                     44.93 |             0.05 |                     3.17 |                         0.0759 |                             50 |                        53.8  |
### Comentário sobre a carteira
A carteira de investimentos apresentou uma variação de 2,1% no período analisado, considerando um investimento inicial de R$1.000. Para avaliar sua performance, é fundamental analisar os dados fornecidos.

Os dados mostram que a carteira é diversificada, com investimentos distribuídos em 13 ativos diferentes. A distribuição dos pesos na carteira varia entre 0,05 e 0,18, indicando uma diversificação relativamente equilibrada, com destaque para MULT3, que detém 18% do peso total.

Ao examinar a variação individual dos ativos, nota-se que 8 dos 13 ativos apresentaram variação positiva, enquanto 5 tiveram desempenho negativo. Os destaques positivos incluem MULT3 (8,17%), PRIO3 (7,59%) e CLSC4 (6,42%), que contribuíram significativamente para o resultado geral da carteira. Por outro lado, os ativos com pior desempenho foram SBSP3 (-6,82%), WEGE3 (-4,21%) e CGRA4 (-3,33%).

A análise da contribuição individual dos ativos para o resultado geral da carteira é crucial. MULT3, com seu peso de 18%, foi o principal contribuinte para o resultado positivo, com uma contribuição de aproximadamente 1,47% (0,18 x 8,17%). Outros ativos, como PRIO3 e CLSC4, também contribuíram positivamente, com 0,38% e 0,45%, respectivamente.

Por outro lado, os ativos com desempenho negativo, como SBSP3 e WEGE3, tiveram um impacto negativo na carteira. SBSP3, com um peso de 7%, contribuiu negativamente em aproximadamente -0,48% (0,07 x -6,82%). WEGE3 e CGRA4 também tiveram contribuições negativas, embora menores.

Considerando o resultado geral da carteira (2,1%), é possível afirmar que a performance foi satisfatória, uma vez que superou a variação do Ibovespa no mesmo período (embora o valor exato da variação do Ibovespa não seja fornecido). Além disso, a diversificação da carteira ajudou a mitigar os efeitos negativos dos ativos com pior desempenho.

No entanto, é importante notar que a carteira poderia ter apresentado um desempenho ainda melhor se os ativos com pior performance tivessem apresentado resultados mais satisfatórios. Portanto, é recomendável revisar a composição da carteira e considerar ajustes para otimizar o desempenho futuro.

Em resumo, a carteira apresentou uma performance satisfatória no período analisado, com uma variação de 2,1%. A diversificação e a presença de ativos com desempenho positivo foram fundamentais para esse resultado. No entanto, é necessário continuar monitorando o desempenho dos ativos e realizar ajustes quando necessário para garantir a maximização dos retornos.


## 🤖 Agentes e Fluxos de Trabalho

### Agente Avaliação TICS

O agente [Avaliação TICS](https://github.com/Jeferson100/Agent-Portfolio-Optimizer/blob/main/src/portfolio_optimizer/build_langgraph/graph_avaliacao_tics.py) é responsável por processar indicadores financeiros brutos e transformá-los em inteligência de investimento. O fluxo opera sob um sistema de auto-correção que garante a qualidade da análise. O fluxo é o seguinte:

![Fluxo do agente](https://github.com/Jeferson100/Agent-Portfolio-Optimizer/raw/main/image/agente_avaliador_tics.png)

- [Coleta Fundamentalista](https://github.com/Jeferson100/Agent-Portfolio-Optimizer/blob/main/src/portfolio_optimizer/build_langgraph/nodes_avaliacao_tics.py): O primeiro nó extrai uma série histórica de 8 trimestres dos principais indicadores da empresa, incluindo:

  - Eficiência e Lucratividade: Receita Líquida, EBITDA, Margem Líquida e Lucro por Ação (LPA).

  - Endividamento: Alavancagem Financeira e Dívida Líquida/EBITDA.

  - Valuation e Fluxo de Caixa: P/L, P/VPA, Fluxo de Caixa Operacional e Variação de Caixa.

- [Analise fundamentalista](https://github.com/Jeferson100/Agent-Portfolio-Optimizer/blob/main/src/portfolio_optimizer/build_langgraph/nodes_avaliacao_tics.py): O segundo nó processa esses dados para atribuir um rating ao ativo (`Excellent`, `Good`, `Fair`, `Poor` ou `Very Poor`) acompanhado de uma justificativa.

- [Avaliação Analise](https://github.com/Jeferson100/Agent-Portfolio-Optimizer/blob/main/src/portfolio_optimizer/build_langgraph/nodes_avaliacao_tics.py): O nó Avaliação da Análise atua como um revisor, validando a coerência lógica entre os dados e a classificação dada.

Nota de Robustez: Se a análise for considerada insuficiente, o fluxo entra em um loop de reprocessamento (limitado a 4 tentativas) para garantir que apenas classificações consistentes sejam entregues ao próximo agente.

### Agente Criador de Carteira de Ações

Esse agente [Criador de Carteira de Ações](https://github.com/Jeferson100/Agent-Portfolio-Optimizer/blob/main/src/portfolio_optimizer/build_langgraph/graph_criador_carteira.py) consolida as avaliações individuais para montar um portfólio de ações brasileiras otimizado. Para maximizar a precisão e evitar a sobrecarga de contexto, o agente foca exclusivamente em ativos com selo de qualidade `Excellent` ou `Good`. O fluxo é o seguinte:

![Fluxo do agente](https://github.com/Jeferson100/Agent-Portfolio-Optimizer/raw/main/image/agente_criador_carteira.png)

Além das avaliações individuais, o agente utiliza uma matriz de correlação entre os ativos como parâmetro de entrada, permitindo mitigar riscos de sobreposição e evitar a concentração em ativos altamente correlacionados.

- [analista_criador_carteira](https://github.com/Jeferson100/Agent-Portfolio-Optimizer/blob/main/src/portfolio_optimizer/build_langgraph/nodes_criador_carteira.py): O primeiro nó  recebe as avaliações do agente de avaliação TICS e retorna uma sugestão de carteira de ações brasileiras com as seguintes restrições:

  - Os ativos devem ter classificação `Excellent` ou `Good`.
  - O ativo de maior peso deve ser de 20% da carteira.
  - O ativo de menor peso deve ser de 5% da carteira.
  - O peso total da carteira deve ser de 100%.
  - Deve-se priorizar a diversificação da carteira.

- [verify_weight_sum](https://github.com/Jeferson100/Agent-Portfolio-Optimizer/blob/main/src/portfolio_optimizer/build_langgraph/nodes_criador_carteira.py): O segundo nó verifica se o peso total da carteira foi de 100%. Se não for, ele retorna um erro.

- [verifica_tics_selecionados](https://github.com/Jeferson100/Agent-Portfolio-Optimizer/blob/main/src/portfolio_optimizer/build_langgraph/nodes_criador_carteira.py): O terceiro nó realiza o cross-check dos tickers sugeridos para garantir que o agente não "inventou" ativos inexistentes durante a geração.

- [analista_avaliador_peso_carteira](https://github.com/Jeferson100/Agent-Portfolio-Optimizer/blob/main/src/portfolio_optimizer/build_langgraph/nodes_criador_carteira.py): O quarto nó recebe a carteira e retorna uma avaliação de qualidade da carteira. Ele retorna um campo booleano de validação e um texto explicando se a carteira é consistente e o que pode ser melhorado.

Tal como o agente anterior, este fluxo possui um ciclo de feedback de 3 iterações para ajustar pesos e ativos até atingir o critério de qualidade exigido.

## Simulação de uma Carteira de Ações ao longo de varios anos

Para simular a validade do agentes, simulei uma carteira de ações brasileiras ao longo de varios anos. Com isso, pude avaliar o desempenho do agente ao longo do tempo e identificar se a estrategia era eficiente.

![Simulação de uma Carteira de Ações ao longo de varios anos](https://github.com/Jeferson100/Agent-Portfolio-Optimizer/blob/main/image/grafico_retornos_carteira_historico.png)

Como funcionou a simulação:

Mantive a mesma idea, peguei um intervalo de dados, geralmente 7 a 8 trimestre, avalie as acoes para aquele intervalo, apos isso selecionei as acaoes avaliadas com selo `Excellent` e `Good`, e apos isso, o proximo agente gerou uma carteira com esses ativos. Para avaliar o desempenho para a carteira desse periodo, avalie essa carteira no proximo trimestre e assim por diante.

Um exemplo:

Para o periodo inicial da simulacao foi de 2013-04-01 ate 2015-01-01, com a avaliacao da carteira de 2015-01-01 para 2015-04-01, e assim por diante.

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
