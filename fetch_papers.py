"""
直接使用 arxiv 库采集论文数据
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

import arxiv
import json
import io
from datetime import datetime, timedelta, timezone
from backend.app.core.database import SessionLocal, engine, Base
from backend.app.models.paper import Paper

def safe_print(*args, **kwargs):
    """安全打印，处理Unicode编码问题"""
    # 先处理所有字符，确保安全
    text = ' '.join(str(arg) for arg in args)
    
    # 替换emoji为ASCII字符
    emoji_map = {
        '⏭️': '[SKIP]',
        '✅': '[OK]', 
        '❌': '[ERR]',
        '📊': '[STAT]',
        '🚀': '[START]',
        '📁': '[CAT]',
        '📅': '[DATE]',
        '🔢': '[NUM]',
        '\U0001f680': '[START]'
    }
    for emoji, replacement in emoji_map.items():
        text = text.replace(emoji, replacement)
    
    # 使用错误处理输出
    try:
        print(text, **kwargs)
    except UnicodeEncodeError:
        # 强制使用ASCII输出
        ascii_text = text.encode('ascii', errors='replace').decode('ascii')
        print(ascii_text, **kwargs)

def fetch_papers(categories=['cs.AI', 'cs.LG', 'cs.RO', 'cs.CV'], days_back=7, max_results=20):
    """采集 arXiv 论文"""
    
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        start_date = datetime.now(timezone.utc) - timedelta(days=days_back)
        
        total_count = 0
        duplicate_count = 0
        
        for category in categories:
            safe_print(f"\n{'='*60}")
            safe_print(f"正在处理分类：{category}")
            
            query = f"cat:{category}"
            
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.SubmittedDate,
                sort_order=arxiv.SortOrder.Descending
            )
            
            category_count = 0
            
            for result in search.results():
                # 检查是否已存在
                existing_paper = db.query(Paper).filter(Paper.paper_id == result.entry_id).first()
                
                if existing_paper:
                    safe_print(f"⏭️ 跳过已存在: {result.title}")
                    duplicate_count += 1
                    continue
                
                # 创建论文记录
                paper = Paper(
                    paper_id=result.entry_id,
                    title=result.title,
                    authors=json.dumps([str(a) for a in result.authors]),
                    categories=json.dumps(result.categories),
                    pdf_url=result.pdf_url,
                    published_at=result.published.replace(tzinfo=None) if result.published else None,
                    last_updated=result.updated.replace(tzinfo=None) if result.updated else None,
                    journal_ref=result.journal_ref,
                    source="arxiv",
                    source_url=result.entry_id
                )
                
                db.add(paper)
                db.commit()
                
                category_count += 1
                total_count += 1
                
                safe_print(f"✅ 添加: {result.title[:50]}...")
            
            safe_print(f"分类 {category} 完成，新增 {category_count} 篇")
        
        db.commit()
        
        safe_print(f"\n{'='*60}")
        safe_print(f"📊 爬取完成！")
        safe_print(f"📊 新增论文: {total_count} 篇")
        safe_print(f"📊 跳过重复: {duplicate_count} 篇")
        
    except Exception as e:
        safe_print(f"❌ 爬取过程中发生错误: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='采集 arXiv 论文数据')
    parser.add_argument('--categories', type=str, default='cs.AI,cs.LG,cs.RO,cs.CV',
                        help='要爬取的分类，用逗号分隔')
    parser.add_argument('--days', type=int, default=30,
                        help='时间范围（天）')
    parser.add_argument('--max', type=int, default=50,
                        help='每类最大论文数')
    
    args = parser.parse_args()
    
    categories = [c.strip() for c in args.categories.split(',')]
    
    safe_print(f"🚀 开始采集 arXiv 论文")
    safe_print(f"📁 分类: {categories}")
    safe_print(f"📅 时间范围: 最近 {args.days} 天")
    safe_print(f"🔢 每类最大: {args.max} 篇")
    
    fetch_papers(categories=categories, days_back=args.days, max_results=args.max)