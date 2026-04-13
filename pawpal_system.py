from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


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

    def get_today_tasks(self) -> list[Task]:
        """Return tasks due today from all pets."""
        today = datetime.now().date()
        return [
            task for task in self.owner.get_all_tasks()
            if task.due_date.date() == today and not task.is_completed
        ]

    def get_upcoming_tasks(self) -> list[Task]:
        """Return future tasks that are not due today from all pets."""
        now = datetime.now()
        today = now.date()
        return [
            task for task in self.owner.get_all_tasks()
            if task.due_date > now and task.due_date.date() != today and not task.is_completed
        ]

    def get_overdue_tasks(self) -> list[Task]:
        """Return overdue incomplete tasks from all pets."""
        return [
            task for task in self.owner.get_all_tasks()
            if task.is_overdue()
        ]