# hello-python 学习资料重构 — 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 hello-python 重构为专业、完整的 Python 学习资源仓库，清理 java_code_inspector 残留，将 codes/ 整合为结构化的 lessons/，添加 CLI 入口和代码运行器。

**Architecture:** 基于方案 B：`codes/` → `src/hello_python/lessons/`（按 11 个学习阶段编号），新增 `cli.py`（argparse CLI）和 `runner.py`（subprocess 安全执行器），删除样板代码和残留引用。

**Tech Stack:** Python 3.9+, argparse, subprocess, pytest

---

## 文件变更总览

| 操作 | 文件 |
|---|---|
| 创建 | `src/hello_python/lessons/__init__.py` |
| 创建 | `src/hello_python/lessons/index.py` |
| 创建 | `src/hello_python/cli.py` |
| 创建 | `src/hello_python/runner.py` |
| 创建 | `tests/test_lessons.py` |
| 创建 | `tests/test_runner.py` |
| 重写 | `src/hello_python/__init__.py` |
| 重写 | `examples/basic_usage.py` |
| 重写 | `README.md` |
| 重写 | `docs/getting_started.md` |
| 移动 | `codes/*` → `src/hello_python/lessons/stage*` |
| 删除 | `tests/test_basic.py` |
| 删除 | `optimize_project.py` |
| 删除 | `optimization_report_*.md` |
| 删除 | `.DS_Store` (untrack) |
| 修改 | `Makefile` |
| 修改 | `.pre-commit-config.yaml` |
| 修改 | `.github/workflows/ci.yml` |
| 修改 | `pyproject.toml` |
| 修改 | `PROJECT_SUMMARY.md` |
| 修改 | `CHANGELOG.md` |
| 删除 | `.github/workflows/release.yml` |

---

### Task 1: 迁入 lessons/ 目录并添加 __init__.py

**Files:**
- Create: `src/hello_python/lessons/__init__.py`
- Create: `src/hello_python/lessons/stage01_basic/__init__.py` 等

**说明:** 将 `codes/` 下所有目录迁移到 `src/hello_python/lessons/`，重命名为 stage 编号前缀。为原本没有 `__init__.py` 的目录创建空的 `__init__.py`（已有的保留）。

- [ ] **Step 1: 执行目录迁移**

```bash
cd /Users/lile/Desktop/mycode/hello-python

# 创建 lessons 目录
mkdir -p src/hello_python/lessons

# 迁移所有子目录（stage 编号前缀）
mv codes/python_basic src/hello_python/lessons/stage01_basic
mv codes/cycle src/hello_python/lessons/stage02_cycle
mv codes/function src/hello_python/lessons/stage03_function
mv codes/advanced_grammar src/hello_python/lessons/stage04_advanced_grammar
mv codes/advanced_data_structures src/hello_python/lessons/stage05_advanced_data_structures
mv codes/oop_basic src/hello_python/lessons/stage06_oop_basic
mv codes/oop_advanced src/hello_python/lessons/stage07_oop_advanced
mv codes/oop_inherit src/hello_python/lessons/stage08_oop_inherit
mv codes/oop_encapsulation src/hello_python/lessons/stage09_oop_encapsulation
mv codes/oop_application src/hello_python/lessons/stage10_oop_application
mv codes/card_manage src/hello_python/lessons/stage11_card_manage

# 删除空的 codes/ 目录和其中的 .DS_Store
rm -rf codes
```

- [ ] **Step 2: 为缺少 __init__.py 的目录创建空文件**

```bash
cd /Users/lile/Desktop/mycode/hello-python

# 已有 __init__.py: stage06-10
# 缺少的: stage01-05, stage11
for d in stage01_basic stage02_cycle stage03_function stage04_advanced_grammar stage05_advanced_data_structures stage11_card_manage; do
  touch "src/hello_python/lessons/$d/__init__.py"
done
```

- [ ] **Step 3: 创建 lessons/__init__.py**

