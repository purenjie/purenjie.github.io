# 文章

1. 创建文章

`hugo new posts/20xx-0x-xx-PostTitle.md`

2. 本地查看

`hugo server -D`

3. 部署 github

```bash
git add .
git commit -m "update"
git push origin master
```

4. 同步到服务器

```bash
rsync -avuz --progress --delete -e 'ssh -p 1202' dist/ root@104.168.120.15:/var/www/blog
```