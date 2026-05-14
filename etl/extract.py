import psycopg2
import pandas as pd
from typing import Optional, List


class DataExtractor:
    """数据提取器：从数据库提取论文数据"""

    def __init__(self, db_settings: Optional[dict] = None):
        self.db_settings = db_settings or {
            'dbname': 'spy_analytics',
            'user': 'admin',
            'password': 'password',
            'host': 'localhost',
            'port': '5432'
        }
        self.conn = None

    def connect(self):
        """连接数据库"""
        self.conn = psycopg2.connect(**self.db_settings)

    def extract_papers(self, filters: Optional[dict] = None) -> pd.DataFrame:
        """
        提取论文数据

        Args:
            filters: 过滤条件字典，如 {'category': 'cs.AI'}

        Returns:
            DataFrame 包含论文数据
        """
        if not self.conn:
            self.connect()

        query = "SELECT * FROM papers"
        params = []

        if filters:
            conditions = []
            for key, value in filters.items():
                conditions.append(f"{key} = %s")
                params.append(value)
            if conditions:
                query += " WHERE " + " AND ".join(conditions)

        return pd.read_sql(query, self.conn, params=tuple(params))

    def extract_papers_by_category(self, category: str) -> pd.DataFrame:
        """
        按分类提取论文

        Args:
            category: arXiv 分类，如 'cs.AI'

        Returns:
            DataFrame 包含该分类的论文数据
        """
        if not self.conn:
            self.connect()

        query = """
            SELECT * FROM papers
            WHERE categories LIKE %s
            OR categories LIKE %s
        """
        return pd.read_sql(
            query,
            self.conn,
            params=(f'%{category}%', f'%{category}%')
        )

    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()
