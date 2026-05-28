import pytest
from hello_python import (
    greet,
    calculate_fibonacci,
    analyze_text,
    PythonTutorial,
    CodeInspector,
)


class TestGreet:
    def test_default_greeting(self):
        result = greet()
        assert result == "Hello, Python Developer! Welcome to hello-python!"

    def test_custom_name(self):
        result = greet("Alice")
        assert result == "Hello, Alice! Welcome to hello-python!"


class TestCalculateFibonacci:
    def test_first_five(self):
        assert calculate_fibonacci(5) == [0, 1, 1, 2, 3]

    def test_first_one(self):
        assert calculate_fibonacci(1) == [0]

    def test_first_two(self):
        assert calculate_fibonacci(2) == [0, 1]

    def test_invalid_zero(self):
        with pytest.raises(ValueError, match="n必须大于0"):
            calculate_fibonacci(0)

    def test_invalid_negative(self):
        with pytest.raises(ValueError, match="n必须大于0"):
            calculate_fibonacci(-1)


class TestAnalyzeText:
    def test_basic_text(self):
        result = analyze_text("Hello Python")
        assert result["char_count"] == 12
        assert result["word_count"] == 2
        assert result["line_count"] == 1
        assert result["avg_word_length"] == 5.5
        assert result["unique_words"] == 2

    def test_multiline_text(self):
        result = analyze_text("line1\nline2\nline3")
        assert result["line_count"] == 3
        assert result["word_count"] == 3

    def test_empty_text(self):
        result = analyze_text("")
        assert result["char_count"] == 0
        assert result["word_count"] == 0
        assert result["line_count"] == 0
        assert result["avg_word_length"] == 0
        assert result["unique_words"] == 0

    def test_duplicate_words(self):
        result = analyze_text("hello hello hello")
        assert result["unique_words"] == 1


class TestPythonTutorial:
    def test_default_level(self):
        tutorial = PythonTutorial()
        assert tutorial.level == "beginner"

    def test_beginner_topics(self):
        tutorial = PythonTutorial("beginner")
        topics = tutorial.get_topics()
        assert "变量和数据类型" in topics
        assert tutorial.get_topic_count() == 6

    def test_intermediate_topics(self):
        tutorial = PythonTutorial("intermediate")
        topics = tutorial.get_topics()
        assert "面向对象编程" in topics
        assert tutorial.get_topic_count() == 6

    def test_advanced_topics(self):
        tutorial = PythonTutorial("advanced")
        topics = tutorial.get_topics()
        assert "并发编程" in topics

    def test_invalid_level_fallback(self):
        tutorial = PythonTutorial("unknown")
        assert tutorial.level == "unknown"
        assert len(tutorial.get_topics()) == 6

    def test_has_topic(self):
        tutorial = PythonTutorial("beginner")
        assert tutorial.has_topic("变量和数据类型")
        assert not tutorial.has_topic("不存在的话题")


class TestCodeInspector:
    def test_empty_code_warning(self):
        inspector = CodeInspector()
        issues = inspector.inspect("")
        assert len(issues) == 1
        assert issues[0]["type"] == "warning"

    def test_long_line_detection(self):
        inspector = CodeInspector()
        long_line = "x" * 150
        issues = inspector.inspect(long_line)
        style_issues = [i for i in issues if i["type"] == "style"]
        assert len(style_issues) >= 1

    def test_trailing_whitespace(self):
        inspector = CodeInspector()
        code = "print('hello')   \n"
        issues = inspector.inspect(code)
        style_issues = [i for i in issues if i["type"] == "style"]
        assert len(style_issues) >= 1

    def test_complexity_long_code(self):
        inspector = CodeInspector()
        code = "\n".join(f"print({i})" for i in range(60))
        issues = inspector.inspect(code)
        complexity_issues = [i for i in issues if i["type"] == "complexity"]
        assert len(complexity_issues) == 1

    def test_get_issue_count(self):
        inspector = CodeInspector()
        inspector.inspect("")
        assert inspector.get_issue_count() >= 1

    def test_get_issues_by_severity(self):
        inspector = CodeInspector()
        inspector.inspect("")
        low_issues = inspector.get_issues_by_severity("low")
        assert len(low_issues) >= 1
