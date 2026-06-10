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
