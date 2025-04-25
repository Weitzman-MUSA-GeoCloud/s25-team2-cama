## Deploying Instructions

*extract_phl_opa_properties*:
```shell
gcloud functions deploy extract_phl_opa_properties `
    --gen2 `
    --region=us-east4 `
    --runtime=python312 `
    --source=. `
    --entry-point=extract_phl_opa_properties `
    --service-account=data-pipelne-jiayue-2024@musa5090s25-team2.iam.gserviceaccount.com `
    --memory=1Gi `
    --no-allow-unauthenticated `
    --trigger-http
