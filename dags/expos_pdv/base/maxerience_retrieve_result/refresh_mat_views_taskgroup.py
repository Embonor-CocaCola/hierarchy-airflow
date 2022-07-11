from airflow.models.dag import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.task_group import TaskGroup

from expos_pdv.base.run_sqls.utils.graph import Graph
from expos_pdv.base.utils.tasks import arrange_task_list_sequentially
from expos_pdv.config.etl.settings import ES_AIRFLOW_DATABASE_CONN_ID
from expos_pdv.config.run_sqls.settings import SQL_DEPENDENCY_GRAPH


class RefreshMatViewsTaskGroup:
    def __init__(self, dag: DAG, group_id: str) -> None:
        if not group_id:
            raise ValueError('group_id parameter is missing')
        if not dag:
            raise ValueError('dag parameter is missing')

        self.dag = dag
        self.group_id = group_id
        self.graph = Graph(SQL_DEPENDENCY_GRAPH)

    def build(self):
        task_group = TaskGroup(group_id=self.group_id)

        sql_tasks = self.graph.get_topology_sort()

        tasks = list(
            map(lambda node_name: list(map(lambda refresh_data: PostgresOperator(
                task_id=f'refresh_{refresh_data["table_name"]}',
                task_group=task_group,
                postgres_conn_id=ES_AIRFLOW_DATABASE_CONN_ID,
                execution_timeout=None,
                sql=f"""
                    REFRESH MATERIALIZED VIEW CONCURRENTLY {refresh_data["table_name"]}
                """), self.graph.get_node(node_name)['refresh_data'])),
                filter(
                    lambda node_name: self.graph.get_node(node_name).get('refresh_data', None),
                    sql_tasks),
                ),
        )

        arrange_task_list_sequentially(tasks)

        return task_group
