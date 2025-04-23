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
def extract_phl_pwd_parcels(request):
    print('Extracting Philadelphia PWD Parcels data...')
    extract_data(
        'https://opendata.arcgis.com/datasets/84baed491de44f539889f2af178ad85c_0.geojson',
        DIRNAME / 'phl_pwd_parcels.geojson',
        'phl_pwd_parcels/phl_pwd_parcels.geojson',
    )
    return f'✅ Downloaded to {DIRNAME / "phl_pwd_parcels.geojson"} and uploaded to gs://{BUCKET_NAME}/raw/phl_pwd_parcels/phl_pwd_parcels.geojson'