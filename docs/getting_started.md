# 快速开始指南

本指南将帮助您快速开始使用hello-python项目。

## 🚀 安装

### 从GitHub克隆
```bash
# 克隆项目
git clone https://github.com/CoderLiLe/hello-python.git
cd hello-python

# 安装依赖
pip install -r requirements.txt
```

### 从PyPI安装（未来版本）
```bash
pip install hello-python
```

## 📚 基本使用

### 导入模块
```python
from hello_python import greet, calculate_fibonacci, analyze_text

# 打招呼
print(greet("开发者"))

# 计算斐波那契数列
fib = calculate_fibonacci(10)
print(f"前10个斐波那契数: {fib}")

# 分析文本
text = "Hello Python World!"
stats = analyze_text(text)
print(f"文本统计: {stats}")
```

### 使用Python教程
```python
from hello_python import PythonTutorial

# 创建初学者教程
tutorial = PythonTutorial("beginner")
print(f"初学者主题: {tutorial.get_topics()}")
print(f"主题数量: {tutorial.get_topic_count()}")
```

### 使用代码检查器
```python
from hello_python import CodeInspector

# 创建代码检查器
inspector = CodeInspector("python")

# 检查代码
code = '''
def example():
    x = 1
    return x
'''

issues = inspector.inspect(code)
print(f"发现问题: {len(issues)}个")
for issue in issues:
    print(f"- {issue['message']}")
```

## 💻 命令行使用

### 运行示例
```bash
# 运行基础示例
python examples/basic_usage.py

# 运行测试
python tests/test_basic.py

# 使用pytest运行测试
pytest tests/ -v
```

### 使用Makefile
```bash
# 安装依赖
make install

# 运行测试
make test

# 代码检查
make lint

# 代码格式化
make format

# 清理临时文件
make clean
```

## 🔧 开发环境设置

### 1. 创建虚拟环境（推荐）
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 安装开发工具
```bash
# 安装预提交钩子
pip install pre-commit
pre-commit install

# 安装测试工具
pip install pytest pytest-cov

# 安装代码质量工具
pip install black flake8 mypy
```

### 3. 配置编辑器
推荐使用VS Code，安装以下扩展：
- Python
- Pylance
- Black Formatter
- flake8

## 📁 项目结构

了解项目结构有助于更好地使用：

```
hello-python/
├── src/                    # 源代码目录
│   └── hello_python/      # 核心模块
├── tests/                  # 测试代码
├── examples/               # 使用示例
├── docs/                   # 文档
├── scripts/                # 工具脚本
├── config/                 # 配置文件
├── codes/                  # Python代码示例（学习用）
├── doc/                    # 学习文档（教程）
├── java_code_inspector/    # Java代码检查工具
├── pyproject.toml         # 项目配置
├── requirements.txt       # 依赖列表
├── Makefile              # 构建命令
└── README.md             # 项目说明
```

## 🎯 学习路径

### 初学者
1. 查看 `doc/` 目录中的教程
2. 运行 `codes/` 目录中的示例
3. 尝试修改示例代码

### 中级开发者
1. 阅读 `src/` 目录中的源代码
2. 查看 `tests/` 目录中的测试用例
3. 尝试添加新功能

### 高级开发者
1. 研究设计模式和架构
2. 优化性能
3. 贡献代码

## 🔍 代码检查工具

项目包含Java代码检查工具：

```bash
cd java_code_inspector/

# 查看帮助
python src/java_inspector.py --help

# 检查Java文件
python src/java_inspector.py path/to/java/file.java

# 批量检查
python src/java_inspector.py --directory path/to/java/project
```

## 🤝 获取帮助

### 查看文档
- `docs/` 目录包含详细文档
- `README.md` 项目总览
- `CONTRIBUTING.md` 贡献指南

### 运行帮助命令
```bash
# 查看模块帮助
python -c "import hello_python; help(hello_python)"

# 查看函数帮助
python -c "from hello_python import greet; help(greet)"
```

### 遇到问题？
1. 查看 `CHANGELOG.md` 了解更新
2. 检查GitHub Issues
3. 在GitHub Discussions提问

## 🚀 下一步

### 学习更多
- 查看 `examples/` 目录中的高级示例
- 阅读源代码了解实现细节
- 尝试修改和扩展功能

### 贡献代码
- 参考 `CONTRIBUTING.md`
- 提交Pull Request
- 报告问题和建议

### 分享经验
- 写博客或教程
- 在社交媒体分享
- 帮助其他开发者

---

祝您使用愉快！🎉

如果有任何问题或建议，请随时联系我们。