# Solejay's Blog

基于 Astro 和 astro-pure 主题构建的个人博客，支持双语内容，集成博客分析工具和自动化脚本。

## 📂 项目目录结构

### 完整目录树

```
📦 blog/
├── 📝 astro.config.ts          # Astro 框架配置
├── 📝 uno.config.ts            # UnoCSS 样式配置
├── 📝 tsconfig.json            # TypeScript 配置
├── 📝 package.json             # 依赖和脚本
├── 📝 prettier.config.mjs      # Prettier 代码格式化配置
├── 📝 eslint.config.mjs        # ESLint 代码检查配置
│
├── 📂 src/                     # ⭐ 主要源代码目录
│   ├── 📄 site.config.ts       # 🎯 网站配置（主题、导航、页脚）
│   ├── 📄 content.config.ts    # 🎯 内容集合 Schema 定义
│   │
│   ├── 📁 content/             # 📝 内容集合目录
│   │   ├── blog/               # ✍️ 博客文章（Markdown/MDX 格式）
│   │   │   ├── post-name.md    # 单文件模式文章
│   │   │   └── post-folder/    # 目录模式文章（推荐）
│   │   │       ├── index.md    # 文章内容
│   │   │       └── images/     # 文章资源（图片等）
│   │   └── docs/               # 文档页面
│   │
│   ├── 📁 pages/               # 🌐 基于文件的路由
│   │   ├── index.astro         # 首页
│   │   ├── about/              # 关于页面
│   │   ├── blog/               # 博客列表和文章页面
│   │   ├── archives/           # 归档页面
│   │   ├── tags/               # 标签和标签页面
│   │   ├── projects/           # 项目展示页面
│   │   ├── links/              # 友链页面
│   │   ├── search/             # 搜索页面
│   │   └── terms/              # 条款页面
│   │
│   ├── 📁 layouts/             # 🎨 页面布局模板
│   │   ├── BaseLayout.astro    # 基础布局包装器
│   │   ├── BlogPost.astro      # 博客文章布局
│   │   ├── CommonPage.astro    # 通用页面布局
│   │   ├── ContentLayout.astro # 内容布局
│   │   └── IndividualPage.astro# 独立页面布局
│   │
│   ├── 📁 components/          # 🧩 可复用组件
│   │   ├── about/              # 关于页面组件
│   │   ├── home/               # 首页组件
│   │   ├── links/              # 友链页面组件
│   │   └── projects/           # 项目页面组件
│   │
│   ├── 📁 assets/              # 🖼️ 静态资源
│   │   ├── styles/             # 样式表（CSS）
│   │   ├── icons/              # 图标文件
│   │   ├── tools/              # 工具 Logo 图片
│   │   ├── projects/           # 项目图片
│   │   ├── avatar.png          # 头像
│   │   └── *-qrcode.jpg        # 二维码图片
│   │
│   └── 📁 plugins/             # 🔌 Astro 插件
│
├── 📂 public/                  # 🌍 公共静态文件（直接提供）
│   ├── favicon/                # 网站图标
│   ├── fonts/                  # 网页字体
│   ├── images/                 # 公共图片
│   ├── scripts/                # 客户端脚本
│   └── links.json              # 友链数据配置
│
├── 📂 scripts/                 # 🐍 Python 工具脚本
│   ├── blog_analysis.py        # AI 驱动的博客分析
│   ├── generate_new_post.py    # 新文章生成器
│   ├── generate_cover_image.py # 封面图生成器
│   ├── integrate_analysis_to_about.py # 分析结果集成到关于页面
│   ├── extract_chinese_chars.py # 提取中文字符工具
│   ├── requirements.txt        # Python 依赖
│   ├── analyzers/              # 分析器模块
│   ├── utils/                  # 工具函数
│   └── output/                 # 分析输出结果
│
├── 📂 packages/                # 📦 Monorepo 包
│   └── pure/                   # astro-pure 主题包
│
├── 📂 preset/                  # 🎨 预设配置和模板
│
└── 📂 dist/                    # 🚀 构建输出（生成的）
```

### 核心配置文件

| 文件                      | 作用                             | 何时修改                       |
| ------------------------- | -------------------------------- | ------------------------------ |
| `src/site.config.ts`    | 网站元数据、导航、页脚、主题设置 | 自定义网站信息、菜单、社交链接 |
| `src/content.config.ts` | 内容集合 Schema（博客、文档）    | 修改 frontmatter 字段定义      |
| `astro.config.ts`       | Astro 框架、集成、Markdown 插件  | 添加集成、配置 Markdown 处理   |
| `uno.config.ts`         | UnoCSS 样式、自定义工具类、字体  | 添加自定义样式、颜色、快捷方式 |
| `package.json`          | 依赖包、脚本命令                 | 添加包、修改命令               |
| `public/links.json`     | 友链数据                         | 添加或修改友情链接             |

### 快速任务指南

| 任务                       | 位置                            | 命令/操作                                                 |
| -------------------------- | ------------------------------- | --------------------------------------------------------- |
| ✍️**写新博客文章** | `src/content/blog/`           | `python scripts/generate_new_post.py "标题" --mode dir` |
| 🎨**自定义网站主题** | `src/site.config.ts`          | 编辑 `theme` 对象                                       |
| 🧭**修改导航菜单**   | `src/site.config.ts`          | 编辑 `nav` 数组                                         |
| 📝**编辑关于页面**   | `src/pages/about/index.astro` | 编辑 Astro 组件                                           |
| 🖼️**添加项目展示** | `src/pages/projects/`         | 添加到项目列表                                            |
| 🔗**管理友链**       | `public/links.json`           | 编辑 JSON 文件                                            |
| 🎯**更改首页布局**   | `src/components/home/`        | 修改首页组件                                              |
| 📊**运行博客分析**   | `scripts/`                    | `python blog_analysis.py`                               |
| 🏗️**生产环境构建** | 根目录                          | `npm run build`                                         |
| 🚀**部署到服务器**   | `dist/`                       | 使用 rsync 同步                                           |

### 文章内容结构

博客文章支持两种格式：

1. **单文件模式**: `src/content/blog/my-post.md`
2. **目录模式**: `src/content/blog/my-post/index.md` （推荐，便于管理图片资源）

必需的 frontmatter 字段：

```yaml
---
title: "文章标题"              # 最多 60 字符
description: "简短描述"        # 最多 160 字符
publishDate: 2025-01-01       # ISO 日期格式
tags: [标签1, 标签2]          # 小写，自动去重
heroImage:                    # 可选
  src: ./image.jpg
  alt: "图片描述"
draft: false                  # 默认: false
---
```

---

## ⚡ 常用脚本命令

生成文章

```bash
# 创建单文件模式
python scripts/generate_new_post.py "我的新文章" --mode file

# 创建目录模式
python scripts/generate_new_post.py "我的新文章" --mode dir
```

# 构建命令

```bash
# 本地调试
npm run dev

# 本地构建
npm run build

# 同步文件到服务器
rsync -avuz --progress --delete -e 'ssh -p 1202' dist/ root@104.168.120.15:/opt/1panel/apps/openresty/openresty/www/sites/solejay.cn/index
```

# 博客使用

[Astro博客使用](https://solejay.cn/blog/2025-08-15-astro%E5%8D%9A%E5%AE%A2%E8%BF%81%E7%A7%BB/)
