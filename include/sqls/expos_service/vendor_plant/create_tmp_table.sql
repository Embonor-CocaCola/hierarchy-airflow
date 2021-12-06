DROP TABLE IF EXISTS airflow.tmp_vendor_plant;

CREATE TABLE airflow.tmp_vendor_plant (
    vendorId TEXT,
    supervisorId TEXT,
    vendorCode TEXT,
    vendorSap TEXT,
    vendorName TEXT,
    chiefRut TEXT,
    plantId TEXT,
    plant TEXT,
    chiefUnit TEXT
);
