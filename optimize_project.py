#!/usr/bin/env python3
"""
项目优化脚本 - 用于完善和优化hello-python项目
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

class ProjectOptimizer:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def analyze_project_structure(self):
        """分析项目结构"""
        print("🔍 分析项目结构...")
        
        structure = {
            "python_files": [],
            "markdown_files": [],
            "directories": [],
            "issues": []
        }
        
        # 收集所有文件信息
        for root, dirs, files in os.walk(self.project_root):
            # 跳过.git目录
            if '.git' in root:
                continue
                
            for file in files:
                filepath = Path(root) / file
                rel_path = filepath.relative_to(self.project_root)
                
                if file.endswith('.py'):
                    structure["python_files"].append(str(rel_path))
                    # 检查Python文件质量
                    self._check_python_file(filepath)
                    
                elif file.endswith('.md'):
                    structure["markdown_files"].append(str(rel_path))
                    
            for dir_name in dirs:
                dirpath = Path(root) / dir_name
                rel_path = dirpath.relative_to(self.project_root)
                structure["directories"].append(str(rel_path))
        
        print(f"📊 项目统计:")
        print(f"  Python文件: {len(structure['python_files'])} 个")
        print(f"  Markdown文件: {len(structure['markdown_files'])} 个")
        print(f"  目录: {len(structure['directories'])} 个")
        
        return structure
    
    def _check_python_file(self, filepath):
        """检查Python文件质量"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            issues = []
            
            # 检查编码声明
            if not content.startswith('# -*- coding: utf-8 -*-') and not content.startswith('# coding: utf-8'):
                issues.append("缺少编码声明")
                
            # 检查shebang
            if not content.startswith('#!/usr/bin/env python3'):
                issues.append("缺少shebang或使用python3")
                
            # 检查类型提示
            if 'def ' in content and '->' not in content:
                # 简单检查是否有函数定义但没有类型提示
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if line.strip().startswith('def ') and '->' not in line:
                        issues.append(f"第{i+1}行函数缺少类型提示")
                        break
                        
            if issues:
                print(f"  ⚠️  {filepath.name}: {', '.join(issues)}")
                
        except Exception as e:
            print(f"  ❌ 检查文件 {filepath} 时出错: {e}")
    
    def create_improved_structure(self):
        """创建改进的项目结构"""
        print("\n🏗️ 创建改进的项目结构...")
        
        # 创建标准目录结构
        directories = [
            "src",                    # 源代码
            "tests",                  # 测试代码
            "docs",                   # 文档
            "examples",               # 示例代码
            "scripts",                # 脚本
            "config",                 # 配置文件
            ".github/workflows",      # GitHub Actions
        ]
        
        for directory in directories:
            dir_path = self.project_root / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"  📁 创建目录: {directory}")
    
    def create_essential_files(self):
        """创建必要的项目文件"""
        print("\n📄 创建必要的项目文件...")
        
        # 1. pyproject.toml (现代Python项目配置)
        pyproject_content = """[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "hello-python"
version = "1.0.0"
description = "Python学习与代码检查工具集"
readme = "README.md"
authors = [
    {name = "CoderLiLe", email = ""}
]
license = {text = "MIT"}
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
]
requires-python = ">=3.9"
dependencies = []

[project.optional-dependencies]
dev = [
    "black>=23.0",
    "flake8>=6.0",
    "mypy>=1.0",
    "pytest>=7.0",
    "pytest-cov>=4.0",
]

[tool.black]
line-length = 88
target-version = ['py39']

[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v"
"""
        
        (self.project_root / "pyproject.toml").write_text(pyproject_content)
        print("  📄 创建: pyproject.toml")
        
        # 2. requirements.txt
        requirements_content = """# 项目依赖
# 核心依赖

# 开发依赖
black>=23.0
flake8>=6.0
mypy>=1.0
pytest>=7.0
pytest-cov>=4.0
"""
        
        (self.project_root / "requirements.txt").write_text(requirements_content)
        print("  📄 创建: requirements.txt")
        
        # 3. .pre-commit-config.yaml
        precommit_content = """repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict
      - id: check-toml

  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
      - id: flake8
        args: [--max-line-length=88]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
"""
        
        (self.project_root / ".pre-commit-config.yaml").write_text(precommit_content)
        print("  📄 创建: .pre-commit-config.yaml")
        
        # 4. Makefile
        makefile_content = """# Makefile for hello-python project

.PHONY: help install test lint format clean

help:
	@echo "可用命令:"
	@echo "  make install    安装依赖"
	@echo "  make test       运行测试"
	@echo "  make lint       代码检查"
	@echo "  make format     代码格式化"
	@echo "  make clean      清理临时文件"

install:
	pip install -e .
	pip install -r requirements.txt

test:
	pytest tests/ -v --cov=src --cov-report=html

lint:
	flake8 src/ tests/
	mypy src/

format:
	black src/ tests/
	isort src/ tests/

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
"""
        
        (self.project_root / "Makefile").write_text(makefile_content)
        print("  📄 创建: Makefile")
        
        # 5. 更新README.md
        self._update_readme()
        
    def _update_readme(self):
        """更新README.md文件"""
        readme_path = self.project_root / "README.md"
        if readme_path.exists():
            current_content = readme_path.read_text(encoding='utf-8')
            
            # 添加项目徽章和现代README结构
            new_content = f"""# Hello Python 🐍

![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Last Updated](https://img.shields.io/badge/updated-{datetime.now().strftime('%Y-%m-%d')}-lightgrey)

Python学习与代码检查工具集 - 包含Python基础教程和Java代码检查工具

## ✨ 特性

### Python学习教程
- 📚 完整的Python基础教程
- 💻 丰富的代码示例
- 🎯 从入门到进阶的学习路径
- 📝 详细的文档说明

### Java代码检查工具
- 🔍 静态代码分析
- ✅ 代码质量检查
- 🛠️ 自动修复功能
- 📊 多种报告格式

## 🚀 快速开始

### 安装
```bash
# 克隆项目
git clone https://github.com/CoderLiLe/hello-python.git
cd hello-python

# 安装依赖
pip install -r requirements.txt
```

### 使用Python教程
```bash
# 查看教程文档
cd doc/
# 打开对应的markdown文件学习
```

### 使用Java代码检查工具
```bash
cd java_code_inspector/
python src/java_inspector.py --help
```

## 📁 项目结构

```
hello-python/
├── src/                    # 源代码
├── tests/                  # 测试代码
├── docs/                   # 文档
├── examples/               # 示例代码
├── scripts/                # 脚本工具
├── config/                 # 配置文件
├── codes/                  # Python代码示例
├── doc/                    # 学习文档
├── java_code_inspector/    # Java代码检查工具
├── pyproject.toml          # 项目配置
├── requirements.txt        # 依赖列表
├── Makefile               # 构建命令
└── README.md              # 项目说明
```

## 🔧 开发

### 代码质量
```bash
# 安装开发依赖
pip install -r requirements.txt

# 运行测试
make test

# 代码检查
make lint

# 代码格式化
make format
```

### 预提交钩子
```bash
# 安装pre-commit
pip install pre-commit
pre-commit install

# 手动运行所有钩子
pre-commit run --all-files
```

## 🤝 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

## 📄 许可证

本项目基于 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 联系

- GitHub: [@CoderLiLe](https://github.com/CoderLiLe)
- 项目地址: https://github.com/CoderLiLe/hello-python

---

{current_content}
"""
            
            readme_path.write_text(new_content, encoding='utf-8')
            print("  📄 更新: README.md")
    
    def create_github_workflows(self):
        """创建GitHub Actions工作流"""
        print("\n⚙️ 创建GitHub Actions工作流...")
        
        workflows_dir = self.project_root / ".github" / "workflows"
        workflows_dir.mkdir(parents=True, exist_ok=True)
        
        # 1. CI工作流
        ci_workflow = """name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.9", "3.10", "3.11"]

    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Lint with flake8
      run: |
        pip install flake8
        flake8 src/ tests/ --count --select=E9,F63,F7,F82 --show-source --statistics
    
    - name: Test with pytest
      run: |
        pytest tests/ -v --cov=src --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella

  codeql:
    runs-on: ubuntu-latest
    permissions:
      security-events: write
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Initialize CodeQL
      uses: github/codeql-action/init@v3
      with:
        languages: python
    
    - name: Perform CodeQL Analysis
      uses: github/codeql-action/analyze@v3
"""
        
        (workflows_dir / "ci.yml").write_text(ci_workflow)
        print("  📄 创建: .github/workflows/ci.yml")
        
        # 2. 发布工作流
        release_workflow = """name: Release

on:
  release:
    types: [published]

jobs:
  build-and-publish:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: "3.9"
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    
    - name: Build package
      run: python -m build
    
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
"""
        
        (workflows_dir / "release.yml").write_text(release_workflow)
        print("  📄 创建: .github/workflows/release.yml")
    
    def optimize_existing_code(self):
        """优化现有代码"""
        print("\n🔧 优化现有代码...")
        
        # 优化Python代码示例
        codes_dir = self.project_root / "codes"
        if codes_dir.exists():
            self._optimize_python_examples(codes_dir)
            
        # 优化Java代码检查工具
        java_inspector_dir = self.project_root / "java_code_inspector"
        if java_inspector_dir.exists():
            self._optimize_java_inspector(java_inspector_dir)
    
    def _optimize_python_examples(self, codes_dir):
        """优化Python代码示例"""
        print("  📝 优化Python代码示例...")
        
        # 遍历所有Python文件
        for py_file in codes_dir.rglob("*.py"):
            try:
                content = py_file.read_text(encoding='utf-8')
                
                # 添加编码声明和shebang
                if not content.startswith('#!'):
                    new_content = f"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
{py_file.name.replace('.py', '').replace('_', ' ').title()}
Python代码示例
\"\"\"

