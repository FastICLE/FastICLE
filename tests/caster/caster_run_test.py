import logging
import random

import pytest
from fasticrl.icrl_learner import ICRLLearner

from campus.core import Campus
from caster.core import CasterAgent

LOGGER = logging.getLogger(__name__)
import pytest

prompt = """
Set up an automated backup system for a local Docker environment. It needs to safely stop specific containers, compress and backup their appdata directories to a secondary NAS drive, restart the containers, and send a status notification when finished.
"""


@pytest.mark.api
def test_caster_run(g_data):
    campus = Campus(
        global_task="Write poems.",
        save_path="./tests/data/dummy_experts",
        model=g_data["model"],
    )

    caster = CasterAgent(
        model=g_data["model"], global_task="Write poetic poems.", campus=campus
    )

    caster.update_system_message()

    LOGGER.info(caster.system_message)

    LOGGER.info(caster.run("Hallo, was sind die Experten"))
    LOGGER.info("Hallo")
