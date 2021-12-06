DROP TABLE IF EXISTS airflow.tmp_answer;

CREATE TABLE airflow.tmp_answer (
    id TEXT,
    latitude TEXT,
    longitude TEXT,
    answers TEXT,
    pollsterId TEXT,
    surveyId TEXT,
    surveyedId TEXT,
    createdAt TEXT,
    updatedAt TEXT,
    v TEXT,
    skipsSurvey TEXT
);
