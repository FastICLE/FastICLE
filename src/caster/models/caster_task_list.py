
from dispatcher.models.dispatcher_task import DispatcherTask
from pydantic import Field
from typing import Annotated
from pydantic import BaseModel

class CasterTaskList(BaseModel):
    assigned_tasks: Annotated[list[tuple[list[str], DispatcherTask]], Field()]