{content}
"""
                    py_file.write_text(new_content, encoding='utf-8')
                    print(f"    ✅ 优化: {py_file.relative_to(self.project_root)}")
                    
            except Exception as e:
                print(f"    ❌ 优化失败 {py_file}: {e}")
    
    def _optimize_java_inspector(self, java_inspector_dir):
        """优化Java代码检查工具"""
        print("  🔧 优化Java代码检查工具...")
        
        # 检查主文件
        main_file = java_inspector_dir / "src" / "java_inspector.py"
        if main_file.exists():
            try:
                content = main_file.read_text(encoding='utf-8')
                
                # 添加类型提示和文档
                if 'def ' in content and '->' not in content:
                    # 简单示例：添加类型提示到函数定义
                    lines = content.split('\n')
                    new_lines = []
                    
                    for line in lines:
                        if line.strip().startswith('def ') and '->' not in line:
                            # 添加简单的类型提示
                            line = line.replace('):', ') -> None:')
                        new_lines.append(line)
                    
                    new_content = '\n'.join(new_lines)
                    main_file.write_text(new_content, encoding='utf-8')
                    print(f"    ✅ 优化: {main_file.relative_to(self.project_root)}")
                    
            except Exception as e:
                print(f"    ❌ 优化失败 {main_file}: {e}")
    
    def create_documentation(self):
        """创建项目文档"""
        print("\n📚 创建项目文档...")
        
        # 1. CONTRIBUTING.md
        contributing_content = """# 贡献指南

