#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目质量检查报告生成器
分析hello-python项目的代码质量和结构
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Tuple


class QualityAnalyzer:
    """项目质量分析器"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.report_data: Dict[str, Any] = {
            "timestamp": datetime.now().isoformat(),
            "project": "hello-python",
            "metrics": {},
            "issues": [],
            "recommendations": []
        }
    
    def analyze_project_structure(self) -> Dict[str, Any]:
        """分析项目结构"""
        print("📁 分析项目结构...")
        
        structure = {
            "directories": [],
            "python_files": [],
            "markdown_files": [],
            "other_files": [],
            "total_files": 0,
            "total_size_kb": 0
        }
        
        for root, dirs, files in os.walk(self.project_root):
            # 跳过.git目录
            if '.git' in root:
                continue
                
            rel_root = Path(root).relative_to(self.project_root)
            
            for dir_name in dirs:
                if dir_name not in ['.git', '__pycache__', '.pytest_cache']:
                    structure["directories"].append(str(rel_root / dir_name))
            
            for file in files:
                filepath = Path(root) / file
                rel_path = filepath.relative_to(self.project_root)
                size_kb = filepath.stat().st_size / 1024
                
                structure["total_files"] += 1
                structure["total_size_kb"] += size_kb
                
                if file.endswith('.py'):
                    structure["python_files"].append({
                        "path": str(rel_path),
                        "size_kb": round(size_kb, 2)
                    })
                elif file.endswith('.md'):
                    structure["markdown_files"].append({
                        "path": str(rel_path),
                        "size_kb": round(size_kb, 2)
                    })
                else:
                    structure["other_files"].append({
                        "path": str(rel_path),
                        "size_kb": round(size_kb, 2),
                        "type": file.split('.')[-1] if '.' in file else "unknown"
                    })
        
        self.report_data["structure"] = structure
        return structure
    
    def analyze_python_code_quality(self) -> Dict[str, Any]:
        """分析Python代码质量"""
        print("🐍 分析Python代码质量...")
        
        quality = {
            "total_python_files": 0,
            "total_lines": 0,
            "files_with_issues": [],
            "type_hint_coverage": 0,
            "docstring_coverage": 0,
            "complexity_issues": []
        }
        
        python_files = []
        for root, dirs, files in os.walk(self.project_root):
            for file in files:
                if file.endswith('.py'):
                    python_files.append(Path(root) / file)
        
        quality["total_python_files"] = len(python_files)
        
        for py_file in python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')
                    
                rel_path = py_file.relative_to(self.project_root)
                file_issues = []
                
                # 检查编码声明
                if not any(content.startswith(prefix) for prefix in ['# -*- coding: utf-8 -*-', '# coding: utf-8']):
                    file_issues.append("缺少编码声明")
                
                # 检查shebang
                if not content.startswith('#!/usr/bin/env python3'):
                    file_issues.append("缺少shebang或使用python3")
                
                # 检查类型提示
                functions = [line for line in lines if line.strip().startswith('def ')]
                typed_functions = [line for line in functions if '->' in line]
                
                if functions:
                    type_coverage = len(typed_functions) / len(functions) * 100
                    if type_coverage < 50:
                        file_issues.append(f"类型提示覆盖率低: {type_coverage:.1f}%")
                
                # 检查文档字符串
                has_docstring = '"""' in content or "'''" in content
                if not has_docstring and len(lines) > 10:
                    file_issues.append("缺少文档字符串")
                
                # 检查行长度
                long_lines = []
                for i, line in enumerate(lines, 1):
                    if len(line) > 100:
                        long_lines.append(i)
                
                if long_lines:
                    file_issues.append(f"行过长: {long_lines}")
                
                if file_issues:
                    quality["files_with_issues"].append({
                        "file": str(rel_path),
                        "issues": file_issues,
                        "line_count": len(lines)
                    })
                
                quality["total_lines"] += len(lines)
                
            except Exception as e:
                print(f"  警告: 分析文件 {py_file} 时出错: {e}")
        
        # 计算覆盖率
        if quality["total_python_files"] > 0:
            quality["type_hint_coverage"] = round(
                (quality["total_python_files"] - len(quality["files_with_issues"])) / 
                quality["total_python_files"] * 100, 1
            )
        
        self.report_data["python_quality"] = quality
        return quality
    
    def analyze_documentation(self) -> Dict[str, Any]:
        """分析文档质量"""
        print("📚 分析文档质量...")
        
        docs = {
            "markdown_files": [],
            "readme_exists": False,
            "contributing_exists": False,
            "license_exists": False,
            "changelog_exists": False,
            "total_docs_size_kb": 0
        }
        
        # 检查关键文档文件
        key_files = {
            "README.md": "readme_exists",
            "CONTRIBUTING.md": "contributing_exists",
            "LICENSE": "license_exists",
            "CHANGELOG.md": "changelog_exists"
        }
        
        for filename, key in key_files.items():
            filepath = self.project_root / filename
            if filepath.exists():
                docs[key] = True
                size_kb = filepath.stat().st_size / 1024
                docs["total_docs_size_kb"] += size_kb
        
        # 收集所有markdown文件
        for root, dirs, files in os.walk(self.project_root):
            for file in files:
                if file.endswith('.md'):
                    filepath = Path(root) / file
                    rel_path = filepath.relative_to(self.project_root)
                    size_kb = filepath.stat().st_size / 1024
                    
                    docs["markdown_files"].append({
                        "path": str(rel_path),
                        "size_kb": round(size_kb, 2)
                    })
                    docs["total_docs_size_kb"] += size_kb
        
        self.report_data["documentation"] = docs
        return docs
    
    def analyze_automation(self) -> Dict[str, Any]:
        """分析自动化工具"""
        print("⚙️ 分析自动化工具...")
        
        automation = {
            "makefile_exists": False,
            "precommit_exists": False,
            "github_actions_exists": False,
            "ci_cd_configured": False,
            "testing_framework": "unknown"
        }
        
        # 检查Makefile
        if (self.project_root / "Makefile").exists():
            automation["makefile_exists"] = True
        
        # 检查pre-commit配置
        if (self.project_root / ".pre-commit-config.yaml").exists():
            automation["precommit_exists"] = True
        
        # 检查GitHub Actions
        workflows_dir = self.project_root / ".github" / "workflows"
        if workflows_dir.exists():
            automation["github_actions_exists"] = True
            workflow_files = list(workflows_dir.glob("*.yml")) + list(workflows_dir.glob("*.yaml"))
            automation["ci_cd_configured"] = len(workflow_files) > 0
        
        # 检查测试框架
        if (self.project_root / "pytest.ini").exists() or (self.project_root / "pyproject.toml").exists():
            automation["testing_framework"] = "pytest"
        elif (self.project_root / "tests").exists():
            automation["testing_framework"] = "unittest"
        
        self.report_data["automation"] = automation
        return automation
    
    def run_external_tools(self) -> Dict[str, Any]:
        """运行外部代码质量工具"""
        print("🔧 运行外部代码质量工具...")
        
        tools = {
            "flake8": {"installed": False, "issues": []},
            "black": {"installed": False, "check_passed": False},
            "mypy": {"installed": False, "issues": []}
        }
        
        try:
            # 检查flake8
            result = subprocess.run(
                ["flake8", "--version"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                tools["flake8"]["installed"] = True
                
                # 运行flake8检查
                flake8_result = subprocess.run(
                    ["flake8", str(self.project_root), "--count"],
                    capture_output=True,
                    text=True
                )
                if flake8_result.stdout:
                    tools["flake8"]["issues"] = flake8_result.stdout.strip().split('\n')
        
        except FileNotFoundError:
            pass
        
        try:
            # 检查black
            result = subprocess.run(
                ["black", "--version"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                tools["black"]["installed"] = True
                
                # 运行black检查
                black_result = subprocess.run(
                    ["black", "--check", str(self.project_root)],
                    capture_output=True,
                    text=True
                )
                tools["black"]["check_passed"] = black_result.returncode == 0
        
        except FileNotFoundError:
            pass
        
        try:
            # 检查mypy
            result = subprocess.run(
                ["mypy", "--version"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                tools["mypy"]["installed"] = True
                
                # 运行mypy检查（仅检查src目录）
                src_dir = self.project_root / "src"
                if src_dir.exists():
                    mypy_result = subprocess.run(
                        ["mypy", str(src_dir)],
                        capture_output=True,
                        text=True
                    )
                    if mypy_result.stdout:
                        tools["mypy"]["issues"] = mypy_result.stdout.strip().split('\n')[:10]  # 限制输出
        
        except FileNotFoundError:
            pass
        
        self.report_data["external_tools"] = tools
        return tools
    
    def generate_metrics(self) -> Dict[str, Any]:
        """生成综合指标"""
        print("📊 生成综合指标...")
        
        metrics = {
            "overall_score": 0,
            "structure_score": 0,
            "code_quality_score": 0,
            "documentation_score": 0,
            "automation_score": 0,
            "scores": {}
        }
        
        # 结构评分
        structure = self.report_data.get("structure", {})
        if structure:
            required_dirs = ["src", "tests", "docs", "examples"]
            existing_dirs = [d for d in required_dirs if any(d in dir_path for dir_path in structure["directories"])]
            metrics["structure_score"] = len(existing_dirs) / len(required_dirs) * 100
        
        # 代码质量评分
        python_quality = self.report_data.get("python_quality", {})
        if python_quality:
            files_with_issues = len(python_quality.get("files_with_issues", []))
            total_files = python_quality.get("total_python_files", 1)
            metrics["code_quality_score"] = (1 - files_with_issues / max(total_files, 1)) * 100
        
        # 文档评分
        documentation = self.report_data.get("documentation", {})
        if documentation:
            key_files = ["readme_exists", "contributing_exists", "license_exists", "changelog_exists"]
            existing_files = sum(1 for key in key_files if documentation.get(key, False))
            metrics["documentation_score"] = existing_files / len(key_files) * 100
        
        # 自动化评分
        automation = self.report_data.get("automation", {})
        if automation:
            automation_items = ["makefile_exists", "precommit_exists", "github_actions_exists", "ci_cd_configured"]
            existing_items = sum(1 for item in automation_items if automation.get(item, False))
            metrics["automation_score"] = existing_items / len(automation_items) * 100
        
        # 总体评分（加权平均）
        weights = {
            "structure": 0.2,
            "code_quality": 0.4,
            "documentation": 0.2,
            "automation": 0.2
        }
        
        metrics["overall_score"] = round(
            metrics["structure_score"] * weights["structure"] +
            metrics["code_quality_score"] * weights["code_quality"] +
            metrics["documentation_score"] * weights["documentation"] +
            metrics["automation_score"] * weights["automation"], 1
        )
        
        # 存储详细分数
        metrics["scores"] = {
            "structure": round(metrics["structure_score"], 1),
            "code_quality": round(metrics["code_quality_score"], 1),
            "documentation": round(metrics["documentation_score"], 1),
            "automation": round(metrics["automation_score"], 1)
        }
        
        self.report_data["metrics"] = metrics
        return metrics
    
    def generate_recommendations(self) -> List[str]:
        """生成改进建议"""
        print("💡 生成改进建议...")
        
        recommendations = []
        
        # 基于结构分析的建议
        structure = self.report_data.get("structure", {})
        if structure:
            python_files = len(structure.get("python_files", []))
            if python_files < 5:
                recommendations.append("添加更多Python代码示例")
        
        # 基于代码质量分析的建议
        python_quality = self.report_data.get("python_quality", {})
        if python_quality:
            files_with_issues = python_quality.get("files_with_issues", [])
            if files_with_issues:
                recommendations.append("修复Python代码质量问题")
            
            type_coverage = python_quality.get("type_hint_coverage", 0)
            if type_coverage < 80:
                recommendations.append("提高类型提示覆盖率")
        
        # 基于文档分析的建议
        documentation = self.report_data.get("documentation", {})
        if documentation:
            if not documentation.get("changelog_exists", False):
                recommendations.append("维护更新日志")
            
            markdown_files = documentation.get("markdown_files", [])
            if len(markdown_files) < 5:
                recommendations.append("添加更多文档")
        
        # 基于自动化分析的建议
        automation = self.report_data.get("automation", {})
        if automation:
            if not automation.get("precommit_exists", False):
                recommendations.append("配置pre-commit钩子")
            
            if not automation.get("ci_cd_configured", False):
                recommendations.append("设置CI/CD流水线")
        
        # 基于外部工具的建议
        external_tools = self.report_data.get("external_tools", {})
        if external_tools:
            if not external_tools.get("flake8", {}).get("installed", False):
                recommendations.append("安装flake8进行代码风格检查")
            
            if not external_tools.get("black", {}).get("installed", False):
                recommendations.append("安装black进行代码格式化")
        
        self.report_data["recommendations"] = recommendations
        return recommendations
    
    def generate_issues(self) -> List[Dict[str, Any]]:
        """生成问题列表"""
        print("⚠️ 生成问题列表...")
        
        issues = []
        
        # 检查Python文件问题
        python_quality = self.report_data.get("python_quality", {})
        if python_quality:
            for file_info in python_quality.get("files_with_issues", []):
                for issue in file_info["issues"]:
                    issues.append({
                        "type": "code_quality",
                        "severity": "medium",
                        "file": file_info["file"],
                        "description": issue,
                        "suggestion": "修复代码质量问题"
                    })
        
        # 检查文档问题
        documentation = self.report_data.get("documentation", {})
        if documentation:
            if not documentation.get("license_exists", False):
                issues.append({
                    "type": "documentation",
                    "severity": "high",
                    "file": "LICENSE",
                    "description": "缺少许可证文件",
                    "suggestion": "添加合适的开源许可证"
                })
        
        # 检查自动化问题
        automation = self.report_data.get("automation", {})
        if automation:
            if not automation.get("testing_framework") or automation["testing_framework"] == "unknown":
                issues.append({
                    "type": "automation",
                    "severity": "medium",
                    "file": "tests/",
                    "description": "测试框架未明确配置",
                    "suggestion": "配置pytest或unittest测试框架"
                })
        
        self.report_data["issues"] = issues
        return issues
    
    def save_report(self, output_format: str = "both") -> Tuple[Path, Path]:
        """保存报告"""
        print("💾 保存报告...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_path = self.project_root / f"reports/quality_report_{timestamp}.json"
        md_path = self.project_root / f"reports/quality_report_{timestamp}.md"
        
        # 创建reports目录
        reports_dir = self.project_root / "reports"
        reports_dir.mkdir(exist_ok=True)
        
        # 保存JSON报告
        if output_format in ["json", "both"]:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(self.report_data, f, indent=2, ensure_ascii=False)
            print(f"  📄 JSON报告: {json_path}")
        
        # 保存Markdown报告
        if output_format in ["markdown", "both"]:
            md_content = self._generate_markdown_report()
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(md_content)
            print(f"  📄 Markdown报告: {md_path}")
        
        return json_path, md_path
    
    def _generate_markdown_report(self) -> str:
        """生成Markdown格式报告"""
        metrics = self.report_data.get("metrics", {})
        structure = self.report_data.get("structure", {})
        python_quality = self.report_data.get("python_quality", {})
        documentation = self.report_data.get("documentation", {})
        automation = self.report_data.get("automation", {})
        issues = self.report_data.get("issues", [])
        recommendations = self.report_data.get("recommendations", [])
        
        # 生成评分徽章
        overall_score = metrics.get("overall_score", 0)
        score_color = "green" if overall_score >= 80 else "yellow" if overall_score >= 60 else "red"
        
        report = f"""# 项目质量检查报告

## 📊 总体评分

![总体评分](https://img.shields.io/badge/评分-{overall_score}/100-{score_color})
![生成时间](https://img.shields.io/badge/时间-{self.report_data['timestamp'][:10]}-blue)
![Python项目](https://img.shields.io/badge/Python-3.9%2B-blue)

### 详细评分
| 类别 | 分数 | 状态 |
|------|------|------|
| 项目结构 | {metrics.get('scores', {}).get('structure', 0)}/100 | {'✅' if metrics.get('structure_score', 0) >= 70 else '⚠️' if metrics.get('structure_score', 0) >= 50 else '❌'} |
| 代码质量 | {metrics.get('scores', {}).get('code_quality', 0)}/100 | {'✅' if metrics.get('code_quality_score', 0) >= 70 else '⚠️' if metrics.get('code_quality_score', 0) >= 50 else '❌'} |
| 文档质量 | {metrics.get('scores', {}).get('documentation', 0)}/100 | {'✅' if metrics.get('documentation_score', 0) >= 70 else '⚠️' if metrics.get('documentation_score', 0) >= 50 else '❌'} |
| 自动化 | {metrics.get('scores', {}).get('automation', 0)}/100 | {'✅' if metrics.get('automation_score', 0) >= 70 else '⚠️' if metrics.get('automation_score', 0) >= 50 else '❌'} |

## 📁 项目结构分析

### 文件统计
- 总文件数: {structure.get('total_files', 0)}
- 总大小: {structure.get('total_size_kb', 0):.1f} KB
- Python文件: {len(structure.get('python_files', []))}
- Markdown文件: {len(structure.get('markdown_files', []))}
- 其他文件: {len(structure.get('other_files', []))}

### 目录结构
```
{chr(10).join(f"- {dir_path}" for dir_path in structure.get('directories', [])[:20])}
{'...' if len(structure.get('directories', [])) > 20 else ''}
```

## 🐍 Python代码质量分析

### 基本统计
- Python文件总数: {python_quality.get('total_python_files', 0)}
- 总代码行数: {python_quality.get('total_lines', 0)}
- 有问题的文件: {len(python_quality.get('files_with_issues', []))}
- 类型提示覆盖率: {python_quality.get('type_hint_coverage', 0)}%

### 问题文件
"""
        
        # 添加问题文件
        for file_info in python_quality.get("files_with_issues", [])[:10]:
            report += f"- **{file_info['file']}** ({file_info['line_count']}行)\n"
            for issue in file_info["issues"][:3]:
                report += f"  - ⚠️ {issue}\n"
        
        if len(python_quality.get("files_with_issues", [])) > 10:
            report += f"- ... 还有 {len(python_quality.get('files_with_issues', [])) - 10} 个文件有问题\n"
        
        report += f"""
## 📚 文档质量分析

### 关键文档
"""
        
        # 添加关键文档状态
        doc_keys = [
            ("README.md", "readme_exists", "项目说明"),
            ("CONTRIBUTING.md", "contributing_exists", "贡献指南"),
            ("LICENSE", "license_exists", "许可证"),
            ("CHANGELOG.md", "changelog_exists", "更新日志")
        ]
        
        for filename, key, description in doc_keys:
            exists = documentation.get(key, False)
            report += f"- {'✅' if exists else '❌'} **{filename}** - {description}\n"
        
        report += f"""
### 文档统计
- Markdown文件总数: {len(documentation.get('markdown_files', []))}
- 文档总大小: {documentation.get('total_docs_size_kb', 0):.1f} KB

## ⚙️ 自动化工具分析

### 工具配置
"""
        
        # 添加自动化工具状态
        auto_items = [
            ("Makefile", "makefile_exists", "构建自动化"),
            ("pre-commit", "precommit_exists", "预提交钩子"),
            ("GitHub Actions", "github_actions_exists", "CI/CD"),
            ("CI/CD配置", "ci_cd_configured", "工作流配置"),
            ("测试框架", "testing_framework", automation.get("testing_framework", "未知"))
        ]
        
        for name, key, value in auto_items:
            if key == "testing_framework":
                status = f"`{value}`"
            else:
                exists = automation.get(key, False)
                status = "✅" if exists else "❌"
            report += f"- {status} **{name}** - {value}\n"
        
        report += f"""
## ⚠️ 发现的问题 ({len(issues)}个)

"""
        
        # 添加问题列表
        for i, issue in enumerate(issues[:10], 1):
            severity_emoji = {"high": "🔴", "medium": "🟡", "low": "🔵"}.get(issue["severity"], "⚪")
            report += f"{i}. {severity_emoji} **{issue['type']}** - {issue['file']}\n"
            report += f"   - 问题: {issue['description']}\n"
            report += f"   - 建议: {issue['suggestion']}\n"
        
        if len(issues) > 10:
            report += f"... 还有 {len(issues) - 10} 个问题\n"
        
        report += f"""
## 💡 改进建议 ({len(recommendations)}条)

"""
        
        # 添加建议列表
        for i, recommendation in enumerate(recommendations, 1):
            report += f"{i}. ✅ {recommendation}\n"
        
        report += f"""
## 🚀 下一步行动

### 立即处理
1. 修复高优先级问题
2. 完善缺失的文档
3. 配置自动化工具

### 短期计划
1. 提高代码质量分数到80+
2. 完善测试覆盖率
3. 优化项目结构

### 长期目标
1. 达到90+的总体评分
2. 建立完整的CI/CD流程
3. 提高代码可维护性

## 📈 趋势跟踪

建议定期运行质量检查，跟踪改进进度：

```bash
# 运行质量检查
python scripts/quality_report.py

# 查看最新报告
ls -la reports/
```

---

*报告生成时间: {self.report_data['timestamp']}*
*项目: {self.report_data['project']}*
"""
        
        return report
    
    def run_analysis(self) -> Dict[str, Any]:
        """运行完整分析"""
        print("=" * 60)
        print("🔍 开始项目质量分析")
        print("=" * 60)
        
        # 运行各个分析步骤
        self.analyze_project_structure()
        self.analyze_python_code_quality()
        self.analyze_documentation()
        self.analyze_automation()
        self.run_external_tools()
        self.generate_metrics()
        self.generate_issues()
        self.generate_recommendations()
        
        # 保存报告
        json_path, md_path = self.save_report("both")
        
        print("=" * 60)
        print("🎉 质量分析完成！")
        print("=" * 60)
        
        # 显示摘要
        metrics = self.report_data["metrics"]
        print(f"\n📊 分析摘要:")
        print(f"  总体评分: {metrics['overall_score']}/100")
        print(f"  项目结构: {metrics['scores']['structure']}/100")
        print(f"  代码质量: {metrics['scores']['code_quality']}/100")
        print(f"  文档质量: {metrics['scores']['documentation']}/100")
        print(f"  自动化: {metrics['scores']['automation']}/100")
        print(f"\n📋 发现 {len(self.report_data['issues'])} 个问题")
        print(f"💡 提出 {len(self.report_data['recommendations'])} 条建议")
        print(f"\n📄 报告文件:")
        print(f"  JSON: {json_path}")
        print(f"  Markdown: {md_path}")
        
        return self.report_data


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="项目质量检查报告生成器")
    parser.add_argument("--project", "-p", default=".", help="项目根目录路径")
    parser.add_argument("--output", "-o", choices=["json", "markdown", "both"], default="both", help="输出格式")
    parser.add_argument("--quiet", "-q", action="store_true", help="安静模式，减少输出")
    
    args = parser.parse_args()
    
    # 设置项目根目录
    project_root = Path(args.project).absolute()
    if not project_root.exists():
        print(f"错误: 项目目录不存在: {project_root}")
        sys.exit(1)
    
    # 运行分析
    analyzer = QualityAnalyzer(project_root)
    report = analyzer.run_analysis()
    
    # 根据评分退出
    overall_score = report["metrics"]["overall_score"]
    if overall_score < 60:
        print("\n⚠️  警告: 项目质量评分较低，建议立即改进")
        sys.exit(1)
    elif overall_score < 80:
        print("\nℹ️  提示: 项目质量有改进空间")
        sys.exit(0)
    else:
        print("\n✅ 优秀: 项目质量良好")
        sys.exit(0)


if __name__ == "__main__":
    main()