from agno.workflow import StepInput, StepOutput

from step_identifier import STEP_IDENTIFIER
from task import CasterTaskList, DispatcherTaskList


def runtime(step_input: StepInput) -> StepOutput:
    caster_out: CasterTaskList = step_input.get_step_content(STEP_IDENTIFIER.CAST)
    dispatcher_out: DispatcherTaskList = step_input.get_step_content(
        STEP_IDENTIFIER.DISPATCH
    )

    out: StepOutput = StepOutput(
        content=f"{caster_out.model_dump_json()}\n{dispatcher_out.model_dump_json()}"
    )

    return out
