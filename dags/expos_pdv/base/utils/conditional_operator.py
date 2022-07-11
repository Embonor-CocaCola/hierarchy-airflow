from airflow.operators.dummy import DummyOperator


def conditional_operator(condition, operator, should_build=False, **kwargs):
    task = operator(**kwargs) if condition else DummyOperator(task_id=kwargs.get('task_id',
                                                                                 kwargs.get('group_id',
                                                                                            kwargs.get('stage'))))
    return task.build() if should_build and condition else task
