# hello-python 学习资料重构设计

## 目标

将 hello-python 重构为一个专业、完整的 Python 学习资源仓库。

## 项目结构

```
hello-python/
├── src/hello_python/
│   ├── __init__.py              # 版本、包信息
│   ├── cli.py                   # CLI 入口 (list/show/run/check)
│   ├── runner.py                # 安全代码运行器
│   └── lessons/                 # 从 codes/ 迁入，按学习阶段组织
│       ├── __init__.py
│       ├── index.py             # 学习路径定义（11个阶段）
│       ├── stage01_basic/
│       ├── stage02_cycle/
│       ├── stage03_function/
│       ├── stage04_advanced_grammar/
│       ├── stage05_advanced_data_structures/
│       ├── stage06_oop_basic/
│       ├── stage07_oop_advanced/
│       ├── stage08_oop_inherit/
│       ├── stage09_oop_encapsulation/
│       ├── stage10_oop_application/
│       └── stage11_card_manage/
├── tests/
│   ├── test_lessons.py          # 验证所有课程代码可 import 无语法错误
│   └── test_runner.py
├── doc/                         # 中文教程文档（不变）
├── examples/
│   └── basic_usage.py
├── scripts/
│   └── quality_report.py
├── config/
├── README.md
├── Makefile
├── pyproject.toml
├── .pre-commit-config.yaml
├── .github/workflows/ci.yml
└── .gitignore
```

## 核心模块

### lessons/index.py — 学习路径索引

定义 `STAGES` 列表，每个阶段包含：
- `id`: 阶段标识
- `name`: 中文名称
- `description`: 简短描述
- `requires`: 前置阶段 id 列表
- `files`: 该阶段 Python 文件列表

提供 `get_stage(id)`, `list_stages()`, `get_ordered_stages()` 函数。

### cli.py — 命令行入口

- `hello-python list` — 列出所有学习阶段
- `hello-python show <stage>` — 显示阶段详情和代码列表
- `hello-python run <stage>` — 运行该阶段示例
- `hello-python check` — 检查 Python 版本和依赖

使用 argparse 实现，不引入额外依赖。

### runner.py — 代码运行器

- 读取指定 stage 的 .py 文件，使用 subprocess 安全执行
- 捕获输出并显示给用户
- 超时保护

### __init__.py — 精简

移除 greet、calculate_fibonacci、analyze_text、PythonTutorial、CodeInspector 等样板代码，只保留包元信息。

## 清理清单

| 文件/目录 | 操作 | 原因 |
|---|---|---|
| `optimize_project.py` | 删除 | 与学习资料定位无关 |
| `src/hello_python/__init__.py` 样板代码 | 删除 | greet/fibonacci 等与学习无关 |
| `tests/test_basic.py` | 重写为 test_lessons.py / test_runner.py | 旧测试针对已删除的样板代码 |
| `codes/` | 整体迁入 lessons/ | 重命名体现学习顺序 |
| `docs/` | 合并到 doc/ 或删除 | 消除重复 |
| `reports/` | 删除旧报告 | 临时产物 |
| `Makefile` | 移除 java_code_inspector 路径 | 该目录已删除 |
| `.pre-commit-config.yaml` | 同上 | 同上 |
| `.github/workflows/ci.yml` | 更新测试路径，添加多版本 | 适配新结构 |
| `.github/workflows/release.yml` | 删除 | 暂不需要发布 |
| `README.md` | 重写 | 突出学习资料定位 |
| `PROJECT_SUMMARY.md` | 更新 | 反映新结构 |
| `CHANGELOG.md` | 更新 | 记录本次变更 |
| `.DS_Store` | 删除 + 加入 .gitignore | 不应跟踪 |

## 测试策略

- **test_lessons.py**：遍历所有 stage 的 .py 文件，对每个文件做 `compile()` 检查语法，确保所有示例代码无语法错误
- **test_runner.py**：验证 runner 能正确执行代码并捕获输出
- 不要求运行所有示例（部分示例可能需要交互输入），但必须保证语法正确

## CI / 工具链

- flake8、black、isort、mypy 保持现有配置
- CI 保留多 Python 版本测试（3.9/3.10/3.11）
- 移除 CodeQL（Python 项目价值有限）
- 移除 codecov 上传（保持简单）
- pre-commit 更新 exclude 路径
