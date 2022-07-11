from datetime import datetime

from airflow.models import DAG

from expos_pdv.base.run_sqls.create_procedures_taskgroup import CreateProceduresTaskGroup
from expos_pdv.base.utils.slack import notify_start_task
from expos_pdv.config.common.defaults import default_task_kwargs, default_dag_kwargs
from expos_pdv.config.run_sqls.settings import RSQLS_DAG_ID, RSQLS_DAG_SCHEDULE_INTERVAL, RSQLS_DAG_START_DATE_VALUE


class RunSqlsDagFactory:
    @staticmethod
    def build() -> DAG:
        _start_date = datetime.strptime(
            RSQLS_DAG_START_DATE_VALUE, '%Y-%m-%d')
        _default_args = {
            **default_task_kwargs,
            'start_date': _start_date,
        }

        with DAG(
                RSQLS_DAG_ID,
                **default_dag_kwargs,
                schedule_interval=RSQLS_DAG_SCHEDULE_INTERVAL,
                default_args=_default_args,
        ) as _dag:

            notify_dag_start = notify_start_task(_dag)

            run_procedures = CreateProceduresTaskGroup(group_id='run_procedures', dag=_dag).build()

            notify_dag_start >> run_procedures
        return _dag
