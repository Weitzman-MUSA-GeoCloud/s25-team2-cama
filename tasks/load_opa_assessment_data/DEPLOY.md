```shell
gcloud functions deploy run_sql_opa_assessment `
--gen2 `
--region=us-east4 `
--runtime=python312 `
--source=. `
--entry-point=run_sql_opa_assessment `
--service-account=data-pipeline-user@musa5090s25-team2.iam.gserviceaccount.com `
--memory=8Gi `
--timeout=480s `
--set-env-vars=DATA_LAKE_BUCKET=musa5090s25-team2-prepared_data `
--set-env-vars=DATA_LAKE_DATASET=source `
--set-env-vars=CORE_DATASET=core `
--trigger-http `
--no-allow-unauthenticated
```

```shell
gcloud functions call run_sql_opa_assessment --region=us-east4
```