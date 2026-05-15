"""
智能搜索模块 - 中文关键词映射和搜索逻辑
"""
from typing import List, Dict, Set

# 中文关键词到 arXiv 分类和英文关键词的映射
RESEARCH_DIRECTIONS = {
    "具身智能": {
        "categories": ["cs.RO", "cs.AI", "cs.LG"],
        "keywords": ["embodied", "robot", "physical", "interaction", "manipulation"],
        "sub_directions": [
            "机器人学",
            "强化学习",
            "计算机视觉",
            "人机交互"
        ]
    },
    "大模型": {
        "categories": ["cs.CL", "cs.AI", "cs.LG"],
        "keywords": ["llm", "gpt", "transformer", "large language", "foundation model"],
        "sub_directions": [
            "自然语言处理",
            "模型训练",
            "对齐",
            "推理"
        ]
    },
    "人工智能": {
        "categories": ["cs.AI", "cs.LG"],
        "keywords": ["ai", "artificial intelligence", "machine learning"],
        "sub_directions": [
            "机器学习",
            "深度学习",
            "计算机视觉",
            "自然语言处理"
        ]
    },
    "机器学习": {
        "categories": ["cs.LG", "cs.AI", "stat.ML"],
        "keywords": ["machine learning", "deep learning", "neural network"],
        "sub_directions": [
            "监督学习",
            "无监督学习",
            "强化学习",
            "优化"
        ]
    },
    "机器人学": {
        "categories": ["cs.RO", "cs.AI"],
        "keywords": ["robot", "robotics", "manipulation", "navigation"],
        "sub_directions": [
            "运动规划",
            "机器人控制",
            "人机交互",
            "自主导航"
        ]
    },
    "计算机视觉": {
        "categories": ["cs.CV", "cs.LG"],
        "keywords": ["computer vision", "image", "video", "detection", "segmentation"],
        "sub_directions": [
            "目标检测",
            "图像分割",
            "视频理解",
            "三维视觉"
        ]
    },
    "自然语言处理": {
        "categories": ["cs.CL", "cs.AI"],
        "keywords": ["nlp", "natural language", "text", "language"],
        "sub_directions": [
            "机器翻译",
            "文本生成",
            "情感分析",
            "问答系统"
        ]
    },
    "强化学习": {
        "categories": ["cs.LG", "cs.AI", "cs.RO"],
        "keywords": ["reinforcement learning", "rl", "policy", "reward"],
        "sub_directions": [
            "深度强化学习",
            "多智能体",
            "离线强化学习",
            "探索"
        ]
    },
    "深度学习": {
        "categories": ["cs.LG", "cs.AI", "cs.CV", "cs.CL"],
        "keywords": ["deep learning", "neural network", "cnn", "transformer"],
        "sub_directions": [
            "神经网络",
            "优化方法",
            "架构设计",
            "预训练"
        ]
    }
}


def parse_chinese_query(query: str) -> Dict:
    """
    解析中文查询，识别研究方向和关键词
    
    Args:
        query: 中文查询字符串，如 "具身智能"
    
    Returns:
        包含分类、关键词、子方向的字典
    """
    query_lower = query.lower().strip()
    
    # 精确匹配研究方向
    if query_lower in RESEARCH_DIRECTIONS:
        return RESEARCH_DIRECTIONS[query_lower]
    
    # 模糊匹配（包含关键词）
    for direction, data in RESEARCH_DIRECTIONS.items():
        if any(keyword in query_lower for keyword in direction):
            return data
    
    # 如果没有匹配到，返回默认配置
    return {
        "categories": ["cs.AI", "cs.LG", "cs.RO", "cs.CV", "cs.CL"],
        "keywords": query_lower.split(),
        "sub_directions": ["人工智能", "机器学习", "机器人学", "计算机视觉"]
    }


def get_search_suggestions(query: str) -> List[Dict]:
    """
    获取搜索建议
    
    Args:
        query: 用户输入的查询
    
    Returns:
        搜索建议列表
    """
    suggestions = []
    
    # 基于输入提供相关的研究方向建议
    query_lower = query.lower()
    
    for direction in RESEARCH_DIRECTIONS.keys():
        if query_lower in direction.lower():
            suggestions.append({
                "type": "研究方向",
                "text": direction,
                "data": RESEARCH_DIRECTIONS[direction]
            })
    
    # 如果没有匹配，显示热门研究方向
    if not suggestions:
        top_directions = list(RESEARCH_DIRECTIONS.keys())[:5]
        for direction in top_directions:
            suggestions.append({
                "type": "热门研究方向",
                "text": direction,
                "data": RESEARCH_DIRECTIONS[direction]
            })
    
    return suggestions
