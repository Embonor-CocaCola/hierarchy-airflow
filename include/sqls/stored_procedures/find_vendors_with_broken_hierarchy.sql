DROP FUNCTION IF EXISTS find_vendors_with_broken_hierarchy(jobid int);
CREATE FUNCTION find_vendors_with_broken_hierarchy(jobid int)
    RETURNS TABLE (
                    vendor_source_id int,
                    vendor_name text,
                    vendor_rut text,
                    vendor_email text,
                    vendor_phone text,
                    branch_office_name text,
                    plant_name text,
                    last_evaluation_at text,
                    evaluations_total bigint
                  ) AS $$
    BEGIN
        RETURN QUERY SELECT
            vc.source_id,
            vc.name,
            vc.rut,
            vc.email,
            vc.phone,
            boc.name,
            pc.name,
            MAX(sc.external_created_at)::text,
            COALESCE(count(sc.id), 0)
        FROM airflow.vendor_conform vc
            INNER JOIN airflow.branch_office_conform boc ON vc.branch_office_id = boc.source_id
            INNER JOIN airflow.plant_conform pc ON boc.plant_id = pc.source_id
            LEFT JOIN airflow.survey_conform sc on sc.vendor_id = vc.source_id
        WHERE vc.source_id IN
            (
              SELECT distinct ON (VEC.source_id) VEC.source_id FROM airflow.vendor_conform VEC
                    LEFT JOIN airflow.vendor_plant_conform VPC ON
                        substr(VEC.rut, 1, length(COALESCE(NULLIF(VEC.rut, ''), ' ')) - 1) = VPC.vendor_id :: TEXT
                    WHERE
                    VEC.job_id = jobid AND
                    SC.job_id = jobid AND
                    VPC.id IS NULL
        )
        AND vc.job_id = jobid
        AND boc.job_id = jobid
        AND pc.job_id = jobid
        AND sc.job_id = jobid
        GROUP BY vc.source_id,
            vc.name,
            vc.rut,
            vc.email,
            vc.phone,
            boc.name,
            pc.name
;
    RETURN;
    END;
$$ LANGUAGE plpgsql;
