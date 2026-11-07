"""Initial tests for PawPal+ core behavior."""

from datetime import datetime

from pawpal_system import Pet, Task


def test_mark_complete_changes_task_status():
    task = Task("Feed", datetime(2026, 11, 7, 8), 10, "high")

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet("Mochi", "cat")
    task = Task("Feed", datetime(2026, 11, 7, 8), 10, "high")
    before = len(pet.tasks)

    pet.add_task(task)

    assert len(pet.tasks) == before + 1
    assert pet.tasks[-1] is task
