DELETE FROM
    airflow.vendor_type_raw
WHERE
    job_id = %(job_id)s :: BIGINT;

INSERT INTO airflow.vendor_type_raw (
    source_id,
    name,

    created_at,
    updated_at,
    job_id,
    id
)

SELECT
    id,
    name,

    now(),
    now(),
    %(job_id)s :: BIGINT,
    uuid_generate_v4()
FROM
    airflow.tmp_vendor_type
;

DROP TABLE IF EXISTS airflow.tmp_vendor_type;
