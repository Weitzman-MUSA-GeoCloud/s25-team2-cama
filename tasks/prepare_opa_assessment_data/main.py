import os
import csv
import json
import pathlib
import pyproj
from shapely import wkt
import functions_framework
from google.cloud import storage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DIRNAME = pathlib.Path(__file__).parent

# Google Cloud Storage details
BUCKET_NAME_RAW = os.getenv('RAW_DATA_BUCKET')  # Bucket for raw data
BUCKET_NAME_PREPARED = os.getenv('PREPARED_DATA_BUCKET')  # Bucket for processed data

RAW_BLOBNAME = 'phl_opa_assessment/phl_opa_assessment.csv'  
PREPARED_BLOBNAME = 'tables/phl_opa_assessment/phl_opa_assessment.jsonl'  

@functions_framework.http
def prepare_opa_assessment(request):
    """Cloud Function to process Philadelphia OPA Assessment data."""
    print('Preparing Philadelphia OPA Assessment data...')

    storage_client = storage.Client()

    # Download raw data from Cloud Storage
    raw_filename = DIRNAME / 'phl_opa_assessment.csv'
    prepared_filename = DIRNAME / 'phl_opa_assessment.jsonl'

    bucket_raw = storage_client.bucket(BUCKET_NAME_RAW)
    blob_raw = bucket_raw.blob(RAW_BLOBNAME)
    blob_raw.download_to_filename(raw_filename)
    print(f'Downloaded raw data to {raw_filename}')

    # Load the data from the CSV file
    with open(raw_filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        data = list(reader)

    # Write the data to a JSONL file
    with open(prepared_filename, 'w') as f:
        for row in data:
            f.write(json.dumps(row) + '\n') 

    print(f'Processed data into {prepared_filename}')

    # Upload the processed file to the prepared data bucket
    bucket_prepared = storage_client.bucket(BUCKET_NAME_PREPARED)
    blob_prepared = bucket_prepared.blob(PREPARED_BLOBNAME)
    blob_prepared.upload_from_filename(prepared_filename)

    print(f'Uploaded processed data to gs://{BUCKET_NAME_PREPARED}/{PREPARED_BLOBNAME}')

    return f'Processed and uploaded to gs://{BUCKET_NAME_PREPARED}/{PREPARED_BLOBNAME}'