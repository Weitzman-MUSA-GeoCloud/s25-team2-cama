CREATE OR REPLACE EXTERNAL TABLE source.phl_parks
OPTIONS (
  format = 'JSON',
  uris = ['gs://musa5090s25-team2-prepared_data/tables/phl_parks/*.jsonl']
);
