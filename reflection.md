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

The initial UML uses four classes. An `Owner` holds pets and can gather their tasks; each `Pet` holds its own details and tasks. A `Task` describes a care activity, including its due date and time, duration, priority, frequency, and completion status. A `Scheduler` accesses the owner to organize tasks, detect conflicts, handle completion and recurrence, and build a daily plan. This keeps the user interface separate from the care and scheduling logic.

**b. Design changes**

The draft diagram was translated into class skeletons without a structural change: the scheduler reaches tasks through the owner and pets, rather than maintaining a second task list. The task model includes a full date and time as well as duration and priority so that future recurrence and daily planning have the information they need.

A review identified several decisions that the implementation now addresses: name filtering matches all pets with the same name, completion checks that the task belongs to the supplied pet, and completing an occurrence twice does not create duplicates. Conflicts compare full dates and start times; overlapping durations remain a limitation.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The daily planner considers the selected date, completion status, task priority, duration, and a total time budget. It chooses higher-priority tasks first, then returns the selected tasks in chronological order. Owner preferences are stored but not used yet.

**b. Tradeoffs**

Conflict detection checks exact date-and-start-time matches, rather than overlapping durations. This is straightforward for an initial scheduler but can miss a task starting before another ends; users need to review the schedule until overlap detection is added. Recurring tasks are scheduled one or seven days after completion, even when the original task is overdue.

The conflict method was reviewed for readability: `itertools.combinations` expresses each unique pair directly and avoids manually managing nested indexes. It remains a pairwise comparison, which is appropriate for a small set of pet-care tasks but grows quadratically as the list grows.

---

## 3. AI Collaboration

**a. How you used AI**

Codex helped break down the assignment, brainstorm the classes, create the UML and skeleton, implement the scheduler and interface, and write and run tests. Requests focused on one project phase at a time made the work and its outputs easier to review. All phases were discussed in the same chat rather than in separate chats; using separate sessions might have made the design, algorithms, and testing discussions easier to locate.

**b. Judgment and verification**

The AI program worked well and seemed to keep all the classes and ideas we had intact. However, I do think that it got too many extra ideas that I had to keep it on track and make sure the AI kept everything simple.

---

## 4. Testing and Verification

**a. What you tested**

The test suite checks task addition and completion, chronological sorting, pet and status filters, daily and weekly recurrence, duplicate completion, conflict detection, ownership, empty schedules, priority-based planning, and a Streamlit add-and-complete workflow. These checks cover both ordinary use and cases that could otherwise silently create an incorrect schedule.

**b. Confidence**

I think I give it a confidence rating of 4/5.

---

## 5. Reflection

**a. What went well**

The working CLI demonstration and automated tests make the scheduler's behavior easier to inspect independently of the interface. Working with the AI assistant was smooth and made sure that the program and code all went smoothly. It was very easy and convenient to change certain things and add little flourishes.

**b. What you would improve**

Add durable storage, detect overlapping durations, and make the planner resolve conflicts while considering owner preferences.

**c. Key takeaway**

I think this was a good project to see how it was building a system from the ground up with an AI, it was more stress free and saved a lot more time than if I did by myself by hand.
