# 动态语言统计设置指南

本系统可以自动读取你的所有GitHub仓库（包括私有仓库）并生成动态的语言统计SVG图表。

## 🚀 快速开始

### 1. 获取GitHub Personal Access Token

1. 访问 [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
2. 点击 "Generate new token (classic)"
3. 设置token名称，如 "Language Stats Generator"
4. 选择权限：
   - ✅ `repo` - 访问私有仓库
   - ✅ `read:user` - 读取用户信息
5. 点击 "Generate token" 并**立即复制保存**（只显示一次）

### 2. 本地配置

1. 复制配置文件：
   ```bash
   copy .env.example .env
   ```

2. 编辑 `.env` 文件，填入你的信息：
   ```env
   GITHUB_TOKEN=ghp_your_token_here
   GITHUB_USERNAME=YourUsername
   OUTPUT_PATH=assets/lang-stats-dynamic.svg
   ```

3. 安装Python依赖：
   ```bash
   pip install -r requirements.txt
   ```

### 3. 生成语言统计

#### 方法一：使用批处理脚本（Windows）
```bash
.\update_lang_stats.bat
```

#### 方法二：直接运行Python脚本
```bash
python generate_lang_stats.py
```

## 🤖 自动化更新

### GitHub Actions 自动更新

系统已配置GitHub Actions工作流，会：
- 每天自动更新语言统计
- 在代码推送时触发更新
- 支持手动触发更新

**无需额外配置**，GitHub Actions会自动使用仓库的GITHUB_TOKEN。

### 手动触发GitHub Actions

1. 进入你的GitHub仓库
2. 点击 "Actions" 标签
3. 选择 "Update Language Statistics" 工作流
4. 点击 "Run workflow"

## 📊 功能特性

### ✨ 动态数据源
- 📈 实时读取所有仓库语言数据
- 🔒 支持私有仓库统计
- 🎯 智能排除fork仓库（可配置）
- 📊 按字节数精确计算占比

### 🎨 视觉效果
- 🌈 每种语言使用官方配色
- ✨ 呼吸灯动画效果
- 📱 响应式SVG设计
- 🎭 渐变填充动画

### ⚡ 性能优化
- 🚀 智能API请求限制
- 💾 本地SVG生成，无外部依赖
- 🔄 增量更新机制

## 🛠️ 高级配置

### 自定义语言颜色

编辑 `generate_lang_stats.py` 中的 `language_colors` 字典：

```python
language_colors = {
    'Python': ('#3776ab', '#ffd43b'),
    'JavaScript': ('#f7df1e', '#323330'),
    # 添加更多语言...
}
```

### 调整显示语言数量

修改 `get_top_languages()` 方法的 `limit` 参数：

```python
def get_top_languages(self, limit: int = 8):  # 显示前8种语言
```

### 排除特定仓库

在 `get_all_repositories()` 方法中添加过滤逻辑：

```python
# 排除fork仓库
if not repo['fork']:
    repos.extend(page_repos)
```

## 🔧 故障排除

### 常见问题

**Q: 提示"Error: 请设置GITHUB_TOKEN环境变量"**
A: 检查 `.env` 文件是否存在且格式正确

**Q: API请求失败**
A: 检查token权限，确保包含 `repo` 权限

**Q: 生成的SVG为空**
A: 检查仓库是否包含代码文件，或调整语言过滤设置

**Q: GitHub Actions失败**
A: 检查仓库是否启用了Actions，确保有推送权限

### 调试模式

在脚本中添加调试输出：

```python
# 在main()函数开头添加
print(f"Token: {token[:10]}...")
print(f"Username: {username}")
```

## 📝 更新日志

- **v1.0.0** - 初始版本，支持基本语言统计
- **v1.1.0** - 添加呼吸灯效果和渐变动画
- **v1.2.0** - 支持GitHub Actions自动更新
- **v1.3.0** - 优化API请求和错误处理

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 📄 许可证

MIT License - 详见 LICENSE 文件