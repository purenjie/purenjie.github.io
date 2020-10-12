title: gitee+hugo博客搭建
author: Solejay
top: false
cover: false
toc: true
mathjax: false
tags:
  - hugo
  - gitee
img: >-
  https://ss2.bdstatic.com/70cFvnSh_Q1YnxGkpoWK1HF6hhy/it/u=299634975,2536544645&fm=26&gp=0.jpg
categories: []
date: 2020-10-11 21:36:00
coverImg:
summary:
---
## Hugo 构建

### Hugo 安装

- 下载[安装包](https://github.com/gohugoio/hugo/releases)
- `hugo version` 查看是否安装成功

### 生成站点基础框架

- 进入自己指定文件夹下执行 `hugo new site solejay-blog`
- 创建仓库

```bash
cd solejay-blog
git init
```

### 主题配置

- 进入 [Hugo 主题页面](https://themes.gohugo.io/) 选择主题并下载 

> 个人喜欢的两个主题：[newsroom](https://themes.gohugo.io/newsroom/)、[Swift](https://themes.gohugo.io/hugo-swift-theme/)

```bash
git submodule add https://github.com/onweru/newsroom.git themes/newsroom # 前面初始化仓库主题的仓库就没有 git 仓库了
```

- 在配置文件 `config.toml` 中设置主题

在 `config.toml` 文件里最后一行添加 `theme = "hugo-swift-theme"`

### 新建博客

```bash
hugo new posts/first-post.md
```

### 本地调试和打包构建

- 本地调试

```bash
hugo server -D
```

即可在本地 http://localhost:1313/ 看到静态页面

- 打包构建

调试没有问题运行 `hugo` 在当前目录下生成 `public` 子目录

## Gitee 部署

- 新建仓库

添加一个空白 repository，注意不要添加如 `README`，`.gitignore` 等文档。仓库名最好与个人空间地址一致

- 使用两个分支，一个控制源文档，一个控制生成的网页文档
- master 分支

```bash
echo "public" >> .gitignore
git add .
git commit -m "first source code"
git remote add origin https://gitee.com/solejay/solejay.git
git push -u origin master
```

- hugo 分支

```bash
git checkout --orphan hugo
```

创建脚本 `hugo.sh` 并执行

```bash
#!/bin/sh

if [[ $(git status -s) ]]
then
    echo "The working directory is dirty. Please commit any pending changes."
    exit 1;
fi

echo "Deleting old publication"
rm -rf public
mkdir public
rm -rf .git/worktrees/public/

echo "Checking out hugo branch into public"
git worktree add -B hugo public origin/hugo

echo "Removing existing files"
rm -rf public/*

echo "Generating site"
hugo

echo "Updating hugo branch"
cd public && git add --all && git commit -m "Publishing to hugo (publish.sh)"

echo "Push to origin"
git push origin hugo
```

- 进入 [Gitee](https://gitee.com/) 创建的仓库页面，从 `服务` 栏里选择 `Gitee Pages`，部署分支选择 `hugo`，然后点击 `启动`

## 博客更新

1. 本地推送

```bash
hugo new posts/name.md
hugo server -D

git add .
git commit -m ""
git push origin master

./hugo.sh
```

2. Gitee 更新

进入 [pages](https://gitee.com/solejay/solejay/pages) 页面点击 `更新`

**参考资料**

[Hugo+Gitee 搭建个人博客](https://zhuanlan.zhihu.com/p/184625753)

[如何使用 Hugo 在 GitHub Pages 上搭建免费个人网站](https://zhuanlan.zhihu.com/p/37752930)