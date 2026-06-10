import pytest
from pathlib import Path

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
