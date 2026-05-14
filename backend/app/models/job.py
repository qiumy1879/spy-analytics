from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False)
    salary = Column(String(100))
    salary_min = Column(Float)
    salary_max = Column(Float)
    city = Column(String(100))
    district = Column(String(100))
    tags = Column(Text)
    description = Column(Text)
    company_size = Column(String(100))
    company_industry = Column(String(255))
    source = Column(String(100), nullable=False)
    source_url = Column(Text)
    published_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

