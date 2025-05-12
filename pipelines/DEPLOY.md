# Deploy pipeline
```shell
gcloud workflows deploy main-processing-pipeline \
--project=musa5090s25-team2 \
--location=us-east4 \
--source=main-processing-pipeline.yaml \
--service-account=data-pipeline-robot-claudia@musa5090s25-team2.iam.gserviceaccount.com
```

# Schedule pipeline run
```shell
gcloud scheduler jobs create http main-processing-pipeline \
--project=musa5090s25-team2 \
--location=us-east4 \
--schedule='0 9 * * 1' \
--time-zone='America/New_York' \
--uri='https://workflowexecutions.googleapis.com/v1/projects/musa5090s25-team2/locations/us-east4/workflows/main-processing-pipeline/executions' \
--oauth-service-account-email='data-pipeline-robot-claudia@musa5090s25-team2.iam.gserviceaccount.com'
```

# Run pipeline
```shell
gcloud workflows run main-processing-pipeline \
--project=musa5090s25-team2 \
--location=us-east4
```