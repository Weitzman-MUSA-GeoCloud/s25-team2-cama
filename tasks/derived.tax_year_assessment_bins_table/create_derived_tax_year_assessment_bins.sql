CREATE OR REPLACE TABLE derived.tax_year_assessment_bins AS
WITH labeled AS (
  SELECT
    year AS tax_year,
    -- Lower bound: floor market_value to the nearest 10,000
    FLOOR(pa.market_value / 10000) * 10000 AS lower_bound,
    
    -- Upper bound: ceil market_value to the next 10,000
    (FLOOR(pa.market_value / 10000) + 1) * 10000 AS upper_bound
  FROM derived.current_assessments_model_training_data ca
  JOIN core.phl_opa_assessment pa
    ON ca.property_id = pa.parcel_number  -- Join on matching columns
  WHERE pa.market_value > 0
),
aggregated AS (
  SELECT
    tax_year,
    lower_bound,
    upper_bound,
    COUNT(*) AS property_count
  FROM labeled
  GROUP BY tax_year, lower_bound, upper_bound
)
SELECT *
FROM aggregated
ORDER BY lower_bound;
