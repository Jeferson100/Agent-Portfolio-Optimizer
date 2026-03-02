# Agent Portfolio Optimizer

|||
|-----------|-----------|
| **Testing**  | [![Testes CI e CD](https://github.com/Jeferson100/Agent-Portfolio-Optimizer/actions/workflows/testes_ci_cd.yml/badge.svg)](https://github.com/Jeferson100/Agent-Portfolio-Optimizer/actions/workflows/testes_ci_cd.yml) ||
| **Tecnologias**  | ![Python](https://img.shields.io/badge/Python-3.12%2B-blue?style=flat&logo=python) [![LangGraph](https://img.shields.io/badge/LangGraph-gray?style=flat&logo=langgraph&logoColor=white)](https://langchain-ai.github.io/langgraph/) [![LangChain](https://img.shields.io/badge/LangChain-gray?style=flat&logo=langchain&logoColor=white)](https://www.langchain.com/)  ![Pydantic](https://img.shields.io/badge/Pydantic-gray?style=flat&logo=pydantic&logoColor=purple) [![HuggingFace](https://img.shields.io/badge/HuggingFace-gray?style=flat&logo=huggingface)](https://huggingface.co/)  ![NVIDIA](https://img.shields.io/badge/-NVIDIA-gray?logo=nvidia) [![Cerebras](https://img.shields.io/badge/-Cerebras-gray?logo=cerebras/)](https://www.cerebras.ai/) [![Groq](https://img.shields.io/badge/Groq-gray?style=flat&logo=groq&logoColor=white)](https://groq.com/) ![Pandas](https://img.shields.io/badge/pandas-gray?style=flat&logo=pandas&logoColor=150458)||


## 👁️ Visão geral

**Agent Portfolio Optimizer** é uma solução inteligente em Python que automatiza a análise fundamentalista de ações brasileiras (B3) utilizando Large Language Models (LLMs). O sistema avalia empresas, classifica ativos por qualidade e constrói carteiras otimizadas através de uma arquitetura multi-agente baseada em **LangGraph**, onde cada agente especializado contribui para decisões de investimento fundamentadas e diversificadas. 

Primero um agente avalia os ativos classificando-os por qualidade atraves dos dados fundamentais, essa classificacao pode ser `Excellent`, `Good`, `Fair`, `Poor` ou `Very Poor`, depois outro agente cria uma carteira de ações com os ativos com qualidade `Excellent` e `Good` tendo como restrição que ativos de maior peso devem ser de 20% da carteira e ativos de menor peso devem ser de 5% da carteira.


## Avisos importantes

⚠️ **Este projeto é para fins educacionais e de pesquisa. Não constitui aconselhamento financeiro.**

- As análises geradas por LLMs podem conter erros ou alucinações
- Sempre valide os resultados antes de tomar decisões de investimento
- O desempenho passado não garante resultados futuros
- Consulte um profissional de investimentos qualificado antes de investir


## 📋 Modelos usados e provedores

| Provedor | Modelos Disponíveis |
|-----------|-----------|
| **NVIDIA (API)** | `nvidia/nemotron-3-nano-30b-a3b`, `moonshotai/kimi-k2-instruct`, `deepseek-ai/deepseek-v3.2`, `moonshotai/kimi-k2-instruct-0905`, `meta/llama-4-scout-17b-16e-instruct`, `qwen/qwen3-next-80b-a3b-instruct`|
| **Groq** | `moonshotai/kimi-k2-instruct-0905`, `meta-llama/llama-4-scout-17b-16e-instruct`, `openai/gpt-oss-120b` | 
| **Cerebras** | `qwen-3-235b-a22b-instruct-2507`, `gpt-oss-120b`, `qwen-3-32b` |
| **Nvidia com OpenAI** | `qwen/qwen3-next-80b-a3b-instruct`, `deepseek-ai/deepseek-v3.2`, `nvidia/nemotron-3-nano-30b-a3b` , `moonshotai/kimi-k2-instruct`, `nvidia/nemotron-4-mini-hindi-4b-instruct`|

## 💼 Carteria de ações para o trimestre

### 📊 Tabela Resultados

|        |   preco_inicial(2026-01-02) |   preco_atual(2026-02-27) |   pesos_carteira |   diferenca_inicio_atual |   diferenca_inicio_atual(em %) |   valor_inicial_investido_1000 |   valor_atual_investido_1000 |
|:-------|----------------------------:|--------------------------:|-----------------:|-------------------------:|-------------------------------:|-------------------------------:|-----------------------------:|
| MULT3  |                       27.04 |                     35.2  |             0.18 |                     8.16 |                         0.3018 |                            180 |                       234.32 |
| BMOB3  |                       22    |                     24.2  |             0.09 |                     2.2  |                         0.1    |                             90 |                        99    |
| ALOS3  |                       28    |                     32.69 |             0.09 |                     4.69 |                         0.1675 |                             90 |                       105.08 |
| CLSC4  |                      124.95 |                    150.5  |             0.07 |                    25.55 |                         0.2045 |                             70 |                        84.32 |
| CGRA4  |                       27.3  |                     27.51 |             0.07 |                     0.21 |                         0.0077 |                             70 |                        70.54 |
| WEGE3  |                       48.25 |                     49.7  |             0.07 |                     1.45 |                         0.0301 |                             70 |                        72.11 |
| ALPA3  |                       10.38 |                     13.2  |             0.07 |                     2.82 |                         0.2717 |                             70 |                        89.02 |
| ENEV3  |                       20.02 |                     21.4  |             0.07 |                     1.38 |                         0.0689 |                             70 |                        74.82 |
| FIQE3  |                        4.89 |                      5.28 |             0.07 |                     0.39 |                         0.0798 |                             70 |                        75.59 |
| SBSP3  |                      133.07 |                    153.89 |             0.07 |                    20.82 |                         0.1565 |                             70 |                        80.96 |
| IGTI11 |                       25.16 |                     29.22 |             0.05 |                     4.06 |                         0.1614 |                             50 |                        58.07 |
| CMIG4  |                       11.16 |                     12.07 |             0.05 |                     0.91 |                         0.0815 |                             50 |                        54.08 |
| PRIO3  |                       41.76 |                     54.49 |             0.05 |                    12.73 |                         0.3048 |                             50 |                        65.24 |

### 💬 Comentário sobre a carteira
A carteira de investimentos apresentou uma variação de 16,32% no período analisado, entre 02/01/2026 e 27/02/2026. Este desempenho pode ser considerado satisfatório, dado que reflete uma rentabilidade positiva significativa em um curto período.

Ao examinar os dados fornecidos, observa-se que a carteira é diversificada, com investimentos distribuídos em 13 ativos diferentes. A diversificação é uma estratégia importante para gerenciar o risco, e neste caso, parece ter contribuído para um desempenho estável.

Os ativos que mais contribuíram para o desempenho positivo da carteira foram MULT3, com uma valorização de 30,18%, e PRIO3, com uma valorização de 30,48%. Esses dois ativos, juntos, representam 23% da carteira e contribuíram significativamente para a rentabilidade total. Outros ativos, como ALOS3 e CLSC4, também apresentaram desempenhos notáveis, com valorizações de 16,75% e 20,45%, respectivamente.

Por outro lado, alguns ativos apresentaram desempenhos mais modestos. CGRA4, por exemplo, teve uma valorização de apenas 0,77%, enquanto WEGE3 subiu 3,01%. Embora esses desempenhos sejam menos expressivos, ainda assim contribuíram positivamente para a carteira.

É importante notar que a carteira apresenta uma concentração relativamente alta nos primeiros cinco ativos (MULT3, BMOB3, ALOS3, CLSC4 e CGRA4), que juntos representam 50% do total investido. Embora essa concentração possa aumentar o risco, os dados sugerem que a escolha desses ativos foi acertada, dado que a maioria deles apresentou desempenhos positivos.

Considerando o valor inicial investido de R$1.000 na carteira como um todo, o valor atual é de aproximadamente R$1.163,20, representando um ganho de R$163,20. Esse resultado é bastante animador e sugere que a estratégia de investimento adotada está funcionando.

Em resumo, a carteira de investimentos apresentou um desempenho satisfatório no período analisado, com uma rentabilidade de 16,32%. A diversificação e a escolha acertada dos ativos contribuíram para esse resultado. Embora haja espaço para ajustes e melhorias, a estratégia atual parece estar no caminho certo. Recomenda-se continuar monitorando o desempenho dos ativos e ajustando a carteira conforme necessário para manter o alinhamento com os objetivos de investimento.

Além disso, seria interessante realizar uma análise mais aprofundada dos fatores que influenciaram o desempenho dos ativos, bem como avaliar a sensibilidade da carteira a diferentes cenários de mercado. Isso poderia ajudar a identificar oportunidades de melhoria e a otimizar a estratégia de investimento para os próximos períodos.


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



## 🔍 Lista de ações avaliadas

|     | Empresa      | Segmento de Listagem              | Setor                           | Segmento                                 | tic    |
|----:|:-------------|:----------------------------------|:--------------------------------|:-----------------------------------------|:-------|
|   0 | ALLIAR       | Novo Mercado                      | Saúde                           | Serv.Méd.Hospit..Análises e Diagnósticos | AALR3  |
|   1 | AMBEV S/A    | Tradicional - BOVESPA             | Consumo não Cíclico             | Cervejas e Refrigerantes                 | ABEV3  |
|   2 | AFLUENTE T   | Tradicional - BOVESPA             | Utilidade Pública               | Energia Elétrica                         | AFLT3  |
|   3 | BRASILAGRO   | Novo Mercado                      | Consumo não Cíclico             | Agricultura                              | AGRO3  |
|   4 | AGROGALAXY   | Novo Mercado                      | Consumo não Cíclico             | Agricultura                              | AGXY3  |
|   5 | SPTURIS      | Tradicional - BOVESPA             | Consumo Cíclico                 | Produção de Eventos e Shows              | AHEB3  |
|   6 | ALPARGATAS   | Nível 1 de Governança Corporativa | Consumo Cíclico                 | Calçados                                 | ALPA3  |
|   7 | ALPARGATAS   | Nível 1 de Governança Corporativa | Consumo Cíclico                 | Calçados                                 | ALPA4  |
|   8 | ESTAPAR      | Novo Mercado                      | Bens Industriais                | Serviços Diversos                        | ALPK3  |
|   9 | ALLIED       | Novo Mercado                      | Consumo Cíclico                 | Eletrodomésticos                         | ALLD3  |
|  10 | ALLOS        | Novo Mercado                      | Financeiro                      | Exploração de Imóveis                    | ALOS3  |
|  11 | AMBIPAR      | Novo Mercado                      | Utilidade Pública               | Água e Saneamento                        | AMBP3  |
|  12 | LOJAS MARISA | Novo Mercado                      | Consumo Cíclico                 | Tecidos. Vestuário e Calçados            | AMAR3  |
|  13 | AMERICANAS   | Novo Mercado                      | Consumo Cíclico                 | Produtos Diversos                        | AMER3  |
|  14 | ANIMA        | Novo Mercado                      | Consumo Cíclico                 | Serviços Educacionais                    | ANIM3  |
|  15 | ASSAI        | Novo Mercado                      | Consumo não Cíclico             | Alimentos                                | ASAI3  |
|  16 | AUREN        | Novo Mercado                      | Utilidade Pública               | Energia Elétrica                         | AURE3  |
|  17 | ALPHAVILLE   | Novo Mercado                      | Consumo Cíclico                 | Incorporações                            | AVLL3  |
|  18 | AZEVEDO      | Tradicional - BOVESPA             | Bens Industriais                | Construção Pesada                        | AZEV3  |
|  19 | AZUL         | Nível 2 de Governança Corporativa | Bens Industriais                | Transporte Aéreo                         | AZUL4  |
|  20 | AZZAS 2154   | Novo Mercado                      | Consumo Cíclico                 | Tecidos. Vestuário e Calçados            | AZZA3  |
|  21 | BAUMER       | Tradicional - BOVESPA             | Saúde                           | Equipamentos                             | BALM4  |
|  22 | EXCELSIOR    | Tradicional - BOVESPA             | Consumo não Cíclico             | Carnes e Derivados                       | BAUH4  |
|  23 | AMAZONIA     | Tradicional - BOVESPA             | Financeiro                      | Bancos                                   | BAZA3  |
|  24 | BRASIL       | Novo Mercado                      | Financeiro                      | Bancos                                   | BBAS3  |
|  25 | BBSEGURIDADE | Novo Mercado                      | Financeiro                      | Seguradoras                              | BBSE3  |
|  26 | BRADESCO     | Nível 1 de Governança Corporativa | Financeiro                      | Bancos                                   | BBDC3  |
|  27 | BRADESCO     | Nível 1 de Governança Corporativa | Financeiro                      | Bancos                                   | BBDC4  |
|  28 | BANESE       | Tradicional - BOVESPA             | Financeiro                      | Bancos                                   | BGIP3  |
|  29 | BANESE       | Tradicional - BOVESPA             | Financeiro                      | Bancos                                   | BGIP4  |
|  30 | BIOMM        | Bovespa Mais                      | Saúde                           | Medicamentos e Outros Produtos           | BIOM3  |
|  31 | BLAU         | Novo Mercado                      | Saúde                           | Medicamentos e Outros Produtos           | BLAU3  |
|  32 | MERCANTIL    | Nível 1 de Governança Corporativa | Financeiro                      | Bancos                                   | BMEB3  |
|  33 | MERCANTIL    | Nível 1 de Governança Corporativa | Financeiro                      | Bancos                                   | BMEB4  |
|  34 | BIC MONARK   | Tradicional - BOVESPA             | Consumo Cíclico                 | Bicicletas                               | BMKS3  |
|  35 | MERC INVEST  | Tradicional - BOVESPA             | Financeiro                      | Bancos                                   | BMIN3  |
|  36 | MERC INVEST  | Tradicional - BOVESPA             | Financeiro                      | Bancos                                   | BMIN4  |
|  37 | BEMOBI TECH  | Novo Mercado                      | Tecnologia da Informação        | Programas e Serviços                     | BMOB3  |
|  38 | BANCO PAN    | Nível 1 de Governança Corporativa | Financeiro                      | Bancos                                   | BPAN4  |
|  39 | BTGP BANCO   | Nível 2 de Governança Corporativa | Financeiro                      | Bancos                                   | BPAC11 |
|  40 | BTGP BANCO   | Nível 2 de Governança Corporativa | Financeiro                      | Bancos                                   | BPAC3  |
|  41 | BTGP BANCO   | Nível 2 de Governança Corporativa | Financeiro                      | Bancos                                   | BPAC5  |
|  42 | BRADESPAR    | Nível 1 de Governança Corporativa | Materiais Básicos               | Minerais Metálicos                       | BRAP3  |
|  43 | BRADESPAR    | Nível 1 de Governança Corporativa | Materiais Básicos               | Minerais Metálicos                       | BRAP4  |
|  44 | BRAVA        | Novo Mercado                      | Petróleo. Gás e Biocombustíveis | Exploração. Refino e Distribuição        | BRAV3  |
|  45 | BR PARTNERS  | Nível 2 de Governança Corporativa | Financeiro                      | Bancos                                   | BRBI11 |
|  46 | BRASKEM      | Nível 1 de Governança Corporativa | Materiais Básicos               | Petroquímicos                            | BRKM3  |
|  47 | BRASKEM      | Nível 1 de Governança Corporativa | Materiais Básicos               | Petroquímicos                            | BRKM5  |
|  48 | BRISANET     | Novo Mercado                      | Comunicações                    | Telecomunicações                         | BRST3  |
|  49 | BANRISUL     | Nível 1 de Governança Corporativa | Financeiro                      | Bancos                                   | BRSR3  |
|  50 | BANRISUL     | Nível 1 de Governança Corporativa | Financeiro                      | Bancos                                   | BRSR6  |
|  51 | BRB BANCO    | Tradicional - BOVESPA             | Financeiro                      | Bancos                                   | BSLI3  |
|  52 | BRB BANCO    | Tradicional - BOVESPA             | Financeiro                      | Bancos                                   | BSLI4  |
|  53 | CAMBUCI      | Tradicional - BOVESPA             | Consumo Cíclico                 | Calçados                                 | CAMB3  |
|  54 | CAMIL        | Novo Mercado                      | Consumo não Cíclico             | Alimentos Diversos                       | CAML3  |
|  55 | MELIUZ       | Novo Mercado                      | Tecnologia da Informação        | Programas e Serviços                     | CASH3  |
|  56 | CEA MODAS    | Novo Mercado                      | Consumo Cíclico                 | Tecidos. Vestuário e Calçados            | CEAB3  |
|  57 | CEB          | Tradicional - BOVESPA             | Utilidade Pública               | Energia Elétrica                         | CEBR6  |
|  58 | CEDRO        | Nível 1 de Governança Corporativa | Consumo Cíclico                 | Fios e Tecidos                           | CEDO3  |
|  59 | CEDRO        | Nível 1 de Governança Corporativa | Consumo Cíclico                 | Fios e Tecidos                           | CEDO4  |
|  60 | COMGAS       | Tradicional - BOVESPA             | Utilidade Pública               | Gás                                      | CGAS3  |
|  61 | COMGAS       | Tradicional - BOVESPA             | Utilidade Pública               | Gás                                      | CGAS5  |
|  62 | GRAZZIOTIN   | Tradicional - BOVESPA             | Consumo Cíclico                 | Tecidos. Vestuário e Calçados            | CGRA4  |
|  63 | CELESC       | Nível 2 de Governança Corporativa | Utilidade Pública               | Energia Elétrica                         | CLSC4  |
|  64 | CEMIG        | Nível 1 de Governança Corporativa | Utilidade Pública               | Energia Elétrica                         | CMIG3  |
|  65 | CEMIG        | Nível 1 de Governança Corporativa | Utilidade Pública               | Energia Elétrica                         | CMIG4  |
|  66 | COGNA ON     | Novo Mercado                      | Consumo Cíclico                 | Serviços Educacionais                    | COGN3  |
|  67 | COSAN        | Novo Mercado                      | Petróleo. Gás e Biocombustíveis | Exploração. Refino e Distribuição        | CSAN3  |
|  68 | COPASA       | Novo Mercado                      | Utilidade Pública               | Água e Saneamento                        | CSMG3  |
|  69 | SID NACIONAL | Tradicional - BOVESPA             | Materiais Básicos               | Siderurgia                               | CSNA3  |
|  70 | CSU DIGITAL  | Novo Mercado                      | Financeiro                      | Serviços Financeiros Diversos            | CSUD3  |
|  71 | CYRELA REALT | Novo Mercado                      | Consumo Cíclico                 | Incorporações                            | CYRE3  |
|  72 | DIRECIONAL   | Novo Mercado                      | Consumo Cíclico                 | Incorporações                            | DIRR3  |
|  73 | DEXCO        | Novo Mercado                      | Materiais Básicos               | Madeira                                  | DXCO3  |
|  74 | ACO ALTONA   | Tradicional - BOVESPA             | Bens Industriais                | Máq. e Equip. Industriais                | EALT3  |
|  75 | ACO ALTONA   | Tradicional - BOVESPA             | Bens Industriais                | Máq. e Equip. Industriais                | EALT4  |
|  76 | ECORODOVIAS  | Novo Mercado                      | Bens Industriais                | Exploração de Rodovias                   | ECOR3  |
|  77 | ENGIE BRASIL | Novo Mercado                      | Utilidade Pública               | Energia Elétrica                         | EGIE3  |
|  78 | ENEVA        | Novo Mercado                      | Utilidade Pública               | Energia Elétrica                         | ENEV3  |
|  79 | ENERGISA     | Nível 2 de Governança Corporativa | Utilidade Pública               | Energia Elétrica                         | ENGI11 |
|  80 | ENERGISA     | Nível 2 de Governança Corporativa | Utilidade Pública               | Energia Elétrica                         | ENGI3  |
|  81 | ENERGISA     | Nível 2 de Governança Corporativa | Utilidade Pública               | Energia Elétrica                         | ENGI4  |
|  82 | EQUATORIAL   | Novo Mercado                      | Utilidade Pública               | Energia Elétrica                         | EQTL3  |
|  83 | ESPACOLASER  | Novo Mercado                      | Consumo não Cíclico             | Produtos de Uso Pessoal                  | ESPA3  |
|  84 | EZTEC        | Novo Mercado                      | Consumo Cíclico                 | Incorporações                            | EZTC3  |
|  85 | FERBASA      | Nível 1 de Governança Corporativa | Materiais Básicos               | Siderurgia                               | FESA3  |
|  86 | FERBASA      | Nível 1 de Governança Corporativa | Materiais Básicos               | Siderurgia                               | FESA4  |
|  87 | UNIFIQUE     | Novo Mercado                      | Comunicações                    | Telecomunicações                         | FIQE3  |
|  88 | FLEURY       | Novo Mercado                      | Saúde                           | Serv.Méd.Hospit..Análises e Diagnósticos | FLRY3  |
|  89 | FRAS-LE      | Nível 1 de Governança Corporativa | Bens Industriais                | Material Rodoviário                      | FRAS3  |
|  90 | METALFRIO    | Novo Mercado                      | Bens Industriais                | Máq. e Equip. Industriais                | FRIO3  |
|  91 | GERDAU       | Nível 1 de Governança Corporativa | Materiais Básicos               | Siderurgia                               | GGBR3  |
|  92 | GERDAU       | Nível 1 de Governança Corporativa | Materiais Básicos               | Siderurgia                               | GGBR4  |
|  93 | GERDAU MET   | Nível 1 de Governança Corporativa | Materiais Básicos               | Siderurgia                               | GOAU3  |
|  94 | GERDAU MET   | Nível 1 de Governança Corporativa | Materiais Básicos               | Siderurgia                               | GOAU4  |
|  95 | HAPVIDA      | Novo Mercado                      | Saúde                           | Serv.Méd.Hospit..Análises e Diagnósticos | HAPV3  |
|  96 | HYPERA       | Novo Mercado                      | Saúde                           | Medicamentos e Outros Produtos           | HYPE3  |
|  97 | IGUATEMI S.A | Nível 1 de Governança Corporativa | Financeiro                      | Exploração de Imóveis                    | IGTI3  |
|  98 | IGUATEMI S.A | Nível 1 de Governança Corporativa | Financeiro                      | Exploração de Imóveis                    | IGTI11 |
|  99 | INTELBRAS    | Novo Mercado                      | Tecnologia da Informação        | Computadores e Equipamentos              | INTB3  |
| 100 | IRBBRASIL RE | Novo Mercado                      | Financeiro                      | Resseguradoras                           | IRBR3  |
| 101 | ITAUSA       | Nível 1 de Governança Corporativa | Financeiro                      | Holdings Diversificadas                  | ITSA3  |
| 102 | ITAUSA       | Nível 1 de Governança Corporativa | Financeiro                      | Holdings Diversificadas                  | ITSA4  |
| 103 | ITAUUNIBANCO | Nível 1 de Governança Corporativa | Financeiro                      | Bancos                                   | ITUB3  |
| 104 | ITAUUNIBANCO | Nível 1 de Governança Corporativa | Financeiro                      | Bancos                                   | ITUB4  |
| 105 | JHSF PART    | Novo Mercado                      | Consumo Cíclico                 | Incorporações                            | JHSF3  |
| 106 | KLABIN S/A   | Nível 2 de Governança Corporativa | Materiais Básicos               | Papel e Celulose                         | KLBN3  |
| 107 | KLABIN S/A   | Nível 2 de Governança Corporativa | Materiais Básicos               | Papel e Celulose                         | KLBN4  |
| 108 | KLABIN S/A   | Nível 2 de Governança Corporativa | Materiais Básicos               | Papel e Celulose                         | KLBN11 |
| 109 | LIGHT S/A    | Novo Mercado                      | Utilidade Pública               | Energia Elétrica                         | LIGT3  |
| 110 | LOG COM PROP | Novo Mercado                      | Financeiro                      | Exploração de Imóveis                    | LOGG3  |
| 111 | LOJAS RENNER | Novo Mercado                      | Consumo Cíclico                 | Tecidos. Vestuário e Calçados            | LREN3  |
| 112 | LWSA         | Novo Mercado                      | Tecnologia da Informação        | Programas e Serviços                     | LWSA3  |
| 113 | M.DIASBRANCO | Novo Mercado                      | Consumo não Cíclico             | Alimentos Diversos                       | MDIA3  |
| 114 | MAGAZ LUIZA  | Novo Mercado                      | Consumo Cíclico                 | Eletrodomésticos                         | MGLU3  |
| 115 | MRV          | Novo Mercado                      | Consumo Cíclico                 | Incorporações                            | MRVE3  |
| 116 | MULTIPLAN    | Nível 2 de Governança Corporativa | Financeiro                      | Exploração de Imóveis                    | MULT3  |
| 117 | NEOENERGIA   | Novo Mercado                      | Utilidade Pública               | Energia Elétrica                         | NEOE3  |
| 118 | NUTRIPLANT   | Bovespa Mais                      | Materiais Básicos               | Fertilizantes e Defensivos               | NUTR3  |
| 119 | OI           | Nível 1 de Governança Corporativa | Comunicações                    | Telecomunicações                         | OIBR3  |
| 120 | OI           | Nível 1 de Governança Corporativa | Comunicações                    | Telecomunicações                         | OIBR4  |
| 121 | ONCOCLINICAS | Novo Mercado                      | Saúde                           | Serv.Méd.Hospit..Análises e Diagnósticos | ONCO3  |
| 122 | P.ACUCAR-CBD | Novo Mercado                      | Consumo não Cíclico             | Alimentos                                | PCAR3  |
| 123 | PETROBRAS    | Nível 2 de Governança Corporativa | Petróleo. Gás e Biocombustíveis | Exploração. Refino e Distribuição        | PETR3  |
| 124 | PETROBRAS    | Nível 2 de Governança Corporativa | Petróleo. Gás e Biocombustíveis | Exploração. Refino e Distribuição        | PETR4  |
| 125 | PETZ         | Novo Mercado                      | Consumo Cíclico                 | Produtos Diversos                        | PETZ3  |
| 126 | POSITIVO TEC | Novo Mercado                      | Tecnologia da Informação        | Computadores e Equipamentos              | POSI3  |
| 127 | PORTO SEGURO | Novo Mercado                      | Financeiro                      | Seguradoras                              | PSSA3  |
| 128 | PETRORIO     | Novo Mercado                      | Petróleo. Gás e Biocombustíveis | Exploração. Refino e Distribuição        | PRIO3  |
| 129 | QUALICORP    | Novo Mercado                      | Saúde                           | Serv.Méd.Hospit..Análises e Diagnósticos | QUAL3  |
| 130 | RAIADROGASIL | Novo Mercado                      | Saúde                           | Medicamentos e Outros Produtos           | RADL3  |
| 131 | RUMO S.A.    | Novo Mercado                      | Bens Industriais                | Transporte Ferroviário                   | RAIL3  |
| 132 | RAIZEN       | Nível 2 de Governança Corporativa | Petróleo. Gás e Biocombustíveis | Exploração. Refino e Distribuição        | RAIZ4  |
| 133 | LOCALIZA     | Novo Mercado                      | Consumo Cíclico                 | Aluguel de carros                        | RENT3  |
| 134 | SABESP       | Novo Mercado                      | Utilidade Pública               | Água e Saneamento                        | SBSP3  |
| 135 | SLC AGRICOLA | Novo Mercado                      | Consumo não Cíclico             | Agricultura                              | SLCE3  |
| 136 | SMART FIT    | Novo Mercado                      | Consumo Cíclico                 | Atividades Esportivas                    | SMFT3  |
| 137 | SAO MARTINHO | Novo Mercado                      | Consumo não Cíclico             | Açucar e Alcool                          | SMTO3  |
| 138 | SUZANO S.A.  | Novo Mercado                      | Materiais Básicos               | Papel e Celulose                         | SUZB3  |
| 139 | TAESA        | Nível 2 de Governança Corporativa | Utilidade Pública               | Energia Elétrica                         | TAEE11 |
| 140 | TAESA        | Nível 2 de Governança Corporativa | Utilidade Pública               | Energia Elétrica                         | TAEE3  |
| 141 | TAESA        | Nível 2 de Governança Corporativa | Utilidade Pública               | Energia Elétrica                         | TAEE4  |
| 142 | TAURUS ARMAS | Nível 2 de Governança Corporativa | Bens Industriais                | Armas e Munições                         | TASA3  |
| 143 | TAURUS ARMAS | Nível 2 de Governança Corporativa | Bens Industriais                | Armas e Munições                         | TASA4  |
| 144 | TIM          | Novo Mercado                      | Comunicações                    | Telecomunicações                         | TIMS3  |
| 145 | TOTVS        | Novo Mercado                      | Tecnologia da Informação        | Programas e Serviços                     | TOTS3  |
| 146 | TRISUL       | Novo Mercado                      | Consumo Cíclico                 | Incorporações                            | TRIS3  |
| 147 | ULTRAPAR     | Novo Mercado                      | Petróleo. Gás e Biocombustíveis | Exploração. Refino e Distribuição        | UGPA3  |
| 148 | USIMINAS     | Nível 1 de Governança Corporativa | Materiais Básicos               | Siderurgia                               | USIM3  |
| 149 | USIMINAS     | Nível 1 de Governança Corporativa | Materiais Básicos               | Siderurgia                               | USIM5  |
| 150 | VALE         | Novo Mercado                      | Materiais Básicos               | Minerais Metálicos                       | VALE3  |
| 151 | TELEF BRASIL | Tradicional - BOVESPA             | Comunicações                    | Telecomunicações                         | VIVT3  |
| 152 | WEG          | Novo Mercado                      | Bens Industriais                | Motores . Compressores e Outros          | WEGE3  |
| 153 | WIZ CO       | Novo Mercado                      | Financeiro                      | Corretoras de Seguros e Resseguros       | WIZC3  |
| 154 | WHIRLPOOL    | Tradicional - BOVESPA             | Consumo Cíclico                 | Eletrodomésticos                         | WHRL3  |
| 155 | ABC BRASIL   | Nível 2 de Governança Corporativa | Financeiro                      | Bancos                                   | ABCB4  |
| 156 | YDUQS PART   | Novo Mercado                      | Consumo Cíclico                 | Serviços Educacionais                    | YDUQ3  |



## 📁 Estrutura do projeto

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
│   ├── rodando_carteira_historica/   # Carteiras históricas
│   │   ├── rodando_agente_avaliador_tics_historico_2013-04-01_to_2015-01-01.py
│   │   ├── rodando_agente_avaliador_tics_historico_2013-07-01_to_2015-04-01.py
│   │   ├── ...
│   │   ├── rodando_criando_carteira_historico.py.py
│   │   └── rodando_avaliacao_carteira_historica.py
│   ├── rodando_avaliacao_tics.py
│   ├── rodando_criando_carteira.py
│   └── ...
├── tests/                            # Testes automatizados
│   ├── test_build_langgraph/
│   ├── test_roteador_llms/
│   └── ...
├── data/                             # Dados e resultados
│   ├── avaliacao_historicos_tics/
│   │   ├── avaliacao_tics_historico_2013-04-01_to_2015-01-01.json
│   │   ├── avaliacao_tics_historico_2013-07-01_to_2015-04-01.json
│   │   └── ...
│   ├── historico_carteira/
│   │   ├── pesos_2013-04-01_to_2015-01-01_carteira.csv
│   │   ├── pesos_2013-07-01_to_2015-04-01_carteira.csv
│   │   └── ...
│   ├── historico_carteira_markowitz/
│   │   ├── pesos_2013-04-01_to_2015-01-01_carteira_markowitz.csv
│   │   ├── pesos_2013-07-01_to_2015-04-01_carteira_markowitz.csv
│   │   └── ...
│   ├── resultado_carteira_futuro/
│   │   ├── resultado_carteira_atual.csv
│   │   └── ...
│   └── carteira_resultado.json
└── pyproject.toml                    # Configuração do projeto
```
## Licença

Este projeto está licenciado sob a licença especificada no arquivo [LICENSE](LICENSE).
