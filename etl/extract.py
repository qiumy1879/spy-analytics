import psycopg2
import pandas as pd
from typing import Optional


class DataExtractor:
    def __init__(self, db_settings: Optional[dict] = None):
        self.db_settings = db_settings or {
            'dbname': 'jobspy',
            'user': 'admin',
            'password': 'password',
            'host': 'localhost',
            'port': '5432'
        }
        self.conn = None

    def connect(self):
        self.conn = psycopg2.connect(**self.db_settings)

    def extract_jobs(self, filters: Optional[dict] = None) -> pd.DataFrame:
        if not self.conn:
            self.connect()
        
        query = "SELECT * FROM jobs"
        if filters:
            conditions = []
            for key, value in filters.items():
                conditions.append(f"{key} = '{value}'")
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
        
        return pd.read_sql(query, self.conn)

    def close(self):
        if self.conn:
            self.conn.close()

