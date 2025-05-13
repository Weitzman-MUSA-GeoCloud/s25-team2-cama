```shell
gcloud functions deploy previous_generate-assessment-chart-configs \
--gen2 \
--region=us-east4 \
--runtime=python312 \
--source=previous_generate_assessment_chart/ \
--entry-point=previous_generate_assessment_chart_configs \
--service-account=data-pipeline-robot-claudia@musa5090s25-team2.iam.gserviceaccount.com \
--memory=4Gi \
--timeout=240s \
--trigger-http \
--no-allow-unauthenticated
```

```shell
gcloud functions call previous_generate-assessment-chart-configs --region=us-east4
```
