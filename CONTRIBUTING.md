# 贡献指南

感谢您对 ProTox3-Automation 项目的关注！我们欢迎所有形式的贡献。

## 如何贡献

### 报告问题

如果您发现了bug或有功能建议，请：

1. 检查 [Issues](https://github.com/YOUR_USERNAME/ProTox3-Automation/issues) 是否已有相同问题
2. 如果没有，创建一个新的 Issue
3. 清楚地描述问题或建议
4. 如果是bug，请提供复现步骤和环境信息

### 提交代码

1. **Fork 仓库**
   ```bash
   # 点击GitHub页面右上角的 Fork 按钮
   ```

2. **克隆您的Fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/ProTox3-Automation.git
   cd ProTox3-Automation
   ```

3. **创建特性分支**
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **进行更改**
   - 编写清晰的代码
   - 添加必要的注释
   - 遵循现有的代码风格

5. **测试您的更改**
   ```bash
   # 运行测试（如果有）
   pytest tests/
   ```

6. **提交更改**
   ```bash
   git add .
   git commit -m "Add: 简短描述您的更改"
   ```

7. **推送到您的Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

8. **创建 Pull Request**
   - 访问您的Fork页面
   - 点击 "New Pull Request"
   - 填写PR描述
   - 等待审核

## 代码规范

### Python代码风格

- 遵循 PEP 8 规范
- 使用4个空格缩进
- 函数和变量使用小写+下划线命名
- 类名使用驼峰命名

### 提交信息格式

```
类型: 简短描述

详细描述（可选）

相关Issue: #123
```

**类型**:
- `Add`: 新功能
- `Fix`: 修复bug
- `Update`: 更新功能
- `Docs`: 文档更新
- `Style`: 代码格式调整
- `Refactor`: 代码重构
- `Test`: 测试相关
- `Chore`: 构建/工具相关

## 开发环境设置

```bash
# 安装开发依赖
pip install -r requirements-dev.txt

# 安装pre-commit钩子
pre-commit install

# 运行代码格式化
black src/

# 运行代码检查
flake8 src/
```

## 测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_smiles.py

# 查看覆盖率
pytest --cov=src tests/
```

## 文档

- 更新代码时，请同步更新相关文档
- 新功能需要添加使用示例
- 复杂功能需要添加详细说明

## 行为准则

- 尊重所有贡献者
- 保持友好和专业
- 接受建设性批评
- 关注项目的最佳利益

## 问题？

如有任何问题，请：
- 查看 [文档](docs/)
- 在 [Discussions](https://github.com/YOUR_USERNAME/ProTox3-Automation/discussions) 提问
- 联系维护者

感谢您的贡献！🎉
