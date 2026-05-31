
from campus.core import Campus

import pytest


@pytest.mark.api
def test_run_campus(g_data):
    campus = Campus(
        global_task="Write poems.",
        save_path="./tests/data",
        model=g_data["model"]
    )

    campus.train_new_expert("Nature poems", "Poems about the nature.")