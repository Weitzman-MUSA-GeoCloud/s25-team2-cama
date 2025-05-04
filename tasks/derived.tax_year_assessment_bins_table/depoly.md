```shell
gcloud functions deploy run_sql_derived_previous_assessments `
--gen2 `
--region=us-east4 `
--runtime=python312 `
--source=. `
--entry-point=run_sql_derived_previous_assessments `
--service-account=data-pipeline-robot-claudia@musa5090s25-team2.iam.gserviceaccount.com `
--memory=8Gi `
--timeout=480s `
--set-env-vars=RAW_DATA_BUCKET=musa5090s25-team2-raw_data `
--trigger-http `
--no-allow-unauthenticated
```

```shell
gcloud functions call run_sql_derived_previous_assessments --region=us-east4
```
