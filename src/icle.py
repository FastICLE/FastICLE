from runtime.core import runtime
from step_identifier import STEP_IDENTIFIER

from agno.workflow import Step, Workflow

from caster.core import CasterAgent
from dispatcher.core import DispatcherAgent


class ICLE(Workflow):

    def __init__(
        self, dispatcher_agent: DispatcherAgent, caster_agent: CasterAgent, **kwargs
    ):
        super().__init__(**kwargs)

        self.dispatcher_agent = dispatcher_agent
        self.caster_agent = caster_agent
        self.name = "ICLE Pipeline"
        self.steps = [
            Step(name=STEP_IDENTIFIER.DISPATCH, agent=dispatcher_agent),
            Step(name=STEP_IDENTIFIER.CAST, agent=caster_agent),
            Step(name=STEP_IDENTIFIER.RUNTIME, executor=runtime)
        ]
