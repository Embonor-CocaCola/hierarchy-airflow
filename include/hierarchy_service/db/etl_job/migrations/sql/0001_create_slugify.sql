CREATE EXTENSION IF NOT EXISTS unaccent;

CREATE OR REPLACE FUNCTION slugify("value" TEXT, "allow_unicode" BOOLEAN) RETURNS TEXT AS $$
  WITH "normalized" AS (
    SELECT CASE
      WHEN "allow_unicode" THEN "value"
      ELSE unaccent("value")
    END AS "value"
  )
  SELECT regexp_replace(
    trim(
      lower(
        regexp_replace(
          "value",
          E'[^\\w\\s-]',
          '',
          'gi'
        )
      )
    ),
    E'[-\\s]+', '-', 'gi'
  ) FROM "normalized";
$$ LANGUAGE SQL STRICT IMMUTABLE;
