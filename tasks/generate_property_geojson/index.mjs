import dotenv from 'dotenv';
import findConfig from 'find-config';
dotenv.config({ path: findConfig('.env') });

import { BigQuery } from '@google-cloud/bigquery';
import { Storage } from '@google-cloud/storage';

const bigqueryClient = new BigQuery();

export const generate_clean_properties_geojson = async (req, res) => {
    const storageClient = new Storage();
    
    console.log('Starting BigQuery query...');
    const sql = `
        SELECT
            property_id,
            value_2021,
            value_2022,
            value_2023,
            value_2024,
            value_2025,
            value_2026,
            change_2025_2026_absolute,
            change_2025_2026_change_relative,
            change_2024_2025_absolute,
            change_2024_2025_change_relative,
            change_2023_2024_absolute,
            change_2023_2024_change_relative,
            change_2022_2023_absolute,
            change_2022_2023_change_relative,
            change_2021_2022_absolute,
            change_2021_2022_change_relative,
            location,
            ST_AsGeoJSON(parcel_geog) AS geometry
        FROM derived.assessments_with_parcels
        WHERE parcel_geog IS NOT NULL
    `;

    try {
        const [rows] = await bigqueryClient.query(sql);
        console.log(`Retrieved ${rows.length} records`);

        // Build valid GeoJSON features
        const features = rows
            .filter(row => row.geometry)
            .map(row => ({
                type: 'Feature',
                properties: {
                    property_id: row.property_id,
                    value_2021: row.value_2021,
                    value_2022: row.value_2022,
                    value_2023: row.value_2023,
                    value_2024: row.value_2024,
                    value_2025: row.value_2025,
                    value_2026: row.value_2026,
                    change_2025_2026_absolute: row.change_2025_2026_absolute,
                    change_2025_2026_change_relative: row.change_2025_2026_change_relative,
                    change_2024_2025_absolute: row.change_2024_2025_absolute,
                    change_2024_2025_change_relative: row.change_2024_2025_change_relative,
                    change_2023_2024_absolute: row.change_2023_2024_absolute,
                    change_2023_2024_change_relative: row.change_2023_2024_change_relative,
                    change_2022_2023_absolute: row.change_2022_2023_absolute,
                    change_2022_2023_change_relative: row.change_2022_2023_change_relative,
                    change_2021_2022_absolute: row.change_2021_2022_absolute,
                    change_2021_2022_change_relative: row.change_2021_2022_change_relative,
                    address: row.location
                },
                geometry: JSON.parse(row.geometry)
            }));

        const featureCollection = {
            type: 'FeatureCollection',
            features: features
        };

        console.log('Initiating GCS upload...');
        const bucket = storageClient.bucket('musa5090s25-team2-temp_data');
        const file = bucket.file('property-tile-info.geojson');
        await file.save(JSON.stringify(featureCollection), {
            contentType: 'application/geo+json'
        });
        
        console.log('Operation completed successfully');
        res.status(200).json({
            message: 'GeoJSON data processed and uploaded to GCS',
            featureCount: features.length
        });
    } catch (error) {
        console.error('Error:', error);
        res.status(500).json({
            error: error.message,
            stack: process.env.NODE_ENV === 'development' ? error.stack : undefined
        });
    }
};
