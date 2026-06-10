# 快速开始

## 安装

```bash
git clone https://github.com/CoderLiLe/hello-python.git
cd hello-python
pip install -e .
```

## 使用

### 命令行

```bash
# 查看学习路径
hello-python list

# 查看阶段详情
hello-python show stage01_basic

# 运行阶段代码
hello-python run stage01_basic

# 检查环境
hello-python check
```

### Python API

```python
from hello_python.lessons.index import list_stages, get_stage
from hello_python.runner import run_stage

# 列出所有阶段
for stage_id, name in list_stages():
    print(stage_id, name)

# 运行某个阶段
print(run_stage("stage02_cycle"))
```

## 学习路径

查看 `doc/` 目录获取详细的教程文档，配合 CLI 运行对应阶段的代码示例。

1. Python基础 → 2. 循环 → 3. 函数 → 4. 高级语法 → 5. 数据结构 → 6-11. 面向对象
