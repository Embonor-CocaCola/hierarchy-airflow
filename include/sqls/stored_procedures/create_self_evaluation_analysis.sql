CREATE OR REPLACE PROCEDURE create_self_evaluation_analysis(create_date timestamp without time zone, survey_id uuid, analysis_id uuid)
language plpgsql
as $$
declare
begin
    raise notice 'Attempting to insert %', analysis_id;
    INSERT INTO public.self_evaluation_analysis (id, created_at, updated_at, self_evaluation_id) VALUES (
        analysis_id,
        create_date,
        create_date,
        survey_id
    );
END; $$
