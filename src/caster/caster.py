from agno.run.agent import RunOutput
from agno.agent import Agent
from functools import wraps


class CasterAgent(Agent):        
    
    @wraps(Agent.run)
    def invoke(self, *args, **kwargs) -> RunOutput:
        
        return super().run(*args, **kwargs)
    

    