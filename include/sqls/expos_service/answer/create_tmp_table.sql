DROP TABLE IF EXISTS airflow.tmp_answer;

CREATE TABLE airflow.tmp_answer (
    v TEXT,
    id TEXT,
    answers TEXT,
    createdAt TEXT,
    latitude TEXT,
    longitude TEXT,
    pollsterId TEXT,
    skipsSurvey TEXT,
    surveyId TEXT,
    surveyedId TEXT,
    updatedAt TEXT
);
