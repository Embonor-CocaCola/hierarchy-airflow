CREATE OR REPLACE PROCEDURE update_success_photo_products()
     AS
$$
DECLARE
    sku_family RECORD;
BEGIN
    for sku_family in select
       distinct on (spp.sku_family_id)
       spp.sku_family_id id,
        p.category category,
        p.group p_group,
        array_to_string(array_agg(distinct p.identity->>'brand_name'), ' / ')
            brand_name,
       case (array_agg(p.flavour_name))[1]
        when 'Cola' THEN true
        ELSE
            false
        END is_cola,
       case
           when (array_agg(distinct p.details->>'local_category_name'))[1] = 'PURIFICADA' OR (array_agg(distinct p.details->>'local_category_name'))[1] = 'MINERAL'
                THEN 'SIN SABOR'
            ELSE (array_agg(distinct p.details->>'local_category_name'))[1]
                END
           sub_category
       from success_photo_product spp inner join product p on p.sku = ANY(spp.skus) group by spp.sku_family_id, p.category, p.group
  LOOP
        UPDATE success_photo_product target SET
            product_group = sku_family.p_group,
            product_category = sku_family.category,
            is_cola = sku_family.is_cola,
            sub_category = sku_family.sub_category,
            brand = sku_family.brand_name
        WHERE target.sku_family_id = sku_family.id;

    END LOOP;
END;
$$ LANGUAGE plpgsql;
