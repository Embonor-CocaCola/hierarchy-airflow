DROP TABLE IF EXISTS airflow.tmp_survey;

CREATE TABLE airflow.tmp_survey (
    id TEXT,
    paused TEXT,
    answers_goal_number TEXT,
    name TEXT,
    portals TEXT,
    created_at TEXT,
    updated_at TEXT,
    ver TEXT,
    valid_until TEXT,
    valid_since TEXT
);
