# 字体使用指南

## 概述

本项目已集成霞鹜文楷字体，提供优秀的中文显示效果。字体系统采用中英文字体混合策略，确保在不同语言环境下都有最佳的显示效果。

## 字体配置

### 字体文件
- **霞鹜文楷 (LXGWWenKai)**: 中文字体，基于Fontworks的Klee One字体衍生
- **Satoshi**: 英文字体，现代化的无衬线字体
- **等宽字体**: 代码显示专用字体

### 字体特性
- 霞鹜文楷：优雅的楷体风格，适合中文阅读
- Satoshi：清晰易读，适合英文内容
- 支持字体回退，确保在不同系统下都有良好显示

## 使用方法

### 1. CSS类方式

#### 中文字体
```css
.chinese-text {
  font-family: 'LXGWWenKai', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', 'WenQuanYi Micro Hei', sans-serif;
}
```

#### 英文字体
```css
.english-text {
  font-family: 'Satoshi', 'LXGWWenKai', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', 'WenQuanYi Micro Hei', sans-serif;
}
```

#### 代码字体
```css
.code-text {
  font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', 'Source Code Pro', 'Menlo', 'Consolas', 'DejaVu Sans Mono', monospace;
}
```

### 2. UnoCSS类方式

#### 字体族类
```html
<!-- 使用霞鹜文楷字体 -->
<div class="font-wenkai">这是中文内容</div>

<!-- 使用Satoshi字体 -->
<div class="font-satoshi">This is English content</div>

<!-- 使用等宽字体 -->
<div class="font-mono">console.log('Hello World');</div>
```

#### 组合使用
```html
<!-- 中英文混合内容 -->
<article class="font-wenkai">
  <h1>文章标题</h1>
  <p>这是中文段落内容。</p>
  <p class="font-satoshi">This is an English paragraph.</p>
  <pre class="font-mono"><code>const message = "Hello 世界";</code></pre>
</article>
```

### 3. 组件中使用

#### Astro组件
```astro
---
// 在组件中定义字体样式
const fontClass = 'font-wenkai'
---

<div class={fontClass}>
  <h2>组件标题</h2>
  <p>组件内容使用霞鹜文楷字体显示。</p>
</div>
```

#### 动态字体切换
```astro
---
// 根据语言动态选择字体
const isChinese = true
const fontClass = isChinese ? 'font-wenkai' : 'font-satoshi'
---

<div class={fontClass}>
  {isChinese ? '中文内容' : 'English Content'}
</div>
```

## 性能优化

### 1. 字体预加载
字体已在 `BaseHead.astro` 中配置预加载：
```html
<link rel='preload' href='/fonts/LXGWWenKai-Regular.ttf' as='font' type='font/ttf' crossorigin />
```

### 2. 字体回退策略
使用 `font-display: swap` 确保字体加载过程中有良好的用户体验：
```css
@font-face {
  font-family: 'LXGWWenKai';
  src: url('/fonts/LXGWWenKai-Regular.ttf') format('truetype');
  font-display: swap;
}
```

### 3. Unicode范围限制
中文字体只在需要的字符范围内加载：
```css
unicode-range: U+4E00-9FFF, U+3400-4DBF, U+20000-2A6DF, U+2A700-2B73F, U+2B740-2B81F, U+2B820-2CEAF, U+F900-FAFF, U+2F800-2FA1F;
```

## 最佳实践

### 1. 字体选择原则
- **中文内容**: 优先使用 `font-wenkai` 或 `font-wenkai` 类
- **英文内容**: 使用 `font-satoshi` 类
- **代码内容**: 使用 `font-mono` 类
- **混合内容**: 根据主要语言选择字体，次要语言使用内联样式覆盖

### 2. 响应式字体
```css
/* 在不同屏幕尺寸下调整字体大小 */
.text-content {
  font-size: 1rem;
}

@media (min-width: 768px) {
  .text-content {
    font-size: 1.125rem;
  }
}

@media (min-width: 1024px) {
  .text-content {
    font-size: 1.25rem;
  }
}
```

### 3. 字体权重
```css
/* 标题使用较重的字重 */
h1, h2, h3 {
  font-weight: 600;
}

/* 正文使用正常字重 */
p, div {
  font-weight: 400;
}
```

## 故障排除

### 1. 字体不显示
- 检查字体文件是否正确放置在 `public/fonts/` 目录
- 确认CSS中的字体路径是否正确
- 检查浏览器开发者工具中的网络请求

### 2. 字体加载缓慢
- 确认字体预加载配置是否正确
- 考虑使用字体子集化减少文件大小
- 检查网络连接和服务器响应时间

### 3. 字体回退问题
- 确认字体回退链配置正确
- 测试在不同系统环境下的显示效果
- 检查字体文件的兼容性

## 扩展和自定义

### 1. 添加新字体
1. 将字体文件放入 `public/fonts/` 目录
2. 在 `src/assets/styles/app.css` 中添加 `@font-face` 声明
3. 在 `uno.config.ts` 中添加字体族配置
4. 更新字体回退策略

### 2. 字体子集化
使用工具如 `fonttools` 创建字体子集：
```bash
# 安装fonttools
npm install --save-dev fonttools

# 创建字体子集
pyftsubset LXGWWenKai-Regular.ttf --text-file=chars.txt --output-file=LXGWWenKai-Subset.ttf
```

### 3. CDN分发
考虑使用CDN分发字体文件以提升加载速度：
```css
@font-face {
  font-family: 'LXGWWenKai';
  src: url('https://cdn.example.com/fonts/LXGWWenKai-Regular.ttf') format('truetype');
}
```

## 参考资源

- [霞鹜文楷字体项目](https://github.com/lxgw/LxgwWenKai)
- [字体加载性能优化指南](https://web.dev/font-display/)
- [UnoCSS字体配置文档](https://unocss.dev/config/theme#fontfamily)
- [CSS字体回退策略](https://developer.mozilla.org/en-US/docs/Web/CSS/font-family)
