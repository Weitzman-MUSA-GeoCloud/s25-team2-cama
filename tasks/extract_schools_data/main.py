from dotenv import load_dotenv
load_dotenv()

import os
import pathlib
import requests
import functions_framework
from google.cloud import storage

DIRNAME = pathlib.Path(__file__).parent
BUCKET_NAME = os.getenv('RAW_DATA_BUCKET')

SCHOOL_CATCHMENTS_URL = "https://services.arcgis.com/fLeGjb7u4uXqeF9q/arcgis/rest/services/SchoolDist_Catchments_ES/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"

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
def extract_phl_schools(request):
    """Cloud Function to extract Philadelphia school catchments data."""
    print('Extracting Philadelphia school catchments data...')
    extract_data(
        SCHOOL_CATCHMENTS_URL,
        DIRNAME / 'phl_schools.geojson',
        'phl_schools/phl_schools.geojson',
    )
    return f'✅ Downloaded to {DIRNAME / "phl_schools.geojson"} and uploaded to gs://{BUCKET_NAME}/phl_schools/phl_schools.geojson'
