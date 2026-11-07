# PawPal+ Project Reflection

## 1. System Design

**Three core user actions**

1. Add a pet and its basic details to an owner's profile.
2. Schedule a care task for a pet, such as a feeding, walk, or medication.
3. View the day's care tasks in a clear schedule.

**Building blocks (initial brainstorm)**

These are proposed attributes and methods; they may change as the design and implementation develop.

- **Owner** represents the person responsible for care. It holds a name, preferences, and a list of pets. It can add a pet and retrieve tasks across its pets.
- **Pet** represents an animal receiving care. It holds a name, species, optional details, and a list of its tasks. It can add a task and provide its current tasks.
- **Task** represents one care activity. It holds a description, due date and time, duration, priority, frequency (once, daily, or weekly), and completion status. It can be marked complete; recurring tasks will need a next occurrence.
- **Scheduler** organizes an owner's care tasks. It can collect tasks from the owner's pets, sort them by date and time, filter by pet or completion status, flag conflicts, and build a daily plan using available time and priority. It can coordinate completion and creation of the next recurring occurrence.

An owner can have multiple pets, and each pet can have multiple tasks. The scheduler uses the owner to reach those pets and their tasks. A task belongs to the pet whose care it describes.

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

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
