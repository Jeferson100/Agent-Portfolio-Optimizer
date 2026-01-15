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
|        |   preco_inicial(2026-01-02) |   preco_atual(2026-01-14) |   pesos_carteira |   diferenca_inicio_atual |   diferenca_inicio_atual(em %) |   valor_inicial_investido_1000 |   valor_atual_investido_1000 |
|:-------|----------------------------:|--------------------------:|-----------------:|-------------------------:|-------------------------------:|-------------------------------:|-----------------------------:|
| MULT3  |                       27.04 |                     28.64 |             0.18 |                     1.6  |                         0.0592 |                            180 |                       190.66 |
| BMOB3  |                       22    |                     21.37 |             0.09 |                    -0.63 |                        -0.0286 |                             90 |                        87.43 |
| ALOS3  |                       28.55 |                     28.97 |             0.09 |                     0.42 |                         0.0147 |                             90 |                        91.32 |
| CLSC4  |                      124.95 |                    130.67 |             0.07 |                     5.72 |                         0.0458 |                             70 |                        73.21 |
| CGRA4  |                       27.3  |                     26.33 |             0.07 |                    -0.97 |                        -0.0355 |                             70 |                        67.52 |
| WEGE3  |                       48.25 |                     47.01 |             0.07 |                    -1.24 |                        -0.0257 |                             70 |                        68.2  |
| ALPA3  |                       10.38 |                     10.45 |             0.07 |                     0.07 |                         0.0067 |                             70 |                        70.47 |
| ENEV3  |                       20.02 |                     21.29 |             0.07 |                     1.27 |                         0.0634 |                             70 |                        74.44 |
| FIQE3  |                        4.89 |                      4.87 |             0.07 |                    -0.02 |                        -0.0041 |                             70 |                        69.71 |
| SBSP3  |                      133.07 |                    124.95 |             0.07 |                    -8.12 |                        -0.061  |                             70 |                        65.73 |
| IGTI11 |                       25.31 |                     26.72 |             0.05 |                     1.41 |                         0.0557 |                             50 |                        52.78 |
| CMIG4  |                       11.16 |                     10.74 |             0.05 |                    -0.42 |                        -0.0376 |                             50 |                        48.12 |
| PRIO3  |                       41.76 |                     44.07 |             0.05 |                     2.31 |                         0.0553 |                             50 |                        52.76 |
### Comentário sobre a carteira
A carteira apresentou uma variação de 1,24% no período analisado, o que indica um desempenho ligeiramente positivo. Considerando o curto período de análise (12 dias), essa rentabilidade pode ser considerada razoável, dependendo do contexto de mercado e das expectativas do investidor.

Uma análise mais detalhada dos dados revela que a carteira é composta por 13 ativos, com pesos variados entre 5% e 18%. O ativo com maior peso é a MULT3, com 18% do total investido, e apresentou uma valorização de 5,92% no período, contribuindo positivamente para o resultado geral da carteira.

Os ativos que mais contribuíram para a valorização da carteira foram MULT3 (com uma contribuição de aproximadamente 1,07% para o resultado total), ENEV3 (com uma contribuição de cerca de 0,44%) e IGTI11 (com uma contribuição de aproximadamente 0,28%). Já os ativos que mais afetaram negativamente o resultado foram SBSP3 (com uma contribuição negativa de cerca de -0,43%), CGRA4 (com uma contribuição negativa de aproximadamente -0,25%) e WEGE3 (com uma contribuição negativa de cerca de -0,18%).

É importante notar que a carteira apresenta uma certa diversificação setorial, com ativos de diferentes setores, o que pode ajudar a reduzir o risco. No entanto, é possível observar que alguns ativos apresentaram desempenhos negativos significativos, como SBSP3 (-6,1%) e CMIG4 (-3,76%), o que pode indicar uma exposição a riscos específicos.

Considerando o valor investido de R$1.000,00 na carteira total, o resultado de 1,24% se traduz em um ganho de R$12,40. Embora seja um resultado modesto, é importante considerar o curto período de análise e o contexto de mercado.

Em resumo, o desempenho da carteira pode ser considerado satisfatório, dado o contexto de curto prazo e a diversificação setorial. No entanto, é fundamental monitorar os ativos que apresentaram desempenhos negativos e avaliar se as posições atuais estão alinhadas com as expectativas e objetivos do investidor. Além disso, é importante considerar a possibilidade de rebalanciamento da carteira para otimizar o desempenho e minimizar os riscos.

Para uma análise mais aprofundada, seria interessante avaliar o desempenho da carteira em um período mais longo, bem como comparar o resultado com benchmarks de mercado relevantes. Isso permitiria uma avaliação mais precisa da capacidade do gestor da carteira em gerar valor para o investidor.


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
