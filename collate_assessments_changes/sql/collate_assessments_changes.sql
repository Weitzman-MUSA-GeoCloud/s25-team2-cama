CREATE OR REPLACE TABLE
  `derived.assessments_changes` AS

WITH 

# Filter historic assessments to 2021-2025 only
filtered_historical_assessments_long AS (
  SELECT 
    property_id,
    year,
    market_value AS value
  FROM 
    `musa5090s25-team2.core.phl_opa_assessment`
  WHERE year >= 2021 and year < 2026
),

# Reshape to long format
filtered_historical_assessments_wide AS (
  SELECT *
  FROM filtered_historical_assessments_long
  PIVOT( MAX(value) FOR year IN (2021 AS value_2021, 2022 AS value_2022, 2023 AS value_2023, 2024 AS value_2024, 2025 AS value_2025))
  ORDER BY property_id
),

# Select only needed columns from current assessments
current_assessments_selected AS (
  SELECT 
    property_id AS property_id_current,
    predicted_value AS value_2026
  FROM `musa5090s25-team2.derived.current_assessments`
),

# Join to above to current assessments
assessments_joined AS (
  SELECT * EXCEPT (property_id_current)
  FROM filtered_historical_assessments_wide AS historic_assessments
  RIGHT JOIN current_assessments_selected AS current_assessments 
  ON historic_assessments.property_id=current_assessments.property_id_current
),

# Calculate change from 2024 to predicted, percentage and dollar amount
assessments_changes AS (
  SELECT *,
    value_2026 - value_2025 AS change_2025_2026_absolute,
    value_2026 / (value_2025 + 1) AS change_2025_2026_change_relative,
    value_2025 - value_2024 AS change_2024_2025_absolute,
    value_2025 / (value_2024 + 1) AS change_2024_2025_change_relative,
    value_2024 - value_2023 AS change_2023_2024_absolute,
    value_2024 / (value_2023 + 1) AS change_2023_2024_change_relative,
    value_2023 - value_2022 AS change_2022_2023_absolute,
    value_2023 / (value_2022 + 1) AS change_2022_2023_change_relative,
    value_2022 - value_2021 AS change_2021_2022_absolute,
    value_2022 / (value_2021 + 1) AS change_2021_2022_change_relative
  FROM assessments_joined
),

# Get property addresses
property_addresses AS (
  SELECT 
    property_id AS property_id_addresses,
    location
  FROM `musa5090s25-team2.core.phl_opa_properties`
),

# Join in property addresses
assessments_addresses AS (
  SELECT * EXCEPT (property_id_addresses)
  FROM assessments_changes
  LEFT JOIN property_addresses
  ON assessments_changes.property_id=property_addresses.property_id_addresses
)

SELECT * FROM assessments_addresses;
