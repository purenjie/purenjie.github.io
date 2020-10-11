---
title: hexo各种问题
date: 2020-04-08 22:15:55
author: Solejay
img: https://pic2.zhimg.com/80/v2-6890485c84748900d9dae824b7f7cbb1_720w.jpg
top: false
cover: false
coverImg: 
toc: true
mathjax: false
summary: 
categories: 
tags:
  - hexo
---

## 模版（Scaffold）

在新建文章时，Hexo 会根据 `scaffolds` 文件夹内相对应的文件来建立文件，例如：

```
$ hexo new photo "My Gallery"
```
在执行这行指令时，Hexo 会尝试在 `scaffolds` 文件夹中寻找 `photo.md`，并根据其内容建立文章

## hexo 本地图片无法显示

1. 找到`Hexo`下的`_config.yml`里的`post_asset_folder`，把这个选项从`false`改成`true`
2. 在`Hexo`目录下打开Git Brsh，执行一个下载上传图片插件的命令`npm install hexo-asset-image --save`
3. 修改 `/node_modules/hexo-asset-image/index.js` 文件

```js
'use strict';
var cheerio = require('cheerio');

// http://stackoverflow.com/questions/14480345/how-to-get-the-nth-occurrence-in-a-string
function getPosition(str, m, i) {
  return str.split(m, i).join(m).length;
}

var version = String(hexo.version).split('.');
hexo.extend.filter.register('after_post_render', function(data){
  var config = hexo.config;
  if(config.post_asset_folder){
    	var link = data.permalink;
	if(version.length > 0 && Number(version[0]) == 3)
	   var beginPos = getPosition(link, '/', 1) + 1;
	else
	   var beginPos = getPosition(link, '/', 3) + 1;
	// In hexo 3.1.1, the permalink of "about" page is like ".../about/index.html".
	var endPos = link.lastIndexOf('/') + 1;
    link = link.substring(beginPos, endPos);

    var toprocess = ['excerpt', 'more', 'content'];
    for(var i = 0; i < toprocess.length; i++){
      var key = toprocess[i];
 
      var $ = cheerio.load(data[key], {
        ignoreWhitespace: false,
        xmlMode: false,
        lowerCaseTags: false,
        decodeEntities: false
      });

      $('img').each(function(){
		if ($(this).attr('src')){
			// For windows style path, we replace '\' to '/'.
			var src = $(this).attr('src').replace('\\', '/');
			if(!/http[s]*.*|\/\/.*/.test(src) &&
			   !/^\s*\//.test(src)) {
			  // For "about" page, the first part of "src" can't be removed.
			  // In addition, to support multi-level local directory.
			  var linkArray = link.split('/').filter(function(elem){
				return elem != '';
			  });
			  var srcArray = src.split('/').filter(function(elem){
				return elem != '' && elem != '.';
			  });
			  if(srcArray.length > 1)
				srcArray.shift();
			  src = srcArray.join('/');
			  $(this).attr('src', config.root + link + src);
			  console.info&&console.info("update link as:-->"+config.root + link + src);
			}
		}else{
			console.info&&console.info("no src attr, skipped...");
			console.info&&console.info($(this));
		}
      });
      data[key] = $.html();
    }
  }
});
```

[Hexo上传的图片在网页上无法显示的解决办法](http://www.yuanerhero.top/2018/04/18/Hexo%E4%B8%8A%E4%BC%A0%E7%9A%84%E5%9B%BE%E7%89%87%E5%9C%A8%E7%BD%91%E9%A1%B5%E4%B8%8A%E6%97%A0%E6%B3%95%E6%98%BE%E7%A4%BA%E7%9A%84%E8%A7%A3%E5%86%B3%E5%8A%9E%E6%B3%95/)

[hexo引用本地图片无法显示](https://blog.csdn.net/xjm850552586/article/details/84101345)

### Hexo 安装

```bash
git clone git@github.com:purenjie/purenjie.github.io.git
sudo apt-get install nodejs
sudo npm install -g cnpm --registry=https://registry.npm.taobao.org //淘宝镜像源
sudo cnpm install hexo-cli -g
cnpm install
cnpm install hexo-deployer-git --save
```

### 备份

修改并本地调试好之后 `hexo clean && hexo g && hexo s` （可以在配置文件里设置 alias）

```bash
git add .
git commit -m "这次 post 的内容"
git push origin hexo

hexo d # 部署到 master 分支
```

### 恢复

```bash
git clone https://github.com/purenjie/purenjie.github.io.git
```

[使用 hexo，如果换了电脑怎么更新博客？](https://www.zhihu.com/question/21193762)

### Hexo 博客管理

[Hexo Admin Plugin](https://jaredforsyth.com/hexo-admin/)

```bash
cd blog_path
cnpm install --save hexo-admin
hexo server -d
```





