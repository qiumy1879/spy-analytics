import pandas as pd
import re
from typing import Tuple


class DataTransformer:
    @staticmethod
    def clean_salary(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        
        def parse_salary(salary_str):
            if pd.isna(salary_str):
                return None, None
            
            matches = re.findall(r'(\d+)', str(salary_str))
            if len(matches) >= 2:
                return float(matches[0]), float(matches[1])
            elif len(matches) == 1:
                return float(matches[0]), float(matches[0])
            return None, None
        
        df[['salary_min_parsed', 'salary_max_parsed']] = df['salary'].apply(
            lambda x: pd.Series(parse_salary(x))
        )
        
        return df

    @staticmethod
    def calculate_stats(df: pd.DataFrame) -> dict:
        stats = {}
        
        if 'salary_min_parsed' in df.columns and 'salary_max_parsed' in df.columns:
            df['avg_salary'] = (df['salary_min_parsed'] + df['salary_max_parsed']) / 2
            
            stats['salary_by_city'] = df.groupby('city')['avg_salary'].agg([
                'mean', 'median', 'count'
            ]).to_dict(orient='index')
            
            stats['top_tags'] = df['tags'].value_counts().head(20).to_dict()
        
        return stats

