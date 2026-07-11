import pytest
from pydantic import ValidationError

from icle.campus.models.training_task_list import TrainingTask, TrainingTaskList


def make_task(prompt: str) -> TrainingTask:
    return TrainingTask(
        task=prompt, relevance_justification=f"Trains the expert on: {prompt}"
    )


def test_creation_with_tasks():
    tl = TrainingTaskList(tasks=[make_task("Task A"), make_task("Task B")])
    assert len(tl.tasks) == 2


def test_tasks_content_preserved():
    tl = TrainingTaskList(tasks=[make_task(p) for p in ["Do X", "Do Y", "Do Z"]])
    assert "Do X" in tl.task_prompts
    assert "Do Y" in tl.task_prompts
    assert "Do Z" in tl.task_prompts


def test_single_task_is_valid():
    tl = TrainingTaskList(tasks=[make_task("Only task")])
    assert len(tl.tasks) == 1


def test_empty_task_list_fails_validation():
    with pytest.raises(ValidationError):
        TrainingTaskList(tasks=[])


def test_task_requires_relevance_justification():
    with pytest.raises(ValidationError):
        TrainingTask(task="Write a poem")


def test_task_prompts_is_list_of_strings():
    tl = TrainingTaskList(
        tasks=[make_task("Write a poem"), make_task("Refine the poem")]
    )
    assert all(isinstance(t, str) for t in tl.task_prompts)
