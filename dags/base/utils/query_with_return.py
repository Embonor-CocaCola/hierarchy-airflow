import os

from psycopg2 import ProgrammingError
from airflow.providers.postgres.hooks.postgres import PostgresHook
from psycopg2.extras import execute_values

from config.common.settings import airflow_root_dir
from config.maxerience_load.settings import ML_AIRFLOW_DATABASE_CONN_ID


def parameterized_query(sql, wrap=True, is_procedure=False, **kwargs):
    print('Running parameterized query:')
    print(sql)
    print('params: ')
    print(kwargs.get('templates_dict', 'no params provided'))
    pg_hook = PostgresHook(postgres_conn_id=ML_AIRFLOW_DATABASE_CONN_ID)
    with pg_hook.get_conn() as conn:
        if is_procedure:
            conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute(sql, kwargs.get('templates_dict'))
            try:
                rows = cursor.fetchall()
            except ProgrammingError:
                rows = []

    if wrap:
        return [item for sublist in rows for item in sublist]
    else:
        return rows


def multiple_insert_query(sql, values, wrap=True, autocommit=True):
    print('Running multiple inserts query:')
    print(sql)
    pg_hook = PostgresHook(postgres_conn_id=ML_AIRFLOW_DATABASE_CONN_ID)
    with pg_hook.get_conn() as conn:
        if autocommit:
            conn.autocommit = True
        with conn.cursor() as cursor:
            execute_values(cursor, sql, values)

            try:
                rows = cursor.fetchall()
            except ProgrammingError:
                rows = []

    if wrap:
        return [item for sublist in rows for item in sublist]
    else:
        return rows


def enclose(sql):
    if sql:
        return f'( {sql} )'
    return sql


def copy_csv_to_table(table, filepath, columns):
    print(f'Executing COPY to {table} from {filepath}')
    tmp_table_name_raw = f'tmp_{table}_raw'
    tmp_table_name_typed = f'tmp_{table}_typed'
    columns_without_type = map(lambda name: name.split('::')[0], columns)
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f'CSV file {filepath} not found')

    print(f'Creating temporary raw and typed tables for "{table}"')
    pg_hook = PostgresHook(postgres_conn_id=ML_AIRFLOW_DATABASE_CONN_ID)
    with pg_hook.get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"""
                DROP TABLE IF EXISTS {tmp_table_name_raw};
                CREATE TABLE {tmp_table_name_raw}
                ({','.join(map(lambda name: f'{name} TEXT', columns_without_type))})
            """)
            cursor.execute(f"""
                DROP TABLE IF EXISTS {tmp_table_name_typed};
                CREATE TABLE {tmp_table_name_typed}
                ({','.join(map(lambda name: f'{name.split("::")[0]} {name.split("::")[1]}', columns))})
            """)
            conn.commit()
            print('COPYing to raw tmp table')
            pg_hook.copy_expert(
                f"""
                    COPY {tmp_table_name_raw}{enclose(','.join(columns_without_type))}
                    FROM STDIN DELIMITER E',' CSV QUOTE '|'
                    """,
                filepath,
            )
            print('Inserting typed data...')
            cursor.execute(f"""
                            INSERT INTO {tmp_table_name_typed}{enclose(','.join(columns_without_type))}
                            SELECT {','.join(columns)} FROM {tmp_table_name_raw}
                        """)

            with open(f'{airflow_root_dir}/include/sqls/maxerience_retrieve_result/{table}_inserts.sql', 'r') as file:
                sql = file.read()
                cursor.execute(sql)
            conn.commit()
