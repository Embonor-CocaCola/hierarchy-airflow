UPDATE survey TARGET
SET skip_reason  = CASE
                       WHEN ans.values ->> 0 LIKE '%%encuentra con reja%%' THEN 'gated'
                       WHEN ans.values ->> 0 LIKE '%%encuentra cerrado%%' THEN 'closed'
                       ELSE 'INVALID_REASON'
    END,
    skips_survey = true
FROM answer ans
WHERE ans.survey_id = TARGET.id
  AND TARGET.skip_reason IS NULL
  AND (
                ans.values ->> 0 LIKE '%%encuentra con reja%%' OR
                ans.values ->> 0 LIKE '%%encuentra cerrado%%'
    )
;

ANALYZE survey;

WITH answer_counts AS (
    select count(a.id) ans_count,
           s.id        survey_id
    from survey s
             left join answer a on a.survey_id = s.id
    group by s.id
)
UPDATE survey TARGET
SET answer_count = ac.ans_count
from answer_counts ac
where ac.survey_id = TARGET.id
;
