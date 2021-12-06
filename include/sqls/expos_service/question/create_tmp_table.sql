DROP TABLE IF EXISTS airflow.tmp_question;

CREATE TABLE airflow.tmp_question (
   id TEXT,
   attach TEXT,
   type TEXT,
   subType TEXT,
   options TEXT,
   inputExpirationDays TEXT,
   heading TEXT,
   createdAt TEXT,
   updatedAt TEXT,
   v TEXT
);
