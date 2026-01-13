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
|        |   preco_inicial(2026-01-02) |   preco_atual(2026-01-12) |   pesos_carteira |   diferenca_inicio_atual |   diferenca_inicio_atual(em %) |   valor_inicial_investido_1000 |   valor_atual_investido_1000 |
|:-------|----------------------------:|--------------------------:|-----------------:|-------------------------:|-------------------------------:|-------------------------------:|-----------------------------:|
| MULT3  |                       27.04 |                     28.82 |             0.18 |                     1.78 |                         0.0658 |                            180 |                       191.84 |
| BMOB3  |                       22    |                     21.86 |             0.09 |                    -0.14 |                        -0.0064 |                             90 |                        89.42 |
| ALOS3  |                       28.55 |                     29.43 |             0.09 |                     0.88 |                         0.0308 |                             90 |                        92.77 |
| CLSC4  |                      124.95 |                    128.25 |             0.07 |                     3.3  |                         0.0264 |                             70 |                        71.85 |
| CGRA4  |                       27.3  |                     26.45 |             0.07 |                    -0.85 |                        -0.0311 |                             70 |                        67.82 |
| WEGE3  |                       48.25 |                     46.75 |             0.07 |                    -1.5  |                        -0.0311 |                             70 |                        67.82 |
| ALPA3  |                       10.38 |                     10.6  |             0.07 |                     0.22 |                         0.0212 |                             70 |                        71.48 |
| ENEV3  |                       20.02 |                     20.73 |             0.07 |                     0.71 |                         0.0355 |                             70 |                        72.48 |
| FIQE3  |                        4.89 |                      4.82 |             0.07 |                    -0.07 |                        -0.0143 |                             70 |                        69    |
| SBSP3  |                      133.07 |                    127.26 |             0.07 |                    -5.81 |                        -0.0437 |                             70 |                        66.94 |
| IGTI11 |                       25.31 |                     26.62 |             0.05 |                     1.31 |                         0.0518 |                             50 |                        52.59 |
| CMIG4  |                       11.16 |                     10.9  |             0.05 |                    -0.26 |                        -0.0233 |                             50 |                        48.84 |
| PRIO3  |                       41.76 |                     43.24 |             0.05 |                     1.48 |                         0.0354 |                             50 |                        51.77 |
### Comentário sobre a carteira
A carteira de investimentos apresentou uma variação de 1,46% no período analisado, entre 02/01/2026 e 12/01/2026. Este desempenho deve ser avaliado considerando a composição da carteira e as variações individuais de cada ativo.

A análise da carteira revela que os ativos MULT3, ALOS3, CLSC4, ALPA3, ENEV3 e IGTI11 apresentaram desempenho positivo, com variações percentuais de 6,58%, 3,08%, 2,64%, 2,12%, 3,55% e 5,18%, respectivamente. Esses ganhos contribuíram para a valorização da carteira. Em contrapartida, os ativos BMOB3, CGRA4, WEGE3, FIQE3, CMIG4 e SBSP3 registraram perdas, com variações negativas de -0,64%, -3,11%, -3,11%, -1,43%, -2,33% e -4,37%, respectivamente.

A composição da carteira é diversificada, com diferentes pesos atribuídos a cada ativo. Os ativos com maior peso são MULT3 (18%), BMOB3 (9%) e ALOS3 (9%). Embora MULT3 e ALOS3 tenham apresentado desempenho positivo, BMOB3 registrou perda, o que afetou o desempenho geral da carteira.

O valor investido inicialmente em cada ativo, proporcionalmente ao peso na carteira, variou de R$ 50.000,00 a R$ 180.000,00, considerando o investimento total de R$ 1.000,00 na carteira. Os ativos com maior investimento inicial foram MULT3 (R$ 180.000,00), BMOB3 (R$ 90.000,00) e ALOS3 (R$ 90.000,00).

A variação da carteira de 1,46% pode ser considerada um desempenho moderado, considerando que alguns ativos apresentaram ganhos significativos, enquanto outros registraram perdas. No entanto, é fundamental avaliar esse desempenho em relação a um benchmark ou índice de referência para determinar se a carteira está apresentando um desempenho satisfatório.

Em uma análise mais detalhada, é possível observar que os ativos com maior peso na carteira tiveram um impacto significativo no desempenho geral. O ganho de 6,58% do ativo MULT3, que representa 18% da carteira, contribuiu positivamente para o resultado final. Por outro lado, as perdas registradas por ativos como BMOB3 e SBSP3, embora com pesos menores, também influenciaram o desempenho da carteira.

Considerando o período de análise e a variação da carteira, é possível concluir que o desempenho foi moderado. Embora alguns ativos tenham apresentado ganhos significativos, as perdas registradas por outros ativos limitaram o potencial de valorização da carteira. Portanto, é recomendável monitorar o desempenho dos ativos e realizar ajustes na composição da carteira, se necessário, para otimizar o retorno do investimento.

Além disso, é fundamental considerar os riscos associados a cada ativo e à carteira como um todo. A diversificação da carteira é um aspecto positivo, pois ajuda a mitigar os riscos. No entanto, é importante continuar monitorando o desempenho dos ativos e realizar ajustes para garantir que a carteira continue a atender aos objetivos de investimento.

Em resumo, o desempenho da carteira no período analisado foi moderado, com uma variação de 1,46%. Embora alguns ativos tenham apresentado ganhos significativos, as perdas registradas por outros limitaram o potencial de valorização da carteira. É recomendável continuar monitorando o desempenho dos ativos e realizar ajustes na composição da carteira para otimizar o retorno do investimento.


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
