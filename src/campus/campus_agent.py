from dotenv import load_dotenv
from agno.models.openai import OpenAIResponses
from agno.run.agent import RunOutput
from campus.prompts import campus_agent_system_prompt
from campus.models.training_task_list import TrainingTaskList
from agno.agent import Agent
from pathlib import Path
from pydantic import SkipValidation
from pydantic import ConfigDict
from agno.models.base import Model
from typing import Annotated

from pydantic import BaseModel, Field

from campus.models.agent_config import AgentConfig
from fasticrl.icrl_learner import ICRLLearner

from loguru import logger


class Campus(BaseModel):

    model_config: ConfigDict = ConfigDict(arbitrary_types_allowed=True)

    global_task: Annotated[str, Field()]

    save_path: Annotated[str, Field(default="~")]
    auto_save: Annotated[bool, Field(default=True)]
    agent_configs: Annotated[list[AgentConfig], Field(default_factory=list)]

    model: Model

    learner: Annotated[ICRLLearner, SkipValidation()]

    def get_expert_descriptions(self) -> list[tuple[str, str]]:
        for yaml_file in Path(self.save_path).glob("*.yaml"):
            pass

    def train_new_expert(self, expert_task: str) -> None:
        # Build training tasks (API call)

        logger.debug(f"Building synthetic tasks for {expert_task}...")
        
        task_agent = Agent(
            model=self.model,
            output_schema=TrainingTaskList,
            system_message=campus_agent_system_prompt
        )

        run_output: RunOutput = task_agent.run(f"""Global task: {self.global_task}
                       
                       Expert task: {expert_task}""")

        task_list: TrainingTaskList = TrainingTaskList.model_validate(
            run_output.content
        )

        
        for t in task_list.tasks:
            print(t)

        # Build reward func (prompt)

        # Train new expert
        logger.debug(f"Start training")

        # Save expert

        pass


if __name__ == "__main__":
    import os

    load_dotenv()

    icrl = ICRLLearner()

    campus = Campus(
        global_task="Write poems.",
        learner=icrl,
        model=OpenAIResponses(
            id="gpt-4.1-mini", api_key=os.getenv(f"OPENAI_TEST_API_KEY")
        ),
    )

    campus.train_new_expert("Poems about the nature.")
