from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Dict, List, Optional


PRIORITY_RANK = {"low": 1, "medium": 2, "high": 3}

# How many days until the next occurrence for each frequency type.
RECURRENCE_DAYS = {"daily": 1, "weekly": 7}


@dataclass
class Task:
    """Represents a single pet care activity."""
    description: str
    duration_minutes: int
    frequency: str                        # "daily", "weekly", "as-needed"
    priority: str                         # "low", "medium", "high"
    completed: bool = False
    time: str = "00:00"                   # Scheduled time in "HH:MM" format (24-hour)
    pet_name: str = ""                    # Name of the pet this task belongs to
    due_date: Optional[date] = None       # Date this occurrence is due
    completed_date: Optional[date] = None # Date this occurrence was completed

    def mark_complete(self):
        """Mark this task as completed and record today as the completion date."""
        self.completed = True
        self.completed_date = date.today()

    def reset(self):
        """Reset this task to incomplete."""
        self.completed = False
        self.completed_date = None

    def next_occurrence(self) -> Optional["Task"]:
        """Return a new Task for the next recurrence of this one, or None.

        Calculates the next due date with timedelta:
          - ``daily``     → today + timedelta(days=1)
          - ``weekly``    → today + timedelta(days=7)
          - ``as-needed`` → returns None (no automatic recurrence)

        Returns:
            A fresh Task with the same fields and an updated ``due_date``,
            or None when the frequency does not repeat on a fixed schedule.
        """
        if self.frequency not in RECURRENCE_DAYS:
            return None

        days_ahead = RECURRENCE_DAYS[self.frequency]
        next_due = date.today() + timedelta(days=days_ahead)

        return Task(
            description=self.description,
            duration_minutes=self.duration_minutes,
            frequency=self.frequency,
            priority=self.priority,
            time=self.time,
            pet_name=self.pet_name,
            due_date=next_due,
        )


@dataclass
class Pet:
    """Stores pet details and owns a list of tasks."""
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a task to this pet's task list and stamp the pet name on it."""
        task.pet_name = self.name
        self.tasks.append(task)

    def get_pending_tasks(self) -> List[Task]:
        """Return tasks that have not been completed."""
        return [t for t in self.tasks if not t.completed]


@dataclass
class Owner:
    """Manages multiple pets and provides access to all their tasks."""
    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet):
        """Add a pet to this owner's pet list."""
        self.pets.append(pet)

    def get_pet(self, name: str) -> Optional[Pet]:
        """Return the first pet whose name matches (case-insensitive), or None."""
        for pet in self.pets:
            if pet.name.lower() == name.lower():
                return pet
        return None

    def get_all_tasks(self) -> List[Task]:
        """Return every task across all pets."""
        return [task for pet in self.pets for task in pet.tasks]

    def get_all_pending_tasks(self) -> List[Task]:
        """Return incomplete tasks across all pets."""
        return [task for pet in self.pets for task in pet.get_pending_tasks()]


