DEPENDENCY_CONTEXT_PREAMBLE = (
    "The <dependency_outputs> block below contains the completed results of the "
    "tasks this task depends on. Treat them as fixed, authoritative decisions: "
    "your output MUST be consistent with them and build directly on them — do "
    "not contradict, replace, or reinvent anything they already established."
)

ORIGINAL_REQUEST_PREAMBLE = (
    "The <original_user_request> block below is the full request the overall "
    "pipeline is fulfilling. It is BACKGROUND ONLY — your job is solely the "
    "sub-task described at the end of this message. However, honor every "
    "requirement in the request that applies to your sub-task (constraints, "
    "level of detail, deliverables, output format), even if the sub-task "
    "description does not repeat it."
)

TASK_EXECUTION_INSTRUCTIONS = (
    "You are executing one sub-task of a larger automated pipeline. "
    "There is no human user available: NEVER ask clarifying questions or request "
    "missing details. If information is missing or ambiguous, make sensible "
    "assumptions, state them briefly, and deliver the completed work anyway. "
    "Your response must contain ONLY the finished work product for this sub-task "
    "— no meta-commentary, no questions, and no notes about delegation or team "
    "coordination."
)
