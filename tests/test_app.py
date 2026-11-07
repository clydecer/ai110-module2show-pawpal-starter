"""Exercise the main Streamlit workflow against the real backend."""

from streamlit.testing.v1 import AppTest


def test_pet_task_and_daily_recurrence_in_ui():
    app = AppTest.from_file("app.py", default_timeout=30).run()
    next(field for field in app.text_input if field.label == "Pet name").set_value("Mochi")
    next(button for button in app.button if button.label == "Add pet").click().run()
    next(field for field in app.text_input if field.label == "Task description").set_value("Breakfast")
    next(field for field in app.selectbox if field.label == "Frequency").select("daily")
    next(button for button in app.button if button.label == "Add task").click().run()
    pet = app.session_state["owner"].pets[0]
    assert len(pet.tasks) == 1
    assert not app.exception

    next(button for button in app.button if button.label == "Mark complete").click().run()
    assert len(pet.tasks) == 2
    assert pet.tasks[0].completed and not pet.tasks[1].completed
    assert (pet.tasks[1].due_at - pet.tasks[0].due_at).days == 1
    assert not app.exception
