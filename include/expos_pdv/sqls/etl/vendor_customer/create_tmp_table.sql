DROP TABLE IF EXISTS airflow.tmp_vendor_customer;

CREATE TABLE airflow.tmp_vendor_customer (
    vendorId TEXT,
    customerId TEXT,
    startDate TEXT,
    frequency TEXT,
    priority TEXT
);
