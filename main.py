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
    mochi.add_task(Task("Evening medication", datetime.combine(today, time(18, 0)), 5, "high"))
    biscuit.add_task(Task("Morning walk", datetime.combine(today, time(8, 0)), 30, "medium"))
    breakfast = Task("Breakfast", datetime.combine(today, time(8, 0)), 10, "high", "daily")
    mochi.add_task(breakfast)

    scheduler = Scheduler(owner)
    print(f"Today's Schedule for {owner.name} ({today:%Y-%m-%d})")
    print("-" * 45)
    for task in scheduler.sort_by_time():
        # Tasks are stored on pets, so find the pet that owns this occurrence.
        pet = next(pet for pet in owner.pets if any(item is task for item in pet.tasks))
        print(f"{task.due_at:%H:%M}  {pet.name}: {task.description} ({task.duration_minutes} min)")

    print("\nMochi's incomplete tasks:")
    for task in scheduler.filter_tasks(pet_name="Mochi", completed=False):
        print(f"- {task.description}")

    for first, second in scheduler.detect_conflicts():
        print(f"\nWarning: {first.description} and {second.description} both start at {first.due_at:%H:%M}.")

    scheduler.complete_task(mochi, breakfast)
    print(f"\nCompleted {breakfast.description}; next occurrence: {mochi.tasks[-1].due_at:%Y-%m-%d %H:%M}")
    print("Completed tasks:", ", ".join(task.description for task in scheduler.filter_tasks(completed=True)))
    plan = scheduler.build_daily_plan(today, available_minutes=35)
    print("Today's plan (35 minute budget):", ", ".join(task.description for task in plan))


if __name__ == "__main__":
    main()
