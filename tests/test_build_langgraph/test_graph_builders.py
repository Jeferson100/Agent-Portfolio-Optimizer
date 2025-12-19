"""Testes para os builders de grafo do build_langgraph."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from langgraph.graph import StateGraph


class TestBuildGraphCriadorCarteira:
    """Testes para a classe BuildGraphCriadorCarteira."""

    @patch('portfolio_optimizer.build_langgraph.graph_criador_carteira.StateCarteira')
    def test_init(self, mock_state_carteira):
        """Testa inicialização da classe."""
        from portfolio_optimizer.build_langgraph.graph_criador_carteira import BuildGraphCriadorCarteira
        
        builder = BuildGraphCriadorCarteira()
        
        assert builder is not None
        assert hasattr(builder, 'graph')
        assert isinstance(builder.graph, StateGraph)

    @patch('portfolio_optimizer.build_langgraph.graph_criador_carteira.analista_criador_carteira')
    @patch('portfolio_optimizer.build_langgraph.graph_criador_carteira.verify_weight_sum')
    @patch('portfolio_optimizer.build_langgraph.graph_criador_carteira.verifica_tics_selecionados')
    @patch('portfolio_optimizer.build_langgraph.graph_criador_carteira.analista_avaliador_peso_carteira')
    @patch('portfolio_optimizer.build_langgraph.graph_criador_carteira.should_continue')
    def test_build_method(self, mock_should_continue, mock_analista_avaliador,
                          mock_verifica_tics, mock_verify_weight, mock_analista_criador):
        """Testa o método build."""
        from portfolio_optimizer.build_langgraph.graph_criador_carteira import BuildGraphCriadorCarteira
        
        builder = BuildGraphCriadorCarteira()
        
        # Mock das funções para evitar imports complexos
        mock_analista_criador.__name__ = 'analista_criador_carteira'
        mock_verify_weight.__name__ = 'verify_weight_sum'
        mock_verifica_tics.__name__ = 'verifica_tics_selecionados'
        mock_analista_avaliador.__name__ = 'analista_avaliador_peso_carteira'
        mock_should_continue.__name__ = 'should_continue'
        
        graph = builder.build()
        
        # Verifica se o grafo foi construído
        assert graph is not None
        assert isinstance(graph, StateGraph)
        
        # Verifica se os nós foram adicionados
        expected_nodes = [
            "analista_criador_carteira",
            "verify_weight_sum",
            "verifica_tics_selecionados", 
            "analista_avaliador_peso_carteira"
        ]
        
        for node_name in expected_nodes:
            assert node_name in graph.nodes

    @patch('portfolio_optimizer.build_langgraph.graph_criador_carteira.analista_criador_carteira')
    @patch('portfolio_optimizer.build_langgraph.graph_criador_carteira.verify_weight_sum')
    @patch('portfolio_optimizer.build_langgraph.graph_criador_carteira.verifica_tics_selecionados')
    @patch('portfolio_optimizer.build_langgraph.graph_criador_carteira.analista_avaliador_peso_carteira')
    @patch('portfolio_optimizer.build_langgraph.graph_criador_carteira.should_continue')
    def test_compile_method(self, mock_should_continue, mock_analista_avaliador,
                            mock_verifica_tics, mock_verify_weight, mock_analista_criador):
        """Testa o método compile."""
        from portfolio_optimizer.build_langgraph.graph_criador_carteira import BuildGraphCriadorCarteira
        
        builder = BuildGraphCriadorCarteira()
        
        # Mock das funções
        mock_analista_criador.__name__ = 'analista_criador_carteira'
        mock_verify_weight.__name__ = 'verify_weight_sum'
        mock_verifica_tics.__name__ = 'verifica_tics_selecionados'
        mock_analista_avaliador.__name__ = 'analista_avaliador_peso_carteira'
        mock_should_continue.__name__ = 'should_continue'
        
        compiled_graph = builder.compile()
        
        # Verifica se o grafo foi compilado
        assert compiled_graph is not None
        # Grafo compilado deve ter métodos de execução
        assert hasattr(compiled_graph, 'invoke') or hasattr(compiled_graph, 'stream')

    def test_multiple_instances(self):
        """Testa se múltiplas instâncias são independentes."""
        from portfolio_optimizer.build_langgraph.graph_criador_carteira import BuildGraphCriadorCarteira
        
        builder1 = BuildGraphCriadorCarteira()
        builder2 = BuildGraphCriadorCarteira()
        
        # Cada instância deve ter seu próprio grafo
        assert builder1.graph is not builder2.graph
        assert id(builder1.graph) != id(builder2.graph)


class TestBuildGraphAvaliacaoTics:
    """Testes para a classe BuildGraphAvaliacaoTics."""

    @patch('portfolio_optimizer.build_langgraph.graph_avaliacao_tics.StateClassification')
    def test_init(self, mock_state_classification):
        """Testa inicialização da classe."""
        from portfolio_optimizer.build_langgraph.graph_avaliacao_tics import BuildGraphAvaliacaoTics
        
        builder = BuildGraphAvaliacaoTics()
        
        assert builder is not None
        assert hasattr(builder, 'graph')
        assert isinstance(builder.graph, StateGraph)

    @patch('portfolio_optimizer.build_langgraph.graph_avaliacao_tics.get_data_fundamentalistas')
    @patch('portfolio_optimizer.build_langgraph.graph_avaliacao_tics.analista_fundamentalista')
    @patch('portfolio_optimizer.build_langgraph.graph_avaliacao_tics.avaliador_analista_fundamentalista')
    @patch('portfolio_optimizer.build_langgraph.graph_avaliacao_tics.should_continue')
    def test_build_method(self, mock_should_continue, mock_avaliador,
                          mock_analista, mock_get_data):
        """Testa o método build."""
        from portfolio_optimizer.build_langgraph.graph_avaliacao_tics import BuildGraphAvaliacaoTics
        
        builder = BuildGraphAvaliacaoTics()
        
        # Mock das funções
        mock_get_data.__name__ = 'get_data_fundamentalistas'
        mock_analista.__name__ = 'analista_fundamentalista'
        mock_avaliador.__name__ = 'avaliador_analista_fundamentalista'
        mock_should_continue.__name__ = 'should_continue'
        
        graph = builder.build()
        
        # Verifica se o grafo foi construído
        assert graph is not None
        assert isinstance(graph, StateGraph)
        
        # Verifica se os nós foram adicionados
        expected_nodes = [
            "coleta_fundamentalistas",
            "analise_fundamentalista",
            "avaliacao_analise"
        ]
        
        for node_name in expected_nodes:
            assert node_name in graph.nodes

    @patch('portfolio_optimizer.build_langgraph.graph_avaliacao_tics.get_data_fundamentalistas')
    @patch('portfolio_optimizer.build_langgraph.graph_avaliacao_tics.analista_fundamentalista')
    @patch('portfolio_optimizer.build_langgraph.graph_avaliacao_tics.avaliador_analista_fundamentalista')
    @patch('portfolio_optimizer.build_langgraph.graph_avaliacao_tics.should_continue')
    def test_compile_method(self, mock_should_continue, mock_avaliador,
                            mock_analista, mock_get_data):
        """Testa o método compile."""
        from portfolio_optimizer.build_langgraph.graph_avaliacao_tics import BuildGraphAvaliacaoTics
        
        builder = BuildGraphAvaliacaoTics()
        
        # Mock das funções
        mock_get_data.__name__ = 'get_data_fundamentalistas'
        mock_analista.__name__ = 'analista_fundamentalista'
        mock_avaliador.__name__ = 'avaliador_analista_fundamentalista'
        mock_should_continue.__name__ = 'should_continue'
        
        compiled_graph = builder.compile()
        
        # Verifica se o grafo foi compilado
        assert compiled_graph is not None
        assert hasattr(compiled_graph, 'invoke') or hasattr(compiled_graph, 'stream')

    def test_builder_has_required_methods(self):
        """Testa se o builder tem os métodos necessários."""
        from portfolio_optimizer.build_langgraph.graph_avaliacao_tics import BuildGraphAvaliacaoTics
        
        builder = BuildGraphAvaliacaoTics()
        
        assert hasattr(builder, 'build')
        assert hasattr(builder, 'compile')
        assert callable(builder.build)
        assert callable(builder.compile)