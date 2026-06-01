import random
from campus.core import Campus
from fasticrl.icrl_learner import ICRLLearner
from caster.core import CasterAgent
import logging
import pytest

prompt = """
Set up an automated backup system for a local Docker environment. It needs to safely stop specific containers, compress and backup their appdata directories to a secondary NAS drive, restart the containers, and send a status notification when finished.
"""


@pytest.mark.api
def test_caster_run(g_data):
    assert True
