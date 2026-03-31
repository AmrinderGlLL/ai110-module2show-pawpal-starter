import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")
st.caption("Daily pet care planner — enter your info, add tasks, and generate a schedule.")

st.divider()

# --- Owner & Pet Info ---
st.subheader("Owner & Pet")
col1, col2 = st.columns(2)
with col1:
    owner_name = st.text_input("Owner name", value="Jordan")
    available_minutes = st.number_input(
        "Time available today (minutes)", min_value=10, max_value=480, value=120, step=10
    )
with col2:
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    pet_age = st.number_input("Pet age (years)", min_value=0.0, max_value=30.0, value=3.0, step=0.5)

st.divider()

# --- Task Management ---
st.subheader("Tasks")

if "tasks" not in st.session_state:
    st.session_state.tasks = [
        {"title": "Morning walk", "duration_minutes": 30, "priority": "high", "category": "exercise"},
        {"title": "Feeding", "duration_minutes": 10, "priority": "high", "category": "nutrition"},
        {"title": "Grooming", "duration_minutes": 20, "priority": "medium", "category": "grooming"},
    ]

with st.expander("Add a task", expanded=True):
    col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
    with col1:
        task_title = st.text_input("Task title", value="Playtime")
    with col2:
        duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=15)
    with col3:
        priority = st.selectbox("Priority", ["high", "medium", "low"], index=1)
    with col4:
        category = st.selectbox("Category", ["exercise", "nutrition", "grooming", "enrichment", "medical", "general"])

    if st.button("Add task"):
        st.session_state.tasks.append(
            {
                "title": task_title,
                "duration_minutes": int(duration),
                "priority": priority,
                "category": category,
            }
        )
        st.success(f"Added: {task_title}")

if st.session_state.tasks:
    st.write(f"**{len(st.session_state.tasks)} task(s) queued:**")
    st.table(st.session_state.tasks)

    to_remove = st.selectbox(
        "Remove a task",
        options=["(none)"] + [t["title"] for t in st.session_state.tasks],
    )
    if st.button("Remove selected task") and to_remove != "(none)":
        st.session_state.tasks = [t for t in st.session_state.tasks if t["title"] != to_remove]
        st.rerun()
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# --- Schedule Generation ---
st.subheader("Generate Schedule")

start_hour = st.slider("Day starts at (hour)", min_value=5, max_value=12, value=8)

if st.button("Generate schedule", type="primary"):
    if not st.session_state.tasks:
        st.warning("Add at least one task before generating a schedule.")
    else:
        pet = Pet(name=pet_name, species=species, age_years=float(pet_age))
        owner = Owner(name=owner_name, pet=pet, available_minutes=int(available_minutes))
        tasks = [
            Task(
                title=t["title"],
                duration_minutes=t["duration_minutes"],
                priority=t["priority"],
                category=t.get("category", "general"),
            )
            for t in st.session_state.tasks
        ]

        scheduler = Scheduler(owner, start_minute=start_hour * 60)
        plan = scheduler.build_plan(tasks)

        st.success(f"Schedule built for {owner_name} & {pet_name}!")

        if plan.scheduled:
            st.markdown("### Daily Plan")
            for st_task in plan.scheduled:
                badge = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(st_task.task.priority, "⚪")
                st.markdown(
                    f"{badge} **{st_task.task.title}** &nbsp; `{st_task.time_label()}` &nbsp; "
                    f"_{st_task.task.duration_minutes} min · {st_task.task.category}_"
                )

        if plan.skipped:
            st.markdown("### Skipped (not enough time)")
            for t in plan.skipped:
                st.markdown(f"- ~~{t.title}~~ ({t.duration_minutes} min, {t.priority} priority)")

        st.markdown("### Explanation")
        st.code(plan.explain(), language=None)

        used_pct = plan.total_minutes_used / plan.total_minutes_available
        st.progress(min(used_pct, 1.0), text=f"{plan.total_minutes_used} / {plan.total_minutes_available} min used")
