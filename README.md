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
|        |   preco_inicial(2026-01-02) |   preco_atual(2026-01-21) |   pesos_carteira |   diferenca_inicio_atual |   diferenca_inicio_atual(em %) |   valor_inicial_investido_1000 |   valor_atual_investido_1000 |
|:-------|----------------------------:|--------------------------:|-----------------:|-------------------------:|-------------------------------:|-------------------------------:|-----------------------------:|
| MULT3  |                       27.04 |                     30.36 |             0.18 |                     3.32 |                         0.1228 |                            180 |                       202.1  |
| BMOB3  |                       22    |                     23.84 |             0.09 |                     1.84 |                         0.0836 |                             90 |                        97.52 |
| ALOS3  |                       28.26 |                     28.85 |             0.09 |                     0.59 |                         0.0209 |                             90 |                        91.88 |
| CLSC4  |                      124.95 |                    135.98 |             0.07 |                    11.03 |                         0.0883 |                             70 |                        76.18 |
| CGRA4  |                       27.3  |                     26.13 |             0.07 |                    -1.17 |                        -0.0429 |                             70 |                        67    |
| WEGE3  |                       48.25 |                     47.59 |             0.07 |                    -0.66 |                        -0.0137 |                             70 |                        69.04 |
| ALPA3  |                       10.38 |                     10.13 |             0.07 |                    -0.25 |                        -0.0241 |                             70 |                        68.31 |
| ENEV3  |                       20.02 |                     21.55 |             0.07 |                     1.53 |                         0.0764 |                             70 |                        75.35 |
| FIQE3  |                        4.89 |                      5.04 |             0.07 |                     0.15 |                         0.0307 |                             70 |                        72.15 |
| SBSP3  |                      133.07 |                    130.82 |             0.07 |                    -2.25 |                        -0.0169 |                             70 |                        68.82 |
| IGTI11 |                       25.31 |                     27.23 |             0.05 |                     1.92 |                         0.0759 |                             50 |                        53.8  |
| CMIG4  |                       11.16 |                     11.16 |             0.05 |                     0    |                         0      |                             50 |                        50    |
| PRIO3  |                       41.76 |                     46.88 |             0.05 |                     5.12 |                         0.1226 |                             50 |                        56.13 |
### Comentário sobre a carteira
A carteira apresentou uma variação de 4,83% no período analisado, o que indica um desempenho positivo. Considerando que o valor investido foi de R$1.000,00 na carteira total, é possível avaliar a rentabilidade dos ativos que compõem a carteira.

Os dados fornecidos revelam que os ativos com maior peso na carteira são MULT3 (18%), BMOB3 (9%) e ALOS3 (9%). Dentre esses, MULT3 foi o que apresentou o maior ganho, com uma valorização de 12,28% (R$ 3,32 de diferença em relação ao preço inicial), contribuindo significativamente para o desempenho geral da carteira. BMOB3 e ALOS3 também apresentaram ganhos, embora menores, de 8,36% e 2,09%, respectivamente.

Além disso, é notável que alguns ativos com menor peso na carteira também apresentaram desempenhos destacados. PRIO3, por exemplo, teve uma valorização de 12,26% (R$ 5,12 de diferença), e IGTI11 valorizou 7,59% (R$ 1,92 de diferença). Outros ativos, como ENEV3 e FIQE3, também apresentaram ganhos, de 7,64% e 3,07%, respectivamente.

Por outro lado, alguns ativos apresentaram perdas no período. CGRA4, WEGE3, ALPA3 e SBSP3 registraram desvalorizações de -4,29%, -1,37%, -2,41% e -1,69%, respectivamente. No entanto, essas perdas foram compensadas pelos ganhos dos demais ativos, resultando em um desempenho geral positivo da carteira.

É importante observar que a carteira apresenta uma diversificação razoável, com ativos de diferentes setores, o que pode contribuir para a redução do risco. A presença de ativos com desempenhos variados também sugere que a estratégia de investimento adotada busca equilibrar os riscos e as oportunidades de ganho.

Considerando o desempenho geral da carteira e a valorização dos principais ativos, é possível concluir que a carteira está apresentando um desempenho satisfatório no período analisado. A variação de 4,83% é um indicador positivo, especialmente se considerarmos que o período é relativamente curto.

No entanto, é fundamental continuar monitorando o desempenho dos ativos e ajustar a estratégia de investimento conforme necessário. Além disso, é importante considerar outros fatores, como o contexto econômico e as perspectivas para os setores representados na carteira, para tomar decisões informadas e maximizar os retornos.

Em resumo, a carteira está apresentando um desempenho positivo, impulsionado principalmente pelos ganhos de MULT3, PRIO3 e outros ativos. A diversificação da carteira e a presença de ativos com desempenhos variados contribuem para um perfil de risco equilibrado. Com um acompanhamento contínuo e ajustes estratégicos, é possível manter ou melhorar o desempenho da carteira nos próximos períodos.


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

