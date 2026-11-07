"""Core objects for the PawPal+ care scheduler."""

from dataclasses import dataclass, field
from datetime import date, datetime
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
        """Mark this occurrence as complete."""
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
        """Filter tasks by pet name and completion status."""
        raise NotImplementedError

    def detect_conflicts(self) -> List[Tuple[Task, Task]]:
        """Identify pairs of tasks that conflict."""
        raise NotImplementedError

    def complete_task(self, pet: Pet, task: Task) -> None:
        """Mark a task belonging to one of the owner's pets complete."""
        # Identity checks prevent an equal-looking task or pet from being mistaken for this one.
        if not any(owned_pet is pet for owned_pet in self.owner.pets):
            raise ValueError("Pet does not belong to this owner")
        if not any(pet_task is task for pet_task in pet.tasks):
            raise ValueError("Task does not belong to this pet")
        task.mark_complete()

    def build_daily_plan(self, day: date, available_minutes: int) -> List[Task]:
        """Plan tasks for a day using the available time and priorities."""
        raise NotImplementedError
