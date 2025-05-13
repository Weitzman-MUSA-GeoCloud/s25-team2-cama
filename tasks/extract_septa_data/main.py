from dotenv import load_dotenv
import os
import pathlib
import requests
import json
from flask import Flask, request  # Ensure Flask is used for HTTP
from google.cloud import storage

load_dotenv()

app = Flask(__name__)  # Use Flask to handle HTTP requests

DIRNAME = pathlib.Path(__file__).parent
BUCKET_NAME = os.getenv('RAW_DATA_BUCKET')

HIGH_SPEED_URL = "https://opendata.arcgis.com/api/v3/datasets/af52d74b872045d0abb4a6bbbb249453_0/downloads/data?format=geojson&spatialRefId=4326"
TROLLEY_URL = "https://opendata.arcgis.com/api/v3/datasets/dd2afb618d804100867dfe0669383159_0/downloads/data?format=geojson&spatialRefId=4326"
MERGED_FILENAME = DIRNAME / "phl_septa.geojson"
BLOBNAME = "phl_septa/merged_septa.geojson"

@app.route("/", methods=["GET", "POST"])  # Handle both GET and POST requests
def extract_phl_septa(request):  # Accept 'request' as argument
    """Extracts, merges, and uploads SEPTA data."""
    def download_geojson(url):
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    try:
        # Download datasets
        highspeed_data = download_geojson(HIGH_SPEED_URL)
        trolley_data = download_geojson(TROLLEY_URL)

        merged_features = []
        fid_counter = 1

        # Standardize and merge datasets
        for feature in highspeed_data["features"]:
            properties = feature["properties"]
            merged_features.append({
                "type": "Feature",
                "properties": {
                    "FID": fid_counter,
                    "Station": properties.get("Station"),
                    "Route": properties.get("Route"),
                    "Latitude": properties.get("Latitude"),
                    "Longitude": properties.get("Longitude"),
                    "Type": "High-Speed"
                },
                "geometry": feature["geometry"]
            })
            fid_counter += 1

        for feature in trolley_data["features"]:
            properties = feature["properties"]
            merged_features.append({
                "type": "Feature",
                "properties": {
                    "FID": fid_counter,
                    "Station": properties.get("StopName"),
                    "Route": properties.get("LineAbbr"),
                    "Latitude": properties.get("Lat"),
                    "Longitude": properties.get("Lon"),
                    "Type": "Trolley"
                },
                "geometry": feature["geometry"]
            })
            fid_counter += 1

        # Save merged data
        merged_data = {
            "type": "FeatureCollection",
            "name": "Philadelphia_SEPTA_Stations",
            "features": merged_features
        }
        with open(MERGED_FILENAME, "w") as f:
            json.dump(merged_data, f)

        # Upload to Google Cloud Storage
        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(BLOBNAME)
        blob.upload_from_filename(MERGED_FILENAME)

        return f"✅ Merged {len(merged_features)} stations and uploaded to gs://{BUCKET_NAME}/{BLOBNAME}", 200

    except Exception as e:
        return f"❌ Error: {str(e)}", 500
