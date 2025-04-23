from dotenv import load_dotenv
load_dotenv()

import os
from google.cloud import bigquery

bucket_name = os.getenv('PREPARE_DATA_BUCKET')
dataset_name = os.getenv('SOURCE_DATASET')

# Load the data into Bigquery as an external table
prepared_blobname = 'phl_opa_properties/phl_opa_properties.jsonl'
table_name = 'phl_opa_properties'
table_uri = f'gs://{bucket_name}/{prepared_blobname}'

create_table_query = f'''
CREATE OR REPLACE EXTERNAL TABLE {dataset_name}.{table_name}
OPTIONS (
    format = 'JSON',
    uris = ['{table_uri}']
)
'''

bigquery_client = bigquery.Client()
bigquery_client.query_and_wait(create_table_query)
print(f'Loaded {table_uri} into {dataset_name}.{table_name}')