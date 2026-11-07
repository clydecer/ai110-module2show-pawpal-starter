# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## Core user actions

1. Add a pet and its basic details to an owner's profile.
2. Schedule a care task for a pet, such as a feeding, walk, or medication.
3. View the day's care tasks in a clear schedule.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Run `python main.py` from the project directory to print the example schedule. The date reflects the day the demo is run. Sample output:

```
Today's Schedule for Jordan (2026-11-06)
---------------------------------------------
08:00  Mochi: Breakfast (10 min)
08:00  Biscuit: Morning walk (30 min)
18:00  Mochi: Evening medication (5 min)

Mochi's incomplete tasks:
- Evening medication
- Breakfast

Warning: Breakfast and Morning walk both start at 08:00.

Completed Breakfast; next occurrence: 2026-11-07 08:00
Completed tasks: Breakfast
Today's plan (35 minute budget): Morning walk, Evening medication
```

## 🧪 Testing PawPal+

```bash
python -m pytest
```

The tests cover task addition and completion, sorting, filtering, recurrence, conflict detection, ownership checks, empty schedules, and daily planning. Sample output from a successful run:

```
============================= test session starts ==============================
platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/clydecermeus/Documents/Codex/2026-11-06/lo/pawpal
collected 11 items

tests/test_pawpal.py ...........                                         [100%]

============================== 11 passed in 0.02s ==============================
```

**Provisional confidence: 3/5 stars.** The core paths and several edge cases pass, but the UI integration and additional scheduling scenarios still need verification.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Orders tasks by full due date and time. |
| Filtering | `Scheduler.filter_tasks()` | Filters by completion status and/or case-insensitive pet name; duplicate names all match. |
| Conflict detection | `Scheduler.detect_conflicts()` | Returns pairs of incomplete tasks with the same date and start time, across pets. It does not detect overlapping durations. |
| Recurring tasks | `Scheduler.complete_task()` | Completing a daily or weekly task creates one incomplete occurrence one or seven days after its scheduled date; repeat completion does not create duplicates. Call this scheduler method for recurrence. |
| Daily planning | `Scheduler.build_daily_plan()` | Selects incomplete tasks for a date by priority within a total minute budget, then displays them in time order. It does not resolve conflicts or use owner preferences. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
