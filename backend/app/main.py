from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
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
    description="arXiv 论文数据分析平台 API",
    version="1.3.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含路由
app.include_router(papers.router)
app.include_router(crawler_manager.router)


@app.get("/")
async def root():
    """返回中文前端界面"""
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Welcome to Spy Analytics API", "version": "1.2.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# 挂载静态文件目录（如果需要其他静态资源）
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
