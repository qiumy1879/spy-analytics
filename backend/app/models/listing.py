from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Listing(Base):
    """数据库模型：职位/列表信息
    
    这个类定义了 PostgreSQL 数据库中的 listings 表结构
    与 crawler 中的 ListingItem 对应，但增加了数据库管理字段
    """
    
    __tablename__ = "listings"
    
    # 主键 ID，自增
    id = Column(Integer, primary_key=True, index=True)
    
    # 职位标题，不能为空
    title = Column(String(255), nullable=False)
    
    # 公司名称，不能为空
    company = Column(String(255), nullable=False)
    
    # 原始薪资格式（字符串，如 "15-25K"）
    salary = Column(String(100))
    
    # 薪资下限（浮点数，便于统计）
    salary_min = Column(Float)
    
    # 薪资上限（浮点数，便于统计）
    salary_max = Column(Float)
    
    # 城市
    city = Column(String(100))
    
    # 区域
    district = Column(String(100))
    
    # 标签/技能（大文本）
    tags = Column(Text)
    
    # 职位描述（大文本）
    description = Column(Text)
    
    # 公司规模
    company_size = Column(String(100))
    
    # 公司行业
    company_industry = Column(String(255))
    
    # 数据来源（必填）
    source = Column(String(100), nullable=False)
    
    # 原始数据 URL
    source_url = Column(Text)
    
    # 发布时间
    published_at = Column(DateTime)
    
    # 记录创建时间（自动设置）
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 记录更新时间（自动更新）
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
