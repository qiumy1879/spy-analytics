import psycopg2
import logging
from datetime import datetime
import yaml
import os

logger = logging.getLogger(__name__)


class PaperPipeline:
    """论文数据管道：将爬取的数据存储到 PostgreSQL"""

    def __init__(self, db_settings):
        self.db_settings = db_settings
        self.conn = None

    @classmethod
    def from_crawler(cls, crawler):
        """从配置文件读取数据库设置"""
        config_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "config.yaml"
        )
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        db_settings = config.get('database', {})
        return cls(db_settings)

    def open_spider(self, spider):
        """爬虫启动时：连接数据库并创建表"""
        try:
            self.conn = psycopg2.connect(**self.db_settings)
            self.create_table_if_not_exists()
            logger.info("Database connected successfully")
        except Exception as e:
            logger.error(f"Database connection failed: {e}")

    def close_spider(self, spider):
        """爬虫关闭时：断开数据库连接"""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")

    def process_item(self, item, spider):
        """处理单个论文条目，存储到数据库"""
        if not self.conn:
            return item

        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO papers (
                        paper_id, title, authors, published_at,
                        categories, keywords, source, source_url, pdf_url,
                        last_updated, comments, journal_ref,
                        created_at, updated_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (paper_id) DO UPDATE SET
                        title = EXCLUDED.title,
                        authors = EXCLUDED.authors,
                        published_at = EXCLUDED.published_at,
                        categories = EXCLUDED.categories,
                        keywords = EXCLUDED.keywords,
                        source_url = EXCLUDED.source_url,
                        pdf_url = EXCLUDED.pdf_url,
                        last_updated = EXCLUDED.last_updated,
                        comments = EXCLUDED.comments,
                        journal_ref = EXCLUDED.journal_ref,
                        updated_at = EXCLUDED.updated_at
                """, (
                    item.get('paper_id'),
                    item.get('title'),
                    item.get('authors'),
                    item.get('published_at'),
                    item.get('categories'),
                    item.get('keywords'),
                    item.get('source', 'arxiv'),
                    item.get('source_url'),
                    item.get('pdf_url'),
                    item.get('last_updated'),
                    item.get('comments'),
                    item.get('journal_ref'),
                    datetime.utcnow(),
                    datetime.utcnow()
                ))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Error inserting paper {item.get('paper_id')}: {e}")
            self.conn.rollback()
        return item

    def create_table_if_not_exists(self):
        """如果表不存在则创建 papers 表"""
        if not self.conn:
            return

        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS papers (
                        id SERIAL PRIMARY KEY,
                        paper_id VARCHAR(50) UNIQUE NOT NULL,
                        title TEXT NOT NULL,
                        authors TEXT,
                        published_at TIMESTAMP,
                        categories TEXT,
                        keywords TEXT,
                        source VARCHAR(50) NOT NULL,
                        source_url TEXT,
                        pdf_url TEXT,
                        last_updated TIMESTAMP,
                        comments TEXT,
                        journal_ref TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                    CREATE INDEX IF NOT EXISTS idx_papers_paper_id ON papers(paper_id);
                    CREATE INDEX IF NOT EXISTS idx_papers_published_at ON papers(published_at);
                    CREATE INDEX IF NOT EXISTS idx_papers_source ON papers(source);
                """)
            self.conn.commit()
            logger.info("Table 'papers' ready")
        except Exception as e:
            logger.error(f"Error creating table: {e}")
