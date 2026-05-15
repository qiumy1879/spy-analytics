"""
爬虫管理模块
提供通过 API 调用和管理爬虫任务
"""
import subprocess
import threading
import queue
import os
from typing import Dict, Optional
from datetime import datetime
from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel

router = APIRouter(
    prefix="/crawler",
    tags=["crawler"],
)

# 爬虫任务状态管理
crawler_status = {
    "is_running": False,
    "current_task": None,
    "logs": [],
    "start_time": None
}

# 日志队列
log_queue = queue.Queue()


class CrawlerRequest(BaseModel):
    years: Optional[float] = 0.5
    categories: str = "cs.AI,cs.LG,cs.RO,cs.CV,cs.NE"
    max_results: int = 50


def run_crawler_process(years: float, categories: str, max_results: int):
    """在后台线程中运行爬虫"""
    global crawler_status
    
    crawler_status["is_running"] = True
    crawler_status["start_time"] = datetime.now()
    crawler_status["logs"] = []
    crawler_status["current_task"] = {
        "years": years,
        "categories": categories,
        "max_results": max_results
    }
    
    try:
        # 构建命令
        cmd = [
            "python", "-m", "scrapy", "crawl", "arxiv",
            "-a", f"years={years}",
            "-a", f"categories={categories}",
            "-a", f"max_results={max_results}"
        ]
        
        crawler_status["logs"].append("📋 开始爬取任务启动...")
        
        # 运行命令，捕获输出
        process = subprocess.Popen(
            cmd,
            cwd="/workspace",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # 读取输出，过滤掉SQLAlchemy调试信息
        for line in process.stdout:
            line = line.strip()
            if line:
                # 过滤掉SQLAlchemy的调试信息
                if any(keyword in line for keyword in ["sqlalchemy.engine", "BEGIN", "COMMIT", "SELECT", "INSERT", "UPDATE"]):
                    continue
                crawler_status["logs"].append(line)
                # 限制日志数量，防止内存溢出
                if len(crawler_status["logs"]) > 200:
                    crawler_status["logs"] = crawler_status["logs"][-100:]
        
        process.wait()
        
        crawler_status["logs"].append("✅ 爬取完成！")
        
    except Exception as e:
        crawler_status["logs"].append(f"❌ 错误: {str(e)}")
    finally:
        crawler_status["is_running"] = False
        crawler_status["current_task"] = None


@router.post("/start")
async def start_crawler(request: CrawlerRequest, background_tasks: BackgroundTasks):
    """启动爬虫任务"""
    if crawler_status["is_running"]:
        return {"success": False, "message": "爬虫正在运行中，请稍候"}
    
    # 在后台任务中启动爬虫
    background_tasks.add_task(
        run_crawler_process,
        request.years,
        request.categories,
        request.max_results
    )
    
    return {
        "success": True,
        "message": "爬虫已启动",
        "task": {
            "years": request.years,
            "categories": request.categories,
            "max_results": request.max_results
        }
    }


@router.get("/status")
async def get_crawler_status():
    """获取爬虫状态"""
    return {
        "is_running": crawler_status["is_running"],
        "current_task": crawler_status["current_task"],
        "logs": crawler_status["logs"][-100:],  # 只返回最近的100条日志
        "start_time": crawler_status["start_time"].isoformat() if crawler_status["start_time"] else None,
        "elapsed_seconds": (datetime.now() - crawler_status["start_time"]).total_seconds() if crawler_status["start_time"] and crawler_status["is_running"] else 0
    }


@router.get("/stop")
async def stop_crawler():
    """停止爬虫（友好停止当前正在运行的爬虫无法直接通过API停止，但可以给用户提示"""
    return {
        "success": True,
        "message": "提示：请在终端中按 Ctrl+C 停止爬虫。或者再次运行时会自动跳过已存在的论文"
    }


@router.get("/directions")
async def get_crawler_directions():
    """获取可选的研究方向列表"""
    return {
        "directions": [
            {"code": "cs.AI", "name": "人工智能"},
            {"code": "cs.LG", "name": "机器学习"},
            {"code": "cs.RO", "name": "机器人学"},
            {"code": "cs.CV", "name": "计算机视觉"},
            {"code": "cs.NE", "name": "神经与演化计算"},
            {"code": "cs.CL", "name": "自然语言处理"},
            {"code": "cs.SE", "name": "软件工程"},
            {"code": "cs.DB", "name": "数据库"},
            {"code": "cs.OS", "name": "操作系统"},
            {"code": "cs.PL", "name": "编程语言"}
        ]
    }
