#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
hello-python 核心模块
提供Python学习和代码检查的核心功能
"""

__version__ = "1.0.0"
__author__ = "CoderLiLe"
__license__ = "MIT"

from typing import List, Dict, Any, Optional, Union


def greet(name: str = "Python Developer") -> str:
    """
    打招呼函数
    
    Args:
        name: 姓名，默认为"Python Developer"
    
    Returns:
        问候语字符串
    
    Examples:
        >>> greet("Alice")
        'Hello, Alice! Welcome to hello-python!'
    """
    return f"Hello, {name}! Welcome to hello-python!"


def calculate_fibonacci(n: int) -> List[int]:
    """
    计算斐波那契数列
    
    Args:
        n: 要计算的斐波那契数列长度
    
    Returns:
        斐波那契数列列表
    
    Raises:
        ValueError: 如果n小于等于0
    
    Examples:
        >>> calculate_fibonacci(5)
        [0, 1, 1, 2, 3]
    """
    if n <= 0:
        raise ValueError("n必须大于0")
    
    if n == 1:
        return [0]
    
    fibonacci = [0, 1]
    for i in range(2, n):
        fibonacci.append(fibonacci[i-1] + fibonacci[i-2])
    
    return fibonacci[:n]


def analyze_text(text: str) -> Dict[str, Any]:
    """
    分析文本统计信息
    
    Args:
        text: 要分析的文本
    
    Returns:
        包含文本统计信息的字典
    
    Examples:
        >>> analyze_text("Hello Python!")
        {
            'char_count': 13,
            'word_count': 2,
            'line_count': 1,
            'avg_word_length': 5.5
        }
    """
    lines = text.splitlines()
    words = text.split()
    
    return {
        "char_count": len(text),
        "word_count": len(words),
        "line_count": len(lines),
        "avg_word_length": sum(len(word) for word in words) / len(words) if words else 0,
        "unique_words": len(set(words)),
    }


class PythonTutorial:
    """Python教程类"""
    
    def __init__(self, level: str = "beginner"):
        """
        初始化教程
        
        Args:
            level: 难度级别，可选值: beginner, intermediate, advanced
        """
        self.level = level
        self.topics = self._get_topics()
    
    def _get_topics(self) -> Dict[str, List[str]]:
        """获取不同级别的主题"""
        topics = {
            "beginner": [
                "变量和数据类型",
                "条件语句",
                "循环语句",
                "函数定义",
                "列表和字典",
                "文件操作",
            ],
            "intermediate": [
                "面向对象编程",
                "异常处理",
                "模块和包",
                "装饰器",
                "生成器",
                "上下文管理器",
            ],
            "advanced": [
                "并发编程",
                "异步编程",
                "元编程",
                "性能优化",
                "设计模式",
                "测试驱动开发",
            ]
        }
        return topics.get(self.level, topics["beginner"])
    
    def get_topic_count(self) -> int:
        """获取主题数量"""
        return len(self.topics)
    
    def get_topics(self) -> List[str]:
        """获取所有主题"""
        return self.topics
    
    def has_topic(self, topic: str) -> bool:
        """检查是否包含特定主题"""
        return topic in self.topics


class CodeInspector:
    """代码检查器基类"""
    
    def __init__(self, language: str = "python"):
        """
        初始化代码检查器
        
        Args:
            language: 编程语言，默认为python
        """
        self.language = language
        self.issues: List[Dict[str, Any]] = []
    
    def inspect(self, code: str) -> List[Dict[str, Any]]:
        """
        检查代码
        
        Args:
            code: 要检查的代码
        
        Returns:
            问题列表
        """
        self.issues = []
        self._check_syntax(code)
        self._check_style(code)
        self._check_complexity(code)
        return self.issues
    
    def _check_syntax(self, code: str) -> None:
        """检查语法"""
        # 基础语法检查
        if not code.strip():
            self.issues.append({
                "type": "warning",
                "message": "代码为空",
                "line": 1,
                "severity": "low"
            })
    
    def _check_style(self, code: str) -> None:
        """检查代码风格"""
        lines = code.splitlines()
        for i, line in enumerate(lines, 1):
            # 检查行长度
            if len(line) > 100:
                self.issues.append({
                    "type": "style",
                    "message": f"行{i}过长 ({len(line)}字符)",
                    "line": i,
                    "severity": "medium"
                })
            
            # 检查尾随空格
            if line.rstrip() != line:
                self.issues.append({
                    "type": "style",
                    "message": f"行{i}有尾随空格",
                    "line": i,
                    "severity": "low"
                })
    
    def _check_complexity(self, code: str) -> None:
        """检查代码复杂度"""
        # 简单复杂度检查
        lines = code.splitlines()
        if len(lines) > 50:
            self.issues.append({
                "type": "complexity",
                "message": f"代码过长 ({len(lines)}行)",
                "line": 1,
                "severity": "medium"
            })
    
    def get_issue_count(self) -> int:
        """获取问题数量"""
        return len(self.issues)
    
    def get_issues_by_severity(self, severity: str) -> List[Dict[str, Any]]:
        """按严重程度获取问题"""
        return [issue for issue in self.issues if issue["severity"] == severity]


# 导出主要功能
__all__ = [
    "greet",
    "calculate_fibonacci",
    "analyze_text",
    "PythonTutorial",
    "CodeInspector",
    "__version__",
    "__author__",
    "__license__",
]