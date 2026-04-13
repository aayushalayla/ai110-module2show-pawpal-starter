import streamlit as st
from datetime import datetime
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

if "owner" not in st.session_state:
    st.session_state["owner"] = Owner(
        name="Sam",
        email="sam@example.com",
        phone="123-456-7890"
    )

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
- View each pet's task list
- View today's, upcoming, and overdue tasks
"""
    )

st.divider()

st.subheader("Owner Info")
owner.name = st.text_input("Owner name", value=owner.name)
owner.email = st.text_input("Email", value=owner.email)
owner.phone = st.text_input("Phone", value=owner.phone)

st.divider()

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
            st.success(f"Task '{task_title}' added for {selected_pet.name}.")
        else:
            st.error("Please enter both a task title and description.")

    st.markdown(f"### Tasks for {selected_pet.name}")

    if selected_pet.tasks:
        for i, task in enumerate(selected_pet.tasks):
            col1, col2 = st.columns([4, 1])

            with col1:
                status = "completed" if task.is_completed else "pending"
                overdue_text = " | overdue" if task.is_overdue() else ""
                recurrence_text = f" | recurrence: {task.recurrence}" if task.recurrence else ""
                st.write(
                    f"- **{task.title}** | {task.description} | due {task.due_date.strftime('%Y-%m-%d %H:%M')} | {status}{overdue_text}{recurrence_text}"
                )

            with col2:
                if not task.is_completed:
                    if st.button("Complete", key=f"complete_{selected_pet.name}_{i}"):
                        task.mark_complete()
                        st.success(f"Marked '{task.title}' complete.")
                        st.rerun()
    else:
        st.info("No tasks for this pet yet.")
else:
    st.info("Add a pet first before scheduling tasks.")

st.divider()

st.subheader("Task Dashboard")

try:
    today_tasks = scheduler.get_today_tasks()
    upcoming_tasks = scheduler.get_upcoming_tasks()
    overdue_tasks = scheduler.get_overdue_tasks()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### Today")
        if today_tasks:
            for task in today_tasks:
                st.write(f"- {task.title} ({task.due_date.strftime('%H:%M')})")
        else:
            st.write("No tasks for today.")

    with col2:
        st.markdown("### Upcoming")
        if upcoming_tasks:
            for task in upcoming_tasks:
                st.write(f"- {task.title} ({task.due_date.strftime('%Y-%m-%d %H:%M')})")
        else:
            st.write("No upcoming tasks.")

    with col3:
        st.markdown("### Overdue")
        if overdue_tasks:
            for task in overdue_tasks:
                st.write(f"- {task.title} ({task.due_date.strftime('%Y-%m-%d %H:%M')})")
        else:
            st.write("No overdue tasks.")

except Exception:
    st.warning(
        "Your Scheduler methods may not be implemented yet. Once get_today_tasks(), "
        "get_upcoming_tasks(), and get_overdue_tasks() are finished, this dashboard will work."
    )