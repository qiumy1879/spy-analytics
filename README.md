# Spy Analytics - arXiv 论文分析平台

## 项目简介

Spy Analytics 是一个 arXiv 论文数据采集与分析平台，爬取 arXiv 论文数据，提供 API 接口和数据分析功能。

## 技术栈

- **Web框架**: FastAPI
- **爬虫**: Scrapy + arxiv.py
- **数据库**: SQLite
- **ORM**: SQLAlchemy
- **容器化**: Docker + Docker Compose (可选)

## 已实现功能 (v1.6.0)

✅ **后端 API**
- FastAPI 应用
- SQLite 数据库集成
- 论文数据 CRUD 接口
- 关键词搜索功能（搜索标题和作者）
- 分类筛选功能
- 统计信息接口（汇总、趋势、分类、作者、关键词）
- Swagger API 文档
- 智能中文搜索（支持同义词扩展）
- 研究方向分析

✅ **arXiv 爬虫**
- 使用 arxiv 库直接调用 API
- 支持命令行参数（自定义天数和分类）
- 增量爬取（自动跳过已存在的论文）
- 按分类和时间范围过滤
- Unicode 编码兼容（支持中文显示）
- 友好的日志输出

✅ **数据分析与可视化**
- 📈 论文数量时间趋势图
- 🥧 分类分布饼图
- 🏆 活跃作者排行榜
- 🔤 关键词云图
- 统计卡片（论文总数、新增数量、作者总数、分类数量）

✅ **前端界面**
- 响应式设计
- 论文搜索功能
- 数据采集配置
- API 文档快速跳转
- 数据可视化页面
- 统计信息查看

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

---

#### 2. 启动后端 API

```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

启动后访问以下地址：
- **API 主页**: http://localhost:8000
- **API 文档（推荐！）**: http://localhost:8000/docs
  - 这是交互式文档，可以直接在浏览器里测试 API！
- **论文列表**: http://localhost:8000/papers/

---

#### 3. 运行爬虫采集数据

爬虫支持两种使用方式：

##### 方式一：使用配置文件（默认）

直接运行，使用 `crawler/config.yaml` 中的配置：

```bash
cd /workspace
python -m scrapy crawl arxiv
```

##### 方式二：使用命令行参数（推荐，更灵活！）

自定义爬取天数和分类：

```bash
# 只爬取最近 1 天，只爬人工智能分类
python -m scrapy crawl arxiv -a days=1 -a categories=cs.AI

# 爬取最近 3 天，爬多个分类（用逗号分隔）
python -m scrapy crawl arxiv -a days=3 -a categories=cs.AI,cs.LG,cs.RO

# 爬取最近 7 天，爬 5 个分类
python -m scrapy crawl arxiv -a days=7 -a categories=cs.AI,cs.LG,cs.RO,cs.CV,cs.NE
```

**参数说明：**
- `days`: 爬取最近几天的论文（如不指定，使用配置文件中的默认值）
- `categories`: 要爬取的分类，多个分类用逗号分隔（如不指定，使用配置文件中的默认值）

---

### 配置说明

修改 `crawler/config.yaml` 可以调整默认爬取策略：

```yaml
arXiv:
  categories:
    - cs.AI    # 人工智能
    - cs.LG    # 机器学习
    - cs.RO    # 机器人
    - cs.CV    # 计算机视觉
    - cs.NE    # 神经与演化计算
  days_back: 1              # 爬取最近几天
  max_results_per_request: 10 # 每类最多论文数
```

---

## API 接口使用指南

### 基础接口

- `GET /` - 欢迎信息和版本号
- `GET /health` - 健康检查

### 论文相关接口

#### 1. 获取论文列表（支持搜索和筛选）

**接口**: `GET /papers/`

**参数**:
- `skip`: 跳过多少条（分页用，默认 0）
- `limit`: 最多返回多少条（默认 100）
- `category`: 按分类筛选（如 cs.AI，可选）
- `keyword`: 按关键词搜索（搜索标题和作者，可选）

**使用示例**（在浏览器或 Swagger UI 中测试）：

```
# 获取所有论文
http://localhost:8000/papers/

# 只获取人工智能分类的论文
http://localhost:8000/papers/?category=cs.AI

# 搜索包含 "GPT" 的论文
http://localhost:8000/papers/?keyword=GPT

# 搜索包含 "Zhang" 的作者
http://localhost:8000/papers/?keyword=Zhang

# 组合使用：搜索人工智能分类中包含 "deep" 的论文
http://localhost:8000/papers/?category=cs.AI&keyword=deep
```

#### 2. 获取单篇论文

**接口**: `GET /papers/{paper_id}`

**示例**:
```
http://localhost:8000/papers/2301.12345v1
```

#### 3. 获取统计信息

**接口**: `GET /papers/stats/summary`

**返回内容**:
- 论文总数
- 各分类的论文数量

---

## arXiv 分类说明

常用的 arXiv 分类：
- `cs.AI` - 人工智能
- `cs.LG` - 机器学习
- `cs.RO` - 机器人
- `cs.CV` - 计算机视觉
- `cs.NE` - 神经与演化计算
- `cs.CL` - 计算语言学
- `cs.SE` - 软件工程

更多分类请参考：https://arxiv.org/category_taxonomy

---

## 常见问题

### Q: 如何重新运行爬虫？
A: 直接再次运行爬虫命令即可，已存在的论文会被自动更新，不会重复创建。

### Q: 数据库文件在哪里？
A: 在项目根目录下：`spy_analytics.db`

### Q: 如何清空数据库重新开始？
A: 删除 `spy_analytics.db` 文件，然后重新启动后端 API 会自动创建新的数据库。

---

## 更新日志

### v1.6.0 (2026-05-17)
- 🎨 优化：分类统计同时显示中文和代码（方便识别）
- 🎨 优化：添加分类和关键词统计的标签页切换（节省空间）
- 🐛 修复：作者统计API字段错误
- ✨ 新增：删除分类时显示中文分类名
- 📝 更新：版本号更新为 1.6.0

### v1.1.0 (2026-05-15)
- ✨ 新增：API 关键词搜索功能
- ✨ 新增：爬虫支持命令行参数（天数、分类）
- 📝 优化：添加详细的中文文档和注释
- 🎨 优化：更友好的日志输出

### v1.0.0 (2026-05-15)
- 🎉 初始版本发布
- ✅ 完整的 FastAPI 后端
- ✅ arXiv 论文爬虫
- ✅ SQLite 数据库集成

## 许可证

MIT
