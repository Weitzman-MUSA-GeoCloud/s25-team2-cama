CREATE OR REPLACE TABLE derived.current_assessment_bin AS
SELECT
-- Lower bound floor predicted_value to the nearest 10,000
FLOOR(ca.predicted_value / 10000) * 10000 AS lower_bound,
-- Upper bound ceil predicted_value to the next 10,000
CEIL(ca.predicted_value / 10000) * 10000 AS upper_bound,
-- Number of properties in each bin
COUNT(*) AS property_count
FROM derived.current_assessments ca
WHERE ca.predicted_value > 0
GROUP BY lower_bound, upper_bound
ORDER BY lower_bound;