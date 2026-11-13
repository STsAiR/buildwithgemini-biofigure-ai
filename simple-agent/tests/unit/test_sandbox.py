"""Unit test for AgentEngineSandboxCodeExecutor configuration and execution."""

from app.agent import SANDBOX_RESOURCE_NAME, root_agent
from google.adk.code_executors.agent_engine_sandbox_code_executor import AgentEngineSandboxCodeExecutor
from google.adk.code_executors.code_execution_utils import CodeExecutionInput


def test_agent_code_executor_configured() -> None:
    assert root_agent.code_executor is not None
    assert isinstance(root_agent.code_executor, AgentEngineSandboxCodeExecutor)
    assert root_agent.code_executor.sandbox_resource_name == SANDBOX_RESOURCE_NAME


def test_sandbox_code_execution() -> None:
    executor = AgentEngineSandboxCodeExecutor(sandbox_resource_name=SANDBOX_RESOURCE_NAME)
    result = executor.execute_code(
        invocation_context=None,
        code_execution_input=CodeExecutionInput(code="result = 12 * 12\nprint(f'Computed: {result}')")
    )
    assert result is not None
    assert "Computed: 144" in result.stdout
