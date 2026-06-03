from __future__ import annotations

import pytest

from qapitol.evals.llm.wrapper import LLM
from qapitol.evals.testing import MockCompletionClient


@pytest.fixture
def mock_llm() -> LLM:
    return LLM(provider="openai", model="test", client=MockCompletionClient())
