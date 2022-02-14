CREATE OR REPLACE PROCEDURE create_survey_analysis(create_date timestamp without time zone, survey_id uuid, analysis_id uuid)
language plpgsql
as $$
declare
begin
    raise notice 'Attempting to insert %', analysis_id;
    INSERT INTO public.survey_analysis (id, created_at, updated_at, survey_id) VALUES (
        analysis_id,
        create_date,
        create_date,
        survey_id
    );
END; $$
