DELETE FROM
    airflow.customer_staged
WHERE
    job_id = %(job_id)s :: BIGINT;
ANALYZE airflow.customer_staged;

INSERT INTO airflow.customer_staged (
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

    created_at,
    updated_at,
    job_id,
    id
)
SELECT
    CUC.source_id,
    CUC.price_list,
    CUC.name,
    CUC.dni,
    CUC.email,
    CUC.street,
    CUC.street_number,
    CUC.location,
    CUC.sub_location,
    CUC.phone_number,
    COALESCE(bo.id, BOC.id),
    CUC.business_name,
    CUC.category_name,
    CUC.category_id,
    CUC.main_category_name,
    CUC.main_category_id,
    CUC.latitude,
    CUC.longitude,
    CUC.observations,
    CUC.credit_amount,
    CUC.credit_balance,
    CUC.duty_free_price_list,
    COALESCE(p.id, PLC.id),
    CUC.zone_id,
    CUC.route_id,
    CUC.territory_id,
    CUC.channel_mkt,
    CUC.cluster,
    CUC.deleted_at,
    CUC.market_group_id,
    CUC.market_chain_id,

    now(),
    now(),
    CUC.job_id,
    CUC.id
FROM
    airflow.customer_conform CUC
    INNER JOIN airflow.branch_office_conform BOC ON BOC.source_id = CUC.branch_office
    LEFT JOIN branch_office bo ON BOC.source_id = bo.source_id
    INNER JOIN airflow.plant_conform PLC ON PLC.source_id = CUC.plant_id
    LEFT JOIN plant p on PLC.source_id = p.source_id
WHERE
    CUC.job_id = %(job_id)s :: BIGINT AND
    BOC.job_id = %(job_id)s :: BIGINT AND
    PLC.job_id = %(job_id)s :: BIGINT
;
ANALYZE airflow.customer_staged;
