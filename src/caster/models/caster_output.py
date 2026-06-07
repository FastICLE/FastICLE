from pydantic import Field
from typing import Annotated
from pydantic import BaseModel


class CasterOutput(BaseModel):
    assigned_tasks: Annotated[
        list[tuple[list[str], int]],
        Field(
            description="A list of task assignments. Each assignment is a tuple containing: 1. A list of assigned agent IDs (use ['train_new_expert'] if no existing expert fits and a new one must be trained), and 2. The integer ID of the task."
        ),
    ]
