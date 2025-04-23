## Deploying

### extract_opa_assessment:

```shell
gcloud functions deploy extract_opa_assessment `
--gen2 `
--region=us-east4 `
--runtime=python312 `
--source=. `
--entry-point=extract_opa_assessment `
--service-account=data-pipeline-user@musa5090s25-team2.iam.gserviceaccount.com `
--memory=4Gi `
--timeout=300s `
--set-env-vars=RAW_DATA_BUCKET=musa5090s25-team2-raw_data `
--trigger-http `
--no-allow-unauthenticated
```

```shell
gcloud functions call extract_opa_assessment --region=us-east4
```