INSERT INTO product (
    id,
    identity,
    display,
    details,
    recognition_details,
    created_by_user_id,
    created_on,
    modified_by_user_id,
    modified_on,
    sku,
    "name",
    "group",
    "category",
    local_category_name,
    is_foreign,
    flavour_name
)
VALUES (
    18,
    '{"name": "Empty", "sku": ""}',
    '{}',
    '{}',
    '{}',
    1,
    now() :: timestamp,
    1,
    now():: timestamp,
    null,
    null,
    null,
    null,
    null,
    null,
    null
       ), (
    54,
    '{"name": "Foreign", "sku": "0"}',
    '{}',
    '{}',
    '{"is_foreign": true}',
    1,
    now() :: timestamp,
    1,
    now():: timestamp,
    0,
    null,
    null,
    null,
    null,
    true,
    null
)
ON CONFLICT(id) DO NOTHING
;

INSERT INTO product (
    id,
    identity,
    display,
    details,
    recognition_details,
    created_by_user_id,
    created_on,
    modified_by_user_id,
    modified_on,
    sku,
    "name",
    "group",
    "category",
    local_category_name,
    is_foreign,
    flavour_name
)
SELECT
    id,
    identity,
    display,
    details,
    recognition_details,
    created_by_user_id,
    created_on,
    modified_by_user_id,
    modified_on,
    sku,
    "name",
    "group",
    "category",
    local_category_name,
    is_foreign,
    flavour_name
FROM tmp_product_typed
WHERE manufacturer != 'Embol'
ON CONFLICT(id) DO UPDATE SET
    identity = EXCLUDED.identity,
    display = EXCLUDED.display,
    details = EXCLUDED.details,
    recognition_details = EXCLUDED.recognition_details,
    created_by_user_id = EXCLUDED.created_by_user_id,
    created_on = EXCLUDED.created_on,
    modified_by_user_id = EXCLUDED.modified_by_user_id,
    modified_on = EXCLUDED.modified_on,
    sku = EXCLUDED.sku,
    "name" = EXCLUDED."name",
    "group" = EXCLUDED."group",
    "category" = EXCLUDED."category",
    local_category_name = EXCLUDED.local_category_name,
    is_foreign = EXCLUDED.is_foreign,
    flavour_name = EXCLUDED.flavour_name
;

ANALYZE product;

DELETE FROM
    product TARGET
WHERE
    TARGET.id IN (
            SELECT p.id FROM product p
                LEFT JOIN tmp_product_typed pt
                ON pt.id = p.id AND pt.manufacturer != 'Embol'
                WHERE pt.id IS NULL
        )
    AND TARGET.id NOT IN (18, 54)
;
