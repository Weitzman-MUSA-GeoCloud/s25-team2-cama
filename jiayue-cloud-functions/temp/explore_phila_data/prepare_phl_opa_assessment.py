from dotenv import load_dotenv
load_dotenv()

import os
import csv
import json
import pathlib
import pyproj
from shapely import wkt
from google.cloud import storage

RAW_DATA_DIR = pathlib.Path(__file__).parent / 'raw_data'
PREPARED_DATA_DIR = pathlib.Path(__file__).parent / 'prepared_data'

raw_filename = RAW_DATA_DIR / 'phl_opa_assessment.csv'
prepared_filename = PREPARED_DATA_DIR / 'phl_opa_assessment.jsonl'

# Connecting to bucket
raw_bucket_name = os.getenv('RAW_DATA_BUCKET')
storage_client = storage.Client()
raw_bucket = storage_client.bucket(raw_bucket_name)

# Download the raw data from the bucket
raw_blobname = 'phl_opa_assessment/phl_opa_assessment.csv'
blob = raw_bucket.blob(raw_blobname)
blob.download_to_filename(raw_filename)
print(f'Downloaded to {raw_filename}')

# Load the data from the CSV file
with open(raw_filename, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    data = list(reader)

# Write the data to a JSONL file
with open(prepared_filename, 'w') as f:
    for row in data:
        f.write(json.dumps(row) + '\n')

print(f'Processed data into {prepared_filename}')

# Connecting to prepared bucket
prep_bucket_name = os.getenv('PREPARE_DATA_BUCKET')
storage_client = storage.Client()
prep_bucket = storage_client.bucket(prep_bucket_name)

# Upload the prepared data to the prepared bucket
prepared_blobname = 'phl_opa_assessment/phl_opa_assessment.jsonl'
blob = prep_bucket.blob(prepared_blobname)
blob.upload_from_filename(prepared_filename, timeout=300)
print(f'Uploaded to {prepared_blobname}')