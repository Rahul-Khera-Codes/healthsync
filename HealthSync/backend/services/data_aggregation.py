import psycopg2
from psycopg2 import sql
import requests
import json
from fastapi import HTTPException

class HealthDataAggregator:
    def __init__(self, db_config):
        self.connection = psycopg2.connect(**db_config)

    def fetch_data_from_source(self, source_url):
        try:
            response = requests.get(source_url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Error fetching data from {source_url}: {str(e)}")

    def aggregate_data(self, sources):
        aggregated_data = []
        for source in sources:
            data = self.fetch_data_from_source(source)
            aggregated_data.extend(data.get('results', []))
        return aggregated_data

    def save_to_database(self, data):
        with self.connection.cursor() as cursor:
            for entry in data:
                try:
                    cursor.execute(
                        sql.SQL("INSERT INTO health_data (field1, field2, field3) VALUES (%s, %s, %s) ON CONFLICT (id) DO NOTHING"),
                        (entry['field1'], entry['field2'], entry['field3'])
                    )
                except Exception as e:
                    raise HTTPException(status_code=500, detail=f"Error saving data to database: {str(e)}")
            self.connection.commit()

    def run_aggregation(self, sources):
        try:
            aggregated_data = self.aggregate_data(sources)
            self.save_to_database(aggregated_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Data aggregation failed: {str(e)}")
        finally:
            self.connection.close()