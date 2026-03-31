# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

Started with Task, Pet, and a "PlanBuilder" class. Task held the core attributes,
Pet held owner info too which was a mistake. Drew it out on paper first and the
relationships became obvious once I had the arrows down.

**b. Design changes**

Split Owner and Pet early — having `owner_name` on Pet felt backwards.
Also added `DailyPlan` as its own dataclass instead of returning a raw list,
needed a clean place for `explain()` and the skipped tasks.

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

Priority first, then available time. High priority tasks always go in before medium or low —
you don't skip a dog's meds because a walk fits better. Within the same priority level,
tasks are sorted alphabeticaly to keep output deterministc.

**b. Tradeoffs**

Greedy approach can waste time — a high-priority 55-min task eats up the slot even if
two smaller tasks wouldve fit. Reasonable tradeoff here bc pet care priorities are real,
conveinence doesn't override them.

## 3. AI Collaboration

**a. How you used AI**

Used it mainly for early structural decisions like "does Scheduler belong on Owner or stand alone?"
Specific prompts worked way better than vague ones — asking about tradeoffs got useful answers,
asking "help me design this" got nothing.

**b. Judgment and verification**

AI suggested making priority a numeric field (1–5). Didn't go with it — the UI already used
"high/medium/low" strings and converting back and forth was unnecessery. Checked by tracing
where priority was used across the whole codebase before deciding.

## 4. Testing and Verification

**a. What you tested**

Priority ordering, time constraints, empty task list, time label formatting, and explain() output.
If priority and time handling break, nothing else matters.

**b. Confidence**

Pretty confident in the core paths. Would add next: identical task titles breaking removal,
tasks longer than total available time, and time labels for  post-noon schedules.

## 5. Reflection

**a. What went well**

The data/logic separation worked out well. `DailyPlan.explain()` ended up being a favorite —
having reasoning baked into the plan object made the UI side trivial.

**b. What you would improve**

Add time-of-day preferences to tasks, like "morning only" or "before noon."
Right now the scheduler has no concept of when in the day something should happen.

**c. Key takeaway**

Designing classes on paper before writing any code saved a ton of refactoring.
AI speeds up that design phase but you still have to make the final calls —
it doesn't know your constraintss the way you do.
