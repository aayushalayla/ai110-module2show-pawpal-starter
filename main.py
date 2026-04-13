from datetime import datetime, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler

owner = Owner("Alice", "alice@example.com", "555-123-4567")

dog = Pet("Milo", "dog", "beagle", 3)
cat = Pet("Luna", "cat", "tabby", 2)

owner.add_pet(dog)
owner.add_pet(cat)

same_time = datetime.now() + timedelta(hours=1)

task1 = Task(
    title="Morning Walk",
    description="Take Milo for a walk",
    due_date=same_time
)

task2 = Task(
    title="Feed Luna",
    description="Give Luna dinner",
    due_date=same_time
)

task3 = Task(
    title="Vet Appointment",
    description="Bring Milo to the vet",
    due_date=datetime.now() + timedelta(hours=3)
)

dog.add_task(task1)
cat.add_task(task2)
dog.add_task(task3)

scheduler = Scheduler(owner)

print("\n=== Today's Schedule ===")
today_tasks = scheduler.get_today_tasks()

if today_tasks:
    for task in today_tasks:
        status = "Completed" if task.is_completed else "Pending"
        print(f"- {task.title}")
        print(f"  Description: {task.description}")
        print(f"  Due: {task.due_date.strftime('%Y-%m-%d %H:%M')}")
        print(f"  Status: {status}")
        print()
else:
    print("No tasks scheduled for today.")

print("=== Overdue Tasks ===")
overdue_tasks = scheduler.get_overdue_tasks()

if overdue_tasks:
    for task in overdue_tasks:
        print(f"- {task.title} (due {task.due_date.strftime('%Y-%m-%d %H:%M')})")
else:
    print("No overdue tasks.")

print("\n=== Conflict Check ===")
conflicts = scheduler.detect_task_conflicts()

if conflicts:
    for warning in conflicts:
        print(warning)
else:
    print("No conflicts detected.")