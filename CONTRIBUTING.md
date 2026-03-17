# 贡献指南

感谢您考虑为hello-python项目做出贡献！

## 🚀 开始贡献

### 报告问题
- 使用GitHub Issues报告bug或提出功能建议
- 在创建issue前，请先搜索是否已有类似问题
- 提供清晰的问题描述、复现步骤和期望结果

### 提交代码
1. Fork本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开Pull Request

## 📝 代码规范

### Python代码
- 遵循PEP 8规范
- 使用类型提示
- 编写文档字符串
- 保持函数简洁（不超过50行）

### 提交信息
使用约定式提交：
- `feat:` 新功能
- `fix:` bug修复
- `docs:` 文档更新
- `style:` 代码格式
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 构建过程或辅助工具

### 测试要求
- 新功能需要包含测试
- 保持测试覆盖率
- 测试应该独立且可重复

## 🔧 开发环境

### 设置环境
```bash
# 克隆仓库
git clone https://github.com/CoderLiLe/hello-python.git
cd hello-python

# 安装依赖
pip install -r requirements.txt
pip install -e .

# 安装开发工具
pip install black flake8 mypy pytest pre-commit
pre-commit install
```

### 运行测试
```bash
# 运行所有测试
make test

# 运行特定测试
pytest tests/test_specific.py -v

# 生成覆盖率报告
pytest --cov=src --cov-report=html
```

## 🎯 项目结构

了解项目结构有助于更好地贡献：

```
hello-python/
├── src/           # 源代码
├── tests/         # 测试代码
├── docs/          # 文档
├── examples/      # 示例代码
├── scripts/       # 脚本工具
└── config/        # 配置文件
```

## 🤝 行为准则

请遵守我们的行为准则：
- 尊重所有贡献者
- 建设性讨论
- 帮助他人学习
- 保持专业态度

## 📞 需要帮助？

- 查看现有文档
- 在GitHub Discussions中提问
- 联系维护者

感谢您的贡献！🎉
