DROP TABLE IF EXISTS airflow.tmp_survey;

CREATE TABLE airflow.tmp_survey (
    ver TEXT,
    id TEXT,
    {{ params.additional_columns }}
);
