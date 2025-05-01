# Deploy
```shell
gcloud functions deploy predict_current_assessments \
--gen2 \
--region=us-east4 \
--runtime=python312 \
--project=musa5090s25-team2 \
--source=predict_current_assessments/ \
--entry-point=predict_current_assessments \
--service-account=data-pipeline-robot-claudia@musa5090s25-team2.iam.gserviceaccount.com \
--memory=4Gi \
--timeout=1000s \
--trigger-http \
--no-allow-unauthenticated
```

# Test
```shell
gcloud functions call predict_current_assessments \
--project=musa5090s25-team2 \
--region=us-east4
```
