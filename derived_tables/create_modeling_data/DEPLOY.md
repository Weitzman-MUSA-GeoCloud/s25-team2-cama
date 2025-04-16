```shell
gcloud functions deploy run_create_modeling_data \
--gen2 \
--region=us-east4 \
--runtime=python312 \
--source=create_modeling_data/ \
--entry-point=run_create_modeling_data \
--service-account=data-pipeline-robot-claudia@musa5090s25-team2.iam.gserviceaccount.com \
--memory=8Gi \
--timeout=480s \
--set-env-vars=DERIVED_DATASET=derived \
--trigger-http \
--no-allow-unauthenticated
  ```

```shell
gcloud functions call run_create_modeling_data --region=us-east4
```