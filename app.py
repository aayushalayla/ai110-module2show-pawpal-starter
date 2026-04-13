import streamlit as st
from datetime import datetime
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

if "owner" not in st.session_state:
    st.session_state["owner"] = Owner.load_from_json("data.json")

owner = st.session_state["owner"]
scheduler = Scheduler(owner)

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to PawPal+.

This app helps a pet owner manage pets and their care tasks.
You can add pets, assign tasks, and view task lists.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.
"""
    )

with st.expander("What this version does", expanded=True):
    st.markdown(
        """
This version lets you:
- Add pets
- Add tasks to a selected pet
- View each pet's task list sorted chronologically
- Detect scheduling conflicts across all pets
- View today's, upcoming, and overdue tasks
- Filter tasks by pet or completion status
"""
    )

st.divider()

# ── Owner Info ────────────────────────────────────────────────────────────────
st.subheader("Owner Info")
owner.name = st.text_input("Owner name", value=owner.name)
owner.email = st.text_input("Email", value=owner.email)
owner.phone = st.text_input("Phone", value=owner.phone)

st.divider()

# ── Add a Pet ─────────────────────────────────────────────────────────────────
st.subheader("Add a Pet")

with st.form("add_pet_form"):
    pet_name = st.text_input("Pet name")
    pet_species = st.selectbox("Species", ["dog", "cat", "other"])
    pet_breed = st.text_input("Breed")
    pet_age = st.number_input("Age", min_value=0, max_value=50, value=1)
    add_pet_submitted = st.form_submit_button("Add Pet")

if add_pet_submitted:
    if pet_name.strip() and pet_breed.strip():
        new_pet = Pet(
            name=pet_name.strip(),
            species=pet_species,
            breed=pet_breed.strip(),
            age=int(pet_age)
        )
        owner.add_pet(new_pet)
        owner.save_to_json("data.json")
        st.success(f"{pet_name} added successfully.")
    else:
        st.error("Please enter both a pet name and breed.")

st.subheader("Current Pets")

if owner.pets:
    for pet in owner.pets:
        st.write(f"**{pet.name}** — {pet.species}, {pet.breed}, age {pet.age}")
else:
    st.info("No pets added yet.")

st.divider()

# ── Schedule a Task ───────────────────────────────────────────────────────────
st.subheader("Schedule a Task")

if owner.pets:
    pet_names = [pet.name for pet in owner.pets]
    selected_pet_name = st.selectbox("Choose a pet", pet_names)
    selected_pet = next(p for p in owner.pets if p.name == selected_pet_name)

    with st.form("add_task_form"):
        task_title = st.text_input("Task title")
        task_description = st.text_input("Description")
        task_due_date = st.date_input("Due date")
        task_due_time = st.time_input("Due time")
        task_recurrence = st.selectbox("Recurrence", ["none", "daily", "weekly"])
        add_task_submitted = st.form_submit_button("Add Task")

    if add_task_submitted:
        if task_title.strip() and task_description.strip():
            due_datetime = datetime.combine(task_due_date, task_due_time)
            recurrence_value = None if task_recurrence == "none" else task_recurrence

            new_task = Task(
                title=task_title.strip(),
                description=task_description.strip(),
                due_date=due_datetime,
                recurrence=recurrence_value
            )
            selected_pet.add_task(new_task)
            owner.save_to_json("data.json")
            st.success(f"Task '{task_title}' added for {selected_pet.name}.")
        else:
            st.error("Please enter both a task title and description.")

    # ── Per-pet task list (sorted chronologically) ────────────────────────────
    st.markdown(f"### Tasks for {selected_pet.name}")

    sorted_tasks = scheduler.sort_by_time(selected_pet.tasks)

    if sorted_tasks:
        for i, task in enumerate(sorted_tasks):
            with st.container():
                col1, col2 = st.columns([5, 1])

                with col1:
                    due_str = task.due_date.strftime("%Y-%m-%d %H:%M")
                    recur_badge = f"  `↻ {task.recurrence}`" if task.recurrence else ""

                    if task.is_completed:
                        st.success(
                            f"✅ **{task.title}** — {task.description}  \n"
                            f"Due: {due_str}{recur_badge}"
                        )
                    elif task.is_overdue():
                        st.error(
                            f"🔴 **{task.title}** — {task.description}  \n"
                            f"Due: {due_str}{recur_badge}"
                        )
                    else:
                        st.info(
                            f"📋 **{task.title}** — {task.description}  \n"
                            f"Due: {due_str}{recur_badge}"
                        )

                with col2:
                    if not task.is_completed:
                        if st.button("Complete", key=f"complete_{selected_pet.name}_{i}"):
                            task.mark_complete()
                            if task.recurrence in ("daily", "weekly"):
                                scheduler.create_recurring_task(task, selected_pet)
                                st.success(
                                    f"'{task.title}' marked complete. "
                                    f"Next {task.recurrence} occurrence scheduled."
                                )
                            else:
                                st.success(f"Marked '{task.title}' complete.")
                            owner.save_to_json("data.json")
                            st.rerun()
    else:
        st.info("No tasks for this pet yet.")

else:
    st.info("Add a pet first before scheduling tasks.")

st.divider()

# ── Conflict Warnings ─────────────────────────────────────────────────────────
st.subheader("⚠️ Conflict Checker")

conflicts = scheduler.detect_task_conflicts()
if conflicts:
    st.error(
        f"**{len(conflicts)} scheduling conflict(s) detected.** "
        "Two or more tasks are assigned to the same time slot. "
        "Reschedule one of the tasks below to avoid missing a care routine."
    )
    for warning in conflicts:
        st.warning(warning)
else:
    st.success("No scheduling conflicts — all tasks have unique time slots.")

st.divider()

# ── Task Dashboard ────────────────────────────────────────────────────────────
st.subheader("Task Dashboard")


def tasks_to_rows(tasks: list) -> list[dict]:
    """Convert a list of Task objects to plain dicts for st.table."""
    rows = []
    for task in tasks:
        pet_label = next(
            (p.name for p in owner.pets if task in p.tasks), "—"
        )
        rows.append({
            "Pet": pet_label,
            "Task": task.title,
            "Description": task.description,
            "Due": task.due_date.strftime("%Y-%m-%d %H:%M"),
            "Recurrence": task.recurrence or "—",
        })
    return rows


try:
    today_tasks = scheduler.get_today_tasks()
    upcoming_tasks = scheduler.get_upcoming_tasks()
    overdue_tasks = scheduler.get_overdue_tasks()

    # Overdue banner — most urgent, shown first
    if overdue_tasks:
        st.error(f"**{len(overdue_tasks)} overdue task(s)** need your attention.")
        st.table(tasks_to_rows(overdue_tasks))
    else:
        st.success("No overdue tasks — great job staying on schedule!")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Today")
        if today_tasks:
            st.table(tasks_to_rows(today_tasks))
        else:
            st.info("No tasks due today.")

    with col2:
        st.markdown("#### Upcoming")
        if upcoming_tasks:
            st.table(tasks_to_rows(upcoming_tasks))
        else:
            st.info("No upcoming tasks.")

except Exception:
    st.warning(
        "Your Scheduler methods may not be implemented yet. Once get_today_tasks(), "
        "get_upcoming_tasks(), and get_overdue_tasks() are finished, this dashboard will work."
    )

st.divider()

# ── Filter Tasks ──────────────────────────────────────────────────────────────
st.subheader("Filter Tasks")

filter_col1, filter_col2 = st.columns(2)

with filter_col1:
    all_pet_names = ["All pets"] + [p.name for p in owner.pets]
    filter_pet = st.selectbox("Filter by pet", all_pet_names, key="filter_pet")

with filter_col2:
    filter_status = st.selectbox(
        "Filter by status",
        ["All", "Pending", "Completed"],
        key="filter_status"
    )

pet_name_arg = None if filter_pet == "All pets" else filter_pet
completed_arg = None
if filter_status == "Pending":
    completed_arg = False
elif filter_status == "Completed":
    completed_arg = True

filtered = scheduler.filter_tasks(pet_name=pet_name_arg, is_completed=completed_arg)

if filtered:
    st.table(tasks_to_rows(filtered))
else:
    st.info("No tasks match the selected filters.")
