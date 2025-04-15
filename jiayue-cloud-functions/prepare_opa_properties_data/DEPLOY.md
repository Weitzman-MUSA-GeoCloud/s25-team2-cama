```shell
gcloud functions deploy prepare_opa_properties `
  --gen2 `
  --region=us-east4 `
  --runtime=python312 `
  --source=. `
  --entry-point=prepare_opa_properties `
  --service-account=data-pipeline-user@musa5090s25-team2.iam.gserviceaccount.com `
  --memory=8Gi `
  --timeout=240s `
  --set-env-vars=RAW_DATA_BUCKET=musa5090s25-team2-raw_data `
  --set-env-vars=PREPARED_DATA_BUCKET=musa5090s25-team2-prepared_data `
  --trigger-http `
  --no-allow-unauthenticated
  ```

```shell
gcloud functions call prepare_opa_properties --region=us-east4
```