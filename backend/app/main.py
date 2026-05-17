from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from app.api import papers
from app import crawler_manager
from app.core.database import engine, Base
from app.models import paper
import os

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Spy Analytics API",
    description="arXiv 论文分析平台 API",
    version="1.6.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/test")
async def test_page():
    """测试页面"""
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    test_path = os.path.join(static_dir, "test.html")
    if os.path.exists(test_path):
        return FileResponse(test_path)
    return {"message": "Test page not found"}


@app.get("/")
async def root():
    """返回中文前端界面"""
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    index_path = os.path.join(static_dir, "simple.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Welcome to Spy Analytics API", "version": "1.3.0"}


@app.get("/simple")
async def simple_page():
    """简化版前端界面"""
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    simple_path = os.path.join(static_dir, "simple.html")
    if os.path.exists(simple_path):
        return FileResponse(simple_path)
    return {"message": "Simple page not found"}


@app.get("/analytics")
async def analytics_page():
    """数据分析可视化页面"""
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    analytics_path = os.path.join(static_dir, "analytics.html")
    if os.path.exists(analytics_path):
        return FileResponse(analytics_path)
    return {"message": "Analytics page not found"}


# 包含路由（最后加载，避免覆盖）
app.include_router(papers.router)
app.include_router(crawler_manager.router)
