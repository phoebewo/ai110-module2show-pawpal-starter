# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Smarter Scheduling

Four algorithmic improvements were added to `pawpal_system.py` beyond the base scheduler:

**Sort by time** — `Scheduler.sort_by_time(tasks)`
Returns tasks in chronological order using a `lambda` key on the `"HH:MM"` time field. Zero-padded strings sort correctly without any datetime parsing.

**Filter by pet or status** — `Scheduler.filter_tasks(tasks, pet_name, status)`
Filters a task list by pet name (case-insensitive) and/or completion status (`"pending"`, `"completed"`, `"all"`). Both filters can be combined in a single call.

**Recurring tasks** — `Task.next_occurrence()` + `Scheduler.mark_task_complete(task)`
When a `"daily"` or `"weekly"` task is marked complete, `timedelta` calculates the next due date (today + 1 or + 7 days) and a fresh Task is automatically added back to the pet's list. `"as-needed"` tasks are left as-is.

**Conflict detection** — `Scheduler.detect_conflicts(tasks)`
Checks for tasks assigned to the exact same time slot and returns a list of warning strings — one per conflicting slot — without crashing the program. Works across pets and within the same pet.

---

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
