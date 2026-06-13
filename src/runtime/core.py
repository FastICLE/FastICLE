import logging
import os

from agno.agent import Agent
from agno.models.base import Model
from agno.models.openai import OpenAIResponses
from agno.run.agent import RunOutput
from agno.team import Team, TeamMode
from agno.workflow import StepInput, StepOutput
from dotenv import load_dotenv
from pydantic import BaseModel

from campus.models.expert_config import ExpertConfig
from models.tasks import CasterTask, CasterTaskList, RuntimeTask, RuntimeTaskList

LOGGER = logging.getLogger(__name__)


class Runtime(BaseModel):

    expert_save_dir: str
    model: Model

    def runtime(self, step_input: StepInput) -> StepOutput:
        runtime_task_list: RuntimeTaskList = RuntimeTaskList()

        caster_task_list: CasterTaskList = step_input.get_last_step_content()

        for task in caster_task_list.task_list:
            LOGGER.info(f"Running task ({task.agent_ids}): {task.description[:10]}...")
            runtime_task_list.task_list.append(self._run_task(task))

        return StepOutput(content=runtime_task_list)

    def _run_task(self, caster_task: CasterTask):
        load_dotenv()
        path: str = self.expert_save_dir
        experts: list[Agent] = []

        for agent_id in caster_task.agent_ids:
            expert: Agent = ExpertConfig.from_yaml(
                path + "/" + agent_id + ".yaml"
            ).to_agent()
            experts.append(expert)

        team: Team = Team(members=experts, model=self.model)

        expert_out: RunOutput = team.run(caster_task.description)

        return RuntimeTask(**caster_task.model_dump(), task_output=expert_out.content)
