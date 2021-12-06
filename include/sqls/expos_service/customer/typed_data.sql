DELETE FROM
    airflow.customer_typed
WHERE
    job_id = %(job_id)s :: BIGINT;

INSERT INTO airflow.customer_typed (
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
    country_specific,
    deleted_at,
    market_group_id,
    market_chain_id,

    created_at,
    updated_at,
    job_id,
    id
)
SELECT
    trim(source_id) :: INTEGER,
    trim(price_list) :: INTEGER,
    trim(name),
    trim(dni),
    trim(email),
    trim(street),
    trim(street_number),
    trim(location),
    trim(sub_location),
    trim(phone_number),
    trim(branch_office) :: INTEGER,
    trim(business_name),
    trim(category_name),
    trim(category_id),
    trim(main_category_name),
    trim(main_category_id),
    trim(latitude) :: FLOAT,
    trim(longitude) :: FLOAT,
    trim(observations),
    trim(credit_amount) :: INTEGER,
    trim(credit_balance) :: INTEGER,
    trim(duty_free_price_list) :: INTEGER,
    trim(plant_id) :: INTEGER,
    trim(zone_id) :: INTEGER,
    trim(route_id) :: INTEGER,
    trim(territory_id) :: INTEGER,
    trim(channel_mkt),
    trim(country_specific) :: jsonb,
    to_timestamp(deleted_at, 'YYYY-MM-DD HH24:MI:SS'),
    trim(market_group_id),
    trim(market_chain_id),

    now(),
    now(),
    job_id,
    id
FROM
    airflow.customer_raw
WHERE job_id = %(job_id)s :: BIGINT
;