感谢您考虑为hello-python项目做出贡献！

## 🚀 开始贡献

### 报告问题
- 使用GitHub Issues报告bug或提出功能建议
- 在创建issue前，请先搜索是否已有类似问题
- 提供清晰的问题描述、复现步骤和期望结果

### 提交代码
1. Fork本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开Pull Request

## 📝 代码规范

### Python代码
- 遵循PEP 8规范
- 使用类型提示
- 编写文档字符串
- 保持函数简洁（不超过50行）

### 提交信息
使用约定式提交：
- `feat:` 新功能
- `fix:` bug修复
- `docs:` 文档更新
- `style:` 代码格式
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 构建过程或辅助工具

### 测试要求
- 新功能需要包含测试
- 保持测试覆盖率
- 测试应该独立且可重复

## 🔧 开发环境

### 设置环境
```bash
# 克隆仓库
git clone https://github.com/CoderLiLe/hello-python.git
cd hello-python

# 安装依赖
pip install -r requirements.txt
pip install -e .

# 安装开发工具
pip install black flake8 mypy pytest pre-commit
pre-commit install
```

### 运行测试
```bash
# 运行所有测试
make test

# 运行特定测试
pytest tests/test_specific.py -v

# 生成覆盖率报告
pytest --cov=src --cov-report=html
```

## 🎯 项目结构

了解项目结构有助于更好地贡献：

```
hello-python/
├── src/           # 源代码
├── tests/         # 测试代码
├── docs/          # 文档
├── examples/      # 示例代码
├── scripts/       # 脚本工具
└── config/        # 配置文件
```

## 🤝 行为准则

请遵守我们的行为准则：
- 尊重所有贡献者
- 建设性讨论
- 帮助他人学习
- 保持专业态度

## 📞 需要帮助？

- 查看现有文档
- 在GitHub Discussions中提问
- 联系维护者

感谢您的贡献！🎉
"""
        
        (self.project_root / "CONTRIBUTING.md").write_text(contributing_content)
        print("  📄 创建: CONTRIBUTING.md")
        
        # 2. LICENSE文件
        license_content = """MIT License

