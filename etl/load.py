import pandas as pd
import json
from typing import Optional


class DataLoader:
    @staticmethod
    def save_to_csv(df: pd.DataFrame, filename: str):
        df.to_csv(filename, index=False, encoding='utf-8')

    @staticmethod
    def save_to_json(data: dict, filename: str):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @staticmethod
    def generate_salary_report(stats: dict, output_path: str = 'salary_report.json'):
        DataLoader.save_to_json(stats, output_path)

