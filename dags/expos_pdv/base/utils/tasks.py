def arrange_task_list_sequentially(tasks: list) -> None:
    for index in range(0, len(tasks) - 1):
        if isinstance(tasks[index], list) and isinstance(tasks[index + 1], list):

            tasks[index][0] >> tasks[index + 1]
        else:
            tasks[index] >> tasks[index + 1]
