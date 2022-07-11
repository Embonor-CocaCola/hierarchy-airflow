DROP TABLE IF EXISTS airflow.tmp_dictionary;

CREATE TABLE airflow.tmp_dictionary (
    articuloid TEXT,
    family_name TEXT,
    nombre TEXT,
    something TEXT default '' --This is an extra column because right now the csv is coming with an useless column
);
