"""Testes para o módulo LlmRouter."""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from pydantic import BaseModel
from portfolio_optimizer.roteador_llms.roteador_llms import LlmRouter, AllProvidersFailedError


class MockStructuredOutput(BaseModel):
    """Mock de saída estruturada para testes."""
    result: str
    confidence: float


class TestLlmRouter:
    """Testes para a classe LlmRouter."""

    def test_init_default_models(self):
        """Testa inicialização com modelos padrão."""
        router = LlmRouter("test message")
        
        assert router.messages == "test message"
        assert router.strutured_output is None
        assert len(router.groq_models) > 0
        assert len(router.huggingface_models) > 0
        assert len(router.nvidia_models) > 0
        assert len(router.cerebras_models) > 0
        assert "moonshotai/kimi-k2-instruct-0905" in router.groq_models

    def test_init_custom_models(self):
        """Testa inicialização com modelos customizados."""
        custom_groq = ["custom-groq-model"]
        custom_hf = ["custom-hf-model"]
        custom_nvidia = ["custom-nvidia-model"]
        custom_cerebras = ["custom-cerebras-model"]
        structured_output = MockStructuredOutput(result="test", confidence=0.9)
        
        router = LlmRouter(
            "test message",
            strutured_output=structured_output,
            groq_models=custom_groq,
            huggingface_models=custom_hf,
            nvidia_models=custom_nvidia,
            cerebras_models=custom_cerebras
        )
        
        assert router.groq_models == custom_groq
        assert router.huggingface_models == custom_hf
        assert router.nvidia_models == custom_nvidia
        assert router.cerebras_models == custom_cerebras
        assert router.strutured_output == structured_output

    @pytest.mark.asyncio
    @patch('portfolio_optimizer.roteador_llms.roteador_llms.RouterGroq')
    async def test_try_groq_models_success(self, mock_router_groq):
        """Testa sucesso com modelos Groq."""
        mock_instance = Mock()
        mock_instance.llm_groq = AsyncMock(return_value="groq response")
        mock_router_groq.return_value = mock_instance
        
        router = LlmRouter("test message", groq_models=["test-model"])
        
        result = await router.try_groq_models()
        
        assert result == "groq response"
        mock_router_groq.assert_called_once()

    @pytest.mark.asyncio
    @patch('portfolio_optimizer.roteador_llms.roteador_llms.RouterGroq')
    async def test_try_groq_models_structured_success(self, mock_router_groq):
        """Testa sucesso com modelos Groq estruturados."""
        mock_instance = Mock()
        mock_structured_response = {"result": "test", "confidence": 0.9}
        mock_instance.llm_structured_groq = AsyncMock(return_value=mock_structured_response)
        mock_router_groq.return_value = mock_instance
        
        structured_output = MockStructuredOutput(result="test", confidence=0.9)
        router = LlmRouter("test message", strutured_output=structured_output, groq_models=["test-model"])
        
        result = await router.try_groq_models()
        
        assert result == mock_structured_response
        mock_instance.llm_structured_groq.assert_called_once()

    @pytest.mark.asyncio
    @patch('portfolio_optimizer.roteador_llms.roteador_llms.RouterGroq')
    async def test_try_groq_models_failure(self, mock_router_groq):
        """Testa falha com todos os modelos Groq."""
        mock_instance = Mock()
        mock_instance.llm_groq = AsyncMock(side_effect=ConnectionError("Connection failed"))
        mock_router_groq.return_value = mock_instance
        
        router = LlmRouter("test message", groq_models=["test-model"])
        
        result = await router.try_groq_models()
        
        assert result is None

    @pytest.mark.asyncio
    @patch('portfolio_optimizer.roteador_llms.roteador_llms.RouterNvidia')
    async def test_try_nvidia_models_success(self, mock_router_nvidia):
        """Testa sucesso com modelos Nvidia."""
        mock_instance = Mock()
        mock_instance.llm_nvidia = AsyncMock(return_value="nvidia response")
        mock_router_nvidia.return_value = mock_instance
        
        router = LlmRouter("test message", nvidia_models=["test-model"])
        
        result = await router.try_nvidia_models()
        
        assert result == "nvidia response"

    @pytest.mark.asyncio
    @patch('portfolio_optimizer.roteador_llms.roteador_llms.RouterCerebras')
    async def test_try_cerebras_models_success(self, mock_router_cerebras):
        """Testa sucesso com modelos Cerebras."""
        mock_instance = Mock()
        mock_instance.get_response_cerebras_async = AsyncMock(return_value="cerebras response")
        mock_router_cerebras.return_value = mock_instance
        
        router = LlmRouter("test message", cerebras_models=["test-model"])
        
        result = await router.try_cerebras_models()
        
        assert result == "cerebras response"

    @pytest.mark.asyncio
    @patch('portfolio_optimizer.roteador_llms.roteador_llms.RouterPydanticAI')
    async def test_try_huggingface_models_success(self, mock_router_hf):
        """Testa sucesso com modelos HuggingFace."""
        mock_instance = Mock()
        mock_instance.llm_pydanticai = AsyncMock(return_value="huggingface response")
        mock_router_hf.return_value = mock_instance
        
        router = LlmRouter("test message", huggingface_models=["test-model"])
        
        result = await router.try_huggingface_models()
        
        assert result == "huggingface response"

    @pytest.mark.asyncio
    async def test_llm_router_success_first_provider(self):
        """Testa roteamento com sucesso no primeiro provedor."""
        router = LlmRouter("test message")
        
        with patch.object(router, 'try_nvidia_models', new_callable=AsyncMock) as mock_nvidia:
            mock_nvidia.return_value = "nvidia success"
            
            result = await router.llm_router()
            
            assert result == "nvidia success"
            mock_nvidia.assert_called_once()

    @pytest.mark.asyncio
    async def test_llm_router_fallback_to_second_provider(self):
        """Testa fallback para segundo provedor."""
        router = LlmRouter("test message")
        
        with patch.object(router, 'try_nvidia_models', new_callable=AsyncMock) as mock_nvidia, \
             patch.object(router, 'try_cerebras_models', new_callable=AsyncMock) as mock_cerebras:
            
            mock_nvidia.return_value = None
            mock_cerebras.return_value = "cerebras success"
            
            result = await router.llm_router()
            
            assert result == "cerebras success"
            mock_nvidia.assert_called_once()
            mock_cerebras.assert_called_once()

    @pytest.mark.asyncio
    async def test_llm_router_all_providers_fail(self):
        """Testa falha de todos os provedores."""
        router = LlmRouter("test message")
        
        with patch.object(router, 'try_nvidia_models', new_callable=AsyncMock) as mock_nvidia, \
             patch.object(router, 'try_cerebras_models', new_callable=AsyncMock) as mock_cerebras, \
             patch.object(router, 'try_groq_models', new_callable=AsyncMock) as mock_groq, \
             patch.object(router, 'try_huggingface_models', new_callable=AsyncMock) as mock_hf:
            
            mock_nvidia.return_value = None
            mock_cerebras.return_value = None
            mock_groq.return_value = None
            mock_hf.return_value = None
            
            with pytest.raises(AllProvidersFailedError) as exc_info:
                await router.llm_router()
            
            assert "Todos os provedores falharam" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_llm_router_exception_handling(self):
        """Testa tratamento de exceções no roteamento."""
        router = LlmRouter("test message")
        
        with patch.object(router, 'try_nvidia_models', new_callable=AsyncMock) as mock_nvidia, \
             patch.object(router, 'try_cerebras_models', new_callable=AsyncMock) as mock_cerebras:
            
            mock_nvidia.side_effect = Exception("Nvidia error")
            mock_cerebras.return_value = "cerebras success"
            
            result = await router.llm_router()
            
            assert result == "cerebras success"


class TestAllProvidersFailedError:
    """Testes para a exceção AllProvidersFailedError."""

    def test_exception_creation(self):
        """Testa criação da exceção."""
        error_msg = "Test error message"
        exception = AllProvidersFailedError(error_msg)
        
        assert str(exception) == error_msg
        assert isinstance(exception, Exception)