## 📈 Simulação de Carteira de Ações Histórica

Este módulo valida a eficácia dos agentes inteligentes através da simulação de uma carteira de ações brasileiras ao longo de múltiplos anos. O objetivo é avaliar o desempenho das estratégias geradas pelos agentes em diferentes ciclos de mercado para identificar sua consistência e eficiência. 

### ⚖️ Benchmarks e Comparativo de Performance

Para medir a qualidade real das decisões dos agentes, o desempenho da carteira simulada é comparado com três indicadores fundamentais:

1.  **Selic:** Representa o custo de oportunidade e a taxa livre de risco do mercado brasileiro.
2.  **Ibovespa (IBOV):** O principal índice de referência da bolsa brasileira, refletindo a performance média do mercado.
3.  **Fronteira Eficiente de Markowitz (MVO):** * Para cada período, aplicamos a **Otimização de Variância Mínima** de Harry Markowitz sobre os mesmos ativos selecionados pelo agente.
    * Este benchmark calcula matematicamente os pesos ideais para obter o maior retorno possível para um determinado nível de risco (volatilidade).


![Desempenho da Carteira vs Benchmarks](https://github.com/Jeferson100/Agent-Portfolio-Optimizer/raw/main/image/grafico_retornos_carteira_historico.png)

---
### 📊 Metricas de Desempenho

|           |   retorno_medio_anual |   volatilidade_anual |   cagr |   max_drawdown |   avg_drawdown |   calmar |   sortino |
|:----------|----------------------:|---------------------:|-------:|---------------:|---------------:|---------:|----------:|
| Selic     |                   9.3 |                  0.2 |    9.7 |            0   |            0   |    nan   |       nan |
| IBOV      |                  14   |                 23.3 |   11.8 |          -46.8 |           -4   |     25.1 |       nan |
| Markowitz |                  20   |                 22.1 |   18.6 |          -36.3 |           -4.3 |     51.2 |       nan |
| Carteira  |                  21.7 |                 23.5 |   20.2 |          -40.9 |           -5.3 |     49.4 |       nan |



### 🛠️ Metodologia da Simulação

A simulação utiliza uma abordagem de **janelas deslizantes (rolling windows)** para replicar o comportamento real de um investidor:

1.  **Análise Retrospectiva:** O agente analisa um intervalo de dados históricos (geralmente entre 7 e 8 trimestres).
2.  **Filtragem por Qualidade:** São selecionados apenas os ativos que receberam as classificações `Excellent` (Excelente) e `Good` (Bom) durante a análise.
3.  **Otimização e Alocação:** Um agente especializado gera a composição ideal da carteira com base nesses ativos selecionados.
4.  **Validação Out-of-Sample:** O desempenho da carteira é medido no **trimestre subsequente** ao período de análise.

### Exemplo Prático:
* **Período de Análise:** 01/04/2013 a 01/01/2015.
* **Período de Avaliação (Backtest):** O rendimento é calculado entre 01/01/2015 e 01/04/2015.
* **Próximo Passo:** A janela desliza um trimestre à frente e o processo se repete até os dias atuais.

---

### 🚀 Objetivos do Teste
* Validar a capacidade de seleção (Stock Picking) do agente.
* Testar a robustez dos pesos atribuídos a cada ativo.
* Comparar o retorno acumulado e a volatilidade contra benchmarks do mercado brasileiro.

### ⚠️ Considerações Importantes e Limitações

Ao analisar os resultados desta simulação, é necessário considerar dois fatores críticos que podem influenciar os retornos apresentados:

### 1. Viés de Sobrevivência (Survivorship Bias)
A base de dados utilizada pode conter um **viés de sobrevivência**, uma vez que as ações selecionadas são de empresas que permanecem ativas ou listadas até o presente momento. Empresas que faliram, foram deslistadas ou sofreram fusões durante o período de 2013 a 2024 podem não estar totalmente representadas, o que tende a elevar artificialmente a média de retorno histórico do modelo.

### 2. Exposição Crítica e Treinamento do Modelo
Existe a possibilidade de **Data Leakage** (vazamento de dados) ou viés de treinamento. Como os modelos de linguagem (LLMs) utilizados pelos agentes foram treinados com dados históricos que englobam parte do período simulado, o agente pode "conhecer" o sucesso futuro de certas empresas por meio de seus pesos internos de treinamento, em vez de basear sua decisão puramente nos dados do trimestre analisado.

## Tecnologias e bibliotecas

- **Python 3.12+** (ver `pyproject.toml`)
- **Pydantic / Pydantic AI** para modelos de saída estruturada
- **LangGraph** para orquestração do fluxo de agentes/tools
- **Clientes de LLM**:
  - `Nvidia`
  - `openai` (NVIDIA)
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
