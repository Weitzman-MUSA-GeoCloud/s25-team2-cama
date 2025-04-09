CREATE OR REPLACE TABLE core.phl_schools AS
SELECT
  GENERATE_UUID() AS school_id,
  *
FROM source.phl_schools;
