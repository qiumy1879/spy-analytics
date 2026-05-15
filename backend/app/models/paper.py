from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.core.database import Base


class Paper(Base):
    """数据库模型：论文信息

    v0.1 - 数据分析版本：不包含摘要
    """

    __tablename__ = "papers"

    # 主键 ID，自增
    id = Column(Integer, primary_key=True, index=True)

    # arXiv 论文 ID，如 "2301.12345"
    paper_id = Column(String(50), nullable=False, unique=True, index=True)

    # 论文标题
    title = Column(Text, nullable=False)

    # 作者列表（JSON 字符串存储）
    authors = Column(Text)

    # 发表时间
    published_at = Column(DateTime)

    # arXiv 分类列表（JSON 字符串存储）
    categories = Column(Text)

    # 关键词/tags（JSON 字符串存储）
    keywords = Column(Text)

    # 数据来源，固定为 "arxiv"
    source = Column(String(50), nullable=False)

    # arXiv 页面 URL
    source_url = Column(Text)

    # PDF 下载链接
    pdf_url = Column(Text)

    # arXiv 最后更新时间
    last_updated = Column(DateTime)

    # 作者备注（可选）
    comments = Column(Text)

    # 期刊引用（可选）
    journal_ref = Column(Text)

    # 记录创建时间（自动设置）
    created_at = Column(DateTime, default=datetime.utcnow)

    # 记录更新时间（自动更新）
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
