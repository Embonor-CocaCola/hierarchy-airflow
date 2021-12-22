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
    cluster,
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
    STAGED.cluster,
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
    plant_id = p.id,
    zone_id = STAGED.zone_id,
    route_id = STAGED.route_id,
    territory_id = STAGED.territory_id,
    channel_mkt = STAGED.channel_mkt,
    cluster = STAGED.cluster,
    deleted_at = STAGED.deleted_at,
    market_group_id = STAGED.market_group_id,
    market_chain_id = STAGED.market_chain_id
FROM
    airflow.customer_staged STAGED,
    customer c,
    airflow.plant_staged pls,
    plant p,
    plant pp
WHERE
    STAGED.job_id = %(job_id)s :: BIGINT
    AND c.source_id = STAGED.source_id
    AND pls.id = STAGED.plant_id
    AND pls.source_id = p.source_id
    AND pp.id = c.plant_id
    AND pls.job_id = %(job_id)s :: BIGINT
    AND (
        STAGED.name IS DISTINCT FROM c.name OR
        STAGED.email IS DISTINCT FROM c.email OR
        STAGED.dni IS DISTINCT FROM c.dni OR
        STAGED.street IS DISTINCT FROM c.street OR
        STAGED.street_number IS DISTINCT FROM c.street_number OR
        STAGED.location IS DISTINCT FROM c.location OR
        STAGED.sub_location IS DISTINCT FROM c.sub_location OR
        STAGED.phone_number IS DISTINCT FROM c.phone_number OR
        STAGED.branch_office_id IS DISTINCT FROM c.branch_office_id OR
        STAGED.business_name IS DISTINCT FROM c.business_name OR
        STAGED.category_name IS DISTINCT FROM c.category_name OR
        STAGED.category_id IS DISTINCT FROM c.category_id OR
        STAGED.main_category_name IS DISTINCT FROM c.main_category_name OR
        STAGED.main_category_id IS DISTINCT FROM c.main_category_id OR
        STAGED.latitude IS DISTINCT FROM c.latitude OR
        STAGED.longitude IS DISTINCT FROM c.longitude OR
        STAGED.observations IS DISTINCT FROM c.observations OR
        STAGED.credit_amount IS DISTINCT FROM c.credit_amount OR
        STAGED.credit_balance IS DISTINCT FROM c.credit_balance OR
        STAGED.duty_free_price_list IS DISTINCT FROM c.duty_free_price_list OR
        p.id IS DISTINCT FROM pp.id OR
        STAGED.zone_id IS DISTINCT FROM c.zone_id OR
        STAGED.route_id IS DISTINCT FROM c.route_id OR
        STAGED.territory_id IS DISTINCT FROM c.territory_id OR
        STAGED.channel_mkt IS DISTINCT FROM c.channel_mkt OR
        STAGED.cluster IS DISTINCT FROM c.cluster OR
        STAGED.deleted_at IS DISTINCT FROM c.deleted_at OR
        STAGED.market_group_id IS DISTINCT FROM c.market_group_id OR
        STAGED.market_chain_id IS DISTINCT FROM c.market_chain_id
);
