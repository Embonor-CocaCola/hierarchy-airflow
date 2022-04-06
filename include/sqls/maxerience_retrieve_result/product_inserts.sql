INSERT INTO product (
    id,
    identity,
    display,
    details,
    recognition_details,
    created_by_user_id,
    created_on,
    modified_by_user_id,
    modified_on
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
    now():: timestamp
       ), (
    54,
    '{"name": "Foreign", "sku": "0"}',
    '{}',
    '{}',
    '{}',
    1,
    now() :: timestamp,
    1,
    now():: timestamp
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
    modified_on
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
    modified_on
FROM tmp_product_typed
ON CONFLICT(id) DO UPDATE SET
    identity = EXCLUDED.identity,
    display = EXCLUDED.display,
    details = EXCLUDED.details,
    recognition_details = EXCLUDED.recognition_details,
    created_by_user_id = EXCLUDED.created_by_user_id,
    created_on = EXCLUDED.created_on,
    modified_by_user_id = EXCLUDED.modified_by_user_id,
    modified_on = EXCLUDED.modified_on
;

ANALYZE product;

DELETE FROM
    product TARGET
WHERE
    TARGET.id IN (
            SELECT p.id FROM product p
                LEFT JOIN tmp_product_typed pt
                ON pt.id = p.id
                WHERE pt.id IS NULL
        )
;
