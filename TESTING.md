# Guia de Testes - Agent Portfolio Optimizer

Este documento descreve como executar e contribuir com testes no projeto Agent Portfolio Optimizer.

## Estrutura de Testes

```
tests/
├── conftest.py                    # Configurações e fixtures compartilhadas
├── test_coleta_dados/            # Testes para módulos de coleta de dados
├── test_integration/             # Testes de integração
├── test_state_outputs/           # Testes para estados e outputs
├── test_tratando_dados/          # Testes para tratamento de dados
└── test_utils/                   # Testes para utilitários
```

## Executando Testes

### Métodos Disponíveis

1. **Usando o script Python (Recomendado)**:
   ```bash
   python scripts/run_tests.py --all
   ```

2. **Usando Make**:
   ```bash
   make test_all
   ```

3. **Usando pytest diretamente**:
   ```bash
   uv run pytest
   ```

### Opções de Execução

```bash
# Todos os testes com cobertura e linting
python scripts/run_tests.py --all

# Apenas testes unitários
python scripts/run_tests.py --unit

# Apenas testes de integração
python scripts/run_tests.py --integration

# Testes rápidos (exclui testes marcados como 'slow')
python scripts/run_tests.py --fast

# Testes com relatório de cobertura
python scripts/run_tests.py --coverage

# Apenas linting
python scripts/run_tests.py --lint

# Apenas verificação de tipos
python scripts/run_tests.py --type-check
```

### Usando Makefile

```bash
make test              # Executa testes básicos
make test_coverage     # Testes com cobertura
make test_unit         # Apenas testes unitários
make test_integration  # Apenas testes de integração
make test_fast         # Testes rápidos
make test_all          # Todos os checks
```

## Marcadores de Teste

Use marcadores para categorizar seus testes:

```python
import pytest

@pytest.mark.unit
def test_funcao_simples():
    """Teste unitário básico."""
    pass

@pytest.mark.integration
def test_workflow_completo():
    """Teste de integração."""
    pass

@pytest.mark.slow
def test_operacao_demorada():
    """Teste que demora para executar."""
    pass

@pytest.mark.external_api
def test_chamada_api_externa():
    """Teste que faz chamadas para APIs externas."""
    pass
```

## Fixtures Disponíveis

### Fixtures de Dados Mock

```python
def test_exemplo(mock_ticker_data, mock_historical_data):
    """Exemplo usando fixtures de dados mock."""
    assert mock_ticker_data['symbol'] == 'PETR4.SA'
    assert len(mock_historical_data) == 100
```

### Fixtures de Mock de APIs

```python
def test_exemplo_com_mock_yfinance(mock_yfinance):
    """Exemplo usando mock do yfinance."""
    mock_yfinance.info = {'symbol': 'PETR4.SA'}
    # Seu teste aqui
```

## Escrevendo Novos Testes

### Estrutura Recomendada

```python
"""Testes para o módulo ExemploModulo."""

import pytest
from unittest.mock import Mock, patch
from portfolio_optimizer.modulo import ExemploClasse


class TestExemploClasse:
    """Testes para a classe ExemploClasse."""

    def test_metodo_sucesso(self):
        """Testa execução bem-sucedida do método."""
        # Arrange
        instancia = ExemploClasse("parametro")
        
        # Act
        resultado = instancia.metodo()
        
        # Assert
        assert resultado == "esperado"

    @patch('portfolio_optimizer.modulo.dependencia_externa')
    def test_metodo_com_mock(self, mock_dependencia):
        """Testa método com dependência externa mockada."""
        # Arrange
        mock_dependencia.return_value = "valor_mock"
        instancia = ExemploClasse("parametro")
        
        # Act
        resultado = instancia.metodo_com_dependencia()
        
        # Assert
        assert resultado == "valor_processado"
        mock_dependencia.assert_called_once()

    def test_metodo_erro(self):
        """Testa tratamento de erro."""
        # Arrange
        instancia = ExemploClasse("parametro_invalido")
        
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            instancia.metodo_que_falha()
        
        assert "mensagem esperada" in str(exc_info.value)
```

### Boas Práticas

1. **Nomenclatura**: Use nomes descritivos (`test_funcao_cenario_resultado`)
2. **Arrange-Act-Assert**: Organize testes com essa estrutura
3. **Mocks**: Use mocks para isolar dependências externas
4. **Fixtures**: Reutilize fixtures para dados comuns
5. **Documentação**: Documente testes complexos
6. **Cobertura**: Mantenha cobertura acima de 70%

### Testando Funções Assíncronas

```python
import pytest

@pytest.mark.asyncio
async def test_funcao_async():
    """Testa função assíncrona."""
    resultado = await funcao_async()
    assert resultado == "esperado"
```

### Testando com Dados Parametrizados

```python
@pytest.mark.parametrize("entrada,esperado", [
    ("PETR4.SA", True),
    ("INVALID.SA", False),
    ("", False),
])
def test_validacao_ticker(entrada, esperado):
    """Testa validação de ticker com múltiplos valores."""
    resultado = validar_ticker(entrada)
    assert resultado == esperado
```

## Cobertura de Código

### Visualizando Relatórios

Após executar testes com cobertura:

```bash
# Relatório no terminal
python scripts/run_tests.py --coverage

# Relatório HTML (abra htmlcov/index.html no navegador)
open htmlcov/index.html
```

### Meta de Cobertura

- **Mínimo**: 70%
- **Recomendado**: 80%+
- **Ideal**: 90%+

## Integração Contínua

### GitHub Actions

O projeto usa GitHub Actions para executar testes automaticamente:

- **Push/PR**: Executa linting, type checking e testes
- **Cobertura**: Envia relatórios para Codecov
- **Múltiplas versões**: Testa com Python 3.12

### Pre-commit Hooks

Configure hooks para executar antes de commits:

```bash
pip install pre-commit
pre-commit install
```

## Debugging de Testes

### Executar com Debug

```bash
# Com breakpoints
uv run pytest --pdb

# Verbose com output
uv run pytest -v -s

# Apenas testes que falharam
uv run pytest --lf
```

### Logs Durante Testes

```python
import logging

def test_com_logs(caplog):
    """Testa captura de logs."""
    with caplog.at_level(logging.INFO):
        funcao_que_loga()
    
    assert "mensagem esperada" in caplog.text
```

## Troubleshooting

### Problemas Comuns

1. **Imports falhando**: Verifique se está executando do diretório raiz
2. **Mocks não funcionando**: Verifique o caminho do patch
3. **Fixtures não encontradas**: Verifique se estão em `conftest.py`
4. **Testes lentos**: Use marcador `@pytest.mark.slow`

### Performance

```bash
# Identificar testes mais lentos
uv run pytest --durations=10

# Executar em paralelo
uv run pytest -n auto
```

## Contribuindo

1. Escreva testes para novas funcionalidades
2. Mantenha cobertura acima de 70%
3. Use fixtures existentes quando possível
4. Documente testes complexos
5. Execute todos os checks antes de fazer commit

```bash
# Antes de fazer commit
python scripts/run_tests.py --all
```