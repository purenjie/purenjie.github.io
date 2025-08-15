# 常用脚本命令

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

