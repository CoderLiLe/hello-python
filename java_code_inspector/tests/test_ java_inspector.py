#!/usr/bin/env python3
"""
Java代码检查工具的测试用例
"""

import unittest
import os
import tempfile
import shutil
import json
from pathlib import Path

# 添加src目录到Python路径
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from java_inspector import JavaCodeInspector, InspectionConfig, CodeIssue, Severity

class TestJavaCodeInspector(unittest.TestCase):
    """Java代码检查器测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.test_dir = tempfile.mkdtemp()
        self.config = InspectionConfig()
        self.inspector = JavaCodeInspector(self.config)
        
        # 创建测试文件
        self.create_test_files()
    
    def tearDown(self):
        """测试后清理"""
        shutil.rmtree(self.test_dir)
    
    def create_test_files(self):
        """创建测试文件"""
        # 有问题的测试文件
        bad_code = '''import java.util.List;
import java.util.ArrayList;
import java.util.HashMap; // 未使用的import
import java.io.*; // 未使用的import

public class testExample { // 类名不规范
    private int BadlyNamedField; // 字段名不规范
    
    public void BadlyNamedMethod() { // 方法名不规范
        System.out.println("Hello"); // 不应该使用System.out
        List<String> list = new ArrayList<>();
        
        // 魔法数字
        int result = 100 * 2;
        
        // 空的catch块
        try {
            int test = 10 / 0;
        } catch (Exception e) {
            // 空的catch块
        }
    }
    
    public void emptyMethod() { // 空方法
    }
}
'''
        
        # 良好的测试文件
        good_code = '''import java.util.List;
import java.util.ArrayList;
import java.util.logging.Logger;

public class GoodExample {
    private static final Logger LOGGER = Logger.getLogger(GoodExample.class.getName());
    private static final int MAX_RETRY = 3;
    
    private String properlyNamedField;
    
    public void properlyNamedMethod() {
        LOGGER.info("Proper method");
    }
}
'''
        
        # 写入文件
        with open(os.path.join(self.test_dir, 'TestExample.java'), 'w', encoding='utf-8') as f:
            f.write(bad_code)
        
        with open(os.path.join(self.test_dir, 'GoodExample.java'), 'w', encoding='utf-8') as f:
            f.write(good_code)
    
    def test_inspect_file_with_issues(self):
        """测试检查有问题的文件"""
        file_path = os.path.join(self.test_dir, 'TestExample.java')
        issues = self.inspector.inspect_file(file_path)
        
        # 应该发现问题
        self.assertGreater(len(issues), 0)
        
        # 检查特定问题类型
        issue_types = [issue.rule_id for issue in issues]
        print(f"发现的问题类型: {issue_types}")
        
        # 检查一些常见问题
        has_unused_import = any(issue.rule_id == 'UNUSED_IMPORT' for issue in issues)
        has_naming_issue = any(issue.rule_id in ['CLASS_NAMING', 'METHOD_NAMING'] for issue in issues)
        
        self.assertTrue(has_unused_import, "应该检测到未使用的import")
        self.assertTrue(has_naming_issue, "应该检测到命名问题")
    
    def test_inspect_good_file(self):
        """测试检查良好的文件"""
        file_path = os.path.join(self.test_dir, 'GoodExample.java')
        issues = self.inspector.inspect_file(file_path)
        
        # 良好代码应该没有严重问题
        severe_issues = [issue for issue in issues if issue.severity == Severity.ERROR]
        self.assertEqual(len(severe_issues), 0, "良好代码不应该有严重错误")
    
    def test_inspect_directory(self):
        """测试检查目录"""
        issues_by_file = self.inspector.inspect_directory(self.test_dir)
        
        # 应该找到两个文件
        self.assertEqual(len(issues_by_file), 2, "应该检测到两个文件")
        
        # 测试文件应该有更多问题
        test_file_path = os.path.join(self.test_dir, 'TestExample.java')
        good_file_path = os.path.join(self.test_dir, 'GoodExample.java')
        
        test_file_issues = issues_by_file.get(test_file_path, [])
        good_file_issues = issues_by_file.get(good_file_path, [])
        
        self.assertGreater(len(test_file_issues), len(good_file_issues), 
                          "问题文件应该比良好文件有更多问题")
    
    def test_config_disabled_rules(self):
        """测试禁用规则"""
        # 创建禁用某些规则的配置
        config_data = {
            "rules": {
                "unused_imports": {"enabled": False},
                "naming_conventions": {"enabled": False}
            }
        }
        
        config_file = os.path.join(self.test_dir, 'test_config.json')
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config_data, f)
        
        config = InspectionConfig(config_file)
        inspector = JavaCodeInspector(config)
        
        file_path = os.path.join(self.test_dir, 'TestExample.java')
        issues = inspector.inspect_file(file_path)
        
        # 应该不包含被禁用的规则的问题
        issue_rules = [issue.rule_id for issue in issues]
        self.assertNotIn('UNUSED_IMPORT', issue_rules, "未使用的import检查应该被禁用")
        
    def test_empty_method_detection(self):
        """测试空方法检测"""
        # 启用空方法检测
        config = InspectionConfig()
        config.config['rules']['empty_methods'] = {"enabled": True}
        
        inspector = JavaCodeInspector(config)
        file_path = os.path.join(self.test_dir, 'TestExample.java')
        issues = inspector.inspect_file(file_path)
        
        empty_method_issues = [issue for issue in issues if issue.rule_id == 'EMPTY_METHOD']
        self.assertGreaterEqual(len(empty_method_issues), 1, "应该检测到空方法")
    
    def test_predefined_test_files(self):
        """测试预定义的测试文件"""
        test_file_path = os.path.join(os.path.dirname(__file__), 'test_files', 'TestExample.java')
        good_file_path = os.path.join(os.path.dirname(__file__), 'test_files', 'GoodExample.java')
        
        # 检查文件是否存在
        self.assertTrue(os.path.exists(test_file_path), "测试文件应该存在")
        self.assertTrue(os.path.exists(good_file_path), "良好代码文件应该存在")
        
        # 检查测试文件
        issues = self.inspector.inspect_file(test_file_path)
        self.assertGreater(len(issues), 0, "测试文件应该有问题")
        
        # 检查良好文件
        issues = self.inspector.inspect_file(good_file_path)
        severe_issues = [issue for issue in issues if issue.severity == Severity.ERROR]
        self.assertEqual(len(severe_issues), 0, "良好文件不应该有严重错误")

class TestInspectionConfig(unittest.TestCase):
    """配置类测试"""
    
    def test_default_config(self):
        """测试默认配置"""
        config = InspectionConfig()
        
        # 检查默认启用的规则
        self.assertTrue(config.is_rule_enabled('line_length'))
        self.assertTrue(config.is_rule_enabled('naming_conventions'))
        self.assertTrue(config.is_rule_enabled('unused_imports'))
        
        # 检查默认配置值
        line_config = config.get_rule_config('line_length')
        self.assertEqual(line_config.get('max_length'), 120)
    
    def test_custom_config(self):
        """测试自定义配置"""
        # 使用测试目录中的配置文件
        config_file = os.path.join(os.path.dirname(__file__), 'test_config.json')
        self.assertTrue(os.path.exists(config_file), "测试配置文件应该存在")
        
        config = InspectionConfig(config_file)
        
        # 检查配置覆盖
        self.assertTrue(config.is_rule_enabled('line_length'))
        self.assertFalse(config.is_rule_enabled('naming_conventions'))
        
        # 检查配置值
        line_config = config.get_rule_config('line_length')
        self.assertEqual(line_config.get('max_length'), 80)

class TestBasicFunctionality(unittest.TestCase):
    """基本功能测试"""
    
    def test_issue_creation(self):
        """测试问题创建"""
        issue = CodeIssue(
            file_path="test.java",
            line=10,
            column=5,
            message="测试问题",
            severity=Severity.WARNING,
            rule_id="TEST_RULE",
            category="TEST"
        )
        
        self.assertEqual(issue.file_path, "test.java")
        self.assertEqual(issue.line, 10)
        self.assertEqual(issue.message, "测试问题")
        self.assertEqual(issue.severity, Severity.WARNING)
    
    def test_severity_enum(self):
        """测试严重程度枚举"""
        self.assertEqual(Severity.ERROR.value, "ERROR")
        self.assertEqual(Severity.WARNING.value, "WARNING")
        self.assertEqual(Severity.INFO.value, "INFO")

if __name__ == '__main__':
    unittest.main(verbosity=2)