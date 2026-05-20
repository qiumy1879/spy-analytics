
"""
pytest 配置文件
提供测试客户端和测试数据库
"""
import pytest
from starlette.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base, get_db

# 使用 SQLite 内存数据库作为测试数据库
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """测试数据库依赖"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client():
    """创建测试客户端 fixture"""
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    
    # 覆盖依赖
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    # 清理数据库
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()
