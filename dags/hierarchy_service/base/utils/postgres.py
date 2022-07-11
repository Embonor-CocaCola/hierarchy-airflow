from airflow.providers.postgres.hooks.postgres import PostgresHook
from psycopg2 import ProgrammingError


def perform_pg_query(conn_id, query, handle_result):
    pg_hook = PostgresHook(
        postgres_conn_id=conn_id,
        schema='embonor',
    )
    conn = pg_hook.get_conn()
    cursor = conn.cursor()
    cursor.execute(query)
    try:
        rows = cursor.fetchall()
    except ProgrammingError:
        rows = None
    handle_result(rows)
    cursor.close()
    conn.commit()
    conn.close()


PG_IS_ONLINE_QUERY = 'SELECT 1'


def pg_online_check_result(rows):
    result = rows[0][0]
    if result != 1:
        raise ValueError('Database is not working as expected')
