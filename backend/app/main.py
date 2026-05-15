from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import papers
from app.core.database import engine, Base
from app.models import paper

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Spy Analytics API",
    description="arXiv 论文数据分析平台 API",
    version="0.1.0",
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


@app.get("/")
async def root():
    return {"message": "Welcome to Spy Analytics API", "version": "0.1.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
