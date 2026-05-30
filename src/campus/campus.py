from agno.models.base import Model
from typing import Annotated

from pydantic import BaseModel, Field

from campus.models.agent_config import AgentConfig
from fasticrl.icrl_learner import ICRLLearner


class Campus(BaseModel):
    save_path: Annotated[str, Field(default="~")]
    auto_save: Annotated[bool, Field(default=True)]
    agent_configs: Annotated[list[AgentConfig], Field(default=[])]
    
    model: Annotated[Model, Field()]
    
    learner: Annotated[ICRLLearner, Field(default=False)]

     
    def get_agent_repr(self) -> list:
        pass
    
    
    def train_new_expert(self, task: str) -> None:
        pass
    