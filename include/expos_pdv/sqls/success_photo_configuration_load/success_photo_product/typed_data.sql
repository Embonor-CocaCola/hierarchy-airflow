DROP TABLE IF EXISTs airflow.success_photo_product_typed;

CREATE TABLE IF NOT EXISTS airflow.success_photo_product_typed (
    cluster INT,
    sku_family_id INT,
    is_essential BOOLEAN,
    required_facings INT,
    shelf INT,
    position INT,
    flavors INT,
    cooler INT,
    sku_family_name TEXT,
    created_at DATE,
    updated_at DATE,
    id uuid,
    PRIMARY KEY (id)
);



INSERT INTO airflow.success_photo_product_typed (
    cluster,
    sku_family_id,
    is_essential,
    required_facings,
    shelf,
    position,
    flavors,
    cooler,
    sku_family_name,
    created_at,
    updated_at,
    id
)
SELECT
    trim(raw.cluster) :: INT,
    trim(raw.sku_family_id) :: INT,
    CASE raw.is_essential
    WHEN 'FALSE' THEN false
    WHEN 'TRUE' THEN true
    ELSE false
    END,
    trim(raw.required_facings) :: INT,
    trim(raw.shelf) :: INT,
    trim(raw.position) :: INT,
    trim(raw.flavors) :: INT,
    trim(raw.cooler) :: INT,
    trim(raw.sku_family_name),

    now(),
    now(),
    raw.id
FROM
    airflow.success_photo_product_raw raw
;
