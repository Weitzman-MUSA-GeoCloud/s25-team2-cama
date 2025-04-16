/*
Read in cleaned opa properties table and join relevant variables from other tables
*/

CREATE OR REPLACE TABLE
  `derived.current_assessments_model_training_data` AS

WITH

--Load cleaned opa properties table
opa AS (
  SELECT * 
  FROM `musa5090s25-team2.derived.phl_opa_properties_clean`
),

--Load other data
neighborhoods AS (
  SELECT 
    MAPNAME as neighborhood,
    ST_GEOGFROMGEOJSON(geometry) as neighborhoods_geog
  FROM `musa5090s25-team2.core.phl_neighborhoods`
),

schools AS (
  SELECT
    ES_NAME as school,
    ST_GEOGFROMGEOJSON(geometry) as schools_geog
  FROM `musa5090s25-team2.core.phl_schools`
),

-- parks AS (
--   SELECT
--     ST_GEOGFROMGEOJSON(geometry) as geog
--   FROM `musa5090s25-team2.core.phl_parks`

-- ),

septa AS (
  SELECT
    ST_GEOGFROMGEOJSON(geometry) as geog
  FROM `musa5090s25-team2.core.phl_septa`
),

-- Spatial union of geographies to get distances from
-- parks_union AS (
--   SELECT ST_UNION_AGG(geog) as geog
--   FROM parks
-- ),

septa_union AS (
  SELECT ST_UNION_AGG(geog) as septa_geog
  FROM septa
),

-- Spatially join area labels to properties
opa_joined AS (
  SELECT *
    EXCEPT (neighborhoods_geog, schools_geog)
  FROM opa
  INNER JOIN neighborhoods
    ON ST_COVEREDBY(opa.geog, neighborhoods.neighborhoods_geog)
  INNER JOIN schools
    ON ST_COVEREDBY(opa.geog, schools.schools_geog)
),

-- Get distances to nearest points of interest
opa_distances AS (
  SELECT *
    EXCEPT (septa_geog),
    -- ST_DISTANCE(opa_joined.geog, parks_union.geog) as distance_to_nearest_park,
    ST_DISTANCE(opa_joined.geog, septa_union.septa_geog) as distance_to_nearest_septa
  FROM 
    opa_joined,
    -- parks_union,
    septa_union
)

SELECT *
FROM opa_distances;