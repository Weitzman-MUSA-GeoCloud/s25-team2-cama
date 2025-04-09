from dotenv import load_dotenv
load_dotenv()

import os
import pathlib
import requests
import functions_framework
from google.cloud import storage

DIRNAME = pathlib.Path(__file__).parent
BUCKET_NAME = os.getenv('RAW_DATA_BUCKET')

PARKS_URL = "https://opendata.arcgis.com/datasets/d52445160ab14380a673e5849203eb64_0.geojson"

def extract_data(url, filename, blobname):
    """Downloads a file from a URL and uploads it to Cloud Storage."""
    response = requests.get(url)
    response.raise_for_status()

    with open(filename, 'wb') as f:
        f.write(response.content)

    print(f'✅ Downloaded {filename}')

    # Upload to Cloud Storage
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(blobname)
    blob.upload_from_filename(filename)

    print(f'✅ Uploaded {blobname} to gs://{BUCKET_NAME}')


@functions_framework.http
def extract_phl_parks(request):
    """Cloud Function to extract Philadelphia parks data."""
    print('Extracting Philadelphia parks data...')
    extract_data(
        PARKS_URL,
        DIRNAME / 'phl_parks.geojson',
        'phl_parks/phl_parks.geojson',
    )
    return f'✅ Downloaded to {DIRNAME / "phl_parks.geojson"} and uploaded to gs://{BUCKET_NAME}/phl_parks/phl_parks.geojson'