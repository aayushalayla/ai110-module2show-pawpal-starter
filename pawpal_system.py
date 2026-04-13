from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Optional


@dataclass
class Task:
    title: str
    description: str
    due_date: datetime
    is_completed: bool = False
    recurrence: Optional[str] = None

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        pass

    def is_overdue(self) -> bool:
        """Return True if the task is past due and not completed."""
        pass

    def reschedule(self, new_due_date: datetime) -> None:
        """Update the due date for the task."""
        pass


@dataclass
class Pet:
    name: str
    species: str
    breed: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a new task to this pet."""
        pass

    def get_pending_tasks(self) -> list[Task]:
        """Return all incomplete tasks for this pet."""
        pass

    def get_completed_tasks(self) -> list[Task]:
        """Return all completed tasks for this pet."""
        pass


@dataclass
class Owner:
    name: str
    email: str
    phone: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's pet list."""
        pass

    def remove_pet(self, pet_name: str) -> None:
        """Remove a pet by name."""
        pass

    def get_all_tasks(self) -> list[Task]:
        """Return all tasks across all pets."""
        pass


@dataclass
class Scheduler:
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to the scheduler."""
        pass

    def remove_task(self, task_title: str) -> None:
        """Remove a task by title."""
        pass

    def get_today_tasks(self) -> list[Task]:
        """Return tasks due today."""
        pass

    def get_upcoming_tasks(self) -> list[Task]:
        """Return future tasks that are not due today."""
        pass

    def get_overdue_tasks(self) -> list[Task]:
        """Return overdue incomplete tasks."""
        pass