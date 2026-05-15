from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.paper import Paper
from app.schemas.paper import PaperResponse, PaperCreate
from app.core.database import get_db
import json

router = APIRouter(
    prefix="/papers",
    tags=["papers"],
)


@router.get("/", response_model=List[PaperResponse])
def get_papers(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取论文列表"""
    query = db.query(Paper)
    
    if category:
        query = query.filter(Paper.categories.contains(category))
    
    papers = query.offset(skip).limit(limit).all()
    return papers


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
    
    return {
        "total_papers": total_papers,
        "categories": categories_count
    }
