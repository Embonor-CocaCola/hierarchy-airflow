DROP TABLE IF EXISTS airflow.success_photo_product_conform;

CREATE TABLE IF NOT EXISTS airflow.success_photo_product_conform (
    cluster INT,
    sku_family_id INT,
    is_essential BOOLEAN,
    required_facings INT,
    shelf INT,
    flavors INT,
    sku_family_name TEXT,
    sku INT[],
    created_at DATE,
    updated_at DATE,
    id uuid,
    PRIMARY KEY (id)
);



INSERT INTO airflow.success_photo_product_conform (
    cluster,
    sku_family_id,
    is_essential,
    required_facings,
    shelf,
    flavors,
    sku_family_name,
    sku,

    created_at,
    updated_at,
    id
)
SELECT
    cluster,
    TYPED.sku_family_id,
    is_essential,
    required_facings,
    shelf,
    flavors,
    TYPED.sku_family_name,
    ARRAY_AGG (distinct DIC.sku) sku,

    now(),
    now(),
    (ARRAY_AGG (TYPED.id))[1]
FROM
    airflow.success_photo_product_typed TYPED
    LEFT JOIN airflow.dictionary_typed DIC ON DIC.sku_family_id = TYPED.sku_family_id
GROUP BY cluster, TYPED.sku_family_id, is_essential, required_facings, shelf, flavors, TYPED.sku_family_name
;
