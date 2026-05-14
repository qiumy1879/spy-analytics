from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class PaperBase(BaseModel):
    """论文基础数据模型"""

    paper_id: str
    title: str
    authors: Optional[str] = None  # JSON 字符串
    published_at: Optional[datetime] = None
    categories: Optional[str] = None  # JSON 字符串
    keywords: Optional[str] = None  # JSON 字符串
    source: str = "arxiv"
    source_url: Optional[str] = None
    pdf_url: Optional[str] = None
    last_updated: Optional[datetime] = None
    comments: Optional[str] = None
    journal_ref: Optional[str] = None


class PaperCreate(PaperBase):
    """创建论文请求模型"""

    pass


class PaperUpdate(PaperBase):
    """更新论文请求模型"""

    pass


class PaperResponse(PaperBase):
    """论文响应模型"""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
