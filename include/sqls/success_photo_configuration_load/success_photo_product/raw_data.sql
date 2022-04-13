DROP TABLE IF EXISTS airflow.success_photo_product_raw;

CREATE TABLE IF NOT EXISTS airflow.success_photo_product_raw (
    cluster TEXT,
    sku_family_id TEXT,
    is_essential TEXT,
    required_facings TEXT,
    shelf TEXT,
    position TEXT,
    flavors TEXT,
    cooler TEXT,
    sku_family_name TEXT,
    created_at DATE,
    updated_at DATE,
    id uuid DEFAULT uuid_generate_v4(),
    PRIMARY KEY (id)
);



INSERT INTO airflow.success_photo_product_raw (
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
    updated_at
)
SELECT
    Cluster,
    family_name,
    imprescindible,
    caras,
    bandeja,
    posicion,
    sabores,
    cooler,
    nombre,

    now(),
    now()
FROM
    airflow.tmp_success_photo_product
;

DROP TABLE IF EXISTS airflow.tmp_success_photo_product;