Write `src/hello_python/lessons/__init__.py`:

```python
"""hello-python 学习课程模块"""
```

- [ ] **Step 4: 验证迁移结果**

```bash
cd /Users/lile/Desktop/mycode/hello-python
find src/hello_python/lessons -maxdepth 2 -type f -name "*.py" | sort
```

Expected: 11 个 stage 目录，每个都有 `__init__.py`，原有 .py 文件都在。

- [ ] **Step 5: 提交**

```bash
git add src/hello_python/lessons/ codes/
git commit -m "refactor: move codes/ to src/hello_python/lessons/ with stage numbering"
```

---

### Task 2: 编写 lessons/index.py 学习路径索引

**Files:**
- Create: `src/hello_python/lessons/index.py`
- Test: `tests/test_lessons.py`

- [ ] **Step 1: 编写 tests/test_lessons.py 中 index 相关测试**

Write `tests/test_lessons.py`:

```python
import pytest
import sys
from pathlib import Path

# 确保 lessons 在 path 中
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from hello_python.lessons.index import STAGES, get_stage, list_stages, get_ordered_stages


class TestIndex:
    def test_stages_is_list(self):
        assert isinstance(STAGES, list)
        assert len(STAGES) == 11

    def test_each_stage_has_required_fields(self):
        for stage in STAGES:
            assert "id" in stage
            assert "name" in stage
            assert "description" in stage
            assert "files" in stage

    def test_stage_ids_are_unique(self):
        ids = [s["id"] for s in STAGES]
        assert len(ids) == len(set(ids))

    def test_get_stage_valid(self):
        stage = get_stage("stage01_basic")
        assert stage is not None
        assert stage["name"] == "Python基础"

    def test_get_stage_invalid(self):
        assert get_stage("nonexistent") is None

    def test_list_stages(self):
        names = list_stages()
        assert isinstance(names, list)
        assert len(names) == 11
        assert ("stage01_basic", "Python基础") in names

    def test_get_ordered_stages_respects_requires(self):
        ordered = get_ordered_stages()
        assert len(ordered) == 11
        # stage01 应该在最前面（无前置依赖）
        assert ordered[0]["id"] == "stage01_basic"

    def test_all_files_exist(self):
        """验证索引中引用的所有文件都存在"""
        lessons_dir = Path(__file__).parent.parent / "src" / "hello_python" / "lessons"
        for stage in STAGES:
            stage_dir = lessons_dir / stage["id"]
            assert stage_dir.is_dir(), f"Directory missing: {stage['id']}"
            for filename in stage["files"]:
                filepath = stage_dir / filename
                assert filepath.is_file(), f"File missing: {stage['id']}/{filename}"


class TestCompileAll:
    """验证所有课程代码无语法错误"""

    @pytest.mark.parametrize("stage", STAGES)
    def test_stage_files_compile(self, stage):
        lessons_dir = Path(__file__).parent.parent / "src" / "hello_python" / "lessons"
        for filename in stage["files"]:
            filepath = lessons_dir / stage["id"] / filename
            with open(filepath, "r", encoding="utf-8") as f:
                source = f.read()
            compile(source, str(filepath), "exec")
```

- [ ] **Step 2: 运行测试确认失败**

```bash
cd /Users/lile/Desktop/mycode/hello-python
python -m pytest tests/test_lessons.py -v
```

Expected: FAIL — `ModuleNotFoundError: No module named 'hello_python.lessons.index'`

- [ ] **Step 3: 编写 lessons/index.py**

Write `src/hello_python/lessons/index.py`:

