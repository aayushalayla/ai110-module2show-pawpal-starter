from datetime import datetime
from pawpal_system import Pet, Task


def test_mark_complete_changes_task_status():
    """Verify that calling mark_complete() actually changes the task's status."""
    task = Task(
        title="Feed dog",
        description="Give dog breakfast",
        due_date=datetime.now()
    )

    task.mark_complete()

    assert task.is_completed is True


def test_adding_task_increases_pet_task_count():
    """Verify that adding a task to a Pet increases that pet's task count."""
    pet = Pet(
        name="Fluffy",
        species="Dog",
        breed="Golden Retriever",
        age=4
    )

    task = Task(
        title="Walk",
        description="Take Fluffy for a walk",
        due_date=datetime.now()
    )

    pet.add_task(task)

    assert len(pet.tasks) == 1
    