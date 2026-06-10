from agno.workflow import StepInput, StepOutput

from caster.models.caster_output import CasterOutput
from dispatcher.models.dispatcher_task_list import DispatcherTaskList
from step_identifier import STEP_IDENTIFIER 


def runtime(step_input: StepInput) -> StepOutput:
    caster_out: CasterOutput = step_input.get_step_content(STEP_IDENTIFIER.CAST)
    dispatcher_out: DispatcherTaskList = step_input.get_step_content(
        STEP_IDENTIFIER.DISPATCH
    )

    out: StepOutput = StepOutput(
        content=f"{caster_out.assigned_tasks}\n{dispatcher_out.tasks}"
    )

    return out
