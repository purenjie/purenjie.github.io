# 博客封面图生成器使用指南

## 概述

博客封面图生成器是一个基于AI的自动化工具，能够根据博客文章内容智能生成适合的封面图片。该工具集成了火山引擎豆包API，通过情绪分析和视觉转化技术，为每篇文章创建独特的封面图。

## 功能演进

### 版本对比

#### 初始版本 (v1.0)
- **Prompt系统**: 简单的技术描述生成
- **风格定位**: 科技感、现代感
- **内容提取**: 基于具体文本内容的描述
- **配置方式**: 环境变量管理API密钥

#### 当前版本 (v2.0)
- **Prompt系统**: 情绪叙事与视觉转化专家角色
- **风格定位**: 多艺术风格自动选择（莫奈风、像素风、伦勃朗、巴洛克）
- **内容提取**: 情绪流动和氛围捕捉
- **配置方式**: 硬编码API密钥（开发阶段）

### 核心改进

#### 1. 情绪感知能力
- 从文本内容中捕捉情绪流动
- 识别文章的整体氛围和基调
- 将抽象情绪转化为具象画面

#### 2. 艺术风格多样化
- **莫奈风**: 印象派风格，适合自然、生活类文章
- **像素风**: 复古游戏风格，适合技术、游戏类文章
- **伦勃朗**: 古典油画风格，适合深度思考类文章
- **巴洛克**: 华丽装饰风格，适合艺术、文化类文章

#### 3. 叙事氛围营造
- 构建具有故事感的视觉描述
- 保留文章的象征性元素
- 增强封面图的表达力和吸引力

## 技术架构

### API集成
- **文本生成**: 火山引擎豆包1.5 Pro 32K模型
- **图像生成**: 火山引擎豆包Seedream 3.0 T2I模型
- **图像尺寸**: 1024x1024像素
- **水印**: 自动添加水印保护

### 工作流程
1. **文章读取**: 解析Markdown文件，提取正文内容
2. **情绪分析**: 使用AI分析文章的情绪流和主题
3. **描述生成**: 生成适合AI绘图的视觉描述
4. **图像生成**: 调用文生图API创建封面图
5. **文件保存**: 自动下载并保存到文章目录

## 配置说明

### 当前配置
```python
# API配置常量
ARK_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
TEXT_MODEL = "doubao-1-5-pro-32k-250115"
IMAGE_MODEL = "doubao-seedream-3-0-t2i-250415"
IMAGE_SIZE = "1024x1024"

# API密钥
ARK_API_KEY = "xxx"
```

### 环境变量配置（推荐）
```bash
# 设置环境变量
export ARK_API_KEY=your_api_key

# 在脚本中使用
ARK_API_KEY = os.getenv("ARK_API_KEY")
if not ARK_API_KEY:
    print("错误：未找到环境变量 ARK_API_KEY")
    sys.exit(1)
```

## 使用方法

### 1. 基础使用

#### 安装依赖
```bash
pip install requests
```

#### 运行脚本
```bash
python scripts/generate_cover_image.py "文章标题"
```

#### 示例
```bash
# 为"astro博客迁移"文章生成封面图
python scripts/generate_cover_image.py "astro博客迁移"
```

### 2. 高级配置

#### 自定义图像尺寸
```python
# 修改IMAGE_SIZE常量
IMAGE_SIZE = "1920x1080"  # 宽屏格式
IMAGE_SIZE = "800x600"     # 小尺寸
```

#### 调整生成参数
```python
# 在generate_image函数中修改
data = {
    "model": IMAGE_MODEL,
    "prompt": description,
    "response_format": "url",
    "size": IMAGE_SIZE,
    "guidance_scale": 3.0,  # 增加创意性
    "watermark": False      # 移除水印
}
```

## 最佳实践

### 1. 文章内容优化
- **内容长度**: 建议文章内容不少于100字，确保有足够信息供AI分析
- **主题明确**: 文章主题越明确，生成的封面图越贴合
- **情绪表达**: 在文章中适当表达情感，有助于AI捕捉情绪流

### 2. 封面图使用
- **文件命名**: 生成的封面图自动命名为`cover.jpg`
- **Frontmatter配置**: 在文章中添加封面图引用
```yaml
---
title: '文章标题'
heroImage: { src: './cover.jpg', color: '#9698C1' }
---
```

### 3. 风格选择策略
- **技术文章**: 像素风或现代科技风格
- **生活随笔**: 莫奈风或温暖色调
- **深度思考**: 伦勃朗或古典风格
- **艺术文化**: 巴洛克或装饰风格

## 故障排除

### 1. 常见问题

#### API调用失败
```bash
错误：文本API调用失败: 401 Unauthorized
解决：检查API密钥是否正确，确认账户余额充足
```

#### 文章未找到
```bash
错误：未找到文章: 文章标题
解决：确认文章标题正确，检查目录结构是否符合规范
```

#### 图片生成失败
```bash
错误：图像API调用失败: 400 Bad Request
解决：检查prompt内容是否合规，调整描述长度和内容
```

### 2. 性能优化
- **内容截取**: 脚本自动截取前1500字符，避免超出token限制
- **超时设置**: 文本生成30秒，图像生成60秒
- **错误重试**: 建议在网络不稳定时增加重试机制

### 3. 调试技巧
```python
# 启用详细日志
print(f"API响应: {result}")
print(f"生成描述: {description}")
print(f"图片URL: {image_url}")
```

## 扩展和自定义

### 1. 添加新的艺术风格
在`system_prompt`中添加新的风格描述：
```python
system_prompt = """
- 风格：根据内容，自动选择莫奈风、像素风、伦勃朗、巴洛克风格、新风格
- 新风格：描述新风格的特点和适用场景
"""
```

### 2. 集成其他AI模型
```python
# 修改模型配置
TEXT_MODEL = "your-text-model"
IMAGE_MODEL = "your-image-model"
```

### 3. 批量处理
```bash
# 创建批量处理脚本
for article in articles; do
    python scripts/generate_cover_image.py "$article"
done
```

## 安全注意事项

### 1. API密钥管理
- **开发环境**: 可以使用硬编码密钥进行测试
- **生产环境**: 必须使用环境变量或配置文件
- **密钥轮换**: 定期更换API密钥，避免泄露

### 2. 内容安全
- **内容审核**: 确保生成的内容符合平台规范
- **版权保护**: 生成的图片可能包含水印，注意使用权限
- **隐私保护**: 避免在prompt中包含敏感信息

## 参考资源

- [火山引擎豆包API文档](https://ark.cn-beijing.volces.com/docs)
- [AI文生图最佳实践](https://docs.volcengine.com/ark/docs)
- [Python requests库文档](https://requests.readthedocs.io/)
- [Markdown文件处理](https://python-markdown.github.io/)

## 更新日志

### v2.0 (当前版本)
- ✨ 新增情绪叙事与视觉转化专家角色
- 🎨 支持多种艺术风格自动选择
- 🔄 重构Prompt系统，增强情绪感知能力
- 📝 优化配置管理，支持硬编码和环境变量
- 🚀 提升图像生成质量和创意性

### v1.0 (初始版本)
- 🎯 基础的文章内容读取功能
- 🤖 简单的AI绘图描述生成
- 🖼️ 基础的文生图功能
- ⚙️ 环境变量配置管理
- 📁 自动文件保存和路径管理
