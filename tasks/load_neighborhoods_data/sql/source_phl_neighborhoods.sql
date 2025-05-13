CREATE OR REPLACE EXTERNAL TABLE source.phl_neighborhoods
OPTIONS (
  format = 'JSON',
  uris = ['gs://musa5090s25-team2-prepared_data/tables/phl_neighborhoods/*.jsonl']
);
