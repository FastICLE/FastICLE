from fasticrl.models.agent_save_state import AgentSaveState
from typing import Annotated
from pydantic import Field
from pydantic import BaseModel

class AgentConfig(BaseModel):
    agent_save_state: Annotated[AgentSaveState, Field()]
    description: Annotated[str, Field(default="")]
    