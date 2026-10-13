def edzl_schedule(tasks):
    """
    Educational EDZL scheduler for a single preemptive CPU.

    Each task has:
      pid       : task ID
      arrival   : arrival time
      execution : required CPU time
      deadline  : absolute deadline
    """

    for task in tasks:
        task["remaining"] = task["execution"]
        task["completion"] = None

    time = 0
    gantt = []
    total_tasks = len(tasks)

    while any(task["remaining"] > 0 for task in tasks):
        ready = [
            task for task in tasks
            if task["arrival"] <= time
            and task["remaining"] > 0
        ]

        if not ready:
            gantt.append((time, "IDLE"))
            time += 1
            continue

        # Calculate laxity for each ready task
        for task in ready:
            task["laxity"] = (
                task["deadline"]
                - time
                - task["remaining"]
            )

        # EDZL: zero/negative-laxity tasks have priority.
        urgent = [
            task for task in ready
            if task["laxity"] <= 0
        ]

        if urgent:
            selected = min(
                urgent,
                key=lambda task: (
                    task["deadline"],
                    task["pid"]
                )
            )
        else:
            # Otherwise, select the earliest deadline.
            selected = min(
                ready,
                key=lambda task: (
                    task["deadline"],
                    task["pid"]
                )
            )

        gantt.append((time, selected["pid"]))

        selected["remaining"] -= 1
        time += 1

        if selected["remaining"] == 0:
            selected["completion"] = time

    # Print Gantt chart
    print("\n--- Gantt Chart ---")
    for t, pid in gantt:
        print(f"{t}: {pid}")

    # Print results
    print("\n--- Task Results ---")
    deadline_misses = 0

    for task in tasks:
        completion = task["completion"]
        result = (
            "ON TIME"
            if completion <= task["deadline"]
            else "DEADLINE MISSED"
        )

        if result == "DEADLINE MISSED":
            deadline_misses += 1

        print(
            f'{task["pid"]}: '
            f'Arrival={task["arrival"]}, '
            f'Execution={task["execution"]}, '
            f'Deadline={task["deadline"]}, '
            f'Completion={completion}, '
            f'Result={result}'
        )

    print(f"\nDeadline misses: {deadline_misses}")


if __name__ == "__main__":
    tasks = [
        {
            "pid": "T1",
            "arrival": 0,
            "execution": 3,
            "deadline": 7
        },
        {
            "pid": "T2",
            "arrival": 1,
            "execution": 2,
            "deadline": 4
        },
        {
            "pid": "T3",
            "arrival": 2,
            "execution": 2,
            "deadline": 8
        }
    ]

    edzl_schedule(tasks)