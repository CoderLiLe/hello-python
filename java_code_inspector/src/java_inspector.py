#!/usr/bin/env python3
"""
增强版Java代码质量检查工具
支持多种代码规范检查、自动修复和多种报告格式
"""

import javalang
import os
import re
import ast
import json
import xml.etree.ElementTree as ET
import csv
import pandas as pd
from typing import List, Dict, Set, Tuple, Optional, Any, Callable
from dataclasses import dataclass, asdict
from pathlib import Path
from enum import Enum
import statistics
import tempfile
import subprocess
import shutil
import hashlib

try:
    import xmltodict
except ImportError:
    xmltodict = None

try:
    from jinja2 import Template
except ImportError:
    Template = None

class Severity(Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"

class ReportFormat(Enum):
    TEXT = "text"
    JSON = "json"
    XML = "xml"
    HTML = "html"
    CSV = "csv"

@dataclass
class CodeIssue:
    """代码问题"""
    file_path: str
    line: int
    column: int
    message: str
    severity: Severity
    rule_id: str
    category: str
    fixable: bool = False
    fix_suggestion: str = ""

class CodeMetrics:
    """代码度量指标"""
    def __init__(self):
        self.total_lines: int = 0
        self.code_lines: int = 0
        self.comment_lines: int = 0
        self.method_count: int = 0
        self.class_count: int = 0
        self.cyclomatic_complexity: int = 0
        self.duplication_rate: float = 0.0
        self.code_smells: int = 0

class InspectionConfig:
    """检查配置"""
    def __init__(self, config_file: str = None):
        self.default_config = {
            "rules": {
                "line_length": {"enabled": True, "max_length": 120},
                "naming_conventions": {"enabled": True},
                "unused_imports": {"enabled": True},
                "method_complexity": {"enabled": True, "max_complexity": 10},
                "empty_methods": {"enabled": True},
                "duplicate_code": {"enabled": True, "min_tokens": 50},
                "exception_handling": {"enabled": True},
                "magic_numbers": {"enabled": True},
                "comments_ratio": {"enabled": True, "min_ratio": 0.2},
                "cyclomatic_complexity": {"enabled": True, "max_complexity": 15}
            },
            "auto_fix": {
                "unused_imports": True,
                "naming_conventions": False
            },
            "exclude_patterns": ["**/test/**", "**/generated/**"],
            "ci_cd": {
                "fail_on_error": True,
                "max_warnings": 50,
                "quality_gate": 0.8
            }
        }
        
        self.config = self.default_config.copy()
        if config_file and os.path.exists(config_file):
            self.load_config(config_file)
    
    def load_config(self, config_file: str):
        """加载配置文件"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                self._deep_update(self.config, user_config)
        except Exception as e:
            print(f"加载配置文件失败: {e}")
    
    def _deep_update(self, base: Dict, update: Dict):
        """深度更新字典"""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_update(base[key], value)
            else:
                base[key] = value
    
    def is_rule_enabled(self, rule_id: str) -> bool:
        """检查规则是否启用"""
        return self.config['rules'].get(rule_id, {}).get('enabled', False)
    
    def get_rule_config(self, rule_id: str) -> Dict:
        """获取规则配置"""
        return self.config['rules'].get(rule_id, {})

class JavaCodeInspector:
    """Java代码检查器"""
    
    def __init__(self, config: InspectionConfig = None):
        self.issues: List[CodeIssue] = []
        self.metrics: Dict[str, CodeMetrics] = {}
        self.config = config or InspectionConfig()
        self.duplicate_blocks: Dict[str, List[Tuple[int, int]]] = {}
    
    def inspect_file(self, file_path: str) -> List[CodeIssue]:
        """检查单个Java文件"""
        self.issues.clear()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = javalang.parse.parse(content)
            
            # 执行各种检查
            self._check_unused_imports(tree, file_path, content)
            self._check_naming_conventions(tree, file_path)
            self._check_code_style(tree, file_path, content)
            self._check_method_complexity(tree, file_path, content)
            self._check_class_design(tree, file_path)
            self._check_best_practices(tree, file_path, content)
            self._check_empty_methods(tree, file_path)
            self._check_exception_handling(tree, file_path, content)
            self._check_magic_numbers(tree, file_path, content)
            self._check_cyclomatic_complexity(tree, file_path)
            
            # 计算度量指标
            self._calculate_metrics(tree, file_path, content)
            
        except Exception as e:
            self.issues.append(CodeIssue(
                file_path=file_path,
                line=0,
                column=0,
                message=f"解析文件失败: {str(e)}",
                severity=Severity.ERROR,
                rule_id="PARSE_ERROR",
                category="PARSING"
            ))
        
        return self.issues
    
    def inspect_directory(self, directory_path: str) -> Dict[str, List[CodeIssue]]:
        """检查目录中的所有Java文件"""
        results = {}
        
        # 先检查重复代码（需要所有文件）
        if self.config.is_rule_enabled("duplicate_code"):
            self._check_duplicate_code(directory_path)
        
        for root, _, files in os.walk(directory_path):
            for file in files:
                if file.endswith('.java'):
                    file_path = os.path.join(root, file)
                    # 检查排除模式
                    if self._is_excluded(file_path):
                        continue
                    issues = self.inspect_file(file_path)
                    results[file_path] = issues
        
        return results
    
    def _is_excluded(self, file_path: str) -> bool:
        """检查文件是否在排除列表中"""
        for pattern in self.config.config['exclude_patterns']:
            if Path(file_path).match(pattern):
                return True
        return False
    
    def _check_empty_methods(self, tree, file_path: str):
        """检查空方法"""
        if not self.config.is_rule_enabled("empty_methods"):
            return
        
        for type_decl in tree.types:
            for decl in type_decl.body:
                if isinstance(decl, javalang.tree.MethodDeclaration):
                    if not decl.body or not decl.body.statements:
                        self.issues.append(CodeIssue(
                            file_path=file_path,
                            line=decl.position.line if decl.position else 0,
                            column=decl.position.column if decl.position else 0,
                            message=f"空方法: {decl.name}",
                            severity=Severity.WARNING,
                            rule_id="EMPTY_METHOD",
                            category="DESIGN",
                            fixable=True,
                            fix_suggestion="删除空方法或添加实现"
                        ))
    
    def _check_exception_handling(self, tree, file_path: str, content: str):
        """检查异常处理"""
        if not self.config.is_rule_enabled("exception_handling"):
            return
        
        # 检查空的catch块
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if re.search(r'catch\s*\([^)]+\)\s*\{\s*\}', line):
                self.issues.append(CodeIssue(
                    file_path=file_path,
                    line=i,
                    column=0,
                    message="空的catch块，应该至少记录异常",
                    severity=Severity.WARNING,
                    rule_id="EMPTY_CATCH",
                    category="EXCEPTION",
                    fixable=True,
                    fix_suggestion="添加异常处理逻辑"
                ))
    
    def _check_magic_numbers(self, tree, file_path: str, content: str):
        """检查魔法数字"""
        if not self.config.is_rule_enabled("magic_numbers"):
            return
        
        magic_number_pattern = r'\b([0-9]{2,}|[0-9]\.[0-9]+)\b'
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            numbers = re.findall(magic_number_pattern, line)
            for number in numbers:
                # 排除常见的0,1,-1等
                if number not in ['0', '1', '-1', '0.0', '1.0']:
                    self.issues.append(CodeIssue(
                        file_path=file_path,
                        line=i,
                        column=line.find(number),
                        message=f"魔法数字: {number}，建议定义为常量",
                        severity=Severity.INFO,
                        rule_id="MAGIC_NUMBER",
                        category="STYLE",
                        fixable=True,
                        fix_suggestion=f"定义常量: public static final int NUMBER_{number} = {number};"
                    ))
    
    def _check_cyclomatic_complexity(self, tree, file_path: str):
        """检查圈复杂度"""
        if not self.config.is_rule_enabled("cyclomatic_complexity"):
            return
        
        max_complexity = self.config.get_rule_config("cyclomatic_complexity").get("max_complexity", 15)
        
        def calculate_cyclomatic_complexity(method):
            complexity = 1
            decision_points = [
                'if', 'while', 'for', 'case', 'catch', '&&', '||', '?', ':', 'else if'
            ]
            
            def count_decisions(node):
                nonlocal complexity
                if isinstance(node, (javalang.tree.IfStatement, javalang.tree.WhileStatement,
                                   javalang.tree.ForStatement, javalang.tree.SwitchStatement,
                                   javalang.tree.CatchClause, javalang.tree.ConditionalExpression)):
                    complexity += 1
                
                for child in node.children:
                    if isinstance(child, (list, tuple)):
                        for item in child:
                            if hasattr(item, 'children'):
                                count_decisions(item)
                    elif hasattr(child, 'children'):
                        count_decisions(child)
            
            count_decisions(method)
            return complexity
        
        for type_decl in tree.types:
            for decl in type_decl.body:
                if isinstance(decl, javalang.tree.MethodDeclaration):
                    complexity = calculate_cyclomatic_complexity(decl)
                    if complexity > max_complexity:
                        self.issues.append(CodeIssue(
                            file_path=file_path,
                            line=decl.position.line if decl.position else 0,
                            column=decl.position.column if decl.position else 0,
                            message=f"圈复杂度过高: {complexity} (建议≤{max_complexity})",
                            severity=Severity.WARNING,
                            rule_id="HIGH_CYCLOMATIC_COMPLEXITY",
                            category="COMPLEXITY"
                        ))
    
    def _check_duplicate_code(self, directory_path: str):
        """检查重复代码"""
        if not self.config.is_rule_enabled("duplicate_code"):
            return
        
        min_tokens = self.config.get_rule_config("duplicate_code").get("min_tokens", 50)
        
        # 使用临时文件和外部工具检查重复代码
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            # 使用CPD (Copy-Paste Detector) 如果有的话
            # 这里简化实现，实际可以使用javalang进行token比较
            java_files = []
            for root, _, files in os.walk(directory_path):
                for file in files:
                    if file.endswith('.java') and not self._is_excluded(os.path.join(root, file)):
                        java_files.append(os.path.join(root, file))
            
            # 简单的重复代码检测（实际项目中应该使用更复杂的算法）
            self._simple_duplicate_detection(java_files, min_tokens)
            
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    def _simple_duplicate_detection(self, java_files: List[str], min_tokens: int):
        """简单的重复代码检测"""
        code_blocks = {}
        
        for file_path in java_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 按方法分割代码
                methods = re.findall(r'(\b\w+\s+[^{]+\{[^}]+\})', content, re.DOTALL)
                for method in methods:
                    # 计算代码块的hash
                    code_hash = hashlib.md5(method.strip().encode()).hexdigest()
                    if code_hash in code_blocks:
                        code_blocks[code_hash].append((file_path, method))
                    else:
                        code_blocks[code_hash] = [(file_path, method)]
            
            except Exception as e:
                print(f"分析文件 {file_path} 时出错: {e}")
        
        # 报告重复代码
        for code_hash, occurrences in code_blocks.items():
            if len(occurrences) > 1 and len(occurrences[0][1].split()) >= min_tokens:
                for file_path, method in occurrences:
                    # 估算行号
                    lines = method.count('\n') + 1
                    self.issues.append(CodeIssue(
                        file_path=file_path,
                        line=0,  # 需要更精确的行号计算
                        column=0,
                        message=f"重复代码块 ({len(occurrences)} 处重复)",
                        severity=Severity.WARNING,
                        rule_id="DUPLICATE_CODE",
                        category="QUALITY"
                    ))
    
    def auto_fix_issues(self, file_path: str) -> List[CodeIssue]:
        """自动修复可修复的问题"""
        fixed_issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.split('\n')
            modified = False
            
            # 收集当前文件的问题
            issues = self.inspect_file(file_path)
            fixable_issues = [issue for issue in issues if issue.fixable]
            
            for issue in fixable_issues:
                if issue.rule_id == "UNUSED_IMPORT" and self.config.config['auto_fix'].get('unused_imports', False):
                    # 删除未使用的import
                    line_to_remove = issue.line - 1
                    if 0 <= line_to_remove < len(lines):
                        lines[line_to_remove] = ""  # 置空行
                        modified = True
                        fixed_issues.append(issue)
                
                # 可以添加更多自动修复规则
            
            if modified:
                # 写入修复后的内容
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(lines))
                
                print(f"已自动修复 {len(fixed_issues)} 个问题在文件 {file_path}")
            
        except Exception as e:
            print(f"自动修复失败: {e}")
        
        return fixed_issues

class InspectionReporter:
    """检查结果报告器"""
    
    @staticmethod
    def generate_report(issues_by_file: Dict[str, List[CodeIssue]], 
                       format: ReportFormat = ReportFormat.TEXT,
                       output_file: str = None) -> str:
        """生成报告"""
        if format == ReportFormat.JSON:
            return InspectionReporter.generate_json_report(issues_by_file, output_file)
        elif format == ReportFormat.XML:
            return InspectionReporter.generate_xml_report(issues_by_file, output_file)
        elif format == ReportFormat.HTML:
            return InspectionReporter.generate_html_report(issues_by_file, output_file)
        elif format == ReportFormat.CSV:
            return InspectionReporter.generate_csv_report(issues_by_file, output_file)
        else:
            return InspectionReporter.generate_text_report(issues_by_file, output_file)
    
    @staticmethod
    def generate_text_report(issues_by_file: Dict[str, List[CodeIssue]], output_file: str = None) -> str:
        """生成文本报告"""
        report = []
        total_issues = 0
        severity_counts = {severity: 0 for severity in Severity}
        
        for file_path, issues in issues_by_file.items():
            if issues:
                report.append(f"\n{'='*80}")
                report.append(f"文件: {file_path}")
                report.append(f"{'='*80}")
                
                for issue in issues:
                    total_issues += 1
                    severity_counts[issue.severity] += 1
                    fixable = " [可修复]" if issue.fixable else ""
                    report.append(f"{issue.severity.value}: {issue.message}{fixable} (行{issue.line}, 列{issue.column})")
        
        # 添加统计信息
        report.append(f"\n{'='*80}")
        report.append("统计信息:")
        report.append(f"总问题数: {total_issues}")
        for severity, count in severity_counts.items():
            report.append(f"{severity.value}: {count}")
        report.append(f"{'='*80}")
        
        report_text = '\n'.join(report)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report_text)
        
        return report_text
    
    @staticmethod
    def generate_json_report(issues_by_file: Dict[str, List[CodeIssue]], output_file: str = None) -> str:
        """生成JSON报告"""
        report_data = {
            'summary': {
                'total_files': len(issues_by_file),
                'total_issues': sum(len(issues) for issues in issues_by_file.values()),
                'severity_counts': {severity.value: 0 for severity in Severity}
            },
            'files': {}
        }
        
        for file_path, issues in issues_by_file.items():
            report_data['files'][file_path] = []
            for issue in issues:
                issue_dict = asdict(issue)
                issue_dict['severity'] = issue.severity.value
                report_data['files'][file_path].append(issue_dict)
                report_data['summary']['severity_counts'][issue.severity.value] += 1
        
        json_data = json.dumps(report_data, ensure_ascii=False, indent=2)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(json_data)
        
        return json_data
    
    @staticmethod
    def generate_xml_report(issues_by_file: Dict[str, List[CodeIssue]], output_file: str = None) -> str:
        """生成XML报告"""
        root = ET.Element("codeInspection")
        summary = ET.SubElement(root, "summary")
        ET.SubElement(summary, "totalFiles").text = str(len(issues_by_file))
        ET.SubElement(summary, "totalIssues").text = str(sum(len(issues) for issues in issues_by_file.values()))
        
        files_elem = ET.SubElement(root, "files")
        for file_path, issues in issues_by_file.items():
            file_elem = ET.SubElement(files_elem, "file")
            ET.SubElement(file_elem, "path").text = file_path
            issues_elem = ET.SubElement(file_elem, "issues")
            for issue in issues:
                issue_elem = ET.SubElement(issues_elem, "issue")
                ET.SubElement(issue_elem, "line").text = str(issue.line)
                ET.SubElement(issue_elem, "column").text = str(issue.column)
                ET.SubElement(issue_elem, "message").text = issue.message
                ET.SubElement(issue_elem, "severity").text = issue.severity.value
                ET.SubElement(issue_elem, "ruleId").text = issue.rule_id
                ET.SubElement(issue_elem, "category").text = issue.category
        
        xml_str = ET.tostring(root, encoding='unicode', method='xml')
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(xml_str)
        
        return xml_str
    
    @staticmethod
    def generate_html_report(issues_by_file: Dict[str, List[CodeIssue]], output_file: str = None) -> str:
        """生成HTML报告"""
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Java代码检查报告</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .summary { background: #f5f5f5; padding: 15px; border-radius: 5px; }
                .file { margin: 20px 0; border: 1px solid #ddd; border-radius: 5px; }
                .file-header { background: #e9e9e9; padding: 10px; font-weight: bold; }
                .issue { padding: 8px; border-bottom: 1px solid #eee; }
                .ERROR { background: #ffebee; border-left: 4px solid #f44336; }
                .WARNING { background: #fff8e1; border-left: 4px solid #ffc107; }
                .INFO { background: #e8f5e8; border-left: 4px solid #4caf50; }
            </style>
        </head>
        <body>
            <h1>Java代码检查报告</h1>
            <div class="summary">
                <h2>统计信息</h2>
                <p>总文件数: {{ total_files }}</p>
                <p>总问题数: {{ total_issues }}</p>
                {% for severity, count in severity_counts.items() %}
                <p>{{ severity }}: {{ count }}</p>
                {% endfor %}
            </div>
            
            {% for file_path, issues in files.items() %}
            <div class="file">
                <div class="file-header">{{ file_path }}</div>
                <div class="issues">
                    {% for issue in issues %}
                    <div class="issue {{ issue.severity }}">
                        <strong>{{ issue.severity }}</strong>: {{ issue.message }}<br>
                        <small>行: {{ issue.line }}, 列: {{ issue.column }} | 规则: {{ issue.rule_id }}</small>
                    </div>
                    {% endfor %}
                </div>
            </div>
            {% endfor %}
        </body>
        </html>
        """
        
        total_issues = sum(len(issues) for issues in issues_by_file.values())
        severity_counts = {severity.value: 0 for severity in Severity}
        
        for issues in issues_by_file.values():
            for issue in issues:
                severity_counts[issue.severity.value] += 1
        
        template = Template(html_template)
        html_content = template.render(
            total_files=len(issues_by_file),
            total_issues=total_issues,
            severity_counts=severity_counts,
            files=issues_by_file
        )
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
        
        return html_content
    
    @staticmethod
    def generate_csv_report(issues_by_file: Dict[str, List[CodeIssue]], output_file: str = None) -> str:
        """生成CSV报告"""
        csv_data = []
        headers = ['File', 'Line', 'Column', 'Severity', 'Rule', 'Category', 'Message', 'Fixable']
        
        for file_path, issues in issues_by_file.items():
            for issue in issues:
                csv_data.append([
                    file_path,
                    issue.line,
                    issue.column,
                    issue.severity.value,
                    issue.rule_id,
                    issue.category,
                    issue.message,
                    '是' if issue.fixable else '否'
                ])
        
        csv_content = ','.join(headers) + '\n'
        for row in csv_data:
            # 转义包含逗号的内容
            escaped_row = [f'"{cell}"' if ',' in str(cell) else str(cell) for cell in row]
            csv_content += ','.join(escaped_row) + '\n'
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(csv_content)
        
        return csv_content

class CICDIntegrator:
    """CI/CD集成工具"""
    
    def __init__(self, config: InspectionConfig):
        self.config = config
        self.exit_code = 0
    
    def check_quality_gate(self, issues_by_file: Dict[str, List[CodeIssue]]) -> bool:
        """检查质量门禁"""
        ci_config = self.config.config['ci_cd']
        total_errors = 0
        total_warnings = 0
        
        for issues in issues_by_file.values():
            for issue in issues:
                if issue.severity == Severity.ERROR:
                    total_errors += 1
                elif issue.severity == Severity.WARNING:
                    total_warnings += 1
        
        # 检查错误数量
        if ci_config['fail_on_error'] and total_errors > 0:
            print(f"CI/CD检查失败: 发现 {total_errors} 个错误")
            self.exit_code = 1
            return False
        
        # 检查警告数量
        if total_warnings > ci_config['max_warnings']:
            print(f"CI/CD检查失败: 警告数量 {total_warnings} 超过限制 {ci_config['max_warnings']}")
            self.exit_code = 1
            return False
        
        print(f"CI/CD检查通过: 错误 {total_errors}, 警告 {total_warnings}")
        return True
    
    def get_exit_code(self) -> int:
        """获取退出代码"""
        return self.exit_code

# Git钩子集成
def install_git_hook():
    """安装Git预提交钩子"""
    hook_content = '''#!/bin/bash
# Java代码检查Git钩子
echo "运行Java代码检查..."
python java_inspector.py --ci-cd
if [ $? -ne 0 ]; then
    echo "代码检查失败，请修复问题后再提交"
    exit 1
fi
echo "代码检查通过"
exit 0
'''
    
    git_dir = subprocess.run(['git', 'rev-parse', '--git-dir'], 
                           capture_output=True, text=True).stdout.strip()
    hook_path = os.path.join(git_dir, 'hooks', 'pre-commit')
    
    with open(hook_path, 'w') as f:
        f.write(hook_content)
    
    os.chmod(hook_path, 0o755)
    print("Git预提交钩子安装完成")

# 使用示例和主程序
def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='增强版Java代码质量检查工具')
    parser.add_argument('path', nargs='?', default='.', help='要检查的Java文件或目录路径')
    parser.add_argument('--config', '-c', help='配置文件路径')
    parser.add_argument('--output', '-o', help='输出报告文件')
    parser.add_argument('--format', '-f', choices=['text', 'json', 'xml', 'html', 'csv'], 
                       default='text', help='报告格式')
    parser.add_argument('--fix', action='store_true', help='自动修复可修复的问题')
    parser.add_argument('--ci-cd', action='store_true', help='CI/CD模式，会返回适当的退出代码')
    parser.add_argument('--install-hook', action='store_true', help='安装Git预提交钩子')
    
    args = parser.parse_args()
    
    if args.install_hook:
        install_git_hook()
        return
    
    config = InspectionConfig(args.config)
    inspector = JavaCodeInspector(config)
    reporter = InspectionReporter()
    ci_cd = CICDIntegrator(config)
    
    # 自动修复
    if args.fix:
        if os.path.isfile(args.path) and args.path.endswith('.java'):
            fixed_issues = inspector.auto_fix_issues(args.path)
            print(f"修复了 {len(fixed_issues)} 个问题")
        else:
            print("自动修复目前只支持单个文件")
        return
    
    # 代码检查
    if os.path.isfile(args.path) and args.path.endswith('.java'):
        issues = inspector.inspect_file(args.path)
        issues_by_file = {args.path: issues}
    elif os.path.isdir(args.path):
        issues_by_file = inspector.inspect_directory(args.path)
    else:
        print("错误: 请输入有效的Java文件或目录路径")
        return
    
    # 生成报告
    report = reporter.generate_report(
        issues_by_file, 
        ReportFormat(args.format), 
        args.output
    )
    
    if not args.output:
        print(report)
    
    # CI/CD检查
    if args.ci_cd:
        success = ci_cd.check_quality_gate(issues_by_file)
        exit(ci_cd.get_exit_code())

if __name__ == "__main__":
    main()