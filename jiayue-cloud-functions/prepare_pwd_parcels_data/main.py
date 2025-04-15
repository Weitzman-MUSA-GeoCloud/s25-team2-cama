import os
import json
import pathlib
import functions_framework
from google.cloud import storage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DIRNAME = pathlib.Path(__file__).parent

# Google Cloud Storage details
BUCKET_NAME_RAW = os.getenv('RAW_DATA_BUCKET')  # Bucket for raw data
BUCKET_NAME_PREPARED = os.getenv('PREPARED_DATA_BUCKET')  # Bucket for processed data

RAW_BLOBNAME = 'phl_pwd_parcels/phl_pwd_parcels.geojson'  
PREPARED_BLOBNAME = 'tables/phl_pwd_parcels/phl_pwd_parcels.jsonl'  

@functions_framework.http
def prepare_pwd_parcels(request):
    """Cloud Function to process Philadelphia PWD Parcels data."""
    print('Preparing Philadelphia PWD Parcels data...')

    storage_client = storage.Client()

    # Download raw data from Cloud Storage
    raw_filename = DIRNAME / 'phl_pwd_parcels.geojson'
    prepared_filename = DIRNAME / 'phl_pwd_parcels.jsonl'

    bucket_raw = storage_client.bucket(BUCKET_NAME_RAW)
    blob_raw = bucket_raw.blob(RAW_BLOBNAME)
    blob_raw.download_to_filename(raw_filename)
    print(f'Downloaded raw data to {raw_filename}')

    # Convert GeoJSON to JSONL
    with open(raw_filename, 'r') as geojson_file, open(prepared_filename, 'w') as jsonl_file:
        geojson_data = json.load(geojson_file)
        for feature in geojson_data['features']:
            row = feature['properties']
            row['geometry'] = json.dumps(feature['geometry'])  # Store geometry as a JSON string
            jsonl_file.write(json.dumps(row) + '\n')

    print(f'Processed data into {prepared_filename}')

    # Upload the processed file to the prepared data bucket
    bucket_prepared = storage_client.bucket(BUCKET_NAME_PREPARED)
    blob_prepared = bucket_prepared.blob(PREPARED_BLOBNAME)
    blob_prepared.upload_from_filename(prepared_filename)

    print(f'Uploaded processed data to gs://{BUCKET_NAME_PREPARED}/{PREPARED_BLOBNAME}')

    return f'Processed and uploaded to gs://{BUCKET_NAME_PREPARED}/{PREPARED_BLOBNAME}'