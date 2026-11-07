"""Core objects for the PawPal+ care scheduler."""

from dataclasses import dataclass, field, replace
from datetime import date, datetime, timedelta
from itertools import combinations
from typing import Dict, List, Optional, Tuple


@dataclass
class Task:
    """Describe one scheduled pet-care activity."""

    description: str
    due_at: datetime
    duration_minutes: int
    priority: str
    frequency: str = "once"
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this occurrence complete; use Scheduler for recurrence."""
        self.completed = True


@dataclass
class Pet:
    """Store a pet's details and care tasks."""

    name: str
    species: str
    details: str = ""
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task to this pet."""
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        """Return this pet's care tasks."""
        return list(self.tasks)


@dataclass
class Owner:
    """Store an owner's preferences and pets."""

    name: str
    preferences: Dict[str, str] = field(default_factory=dict)
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Collect tasks from all of this owner's pets."""
        return [task for pet in self.pets for task in pet.get_tasks()]


class Scheduler:
    """Organize an owner's pet-care tasks."""

    def __init__(self, owner: Owner) -> None:
        """Connect the scheduler to an owner."""
        self.owner = owner

    def get_all_tasks(self) -> List[Task]:
        """Retrieve tasks from the owner's pets."""
        return self.owner.get_all_tasks()

    def sort_by_time(self) -> List[Task]:
        """Return tasks in chronological order."""
        return sorted(self.get_all_tasks(), key=lambda task: task.due_at)

    def filter_tasks(
        self, pet_name: Optional[str] = None, completed: Optional[bool] = None
    ) -> List[Task]:
        """Filter tasks by pet name and completion status, preserving their order."""
        return [
            task
            for pet in self.owner.pets
            if pet_name is None or pet.name.casefold() == pet_name.casefold()
            for task in pet.tasks
            if completed is None or task.completed == completed
        ]

    def detect_conflicts(self) -> List[Tuple[Task, Task]]:
        """Return incomplete task pairs with identical dates and start times."""
        return [
            (first, second)
            for first, second in combinations(self.filter_tasks(completed=False), 2)
            if first.due_at == second.due_at
        ]

    def complete_task(self, pet: Pet, task: Task) -> None:
        """Complete a task and create its next daily or weekly occurrence once."""
        # Identity checks prevent an equal-looking task or pet from being mistaken for this one.
        if not any(owned_pet is pet for owned_pet in self.owner.pets):
            raise ValueError("Pet does not belong to this owner")
        if not any(pet_task is task for pet_task in pet.tasks):
            raise ValueError("Task does not belong to this pet")
        if task.completed:
            return
        frequency = task.frequency.lower()
        if frequency not in ("once", "daily", "weekly"):
            raise ValueError("Frequency must be once, daily, or weekly")
        task.mark_complete()
        if frequency != "once":
            days = 1 if frequency == "daily" else 7
            # Use completion day while preserving the task's time of day.
            next_due = datetime.combine(date.today() + timedelta(days=days), task.due_at.timetz())
            pet.add_task(replace(task, due_at=next_due, completed=False))

    def build_daily_plan(self, day: date, available_minutes: int) -> List[Task]:
        """Select incomplete tasks by priority within a time budget, then sort by time."""
        if available_minutes < 0:
            raise ValueError("Available time cannot be negative")
        priorities = {"high": 0, "medium": 1, "low": 2}
        candidates = [task for task in self.filter_tasks(completed=False) if task.due_at.date() == day]
        candidates.sort(key=lambda task: (priorities.get(task.priority.lower(), 3), task.due_at))
        plan = []
        remaining = available_minutes
        for task in candidates:
            if task.duration_minutes <= 0:
                raise ValueError("Task duration must be positive")
            if task.duration_minutes <= remaining:
                plan.append(task)
                remaining -= task.duration_minutes
        return sorted(plan, key=lambda task: task.due_at)
