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

# Deploy pipeline
```shell
gcloud workflows deploy run-model-pipeline \
--project=musa5090s25-team2 \
--location=us-east4 \
--source=run-model-pipeline.yaml \
--service-account=data-pipeline-robot-claudia@musa5090s25-team2.iam.gserviceaccount.com
```

# Schedule pipeline run
```shell
gcloud scheduler jobs create http run-model-pipeline \
--project=musa5090s25-team2 \
--location=us-east4 \
--schedule='0 11 * * 1' \
--time-zone='America/New_York' \
--uri='https://workflowexecutions.googleapis.com/v1/projects/musa5090s25-team2/locations/us-east4/workflows/run-model-pipeline/executions' \
--oauth-service-account-email='data-pipeline-robot-claudia@musa5090s25-team2.iam.gserviceaccount.com'
```

# Run pipeline
```shell
gcloud workflows run run-model-pipeline \
--project=musa5090s25-team2 \
--location=us-east4
```