"""
分类映射模块
提供中文大类到arXiv分类代码的映射
支持用户输入中文名称自动转换为对应的arXiv分类
"""

# 中文大类到arXiv分类的映射
CATEGORY_GROUPS = {
    "人工智能": [
        "cs.AI",  # 人工智能
        "cs.LG",  # 机器学习
        "cs.NE",  # 神经网络
        "stat.ML",  # 统计学-机器学习
    ],
    "计算机视觉": [
        "cs.CV",  # 计算机视觉
        "eess.IV",  # 图像处理
    ],
    "自然语言处理": [
        "cs.CL",  # 自然语言处理
        "cs.IR",  # 信息检索
    ],
    "机器人学": [
        "cs.RO",  # 机器人学
    ],
    "医疗健康": [
        "q-bio.QM",  # 定量生物学-方法
        "q-bio.NC",  # 定量生物学-神经
        "stat.AP",  # 统计学-应用
    ],
    "数据科学": [
        "cs.DB",  # 数据库
        "cs.DS",  # 数据结构
        "cs.IR",  # 信息检索
        "stat.ME",  # 统计学-方法论
    ],
    "软件工程": [
        "cs.SE",  # 软件工程
        "cs.PL",  # 编程语言
        "cs.OS",  # 操作系统
    ],
    "网络安全": [
        "cs.CR",  # 密码学与安全
        "cs.CY",  # 计算机与社会
    ],
    "图形学与多媒体": [
        "cs.GR",  # 图形学
        "cs.MM",  # 多媒体
        "cs.SD",  # 声音
    ],
    "分布式计算": [
        "cs.DC",  # 分布式计算
        "cs.NI",  # 网络与互联网
        "cs.AR",  # 硬件架构
    ],
    "数学与统计": [
        "math.NA",  # 数学-数值分析
        "math.OC",  # 数学-优化与控制
        "math.DS",  # 数学-动力系统
        "stat.ME",  # 统计学-方法论
        "stat.AP",  # 统计学-应用
    ],
    "物理学": [
        "physics.comp-ph",  # 计算物理
        "quant-ph",  # 量子物理
        "physics.plasm-ph",  # 等离子体物理
    ],
    "信号处理": [
        "eess.SP",  # 信号处理
        "eess.AS",  # 音频处理
        "eess.SY",  # 系统与控制
    ],
    "材料科学": [
        "cond-mat.mtrl-sci",  # 材料科学
    ],
    "天文学": [
        "astro-ph.IM",  # 天文学-仪器
    ],
    "经济学": [
        "econ.TH",  # 经济学-理论
    ],
}

# 所有可用的中文大类名称
GROUP_NAMES = list(CATEGORY_GROUPS.keys())

# 反向映射：arXiv分类到中文名称
ARXIV_TO_GROUP = {}
for group_name, categories in CATEGORY_GROUPS.items():
    for cat in categories:
        ARXIV_TO_GROUP[cat] = group_name


def get_arxiv_categories(chinese_groups: list) -> list:
    """
    将中文大类名称转换为对应的arXiv分类代码列表
    
    Args:
        chinese_groups: 中文大类名称列表，如 ["人工智能", "计算机视觉"]
    
    Returns:
        arXiv分类代码列表，如 ["cs.AI", "cs.LG", "cs.NE", "cs.CV"]
    """
    result = []
    for group in chinese_groups:
        group = group.strip()
        if group in CATEGORY_GROUPS:
            result.extend(CATEGORY_GROUPS[group])
    # 去重并保持顺序
    return list(dict.fromkeys(result))


def get_group_name(arxiv_category: str) -> str:
    """
    获取arXiv分类所属的中文大类名称
    
    Args:
        arxiv_category: arXiv分类代码，如 "cs.AI"
    
    Returns:
        中文大类名称，如 "人工智能"
    """
    return ARXIV_TO_GROUP.get(arxiv_category, "其他")


def search_groups(keyword: str) -> list:
    """
    根据关键词搜索匹配的中文大类名称
    
    Args:
        keyword: 搜索关键词
    
    Returns:
        匹配的中文大类名称列表
    """
    keyword = keyword.lower()
    result = []
    for group_name in GROUP_NAMES:
        if keyword in group_name.lower():
            result.append(group_name)
    return result


def is_valid_group(group_name: str) -> bool:
    """
    检查是否为有效的中文大类名称
    
    Args:
        group_name: 中文大类名称
    
    Returns:
        是否有效
    """
    return group_name.strip() in CATEGORY_GROUPS