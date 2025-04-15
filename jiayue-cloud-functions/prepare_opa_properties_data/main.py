import os
import csv
import json
import pathlib
import pyproj
import functions_framework
from shapely import wkt
from google.cloud import storage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DIRNAME = pathlib.Path(__file__).parent

# Google Cloud Storage details
BUCKET_NAME_RAW = os.getenv('RAW_DATA_BUCKET')  # Bucket for raw data
BUCKET_NAME_PREPARED = os.getenv('PREPARED_DATA_BUCKET')  # Bucket for processed data

RAW_BLOBNAME = 'phl_opa_properties/phl_opa_properties.csv'  
PREPARED_BLOBNAME = 'tables/phl_opa_properties/phl_opa_properties.jsonl'  

@functions_framework.http
def prepare_opa_properties(request):
    """Cloud Function to process Philadelphia OPA Properties data."""
    print('Preparing Philadelphia OPA Properties data...')

    storage_client = storage.Client()

    # Download raw data from Cloud Storage
    raw_filename = DIRNAME / 'phl_opa_properties.csv'
    prepared_filename = DIRNAME / 'phl_opa_properties.jsonl'

    bucket_raw = storage_client.bucket(BUCKET_NAME_RAW)
    blob_raw = bucket_raw.blob(RAW_BLOBNAME)
    blob_raw.download_to_filename(raw_filename)
    print(f'Downloaded raw data to {raw_filename}')

    # Load the data from the CSV file
    with open(raw_filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        data = list(reader)

    # Set up the projection
    transformer = pyproj.Transformer.from_proj('epsg:2272', 'epsg:4326')

    # Write the data to a JSONL file
    with open(prepared_filename, 'w') as f:
        for i, row in enumerate(data):
            geom_wkt = row.pop('shape').split(';')[1]
            if geom_wkt == 'POINT EMPTY':
                row['geog'] = None
            else:
                geom = wkt.loads(geom_wkt)
                x, y = transformer.transform(geom.x, geom.y)
                row['geog'] = f'POINT({x} {y})'
            f.write(json.dumps(row) + '\n')

    print(f'Processed data into {prepared_filename}')

    # Upload the processed file to the prepared data bucket
    bucket_prepared = storage_client.bucket(BUCKET_NAME_PREPARED)
    blob_prepared = bucket_prepared.blob(PREPARED_BLOBNAME)
    blob_prepared.upload_from_filename(prepared_filename)

    print(f'Uploaded processed data to gs://{BUCKET_NAME_PREPARED}/{PREPARED_BLOBNAME}')

    return f'Processed and uploaded to gs://{BUCKET_NAME_PREPARED}/{PREPARED_BLOBNAME}'