# PawPal+ UML Diagram

```
┌─────────────────────────────┐
│            Owner            │
├─────────────────────────────┤
│ - name: str                 │
│ - pet: Pet                  │
│ - available_minutes: int    │
│ - preferences: list[str]    │
└─────────────────────────────┘
         │ has one
         ▼
┌─────────────────────────────┐
│             Pet             │
├─────────────────────────────┤
│ - name: str                 │
│ - species: str              │
│ - age_years: float          │
└─────────────────────────────┘


┌─────────────────────────────┐
│            Task             │
├─────────────────────────────┤
│ - title: str                │
│ - duration_minutes: int     │
│ - priority: str             │
│ - category: str             │
│ - notes: str                │
├─────────────────────────────┤
│ + priority_value(): int     │
└─────────────────────────────┘


┌─────────────────────────────┐
│         Scheduler           │
├─────────────────────────────┤
│ - owner: Owner              │
│ - start_minute: int         │
├─────────────────────────────┤
│ + build_plan(tasks): Plan   │
└─────────────────────────────┘
         │ produces
         ▼
┌─────────────────────────────┐
│          DailyPlan          │
├─────────────────────────────┤
│ - scheduled: list[Sched..] │
│ - skipped: list[Task]       │
│ - total_minutes_used: int   │
│ - total_minutes_available:  │
│   int                       │
├─────────────────────────────┤
│ + explain(): str            │
└─────────────────────────────┘
         │ contains
         ▼
┌─────────────────────────────┐
│       ScheduledTask         │
├─────────────────────────────┤
│ - task: Task                │
│ - start_minute: int         │
├─────────────────────────────┤
│ + end_minute: int           │
│ + time_label(): str         │
└─────────────────────────────┘
```

## Relationships

- `Owner` **has one** `Pet`
- `Scheduler` **takes** `Owner` + `list[Task]` → produces `DailyPlan`
- `DailyPlan` **contains** a list of `ScheduledTask` and a list of skipped `Task`
- `ScheduledTask` **wraps** one `Task` with a start time
