# Hello Python 🐍

![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Last Updated](https://img.shields.io/badge/updated-2026-03-17-lightgrey)

Python学习与代码检查工具集 - 包含Python基础教程和Java代码检查工具

## ✨ 特性

### Python学习教程
- 📚 完整的Python基础教程
- 💻 丰富的代码示例
- 🎯 从入门到进阶的学习路径
- 📝 详细的文档说明

### Java代码检查工具
- 🔍 静态代码分析
- ✅ 代码质量检查
- 🛠️ 自动修复功能
- 📊 多种报告格式

## 🚀 快速开始

### 安装
```bash
# 克隆项目
git clone https://github.com/CoderLiLe/hello-python.git
cd hello-python

# 安装依赖
pip install -r requirements.txt
```

### 使用Python教程
```bash
# 查看教程文档
cd doc/
# 打开对应的markdown文件学习
```

### 使用Java代码检查工具
```bash
cd java_code_inspector/
python src/java_inspector.py --help
```

## 📁 项目结构

```
hello-python/
├── src/                    # 源代码
├── tests/                  # 测试代码
├── docs/                   # 文档
├── examples/               # 示例代码
├── scripts/                # 脚本工具
├── config/                 # 配置文件
├── codes/                  # Python代码示例
├── doc/                    # 学习文档
├── java_code_inspector/    # Java代码检查工具
├── pyproject.toml          # 项目配置
├── requirements.txt        # 依赖列表
├── Makefile               # 构建命令
└── README.md              # 项目说明
```

## 🔧 开发

### 代码质量
```bash
# 安装开发依赖
pip install -r requirements.txt

# 运行测试
make test

# 代码检查
make lint

# 代码格式化
make format
```

### 预提交钩子
```bash
# 安装pre-commit
pip install pre-commit
pre-commit install

# 手动运行所有钩子
pre-commit run --all-files
```

## 🤝 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

## 📄 许可证

本项目基于 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 联系

- GitHub: [@CoderLiLe](https://github.com/CoderLiLe)
- 项目地址: https://github.com/CoderLiLe/hello-python

---

# Python

## 笔记目录
* [初识Python](doc/introduction.md)
* [安装Python环境](doc/installation.md)
* [编辑器的选择](doc/editor.md)
* [第一行代码](doc/first_line.md)
* [变量](doc/variable.md)
* [判断语句](doc/judgment_statement.md)
* [循环](doc/cycle.md)
* [函数](doc/function.md)
* [列表](doc/list.md)
* [元组字典字符串](doc/tuple_dict_str.md)
* [综合应用--名片管理系统](doc/card_management.md)
