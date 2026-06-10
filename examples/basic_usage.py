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
