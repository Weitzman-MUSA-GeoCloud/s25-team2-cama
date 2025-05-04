```shell
gcloud functions deploy run_sql_derived_current_assessment_bins `
--gen2 `
--region=us-east4 `
--runtime=python312 `
--source=. `
--entry-point=run_sql_derived_current_assessment_bins `
--service-account=data-pipeline-user@musa5090s25-team2.iam.gserviceaccount.com `
--memory=4Gi `
--timeout=480s `
--set-env-vars=DATA_LAKE_BUCKET=musa5090s25-team2-prepared_data `
--trigger-http `
--no-allow-unauthenticated
```

```shell
gcloud functions call run_sql_derived_current_assessment_bins --region=us-east4
```