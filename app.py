"""Streamlit interface for the PawPal+ care scheduler."""

from datetime import date, datetime, time

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")
st.caption("Plan everyday care for all your pets.")

if "owner" not in st.session_state:
    st.session_state.owner = Owner("My household")
owner = st.session_state.owner
scheduler = Scheduler(owner)

owner.name = st.text_input("Owner name", value=owner.name)
st.caption("Your information stays in this browser session and is cleared when the session ends.")

with st.expander("Add a pet", expanded=not owner.pets):
    with st.form("add_pet", clear_on_submit=True):
        pet_name = st.text_input("Pet name")
        species = st.selectbox("Species", ["dog", "cat", "other"])
        details = st.text_input("Pet details (optional)")
        if st.form_submit_button("Add pet"):
            if pet_name.strip():
                owner.add_pet(Pet(pet_name.strip(), species, details.strip()))
                st.success(f"Added {pet_name.strip()}.")
            else:
                st.error("Enter a pet name.")

if owner.pets:
    pet_options = list(range(len(owner.pets)))

    def pet_label(index):
        """Distinguish pets that happen to share a name."""
        return f"{owner.pets[index].name} ({owner.pets[index].species}, #{index + 1})"

    st.subheader("Schedule a task")
    with st.form("add_task", clear_on_submit=True):
        selected_pet = st.selectbox("Pet", pet_options, format_func=pet_label)
        description = st.text_input("Task description")
        due_date = st.date_input("Date", value=date.today())
        due_time = st.time_input("Time", value=time(8, 0))
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=1440, value=15)
        priority = st.selectbox("Priority", ["high", "medium", "low"])
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
        if st.form_submit_button("Add task"):
            if description.strip():
                owner.pets[selected_pet].add_task(Task(description.strip(), datetime.combine(due_date, due_time), int(duration), priority, frequency))
                st.success("Task added.")
            else:
                st.error("Enter a task description.")

    st.subheader("Care schedule")
    selected_date = st.date_input("Show date", value=date.today())
    pet_filter = st.selectbox("Filter by pet", ["All pets"] + [pet_label(i) for i in pet_options])
    status_filter = st.selectbox("Filter by status", ["All", "Incomplete", "Completed"])
    status = {"All": None, "Incomplete": False, "Completed": True}[status_filter]
    matching = scheduler.filter_tasks(completed=status)
    selected_owner_pet = None if pet_filter == "All pets" else owner.pets[[pet_label(i) for i in pet_options].index(pet_filter)]
    rows = []
    for task in scheduler.sort_by_time():
        pet = next(p for p in owner.pets if any(item is task for item in p.tasks))
        if (task.due_at.date() == selected_date and any(item is task for item in matching)
                and (selected_owner_pet is None or pet is selected_owner_pet)):
            rows.append((pet, task))
    if rows:
        st.table([{"Time": task.due_at.strftime("%H:%M"), "Pet": pet.name, "Task": task.description,
                   "Minutes": task.duration_minutes, "Priority": task.priority.title(),
                   "Frequency": task.frequency.title(), "Status": "Done" if task.completed else "Open"}
                  for pet, task in rows])
    else:
        st.info("No tasks match this date and these filters.")

    for first, second in scheduler.detect_conflicts():
        if first.due_at.date() == selected_date:
            first_pet = next(p.name for p in owner.pets if any(t is first for t in p.tasks))
            second_pet = next(p.name for p in owner.pets if any(t is second for t in p.tasks))
            st.warning(f"{first.due_at:%H:%M}: {first_pet}'s {first.description} and {second_pet}'s {second.description} start at the same time.")

    open_rows = [(pet, task) for pet, task in rows if not task.completed]
    if open_rows:
        st.markdown("#### Complete or edit a task")
        chosen = st.selectbox("Choose a task", range(len(open_rows)),
                              format_func=lambda i: f"{open_rows[i][0].name}: {open_rows[i][1].description} at {open_rows[i][1].due_at:%H:%M} (#{i + 1})")
        pet, task = open_rows[chosen]
        if st.button("Mark complete"):
            scheduler.complete_task(pet, task)
            st.rerun()
        with st.expander("Edit selected task"):
            with st.form("edit_task"):
                edited_description = st.text_input("Description", value=task.description)
                edited_date = st.date_input("Due date", value=task.due_at.date())
                edited_time = st.time_input("Due time", value=task.due_at.time())
                edited_duration = st.number_input("Minutes", min_value=1, max_value=1440, value=task.duration_minutes)
                priorities = ["high", "medium", "low"]
                frequencies = ["once", "daily", "weekly"]
                edited_priority = st.selectbox("Task priority", priorities, index=priorities.index(task.priority))
                edited_frequency = st.selectbox("Task frequency", frequencies, index=frequencies.index(task.frequency))
                if st.form_submit_button("Save changes"):
                    if edited_description.strip():
                        task.description = edited_description.strip()
                        task.due_at = datetime.combine(edited_date, edited_time)
                        task.duration_minutes = int(edited_duration)
                        task.priority = edited_priority
                        task.frequency = edited_frequency
                        st.rerun()
                    else:
                        st.error("Enter a task description.")

    st.subheader("Daily plan")
    budget = st.number_input("Available minutes", min_value=0, max_value=1440, value=60)
    plan = scheduler.build_daily_plan(selected_date, int(budget))
    st.caption("Higher-priority incomplete tasks are selected first within your time budget, then shown by time. Review conflicts separately.")
    if plan:
        st.table([{"Time": task.due_at.strftime("%H:%M"),
                   "Pet": next(p.name for p in owner.pets if any(t is task for t in p.tasks)), "Task": task.description,
                   "Minutes": task.duration_minutes, "Priority": task.priority.title()} for task in plan])
    else:
        st.info("No incomplete tasks fit the selected date and time budget.")
