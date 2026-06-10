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
