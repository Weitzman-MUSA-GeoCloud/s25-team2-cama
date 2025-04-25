```shell
gcloud functions deploy run_sql_parks \
--gen2 \
--region=us-east4 \
--runtime=python312 \
--source=load_parks_data/ \
--entry-point=run_sql_parks \
--service-account=data-pipeline-robot-claudia@musa5090s25-team2.iam.gserviceaccount.com \
--memory=8Gi \
--timeout=480s \
--set-env-vars=DATA_LAKE_BUCKET=musa5090s25-team2-prepared_data,DATA_LAKE_DATASET=source,CORE_DATASET=core \
--trigger-http \
--no-allow-unauthenticated
  ```

```shell
gcloud functions call run_sql_parks --region=us-east4
```