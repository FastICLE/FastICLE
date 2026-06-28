
import pytest
from agno.models.base import Model


@pytest.mark.api
def test_model(g_data):
    model: Model = g_data["model"]
    
    assert model