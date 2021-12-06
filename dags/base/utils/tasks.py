def arrange_task_list_sequentially(tasks: list) -> None:
    for index in range(0, len(tasks) - 1):
        tasks[index] >> tasks[index + 1]
