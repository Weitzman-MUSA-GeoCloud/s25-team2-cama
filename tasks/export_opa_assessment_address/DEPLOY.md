## Deploying

### bigquery_extract:

```shell
gcloud functions deploy bigquery_extract `
--gen2 `
--region=us-east4 `
--runtime=python312 `
--source=. `
--entry-point=bigquery_extract `
--service-account=data-pipeline-user@musa5090s25-team2.iam.gserviceaccount.com `
--memory=8Gi `
--timeout=480s `
--trigger-http `
--no-allow-unauthenticated
```

```shell
gcloud functions call bigquery_extract --region=us-east4
```