from caster.models.caster_output import CasterOutput
from pydantic import Field
from typing import Annotated
from caster.prompts import casting_agent_system_prompt
from campus.campus_agent import Campus
from agno.run.agent import RunOutput
from agno.agent import Agent
from functools import wraps


class CasterAgent(Agent):

    campus: Campus

    global_task: str

    @wraps(Agent.__init__)
    def __init__(self, campus: Campus, global_task: str, **kwargs):
        super().__init__(**kwargs)

        self.campus = campus
        self.global_task = global_task
        self.output_model = CasterOutput

    def update_system_message(self):
        experts = self.campus.get_expert_descriptions()

        expert_repr = "\n".join(f"{e[0]}: {e[1]}" for e in experts)

        self.system_message = casting_agent_system_prompt.format(
            "available_experts", expert_repr
        )

    @wraps(Agent.run)
    def run(self, *args, **kwargs) -> RunOutput:
        self.update_system_message()

        return super().run(*args, **kwargs)
