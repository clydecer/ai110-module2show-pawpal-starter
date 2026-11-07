"""Initial tests for PawPal+ core behavior."""

from datetime import datetime, timedelta

import pytest

from pawpal_system import Owner, Pet, Scheduler, Task


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


@pytest.fixture
def schedule():
    owner = Owner("Jordan")
    pet = Pet("Mochi", "cat")
    other = Pet("Biscuit", "dog")
    owner.add_pet(pet)
    owner.add_pet(other)
    return Scheduler(owner), pet, other


def test_sorting_across_pets_and_dates(schedule):
    scheduler, pet, other = schedule
    later = Task("Later", datetime(2026, 11, 8, 7), 10, "low")
    earlier = Task("Earlier", datetime(2026, 11, 7, 18), 10, "high")
    pet.add_task(later)
    other.add_task(earlier)
    assert scheduler.sort_by_time() == [earlier, later]


def test_empty_owner_and_pet():
    owner = Owner("Jordan", pets=[Pet("Mochi", "cat")])
    scheduler = Scheduler(owner)
    assert scheduler.sort_by_time() == []
    assert scheduler.detect_conflicts() == []
    assert scheduler.filter_tasks() == []


def test_filter_by_pet_name_and_status_including_duplicate_names(schedule):
    scheduler, pet, other = schedule
    other.name = "mochi"
    first = Task("Feed", datetime(2026, 11, 7, 8), 10, "high")
    done = Task("Walk", datetime(2026, 11, 7, 9), 20, "low", completed=True)
    pet.add_task(first)
    other.add_task(done)
    assert scheduler.filter_tasks("MOCHI") == [first, done]
    assert scheduler.filter_tasks("mochi", completed=False) == [first]
    assert scheduler.filter_tasks(completed=True) == [done]
    assert scheduler.filter_tasks("missing") == []


@pytest.mark.parametrize("frequency,days", [("daily", 1), ("weekly", 7)])
def test_recurring_task_creates_one_next_occurrence(schedule, frequency, days):
    scheduler, pet, _ = schedule
    task = Task("Medicine", datetime(2026, 11, 7, 8), 5, "high", frequency)
    pet.add_task(task)
    scheduler.complete_task(pet, task)
    scheduler.complete_task(pet, task)
    assert task.completed
    assert len(pet.tasks) == 2
    assert pet.tasks[1].due_at == task.due_at + timedelta(days=days)
    assert not pet.tasks[1].completed
    assert pet.tasks[1].frequency == frequency


def test_one_time_completion_does_not_recur(schedule):
    scheduler, pet, _ = schedule
    task = Task("Vet", datetime(2026, 11, 7, 8), 30, "high")
    pet.add_task(task)
    scheduler.complete_task(pet, task)
    assert task.completed and len(pet.tasks) == 1


def test_completion_rejects_unowned_pet_or_task(schedule):
    scheduler, pet, other = schedule
    task = Task("Feed", datetime(2026, 11, 7, 8), 10, "high")
    pet.add_task(task)
    with pytest.raises(ValueError):
        scheduler.complete_task(other, task)
    with pytest.raises(ValueError):
        scheduler.complete_task(Pet("Stray", "cat"), task)
    assert not task.completed


def test_conflicts_require_same_date_and_time_and_ignore_completed(schedule):
    scheduler, pet, other = schedule
    start = datetime(2026, 11, 7, 8)
    first = Task("Feed", start, 10, "high")
    second = Task("Walk", start, 30, "low")
    pet.add_task(first)
    other.add_task(second)
    other.add_task(Task("Tomorrow", start + timedelta(days=1), 10, "low"))
    pet.add_task(Task("Finished", start, 10, "low", completed=True))
    assert scheduler.detect_conflicts() == [(first, second)]


def test_daily_plan_uses_priority_budget_date_and_completion(schedule):
    scheduler, pet, _ = schedule
    start = datetime(2026, 11, 7, 8)
    low = Task("Play", start, 20, "low")
    high = Task("Medicine", start + timedelta(hours=2), 10, "high")
    pet.tasks.extend([low, high, Task("Done", start, 5, "high", completed=True),
                      Task("Tomorrow", start + timedelta(days=1), 5, "high")])
    assert scheduler.build_daily_plan(start.date(), 20) == [high]
    assert scheduler.build_daily_plan(start.date(), 30) == [low, high]
    assert scheduler.build_daily_plan(start.date(), 0) == []
    with pytest.raises(ValueError):
        scheduler.build_daily_plan(start.date(), -1)
