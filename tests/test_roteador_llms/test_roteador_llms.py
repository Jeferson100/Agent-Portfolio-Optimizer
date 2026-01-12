"""Testes para o módulo LlmRouter."""

import pytest
from unittest.mock import Mock, patch, AsyncMock, MagicMock
from pydantic import BaseModel, Field

try:
    from portfolio_optimizer.roteador_llms import LlmRouter, AllProvidersFailedError
except ImportError:
    pytest.skip("Módulo não disponível devido a dependências", allow_module_level=True)


class MockStructuredOutput(BaseModel):
    """Mock de saída estruturada para testes."""
    result: str = Field(description="Resultado da análise")
    confidence: float = Field(description="Nível de confiança")


class TestLlmRouterInit:
    """Testes para inicialização do LlmRouter."""

    def test_init_with_default_models(self):
        """Testa inicialização com modelos padrão."""
        router = LlmRouter("test message")
        
        assert router.messages == "test message"
        assert router.strutured_output is None
        assert "Groq" in router.models
        assert "Cerebras" in router.models
        assert "API_Nvidia" in router.models
        assert "Langchain_nvidia" in router.models
        assert "Openai_nvidia" in router.models
        
        # Verifica que há modelos padrão
        assert len(router.models["Groq"]) > 0
        assert len(router.models["Cerebras"]) > 0
        assert len(router.models["API_Nvidia"]) > 0

    def test_init_with_custom_models(self):
        """Testa inicialização com modelos customizados."""
        custom_groq = ["custom-groq-model"]
        custom_cerebras = ["custom-cerebras-model"]
        custom_api_nvidia = ["custom-api-nvidia-model"]
        custom_langchain_nvidia = ["custom-langchain-nvidia-model"]
        custom_openai_nvidia = ["custom-openai-nvidia-model"]
        
        router = LlmRouter(
            "test message",
            strutured_output=MockStructuredOutput,
            groq_models=custom_groq,
            cerebras_models=custom_cerebras,
            api_nvidia_models=custom_api_nvidia,
            api_langchain_nvidia_models=custom_langchain_nvidia,
            api_openai_nvidia_models=custom_openai_nvidia,
        )
        
        assert router.models["Groq"] == custom_groq
        assert router.models["Cerebras"] == custom_cerebras
        assert router.models["API_Nvidia"] == custom_api_nvidia
        assert router.models["Langchain_nvidia"] == custom_langchain_nvidia
        assert router.models["Openai_nvidia"] == custom_openai_nvidia
        assert router.strutured_output == MockStructuredOutput

    def test_init_with_structured_output(self):
        """Testa inicialização com saída estruturada."""
        router = LlmRouter("test message", strutured_output=MockStructuredOutput)
        
        assert router.strutured_output == MockStructuredOutput


