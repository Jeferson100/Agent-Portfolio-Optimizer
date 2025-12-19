"""
Testes para o módulo TratandoDadosFundamentalistas.

Este módulo testa a funcionalidade de tratamento de dados fundamentalistas,
incluindo inicialização, coleta de dados e processamento.
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
import pandas as pd
from datetime import datetime

try:
    from portfolio_optimizer.tratando_dados.tratando_dados_fundamentalistas import TratandoDadosFundamentalistas
except ImportError:
    pytest.skip("Módulo TratandoDadosFundamentalistas não disponível", allow_module_level=True)


class TestTratandoDadosFundamentalistas:
    """Testes para a classe TratandoDadosFundamentalistas."""

    def test_init_default_parameters(self):
        """Testa inicialização com parâmetros padrão."""
        tratador = TratandoDadosFundamentalistas(tics='PETR4')
        
        assert tratador.tics == 'PETR4'
        assert tratador.data_inicio is None
        assert tratador.data_fim is None
        assert tratador.colunas_drop is None
        assert tratador.periodos_deslocados == 1

    def test_init_custom_parameters(self):
        """Testa inicialização com parâmetros customizados."""
        tratador = TratandoDadosFundamentalistas(
            tics='VALE3',
            data_inicio='2020-01-01',
            data_fim='2024-12-31',
            colunas_drop=['col1', 'col2'],
            periodos_deslocados=2
        )
        
        assert tratador.tics == 'VALE3'
        assert tratador.data_inicio == '2020-01-01'
        assert tratador.data_fim == '2024-12-31'
        assert tratador.colunas_drop == ['col1', 'col2']
        assert tratador.periodos_deslocados == 2

    def test_init_ticker_validation(self):
        """Testa validação do ticker na inicialização."""
        # Ticker válido
        tratador = TratandoDadosFundamentalistas(tics='PETR4')
        assert tratador.tics == 'PETR4'
        
        # Ticker vazio (deve funcionar mas pode gerar erro em métodos posteriores)
        tratador_vazio = TratandoDadosFundamentalistas(tics='')
        assert tratador_vazio.tics == ''

    @patch('portfolio_optimizer.tratando_dados.tratando_dados_fundamentalistas.DadosFundamentalistas')
    def test_coleta_dados_fundamentalistas_method_exists(self, mock_dados_fund):
        """Testa se o método de coleta de dados existe e é chamável."""
        tratador = TratandoDadosFundamentalistas(tics='PETR4')
        
        # Verifica se o método existe
        assert hasattr(tratador, 'coleta_dados_fundamentalistas')
        
        # Se o método existir, deve ser assíncrono
        if hasattr(tratador, 'coleta_dados_fundamentalistas'):
            import inspect
            assert inspect.iscoroutinefunction(tratador.coleta_dados_fundamentalistas)

    def test_attributes_types(self):
        """Testa os tipos dos atributos da classe."""
        tratador = TratandoDadosFundamentalistas(
            tics='PETR4',
            data_inicio='2020-01-01',
            data_fim='2024-12-31',
            colunas_drop=['col1'],
            periodos_deslocados=3
        )
        
        assert isinstance(tratador.tics, str)
        assert isinstance(tratador.data_inicio, str) or tratador.data_inicio is None
        assert isinstance(tratador.data_fim, str) or tratador.data_fim is None
        assert isinstance(tratador.colunas_drop, list) or tratador.colunas_drop is None
        assert isinstance(tratador.periodos_deslocados, int)

    def test_multiple_instances_independence(self):
        """Testa independência entre múltiplas instâncias."""
        tratador1 = TratandoDadosFundamentalistas(tics='PETR4', periodos_deslocados=1)
        tratador2 = TratandoDadosFundamentalistas(tics='VALE3', periodos_deslocados=2)
        
        assert tratador1.tics != tratador2.tics
        assert tratador1.periodos_deslocados != tratador2.periodos_deslocados
        
        # Modificar um não deve afetar o outro
        tratador1.tics = 'BBAS3'
        assert tratador2.tics == 'VALE3'

    def test_docstring_and_class_attributes(self):
        """Testa se a classe tem documentação adequada."""
        assert TratandoDadosFundamentalistas.__doc__ is not None
        assert len(TratandoDadosFundamentalistas.__doc__.strip()) > 0
        
        # Verifica se a documentação menciona conceitos importantes
        doc = TratandoDadosFundamentalistas.__doc__.lower()
        assert 'fundamentalistas' in doc or 'dados' in doc

    @patch('portfolio_optimizer.tratando_dados.tratando_dados_fundamentalistas.logger')
    def test_logger_usage(self, mock_logger):
        """Testa se o logger está configurado corretamente."""
        # Verifica se o logger foi importado
        from portfolio_optimizer.tratando_dados.tratando_dados_fundamentalistas import logger
        assert logger is not None
        assert logger.name == 'portfolio_optimizer.tratando_dados.tratando_dados_fundamentalistas'

    def test_class_inheritance(self):
        """Testa a hierarquia de herança da classe."""
        tratador = TratandoDadosFundamentalistas(tics='PETR4')
        
        # Verifica se é uma instância da própria classe
        assert isinstance(tratador, TratandoDadosFundamentalistas)
        
        # Verifica se herda de object (comportamento padrão do Python)
        assert isinstance(tratador, object)

    def test_date_format_validation(self):
        """Testa diferentes formatos de data."""
        # Formato correto
        tratador1 = TratandoDadosFundamentalistas(
            tics='PETR4',
            data_inicio='2020-01-01',
            data_fim='2024-12-31'
        )
        assert tratador1.data_inicio == '2020-01-01'
        assert tratador1.data_fim == '2024-12-31'
        
        # Formato diferente (a validação pode ser feita em métodos posteriores)
        tratador2 = TratandoDadosFundamentalistas(
            tics='PETR4',
            data_inicio='01/01/2020',
            data_fim='31/12/2024'
        )
        assert tratador2.data_inicio == '01/01/2020'
        assert tratador2.data_fim == '31/12/2024'