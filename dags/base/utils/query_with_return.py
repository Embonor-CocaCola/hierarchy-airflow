from psycopg2 import ProgrammingError
from airflow.providers.postgres.hooks.postgres import PostgresHook

from config.maxerience_load.settings import ML_AIRFLOW_DATABASE_CONN_ID


def parameterized_query(sql, wrap=True, is_procedure=False, **kwargs):
    print('Running parameterized query:')
    print(sql)
    print('params: ')
    print(kwargs['templates_dict'])
    pg_hook = PostgresHook(postgres_conn_id=ML_AIRFLOW_DATABASE_CONN_ID)
    with pg_hook.get_conn() as conn:
        if is_procedure:
            conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute(sql, kwargs['templates_dict'])
            try:
                rows = cursor.fetchall()
            except ProgrammingError:
                rows = []

    if wrap:
        return [item for sublist in rows for item in sublist]
    else:
        return rows