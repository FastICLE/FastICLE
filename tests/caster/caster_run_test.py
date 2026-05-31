import random
from campus.campus_agent import Campus
from fasticrl.icrl_learner import ICRLLearner
from caster.caster import CasterAgent
import logging
import pytest

LOGGER = logging.getLogger(__name__)

prompt = """
Set up an automated backup system for a local Docker environment. It needs to safely stop specific containers, compress and backup their appdata directories to a secondary NAS drive, restart the containers, and send a status notification when finished.
"""


def reward_func(model_output: str, task: str) -> int:
    return random.randrange(0, 10)


@pytest.mark.api
def test_caster_run(g_data):
    
    caster: CasterAgent = CasterAgent(
        campus=Campus(
            model=g_data["model"],
            learner=ICRLLearner(
                agent=g_data["model"],
                reward_func=reward_func,
                task_description="Write nice short poems about the nature.",
                tasks=[
                    "Write a poem about flowers.",
                    "Write a poem about rivers.",
                    "Write a poem about mountains."
                ],
                buffer=[]
            ),
        )
    )
