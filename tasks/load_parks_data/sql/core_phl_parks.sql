CREATE OR REPLACE TABLE core.phl_parks AS
SELECT
  GENERATE_UUID() AS parks_id,
  *
FROM source.phl_parks;
