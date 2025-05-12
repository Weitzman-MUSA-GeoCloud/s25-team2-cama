CREATE OR REPLACE TABLE core.phl_opa_assessment_address AS
SELECT
  phl_opa_assessment.*,
  phl_opa_properties.location
FROM core.phl_opa_assessment
LEFT JOIN core.phl_opa_properties
ON phl_opa_assessment.parcel_number = phl_opa_properties.parcel_number;