class Scheduler:
    """Retrieves, organizes, and manages tasks across all of an owner's pets."""

    def __init__(self, owner: Owner, available_minutes: int, min_priority: str = "low"):
        self.owner = owner
        self.available_minutes = available_minutes
        self.min_priority = min_priority
        self.scheduled: List[Task] = []
        self.skipped: List[Task] = []

    def generate(self) -> List[Task]:
        """Filter by min priority, sort by priority (high first), fit into time budget."""
        pending = self.owner.get_all_pending_tasks()

        eligible = [
            t for t in pending
            if PRIORITY_RANK[t.priority] >= PRIORITY_RANK[self.min_priority]
        ]

        sorted_tasks = sorted(eligible, key=lambda t: -PRIORITY_RANK[t.priority])

        self.scheduled = []
        self.skipped = []
        time_used = 0

        for task in sorted_tasks:
            if time_used + task.duration_minutes <= self.available_minutes:
                self.scheduled.append(task)
                time_used += task.duration_minutes
            else:
                self.skipped.append(task)

        return self.scheduled

    def mark_task_complete(self, task: Task) -> Optional[Task]:
        """Mark a task done and register its next occurrence on the owning pet.

        Calls ``task.mark_complete()``, then calls ``task.next_occurrence()``
        to produce a follow-up Task.  The follow-up is added directly to the
        matching Pet so it appears in future calls to ``generate()``.

        Args:
            task: The Task to complete.  ``task.pet_name`` must match a pet
                  registered on this Scheduler's owner.

        Returns:
            The newly created follow-up Task, or None when
            ``task.frequency == "as-needed"`` (no recurrence needed).
        """
        task.mark_complete()

        next_task = task.next_occurrence()
        if next_task is None:
            return None

        # Re-register on the owning pet so it appears in future schedules.
        pet = self.owner.get_pet(task.pet_name)
        if pet is not None:
            pet.add_task(next_task)

        return next_task

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Return tasks sorted chronologically by their ``time`` field.

        Zero-padded ``"HH:MM"`` strings compare correctly with Python's default
        string ordering, so no datetime parsing is required.

        Args:
            tasks: Any list of Task objects.

        Returns:
            A new list sorted ascending by ``task.time`` (earliest first).
        """
        return sorted(tasks, key=lambda t: t.time)

    def filter_tasks(
        self,
        tasks: List[Task],
        pet_name: str = None,
        status: str = "all",
    ) -> List[Task]:
        """Filter tasks by pet name and/or completion status.

        Filters are applied together — both conditions must pass for a task
        to be included.  Omitting a filter leaves that dimension unrestricted.

        Args:
            tasks:    The list of Task objects to filter.
            pet_name: Case-insensitive pet name to match.  Pass ``None``
                      (default) to include tasks for all pets.
            status:   ``"pending"``   — incomplete tasks only.
                      ``"completed"`` — completed tasks only.
                      ``"all"``       — no status filter (default).

        Returns:
            A new list containing every task that satisfies all active filters.
        """
        result = tasks

        if pet_name is not None:
            result = [t for t in result if t.pet_name.lower() == pet_name.lower()]

        if status == "pending":
            result = [t for t in result if not t.completed]
        elif status == "completed":
            result = [t for t in result if t.completed]

        return result

    def detect_conflicts(self, tasks: List[Task]) -> List[str]:
        """Detect time-slot conflicts and return warning strings.

        Groups tasks by their exact ``time`` value.  Any slot with two or more
        tasks is reported as a conflict, whether the tasks belong to the same
        pet or different pets.  No exceptions are raised — the return value is
        always a list (empty when the schedule is clean).

        Args:
            tasks: The list of Task objects to inspect.

        Returns:
            A sorted list of human-readable warning strings, one per
            conflicting time slot.  Empty list means no conflicts found.
        """
        # Build a dict mapping each time slot to the tasks scheduled there.
        slots: Dict[str, List[Task]] = defaultdict(list)
        for task in tasks:
            slots[task.time].append(task)

        warnings = []
        for time_slot, slot_tasks in sorted(slots.items()):
            if len(slot_tasks) > 1:
                names = ", ".join(
                    f"{t.pet_name}: {t.description}" for t in slot_tasks
                )
                warnings.append(
                    f"WARNING: Conflict at {time_slot} — {len(slot_tasks)} tasks overlap: {names}"
                )

        return warnings

    def time_used(self) -> int:
        """Return total minutes across scheduled tasks."""
        return sum(t.duration_minutes for t in self.scheduled)

    def summary(self) -> str:
        """Return a human-readable plan with reasoning."""
        if not self.scheduled:
            return "No tasks could be scheduled."

        lines = [f"Daily plan for {self.owner.name}:"]
        for i, task in enumerate(self.scheduled, 1):
            lines.append(
                f"  {i}. {task.description} — {task.duration_minutes} min "
                f"[{task.priority} priority, {task.frequency}]"
            )
        lines.append(f"\nTotal time: {self.time_used()} / {self.available_minutes} min")

        if self.skipped:
            lines.append("\nSkipped (over time budget):")
            for task in self.skipped:
                lines.append(f"  • {task.description} ({task.duration_minutes} min)")

        return "\n".join(lines)
