```shell
gcloud functions deploy collate_assessments_changes \
--gen2 \
--region=us-east4 \
--runtime=python312 \
--project=musa5090s25-team2 \
--source=collate_assessments_changes/ \
--entry-point=collate_assessments_changes \
--service-account=data-pipeline-robot-claudia@musa5090s25-team2.iam.gserviceaccount.com \
--memory=4Gi \
--timeout=100s \
--set-env-vars=DERIVED_DATASET=derived \
--trigger-http \
--no-allow-unauthenticated
  ```

```shell
gcloud functions call collate_assessments_changes --region=us-east4
```