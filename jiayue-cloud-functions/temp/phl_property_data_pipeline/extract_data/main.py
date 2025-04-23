from dotenv import load_dotenv
load_dotenv()

import os
import pathlib
import requests
import functions_framework
from google.cloud import storage


DATA_DIR = pathlib.Path(__file__).parent

@functions_framework.http
def extract_phl_opa_properties(request):
    print('Extracting PHL OPA Properties data...')
    # Download the OPA Properties data as a CSV
    url = 'https://opendata-downloads.s3.amazonaws.com/opa_properties_public.csv'
    filename = DATA_DIR / 'phl_opa_properties.csv'

    response = requests.get(url)
    response.raise_for_status()

    with open(filename, 'wb') as f:
        f.write(response.content)

    print(f'Downloaded {filename}')

    # Upload the download file to cloud storage
    bucket_name = os.getenv('RAW_DATA_BUCKET')
    blobname = 'phl_opa_properties/phl_opa_properties.csv'

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blobname)
    blob.upload_from_filename(filename)

    print(f'Uploaded {filename} to gs://{bucket_name}/{blobname}')

    return f'Downloaded and uploaded gs://{bucket_name}/{blobname}'