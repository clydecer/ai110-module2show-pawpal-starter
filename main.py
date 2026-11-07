"""Demonstrate the core PawPal+ classes in the terminal."""

from datetime import date, datetime, time

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    """Create example pets and print their care schedule for today."""
    owner = Owner("Jordan")
    mochi = Pet("Mochi", "cat")
    biscuit = Pet("Biscuit", "dog")
    owner.add_pet(mochi)
    owner.add_pet(biscuit)

    today = date.today()
    mochi.add_task(Task("Breakfast", datetime.combine(today, time(8, 0)), 10, "high"))
    biscuit.add_task(Task("Morning walk", datetime.combine(today, time(9, 0)), 30, "high"))
    mochi.add_task(Task("Evening medication", datetime.combine(today, time(18, 0)), 5, "high"))

    scheduler = Scheduler(owner)
    print(f"Today's Schedule for {owner.name} ({today:%Y-%m-%d})")
    print("-" * 45)
    for task in scheduler.sort_by_time():
        # Tasks are stored on pets, so find the pet that owns this occurrence.
        pet = next(pet for pet in owner.pets if any(item is task for item in pet.tasks))
        print(f"{task.due_at:%H:%M}  {pet.name}: {task.description} ({task.duration_minutes} min)")


if __name__ == "__main__":
    main()
