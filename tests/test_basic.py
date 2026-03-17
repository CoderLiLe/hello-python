#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基础测试文件
测试hello-python项目的基本功能
"""

import unittest
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestBasic(unittest.TestCase):
    """基础测试类"""
    
    def test_python_version(self):
        """测试Python版本"""
        self.assertEqual(sys.version_info.major, 3)
        self.assertGreaterEqual(sys.version_info.minor, 9)
        print(f"✅ Python版本: {sys.version}")
    
    def test_imports(self):
        """测试基本导入"""
        try:
            import math
            import os
            import sys
            import json
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"导入失败: {e}")
    
    def test_arithmetic(self):
        """测试算术运算"""
        self.assertEqual(2 + 2, 4)
        self.assertEqual(10 * 10, 100)
        self.assertEqual(100 / 10, 10)
    
    def test_string_operations(self):
        """测试字符串操作"""
        text = "hello python"
        self.assertEqual(text.upper(), "HELLO PYTHON")
        self.assertEqual(len(text), 12)
        self.assertTrue("python" in text)
    
    def test_list_operations(self):
        """测试列表操作"""
        numbers = [1, 2, 3, 4, 5]
        self.assertEqual(len(numbers), 5)
        self.assertEqual(sum(numbers), 15)
        self.assertEqual(numbers[0], 1)
        self.assertEqual(numbers[-1], 5)
    
    def test_dict_operations(self):
        """测试字典操作"""
        data = {"name": "hello-python", "version": "1.0.0"}
        self.assertEqual(len(data), 2)
        self.assertEqual(data["name"], "hello-python")
        self.assertEqual(data.get("version"), "1.0.0")
        self.assertIn("name", data)
    
    def test_file_operations(self):
        """测试文件操作"""
        test_file = "test_temp.txt"
        
        # 写入文件
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("Hello Python!")
        
        # 读取文件
        with open(test_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        self.assertEqual(content, "Hello Python!")
        
        # 清理
        if os.path.exists(test_file):
            os.remove(test_file)


class TestProjectStructure(unittest.TestCase):
    """测试项目结构"""
    
    def test_required_files(self):
        """测试必需文件是否存在"""
        required_files = [
            "README.md",
            "pyproject.toml",
            "requirements.txt",
            "Makefile",
            "LICENSE",
            "CONTRIBUTING.md",
            "CHANGELOG.md",
        ]
        
        for file in required_files:
            self.assertTrue(
                os.path.exists(file),
                f"必需文件不存在: {file}"
            )
            print(f"✅ 文件存在: {file}")
    
    def test_required_directories(self):
        """测试必需目录是否存在"""
        required_dirs = [
            "src",
            "tests",
            "docs",
            "examples",
            "scripts",
            "config",
        ]
        
        for directory in required_dirs:
            self.assertTrue(
                os.path.exists(directory) and os.path.isdir(directory),
                f"必需目录不存在: {directory}"
            )
            print(f"✅ 目录存在: {directory}")
    
    def test_python_files(self):
        """测试Python文件"""
        # 检查项目根目录下的Python文件
        python_files = [f for f in os.listdir(".") if f.endswith(".py")]
        self.assertGreater(len(python_files), 0, "应该至少有一个Python文件")
        
        for py_file in python_files:
            self.assertTrue(
                os.path.isfile(py_file),
                f"Python文件不是文件: {py_file}"
            )
            print(f"✅ Python文件: {py_file}")


if __name__ == "__main__":
    # 运行测试
    print("=" * 60)
    print("🧪 运行hello-python项目测试")
    print("=" * 60)
    
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试类
    suite.addTests(loader.loadTestsFromTestCase(TestBasic))
    suite.addTests(loader.loadTestsFromTestCase(TestProjectStructure))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 输出结果
    print("\n" + "=" * 60)
    print("📊 测试结果统计")
    print("=" * 60)
    print(f"运行测试数: {result.testsRun}")
    print(f"失败数: {len(result.failures)}")
    print(f"错误数: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("🎉 所有测试通过！")
    else:
        print("❌ 测试失败，请检查错误信息")
    
    sys.exit(0 if result.wasSuccessful() else 1)