```shell
gcloud functions deploy run_sql_opa_properties_clean \
--gen2 \
--region=us-east4 \
--runtime=python312 \
--source=clean_opa_properties_table/ \
--entry-point=run_sql_opa_properties_clean \
--service-account=data-pipeline-robot-claudia@musa5090s25-team2.iam.gserviceaccount.com \
--memory=8Gi \
--timeout=480s \
--set-env-vars=DERIVED_DATASET=derived \
--trigger-http \
--no-allow-unauthenticated
  ```

```shell
gcloud functions call run_sql_opa_properties_clean --region=us-east4
```