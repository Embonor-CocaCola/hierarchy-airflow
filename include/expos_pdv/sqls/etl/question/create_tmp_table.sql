DROP TABLE IF EXISTS airflow.tmp_question;

CREATE TABLE airflow.tmp_question (
   v TEXT,
   id TEXT,
   attach TEXT,
   createdAt TEXT,
   heading TEXT,
   inputExpirationDays TEXT,
   observation TEXT,
   options TEXT,
   subType TEXT,
   type TEXT,
   updatedAt TEXT
);
