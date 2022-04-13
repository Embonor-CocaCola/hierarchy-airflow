DROP TABLE IF EXISTS airflow.dictionary_typed;

CREATE TABLE IF NOT EXISTS airflow.dictionary_typed (
    sku INT,
    sku_family_id INT,
    sku_family_name TEXT,
    created_at DATE,
    updated_at DATE,
    id uuid,
    PRIMARY KEY (id)
);



INSERT INTO airflow.dictionary_typed (
    sku,
    sku_family_id,
    sku_family_name,
    created_at,
    updated_at,
    id
)
SELECT
    trim(raw.sku) :: INT,
    trim(raw.sku_family_id) :: INT,
    trim(raw.sku_family_name),

    now(),
    now(),
    raw.id
FROM
    airflow.dictionary_raw raw
;
