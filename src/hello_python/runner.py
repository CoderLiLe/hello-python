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