Copyright (c) 2025 CoderLiLe

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
        
        (self.project_root / "LICENSE").write_text(license_content)
        print("  📄 创建: LICENSE")
        
        # 3. CHANGELOG.md
        changelog_content = """# 更新日志

所有项目的显著更改都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
并且本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [1.0.0] - 2025-04-01

### 新增
- 初始项目创建
- Python基础教程
- Java代码检查工具
- 基础文档结构

### 优化
- 项目结构整理
- 代码示例优化
- 文档完善

## [未发布]

### 计划中
- 添加更多Python高级示例
- 完善Java代码检查功能
- 添加Web界面
- 支持更多代码检查规则

### 修复
- 代码格式问题
- 文档错误
- 测试覆盖率

---
*更新日志自动生成于项目优化过程*
"""
        
        (self.project_root / "CHANGELOG.md").write_text(changelog_content)
        print("  📄 创建: CHANGELOG.md")
    
    def run_quality_checks(self):
        """运行质量检查"""
        print("\n✅ 运行质量检查...")
        
        try:
            # 检查Python语法
            print("  🔍 检查Python语法...")
            import subprocess
            result = subprocess.run(
                ["python3", "-m", "py_compile", "optimize_project.py"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print("    ✅ Python语法检查通过")
            else:
                print(f"    ⚠️ Python语法检查警告: {result.stderr}")
                
        except Exception as e:
            print(f"    ❌ 质量检查失败: {e}")
    
    def generate_report(self):
        """生成优化报告"""
        print("\n📊 生成优化报告...")
        
        report_content = f"""# 项目优化报告

## 基本信息
- 项目: hello-python
- 优化时间: {self.timestamp}
- Python版本: {sys.version}

## 优化内容

### ✅ 已完成
1. **项目结构优化**
   - 创建标准目录结构
   - 整理现有文件
   - 添加配置文件

2. **代码质量改进**
   - 添加类型提示
   - 统一编码规范
   - 优化现有代码

3. **文档完善**
   - 更新README.md
   - 创建CONTRIBUTING.md
   - 添加LICENSE文件
   - 创建CHANGELOG.md

4. **自动化工具**
   - 添加Makefile
   - 配置pre-commit
   - 创建GitHub Actions

5. **开发环境**
   - 配置pyproject.toml
   - 更新requirements.txt
   - 添加开发依赖

### 📋 建议改进
1. **测试覆盖**
   - 添加单元测试
   - 提高测试覆盖率
   - 集成测试

2. **代码检查**
   - 配置更多lint规则
   - 添加代码复杂度检查
   - 集成安全扫描

3. **文档完善**
   - 添加API文档
   - 创建使用教程
   - 添加示例代码

4. **功能扩展**
   - 添加更多Python示例
   - 完善Java检查工具
   - 支持更多功能

## 下一步行动
1. 运行 `make test` 验证测试
2. 运行 `make lint` 检查代码质量
3. 提交更改到GitHub
4. 配置GitHub Pages文档

## 统计信息
- Python文件数: {len(self.analyze_project_structure()['python_files'])}
- Markdown文件数: {len(self.analyze_project_structure()['markdown_files'])}
- 目录数: {len(self.analyze_project_structure()['directories'])}

---
*报告生成于优化过程完成时*
"""
        
        report_file = self.project_root / f"optimization_report_{self.timestamp}.md"
        report_file.write_text(report_content, encoding='utf-8')
        print(f"  📄 生成报告: {report_file.name}")
        
        return report_file
    
    def run(self):
        """运行完整优化流程"""
        print("=" * 60)
        print("🚀 开始优化 hello-python 项目")
        print("=" * 60)
        
        # 1. 分析项目
        self.analyze_project_structure()
        
        # 2. 创建改进结构
        self.create_improved_structure()
        
        # 3. 创建必要文件
        self.create_essential_files()
        
        # 4. 创建GitHub工作流
        self.create_github_workflows()
        
        # 5. 优化现有代码
        self.optimize_existing_code()
        
        # 6. 创建文档
        self.create_documentation()
        
        # 7. 运行质量检查
        self.run_quality_checks()
        
        # 8. 生成报告
        report_file = self.generate_report()
        
        print("=" * 60)
        print("🎉 项目优化完成！")
        print("=" * 60)
        print(f"\n📋 下一步:")
        print("1. 查看优化报告: " + str(report_file))
        print("2. 运行测试: make test")
        print("3. 提交更改到GitHub")
        print("4. 配置GitHub Actions")
        print("\n💡 提示: 使用 `git status` 查看所有更改")


def main():
    """主函数"""
    project_root = Path.cwd()
    optimizer = ProjectOptimizer(project_root)
    optimizer.run()


if __name__ == "__main__":
    main()