TRUNCATE TABLE success_photo_product;

INSERT INTO success_photo_product (
    skus,
    is_essential,
    required_facings,
    flavors,
    sku_family_name,
    sku_family_id,
    cluster_id,
    id
)
SELECT
    STAGED.sku,
    STAGED.is_essential,
    STAGED.required_facings,
    STAGED.flavors,
    STAGED.sku_family_name,
    STAGED.sku_family_id,
    cluster.id,
    STAGED.id
FROM
    airflow.success_photo_product_conform STAGED
    INNER JOIN cluster ON cluster.weight = STAGED.cluster
;
