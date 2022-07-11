DROP TABLE IF EXISTS airflow.tmp_branch_office;

CREATE TABLE airflow.tmp_branch_office (
    id TEXT,
    name TEXT,
    closingTime TEXT,
    plantId TEXT,
    freightCode TEXT,
    enableDelayOrders TEXT,
    invoiceLeadTime TEXT,
    webClosingTime TEXT
);
