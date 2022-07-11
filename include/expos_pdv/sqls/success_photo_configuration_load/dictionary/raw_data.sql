DROP TABLE IF EXISTS airflow.dictionary_raw;

CREATE TABLE IF NOT EXISTS airflow.dictionary_raw (
    sku TEXT,
    sku_family_id TEXT,
    sku_family_name TEXT,
    created_at DATE,
    updated_at DATE,
    id uuid DEFAULT uuid_generate_v4(),
    PRIMARY KEY (id)
);



INSERT INTO airflow.dictionary_raw (
    sku,
    sku_family_id,
    sku_family_name,
    created_at,
    updated_at
)
SELECT
    articuloid,
    family_name,
    nombre,

    now(),
    now()
FROM
    airflow.tmp_dictionary
;

DROP TABLE IF EXISTS airflow.tmp_dictionary;
