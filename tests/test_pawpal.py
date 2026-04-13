from datetime import datetime, timedelta
from pawpal_system import Pet, Task, Owner, Scheduler


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


# --- Sorting Correctness ---

def test_sort_by_time_returns_chronological_order():
    """Verify that sort_by_time returns tasks sorted earliest due_date first."""
    now = datetime.now()

    task_late = Task(title="Late task", description="", due_date=now + timedelta(hours=3))
    task_early = Task(title="Early task", description="", due_date=now + timedelta(hours=1))
    task_middle = Task(title="Middle task", description="", due_date=now + timedelta(hours=2))

    pet = Pet(name="Buddy", species="Dog", breed="Labrador", age=2)
    pet.add_task(task_late)
    pet.add_task(task_early)
    pet.add_task(task_middle)

    owner = Owner(name="Alice", email="alice@example.com", phone="555-0100")
    owner.add_pet(pet)
    scheduler = Scheduler(owner=owner)

    sorted_tasks = scheduler.sort_by_time(pet.tasks)

    assert sorted_tasks[0].title == "Early task"
    assert sorted_tasks[1].title == "Middle task"
    assert sorted_tasks[2].title == "Late task"


# --- Recurrence Logic ---

def test_completing_daily_task_creates_next_day_task():
    """Confirm that create_recurring_task adds a new task due one day later."""
    now = datetime.now()
    daily_task = Task(
        title="Morning walk",
        description="Walk around the block",
        due_date=now,
        recurrence="daily"
    )

    pet = Pet(name="Rex", species="Dog", breed="Beagle", age=3)
    pet.add_task(daily_task)

    owner = Owner(name="Bob", email="bob@example.com", phone="555-0200")
    owner.add_pet(pet)
    scheduler = Scheduler(owner=owner)

    daily_task.mark_complete()
    scheduler.create_recurring_task(daily_task, pet)

    # After creating the recurring task there should be 2 tasks total
    assert len(pet.tasks) == 2

    # The new task should be due exactly one day after the original
    new_task = pet.tasks[1]
    assert new_task.due_date == now + timedelta(days=1)
    assert new_task.is_completed is False
    assert new_task.title == daily_task.title


# --- Conflict Detection ---

def test_detect_task_conflicts_flags_duplicate_times():
    """Verify that the Scheduler flags two pending tasks with the same due_date."""
    conflict_time = datetime(2026, 4, 14, 9, 0, 0)

    task_a = Task(title="Feed cat", description="Morning meal", due_date=conflict_time)
    task_b = Task(title="Vet appointment", description="Checkup", due_date=conflict_time)

    pet = Pet(name="Whiskers", species="Cat", breed="Siamese", age=5)
    pet.add_task(task_a)
    pet.add_task(task_b)

    owner = Owner(name="Carol", email="carol@example.com", phone="555-0300")
    owner.add_pet(pet)
    scheduler = Scheduler(owner=owner)

    warnings = scheduler.detect_task_conflicts()

    assert len(warnings) == 1
    assert "Feed cat" in warnings[0]
    assert "Vet appointment" in warnings[0]


def test_no_conflict_when_times_differ():
    """Verify that tasks at different times produce no warnings."""
    now = datetime.now()

    task_a = Task(title="Breakfast", description="", due_date=now + timedelta(hours=1))
    task_b = Task(title="Dinner", description="", due_date=now + timedelta(hours=8))

    pet = Pet(name="Max", species="Dog", breed="Poodle", age=6)
    pet.add_task(task_a)
    pet.add_task(task_b)

    owner = Owner(name="Dan", email="dan@example.com", phone="555-0400")
    owner.add_pet(pet)
    scheduler = Scheduler(owner=owner)

    warnings = scheduler.detect_task_conflicts()

    assert warnings == []
    