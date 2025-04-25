CREATE OR REPLACE TABLE core.phl_septa AS
SELECT
  GENERATE_UUID() AS septa_id,
  *
FROM source.phl_septa;
