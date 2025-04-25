from dotenv import load_dotenv
load_dotenv()

import os
import pathlib
import requests
import functions_framework
from google.cloud import storage

DIRNAME = pathlib.Path(__file__).parent
BUCKET_NAME = os.getenv('RAW_DATA_BUCKET')


def extract_data(url, filename, blobname):
    response = requests.get(url)
    response.raise_for_status()

    with open(filename, 'wb') as f:
        f.write(response.content)

    print(f'✅ Downloaded {filename}')

    # Upload the downloaded file to cloud storage
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(blobname)
    blob.upload_from_filename(filename)

    print(f'✅ Uploaded {blobname} to gs://{BUCKET_NAME}')


@functions_framework.http
def extract_phl_neighborhoods(request):
    print('Extracting Philadelphia Neighborhoods data...')
    extract_data(
        'https://raw.githubusercontent.com/opendataphilly/open-geo-data/refs/heads/master/philadelphia-neighborhoods/philadelphia-neighborhoods.geojson',
        DIRNAME / 'phl_neighborhoods.geojson',
        'phl_neighborhoods/philadelphia_neighborhoods.geojson',
    )
    return f'✅ Downloaded to {DIRNAME / "phl_neighborhoods.geojson"} and uploaded to gs://{BUCKET_NAME}/raw/phl_neighborhoods/philadelphia_neighborhoods.geojson'
