---
title: AI 眼中的我？
publishDate: 2025-10-31
description: '用 AI 分析我的博客，看看我是什么货色'
tags:
  - 博客
  - AI

heroImage:
  { src: 'https://pub-6bd5d0c20d254a3e9d8dea968e62938c.r2.dev/2025/10/AI%E8%BE%85%E5%8A%A9%E5%8D%9A%E5%AE%A2%E5%88%86%E6%9E%90%20(1)_rbpa4iigue', inferSize: true, color: '#9698C1'  }
language: 'Chinese'
---

前段时间突发奇想，能不能让 AI 分析我写的博客内容，给出一些有趣的角度和结果。

虽然自己是「年更博主」，但是几年积攒起来，也写了十几二十篇，虽然模型的上下文能读，但是总觉得有点混乱。最开始的一版，有点倾向于传统的分析，让 cursor 一顿写，也只是基于之前的一些方法，分词统计、主题分析、情感分析。总觉得有点太过老套，不是自己想要的。后来，又重新开始写，搞出了下面的一套。虽然也非常简单，但是也算是初步满意，等到后面有新的想法，再来迭代更新。

下面是太长不用看的 AI 内容，用来后面的优化，以及避免自己忘了怎么用……

有些担忧，如果连博客的文章都要 AI 来写，我的意义是什么呢？

---

## Quick Start

想快速上手这个系统？跟着下面的步骤走：

### 1. 环境准备

```bash
# 确保 Python 版本
python --version  # 需要 3.9+

# 安装依赖
pip install -r scripts/requirements.txt
```

`requirements.txt` 内容：

```txt
pydantic>=2.0.0
requests>=2.28.0
pyyaml>=6.0
```

### 2. 配置 API Key

```bash
# 方式 1: 环境变量（推荐）
export API_KEY="your_deepseek_api_key"

# 方式 2: 写入 .env 文件
echo "API_KEY=your_deepseek_api_key" > .env
```