class TestLlmRouterTryProvider:
    """Testes para o método _try_provider."""

    @pytest.mark.asyncio
    async def test_try_provider_success_first_model(self):
        """Testa sucesso no primeiro modelo do provedor."""
        router = LlmRouter("test message")
        
        mock_router_class = Mock()
        mock_instance = Mock()
        mock_method = AsyncMock(return_value="success response")
        mock_instance.test_method = mock_method
        mock_router_class.return_value = mock_instance
        
        result = await router._try_provider("Groq", mock_router_class, "test_method")
        
        assert result == "success response"
        mock_router_class.assert_called_once()
        mock_method.assert_called_once()

    @pytest.mark.asyncio
    async def test_try_provider_success_second_model(self):
        """Testa sucesso no segundo modelo após falha no primeiro."""
        router = LlmRouter("test message", groq_models=["model1", "model2"])
        
        mock_router_class = Mock()
        mock_instance1 = Mock()
        mock_instance2 = Mock()
        mock_method1 = AsyncMock(side_effect=Exception("Model 1 failed"))
        mock_method2 = AsyncMock(return_value="success response")
        mock_instance1.test_method = mock_method1
        mock_instance2.test_method = mock_method2
        
        # Primeira chamada retorna instância que falha, segunda retorna sucesso
        mock_router_class.side_effect = [mock_instance1, mock_instance2]
        
        result = await router._try_provider("Groq", mock_router_class, "test_method")
        
        assert result == "success response"
        assert mock_router_class.call_count == 2

    @pytest.mark.asyncio
    async def test_try_provider_all_models_fail(self):
        """Testa quando todos os modelos do provedor falham."""
        router = LlmRouter("test message", groq_models=["model1", "model2"])
        
        mock_router_class = Mock()
        mock_instance = Mock()
        mock_method = AsyncMock(side_effect=Exception("Model failed"))
        mock_instance.test_method = mock_method
        mock_router_class.return_value = mock_instance
        
        result = await router._try_provider("Groq", mock_router_class, "test_method")
        
        assert result is None
        assert mock_router_class.call_count == 2

    @pytest.mark.asyncio
    async def test_try_provider_returns_none(self):
        """Testa quando o método retorna None."""
        router = LlmRouter("test message", groq_models=["model1"])
        
        mock_router_class = Mock()
        mock_instance = Mock()
        mock_method = AsyncMock(return_value=None)
        mock_instance.test_method = mock_method
        mock_router_class.return_value = mock_instance
        
        result = await router._try_provider("Groq", mock_router_class, "test_method")
        
        assert result is None

    @pytest.mark.asyncio
    async def test_try_provider_sync_method(self):
        """Testa quando o método é síncrono."""
        router = LlmRouter("test message", groq_models=["model1"])
        
        mock_router_class = Mock()
        mock_instance = Mock()
        mock_method = Mock(return_value="sync response")
        mock_instance.test_method = mock_method
        mock_router_class.return_value = mock_instance
        
        result = await router._try_provider("Groq", mock_router_class, "test_method")
        
        assert result == "sync response"


