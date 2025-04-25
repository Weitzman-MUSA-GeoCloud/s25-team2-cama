CREATE OR REPLACE TABLE derived.current_assessment_bin AS
SELECT
lower_bound,
upper_bound,
property_count
FROM derived.current_assessments;