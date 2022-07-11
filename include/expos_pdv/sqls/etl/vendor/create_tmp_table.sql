DROP TABLE IF EXISTS airflow.tmp_vendor;

CREATE TABLE airflow.tmp_vendor (
    id TEXT,
    name TEXT,
    rut TEXT,
    email TEXT,
    phone TEXT,
    branchOffice TEXT,
    vendorTypeId TEXT,
    operationRange TEXT,
    deletedAt TEXT,
    driverHelperCode TEXT
);