> 💡 **获取 API Key**: 访问 [DeepSeek 平台](https://platform.deepseek.com/)注册并获取

### 3. 首次运行（全量分析）

```bash
# 基础运行
python scripts/ai_analysis/run.py

# 推荐：带详细日志
python scripts/ai_analysis/run.py --verbose

# 或者作为模块运行
python -m scripts.ai_analysis.run --verbose
```

运行后会看到类似输出：

```
19:16:17 [INFO] Found 36 articles in /path/to/blog/src/content/blog
19:16:17 [INFO] Processing 36 articles (0 cached)
19:16:20 [INFO] Successfully analyzed 36/36 articles
19:16:21 [INFO] ✅ Global analysis written to: public/data/blog-analysis.json
```

### 4. 增量更新

修改文章后，再次运行会自动跳过未修改的文章：

```bash
python scripts/ai_analysis/run.py --verbose
```

输出示例：

```
19:20:15 [INFO] Found 36 articles
19:20:15 [DEBUG] Cache hit: 2024-08-19-博客图床搭建.md
19:20:15 [DEBUG] Cache hit: 2024-08-23-postman使用指北.md
...
19:20:15 [INFO] Processing 1 articles (35 cached)  # 只处理1篇新文章
19:20:18 [INFO] Successfully analyzed 1/1 articles
```

### 5. 可选参数

#### `--force` - 强制重新分析

忽略缓存，重新分析所有文章（谨慎使用，会产生完整 API 费用）：

```bash
python scripts/ai_analysis/run.py --force
```

**使用场景**：

- 修改了分析 prompt 或 schema
- 更换了 LLM 模型
- 怀疑缓存数据有问题

#### `--limit N` - 限制分析数量

只处理前 N 篇文章，用于测试：

```bash
# 先测试 5 篇文章
python scripts/ai_analysis/run.py --limit 5 --verbose
```

**使用场景**：

- 首次运行前测试配置是否正确
- 验证新的分析维度
- 调试 prompt 效果

#### `--dry-run` - 预览模式

列出待分析的文章，但不实际调用 LLM：

```bash
python scripts/ai_analysis/run.py --dry-run
```

输出：

```
19:25:10 [INFO] Found 36 articles
19:25:10 [INFO] DRY RUN target: 2025-10-31-AI驱动的博客分析系统/index.md
19:25:10 [INFO] DRY RUN target: 2024-08-19-博客图床搭建.md
```

**使用场景**：

- 查看哪些文章会被重新分析
- 检查缓存命中情况
- 预估 API 调用成本

#### `--target PATH` - 指定文章分析

分析指定的文章（支持多次指定）：

```bash
# 强制重新分析指定文章（使用完整路径）
python scripts/ai_analysis/run.py --target "/Users/renjie.pu/blog/src/content/blog/2025-10-31-AI驱动的博客分析系统/index.md" --force

# 分析多个指定文章
python scripts/ai_analysis/run.py --target "src/content/blog/2025-04-02-初识MCP.md" --target "src/content/blog/2025-04-23-MCP开发指北.md" --force

# 指定文章但使用缓存（如果可用）
python scripts/ai_analysis/run.py --target "src/content/blog/2024-08-19-博客图床搭建.md"
```

**使用场景**：

- 重新分析特定文章以获得新的 AI 见解
- 测试某篇文章的分析效果
- 修复特定文章的分析错误
- 文章内容未变但想强制更新分析结果

**注意**：

- 支持绝对路径和相对路径
- 可以多次使用 `--target` 参数指定多篇文章
- 配合 `--force` 使用可忽略缓存强制重新分析
- 全局 reduce 阶段仍会加载所有缓存文章，确保全局分析完整性

#### 组合使用

```bash
# 强制重新分析前 3 篇，查看详细日志
python scripts/ai_analysis/run.py --force --limit 3 --verbose

# 预览所有未缓存的文章
python scripts/ai_analysis/run.py --dry-run --verbose

# 强制分析指定的多篇文章
python scripts/ai_analysis/run.py --target "article1.md" --target "article2.md" --force --verbose
```

### 6. 查看结果

分析完成后，有三处可以查看结果：

#### 📁 单篇文章缓存

```bash
# 查看某篇文章的详细分析
cat scripts/ai_analysis/cache/2024-08-19-博客图床搭建_01ae6a97.json | python -m json.tool
```

#### 📊 全局汇总数据

```bash
# 查看全局统计
cat public/data/blog-analysis.json | python -m json.tool | head -50
```

#### 🌐 可视化界面

启动开发服务器，访问 `/about` 页面：

```bash
npm run dev
# 打开 http://localhost:4321/about
```

### 7. 常见问题排查

#### 问题 1: API Key 未设置

```
[ERROR] API_KEY not set in environment
```

**解决**：

```bash
export API_KEY="your_key_here"
```

#### 问题 2: 网络超时

```
[WARNING] Request failed (attempt 1/3), retrying...
```

**解决**：

- 检查网络连接
- 调整超时时间：`export AI_REQUEST_TIMEOUT_S=600`
- 使用代理：`export https_proxy=http://127.0.0.1:7890`

#### 问题 3: Python 版本不兼容

```
TypeError: unsupported operand type(s) for |
```

**解决**：升级到 Python 3.10+ 或修改类型注解为 `Union`

#### 问题 4: 缓存目录不存在

```
FileNotFoundError: [Errno 2] No such file or directory: 'scripts/ai_analysis/cache'
```

**解决**：

```bash
mkdir -p scripts/ai_analysis/cache
mkdir -p public/data
```

### 8. 完整工作流示例

```bash
# Step 1: 首次设置
export API_KEY="sk-xxxxx"
pip install -r scripts/requirements.txt

# Step 2: 小规模测试
python scripts/ai_analysis/run.py --limit 3 --verbose

# Step 3: 检查结果
cat public/data/blog-analysis.json | python -m json.tool | head -20

# Step 4: 确认无误后全量分析
python scripts/ai_analysis/run.py --verbose

# Step 5: 启动开发服务器查看可视化
npm run dev

# Step 6: 后续增量更新
# 写新文章后...
python scripts/ai_analysis/run.py --verbose  # 只分析新文章

# Step 7: 重新分析特定文章（不满意某篇文章的分析结果时）
python scripts/ai_analysis/run.py --target "src/content/blog/your-article.md" --force --verbose

# Step 8: 构建生产环境
npm run build
```

> 💰 **成本优化建议**：
>
> - 开发阶段使用 `--limit` 测试
> - 正式运行前用 `--dry-run` 预览
> - 利用缓存机制，避免 `--force`

## 系统架构

整个系统采用经典的 **Map-Reduce** 架构，分为三个核心阶段：

```
Blog Posts → Map (单篇分析) → Cache → Reduce (全局聚合) → 可视化
```

### 核心特性

- ✅ **Map-Reduce 并行处理**：多线程分析单篇文章，提高效率
- ✅ **MD5 智能缓存**：基于内容哈希缓存分析结果，避免重复计算
- ✅ **混合计算策略**：统计型数据用代码计算，分析型数据用 LLM 生成
- ✅ **健壮的错误处理**：LLM 失败时自动 fallback 到统计方法
- ✅ **多维度可视化**：ECharts 呈现 7 种不同的分析维度

## 技术栈

### 后端分析引擎

- **Python 3.9+**：脚本语言
- **Pydantic**：数据验证和 schema 定义
- **DeepSeek API**：LLM 服务（支持替换为其他模型）
- **并发处理**：`ThreadPoolExecutor` 加速分析

### 前端可视化

- **Astro**：博客框架
- **ECharts 5**：图表库
- **echarts-wordcloud**：词云插件

## Map 阶段：单篇文章分析

### 1. 数据提取

首先解析 Markdown 文件的 frontmatter 和正文：

```python
def parse_frontmatter_and_body(path: Path) -> Tuple[Dict, str]:
    """Parse YAML frontmatter and markdown body"""
    content = path.read_text(encoding='utf-8')
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = yaml.safe_load(parts[1])
            body = parts[2].strip()
            return frontmatter, body
    return {}, content
```

### 2. 基础指标计算

在调用 LLM 前，先用代码计算基础指标：

```python
# Calculate sentence lengths
lens = sentence_lengths(body)
avg_len = round(sum(lens) / max(1, len(lens)), 2)

# Bucket distribution
buckets = {
    "1-10": sum(1 for l in lens if l <= 10),
    "11-20": sum(1 for l in lens if 11 <= l <= 20),
    "21-30": sum(1 for l in lens if 21 <= l <= 30),
    "30+": sum(1 for l in lens if l > 30)
}
```

### 3. LLM 深度分析

构建精确的 prompt，让 LLM 分析文章的深层特征：

```python
schema_hint = {
    "style": {
        "tone": {
            "teaching": "float",    # Teaching tone (0-1)
            "reflective": "float",  # Reflective tone (0-1)
            "humor": "float",       # Humor level (0-1)
            "critical": "float"     # Critical thinking (0-1)
        },
        "rhythm": "str",           # Writing rhythm description
        "tropes": ["str"]          # Literary devices used
    },
    "content": {
        "keywords": ["str"],       # Key topics
        "concepts": ["str"]        # Abstract concepts
    },
    "sentiment": {
        "label": "str",            # e.g. "积极", "中性"
        "score": "float"           # Sentiment score
    },
    "structure": {
        "pattern": "str",          # e.g. "总分总", "教程式"
        "opening": "str",          # Opening strategy
        "closing": "str"           # Closing strategy
    },
    "depth": "str"                 # Content depth assessment
}
```

### 4. MD5 缓存机制

使用内容哈希作为缓存键，文章内容不变则直接读取缓存：

```python
content_md5 = md5_hash_text(body)
cache_file = CACHE_DIR / f"{article_name}_{content_md5}.json"

if cache_file.exists() and not force_recompute:
    return load_from_cache(cache_file)
```

这个设计的优点：

- ✅ 修改 frontmatter（标题、日期等）不影响缓存
- ✅ 只有正文修改才会触发重新分析
- ✅ 大幅降低 API 调用成本

## Reduce 阶段：全局数据聚合

### 核心设计理念

**统计型数据用代码计算，分析型数据用 LLM 增强**

```python
def reduce_global(articles: List[ArticleAnalysis]) -> GlobalAnalysis:
    # 1. Statistical calculations (reliable & free)
    tone_avg = _calculate_tone_avg(articles)
    sentiment_dist = _calculate_sentiment_dist(articles)
    concept_network = _concept_network(articles)
    timeline_depth = _calculate_timeline_depth(articles)
    structures = _calculate_structures(articles)
    
    # 2. LLM enhancement (optional, with fallback)
    try:
        topics = _llm_topic_naming(articles)
    except Exception as e:
        topics = _fallback_to_frequency_topics(articles)
    
    return GlobalAnalysis(summary=summary, perArticle=articles)
```

### 1. 平均语气计算

```python
def _calculate_tone_avg(articles: List[ArticleAnalysis]) -> Dict[str, float]:
    """Calculate average tone across all articles"""
    tone_keys = ["teaching", "reflective", "humor", "critical"]
    tone_sums = defaultdict(float)
    tone_counts = defaultdict(int)
    
    for article in articles:
        for key in tone_keys:
            val = article.style.tone.get(key)
            if val is not None:
                tone_sums[key] += val
                tone_counts[key] += 1
    
    return {
        k: round(tone_sums[k] / tone_counts[k], 2) 
        if tone_counts[k] > 0 else 0.0 
        for k in tone_keys
    }
```

### 2. 情感分布统计

使用模糊匹配将 LLM 生成的情感标签归类：

```python
def _calculate_sentiment_dist(articles: List[ArticleAnalysis]) -> Dict[str, float]:
    """Calculate sentiment distribution"""
    sentiment_map = {
        "positive": ["积极", "积极反思", "积极向上", "理性积极"],
        "neutral": ["中性", "中性偏", "反思性中立"],
        "negative": ["消极", "负面"]
    }
    
    counts = {"positive": 0, "neutral": 0, "negative": 0}
    total = 0
    
    for article in articles:
        label = article.sentiment.label
        if not label:
            continue
        total += 1
        
        for category, keywords in sentiment_map.items():
            if any(kw in label for kw in keywords):
                counts[category] += 1
                break
        else:
            counts["neutral"] += 1  # Default
    
    return {k: round(v / total, 3) for k, v in counts.items()}
```

### 3. 概念关系网络

构建概念共现网络，展示思想脉络：

```python
def _concept_network(articles: List[ArticleAnalysis]) -> Dict:
    """Build concept co-occurrence network"""
    node_weight = Counter()
    link_weight = Counter()
    
    for article in articles:
        concepts = article.content.concepts
        
        # Node weights
        for concept in concepts:
            node_weight[concept] += 1
        
        # Link weights (concepts appearing together)
        for i, source in enumerate(concepts):
            for j in range(i + 1, min(len(concepts), i + 10)):
                target = concepts[j]
                key = (source, target) if source < target else (target, source)
                link_weight[key] += 1
    
    return {
        "nodes": [{"id": k, "weight": v} for k, v in node_weight.items()],
        "links": [{"source": s, "target": t, "weight": w} 
                  for (s, t), w in link_weight.items()]
    }
```

## 前端可视化

### 数据加载

```javascript
const res = await fetch('/data/blog-analysis.json')
const data = await res.json()
```

### 雷达图：写作风格

```javascript
const radar = echarts.init(document.getElementById('tone-radar'))
const tone = data.summary.style.toneAvg

radar.setOption({
  radar: {
    indicator: Object.keys(tone).map(k => ({ 
      name: k, 
      max: 1 
    }))
  },
  series: [{
    type: 'radar',
    data: [{
      value: Object.values(tone),
      name: 'Average Tone'
    }]
  }]
})
```

### 力导向图：概念关系网络

```javascript
const force = echarts.init(document.getElementById('concept-force'))
const network = data.summary.conceptNetwork

force.setOption({
  series: [{
    type: 'graph',
    layout: 'force',
    roam: true,
    data: network.nodes.map(n => ({
      name: n.id,
      value: n.weight,
      symbolSize: Math.max(6, Math.min(28, n.weight * 2))
    })),
    links: network.links,
    force: {
      repulsion: 120
    }
  }]
})
```

### 词云图（带 fallback）

```javascript
// Try wordCloud first
if (echarts.graphic && echarts.graphic.RadialGradient) {
  chart.setOption({
    series: [{
      type: 'wordCloud',
      shape: 'circle',
      sizeRange: [12, 60],
      data: keywords.map(([name, value]) => ({ name, value }))
    }]
  })
} else {
  // Fallback to horizontal bar chart
  chart.setOption({
    xAxis: { type: 'value' },
    yAxis: { 
      type: 'category', 
      data: keywords.slice(0, 20).map(([name]) => name)
    },
    series: [{ 
      type: 'bar', 
      data: keywords.slice(0, 20).map(([, value]) => value)
    }]
  })
}
```


## 参考资源

- [ECharts 官方文档](https://echarts.apache.org/)
- [Pydantic 数据验证](https://docs.pydantic.dev/)
- [DeepSeek API](https://platform.deepseek.com/)
- [Astro 框架](https://astro.build/)

