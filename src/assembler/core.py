

from assembler.prompts import ASSEMBLER_AGENT_PROMPT
from agno.agent import Agent


class Assembler(Agent):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.system_message = ASSEMBLER_AGENT_PROMPT
        