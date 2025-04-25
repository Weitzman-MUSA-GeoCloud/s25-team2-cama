## Deploying

### _extract_phl_septa_:

```shell
gcloud functions deploy extract_phl_septa \
--gen2 \
--region=us-east4 \
--runtime=python312 \
--source=extract_septa_data/ \
--entry-point=extract_phl_septa \
--service-account=data-pipeline-robot-claudia@musa5090s25-team2.iam.gserviceaccount.com \
--memory=4Gi \
--timeout=540s \
--set-env-vars=RAW_DATA_BUCKET=musa5090s25-team2-raw_data \
--trigger-http \
--no-allow-unauthenticated
```

```shell
gcloud functions call extract_phl_septa
```
