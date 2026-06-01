from pathlib import Path
from typing import Annotated

from agno.agent import Agent
from agno.models.base import Model
from agno.models.openai import OpenAIResponses
from agno.run.agent import RunOutput
from dotenv import load_dotenv
from fasticrl.icrl_learner import ICRLLearner
from loguru import logger
from pydantic import BaseModel, ConfigDict, Field, SkipValidation

from campus.models.expert_config import ExpertConfig
from campus.models.reward_output import RewardOutput
from campus.models.training_task_list import TrainingTaskList
from campus.prompts import (
    campus_agent_system_prompt,
    icrl_agent_system_prompt,
    reward_agent_system_prompt,
)
from loguru import logger



class Campus(BaseModel):

    model_config: ConfigDict = ConfigDict(arbitrary_types_allowed=True)

    global_task: Annotated[str, Field()]

    save_path: Annotated[str, Field(default="~")]
    auto_save: Annotated[bool, Field(default=True)]
    agent_configs: Annotated[list[ExpertConfig], Field(default_factory=list)]

    model: Model
    
    def get_experts(self) -> list[ExpertConfig]:
        expert_configs: list[ExpertConfig] = list()
        
        for yaml_file in Path(self.save_path).glob("*.yaml"):
            try:
                expert_config: ExpertConfig = ExpertConfig.from_yaml(yaml_file)
                expert_configs.append(expert_config)
            except Exception as e:
                logger.warning(f"Could not load expert config ({str(yaml_file.absolute())}): {e}")
        
        return expert_configs

    def __generate_synth_learning_tasks(self, expert_task):
        task_agent = Agent(
            model=self.model,
            output_schema=TrainingTaskList,
            system_message=campus_agent_system_prompt,
        )

        run_output: RunOutput = task_agent.run(f"""Global task: {self.global_task}

                    Expert task: {expert_task}""")

        task_list: TrainingTaskList = TrainingTaskList.model_validate(
            run_output.content
        )

        return task_list

    def train_new_expert(self, expert_name: str, expert_task: str) -> None:

        expert_name = expert_name.replace(" ", "_").lower()

        logger.debug(f"Creating synthetic tasks for '{expert_task}'...")
        task_list: TrainingTaskList = self.__generate_synth_learning_tasks(expert_task)
        logger.debug(f"...created {len(task_list.tasks)} tasks.")

        def reward_func(model_output: str, task: str) -> int:
            reward_agent = Agent(
                model=self.model,
                system_message=reward_agent_system_prompt.format(
                    expert_task=expert_task, global_task=self.global_task
                ),
                output_schema=RewardOutput,
            )

            output: RunOutput = reward_agent.run(
                f"Task given: {task}\nOutput: {model_output}"
            )

            reward_output: RewardOutput = RewardOutput.model_validate(output.content)
            return reward_output.reward

        learner = ICRLLearner(
            agent=Agent(model=self.model),
            reward_func=reward_func,
            task_description=icrl_agent_system_prompt.format(
                global_task=self.global_task, expert_task=expert_task
            ),
            tasks=task_list.tasks,
        )

        logger.debug(f"Start training")
        learner.auto_learn()
        learner.update_strategy()

        logger.debug("Saving expert...")

        agent_config: ExpertConfig = ExpertConfig(
            name=expert_name,
            **learner.agent_save_state.model_dump(),
        )
        agent_config.to_yaml(self.save_path + f"/{expert_name}")

        logger.debug(f"Saved expert: {expert_name}")
