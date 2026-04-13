from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from datetime import timedelta


@dataclass
class Task:
    title: str
    description: str
    due_date: datetime
    is_completed: bool = False
    recurrence: Optional[str] = None
    completed_at: Optional[datetime] = None

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.completed_at = datetime.now()
        self.is_completed = True

    def is_overdue(self, current_date: Optional[datetime] = None) -> bool:
        """Return True if the task is past due and not completed."""
        if current_date is None:
            current_date = datetime.now()
        return not self.is_completed and self.due_date < current_date

    def reschedule(self, new_due_date: datetime) -> None:
        """Update the due date for the task."""
        self.due_date = new_due_date


@dataclass
class Pet:
    name: str
    species: str
    breed: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a new task to this pet."""
        self.tasks.append(task)

    def get_pending_tasks(self) -> list[Task]:
        """Return all incomplete tasks for this pet."""
        return [task for task in self.tasks if not task.is_completed]

    def get_completed_tasks(self) -> list[Task]:
        """Return all completed tasks for this pet."""
        return [task for task in self.tasks if task.is_completed]


@dataclass
class Owner:
    name: str
    email: str
    phone: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's pet list."""
        self.pets.append(pet)

    def remove_pet(self, pet_name: str) -> None:
        """Remove a pet by name."""
        self.pets = [pet for pet in self.pets if pet.name != pet_name]

    def get_all_tasks(self) -> list[Task]:
        """Return all tasks across all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

@dataclass
class Scheduler:
    owner: Owner

    def detect_task_conflicts(self) -> list[str]:
        """Detect and return warning messages for tasks scheduled at the same time."""
        warnings = []
        all_tasks = self.owner.get_all_tasks()

        for i, task1 in enumerate(all_tasks):
            for task2 in all_tasks[i + 1:]:
                if task1.due_date == task2.due_date and not task1.is_completed and not task2.is_completed:
                    pet1 = next(pet for pet in self.owner.pets if task1 in pet.tasks)
                    pet2 = next(pet for pet in self.owner.pets if task2 in pet.tasks)
                    warning = (
                        f"⚠️ Conflict: '{task1.title}' ({pet1.name}) and "
                        f"'{task2.title}' ({pet2.name}) scheduled for "
                        f"{task1.due_date.strftime('%Y-%m-%d %H:%M')}"
                    )
                    warnings.append(warning)

        return warnings

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Return a list of tasks sorted by due date and time."""
        return sorted(tasks, key=lambda task: task.due_date)

    def get_today_tasks(self) -> list[Task]:
        """Return tasks due today from all pets."""
        today = datetime.now().date()
        tasks = [
            task for task in self.owner.get_all_tasks()
            if task.due_date.date() == today and not task.is_completed
        ]
        return self.sort_by_time(tasks)

    def get_upcoming_tasks(self) -> list[Task]:
        """Return future tasks that are not due today from all pets."""
        now = datetime.now()
        today = now.date()
        tasks = [
            task for task in self.owner.get_all_tasks()
            if task.due_date > now and task.due_date.date() != today and not task.is_completed
        ]
        return self.sort_by_time(tasks)

    def get_overdue_tasks(self) -> list[Task]:
        """Return overdue incomplete tasks from all pets."""
        tasks = [
            task for task in self.owner.get_all_tasks()
            if task.is_overdue()
        ]
        return self.sort_by_time(tasks)

    def filter_tasks(
        self,
        pet_name: Optional[str] = None,
        is_completed: Optional[bool] = None
    ) -> list[Task]:
        """Filter tasks by pet name and/or completion status."""
        filtered_tasks = []

        for pet in self.owner.pets:
            if pet_name is not None and pet.name != pet_name:
                continue

            for task in pet.tasks:
                if is_completed is None or task.is_completed == is_completed:
                    filtered_tasks.append(task)

        return self.sort_by_time(filtered_tasks)

    def create_recurring_task(self, task: Task, pet: Pet) -> None:
        """Create a new recurring task for the next occurrence."""
        if task.recurrence == "daily":
            new_due_date = task.due_date + timedelta(days=1)
        elif task.recurrence == "weekly":
            new_due_date = task.due_date + timedelta(weeks=1)
        else:
            return

        new_task = Task(
            title=task.title,
            description=task.description,
            due_date=new_due_date,
            recurrence=task.recurrence
        )
        pet.add_task(new_task)