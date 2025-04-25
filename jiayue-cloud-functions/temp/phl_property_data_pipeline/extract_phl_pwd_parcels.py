from dotenv import load_dotenv
load_dotenv()

import os
import pathlib
import requests
from google.cloud import storage

DATA_DIR = pathlib.Path(__file__).parent / 'raw_data'

# Download the OPA PWD parcels data as a geojson
url = 'https://opendata.arcgis.com/datasets/84baed491de44f539889f2af178ad85c_0.geojson'
filename = DATA_DIR / 'phl_pwd_parcels.geojson'

response = requests.get(url)
response.raise_for_status()

with open(filename, 'wb') as f:
    f.write(response.content)

print(f'Downloaded {filename}')

# Upload the download file to cloud storage
bucket_name = os.getenv('RAW_DATA_BUCKET')
blobname = 'phl_pwd_parcels/phl_pwd_parcels.geojson'

storage_client = storage.Client()
bucket = storage_client.bucket(bucket_name)
blob = bucket.blob(blobname)
blob.upload_from_filename(filename)

print(f'Uploaded {filename} to gs://{bucket_name}/{blobname}')