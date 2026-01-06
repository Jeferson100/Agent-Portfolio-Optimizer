# Agent Portfolio Optimizer

|||
|-----------|-----------|
| **Testing**  | [![Testes CI e CD](https://github.com/Jeferson100/Agent-Portfolio-Optimizer/actions/workflows/testes_ci_cd.yml/badge.svg)](https://github.com/Jeferson100/Agent-Portfolio-Optimizer/actions/workflows/testes_ci_cd.yml) ||
| **Tecnologias**  | ![Python](https://img.shields.io/badge/Python-3.12%2B-blue?style=flat&logo=python) [![LangGraph](https://img.shields.io/badge/LangGraph-gray?style=flat&logo=langgraph&logoColor=white)](https://langchain-ai.github.io/langgraph/) [![LangChain](https://img.shields.io/badge/LangChain-gray?style=flat&logo=langchain&logoColor=white)](https://www.langchain.com/)  ![Pydantic](https://img.shields.io/badge/Pydantic-gray?style=flat&logo=pydantic&logoColor=purple) [![HuggingFace](https://img.shields.io/badge/HuggingFace-gray?style=flat&logo=huggingface)](https://huggingface.co/)  ![NVIDIA](https://img.shields.io/badge/-NVIDIA-gray?logo=nvidia) [![Cerebras](https://img.shields.io/badge/-Cerebras-gray?logo=cerebras/)](https://www.cerebras.ai/) [![Groq](https://img.shields.io/badge/Groq-gray?style=flat&logo=groq&logoColor=white)](https://groq.com/) ![Pandas](https://img.shields.io/badge/pandas-gray?style=flat&logo=pandas&logoColor=150458)
||

## Visão geral

**Agent Portfolio Optimizer** é uma solução inteligente em Python que automatiza a análise fundamentalista de ações brasileiras (B3) utilizando Large Language Models (LLMs). O sistema avalia empresas, classifica ativos por qualidade e constrói carteiras otimizadas através de uma arquitetura multi-agente baseada em **LangGraph**, onde cada agente especializado contribui para decisões de investimento fundamentadas e diversificadas. 

Primero um agente avalia os ativos classificando-os por qualidade atraves dos dados fundamentais, essa classificacao pode ser `Excellent`, `Good`, `Fair`, `Poor` ou `Very Poor`, depois outro agente cria uma carteira de ações com os ativos com qualidade `Excellent` e `Good` mantendo o maior peso de 20% da carteira para um unio ativo.

## Carteria de ações para a data 



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

### Tecnologias e bibliotecas

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

### Estrutura do projeto

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


### Arquitetura do sistema

O sistema é construído sobre uma arquitetura de agentes multi-etapa:

1. **Camada de coleta de dados**: Módulos especializados coletam dados fundamentalistas, técnicos e de mercado
2. **Camada de processamento**: Dados são tratados e formatados para análise
3. **Camada de agentes LLM**: Agentes especializados analisam e tomam decisões usando LLMs
4. **Camada de orquestração**: LangGraph coordena o fluxo entre agentes
5. **Camada de roteamento**: Sistema de fallback garante disponibilidade dos LLMs

### Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

Certifique-se de que os testes passam antes de submeter:
```bash
pytest
ruff check .
mypy src/
```

### Licença

Este projeto está licenciado sob a licença especificada no arquivo `LICENSE`.

### Links úteis

- [Documentação do LangGraph](https://langchain-ai.github.io/langgraph/)
- [Documentação do Pydantic](https://docs.pydantic.dev/)
- [Repositório no GitHub](https://github.com/Jeferson100/Agent-Portfolio-Optimizer)

### Avisos importantes

⚠️ **Este projeto é para fins educacionais e de pesquisa. Não constitui aconselhamento financeiro.**

- As análises geradas por LLMs podem conter erros ou alucinações
- Sempre valide os resultados antes de tomar decisões de investimento
- O desempenho passado não garante resultados futuros
- Consulte um profissional de investimentos qualificado antes de investir
