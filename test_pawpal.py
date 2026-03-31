import pytest
from pawpal_system import Task, Pet, Owner, Scheduler, DailyPlan


def make_owner(available_minutes=120):
    pet = Pet(name="Mochi", species="dog", age_years=3)
    return Owner(name="Jordan", pet=pet, available_minutes=available_minutes)


# --- Task priority ordering ---

def test_high_priority_scheduled_before_low():
    owner = make_owner(60)
    tasks = [
        Task("Low task", 30, "low"),
        Task("High task", 30, "high"),
    ]
    plan = Scheduler(owner).build_plan(tasks)
    assert plan.scheduled[0].task.title == "High task"
    assert plan.scheduled[1].task.title == "Low task"


def test_medium_priority_between_high_and_low():
    owner = make_owner(90)
    tasks = [
        Task("Low task", 30, "low"),
        Task("Medium task", 30, "medium"),
        Task("High task", 30, "high"),
    ]
    plan = Scheduler(owner).build_plan(tasks)
    titles = [st.task.title for st in plan.scheduled]
    assert titles == ["High task", "Medium task", "Low task"]


# --- Time constraint ---

def test_task_skipped_when_no_time_left():
    owner = make_owner(30)
    tasks = [
        Task("Walk", 20, "high"),
        Task("Bath", 20, "medium"),
    ]
    plan = Scheduler(owner).build_plan(tasks)
    assert len(plan.scheduled) == 1
    assert plan.scheduled[0].task.title == "Walk"
    assert len(plan.skipped) == 1
    assert plan.skipped[0].title == "Bath"


def test_all_tasks_fit_exactly():
    owner = make_owner(60)
    tasks = [
        Task("Feed", 20, "high"),
        Task("Walk", 20, "medium"),
        Task("Play", 20, "low"),
    ]
    plan = Scheduler(owner).build_plan(tasks)
    assert len(plan.scheduled) == 3
    assert len(plan.skipped) == 0
    assert plan.total_minutes_used == 60


def test_empty_task_list_produces_empty_plan():
    owner = make_owner(120)
    plan = Scheduler(owner).build_plan([])
    assert plan.scheduled == []
    assert plan.skipped == []
    assert plan.total_minutes_used == 0


# --- Time labels ---

def test_scheduled_task_time_label():
    owner = make_owner(120)
    tasks = [Task("Morning walk", 30, "high")]
    plan = Scheduler(owner, start_minute=480).build_plan(tasks)  # 8:00 AM
    label = plan.scheduled[0].time_label()
    assert "8:00 AM" in label
    assert "8:30 AM" in label


# --- Low-priority skipped before medium when time is tight ---

def test_low_priority_skipped_before_medium():
    owner = make_owner(40)
    tasks = [
        Task("Low task", 30, "low"),
        Task("Medium task", 30, "medium"),
    ]
    plan = Scheduler(owner).build_plan(tasks)
    assert plan.scheduled[0].task.title == "Medium task"
    assert plan.skipped[0].title == "Low task"


# --- Plan explanation ---

def test_plan_explain_contains_task_names():
    owner = make_owner(60)
    tasks = [Task("Feed", 20, "high"), Task("Walk", 40, "medium")]
    plan = Scheduler(owner).build_plan(tasks)
    explanation = plan.explain()
    assert "Feed" in explanation
    assert "Walk" in explanation


def test_plan_explain_mentions_skipped():
    owner = make_owner(20)
    tasks = [Task("Walk", 20, "high"), Task("Bath", 30, "medium")]
    plan = Scheduler(owner).build_plan(tasks)
    explanation = plan.explain()
    assert "Bath" in explanation
    assert "Skipped" in explanation
