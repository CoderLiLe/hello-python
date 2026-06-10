# 更新日志

## [1.1.0] - 2026-06-10

### 新增
- 学习路径索引 (lessons/index.py) 定义 11 个阶段
- CLI 工具 (cli.py) 支持 list/show/run/check
- 代码运行器 (runner.py) 安全执行课程代码
- 课程文件编译测试

### 变更
- codes/ 迁移至 src/hello_python/lessons/ 并添加 stage 编号
- 精简核心包 __init__.py
- 移除 java_code_inspector 所有残留引用
- 更新 Makefile、CI、pre-commit 配置
- 重写 README 和项目文档

### 移除
- optimize_project.py
- greet/fibonacci/text_analysis 等样板代码
- GitHub Actions release 工作流

## [1.0.0] - 2025-04-01

### 新增
- 初始项目创建
- Python 基础教程
- 基础文档结构
