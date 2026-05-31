from fasticrl.icrl_learner import ICRLLearner
from campus.campus_agent import Campus
from caster.caster import CasterAgent

def test_instance(g_data):
    try:
        caster = CasterAgent(campus=Campus(model=g_data["model"], learner=ICRLLearner()))
    except Exception as _:
        assert False
    assert True
