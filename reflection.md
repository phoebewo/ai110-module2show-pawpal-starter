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

`detect_conflicts()` only flags two tasks if they have the exact same `time` value. It won't catch a 30-minute task at `07:00` overlapping a task at `07:15`, even though they'd actually run at the same time. Checking for real duration overlap would mean comparing every task's start and end time against every other task's, which gets complicated fast. For a pet care schedule with a small number of tasks in round time slots, exact-match is good enough to catch the obvious mistakes.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
