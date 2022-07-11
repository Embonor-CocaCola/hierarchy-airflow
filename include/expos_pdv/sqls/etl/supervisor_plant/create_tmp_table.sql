DROP TABLE IF EXISTS airflow.tmp_supervisor_plant;

CREATE TABLE airflow.tmp_supervisor_plant (
   supervisorId TEXT,
   supervisorCode TEXT,
   supervisorName TEXT,
   supervisorLocation TEXT,
   chiefId TEXT,
   plantId TEXT,
   role TEXT,
   chiefUnit TEXT
);
