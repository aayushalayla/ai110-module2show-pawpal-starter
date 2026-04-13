## Smarter Scheduling

PawPal+ now includes several scheduling improvements beyond basic task storage. Tasks are sorted chronologically by due time so the owner can view a clear daily schedule. The scheduler can also filter tasks by pet name or completion status, making it easier to focus on one animal or only pending work.

To support repeated care routines, the system includes simple recurring-task logic for daily and weekly tasks. It also performs basic conflict detection by identifying incomplete tasks scheduled for the same time and generating warnings when overlaps occur.

## Testing PawPal+

### Running the tests

```bash
python -m pytest tests/test_pawpal.py -v
```

### What the tests cover

| Test | Area | What it verifies |
|---|---|---|
| `test_mark_complete_changes_task_status` | Task state | `mark_complete()` flips `is_completed` to `True` |
| `test_adding_task_increases_pet_task_count` | Pet tasks | `add_task()` appends to the pet's task list |
| `test_sort_by_time_returns_chronological_order` | Sorting | Tasks added out of order are returned earliest-first |
| `test_completing_daily_task_creates_next_day_task` | Recurrence | Calling `create_recurring_task()` on a daily task adds a new task due exactly one day later |
| `test_detect_task_conflicts_flags_duplicate_times` | Conflict detection | Two pending tasks at the same time produce a warning containing both task titles |
| `test_no_conflict_when_times_differ` | Conflict detection | Tasks at different times produce no warnings |

### Confidence Level

(4/5 stars)

The core scheduling features — sorting, recurrence, and conflict detection — are well-covered and all six tests pass. The rating stops short of five stars because edge cases such as weekly recurrence, cross-pet conflicts, and timezone-aware datetimes are not yet tested.