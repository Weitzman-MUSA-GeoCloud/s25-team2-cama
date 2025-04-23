gcloud storage buckets describe gs://musa5090s25-team2-public --format="default(cors_config)"
gcloud storage buckets update gs://musa5090s25-team2-public --cors-file=cors-json-file.json