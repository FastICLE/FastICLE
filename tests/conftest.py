from _pytest.mark import MarkDecorator
import os

from agno.models.base import Model
from agno.models.openai import OpenAIResponses
from dotenv import load_dotenv
import pytest


@pytest.fixture(scope="session")
def mock_model() -> Model:
    """Lightweight model fixture for unit tests — no real API key required."""
    return OpenAIResponses(id="gpt-4.1-mini", api_key="test-key-unit-tests-only")


@pytest.fixture
def g_data() -> dict:
    return {"model": __get_model(provider_key=os.getenv("PROVIDER_KEY", "OPENAI"))}


def pytest_addoption(parser):
    parser.addoption(
        "--run-api",
        action="store_true",
        default=False,
        help="Runs tests, which require API usage",
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "api: marks tests, which require API usage")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--run-api"):
        return

    skip_api: MarkDecorator = pytest.mark.skip(reason="Needs '--run-api' flag.")
    for item in items:
        if "api" in item.keywords:
            item.add_marker(skip_api)


def __get_model(provider_key: str) -> Model:
    load_dotenv()

    api_key = os.getenv(f"{provider_key}_TEST_API_KEY")

    assert api_key

    match provider_key:
        case "OPENAI":
            return OpenAIResponses(id="gpt-4.1-mini", api_key=api_key)

        case _:
            raise NotImplementedError(f"Provider {provider_key} not supported (yet)!")
