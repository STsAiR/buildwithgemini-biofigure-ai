"""Unit tests for A2UI configuration and callback wiring."""

from app.agent import root_agent
from app.a2ui_utils import a2ui_callback


def test_a2ui_callback_wired() -> None:
    assert root_agent.after_model_callback is not None
    assert root_agent.after_model_callback == a2ui_callback


def test_a2ui_instruction_has_schema() -> None:
    assert "beginRendering" in root_agent.instruction
    assert "surfaceUpdate" in root_agent.instruction
