from dotenv import load_dotenv
load_dotenv()

import os
import pathlib
import requests
from google.cloud import storage


DATA_DIR = pathlib.Path(__file__).parent / 'raw_data'

# Download the OPA Assessment data as a CSV
url = 'https://opendata-downloads.s3.amazonaws.com/assessments.csv'
filename = DATA_DIR / 'phl_opa_assessment.csv'

response = requests.get(url)
response.raise_for_status()

with open(filename, 'wb') as f:
    f.write(response.content)

print(f'Downloaded {filename}')

# Upload the download file to cloud storage
bucket_name = os.getenv('RAW_DATA_BUCKET')
blobname = 'phl_opa_assessment/phl_opa_assessment.csv'

storage_client = storage.Client()
bucket = storage_client.bucket(bucket_name)
blob = bucket.blob(blobname)
blob.upload_from_filename(filename, timeout=300)

print(f'Uploaded {filename} to gs://{bucket_name}/{blobname}')