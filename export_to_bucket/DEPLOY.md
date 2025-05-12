# Deploy
```shell
gcloud functions deploy export_assessments_changes \
--gen2 \
--region=us-east4 \
--runtime=python312 \
--project=musa5090s25-team2 \
--source=export_to_bucket/ \
--entry-point=export_assessments_changes \
--service-account=data-pipeline-robot-claudia@musa5090s25-team2.iam.gserviceaccount.com \
--memory=1Gi \
--timeout=60s \
--trigger-http \
--no-allow-unauthenticated
```

# Test
```shell
gcloud functions call export_assessments_changes \
--project=musa5090s25-team2 \
--region=us-east4
```
