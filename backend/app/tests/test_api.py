
"""
基础 API 测试
测试健康检查、论文 CRUD、搜索等核心接口
"""
from datetime import datetime, timedelta
import json


def test_health_check(client):
    """测试健康检查接口"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_root_endpoint(client):
    """测试根端点"""
    response = client.get("/")
    assert response.status_code in [200, 404]  # 可能返回 HTML 或 JSON


def test_get_papers_empty(client):
    """测试获取空论文列表"""
    response = client.get("/papers/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 0


def test_create_paper(client):
    """测试创建论文"""
    paper_data = {
        "paper_id": "2301.00001",
        "title": "Test Paper Title",
        "authors": json.dumps(["Test Author 1", "Test Author 2"]),
        "published_at": (datetime.now() - timedelta(days=30)).isoformat(),
        "categories": json.dumps(["cs.AI", "cs.LG"]),
        "source": "arxiv",
        "source_url": "https://arxiv.org/abs/2301.00001",
        "pdf_url": "https://arxiv.org/pdf/2301.00001.pdf"
    }
    
    response = client.post("/papers/", json=paper_data)
    assert response.status_code == 200
    
    created_paper = response.json()
    assert created_paper["paper_id"] == "2301.00001"
    assert created_paper["title"] == "Test Paper Title"


def test_create_duplicate_paper(client):
    """测试创建重复论文应该失败"""
    paper_data = {
        "paper_id": "2301.00001",
        "title": "Test Paper Title",
        "authors": json.dumps(["Test Author"]),
        "published_at": datetime.now().isoformat(),
        "categories": json.dumps(["cs.AI"]),
        "source": "arxiv"
    }
    
    client.post("/papers/", json=paper_data)
    response = client.post("/papers/", json=paper_data)
    
    assert response.status_code == 400


def test_get_single_paper(client):
    """测试获取单篇论文"""
    paper_data = {
        "paper_id": "2301.00002",
        "title": "Another Test Paper",
        "authors": json.dumps(["Author"]),
        "published_at": datetime.now().isoformat(),
        "categories": json.dumps(["cs.CV"]),
        "source": "arxiv"
    }
    
    client.post("/papers/", json=paper_data)
    response = client.get("/papers/2301.00002")
    
    assert response.status_code == 200
    assert response.json()["title"] == "Another Test Paper"


def test_get_nonexistent_paper(client):
    """测试获取不存在的论文"""
    response = client.get("/papers/nonexistent-id")
    assert response.status_code == 404


def test_search_papers_by_keyword(client):
    """测试关键词搜索"""
    papers = [
        {"paper_id": "2301.00010", "title": "Deep Learning for AI", "authors": "[]", "categories": json.dumps(["cs.AI"]), "source": "arxiv"},
        {"paper_id": "2301.00011", "title": "Machine Learning Survey", "authors": "[]", "categories": json.dumps(["cs.LG"]), "source": "arxiv"},
        {"paper_id": "2301.00012", "title": "Computer Vision Applications", "authors": "[]", "categories": json.dumps(["cs.CV"]), "source": "arxiv"}
    ]
    
    for paper in papers:
        client.post("/papers/", json=paper)
    
    response = client.get("/papers/?keyword=Learning")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_delete_paper(client):
    """测试删除论文"""
    paper_data = {
        "paper_id": "2301.00099",
        "title": "Paper to Delete",
        "authors": "[]",
        "categories": json.dumps(["cs.AI"]),
        "source": "arxiv"
    }
    
    client.post("/papers/", json=paper_data)
    
    response = client.delete("/papers/2301.00099")
    assert response.status_code == 200
    
    check_response = client.get("/papers/2301.00099")
    assert check_response.status_code == 404

