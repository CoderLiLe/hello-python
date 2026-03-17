#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
hello-python 基础使用示例
展示如何使用hello-python库的核心功能
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.hello_python import (
    greet,
    calculate_fibonacci,
    analyze_text,
    PythonTutorial,
    CodeInspector,
    __version__,
)


def demo_greet() -> None:
    """演示打招呼功能"""
    print("=" * 60)
    print("👋 打招呼功能演示")
    print("=" * 60)
    
    # 默认打招呼
    print(greet())
    
    # 自定义名字打招呼
    print(greet("Alice"))
    print(greet("Bob"))
    print(greet("Python开发者"))
    
    print()


def demo_fibonacci() -> None:
    """演示斐波那契数列计算"""
    print("=" * 60)
    print("🔢 斐波那契数列计算演示")
    print("=" * 60)
    
    # 计算不同长度的斐波那契数列
    lengths = [5, 10, 15]
    
    for length in lengths:
        fibonacci = calculate_fibonacci(length)
        print(f"前{length}个斐波那契数: {fibonacci}")
    
    print()


def demo_text_analysis() -> None:
    """演示文本分析功能"""
    print("=" * 60)
    print("📊 文本分析功能演示")
    print("=" * 60)
    
    # 分析不同文本
    texts = [
        "Hello Python!",
        "Python是一种强大的编程语言，广泛应用于Web开发、数据分析和人工智能。",
        """这是多行文本示例。
第一行包含一些文字。
第二行继续分析。
第三行结束示例。""",
    ]
    
    for i, text in enumerate(texts, 1):
        print(f"文本{i}分析结果:")
        analysis = analyze_text(text)
        for key, value in analysis.items():
            print(f"  {key}: {value}")
        print()


def demo_python_tutorial() -> None:
    """演示Python教程功能"""
    print("=" * 60)
    print("📚 Python教程功能演示")
    print("=" * 60)
    
    # 创建不同级别的教程
    levels = ["beginner", "intermediate", "advanced"]
    
    for level in levels:
        tutorial = PythonTutorial(level)
        print(f"{level.title()}级别教程:")
        print(f"  主题数量: {tutorial.get_topic_count()}")
        print(f"  主题列表: {', '.join(tutorial.get_topics())}")
        print()


def demo_code_inspection() -> None:
    """演示代码检查功能"""
    print("=" * 60)
    print("🔍 代码检查功能演示")
    print("=" * 60)
    
    # 创建代码检查器
    inspector = CodeInspector("python")
    
    # 检查不同代码
    code_samples = [
        # 简单代码
        """def hello():
    print("Hello World")""",
        
        # 较长代码
        """def calculate_sum(numbers):
    total = 0
    for number in numbers:
        total += number
    return total

def calculate_average(numbers):
    if not numbers:
        return 0
    return calculate_sum(numbers) / len(numbers)

def process_data(data):
    # 这是一个很长的注释行，用于演示行长度检查，看看是否会被标记为过长的问题
    results = []
    for item in data:
        processed = item * 2
        results.append(processed)
    return results""",
        
        # 有问题的代码
        """def bad_function():
    x=1  
    y=2
    # 尾随空格在这行后面    
    return x+y""",
    ]
    
    for i, code in enumerate(code_samples, 1):
        print(f"代码示例{i}检查结果:")
        issues = inspector.inspect(code)
        
        if not issues:
            print("  ✅ 没有发现问题")
        else:
            print(f"  ⚠️ 发现{len(issues)}个问题:")
            for issue in issues:
                print(f"    - [{issue['severity'].upper()}] 行{issue['line']}: {issue['message']}")
        
        print()


def show_project_info() -> None:
    """显示项目信息"""
    print("=" * 60)
    print("ℹ️  hello-python 项目信息")
    print("=" * 60)
    
    print(f"版本: {__version__}")
    print(f"模块路径: {os.path.abspath(__file__)}")
    print(f"Python版本: {sys.version}")
    print(f"当前目录: {os.getcwd()}")
    print()


def main() -> None:
    """主函数"""
    print("🚀 hello-python 示例程序")
    print()
    
    # 显示项目信息
    show_project_info()
    
    # 演示各个功能
    demo_greet()
    demo_fibonacci()
    demo_text_analysis()
    demo_python_tutorial()
    demo_code_inspection()
    
    print("=" * 60)
    print("🎉 示例演示完成！")
    print("=" * 60)
    print()
    print("💡 提示:")
    print("1. 查看源代码了解更多功能")
    print("2. 运行测试: python -m pytest tests/")
    print("3. 查看文档: docs/ 目录")
    print("4. 贡献代码: 参考CONTRIBUTING.md")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 程序被用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 程序运行出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)