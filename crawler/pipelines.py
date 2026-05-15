import logging
import json
import sys
import os

# 添加后端目录到 Python 路径，以便导入后端模块
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'backend'))

from sqlalchemy.orm import sessionmaker
from app.core.database import engine, Base
from app.models.paper import Paper

logger = logging.getLogger(__name__)


class PaperPipeline:
    """论文数据管道：将爬取的数据存储到 SQLite 数据库

    复用后端的 SQLAlchemy 模型
    """

    def __init__(self):
        self.Session = sessionmaker(bind=engine)

    def open_spider(self, spider):
        """爬虫启动时：创建数据库表"""
        Base.metadata.create_all(bind=engine)
        logger.info("PaperPipeline opened, database tables created if not exists")

    def close_spider(self, spider):
        """爬虫关闭时"""
        logger.info("PaperPipeline closed")

    def process_item(self, item, spider):
        """处理单个论文条目，存储到数据库"""
        session = self.Session()
        try:
            # 检查论文是否已存在
            existing_paper = session.query(Paper).filter_by(paper_id=item['paper_id']).first()
            
            if existing_paper:
                # 更新现有论文
                existing_paper.title = item['title']
                existing_paper.authors = item['authors']
                existing_paper.published_at = item['published_at']
                existing_paper.categories = item['categories']
                existing_paper.keywords = item['keywords']
                existing_paper.source_url = item['source_url']
                existing_paper.pdf_url = item['pdf_url']
                existing_paper.last_updated = item['last_updated']
                existing_paper.comments = item['comments']
                existing_paper.journal_ref = item['journal_ref']
                logger.info(f"Updated paper: {item['paper_id']}")
            else:
                # 创建新论文
                paper = Paper(
                    paper_id=item['paper_id'],
                    title=item['title'],
                    authors=item['authors'],
                    published_at=item['published_at'],
                    categories=item['categories'],
                    keywords=item['keywords'],
                    source=item['source'],
                    source_url=item['source_url'],
                    pdf_url=item['pdf_url'],
                    last_updated=item['last_updated'],
                    comments=item['comments'],
                    journal_ref=item['journal_ref']
                )
                session.add(paper)
                logger.info(f"Created paper: {item['paper_id']}")
            
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Error processing paper {item.get('paper_id')}: {e}")
            raise
        finally:
            session.close()
        
        return item
