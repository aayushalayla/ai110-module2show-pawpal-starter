from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timedelta
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

    def to_dict(self) -> dict:
        """Serialise the task to a JSON-compatible dict."""
        return {
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date.isoformat(),
            "is_completed": self.is_completed,
            "recurrence": self.recurrence,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Reconstruct a Task from a dict produced by to_dict()."""
        return cls(
            title=data["title"],
            description=data["description"],
            due_date=datetime.fromisoformat(data["due_date"]),
            is_completed=data["is_completed"],
            recurrence=data.get("recurrence"),
            completed_at=datetime.fromisoformat(data["completed_at"]) if data.get("completed_at") else None,
        )


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

    def to_dict(self) -> dict:
        """Serialise the pet to a JSON-compatible dict."""
        return {
            "name": self.name,
            "species": self.species,
            "breed": self.breed,
            "age": self.age,
            "tasks": [task.to_dict() for task in self.tasks],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Pet":
        """Reconstruct a Pet from a dict produced by to_dict()."""
        pet = cls(
            name=data["name"],
            species=data["species"],
            breed=data["breed"],
            age=data["age"],
        )
        pet.tasks = [Task.from_dict(t) for t in data.get("tasks", [])]
        return pet


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

    def save_to_json(self, path: str = "data.json") -> None:
        """Persist the owner, all pets, and all tasks to a JSON file."""
        data = {
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "pets": [pet.to_dict() for pet in self.pets],
        }
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    @classmethod
    def load_from_json(cls, path: str = "data.json") -> "Owner":
        """Load an Owner (with pets and tasks) from a JSON file.

        Returns a default Owner if the file does not exist yet.
        """
        if not os.path.exists(path):
            return cls(name="Sam", email="sam@example.com", phone="123-456-7890")
        with open(path) as f:
            data = json.load(f)
        owner = cls(
            name=data["name"],
            email=data["email"],
            phone=data["phone"],
        )
        owner.pets = [Pet.from_dict(p) for p in data.get("pets", [])]
        return owner

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