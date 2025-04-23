CREATE OR REPLACE TABLE core.phl_opa_properties AS
SELECT 
parcel_number AS property_id,
*
FROM source.phl_opa_properties;