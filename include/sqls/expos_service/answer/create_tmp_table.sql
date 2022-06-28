DROP TABLE IF EXISTS airflow.tmp_answer;

CREATE TABLE airflow.tmp_answer (
    v TEXT,
    id TEXT,
    answers TEXT,
    createdAt TEXT,
    {{ params.additional_columns }}
);
