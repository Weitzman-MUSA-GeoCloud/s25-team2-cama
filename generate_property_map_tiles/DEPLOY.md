## Deploying

### _extract_phl_septa_:

```shell
gcloud run jobs deploy generate-vector-tiles-job \
  --image us-east4-docker.pkg.dev/musa5090s25-team2/cloud-run-source-deploy/generate-property-map-tiles-job:latest \
  --region us-east4 \
  --project musa5090s25-team2 \
  --service-account data-pipeline-robot-claudia@musa5090s25-team2.iam.gserviceaccount.com \
  --memory 1Gi \
  --max-retries 0 \
  --execute-now

gcloud builds submit /Users/claudia/Documents/GitHub/s25-team2-cama/generate_property_map_tiles \
  --tag=gcr.io/musa5090s25-team2/generate-property-map-tiles

gcloud beta run jobs delete generate-property-map-tiles --region us-east4

gcloud beta run jobs create generate-property-map-tiles \
  --image gcr.io/musa5090s25-team2/generate-property-map-tiles \
  --service-account data-pipeline-robot-claudia@musa5090s25-team2.iam.gserviceaccount.com \
  --cpu 4 \
  --memory 4Gi \
  --region us-east4

gcloud beta run jobs \
  execute generate-property-map-tiles \
  --region us-east4
```


//  --command="/workspace/script.sh" \
```shell
gcloud run jobs execute generate-property-map-tiles-job --region us-east4
```
