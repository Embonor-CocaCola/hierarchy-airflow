DELETE FROM
    airflow.customer_raw
WHERE
    job_id = %(job_id)s :: BIGINT;

INSERT INTO airflow.customer_raw (
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
    geog,
    deleted_at,
    market_group_id,
    market_chain_id,

    created_at,
    updated_at,
    job_id,
    id
)

SELECT
    id,
    pricelist,
    name,
    dni,
    email,
    street,
    streetnumber,
    location,
    sublocation,
    phonenumber,
    branchoffice,
    businessname,
    categoryname,
    categoryid,
    maincategoryname,
    maincategoryid,
    latitude,
    longitude,
    observations,
    creditamount,
    creditbalance,
    dutyfreepricelist,
    plantid,
    zoneid,
    ruteid,
    territoryid,
    channelmkt,
    countryspecific,
    geog,
    deletedat,
    marketgroupid,
    marketchainid,

    now(),
    now(),
    %(job_id)s :: BIGINT,
    uuid_generate_v4()
FROM
    airflow.tmp_customer
;

DROP TABLE IF EXISTS airflow.tmp_customer;