```python
"""学习路径索引 — 定义所有学习阶段及其文件列表"""
from typing import List, Dict, Optional

STAGES: List[Dict] = [
    {
        "id": "stage01_basic",
        "name": "Python基础",
        "description": "认识 Python：注释、print 输出、第一个程序",
        "requires": [],
        "files": ["comment.py", "print.py"],
    },
    {
        "id": "stage02_cycle",
        "name": "循环",
        "description": "while/for 循环、break/continue、循环嵌套",
        "requires": ["stage01_basic"],
        "files": [
            "cycle.py", "sum.py", "even_sum.py", "break.py", "continue.py",
            "print_star.py", "cycle_print_star.py", "print_end.py",
            "escape_character.py", "multiplication_table.py",
        ],
    },
    {
        "id": "stage03_function",
        "name": "函数",
        "description": "函数定义、参数、返回值、嵌套调用、模块化",
        "requires": ["stage02_cycle"],
        "files": [
            "first_func.py", "first_func_refact.py", "func_return_value.py",
            "function_parameters.py", "nested_func_calls.py",
            "print_line.py", "print_multiple_line.py", "multiplication_table.py",
            "import_func.py", "divider_module.py", "experience_module.py",
        ],
    },
    {
        "id": "stage04_advanced_grammar",
        "name": "高级语法",
        "description": "全局/局部变量、多返回值、默认参数、递归、拆包",
        "requires": ["stage03_function"],
        "files": [
            "global_variables.py", "global_variables2.py",
            "global_variable_name.py", "global_variables_location.py",
            "update_global_variables.py", "local_variables.py",
            "mult_return_values.py", "multi_parameters.py",
            "multi_parameter_sum.py", "default_func_parameters.py",
            "define_func_default_parameter.py", "notes_default_parameter.py",
            "parameter_passing.py", "func_modify_parameters.py",
            "recur_func_features.py", "recur_func_sum.py",
            "swap_nums.py", "unpack_tuple_dict.py", "plus_equal.py", "quote.py",
        ],
    },
    {
        "id": "stage05_advanced_data_structures",
        "name": "高级数据结构",
        "description": "列表、元组、字典、字符串的常用操作",
        "requires": ["stage02_cycle"],
        "files": [
            "list_basic_use.py", "list_traversal.py", "list_statistics.py",
            "list_sort.py", "tuple_basic_use.py", "tuple_traversal.py",
            "dictionary_definition.py", "dictionary_basic_use.py",
            "dictionary_other_use.py", "dictionary_traversal.py",
            "dictionary_application.py", "iterating_dict_list.py",
            "del_keyword.py", "string_definition_traversal.py",
            "string_judgment.py", "string_find_replace.py",
            "string_split_connect.py", "string_statistical.py",
            "string_alignment.py", "format_string.py",
        ],
    },
    {
        "id": "stage06_oop_basic",
        "name": "面向对象基础",
        "description": "类和对象、self、__init__、__str__、__del__",
        "requires": ["stage03_function"],
        "files": [
            "01_class_object.py", "02_self.py", "03_add_attributes.py",
            "04_init.py", "05_str_del.py", "06_sweet_potato.py", "07_furniture.py",
        ],
    },
    {
        "id": "stage07_oop_advanced",
        "name": "面向对象高级",
        "description": "多态、类属性、classmethod/staticmethod、__slots__",
        "requires": ["stage06_oop_basic"],
        "files": [
            "01_polymorphism.py", "02_class_attribute.py",
            "03_classmethod_static.py", "04_slots.py",
        ],
    },
    {
        "id": "stage08_oop_inherit",
        "name": "继承",
        "description": "单继承、多继承、重写、super()、私有属性",
        "requires": ["stage06_oop_basic"],
        "files": [
            "01_basic_inherit.py", "02_single_inherit.py",
            "03_multi_inherit.py", "04_override.py", "05_call_parent.py",
            "06_multi_level.py", "07_super.py", "08_private.py",
        ],
    },
    {
        "id": "stage09_oop_encapsulation",
        "name": "封装",
        "description": "属性封装、对象组合、综合练习",
        "requires": ["stage06_oop_basic"],
        "files": [
            "01_person_run.py", "02_house_furniture.py", "03_soldier_gun.py",
        ],
    },
    {
        "id": "stage10_oop_application",
        "name": "面向对象应用",
        "description": "扑克牌游戏、工资结算系统",
        "requires": ["stage08_oop_inherit", "stage09_oop_encapsulation"],
        "files": ["01_poker_game.py", "02_salary_system.py"],
    },
    {
        "id": "stage11_card_manage",
        "name": "综合应用 — 名片管理系统",
        "description": "名片管理 CRUD 系统，综合运用函数和数据结构",
        "requires": ["stage03_function", "stage05_advanced_data_structures"],
        "files": ["cards_main.py", "cards_tools.py"],
    },
]


def get_stage(stage_id: str) -> Optional[Dict]:
    """根据 id 获取学习阶段"""
    for stage in STAGES:
        if stage["id"] == stage_id:
            return stage
    return None


def list_stages() -> List[tuple]:
    """列出所有学习阶段，返回 [(id, name), ...]"""
    return [(s["id"], s["name"]) for s in STAGES]


def get_ordered_stages() -> List[Dict]:
    """按学习依赖关系排序的阶段列表（拓扑排序）"""
    ordered: List[Dict] = []
    remaining = list(STAGES)
    placed_ids: set = set()

    while remaining:
        ready = [
            s for s in remaining
            if all(r in placed_ids for r in s.get("requires", []))
        ]
        if not ready:
            # 循环依赖或无依赖可满足，按原顺序追加
            ordered.extend(remaining)
            break
        for stage in ready:
            ordered.append(stage)
            placed_ids.add(stage["id"])
            remaining.remove(stage)

    return ordered
```

