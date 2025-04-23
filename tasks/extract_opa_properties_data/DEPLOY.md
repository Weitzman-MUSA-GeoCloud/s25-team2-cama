## Deploying

### extract_opa_properties:

```shell
gcloud functions deploy extract_opa_properties `
--gen2 `
--region=us-east4 `
--runtime=python312 `
--source=. `
--entry-point=extract_opa_properties `
--service-account=data-pipeline-user@musa5090s25-team2.iam.gserviceaccount.com `
--memory=4Gi `
--timeout=240s `
--set-env-vars=RAW_DATA_BUCKET=musa5090s25-team2-raw_data `
--trigger-http `
--no-allow-unauthenticated
```

```shell
gcloud functions call extract_opa_properties --region=us-east4
```