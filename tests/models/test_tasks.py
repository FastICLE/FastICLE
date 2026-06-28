import xml.etree.ElementTree as ET

import pytest
from pydantic import ValidationError

from models.tasks import (
    CasterTask,
    CasterTaskList,
    DispatcherTask,
    DispatcherTaskList,
    RuntimeTask,
    RuntimeTaskList,
)


class TestDispatcherTask:
    def test_creation(self):
        task = DispatcherTask(order_number=1, description="Test task")
        assert task.order_number == 1
        assert task.description == "Test task"

    def test_str_contains_class_name(self):
        task = DispatcherTask(order_number=1, description="Test task")
        assert "DispatcherTask" in str(task)

    def test_str_contains_order_number(self):
        task = DispatcherTask(order_number=42, description="Test task")
        assert "order_number: 42" in str(task)

    def test_str_contains_description(self):
        task = DispatcherTask(order_number=1, description="My description")
        assert "description: My description" in str(task)

    def test_repr_equals_str(self):
        task = DispatcherTask(order_number=1, description="Test task")
        assert repr(task) == str(task)

    def test_to_xml_wraps_in_task_tag(self):
        task = DispatcherTask(order_number=1, description="Test task")
        xml = task.to_xml()
        assert xml.startswith("<task>")
        assert xml.endswith("</task>")

    def test_to_xml_contains_order_number(self):
        task = DispatcherTask(order_number=7, description="Test")
        assert "<order_number>7</order_number>" in task.to_xml()

    def test_to_xml_contains_description(self):
        task = DispatcherTask(order_number=1, description="Do something")
        assert "<description>Do something</description>" in task.to_xml()

    def test_to_xml_is_parseable(self):
        task = DispatcherTask(order_number=1, description="A & B < C > D")
        ET.fromstring(task.to_xml())  # raises ParseError if XML is malformed

    def test_to_xml_preserves_content_when_parsed(self):
        task = DispatcherTask(order_number=1, description="A & B < C > D")
        root = ET.fromstring(task.to_xml())
        assert root.find("description").text == "A & B < C > D"

    def test_requires_order_number(self):
        with pytest.raises(ValidationError):
            DispatcherTask(description="Missing order number")

    def test_requires_description(self):
        with pytest.raises(ValidationError):
            DispatcherTask(order_number=1)


class TestCasterTask:
    def test_inherits_dispatcher_task(self):
        task = CasterTask(order_number=1, description="Cast task")
        assert isinstance(task, DispatcherTask)

    def test_default_agent_ids_empty(self):
        task = CasterTask(order_number=1, description="Cast task")
        assert task.agent_ids == []

    def test_agent_ids_set(self):
        task = CasterTask(order_number=1, description="Cast task", agent_ids=["a1", "a2"])
        assert task.agent_ids == ["a1", "a2"]

    def test_to_xml_inherited(self):
        task = CasterTask(order_number=1, description="Cast task", agent_ids=["agent"])
        xml = task.to_xml()
        assert "<task>" in xml
        assert "<description>Cast task</description>" in xml

    def test_str_contains_agent_ids(self):
        task = CasterTask(order_number=1, description="Cast task", agent_ids=["agent1"])
        assert "agent_ids" in str(task)


class TestRuntimeTask:
    def test_inherits_caster_task(self):
        task = RuntimeTask(order_number=1, description="Run", agent_ids=[], task_output="out")
        assert isinstance(task, CasterTask)
        assert isinstance(task, DispatcherTask)

    def test_task_output_field(self):
        task = RuntimeTask(order_number=1, description="Run", agent_ids=["a"], task_output="result")
        assert task.task_output == "result"

    def test_requires_task_output(self):
        with pytest.raises(ValidationError):
            RuntimeTask(order_number=1, description="Run", agent_ids=[])

    def test_to_xml_inherited(self):
        task = RuntimeTask(order_number=1, description="Run task", agent_ids=[], task_output="out")
        xml = task.to_xml()
        assert "<task>" in xml


class TestDispatcherTaskList:
    def test_empty_list(self):
        tl = DispatcherTaskList(task_list=[])
        assert tl.task_list == []

    def test_multiple_tasks(self):
        tasks = [DispatcherTask(order_number=i, description=f"Task {i}") for i in range(3)]
        tl = DispatcherTaskList(task_list=tasks)
        assert len(tl.task_list) == 3

    def test_tasks_preserved_in_order(self):
        tasks = [DispatcherTask(order_number=i, description=f"Task {i}") for i in range(5)]
        tl = DispatcherTaskList(task_list=tasks)
        for i, task in enumerate(tl.task_list):
            assert task.order_number == i


class TestCasterTaskList:
    def test_creation(self):
        tasks = [CasterTask(order_number=1, description="t", agent_ids=["a"])]
        tl = CasterTaskList(task_list=tasks)
        assert len(tl.task_list) == 1

    def test_empty_list(self):
        tl = CasterTaskList(task_list=[])
        assert tl.task_list == []


class TestRuntimeTaskList:
    def test_default_is_empty(self):
        tl = RuntimeTaskList()
        assert tl.task_list == []

    def test_to_xml_empty_list(self):
        tl = RuntimeTaskList()
        xml = tl.to_xml()
        assert xml.startswith("<tasks>")
        assert xml.endswith("</tasks>")

    def test_to_xml_wraps_all_tasks(self):
        tasks = [
            RuntimeTask(order_number=1, description="First", agent_ids=["a"], task_output="out1"),
            RuntimeTask(order_number=2, description="Second", agent_ids=["b"], task_output="out2"),
        ]
        tl = RuntimeTaskList(task_list=tasks)
        xml = tl.to_xml()
        assert xml.count("<task>") == 2
        assert xml.count("</task>") == 2

    def test_to_xml_contains_task_content(self):
        tasks = [RuntimeTask(order_number=1, description="Do work", agent_ids=[], task_output="done")]
        tl = RuntimeTaskList(task_list=tasks)
        xml = tl.to_xml()
        assert "Do work" in xml

    def test_to_xml_empty_is_parseable(self):
        tl = RuntimeTaskList()
        root = ET.fromstring(tl.to_xml())
        assert root.tag == "tasks"
        assert len(root) == 0

    def test_append_task(self):
        tl = RuntimeTaskList()
        task = RuntimeTask(order_number=1, description="t", agent_ids=[], task_output="o")
        tl.task_list.append(task)
        assert len(tl.task_list) == 1
