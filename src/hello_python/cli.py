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
