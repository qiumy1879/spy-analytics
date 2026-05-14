# Spy Analytics - 数据采集与分析平台

## 项目简介

Spy Analytics 是一个数据采集与分析平台，爬取各类网站数据，提供数据分析和可视化功能。

## 技术栈

- **Web框架**: FastAPI
- **爬虫**: Scrapy
- **数据库**: PostgreSQL + Redis
- **容器化**: Docker + Docker Compose
- **CI/CD**: GitHub Actions
- **数据分析**: Pandas
- **可视化**: ECharts / Pyecharts (待实现)

## 项目结构

```
spy-analytics/
├── backend/              # FastAPI 后端
│   ├── app/
│   │   ├── api/          # API 路由
│   │   ├── core/         # 核心配置
│   │   ├── models/       # 数据库模型
│   │   ├── schemas/      # Pydantic 模型
│   │   └── main.py       # 入口文件
│   ├── tests/            # 测试
│   ├── requirements.txt
│   └── Dockerfile
├── crawler/              # 爬虫模块
│   ├── spiders/          # 爬虫
│   ├── pipelines.py      # 数据处理管道
│   ├── items.py          # 数据模型
│   └── settings.py       # Scrapy 配置
├── etl/                  # 数据处理
│   ├── extract.py
│   ├── transform.py
│   └── load.py
├── frontend/             # 前端（待实现）
├── docker/               # Docker 配置
├── scripts/              # 脚本
├── docs/                 # 文档
├── .github/
│   └── workflows/        # CI/CD
├── docker-compose.yml
├── .gitignore
└── README.md
```

## 快速开始

### 环境要求

- Python 3.11+
- Docker & Docker Compose

### 使用 Docker Compose 启动

```bash
docker-compose up -d
```

访问 http://localhost:8000 查看 API，http://localhost:8000/docs 查看 API 文档。

### 本地开发

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 .\venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 启动后端
cd backend
uvicorn app.main:app --reload
```

## 许可证

MIT