class TestLlmRouterRouting:
    """Testes para o método llm_router."""

    @pytest.mark.asyncio
    async def test_llm_router_success_api_nvidia(self):
        """Testa sucesso com API_Nvidia como primeiro provedor."""
        router = LlmRouter("test message")
        
        with patch.object(router, '_try_provider', new_callable=AsyncMock) as mock_try:
            mock_try.return_value = "api_nvidia response"
            
            result = await router.llm_router()
            
            assert result == "api_nvidia response"
            mock_try.assert_called_once()
            # Verifica que foi chamado com API_Nvidia primeiro
            call_args = mock_try.call_args
            assert call_args[0][0] == "API_Nvidia"

    @pytest.mark.asyncio
    async def test_llm_router_fallback_to_langchain_nvidia(self):
        """Testa fallback para Langchain_nvidia quando API_Nvidia falha."""
        router = LlmRouter("test message")
        
        call_count = 0
        def side_effect(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return None  # API_Nvidia falha
            return "langchain_nvidia response"
        
        with patch.object(router, '_try_provider', new_callable=AsyncMock) as mock_try:
            mock_try.side_effect = side_effect
            
            result = await router.llm_router()
            
            assert result == "langchain_nvidia response"
            assert mock_try.call_count == 2

    @pytest.mark.asyncio
    async def test_llm_router_fallback_to_groq(self):
        """Testa fallback para Groq quando provedores anteriores falham."""
        router = LlmRouter("test message")
        
        call_count = 0
        def side_effect(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count <= 2:
                return None  # API_Nvidia e Langchain_nvidia falham
            return "groq response"
        
        with patch.object(router, '_try_provider', new_callable=AsyncMock) as mock_try:
            mock_try.side_effect = side_effect
            
            result = await router.llm_router()
            
            assert result == "groq response"
            assert mock_try.call_count == 3

    @pytest.mark.asyncio
    async def test_llm_router_fallback_to_cerebras(self):
        """Testa fallback para Cerebras quando provedores anteriores falham."""
        router = LlmRouter("test message")
        
        call_count = 0
        def side_effect(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count <= 3:
                return None  # Provedores anteriores falham
            return "cerebras response"
        
        with patch.object(router, '_try_provider', new_callable=AsyncMock) as mock_try:
            mock_try.side_effect = side_effect
            
            result = await router.llm_router()
            
            assert result == "cerebras response"
            assert mock_try.call_count == 4

    @pytest.mark.asyncio
    async def test_llm_router_fallback_to_openai_nvidia(self):
        """Testa fallback para Openai_nvidia quando provedores anteriores falham."""
        router = LlmRouter("test message")
        
        call_count = 0
        def side_effect(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count <= 4:
                return None  # Provedores anteriores falham
            return "openai_nvidia response"
        
        with patch.object(router, '_try_provider', new_callable=AsyncMock) as mock_try:
            mock_try.side_effect = side_effect
            
            result = await router.llm_router()
            
            assert result == "openai_nvidia response"
            assert mock_try.call_count == 5

    @pytest.mark.asyncio
    async def test_llm_router_all_providers_fail(self):
        """Testa quando todos os provedores falham."""
        router = LlmRouter("test message")
        
        with patch.object(router, '_try_provider', new_callable=AsyncMock) as mock_try:
            mock_try.return_value = None
            
            with pytest.raises(AllProvidersFailedError) as exc_info:
                await router.llm_router()
            
            assert "Falha total" in str(exc_info.value)
            # Deve tentar todos os 5 provedores
            assert mock_try.call_count == 5

    @pytest.mark.asyncio
    async def test_llm_router_provider_exception(self):
        """Testa quando um provedor levanta exceção."""
        router = LlmRouter("test message")
        
        call_count = 0
        def side_effect(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise Exception("Provider error")
            return "success response"
        
        with patch.object(router, '_try_provider', new_callable=AsyncMock) as mock_try:
            mock_try.side_effect = side_effect
            
            result = await router.llm_router()
            
            assert result == "success response"
            assert mock_try.call_count == 2


class TestLlmRouterStructuredOutput:
    """Testes para roteamento com saída estruturada."""

    @pytest.mark.asyncio
    async def test_llm_router_structured_output_api_nvidia(self):
        """Testa roteamento com saída estruturada usando API_Nvidia."""
        router = LlmRouter("test message", strutured_output=MockStructuredOutput)
        
        mock_response = {"result": "test", "confidence": 0.9}
        
        with patch.object(router, '_try_provider', new_callable=AsyncMock) as mock_try:
            mock_try.return_value = mock_response
            
            result = await router.llm_router()
            
            assert result == mock_response
            # Verifica que foi usado método estruturado
            call_args = mock_try.call_args
            # O método deve ser 'ainvoke' para API_Nvidia com structured output
            assert call_args[0][2] == "ainvoke"

    @pytest.mark.asyncio
    async def test_llm_router_structured_output_groq(self):
        """Testa roteamento com saída estruturada usando Groq."""
        router = LlmRouter("test message", strutured_output=MockStructuredOutput)
        
        mock_response = {"result": "test", "confidence": 0.9}
        
        call_count = 0
        def side_effect(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count <= 2:
                return None
            return mock_response
        
        with patch.object(router, '_try_provider', new_callable=AsyncMock) as mock_try:
            mock_try.side_effect = side_effect
            
            result = await router.llm_router()
            
            assert result == mock_response
            # Verifica que foi usado método estruturado do Groq
            groq_call = [call for call in mock_try.call_args_list if call[0][0] == "Groq"][0]
            assert groq_call[0][2] == "llm_structured_groq"

    @pytest.mark.asyncio
    async def test_llm_router_structured_output_cerebras(self):
        """Testa roteamento com saída estruturada usando Cerebras."""
        router = LlmRouter("test message", strutured_output=MockStructuredOutput)
        
        mock_response = MockStructuredOutput(result="test", confidence=0.9)
        
        call_count = 0
        def side_effect(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count <= 3:
                return None
            return mock_response
        
        with patch.object(router, '_try_provider', new_callable=AsyncMock) as mock_try:
            mock_try.side_effect = side_effect
            
            result = await router.llm_router()
            
            assert result == mock_response
            # Verifica que foi usado método estruturado do Cerebras
            cerebras_call = [call for call in mock_try.call_args_list if call[0][0] == "Cerebras"][0]
            assert cerebras_call[0][2] == "get_response_cerebras_structured_async"


class TestLlmRouterNonStructuredOutput:
    """Testes para roteamento sem saída estruturada."""

    @pytest.mark.asyncio
    async def test_llm_router_non_structured_groq(self):
        """Testa roteamento sem saída estruturada usando Groq."""
        router = LlmRouter("test message")
        
        call_count = 0
        def side_effect(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count <= 2:
                return None
            return "groq text response"
        
        with patch.object(router, '_try_provider', new_callable=AsyncMock) as mock_try:
            mock_try.side_effect = side_effect
            
            result = await router.llm_router()
            
            assert result == "groq text response"
            # Verifica que foi usado método não estruturado
            groq_call = [call for call in mock_try.call_args_list if call[0][0] == "Groq"][0]
            assert groq_call[0][2] == "llm_groq"

    @pytest.mark.asyncio
    async def test_llm_router_non_structured_langchain_nvidia(self):
        """Testa roteamento sem saída estruturada usando Langchain_nvidia."""
        router = LlmRouter("test message")
        
        call_count = 0
        def side_effect(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return None
            return "langchain_nvidia text response"
        
        with patch.object(router, '_try_provider', new_callable=AsyncMock) as mock_try:
            mock_try.side_effect = side_effect
            
            result = await router.llm_router()
            
            assert result == "langchain_nvidia text response"
            # Verifica que foi usado método não estruturado
            langchain_call = [call for call in mock_try.call_args_list if call[0][0] == "Langchain_nvidia"][0]
            assert langchain_call[0][2] == "llm_nvidia"


class TestAllProvidersFailedError:
    """Testes para a exceção AllProvidersFailedError."""

    def test_exception_creation(self):
        """Testa criação da exceção."""
        error_msg = "Falha total: {'Provider1': 'Error1', 'Provider2': 'Error2'}"
        exception = AllProvidersFailedError(error_msg)
        
        assert str(exception) == error_msg
        assert isinstance(exception, Exception)

    def test_exception_inheritance(self):
        """Testa que a exceção herda de Exception."""
        exception = AllProvidersFailedError("test")
        
        assert isinstance(exception, Exception)


class TestLlmRouterEdgeCases:
    """Testes para casos extremos do LlmRouter."""

    @pytest.mark.asyncio
    async def test_llm_router_empty_models_list(self):
        """Testa quando uma lista de modelos está vazia."""
        router = LlmRouter("test message", groq_models=[])
        
        # Deve tentar outros provedores
        call_count = 0
        def side_effect(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count <= 2:
                return None
            return "success from cerebras"
        
        with patch.object(router, '_try_provider', new_callable=AsyncMock) as mock_try:
            mock_try.side_effect = side_effect
            
            result = await router.llm_router()
            
            assert result == "success from cerebras"

    @pytest.mark.asyncio
    async def test_llm_router_empty_message(self):
        """Testa com mensagem vazia."""
        router = LlmRouter("")
        
        with patch.object(router, '_try_provider', new_callable=AsyncMock) as mock_try:
            mock_try.return_value = "response"
            
            result = await router.llm_router()
            
            assert result == "response"
            # Verifica que a mensagem vazia foi passada
            assert router.messages == ""

    @pytest.mark.asyncio
    async def test_llm_router_long_message(self):
        """Testa com mensagem muito longa."""
        long_message = "test " * 10000
        router = LlmRouter(long_message)
        
        with patch.object(router, '_try_provider', new_callable=AsyncMock) as mock_try:
            mock_try.return_value = "response"
            
            result = await router.llm_router()
            
            assert result == "response"
            assert len(router.messages) == len(long_message)
