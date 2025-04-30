```shell
gcloud functions deploy generate-style-metadata \
  --gen2 \
  --region=us-east4 \
  --runtime=python310 \
  --source=generate_style_metadata/ \
  --entry-point=process_geojson \
  --service-account=data-pipeline-robot-claudia@musa5090s25-team2.iam.gserviceaccount.com \
  --memory=4Gi \
  --timeout=540s \
  --trigger-http \
  --no-allow-unauthenticated
```

```shell
gcloud functions call generate-style-metadata --region=us-east4
```
