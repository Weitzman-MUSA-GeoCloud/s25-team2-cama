CREATE OR REPLACE TABLE core.phl_neighborhoods AS
SELECT
  GENERATE_UUID() AS neighborhood_id,
  *
FROM source.phl_neighborhoods;