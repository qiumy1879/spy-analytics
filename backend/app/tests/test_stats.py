
"""
统计接口测试
测试 /stats/* 系列接口
"""
from datetime import datetime, timedelta
import json


def create_test_paper(client, paper_id, days_ago, categories, title=None):
    """辅助函数：创建测试论文"""
    published_at = datetime.now() - timedelta(days=days_ago)
    paper_data = {
        "paper_id": paper_id,
        "title": title or f"Test Paper {paper_id}",
        "authors": json.dumps(["Author 1", "Author 2"]),
        "published_at": published_at.isoformat(),
        "categories": json.dumps(categories),
        "source": "arxiv"
    }
    response = client.post("/papers/", json=paper_data)
    assert response.status_code == 200
    return response.json()


def test_summary_stats_empty(client):
    """测试空数据库的统计概览"""
    response = client.get("/papers/stats/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["total_papers"] == 0
    assert data["total_authors"] == 0
    assert data["recent_papers_7d"] == 0


def test_summary_stats_with_data(client):
    """测试有数据的统计概览"""
    create_test_paper(client, "2301.00001", 2, ["cs.AI", "cs.LG"])
    create_test_paper(client, "2301.00002", 5, ["cs.CV"])
    create_test_paper(client, "2301.00003", 10, ["cs.AI", "cs.CL"])
    
    response = client.get("/papers/stats/summary")
    assert response.status_code == 200
    data = response.json()
    
    assert data["total_papers"] == 3
    assert data["recent_papers_7d"] == 2  # 2天和5天前的论文在7天内
    assert len(data["categories"]) >= 1


def test_trend_stats_empty(client):
    """测试空数据库的趋势统计"""
    response = client.get("/papers/stats/trend?days=7")
    assert response.status_code == 200
    data = response.json()
    assert data["total_count"] == 0
    assert len(data["trend"]) == 8  # 7天+今天


def test_trend_stats_with_data(client):
    """测试有数据的趋势统计"""
    create_test_paper(client, "2301.10001", 1, ["cs.AI"])
    create_test_paper(client, "2301.10002", 1, ["cs.LG"])
    create_test_paper(client, "2301.10003", 3, ["cs.CV"])
    
    response = client.get("/papers/stats/trend?days=7")
    assert response.status_code == 200
    data = response.json()
    
    assert data["total_count"] == 3
    assert any(day["count"] > 0 for day in data["trend"])


def test_trend_stats_with_category_filter(client):
    """测试带分类筛选的趋势统计"""
    create_test_paper(client, "2301.20001", 1, ["cs.AI"])
    create_test_paper(client, "2301.20002", 1, ["cs.CV"])
    
    response = client.get("/papers/stats/trend?days=7&category=cs.AI")
    assert response.status_code == 200
    data = response.json()
    
    assert data["category"] == "cs.AI"
    assert data["total_count"] == 1


def test_category_stats(client):
    """测试分类统计接口"""
    create_test_paper(client, "2301.30001", 2, ["cs.AI", "cs.LG"])
    create_test_paper(client, "2301.30002", 5, ["cs.CV"])
    create_test_paper(client, "2301.30003", 3, ["cs.AI"])
    
    response = client.get("/papers/stats/categories")
    assert response.status_code == 200
    data = response.json()
    
    assert data["total_categories"] >= 3
    assert any(cat["category"] == "cs.AI" for cat in data["categories"])
    assert any(cat["category_name"] == "人工智能" for cat in data["categories"])


def test_author_stats(client):
    """测试作者统计接口"""
    create_test_paper(client, "2301.40001", 2, ["cs.AI"])
    
    response = client.get("/papers/stats/authors?limit=10")
    assert response.status_code == 200
    data = response.json()
    
    assert data["total_authors"] >= 1
    assert len(data["top_authors"]) >= 1


def test_keyword_stats(client):
    """测试关键词统计接口"""
    create_test_paper(client, "2301.50001", 2, ["cs.AI"], 
                      title="Deep Learning with Neural Networks")
    create_test_paper(client, "2301.50002", 3, ["cs.LG"], 
                      title="Machine Learning Applications")
    
    response = client.get("/papers/stats/keywords?limit=10")
    assert response.status_code == 200
    data = response.json()
    
    assert len(data["top_keywords"]) >= 1
