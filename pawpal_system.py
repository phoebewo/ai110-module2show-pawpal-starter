from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str  # "low", "medium", "high"


@dataclass
class Pet:
    name: str
    species: str


@dataclass
class Owner:
    name: str
    pets: List[Pet] = field(default_factory=list)


@dataclass
class Constraints:
    available_minutes: int
    min_priority: str = "low"           # minimum priority to include
    preferred_first: List[str] = field(default_factory=list)  # task titles to prioritize


class DailyPlan:
    def __init__(self, owner: Owner, tasks: List[Task], constraints: Constraints):
        self.owner = owner
        self.tasks = tasks
        self.constraints = constraints
        self.scheduled: List[dict] = []

    def generate(self) -> List[dict]:
        """Filter, sort, and schedule tasks within the time budget."""
        pass

    def time_used(self) -> int:
        """Return total minutes of scheduled tasks."""
        pass

    def summary(self) -> str:
        """Return a human-readable plan with reasoning for each task."""
        pass
