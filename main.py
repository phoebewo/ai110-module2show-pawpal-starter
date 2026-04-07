from pawpal_system import Task, Pet, Owner, Scheduler

# --- Setup ---
owner = Owner(name="Jordan")

mochi = Pet(name="Mochi", species="dog")
luna = Pet(name="Luna", species="cat")

# --- Tasks for Mochi (intentional clash: Grooming also at 08:00) ---
mochi.add_task(Task(description="Evening walk",   duration_minutes=30, frequency="daily",     priority="high",   time="18:00"))
mochi.add_task(Task(description="Morning walk",   duration_minutes=30, frequency="daily",     priority="high",   time="07:00"))
mochi.add_task(Task(description="Grooming",       duration_minutes=20, frequency="weekly",    priority="low",    time="08:00"))  # <-- clash with Feeding
mochi.add_task(Task(description="Feeding",        duration_minutes=10, frequency="daily",     priority="high",   time="08:00"))  # <-- clash with Grooming

# --- Tasks for Luna (intentional clash: Litter box also at 07:00) ---
luna.add_task(Task(description="Enrichment play", duration_minutes=15, frequency="as-needed", priority="medium", time="16:00"))
luna.add_task(Task(description="Feeding",         duration_minutes=10, frequency="daily",     priority="high",   time="12:00"))
luna.add_task(Task(description="Litter box",      duration_minutes=5,  frequency="daily",     priority="medium", time="07:00"))  # <-- clash with Mochi's Morning walk

# --- Add pets to owner ---
owner.add_pet(mochi)
owner.add_pet(luna)

# --- Schedule ---
scheduler = Scheduler(owner=owner, available_minutes=120, min_priority="low")
scheduler.generate()

all_tasks = owner.get_all_tasks()

# ── 1. Conflict Detection ────────────────────────────────────────────────────
print("=" * 50)
print("  CONFLICT DETECTION")
print("=" * 50)
conflicts = scheduler.detect_conflicts(all_tasks)
if conflicts:
    for warning in conflicts:
        print(f"  {warning}")
else:
    print("  No conflicts found.")

# ── 2. Sort ALL tasks by time ────────────────────────────────────────────────
print()
print("=" * 50)
print("  ALL TASKS SORTED BY TIME (chronological)")
print("=" * 50)
for task in scheduler.sort_by_time(all_tasks):
    status = "[done]" if task.completed else "[    ]"
    print(f"  {task.time}  {status}  [{task.pet_name:<6}]  {task.description}")

# ── 3. Filter: only Mochi's tasks ───────────────────────────────────────────
print()
print("=" * 50)
print("  MOCHI'S TASKS (sorted by time)")
print("=" * 50)
mochi_tasks = scheduler.filter_tasks(all_tasks, pet_name="Mochi")
for task in scheduler.sort_by_time(mochi_tasks):
    print(f"  {task.time}  [{task.priority:<6}]  {task.description}")

# ── 4. Filter: only Luna's tasks ────────────────────────────────────────────
print()
print("=" * 50)
print("  LUNA'S TASKS (sorted by time)")
print("=" * 50)
luna_tasks = scheduler.filter_tasks(all_tasks, pet_name="Luna")
for task in scheduler.sort_by_time(luna_tasks):
    print(f"  {task.time}  [{task.priority:<6}]  {task.description}")

# ── 5. Filter: pending tasks only ───────────────────────────────────────────
print()
print("=" * 50)
print("  PENDING TASKS ACROSS ALL PETS")
print("=" * 50)
pending = scheduler.filter_tasks(all_tasks, status="pending")
for task in scheduler.sort_by_time(pending):
    print(f"  {task.time}  [{task.pet_name:<6}]  {task.description}")

# ── 6. Mark tasks complete, then show completed filter ──────────────────────
mochi.tasks[1].mark_complete()   # Morning walk -> done
luna.tasks[1].mark_complete()    # Feeding -> done

print()
print("=" * 50)
print("  COMPLETED TASKS")
print("=" * 50)
completed = scheduler.filter_tasks(all_tasks, status="completed")
if completed:
    for task in scheduler.sort_by_time(completed):
        print(f"  {task.time}  [{task.pet_name:<6}]  {task.description}  [done]")
else:
    print("  (none yet)")

# ── 7. Schedule summary ──────────────────────────────────────────────────────
print()
print("=" * 50)
print("  TODAY'S SCHEDULE (priority-ordered)")
print("=" * 50)
print(scheduler.summary())