- [ ] **Step 4: 运行测试确认通过**

```bash
cd /Users/lile/Desktop/mycode/hello-python
python -m pytest tests/test_lessons.py -v
```

Expected: All tests PASS.

- [ ] **Step 5: 提交**

```bash
git add src/hello_python/lessons/index.py src/hello_python/lessons/__init__.py tests/test_lessons.py
git commit -m "feat: add lessons index with 11-stage learning path"
```

---

### Task 3: 编写 runner.py 代码运行器

**Files:**
- Create: `src/hello_python/runner.py`
- Test: `tests/test_runner.py`

- [ ] **Step 1: 编写 tests/test_runner.py**

Write `tests/test_runner.py`:

```python
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from hello_python.runner import run_stage, run_file


class TestRunFile:
    def test_run_simple_print(self, tmp_path):
        f = tmp_path / "test.py"
        f.write_text("print('hello')")
        output = run_file(str(f), timeout=5)
        assert "hello" in output

    def test_run_with_error(self, tmp_path):
        f = tmp_path / "test.py"
        f.write_text("raise ValueError('boom')")
        output = run_file(str(f), timeout=5)
        assert "Error" in output or "boom" in output

    def test_run_nonexistent_file(self):
        output = run_file("/nonexistent/path.py")
        assert "not found" in output.lower()


class TestRunStage:
    def test_run_stage01(self):
        output = run_stage("stage01_basic", timeout=5)
        assert "Stage: stage01_basic" in output
        assert "comment.py" in output
        assert "print.py" in output

    def test_run_invalid_stage(self):
        output = run_stage("nonexistent", timeout=5)
        assert "not found" in output.lower()
```

- [ ] **Step 2: 运行测试确认失败**

```bash
cd /Users/lile/Desktop/mycode/hello-python
python -m pytest tests/test_runner.py -v
```

Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: 编写 runner.py**

Write `src/hello_python/runner.py`:

