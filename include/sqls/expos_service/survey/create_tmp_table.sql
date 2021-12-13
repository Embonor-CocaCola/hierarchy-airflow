DROP TABLE IF EXISTS airflow.tmp_survey;

CREATE TABLE airflow.tmp_survey (
    ver TEXT,
    id TEXT,
    answers_goal_number TEXT,
    created_at TEXT,
    name TEXT,
    paused TEXT,
    portals TEXT,
    updated_at TEXT,
    valid_since TEXT,
    valid_until TEXT
);
