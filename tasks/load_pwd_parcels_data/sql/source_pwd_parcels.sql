CREATE OR REPLACE EXTERNAL TABLE source.phl_pwd_parcels
OPTIONS (
  format = 'JSON',
  uris = ['gs://musa5090s25-team2-prepared_data/tables/phl_pwd_parcels/*.jsonl']
);