```python
"""代码运行器 — 安全执行课程示例代码"""
import subprocess
import sys
from pathlib import Path
from typing import Optional

from hello_python.lessons.index import get_stage

LESSONS_DIR = Path(__file__).parent / "lessons"


def run_file(filepath: str, timeout: int = 10) -> str:
    """运行单个 Python 文件并返回输出"""
    path = Path(filepath)
    if not path.exists():
        return f"File not found: {filepath}"

    try:
        result = subprocess.run(
            [sys.executable, str(path)],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(path.parent),
        )
        output = result.stdout
        if result.stderr:
            output += "\n[stderr]\n" + result.stderr
        return output.strip() or "(no output)"
    except subprocess.TimeoutExpired:
        return f"Timeout: script exceeded {timeout}s"
    except Exception as e:
        return f"Error running {filepath}: {e}"


def run_stage(stage_id: str, timeout: int = 10) -> str:
    """运行指定学习阶段的所有代码文件"""
    stage = get_stage(stage_id)
    if stage is None:
        return f"Stage not found: {stage_id}"

    stage_dir = LESSONS_DIR / stage_id
    lines = [f"Stage: {stage_id} — {stage['name']}", "=" * 50]

    for filename in stage.get("files", []):
        filepath = stage_dir / filename
        lines.append(f"\n--- {filename} ---")
        lines.append(run_file(str(filepath), timeout=timeout))

    return "\n".join(lines)
```

- [ ] **Step 4: 运行测试确认通过**

```bash
cd /Users/lile/Desktop/mycode/hello-python
python -m pytest tests/test_runner.py -v
```

Expected: All tests PASS.

- [ ] **Step 5: 提交**

```bash
git add src/hello_python/runner.py tests/test_runner.py
git commit -m "feat: add lesson code runner with test coverage"
```

---

### Task 4: 编写 cli.py 命令行入口

**Files:**
- Create: `src/hello_python/cli.py`
- Modify: `pyproject.toml` (添加 console_scripts 入口点)

- [ ] **Step 1: 编写 cli.py**

Write `src/hello_python/cli.py`:

```python
"""hello-python CLI — 交互式学习入口"""
import argparse
import sys

from hello_python import __version__
from hello_python.lessons.index import list_stages, get_stage, get_ordered_stages
from hello_python.runner import run_stage


def cmd_list() -> None:
    """列出所有学习阶段"""
    print(f"hello-python v{__version__} — 学习路径\n")
    ordered = get_ordered_stages()
    for i, stage in enumerate(ordered, 1):
        requires = ""
        if stage.get("requires"):
            requires = f" (前置: {', '.join(stage['requires'])})"
        print(f"  {i:2d}. [{stage['id']}] {stage['name']}{requires}")


def cmd_show(stage_id: str) -> None:
    """显示某个阶段的详情"""
    stage = get_stage(stage_id)
    if stage is None:
        print(f"未找到阶段: {stage_id}")
        print(f"可用阶段: {', '.join(s[0] for s in list_stages())}")
        sys.exit(1)

    print(f"{stage['name']} ({stage['id']})")
    print(f"{'─' * 40}")
    print(f"描述: {stage['description']}")
    requires = stage.get("requires", [])
    if requires:
        print(f"前置阶段: {', '.join(requires)}")
    else:
        print("前置阶段: 无（可从本阶段开始）")
    print(f"\n代码文件 ({len(stage['files'])}):")
    for f in stage["files"]:
        print(f"  - {f}")


def cmd_run(stage_id: str) -> None:
    """运行指定阶段的代码"""
    stage = get_stage(stage_id)
    if stage is None:
        print(f"未找到阶段: {stage_id}")
        print(f"可用阶段: {', '.join(s[0] for s in list_stages())}")
        sys.exit(1)

    print(run_stage(stage_id))


def cmd_check() -> None:
    """检查学习环境"""
    print(f"hello-python v{__version__}")
    print(f"Python {sys.version}")
    print(f"平台: {sys.platform}")

    from pathlib import Path
    lessons_dir = Path(__file__).parent / "lessons"
    stage_count = len([d for d in lessons_dir.iterdir() if d.is_dir() and d.name.startswith("stage")])
    print(f"学习阶段: {stage_count} 个")

    try:
        import pytest
        print("pytest: 已安装 ✓")
    except ImportError:
        print("pytest: 未安装 ✗ (pip install pytest)")

    print("\n一切就绪，开始学习吧!")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="hello-python",
        description="Python 学习资源工具",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    sub = parser.add_subparsers(dest="command", help="可用命令")

    sub.add_parser("list", help="列出所有学习阶段")
    show_p = sub.add_parser("show", help="显示阶段详情")
    show_p.add_argument("stage", help="阶段 id，如 stage01_basic")
    run_p = sub.add_parser("run", help="运行阶段代码")
    run_p.add_argument("stage", help="阶段 id，如 stage01_basic")
    sub.add_parser("check", help="检查学习环境")

    args = parser.parse_args()

    if args.command == "list":
        cmd_list()
    elif args.command == "show":
        cmd_show(args.stage)
    elif args.command == "run":
        cmd_run(args.stage)
    elif args.command == "check":
        cmd_check()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: 更新 pyproject.toml 添加 CLI 入口点**

Edit `pyproject.toml` — 在 `[project]` 段末尾添加:

```toml
[project.scripts]
hello-python = "hello_python.cli:main"
```

- [ ] **Step 3: 手动验证 CLI**

```bash
cd /Users/lile/Desktop/mycode/hello-python
pip install -e . 2>/dev/null

