import psycopg2
from psycopg2.extras import RealDictCursor
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class ListingPipeline:
    def __init__(self, db_settings):
        self.db_settings = db_settings
        self.conn = None

    @classmethod
    def from_crawler(cls, crawler):
        db_settings = {
            'dbname': 'spy_analytics',
            'user': 'admin',
            'password': 'password',
            'host': 'localhost',
            'port': '5432'
        }
        return cls(db_settings)

    def open_spider(self, spider):
        try:
            self.conn = psycopg2.connect(**self.db_settings)
            self.create_table_if_not_exists()
        except Exception as e:
            logger.error(f"Database connection failed: {e}")

    def close_spider(self, spider):
        if self.conn:
            self.conn.close()

    def process_item(self, item, spider):
        if not self.conn:
            return item

        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO listings (
                        title, company, salary, salary_min, salary_max, 
                        city, district, tags, description, 
                        company_size, company_industry, 
                        source, source_url, published_at, created_at, updated_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT DO NOTHING
                """, (
                    item.get('title'),
                    item.get('company'),
                    item.get('salary'),
                    item.get('salary_min'),
                    item.get('salary_max'),
                    item.get('city'),
                    item.get('district'),
                    item.get('tags'),
                    item.get('description'),
                    item.get('company_size'),
                    item.get('company_industry'),
                    item.get('source'),
                    item.get('source_url'),
                    item.get('published_at'),
                    datetime.utcnow(),
                    datetime.utcnow()
                ))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Error inserting item: {e}")
        return item

    def create_table_if_not_exists(self):
        if not self.conn:
            return

        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS listings (
                        id SERIAL PRIMARY KEY,
                        title VARCHAR(255) NOT NULL,
                        company VARCHAR(255) NOT NULL,
                        salary VARCHAR(100),
                        salary_min FLOAT,
                        salary_max FLOAT,
                        city VARCHAR(100),
                        district VARCHAR(100),
                        tags TEXT,
                        description TEXT,
                        company_size VARCHAR(100),
                        company_industry VARCHAR(255),
                        source VARCHAR(100) NOT NULL,
                        source_url TEXT,
                        published_at TIMESTAMP,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
            self.conn.commit()
        except Exception as e:
            logger.error(f"Error creating table: {e}")

