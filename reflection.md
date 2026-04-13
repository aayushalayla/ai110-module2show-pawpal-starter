# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.

Three Core Actions: 
User (owner who can add pets)
Pet (type of pet)
Scheduler - Tasks for the User (feedings, walks, medications, and appointments)

The Owner owns the Pet and each Pet has Tasks associated with it. 
The Scheduler manages the Tasks altogether for each pet. 

- What classes did you include, and what responsibilities did you assign to each?

The initial UML design included four core classes:
Owner holds the attributes name, email, phone, and a list of pets.
Its methods are add_pet(), remove_pet(), and get_all_tasks().

Pet holds the attributes name, species, breed, age, and a list of tasks.
Its methods are add_task(), get_pending_tasks(), and get_completed_tasks().

Task holds title, description, due_date, is_completed, and recurrence. 
Its methods are mark_complete(), is_overdue(), and reschedule().

Scheduler holds a list of tasks. 
Its methods are add_task(), remove_task(), get_today_tasks(), get_upcoming_tasks(), and get_overdue_tasks().

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

I changed the scheduler class so it no longer stores its own separate tasks list. 
Scheduler now references an Owner and gathers tasks through the owner's pets. 
This change avoids duplicates. 
In the earlier design, tasks were in both Pet and Scheduler which would be difficuly to maintain. 
The revised design makes the relationship clearer. 
Owner owns pet. Pet owns Task. Scheduler is responsible for organizing and filtering tasks rather than owning them directly. 
I kept 'remove_pet(pet_name).' 
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?
My scheduler mainly considers time, completion status, pet association, recurrence, and task conflicts. 
Time is used to sort tasks in chronological order, completion status determines whether a task should still appear in active schedules, 
pet association allows the owner to filter care by animal, recurrence supports repeated routines such as feedings or medications, 
and conflict detection helps identify overlapping tasks.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
time mattered most because a scheduler is useless if it cannot order tasks
completion status mattered next because the owner needs to distinguish active tasks from finished ones
pet association mattered because the app supports multiple pets

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
It was most helpful in responding to ideas I already had or were described in the assignment. 
- What kinds of prompts or questions were most helpful?
The more specific they were the more helpful they were. The explanations were also useful in justifying the choices. 

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
Sometimes the AI suggestions were too complex for the scale of this project. 
The tradeoff waws between understandable code and less efficent methods for larger task lists. 

- How did you evaluate or verify what the AI suggested?
I tested it and worked backwards from the logic of a user using the app. 

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested two core unit-level behaviors and also verified the overall workflow through a demo script. First, I tested task completion by checking that mark_complete() correctly changes a task’s status from incomplete to complete. This was important because many parts of the scheduler depend on whether a task is still active, including overdue checks, filtering, and schedule views.

Second, I tested task addition by verifying that adding a Task to a Pet increases the number of tasks stored for that pet. This was important because the entire system depends on tasks being correctly attached to pets before they can be retrieved and organized by the Owner and Scheduler.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?
I am moderately confident that the scheduler works correctly.
If I had more time, I would test several additional edge cases: tasks due exactly at the current time, multiple recurring tasks created in sequence, duplicate pet names, pets with no tasks, and cases where completed recurring tasks should generate a new occurrence without remaining in active schedule views. I would also test conflict detection more thoroughly, especially when more than two tasks share the same due time.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
The part I am most satisfied with is the way the system architecture became clearer over time. The final design gives each class a distinct responsibility.
**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
If I had another iteration, I would improve the recurrence system and the overall robustness of task identification.
**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
AI was helpful for scaffolding class skeletons, suggesting algorithms, and drafting tests, but I still had to evaluate whether those suggestions actually fit the scale and goals of the project.
