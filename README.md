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



Aqui estão uma tabela com os resultados da carteira de ações para o trimestre atual. A carteira 


### Tabela Resultados
|        |   preco_inicial(2026-01-02) |   preco_atual(2026-01-05) |   pesos_carteira |   diferenca_inicio_atual |   diferenca_inicio_atual(em %) |   valor_inicial_investido_1000 |   valor_atual_investido_1000 |
|:-------|----------------------------:|--------------------------:|-----------------:|-------------------------:|-------------------------------:|-------------------------------:|-----------------------------:|
| MULT3  |                       27.04 |                     27.33 |             0.18 |                     0.29 |                         0.0107 |                            180 |                       181.93 |
| BMOB3  |                       22    |                     22.15 |             0.09 |                     0.15 |                         0.0068 |                             90 |                        90.61 |
| ALOS3  |                       28.55 |                     28.64 |             0.09 |                     0.09 |                         0.0032 |                             90 |                        90.29 |
| CLSC4  |                      124.95 |                    123.13 |             0.07 |                    -1.82 |                        -0.0146 |                             70 |                        68.98 |
| CGRA4  |                       27.3  |                     27.43 |             0.07 |                     0.13 |                         0.0048 |                             70 |                        70.34 |
| WEGE3  |                       48.25 |                     48.08 |             0.07 |                    -0.17 |                        -0.0035 |                             70 |                        69.76 |
| ALPA3  |                       10.38 |                     10.72 |             0.07 |                     0.34 |                         0.0328 |                             70 |                        72.3  |
| ENEV3  |                       20.02 |                     20.1  |             0.07 |                     0.08 |                         0.004  |                             70 |                        70.28 |
| FIQE3  |                        4.89 |                      4.89 |             0.07 |                     0    |                         0      |                             70 |                        70    |
| SBSP3  |                      133.07 |                    131.26 |             0.07 |                    -1.81 |                        -0.0136 |                             70 |                        69.05 |
| IGTI11 |                       25.31 |                     25.6  |             0.05 |                     0.29 |                         0.0115 |                             50 |                        50.58 |
| CMIG4  |                       11.16 |                     11.19 |             0.05 |                     0.03 |                         0.0027 |                             50 |                        50.14 |
| PRIO3  |                       41.76 |                     41.15 |             0.05 |                    -0.61 |                        -0.0146 |                             50 |                        49.27 |
### Comentário sobre a carteira
A carteira de investimentos apresentou uma variação positiva no período analisado, de 2 a 5 de janeiro de 2026. Considerando um investimento inicial de R$ 1000 em cada ativo proporcionalmente à sua participação na carteira, o valor total investido inicialmente seria de R$ 1000. Após a variação dos preços, o valor total da carteira passou para R$ 1003,83.

A análise da performance geral da carteira revela que os ativos com maior peso na composição da carteira foram fundamentais para o resultado observado. MULT3, com 18% de participação, contribuiu significativamente para o resultado positivo, apresentando uma valorização de 1,07%. Outros ativos como BMOB3, ALOS3 e CGRA4 também apresentaram desempenhos positivos, com valorizações de 0,68%, 0,32% e 0,48%, respectivamente.

No entanto, alguns ativos apresentaram desempenhos negativos, como CLSC4 (-1,46%), WEGE3 (-0,35%) e SBSP3 (-1,36%), o que foi parcialmente compensado pelos ganhos observados nos demais ativos. É importante notar que a diversificação da carteira ajudou a mitigar as perdas, uma vez que os ativos com desempenhos negativos não foram capazes de arrastar a carteira para um resultado negativo.

A carteira apresentou uma leve valorização de 0,383% no período, o que pode ser considerado um resultado satisfatório, dado o contexto de curto prazo e a composição da carteira. A variação positiva foi influenciada principalmente pelos ativos com maior peso e valorização no período.

Ao analisar a contribuição individual dos ativos para o resultado geral, observa-se que MULT3 foi o principal contribuinte positivo, com um ganho de R$ 1,93 para cada R$ 1000 investidos inicialmente. Outros ativos, como BMOB3 e ALPA3, também apresentaram contribuições positivas, embora menores.

Já os ativos que apresentaram desempenhos negativos, como CLSC4 e SBSP3, reduziram o resultado geral da carteira. No entanto, a magnitude dessas perdas foi limitada pela diversificação e pela participação desses ativos na carteira.

Em resumo, a performance da carteira no período analisado pode ser considerada satisfatória, uma vez que apresentou uma valorização, ainda que modesta. A diversificação da carteira e a contribuição positiva de alguns ativos com maior peso foram fundamentais para esse resultado. É importante manter o monitoramento da carteira e ajustar a composição, se necessário, para garantir que os objetivos de investimento sejam alcançados.

Considerando o curto período de análise, é razoável esperar que a carteira continue a apresentar variações, tanto positivas quanto negativas. Portanto, é fundamental manter uma estratégia de investimento diversificada e ajustada aos objetivos e tolerância ao risco do investidor.

A análise da carteira sugere que a estratégia de investimento atual está funcionando de forma relativamente eficaz, mas é sempre prudente realizar ajustes e otimizações para maximizar os retornos e minimizar os riscos. Além disso, é essencial manter-se atento às condições de mercado e realizar análises periódicas para garantir que a carteira continue a atender às necessidades e objetivos do investidor.


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

## Roteador de LLMs (`LlmRouter`)

O projeto implementa um sistema inteligente de roteamento de LLMs que permite usar múltiplos provedores com fallback automático:

- **Provedores suportados**:
  - **NVIDIA**: modelos via `langchain-nvidia-ai-endpoints`
  - **Groq**: modelos via `groq`
  - **Cerebras**: modelos via `cerebras-cloud-sdk`
  - **HuggingFace**: modelos via `pydantic-ai`

- **Funcionalidades**:
  - Tenta sequencialmente diferentes provedores/modelos em caso de falha
  - Suporta **saída estruturada com Pydantic** para garantir respostas consistentes
  - Trata respostas em múltiplos formatos (string, dict, objetos) e normaliza para dicionário
  - Logging detalhado para debugging e monitoramento

- **Vantagens**:
  - Redundância: se um provedor falhar, tenta automaticamente o próximo
  - Flexibilidade: permite escolher modelos específicos por provedor
  - Robustez: garante que o sistema continue funcionando mesmo com problemas em um provedor

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
