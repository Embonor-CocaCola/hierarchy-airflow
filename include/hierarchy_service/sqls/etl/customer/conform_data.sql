DELETE FROM
    airflow.customer_conform
WHERE
    job_id = %(job_id)s :: BIGINT;
ANALYZE airflow.customer_conform;

INSERT INTO airflow.customer_conform (
    source_id,
    price_list,
    name,
    dni,
    email,
    street,
    street_number,
    location,
    sub_location,
    phone_number,
    branch_office,
    business_name,
    category_name,
    category_id,
    main_category_name,
    main_category_id,
    latitude,
    longitude,
    observations,
    credit_amount,
    credit_balance,
    duty_free_price_list,
    plant_id,
    zone_id,
    route_id,
    territory_id,
    channel_mkt,
    cluster,
    deleted_at,
    market_group_id,
    market_chain_id,

    created_at,
    updated_at,
    job_id,
    id
)
SELECT
    source_id,
    price_list,
    INITCAP(name),
    dni,
    email,
    street,
    street_number,
    location,
    sub_location,
    phone_number,
    branch_office,
    business_name,
    category_name,
    category_id,
    main_category_name,
    main_category_id,
    latitude,
    longitude,
    observations,
    credit_amount,
    credit_balance,
    duty_free_price_list,
    plant_id,
    zone_id,
    route_id,
    territory_id,
    channel_mkt,
    COALESCE(country_specific->>'cluster', 'Sin cluster'),
    deleted_at,
    market_group_id,
    market_chain_id,

    now(),
    now(),
    job_id,
    id
FROM
    airflow.customer_typed
WHERE job_id = %(job_id)s :: BIGINT
;
ANALYZE airflow.customer_conform;
