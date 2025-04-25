```shell
gcloud functions deploy create_tax_year_assessments `
--gen2 `
--region=us-east4 `
--runtime=python312 `
--source=. `
--entry-point=create_tax_year_assessments `
--service-account=data-pipeline-robot-claudia@musa5090s25-team2.iam.gserviceaccount.com `
--memory=8Gi `
--timeout=480s `
--set-env-vars=RAW_DATA_BUCKET=musa5090s25-team2-raw_data `
--trigger-http `
--no-allow-unauthenticated
```

```shell
gcloud functions call create_tax_year_assessments --region=us-east4
```
