```shell
gcloud functions deploy prepare_phl_neighborhoods \
  --gen2 \
  --region=us-east4 \
  --runtime=python312 \
  --source=prepare_neighborhoods_data/ \
  --entry-point=prepare_phl_neighborhoods \
  --service-account=data-pipeline-robot-claudia@musa5090s25-team2.iam.gserviceaccount.com \
  --memory=4Gi \
  --timeout=240s \
  --set-env-vars=RAW_DATA_BUCKET=musa5090s25-team2-raw_data,PREPARED_DATA_BUCKET=musa5090s25-team2-prepared_data \
  --trigger-http \
  --no-allow-unauthenticated
  ```

```shell
gcloud functions call prepare_phl_neighborhoods
```