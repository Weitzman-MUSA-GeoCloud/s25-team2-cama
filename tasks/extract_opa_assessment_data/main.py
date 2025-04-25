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
def extract_opa_assessment(request):
    print('Extracting Philadelphia OPA Assessment data...')
    extract_data(
        'https://opendata-downloads.s3.amazonaws.com/assessments.csv',
        DIRNAME / 'phl_opa_assessment.csv',
        'phl_opa_assessment/phl_opa_assessment.csv',
    )
    return f'✅ Downloaded to {DIRNAME / "phl_opa_assessment.csv"} and uploaded to gs://{BUCKET_NAME}/raw/phl_opa_assessment/phl_opa_assessment.csv'