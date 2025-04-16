CREATE OR REPLACE TABLE
  `derived.phl_opa_properties_clean` 
  CLUSTER BY geog AS

WITH 

# Select only needed variables
selected_data AS (
  SELECT
    `property_id`,
    `sale_price`,
    DATE(sale_date) AS sale_date,
    `category_code_description`,
    `building_code_description_new`,
    `exterior_condition`,
    `interior_condition`,
    `number_of_bathrooms`,
    `number_of_bedrooms`,
    `number_stories`,
    `total_area`,
    `year_built`,
    `zoning`,
    `owner_1`,
    `geog`
  FROM `musa5090s25-team2.core.phl_opa_properties`
),

# Take only residential properties
residential_only AS (
  SELECT *
  FROM selected_data
  WHERE category_code_description IN (
    'SINGLE FAMILY',
    'MULTI FAMILY',
    'MIXED USE',
    'APARTMENTS  > 4 UNITS'
  )
),

# Mark properties not sold at arms-length
add_sale_flags AS (
  SELECT *,
         CASE WHEN sale_price < 100 THEN 1 ELSE 0 END AS vlow_sale_price
  FROM residential_only
),

bundles AS (
  SELECT *,
         COUNT(*) OVER (
           PARTITION BY sale_date, CAST(sale_price AS BIGNUMERIC), owner_1
         ) AS bundle_count
  FROM add_sale_flags
),

# Mark records usable for model training
train_labeled AS (
  SELECT *,
       CASE 
         WHEN bundle_count = 1 AND sale_price >= 100 AND sale_date >= '2015-01-01' THEN TRUE
         ELSE FALSE
       END AS can_train
  FROM bundles
),

# Fix nulls coded as 0
fixed_nulls AS (
  SELECT *,
    NULLIF(building_code_description_new, "") as building_code_description_new_fixed,
    NULLIF(exterior_condition, "") as exterior_condition_fixed,
    NULLIF(interior_condition, "") as interior_condition_fixed,
    NULLIF(number_stories, 0) as number_stories_fixed,
    NULLIF(year_built, 0) as year_built_fixed,
    NULLIF(total_area, 0) as total_area_fixed
  FROM train_labeled
),

# Impute nulls for columns to be used in modeling;

# First, get most common value for following variables
building_code_description_new_value AS (
  SELECT building_code_description_new_fixed AS building_code_description_new_value
  FROM fixed_nulls
  GROUP BY building_code_description_new_fixed
  ORDER BY COUNT(building_code_description_new_fixed) DESC
  LIMIT 1
),

exterior_condition_value AS (
  SELECT exterior_condition_fixed AS exterior_condition_value
  FROM fixed_nulls
  GROUP BY exterior_condition_fixed
  ORDER BY COUNT(exterior_condition_fixed) DESC
  LIMIT 1
),

interior_condition_value AS (
  SELECT interior_condition_fixed AS interior_condition_value
  FROM fixed_nulls
  GROUP BY interior_condition_fixed
  ORDER BY COUNT(interior_condition_fixed) DESC
  LIMIT 1
),

number_of_bathrooms_value AS (
  SELECT number_of_bathrooms AS number_of_bathrooms_value
  FROM fixed_nulls
  GROUP BY number_of_bathrooms
  ORDER BY COUNT(number_of_bathrooms) DESC
  LIMIT 1
),

number_of_bedrooms_value AS (
  SELECT number_of_bedrooms AS number_of_bedrooms_value
  FROM fixed_nulls
  GROUP BY number_of_bedrooms
  ORDER BY COUNT(number_of_bedrooms) DESC
  LIMIT 1
),

number_stories_value AS (
  SELECT number_stories_fixed AS number_stories_value
  FROM fixed_nulls
  GROUP BY number_stories_fixed
  ORDER BY COUNT(number_stories_fixed) DESC
  LIMIT 1
),

year_built_value AS (
  SELECT year_built_fixed AS year_built_value
  FROM fixed_nulls
  GROUP BY year_built_fixed
  ORDER BY COUNT(year_built_fixed) DESC
  LIMIT 1
),

zoning_value AS (
  SELECT zoning AS zoning_value
  FROM fixed_nulls
  GROUP BY zoning
  ORDER BY COUNT(zoning) DESC
  LIMIT 1
),

# Use the average value for this variable
total_area_value AS (
  SELECT AVG(total_area_fixed) AS total_area_value
  FROM fixed_nulls
),

# Join imputation values to data
imputation_values_joined AS (
  SELECT *
  FROM fixed_nulls
  CROSS JOIN building_code_description_new_value
  CROSS JOIN exterior_condition_value
  CROSS JOIN interior_condition_value
  CROSS JOIN number_of_bathrooms_value
  CROSS JOIN number_of_bedrooms_value
  CROSS JOIN number_stories_value
  CROSS JOIN year_built_value
  CROSS JOIN zoning_value
  CROSS JOIN total_area_value
),

# Coalesce in imputed values and select final columns
imputed AS (
  SELECT
    property_id,
    can_train,
    sale_price,
    sale_date,
    category_code_description,
    COALESCE(building_code_description_new_fixed, building_code_description_new_value) AS building_code_description_new,
    COALESCE(exterior_condition_fixed, exterior_condition_value) AS exterior_condition,
    COALESCE(interior_condition_fixed, interior_condition_value) AS interior_condition,
    COALESCE(number_of_bathrooms, number_of_bathrooms_value) AS number_of_bathrooms,
    COALESCE(number_of_bedrooms, number_of_bedrooms_value) AS number_of_bedrooms,
    COALESCE(number_stories_fixed, number_stories_value) AS number_stories,
    COALESCE(year_built_fixed, year_built_value) AS year_built,
    COALESCE(total_area_fixed, total_area_value) AS total_area,
    COALESCE(zoning, zoning_value) AS zoning,
    geog
  FROM imputation_values_joined
),

# Recast types
ready AS (
  SELECT
    property_id,
    can_train,
    sale_price,
    sale_date,
    category_code_description,
    building_code_description_new,
    CAST(exterior_condition AS STRING) AS exterior_condition,
    CAST(interior_condition AS STRING) AS interior_condition,
    CAST(number_of_bathrooms AS STRING) AS number_of_bathrooms,
    CAST(number_of_bedrooms AS STRING) AS number_of_bedrooms,
    CAST(number_stories AS STRING) AS number_stories,
    CAST(year_built AS INTEGER) AS year_built,
    total_area,
    zoning,
    ST_GEOGFROMTEXT(geog) as geog,
  FROM imputed
)

select * 
from ready;