# 测试各命令
hello-python --version
hello-python list
hello-python show stage01_basic
hello-python run stage01_basic
hello-python check
```

Expected: 所有命令正常输出。

- [ ] **Step 4: 提交**

```bash
git add src/hello_python/cli.py pyproject.toml
git commit -m "feat: add CLI for interactive learning (list/show/run/check)"
```

---

### Task 5: 精简 __init__.py 并更新 examples

**Files:**
- Modify: `src/hello_python/__init__.py`
- Modify: `examples/basic_usage.py`
- Modify: `docs/getting_started.md`

- [ ] **Step 1: 重写 src/hello_python/__init__.py**

Write `src/hello_python/__init__.py`:

```python
"""hello-python — Python 学习资源包"""
__version__ = "1.1.0"
__author__ = "CoderLiLe"
__license__ = "MIT"
```

- [ ] **Step 2: 重写 examples/basic_usage.py**

Write `examples/basic_usage.py`:

```python
#!/usr/bin/env python3
"""hello-python 使用示例 — 浏览和运行学习课程"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from hello_python import __version__
from hello_python.lessons.index import list_stages, get_stage, get_ordered_stages
from hello_python.runner import run_stage


def main() -> None:
    print(f"hello-python v{__version__} — 示例\n")

    # 列出学习路径
    print("学习路径:")
    for i, stage in enumerate(get_ordered_stages(), 1):
        print(f"  {i:2d}. {stage['name']} ({stage['id']})")

    # 查看第一个阶段
    stage = get_stage("stage01_basic")
    print(f"\n第一个阶段: {stage['name']}")
    print(f"描述: {stage['description']}")
    print(f"文件: {', '.join(stage['files'])}")

    # 运行第一个阶段
    print(f"\n运行 stage01_basic:")
    print(run_stage("stage01_basic"))


if __name__ == "__main__":
    main()
```

- [ ] **Step 3: 重写 docs/getting_started.md**

Write `docs/getting_started.md`:

```markdown
# 快速开始

## 安装

```bash
git clone https://github.com/CoderLiLe/hello-python.git
cd hello-python
pip install -e .
```

## 使用

### 命令行

```bash
# 查看学习路径
hello-python list

# 查看阶段详情
hello-python show stage01_basic

# 运行阶段代码
hello-python run stage01_basic

# 检查环境
hello-python check
```

### Python API

```python
from hello_python.lessons.index import list_stages, get_stage
from hello_python.runner import run_stage

# 列出所有阶段
for stage_id, name in list_stages():
    print(stage_id, name)

# 运行某个阶段
print(run_stage("stage02_cycle"))
```

## 学习路径

查看 `doc/` 目录获取详细的教程文档，配合 CLI 运行对应阶段的代码示例。

1. Python基础 → 2. 循环 → 3. 函数 → 4. 高级语法 → 5. 数据结构 → 6-11. 面向对象
```

- [ ] **Step 4: 提交**

```bash
git add src/hello_python/__init__.py examples/basic_usage.py docs/getting_started.md
git commit -m "refactor: simplify core package, update examples and docs"
```

---

### Task 6: 清理残留引用和删除无用文件

**Files:**
- Delete: `tests/test_basic.py`
- Delete: `optimize_project.py`
- Delete: `optimization_report_20260317_233438.md`
- Delete: `.github/workflows/release.yml`
- Modify: `Makefile`
- Modify: `.pre-commit-config.yaml`
- Modify: `.github/workflows/ci.yml`

- [ ] **Step 1: 删除无用文件和 untrack .DS_Store**

```bash
cd /Users/lile/Desktop/mycode/hello-python

# 删除无用文件
rm tests/test_basic.py
rm optimize_project.py
rm optimization_report_20260317_233438.md
rm .github/workflows/release.yml
rm -f reports/quality_report_*.json reports/quality_report_*.md

# Untrack .DS_Store（已在 .gitignore 中）
git rm --cached .DS_Store codes/.DS_Store 2>/dev/null || true
rm -f .DS_Store
```

- [ ] **Step 2: 更新 Makefile — 移除 java_code_inspector 路径**

Edit `Makefile` — 修改 lint 和 format 目标:

```makefile
# Makefile for hello-python project

.PHONY: help install test lint format clean

help:
	@echo "Available commands:"
	@echo "  make install    Install dependencies"
	@echo "  make test       Run tests"
	@echo "  make lint       Lint code"
	@echo "  make format     Format code"
	@echo "  make clean      Clean temp files"

install:
	pip install -e .
	pip install -r requirements.txt

test:
	pytest tests/ -v --cov=src --cov-report=html

lint:
	flake8 src/ tests/ --max-line-length=88 --exclude=codes/,doc/,docs/,examples/,scripts/
	mypy src/

format:
	black src/ tests/
	isort src/ tests/

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	rm -rf .coverage htmlcov
```

- [ ] **Step 3: 更新 .pre-commit-config.yaml — 移除 java_code_inspector 引用**

Edit `.pre-commit-config.yaml` — 修改 flake8 和 mypy 的 exclude:

```yaml
repos:
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

  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
        args: [--profile=black, --filter-files]

  - repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
      - id: flake8
        args: [--max-line-length=88, --exclude=doc/,docs/,examples/,scripts/]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
        exclude: "doc/|docs/|examples/|scripts/"
```

- [ ] **Step 4: 更新 .github/workflows/ci.yml**

Write `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

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
        pip install -e .
        pip install -r requirements.txt

    - name: Lint with flake8
      run: |
        flake8 src/ tests/ --count --select=E9,F63,F7,F82 --show-source --statistics

    - name: Test with pytest
      run: |
        pytest tests/ -v --cov=src --cov-report=xml
```

- [ ] **Step 5: 提交**

```bash
git add -A
git commit -m "chore: remove java_code_inspector references, clean up stale files"
```

---

### Task 7: 重写 README 和更新项目文档

**Files:**
- Modify: `README.md`
- Modify: `PROJECT_SUMMARY.md`
- Modify: `CHANGELOG.md`

- [ ] **Step 1: 重写 README.md**

Write `README.md`:

```markdown
# Hello Python

Python 学习资源 — 从入门到进阶的完整学习路径。

## 快速开始

```bash
git clone https://github.com/CoderLiLe/hello-python.git
cd hello-python
pip install -e .

# 查看学习路径
hello-python list

# 运行第一个示例
hello-python run stage01_basic
```

## 学习路径

| 阶段 | 内容 |
|------|------|
| stage01 | Python基础 — 注释、print |
| stage02 | 循环 — while/for、break/continue |
| stage03 | 函数 — 定义、参数、返回值、模块化 |
| stage04 | 高级语法 — 全局变量、递归、拆包 |
| stage05 | 数据结构 — 列表、元组、字典、字符串 |
| stage06 | 面向对象基础 — 类、对象、init、str |
| stage07 | 面向对象高级 — 多态、类属性、staticmethod |
| stage08 | 继承 — 单继承、多继承、super |
| stage09 | 封装 — 属性封装、对象组合 |
| stage10 | OOP应用 — 扑克牌、工资系统 |
| stage11 | 综合项目 — 名片管理系统 |

## 使用方式

### CLI

```bash
hello-python list              # 列出所有阶段
hello-python show stage03      # 查看阶段详情
hello-python run stage01       # 运行阶段代码
hello-python check             # 检查环境
```

### Python API

```python
from hello_python.lessons.index import get_stage, get_ordered_stages
from hello_python.runner import run_stage

for stage in get_ordered_stages():
    print(stage["name"])
```

### 教程文档

`doc/` 目录包含每个阶段的中文教程，配合代码示例学习效果最佳。

## 项目结构

```
hello-python/
├── src/hello_python/
│   ├── cli.py              # CLI 入口
│   ├── runner.py           # 代码运行器
│   └── lessons/            # 11 个学习阶段
├── doc/                    # 中文教程文档
├── tests/                  # 测试
├── examples/               # 使用示例
└── scripts/                # 工具脚本
```

## 开发

```bash
pip install -r requirements.txt
make test    # 运行测试
make lint    # 代码检查
make format  # 代码格式化
```

## 许可

MIT
```

- [ ] **Step 2: 更新 PROJECT_SUMMARY.md**

Write `PROJECT_SUMMARY.md`:

```markdown
# hello-python 项目总结

## 项目定位

hello-python 是一个 Python 学习资源仓库，包含从入门到进阶的完整学习路径。

## 内容

- **11 个学习阶段**: 从 Python 基础到面向对象编程
- **60+ 代码示例**: 每个阶段包含可运行的示例代码
- **中文教程文档**: doc/ 目录下各阶段配套教程
- **CLI 工具**: 交互式浏览和运行学习内容

## 学习路径

1. Python基础 → 2. 循环 → 3. 函数 → 4. 高级语法
5. 数据结构 → 6-11. 面向对象（基础/高级/继承/封装/应用/综合）

## 技术栈

- Python 3.9+
- pytest 测试框架
- black/flake8/isort/mypy 代码质量
- GitHub Actions CI

## 版本

当前版本: 1.1.0 (2026-06-10)
```

- [ ] **Step 3: 更新 CHANGELOG.md**

Write `CHANGELOG.md`:

```markdown
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
```

- [ ] **Step 4: 提交**

```bash
git add README.md PROJECT_SUMMARY.md CHANGELOG.md
git commit -m "docs: rewrite README and project docs for learning resource focus"
```

---

### Task 8: 最终验证和收尾

- [ ] **Step 1: 运行完整测试套件**

```bash
cd /Users/lile/Desktop/mycode/hello-python
python -m pytest tests/ -v
```

Expected: All tests PASS.

- [ ] **Step 2: 验证 CLI 安装和运行**

```bash
pip install -e .
hello-python --version
hello-python list
hello-python show stage01_basic
hello-python run stage01_basic
hello-python check
```

Expected: 所有命令正常输出。

- [ ] **Step 3: 确认无 java_code_inspector 残留**

```bash
cd /Users/lile/Desktop/mycode/hello-python
grep -r "java_code_inspector" --include="*.py" --include="*.md" --include="*.yml" --include="*.yaml" --include="Makefile" . 2>/dev/null || echo "No references found."
```

Expected: "No references found."

- [ ] **Step 4: 检查 .DS_Store 不再被跟踪**

```bash
cd /Users/lile/Desktop/mycode/hello-python
git ls-files | grep DS_Store || echo "No DS_Store tracked."
```

Expected: "No DS_Store tracked."

- [ ] **Step 5: 最终提交**

```bash
git add -A
git status
```

确认只有预期的变更，然后:

```bash
git commit -m "chore: final cleanup and verification"
```
