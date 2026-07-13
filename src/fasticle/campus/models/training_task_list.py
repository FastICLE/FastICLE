from typing import Annotated

from pydantic import BaseModel, Field


class TrainingTask(BaseModel):
    task: Annotated[
        str,
        Field(
            description=(
                "Task title and detailed instruction prompt for this training "
                "exercise."
            )
        ),
    ]
    relevance_justification: Annotated[
        str,
        Field(
            description=(
                "One sentence explaining how this exercise trains the expert "
                "task's domain and requires the same kind of artifact the "
                "expert must produce."
            )
        ),
    ]


class TrainingTaskList(BaseModel):
    tasks: Annotated[list[TrainingTask], Field(min_length=1)]

    @property
    def task_prompts(self) -> list[str]:
        return [task.task for task in self.tasks]
