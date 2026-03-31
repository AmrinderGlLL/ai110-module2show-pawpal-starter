from dataclasses import dataclass, field
from typing import Optional


PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str  # "high", "medium", "low"
    category: str = "general"
    notes: str = ""

    def priority_value(self) -> int:
        return PRIORITY_ORDER.get(self.priority, 99)


@dataclass
class Pet:
    name: str
    species: str  # "dog", "cat", "other"
    age_years: Optional[float] = None


@dataclass
class Owner:
    name: str
    pet: Pet
    available_minutes: int = 120  # total time available per day
    preferences: list[str] = field(default_factory=list)  # e.g. ["prefer morning walks"]


@dataclass
class ScheduledTask:
    task: Task
    start_minute: int  # minutes from start of day (e.g. 480 = 8:00 AM)

    @property
    def end_minute(self) -> int:
        return self.start_minute + self.task.duration_minutes

    def time_label(self) -> str:
        def fmt(m: int) -> str:
            h, mn = divmod(m, 60)
            period = "AM" if h < 12 else "PM"
            h = h % 12 or 12
            return f"{h}:{mn:02d} {period}"
        return f"{fmt(self.start_minute)} – {fmt(self.end_minute)}"


@dataclass
class DailyPlan:
    scheduled: list[ScheduledTask]
    skipped: list[Task]
    total_minutes_used: int
    total_minutes_available: int

    def explain(self) -> str:
        lines = []
        lines.append(
            f"Scheduled {len(self.scheduled)} task(s) using "
            f"{self.total_minutes_used} of {self.total_minutes_available} available minutes.\n"
        )
        if self.scheduled:
            lines.append("Included tasks (ordered by priority, then fitted to available time):")
            for st in self.scheduled:
                lines.append(
                    f"  • [{st.task.priority.upper()}] {st.task.title} "
                    f"({st.task.duration_minutes} min) — {st.time_label()}"
                )
        if self.skipped:
            lines.append("\nSkipped tasks (not enough time remaining):")
            for t in self.skipped:
                lines.append(f"  • {t.title} ({t.duration_minutes} min, {t.priority} priority)")
        return "\n".join(lines)


class Scheduler:
    """
    Greedy scheduler: sorts tasks by priority (high → medium → low),
    then fits them into the owner's available time window starting at
    start_minute (default 8:00 AM = 480).
    """

    def __init__(self, owner: Owner, start_minute: int = 480):
        self.owner = owner
        self.start_minute = start_minute

    def build_plan(self, tasks: list[Task]) -> DailyPlan:
        sorted_tasks = sorted(tasks, key=lambda t: (t.priority_value(), t.title))

        scheduled: list[ScheduledTask] = []
        skipped: list[Task] = []
        time_used = 0
        cursor = self.start_minute

        for task in sorted_tasks:
            if time_used + task.duration_minutes <= self.owner.available_minutes:
                scheduled.append(ScheduledTask(task=task, start_minute=cursor))
                cursor += task.duration_minutes
                time_used += task.duration_minutes
            else:
                skipped.append(task)

        return DailyPlan(
            scheduled=scheduled,
            skipped=skipped,
            total_minutes_used=time_used,
            total_minutes_available=self.owner.available_minutes,
        )
