import pytest
from pathlib import Path

from hello_python.lessons.index import STAGES, get_stage, list_stages, get_ordered_stages

LESSONS_DIR = Path(__file__).parent.parent / "src" / "hello_python" / "lessons"


class TestIndex:
    def test_stages_is_list(self):
        assert isinstance(STAGES, list)
        assert len(STAGES) == 11

    def test_each_stage_has_required_fields(self):
        for stage in STAGES:
            assert "id" in stage
            assert "name" in stage
            assert "description" in stage
            assert "requires" in stage
            assert "files" in stage

    def test_stage_ids_are_unique(self):
        ids = [s["id"] for s in STAGES]
        assert len(ids) == len(set(ids))

    def test_requires_refer_to_existing_stages(self):
        all_ids = {s["id"] for s in STAGES}
        for stage in STAGES:
            for req in stage.get("requires", []):
                assert req in all_ids, f"{stage['id']} requires unknown stage '{req}'"

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
        ids = [s["id"] for s in ordered]
        assert ids[0] == "stage01_basic"
        assert ids.index("stage08_oop_inherit") < ids.index("stage10_oop_application")
        assert ids.index("stage09_oop_encapsulation") < ids.index("stage10_oop_application")

    def test_all_files_exist(self):
        """验证索引中引用的所有文件都存在"""
        for stage in STAGES:
            stage_dir = LESSONS_DIR / stage["id"]
            assert stage_dir.is_dir(), f"Directory missing: {stage['id']}"
            for filename in stage["files"]:
                filepath = stage_dir / filename
                assert filepath.is_file(), f"File missing: {stage['id']}/{filename}"


class TestCompileAll:
    """验证所有课程代码无语法错误"""

    @pytest.mark.parametrize("stage", STAGES)
    def test_stage_files_compile(self, stage):
        for filename in stage["files"]:
            filepath = LESSONS_DIR / stage["id"] / filename
            with open(filepath, "r", encoding="utf-8") as f:
                source = f.read()
            compile(source, str(filepath), "exec")
