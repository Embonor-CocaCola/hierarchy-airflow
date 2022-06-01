from airflow.operators.dummy import DummyOperator


def conditional_operator(condition, operator, should_build=False, **kwargs):
    task = operator(**kwargs) if condition else DummyOperator(task_id=kwargs.get('task_id', kwargs.get('group_id')))
    return task.build() if should_build and condition else task
