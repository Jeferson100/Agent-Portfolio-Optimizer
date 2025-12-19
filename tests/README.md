# Testes Unitários - Agent Portfolio Optimizer

Este diretório contém os testes unitários e de integração para o projeto Agent Portfolio Optimizer.

## Estrutura dos Testes

```
tests/
├── __init__.py
├── conftest.py                    # Configurações e fixtures compartilhadas
├── README.md                      # Este arquivo
├── test_coleta_dados/            # Testes para módulos de coleta de dados
│   ├── __init__.py
│   ├── test_data_cache.py        # Testes para DataCache
│   └── test_verificador_ticks.py # Testes para VerificadorTicks
├── test_integration/             # Testes de integração
│   ├── __init__.py
│   └── test_portfolio_workflow.py
├── test_state_outputs/           # Testes para estados e outputs
│   ├── __init__.py
│   ├── test_output_criador_carteira.py
│   └── test_state_criador_carteira.py
├── test_tratando_dados/          # Testes para tratamento de dados
│   └── __init__.py
└── test_utils/                   # Testes para utilitários
    ├── __init__.py
    └── test_funcoes_utilitarias.py
```

## Como Executar os Testes

### Executar todos os testes
```bash
pytest
```

### Executar testes com cobertura
```bash
pytest --cov=src/portfolio_optimizer --cov-report=html
```

### Executar testes específicos
```bash
# Testes de um módulo específico
pytest tests/test_coleta_dados/

# Teste específico
pytest tests/test_utils/test_funcoes_utilitarias.py::TestNormalizarPesos::test_pesos_ja_normalizados

# Testes por marcadores
pytest -m unit          # Apenas testes unitários
pytest -m integration   # Apenas testes de integração
pytest -m "not slow"    # Excluir testes lentos
```

### Executar com diferentes níveis de verbosidade
```bash
pytest -v              # Verbose
pytest -vv             # Muito verbose
pytest -q              # Quiet
```

## Fixtures Disponíveis

As fixtures estão definidas em `conftest.py` e incluem:

- `mock_ticker_data`: Dados mock de ticker para testes
- `mock_historical_data`: Dados históricos mock
- `mock_dividends_data`: Dados de dividendos mock
- `sample_tickers`: Lista de tickers para testes
- `mock_yfinance`: Mock do yfinance
- `sample_weights_dict`: Dicionário de pesos balanceados
- `sample_unbalanced_weights`: Dicionário de pesos desbalanceados

## Marcadores de Teste

- `@pytest.mark.unit`: Testes unitários
- `@pytest.mark.integration`: Testes de integração
- `@pytest.mark.slow`: Testes que demoram para executar
- `@pytest.mark.external_api`: Testes que fazem chamadas para APIs externas

## Cobertura de Código

O projeto está configurado para gerar relatórios de cobertura:

- **HTML**: `htmlcov/index.html`
- **Terminal**: Exibido após execução dos testes
- **XML**: `coverage.xml` (para CI/CD)

Meta de cobertura: **80%**

## Boas Práticas

1. **Nomenclatura**: Use nomes descritivos para testes (`test_funcao_cenario_resultado`)
2. **Arrange-Act-Assert**: Organize testes com essa estrutura
3. **Mocks**: Use mocks para isolar dependências externas
4. **Fixtures**: Reutilize fixtures para dados comuns
5. **Marcadores**: Use marcadores para categorizar testes
6. **Documentação**: Documente testes complexos

## Executando Testes no CI/CD

```yaml
# Exemplo para GitHub Actions
- name: Run tests
  run: |
    pytest --cov=src/portfolio_optimizer --cov-report=xml --cov-fail-under=80
```

## Adicionando Novos Testes

1. Crie o arquivo de teste no diretório apropriado
2. Importe as classes/funções a serem testadas
3. Use fixtures do `conftest.py` quando possível
4. Adicione marcadores apropriados
5. Mantenha a cobertura acima de 80%