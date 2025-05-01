## Deploying

### _extract_phl_septa_:

```shell
gcloud functions deploy generate-clean-properties-geojson \
  --gen2 \
  --region=us-east4 \
  --runtime=python312 \
  --source=generate_property_geojson \
  --entry-point=generate_clean_properties_geojson \
  --service-account=data-pipeline-robot-claudia@musa5090s25-team2.iam.gserviceaccount.com \
  --memory=4GiB \
  --timeout=300s \
  --trigger-http \
  --no-allow-unauthenticated
```

```shell
gcloud functions call generate-clean-properties-geojson  --region=us-east4
```
