from pydantic import Field
from typing import Annotated
from pydantic import BaseModel


class RewardOutput(BaseModel):
    reward: Annotated[
        int, Field(ge=-1, description="Reward given on basis on the input.")
    ]
