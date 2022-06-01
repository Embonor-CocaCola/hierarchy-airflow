import uuid
from pathlib import Path

from base.utils.query_with_return import parameterized_query
from config.common.settings import airflow_root_dir


def create_survey_analysis(survey_id):
    analysis_id = str(uuid.uuid4())

    with open(
            Path(airflow_root_dir) / 'include' / 'sqls' / 'maxerience_load' / 'create_survey_analysis.sql',
            'r',
    ) as file:
        sql = file.read()
        parameterized_query(
            sql=sql,
            templates_dict={
                'survey_id': survey_id,
                'analysis_id': analysis_id,
            },
            is_procedure=True,
        )

    return analysis_id
