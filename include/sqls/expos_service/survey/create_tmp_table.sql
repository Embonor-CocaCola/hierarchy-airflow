DROP TABLE IF EXISTS airflow.tmp_survey;

CREATE TABLE airflow.tmp_survey (
    ver TEXT,
    id TEXT,
    {{ params.additional_columns }}
    portals TEXT,
    updated_at TEXT,
    valid_since TEXT,
    valid_until TEXT
);
