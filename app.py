import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# --- Session state initialization ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="")

if "pet" not in st.session_state:
    st.session_state.pet = None

# --- Owner setup ---
st.subheader("Owner")
owner_name = st.text_input("Owner name", value=st.session_state.owner.name)
if owner_name:
    st.session_state.owner.name = owner_name

# --- Add a pet ---
st.subheader("Add a Pet")
col1, col2 = st.columns(2)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    new_pet = Pet(name=pet_name, species=species)
    st.session_state.owner.add_pet(new_pet)       # Owner.add_pet() handles this
    st.session_state.pet = new_pet                 # track most recently added pet
    st.success(f"Added {pet_name} the {species}!")

# show all pets currently registered
if st.session_state.owner.pets:
    st.caption("Registered pets: " + ", ".join(p.name for p in st.session_state.owner.pets))

st.divider()

# --- Add a task ---
st.subheader("Add a Task")

if not st.session_state.owner.pets:
    st.info("Add a pet first before adding tasks.")
else:
    pet_names = [p.name for p in st.session_state.owner.pets]
    selected_pet_name = st.selectbox("Assign task to", pet_names)
    selected_pet = next(p for p in st.session_state.owner.pets if p.name == selected_pet_name)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        task_desc = st.text_input("Task", value="Morning walk")
    with col2:
        duration = st.number_input("Minutes", min_value=1, max_value=240, value=20)
    with col3:
        frequency = st.selectbox("Frequency", ["daily", "weekly", "as-needed"])
    with col4:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    if st.button("Add task"):
        task = Task(description=task_desc, duration_minutes=int(duration),
                    frequency=frequency, priority=priority)
        selected_pet.add_task(task)                # Pet.add_task() handles this
        st.success(f"Added '{task_desc}' to {selected_pet.name}.")

    # show current tasks for selected pet
    pending = selected_pet.get_pending_tasks()
    if pending:
        st.write(f"Tasks for {selected_pet.name}:")
        st.table([
            {"task": t.description, "minutes": t.duration_minutes,
             "frequency": t.frequency, "priority": t.priority}
            for t in pending
        ])
    else:
        st.info(f"No tasks yet for {selected_pet.name}.")

st.divider()

# --- Generate schedule ---
st.subheader("Generate Schedule")
available = st.number_input("Available time (minutes)", min_value=10, max_value=480, value=60)
min_priority = st.selectbox("Minimum priority to include", ["low", "medium", "high"])

if st.button("Generate schedule"):
    if not st.session_state.owner.pets:
        st.warning("Add a pet and some tasks first.")
    else:
        scheduler = Scheduler(
            owner=st.session_state.owner,
            available_minutes=int(available),
            min_priority=min_priority
        )
        scheduler.generate()                       # Scheduler.generate() handles this
        st.success(f"Scheduled {len(scheduler.scheduled)} tasks.")
        st.text(scheduler.summary())               # Scheduler.summary() explains the plan
