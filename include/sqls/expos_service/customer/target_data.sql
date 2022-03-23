INSERT INTO customer (
    source_id,
    name,
    email,
    dni,
    street,
    street_number,
    location,
    sub_location,
    phone_number,
    branch_office_id,
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
    cluster_id,
    deleted_at,
    market_group_id,
    market_chain_id,
    id

)
SELECT
    STAGED.source_id,
    STAGED.name,
    STAGED.email,
    STAGED.dni,
    STAGED.street,
    STAGED.street_number,
    STAGED.location,
    STAGED.sub_location,
    STAGED.phone_number,
    STAGED.branch_office_id,
    STAGED.business_name,
    STAGED.category_name,
    STAGED.category_id,
    STAGED.main_category_name,
    STAGED.main_category_id,
    STAGED.latitude,
    STAGED.longitude,
    STAGED.observations,
    STAGED.credit_amount,
    STAGED.credit_balance,
    STAGED.duty_free_price_list,
    STAGED.plant_id,
    STAGED.zone_id,
    STAGED.route_id,
    STAGED.territory_id,
    STAGED.channel_mkt,
    STAGED.cluster_id,
    STAGED.deleted_at,
    STAGED.market_group_id,
    STAGED.market_chain_id,
    STAGED.id
FROM
    airflow.customer_staged STAGED
LEFT JOIN customer TARGET ON TARGET.source_id = STAGED.source_id
WHERE STAGED.job_id = %(job_id)s :: BIGINT
    AND TARGET.id IS NULL
;
ANALYZE customer;

UPDATE
    customer TARGET
SET
    name = STAGED.name,
    email = STAGED.email,
    dni = STAGED.dni,
    street = STAGED.street,
    street_number = STAGED.street_number,
    location = STAGED.location,
    sub_location = STAGED.sub_location,
    phone_number = STAGED.phone_number,
    branch_office_id = STAGED.branch_office_id,
    business_name = STAGED.business_name,
    category_name = STAGED.category_name,
    category_id = STAGED.category_id,
    main_category_name = STAGED.main_category_name,
    main_category_id = STAGED.main_category_id,
    latitude = STAGED.latitude,
    longitude = STAGED.longitude,
    observations = STAGED.observations,
    credit_amount = STAGED.credit_amount,
    credit_balance = STAGED.credit_balance,
    duty_free_price_list = STAGED.duty_free_price_list,
    plant_id = STAGED.plant_id,
    zone_id = STAGED.zone_id,
    route_id = STAGED.route_id,
    territory_id = STAGED.territory_id,
    channel_mkt = STAGED.channel_mkt,
    cluster = STAGED.cluster_id,
    deleted_at = STAGED.deleted_at,
    market_group_id = STAGED.market_group_id,
    market_chain_id = STAGED.market_chain_id
FROM
    airflow.customer_staged STAGED
WHERE
    STAGED.job_id = %(job_id)s :: BIGINT
    AND TARGET.source_id = STAGED.source_id
    AND (
        STAGED.name IS DISTINCT FROM TARGET.name OR
        STAGED.email IS DISTINCT FROM TARGET.email OR
        STAGED.dni IS DISTINCT FROM TARGET.dni OR
        STAGED.street IS DISTINCT FROM TARGET.street OR
        STAGED.street_number IS DISTINCT FROM TARGET.street_number OR
        STAGED.location IS DISTINCT FROM TARGET.location OR
        STAGED.sub_location IS DISTINCT FROM TARGET.sub_location OR
        STAGED.phone_number IS DISTINCT FROM TARGET.phone_number OR
        STAGED.branch_office_id IS DISTINCT FROM TARGET.branch_office_id OR
        STAGED.business_name IS DISTINCT FROM TARGET.business_name OR
        STAGED.category_name IS DISTINCT FROM TARGET.category_name OR
        STAGED.category_id IS DISTINCT FROM TARGET.category_id OR
        STAGED.main_category_name IS DISTINCT FROM TARGET.main_category_name OR
        STAGED.main_category_id IS DISTINCT FROM TARGET.main_category_id OR
        STAGED.latitude IS DISTINCT FROM TARGET.latitude OR
        STAGED.longitude IS DISTINCT FROM TARGET.longitude OR
        STAGED.observations IS DISTINCT FROM TARGET.observations OR
        STAGED.credit_amount IS DISTINCT FROM TARGET.credit_amount OR
        STAGED.credit_balance IS DISTINCT FROM TARGET.credit_balance OR
        STAGED.duty_free_price_list IS DISTINCT FROM TARGET.duty_free_price_list OR
        STAGED.plant_id IS DISTINCT FROM TARGET.plant_id OR
        STAGED.zone_id IS DISTINCT FROM TARGET.zone_id OR
        STAGED.route_id IS DISTINCT FROM TARGET.route_id OR
        STAGED.territory_id IS DISTINCT FROM TARGET.territory_id OR
        STAGED.channel_mkt IS DISTINCT FROM TARGET.channel_mkt OR
        STAGED.cluster_id IS DISTINCT FROM TARGET.cluster_id OR
        STAGED.deleted_at IS DISTINCT FROM TARGET.deleted_at OR
        STAGED.market_group_id IS DISTINCT FROM TARGET.market_group_id OR
        STAGED.market_chain_id IS DISTINCT FROM TARGET.market_chain_id
);
ANALYZE customer;
