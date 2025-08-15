---
title: astro博客使用
publishDate: 2025-08-15
description: 'hugo 迁移 astro'
tags:
  - blog
  - astro

heroImage:
  { src: 'https://samuelhorn.com/_astro/astro.DRvFg8I7_Zt0AE0.webp', inferSize: true, color: '#9698C1'  }
language: 'Chinese'
---

# 安装

> Node version 要求：>=18

```bash
❯ npm create astro@latest -- --template cworld1/astro-theme-pure
❯ cd $FOLDER
❯ npm install
❯ npm run dev
```

# 目录结构

```bash
.
├── public // 复制到 root 路径的静态资源
│   ├── favicon
│   ├── fonts
│   ├── icons
│   ├── images
│   ├── links.json
│   ├── scripts
│   └── styles
├── src
│   ├── assets // 静态资源
│   ├── components // 主题中使用的组件，也包括用户类似组件，如 Card 、 Collapse 、 Spoiler 等
│   ├── content // 博客内容
│   ├── content.config.ts
│   ├── layouts // 基本站点布局
│   ├── pages // 页面如 404 、 about 、 blog 、 docs 、 index 等
│   ├── plugins // 主题中使用的扩展插件
│   ├── site.config.ts // 配置文件
│   └── type.d.ts
├── astro.config.ts // Astro 配置文件
├── eslint.config.mjs // ESLint 配置文件
├── package.json // node 包信息
├── prettier.config.mjs // Prettier 配置文件
├── tsconfig.json // ts 配置文件
└── uno.config.ts // UnoCSS 配置文件
```

# 写文章

## 1. 新建文章

在 `/src/content/blog` 目录下直接新建 `.md` 文件

## 2. 新建目录

在 `/src/content/blog` 目录下新建一个目录，文章和图片等资源放在目录下，文章命名为 `index.md`

```yaml
---
title: 'First Article' # (Required, max 60)
description: 'I like writing articles.' # (Required, 10 to 160)
publishDate: '2024-11-30 00:08:00' # (Required, Date)
tags:
  - Markdown # (Also can write format like next line)
heroImage: { src: './thumbnail.jpg', alt: 'an image targetting my article', color: '#B4C6DA' } # 本地文件，需要和文章在同一目录下
heroImage:
  { src: 'https://img.tukuppt.com/ad_preview/00/15/09/5e715a320b68e.jpg!/fw/980', inferSize: true } # 远程文件
# Or specificed width and height
heroImage:
  { src: 'https://img.tukuppt.com/ad_preview/00/15/09/5e715a320b68e.jpg!/fw/980', width: 980, height: 551 } # 远程文件
draft: false # (set true will only show in development)
language: 'English' # (String as you like)
comment: true # (set false will disable comment, even if you've enabled it in site-config)
---

## This is a title

This is a paragraph.
```

# 常用命令及高级用法

## 常用命令

```bash
# 本地调试
npm run dev

# 本地构建
npm run build
```

## 高级用法

[组件](https://astro-pure.js.org/docs/integrations/components#spoiler)

使用 `.astro` 或者 `.mdx` 文件编写，包括卡片、列表、时间线、步骤、icon 等

[高级组件](https://astro-pure.js.org/docs/integrations/advanced)

包括 github 卡片、链接预览、二维码、图片缩放

## 评论系统

评论集成 [Waline Comment System](https://waline.js.org/)

可以在 `src/site.config.ts` 中关闭

## 友链

在 `public/links.json` 中配置

## 定制主题

[文档地址](https://astro-pure.js.org/docs/advanced/customize)
