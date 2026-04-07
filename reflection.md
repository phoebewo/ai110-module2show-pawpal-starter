# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

Three core actions: track tasks, schedule tasks, explain reason for task.

I chose Task, Pet, Owner, and Constraints to be the classes. Task represents an activity, how long it takes, and it's priority level. Pet represents the pet - it's name and species. Owner represents the owner - their name and their pets. Constraints represents the scheduling rules - the avaliable time and priority. THe DailyPlan class is the scheduler.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

DailyPlan had no link to Pet, but it should to know which pet its for, especially if the owner has more than one pet. Task had no link to Pet, but it should because some task are specific to only some pets.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The scheduler looks at three things: how much time is available, the priority of each task (low/medium/high), and a minimum priority cutoff so low-priority tasks can be filtered out. I decided priority mattered most because if time runs short, it makes more sense to drop a weekly grooming than a daily feeding. Time budget came second since that's the real-world limit a pet owner actually has.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

**Exact time match vs. overlapping duration detection**

detect_conflicts() only flags two tasks if they have the exact same time value. It won't catch a 30-minute task at 07:00 overlapping a task at 07:15, even though they'd actually run at the same time. Checking for real duration overlap would mean comparing every task's start and end time against every other task's, which gets complicated fast. For a pet care schedule with a small number of tasks in round time slots, exact-match is good enough to catch the obvious mistakes.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used Copilot across all three phases. In Phase 1 it helped brainstorm the class structure and identify missing relationships like Task needing a back-reference to Pet. In Phase 2 I used inline chat to generate method stubs and asked Agent Mode to implement the more involved logic like recurrence and conflict detection. In Phase 3 I used it to suggest Streamlit components for displaying filtered and sorted data. The most useful prompts were specific ones that included the file context — asking "based on #file:pawpal_system.py, what should this method return?" got much better answers than vague questions.

The most effective Copilot features were **inline chat** for single-method suggestions, **Agent Mode** for multi-file changes like wiring the scheduler into the UI, and **`#file:` context** for getting suggestions grounded in the actual code rather than generic examples.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

When asked how to simplify `detect_conflicts()`, Copilot suggested compressing the entire loop into a nested list comprehension — a generator inside a list comprehension across four lines. It was technically valid Python but harder to read and debug. I kept the explicit loop because the logic has two steps (group by time slot, then format the warning), and those steps are clearer on separate lines. The rule I applied: if I can't scan it in one pass and immediately understand what it does, the "Pythonic" version isn't worth it here.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I verified all four new methods by running `main.py` with intentional edge cases: tasks added out of order to confirm `sort_by_time()` corrected them, two tasks at identical times to trigger `detect_conflicts()`, and a mix of pets and statuses to check `filter_tasks()` combinations. Recurrence was tested by calling `mark_task_complete()` and confirming a new task appeared in the pet's list with the correct due date. These were important because the scheduler's output is only trustworthy if the underlying filters and sort are working correctly — a bug there would silently produce a wrong plan.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

Confident for the happy path. The cases I'd add next: a task whose `duration_minutes` is larger than `available_minutes` (it currently goes straight to skipped, which is correct, but worth an explicit test), an owner with no pets, and a weekly task completed multiple times in the same day to check that recurrence doesn't stack duplicate entries.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

The recurrence logic came together cleanly. Using `timedelta` to calculate the next due date and stamping it directly onto a new Task instance kept the design simple — no separate recurrence engine, just a method on the Task itself that knows how to produce its own successor.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I'd replace the exact time-match conflict detection with real duration-overlap checking, and I'd add persistent storage so tasks survive a page refresh in Streamlit. Right now everything resets when the session ends, which isn't practical for a real pet owner.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

AI is good at filling in the details but bad at knowing when to stop. Every suggestion it made was technically correct, but several added complexity that wasn't needed for this scale — a nested list comprehension, an O(n²) overlap check, extra abstraction layers. Being the lead architect meant deciding not just what to build, but what not to build. That judgment has to come from the human.
