# Spy Analytics - arXiv 论文分析平台

## 项目简介

Spy Analytics 是一个 arXiv 论文数据采集与分析平台，爬取 arXiv 论文数据，提供 API 接口和数据分析功能。

## 技术栈

- **Web框架**: FastAPI
- **爬虫**: Scrapy + arxiv.py
- **数据库**: SQLite
- **ORM**: SQLAlchemy
- **容器化**: Docker + Docker Compose (可选)

## 已实现功能 (v1.0.0)

✅ **后端 API**
- FastAPI 应用
- SQLite 数据库集成
- 论文数据 CRUD 接口
- 统计信息接口
- Swagger API 文档

✅ **arXiv 爬虫**
- 使用 arxiv.py 库
- 可配置爬取策略
- 按分类和时间范围过滤
- Scrapy 管道集成
- 复用后端 SQLAlchemy 模型

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
│   └── requirements.txt
├── crawler/              # 爬虫模块
│   ├── spiders/          # 爬虫
│   ├── pipelines.py      # 数据处理管道
│   ├── items.py          # 数据模型
│   ├── settings.py       # Scrapy 配置
│   └── config.yaml       # 项目配置
├── etl/                  # ETL 模块
├── docs/                 # 文档
├── scrapy.cfg            # Scrapy 配置
├── docker-compose.yml    # Docker Compose (可选)
├── .gitignore
└── README.md
```

## 快速开始

### 环境要求

- Python 3.11+

### 本地开发

#### 1. 安装依赖

```bash
# 后端依赖
cd backend
pip install -r requirements.txt

# 爬虫依赖
cd ..
pip install arxiv scrapy
```

#### 2. 启动后端 API

```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

访问以下地址：
- API 主页: http://localhost:8000/
- API 文档: http://localhost:8000/docs
- 论文列表: http://localhost:8000/papers/

#### 3. 运行爬虫

```bash
cd /workspace
python -m scrapy crawl arxiv
```

爬虫会根据 `crawler/config.yaml` 中的配置爬取 arXiv 论文并存储到数据库。

### 配置说明

修改 `crawler/config.yaml` 可以调整爬取策略：

```yaml
arXiv:
  categories:
    - cs.AI    # 人工智能
    - cs.LG    # 机器学习
    - cs.RO    # 机器人
    - cs.CV    # 计算机视觉
    - cs.NE    # 神经与演化计算
  days_back: 1              # 爬取最近几天的论文
  max_results_per_request: 10 # 每个分类最多论文数
```

## API 接口

### 论文相关

- `GET /papers/` - 获取论文列表
- `GET /papers/{paper_id}` - 获取单篇论文
- `POST /papers/` - 创建论文
- `PUT /papers/{paper_id}` - 更新论文
- `DELETE /papers/{paper_id}` - 删除论文
- `GET /papers/stats/summary` - 获取统计摘要

### 其他

- `GET /` - 欢迎信息
- `GET /health` - 健康检查

## 许可证

MIT
