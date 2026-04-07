# PawPal+ UML Class Diagram

> Updated to match final `pawpal_system.py` implementation.

```mermaid
classDiagram

    %% ── Data classes ─────────────────────────────────────────────────────────

    class Task {
        +str description
        +int duration_minutes
        +str frequency
        +str priority
        +bool completed
        +str time
        +str pet_name
        +date due_date
        +date completed_date
        +mark_complete()
        +reset()
        +next_occurrence() Task
    }

    class Pet {
        +str name
        +str species
        +List~Task~ tasks
        +add_task(task: Task)
        +get_pending_tasks() List~Task~
    }

    class Owner {
        +str name
        +List~Pet~ pets
        +add_pet(pet: Pet)
        +get_pet(name: str) Pet
        +get_all_tasks() List~Task~
        +get_all_pending_tasks() List~Task~
    }

    %% ── Scheduler ────────────────────────────────────────────────────────────

    class Scheduler {
        +Owner owner
        +int available_minutes
        +str min_priority
        +List~Task~ scheduled
        +List~Task~ skipped
        +generate() List~Task~
        +mark_task_complete(task: Task) Task
        +sort_by_time(tasks: List~Task~) List~Task~
        +filter_tasks(tasks, pet_name, status) List~Task~
        +detect_conflicts(tasks: List~Task~) List~str~
        +time_used() int
        +summary() str
    }

    %% ── Relationships ────────────────────────────────────────────────────────

    %% Owner owns its pets (composition: pets cannot exist without an Owner)
    Owner "1" *-- "0..*" Pet : owns

    %% Pet owns its tasks (composition: tasks are stored on a Pet)
    Pet "1" *-- "0..*" Task : owns

    %% Scheduler holds a reference to an Owner (association, not ownership)
    Scheduler "1" --> "1" Owner : schedules for

    %% Task.next_occurrence() produces a new Task (self-dependency)
    Task ..> Task : next_occurrence() creates
```

---

## What changed from the initial design

| Area | Initial design | Final implementation |
|---|---|---|
| `Task` fields | `description`, `duration_minutes`, `frequency`, `priority`, `completed` | Added `time`, `pet_name`, `due_date`, `completed_date` |
| `Task` methods | `mark_complete()`, `reset()` | Added `next_occurrence()` — spawns the next recurring instance |
| `Pet.add_task()` | Added task to list | Now also stamps `task.pet_name = self.name` |
| `Owner` methods | `add_pet()`, `get_all_tasks()`, `get_all_pending_tasks()` | Added `get_pet(name)` — used by Scheduler to look up a pet by name |
| `Scheduler` methods | `generate()`, `time_used()`, `summary()` | Added `mark_task_complete()`, `sort_by_time()`, `filter_tasks()`, `detect_conflicts()` |
| `Scheduler → Owner` | Unnamed association | Explicit — Scheduler holds an `owner` reference and delegates pet lookup to it |
| `Task → Task` | Not modelled | Added self-dependency arrow for `next_occurrence()` |
| Module constants | `PRIORITY_RANK` | Added `RECURRENCE_DAYS` to drive timedelta logic |
