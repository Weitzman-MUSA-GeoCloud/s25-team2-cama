## Deploying

### _extract_phl_parks_:

```shell
gcloud functions deploy extract_phl_parks \
--gen2 \
--region=us-east4 \
--runtime=python312 \
--source=extract_parks_data/ \
--entry-point=extract_phl_parks \
--service-account=data-pipeline-robot-claudia@musa5090s25-team2.iam.gserviceaccount.com \
--memory=4Gi \
--timeout=240s \
--set-env-vars=RAW_DATA_BUCKET=musa5090s25-team2-raw_data \
--trigger-http \
--no-allow-unauthenticated
```

```shell
gcloud functions call extract_phl_parks
```
