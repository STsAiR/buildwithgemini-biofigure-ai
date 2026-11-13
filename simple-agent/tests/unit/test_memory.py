"""Unit test for Memory Bank wiring in root_agent and services."""

from app.agent import root_agent
from app.app_utils import services
from google.adk.memory import VertexAiMemoryBankService
from google.adk.tools.preload_memory_tool import PreloadMemoryTool


def test_agent_memory_tool_and_callback_configured() -> None:
    has_preload_memory = any(isinstance(tool, PreloadMemoryTool) for tool in root_agent.tools)
    assert has_preload_memory, "PreloadMemoryTool must be present in root_agent.tools"
    assert root_agent.after_agent_callback is not None, "after_agent_callback must be configured for memory extraction"


def test_memory_service_builder() -> None:
    service = services.get_memory_service()
    assert service is not None
    assert isinstance(service, VertexAiMemoryBankService)
    assert service._agent_engine_id == services.MEMORY_BANK_ID
    assert service._project == "qwiklabs-gcp-04-e67897557cd7"
