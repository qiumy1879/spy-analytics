from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class JobBase(BaseModel):
    title: str
    company: str
    salary: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    city: Optional[str] = None
    district: Optional[str] = None
    tags: Optional[str] = None
    description: Optional[str] = None
    company_size: Optional[str] = None
    company_industry: Optional[str] = None
    source: str
    source_url: Optional[str] = None
    published_at: Optional[datetime] = None


class JobCreate(JobBase):
    pass


class JobUpdate(JobBase):
    pass


class JobResponse(JobBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

