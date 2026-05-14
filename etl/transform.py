import pandas as pd
import json
from typing import Dict, List, Optional


class DataTransformer:
    """数据转换器：处理和分析论文数据"""

    @staticmethod
    def parse_json_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
        """
        将 JSON 字符串列解析为实际数据

        Args:
            df: 输入 DataFrame
            column: 要解析的列名

        Returns:
            添加解析后数据的 DataFrame
        """
        df = df.copy()

        def parse_json(s):
            if pd.isna(s):
                return []
            try:
                return json.loads(s)
            except:
                return []

        df[f'{column}_parsed'] = df[column].apply(parse_json)
        return df

    @staticmethod
    def get_category_distribution(df: pd.DataFrame) -> Dict[str, int]:
        """
        获取分类分布统计

        Args:
            df: 论文 DataFrame

        Returns:
            分类到数量的映射
        """
        if 'categories_parsed' not in df.columns:
            df = DataTransformer.parse_json_column(df, 'categories')

        categories = []
        for cats in df['categories_parsed']:
            categories.extend(cats)

        return pd.Series(categories).value_counts().to_dict()

    @staticmethod
    def get_top_authors(df: pd.DataFrame, top_n: int = 20) -> Dict[str, int]:
        """
        获取发表论文最多的作者

        Args:
            df: 论文 DataFrame
            top_n: 返回前多少个作者

        Returns:
            作者到论文数的映射
        """
        if 'authors_parsed' not in df.columns:
            df = DataTransformer.parse_json_column(df, 'authors')

        authors = []
        for auths in df['authors_parsed']:
            authors.extend(auths)

        return pd.Series(authors).value_counts().head(top_n).to_dict()

    @staticmethod
    def get_papers_per_month(df: pd.DataFrame) -> pd.DataFrame:
        """
        获取每月论文数量

        Args:
            df: 论文 DataFrame

        Returns:
            按月统计的论文数量 DataFrame
        """
        df = df.copy()
        df['month'] = pd.to_datetime(df['published_at']).dt.to_period('M')
        return df.groupby('month').size().reset_index(name='count')
