from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from typing import List, Optional, Dict
from app.models.paper import Paper
from app.schemas.paper import PaperResponse, PaperCreate
from app.core.database import get_db
from app.smart_search import parse_chinese_query, get_search_suggestions, RESEARCH_DIRECTIONS
from datetime import datetime, timedelta
import json
import re
from collections import Counter

router = APIRouter(
    prefix="/papers",
    tags=["papers"],
)


@router.get("/", response_model=List[PaperResponse])
def get_papers(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    keyword: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    获取论文列表
    
    参数说明：
    - skip: 跳过多少条（分页用）
    - limit: 最多返回多少条
    - category: 按分类筛选（如 cs.AI）
    - keyword: 按关键词搜索（只搜索标题）
    """
    query = db.query(Paper)
    
    # 按分类筛选
    if category:
        query = query.filter(Paper.categories.contains(category))
    
    # 按关键词搜索（只搜索标题）
    if keyword:
        query = query.filter(Paper.title.contains(keyword))
    
    papers = query.offset(skip).limit(limit).all()
    return papers


@router.get("/research-directions")
def get_research_directions():
    """
    获取所有可用的研究方向列表
    
    Returns:
        研究方向列表
    """
    directions = []
    for name, data in RESEARCH_DIRECTIONS.items():
        directions.append({
            "name": name,
            "categories": data["categories"],
            "sub_directions": data["sub_directions"]
        })
    return {
        "directions": directions
    }


@router.get("/search/title")
def search_papers_by_title(
    keyword: str = Query(..., description="搜索关键词（只搜索标题）"),
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    根据论文标题搜索
    
    Args:
        keyword: 搜索关键词
        limit: 返回结果数量
    
    Returns:
        匹配的论文列表
    """
    papers = db.query(Paper).filter(
        Paper.title.contains(keyword)
    ).limit(limit).all()
    
    return {
        "keyword": keyword,
        "total": len(papers),
        "papers": papers
    }


@router.get("/stats/summary")
def get_summary_stats(db: Session = Depends(get_db)):
    """获取论文统计概览"""
    total_papers = db.query(Paper).count()
    
    # 统计各分类
    all_papers = db.query(Paper).all()
    categories_count = {}
    
    for paper in all_papers:
        if paper.categories:
            try:
                cats = json.loads(paper.categories)
                for cat in cats:
                    categories_count[cat] = categories_count.get(cat, 0) + 1
            except:
                pass
    
    # 统计最近一周的数据
    one_week_ago = datetime.now() - timedelta(days=7)
    recent_papers = db.query(Paper).filter(Paper.published >= one_week_ago).count()
    
    # 统计作者数量（去重）
    all_authors = set()
    for paper in all_papers:
        if paper.authors:
            try:
                authors = json.loads(paper.authors)
                for author in authors:
                    all_authors.add(author.strip())
            except:
                pass
    
    return {
        "total_papers": total_papers,
        "recent_papers_7d": recent_papers,
        "total_authors": len(all_authors),
        "categories": categories_count
    }


@router.get("/stats/trend")
def get_paper_trend(
    days: int = Query(30, description="查询天数"),
    db: Session = Depends(get_db)
):
    """获取论文数量时间趋势"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    results = db.query(
        func.date(Paper.published).label('date'),
        func.count(Paper.id).label('count')
    ).filter(
        Paper.published >= start_date
    ).group_by(
        func.date(Paper.published)
    ).order_by(
        func.date(Paper.published)
    ).all()
    
    trend_data = []
    for date, count in results:
        trend_data.append({
            "date": date.strftime("%Y-%m-%d"),
            "count": count
        })
    
    return {
        "trend": trend_data,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d")
    }


@router.get("/stats/categories")
def get_category_stats(db: Session = Depends(get_db)):
    """获取分类统计详情"""
    all_papers = db.query(Paper).all()
    total_papers = len(all_papers)
    
    category_stats = {}
    
    for paper in all_papers:
        if paper.categories:
            try:
                cats = json.loads(paper.categories)
                for cat in cats:
                    if cat not in category_stats:
                        category_stats[cat] = {
                            "count": 0,
                            "papers": []
                        }
                    category_stats[cat]["count"] += 1
                    category_stats[cat]["papers"].append({
                        "id": paper.paper_id,
                        "title": paper.title,
                        "published": paper.published.strftime("%Y-%m-%d") if paper.published else None
                    })
            except:
                pass
    
    sorted_categories = []
    for cat, stats in category_stats.items():
        sorted_categories.append({
            "category": cat,
            "count": stats["count"],
            "percentage": round(stats["count"] / total_papers * 100, 2),
            "sample_papers": stats["papers"][:5]
        })
    
    sorted_categories.sort(key=lambda x: x["count"], reverse=True)
    
    return {
        "total_categories": len(category_stats),
        "categories": sorted_categories
    }


@router.get("/stats/authors")
def get_author_stats(
    limit: int = Query(20, description="返回作者数量限制"),
    db: Session = Depends(get_db)
):
    """获取作者统计（按论文数量排名）"""
    all_papers = db.query(Paper).all()
    
    author_counter = Counter()
    author_papers = {}
    
    for paper in all_papers:
        if paper.authors:
            try:
                authors = json.loads(paper.authors)
                for author in authors:
                    author = author.strip()
                    author_counter[author] += 1
                    if author not in author_papers:
                        author_papers[author] = []
                    author_papers[author].append({
                        "id": paper.paper_id,
                        "title": paper.title,
                        "published": paper.published.strftime("%Y-%m-%d") if paper.published else None
                    })
            except:
                pass
    
    top_authors = []
    for author, count in author_counter.most_common(limit):
        top_authors.append({
            "author": author,
            "paper_count": count,
            "sample_papers": author_papers[author][:3]
        })
    
    return {
        "total_authors": len(author_counter),
        "top_authors": top_authors
    }


@router.get("/stats/keywords")
def get_keyword_stats(
    limit: int = Query(50, description="返回关键词数量限制"),
    db: Session = Depends(get_db)
):
    """获取关键词统计（从标题中提取）"""
    all_papers = db.query(Paper).all()
    
    common_keywords = [
        "learning", "deep", "neural", "network", "model", "based",
        "using", "method", "approach", "system", "algorithm", "data",
        "analysis", "framework", "application", "research", "study",
        "development", "design", "implementation", "evaluation",
        "optimization", "performance", "efficient", "novel", "new",
        "improved", "real-time", "scalable", "robust", "accurate",
        "AI", "ML", "DL", "NLP", "CV", "RL", "GAN", "transformer",
        "attention", "graph", "reinforcement", "supervised", "unsupervised",
        "semi-supervised", "self-supervised", "few-shot", "zero-shot",
        "fine-tuning", "pre-training", "transfer", "federated", "distributed",
        "embedding", "representation", "classification", "detection",
        "segmentation", "generation", "prediction", "recommendation",
        "clustering", "anomaly", "tracking", "matching", "retrieval",
        "summarization", "translation", "question", "answering", "dialogue"
    ]
    
    keyword_counter = Counter()
    
    for paper in all_papers:
        if paper.title:
            words = re.findall(r'[a-zA-Z][a-zA-Z0-9]*', paper.title.lower())
            for word in words:
                if len(word) >= 3 and word in common_keywords:
                    keyword_counter[word] += 1
    
    top_keywords = []
    for keyword, count in keyword_counter.most_common(limit):
        top_keywords.append({
            "keyword": keyword,
            "count": count
        })
    
    return {
        "total_keywords": len(keyword_counter),
        "top_keywords": top_keywords
    }


@router.get("/smart-search")
def smart_search(
    q: str = Query(..., description="中文搜索关键词，如：具身智能"),
    db: Session = Depends(get_db)
):
    """
    智能中文搜索接口
    
    输入中文关键词，自动识别研究方向，返回相关论文
    
    Args:
        q: 中文搜索关键词，如 "具身智能"
    
    Returns:
        包含搜索建议、子方向、论文结果的字典
    """
    # 解析中文查询
    search_data = parse_chinese_query(q)
    
    # 构建查询
    query = db.query(Paper)
    
    # 按分类筛选
    if search_data["categories"]:
        from sqlalchemy import or_
        category_filters = []
        for cat in search_data["categories"]:
            category_filters.append(Paper.categories.contains(cat))
        
        query = query.filter(or_(*category_filters))
    
    # 按关键词搜索（只搜索标题）
    if search_data["keywords"]:
        from sqlalchemy import or_
        keyword_filters = []
        for keyword in search_data["keywords"]:
            keyword_filters.append(Paper.title.ilike(f"%{keyword}%"))
        
        if keyword_filters:
            query = query.filter(or_(*keyword_filters))
    
    # 执行查询
    papers = query.limit(50).all()
    
    return {
        "query": q,
        "matched_direction": q if q in RESEARCH_DIRECTIONS else None,
        "categories": search_data["categories"],
        "sub_directions": search_data["sub_directions"],
        "papers": papers,
        "total_count": len(papers)
    }


@router.get("/search-suggestions")
def search_suggestions(
    q: str = Query("", description="用户输入的查询前缀"),
    _: Session = Depends(get_db)
):
    """
    获取搜索建议
    
    Args:
        q: 用户输入的查询前缀（可选）
    
    Returns:
        搜索建议列表
    """
    suggestions = get_search_suggestions(q)
    return {
        "suggestions": suggestions
    }


@router.get("/{paper_id}", response_model=PaperResponse)
def get_paper(paper_id: str, db: Session = Depends(get_db)):
    """根据 arXiv ID 获取单个论文"""
    paper = db.query(Paper).filter(Paper.paper_id == paper_id).first()
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    return paper


@router.post("/", response_model=PaperResponse)
def create_paper(paper: PaperCreate, db: Session = Depends(get_db)):
    """创建一个新论文记录"""
    # 检查是否已存在
    db_paper = db.query(Paper).filter(Paper.paper_id == paper.paper_id).first()
    if db_paper:
        raise HTTPException(status_code=400, detail="Paper already exists")
    
    db_paper = Paper(**paper.model_dump())
    db.add(db_paper)
    db.commit()
    db.refresh(db_paper)
    return db_paper


@router.put("/{paper_id}", response_model=PaperResponse)
def update_paper(paper_id: str, paper: PaperCreate, db: Session = Depends(get_db)):
    """更新论文记录"""
    db_paper = db.query(Paper).filter(Paper.paper_id == paper_id).first()
    if not db_paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    # 更新字段
    for key, value in paper.model_dump().items():
        setattr(db_paper, key, value)
    
    db.commit()
    db.refresh(db_paper)
    return db_paper


@router.delete("/{paper_id}")
def delete_paper(paper_id: str, db: Session = Depends(get_db)):
    """删除论文记录"""
    db_paper = db.query(Paper).filter(Paper.paper_id == paper_id).first()
    if not db_paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    db.delete(db_paper)
    db.commit()
    return {"message": "Paper deleted successfully"}
