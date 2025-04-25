from dotenv import load_dotenv
load_dotenv()

import os
import json
import pathlib
from google.cloud import storage

RAW_DATA_DIR = pathlib.Path(__file__).parent / 'raw_data'
PREPARED_DATA_DIR = pathlib.Path(__file__).parent / 'prepared_data'

raw_filename = RAW_DATA_DIR / 'phl_pwd_parcels.geojson'
prepared_filename = PREPARED_DATA_DIR / 'phl_pwd_parcels.jsonl'

# Connecting to raw data bucket
bucket_name = os.getenv('RAW_DATA_BUCKET')
storage_client = storage.Client()
bucket = storage_client.bucket(bucket_name)

# Download the raw data from the bucket
raw_blobname = 'phl_pwd_parcels/phl_pwd_parcels.geojson'
blob = bucket.blob(raw_blobname)
blob.download_to_filename(raw_filename)
print(f'Downloaded to {raw_filename}')

# Load the data from the GeoJSON file
with open(raw_filename, 'r') as f:
    data = json.load(f)


# Write the data to a JSONL file
with open(prepared_filename, 'w') as f:
    for feature in data['features']:
        row = feature['properties']
        row['geog'] = (
            json.dumps(feature['geometry'])
            if feature['geometry'] and feature['geometry']['coordinates']
            else None
        )
        f.write(json.dumps(row) + '\n')

print(f'Processed data into {prepared_filename}')

# Connecting to prepared bucket
prep_bucket_name = os.getenv('PREPARE_DATA_BUCKET')
storage_client = storage.Client()
prep_bucket = storage_client.bucket(prep_bucket_name)

# Upload the prepared data to the prepared bucket
prepared_blobname = 'phl_pwd_parcels/phl_pwd_parcels.jsonl'
blob = prep_bucket.blob(prepared_blobname)
blob.upload_from_filename(prepared_filename)
print(f'Uploaded to {prepared_blobname}')