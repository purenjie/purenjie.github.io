---
title: Git 操作
date: 2018-01-31 18:36:37
categories: 编程
tags: Git
---

![](/img/git.png)

<!-- more -->

### 初始配置
```
$ git config --global user.name "user_name"
$ git config --global user.email "user_email"
$ git config --list		//列出 Git 能找到的配置
$ git config 		//检查某一项设置
$ git  --help		//获取帮助
```

### 创建版本库
```
$ mkdir filename
$ cd filename
$ git init	 //文件夹目录变成 Git 可以管理的仓库    
$ ls -ah 命令查看隐藏的 .git 目录
```

版本控制系统，只能跟踪文本文件的改动，二进制文件不能追踪文件变化，word文件改动无法追踪

```
$ git add 	//把文件添加到仓库
$ git commit -m "description"	//把文件提交到仓库 
$ git commit -a -m "description" //add commit合并
$ git status	//查看仓库当前状态
$ git diff		//查看修改内容 different
$ git diff (-- filename)   //工作区(work dict)和暂存区(stage)的比较
$ git diff --cached (-- filename)   //暂存区(stage)和分支(master)的比较
$ git diff HEAD (-- filename)	//工作区(word dict)与分支(master)的比较
```

### 版本回退

```
$ git log	//显示从最近到最远的提交日至
$ git log --pretty=oneline	//日志输出一行
```

- HEAD：当前版本
- HEAD^：上一版本
- HEAD^^:上上一版本
- HEAD~n:上n个版本

```
$ git reset --hard HEAD^	//回退上一个版本
$ git reset --hard commit_id	//回退特定版本
$ git log	//查看提交历史，确定回到哪个版本
$ git reflog	//查看命令历史，重返未来
```
### 管理修改

- Git跟踪并管理的是修改的内容，而非文件
- 暂存区中的修改和工作区的修改分离

### 撤销修改

```
#在工作区
$ git checkout -- filename  //必须加文件名否则不会丢弃工作区更改

#在暂存区
$ git reset HEAD (-- filename)
$ git checkout -- filename

#添加到版本库
$ git reset 	//版本回退
```
### 删除文件

```
$ rm test.txt

1.从版本库删除文件
$ git rm test.txt	//必须加文件名
rm 'test.txt'
$ git commit -m "remove test.txt"
[master d17efd8] remove test.txt
 1 file changed, 1 deletion(-)
 delete mode 100644 test.txt
 
2.想要恢复版本库中的文件
$ git checkout -- test.txt
```

### 远程仓库

[本地仓库连接到 GitHub](http://blog.csdn.net/zhangxinyu11021130/article/details/73410082?yyue=a21bo.50862.201879)

### 添加远程仓库

1. GitHub 创建仓库
2. `$ git remote add origin git@server-name:path/repo-name.git`
3. `$ git push -u origin master`

由于远程库是空的，我们第一次推送`master`分支时，加上了`-u`参数，Git不但会把本地的`master`分支内容推送的远程新的`master`分支，还会把本地的`master`分支和远程的`master`分支关联起来，在以后的推送或者拉取时就可以简化命令。

4. `$ git push origin master`

### 从远程库克隆

要克隆一个仓库，首先必须知道仓库的地址，然后使用`git clone`命令克隆。

Git支持多种协议，包括`https`，但通过`ssh`支持的原生`git`协议速度最快。

```
$ git fetch [remote-name]	//从远程库抓取自己没有的数据
$ git pull 				   //自动的抓取然后合并远程分支到当前分支
$ git remote show [remote-name]//查看远程仓库信息
$ git remote rm				//移除远程仓库
```



### 分支管理

在不破坏原来的分支的基础上新建分支自己进行项目进展

### 创建与合并分支

```
Git鼓励大量使用分支：

查看分支：git branch

创建分支：git branch 

切换分支：git checkout 

创建+切换分支：git checkout -b 

合并某分支到当前分支：git merge 

删除分支：git branch -d 
```



`master`分支是一条线，Git用`master`指向最新的提交，再用`HEAD`指向`master`，就能确定当前分支，以及当前分支的提交点：

![git-br-initial](https://cdn.liaoxuefeng.com/cdn/files/attachments/0013849087937492135fbf4bbd24dfcbc18349a8a59d36d000/0)

每次提交，`master`分支都会向前移动一步，这样，随着你不断提交，`master`分支的线也越来越长

当我们创建新的分支，例如`dev`时，Git新建了一个指针叫`dev`，指向`master`相同的提交，再把`HEAD`指向`dev`，就表示当前分支在`dev`上：

![git-br-create](https://cdn.liaoxuefeng.com/cdn/files/attachments/001384908811773187a597e2d844eefb11f5cf5d56135ca000/0)

对工作区的修改和提交就是针对`dev`分支了，比如新提交一次后，`dev`指针往前移动一步，而`master`指针不变：

![git-br-dev-fd](https://cdn.liaoxuefeng.com/cdn/files/attachments/0013849088235627813efe7649b4f008900e5365bb72323000/0)

假如我们在`dev`上的工作完成了，就可以把`dev`合并到`master`上。Git怎么合并呢？最简单的方法，就是直接把`master`指向`dev`的当前提交，就完成了合并：

![git-br-ff-merge](https://cdn.liaoxuefeng.com/cdn/files/attachments/00138490883510324231a837e5d4aee844d3e4692ba50f5000/0)

所以Git合并分支也很快！就改改指针，工作区内容也不变！

合并完分支后，甚至可以删除`dev`分支。删除`dev`分支就是把`dev`指针给删掉，删掉后，我们就剩下了一条`master`分支：

![git-br-rm](https://cdn.liaoxuefeng.com/cdn/files/attachments/001384908867187c83ca970bf0f46efa19badad99c40235000/0)

### 解决冲突

当Git无法自动合并分支时，就必须首先解决冲突。解决冲突后，再提交，合并完成。

`git log --graph`命令可以看到分支合并图

`$ git log --graph --pretty=oneline --abbrev-commit`可看简略图

### 分支管理策略

通常，合并分支时，如果可能，Git会用`Fast forward`模式，但这种模式下，删除分支后，会丢掉分支信息。

如果要强制禁用`Fast forward`模式，Git就会在merge时生成一个新的commit，这样，从分支历史上就可以看出分支信息。

`git merge --no-ff -m " " `

在实际开发中，我们应该按照几个基本原则进行分支管理：

首先，`master`分支应该是非常稳定的，也就是仅用来发布新版本，平时不能在上面干活；

那在哪干活呢？干活都在`dev`分支上，也就是说，`dev`分支是不稳定的，到某个时候，比如1.0版本发布时，再把`dev`分支合并到`master`上，在`master`分支发布1.0版本；

你和你的小伙伴们每个人都在`dev`分支上干活，每个人都有自己的分支，时不时地往`dev`分支上合并就可以了。

所以，团队合作的分支看起来就像这样：

![git-br-policy](https://cdn.liaoxuefeng.com/cdn/files/attachments/001384909239390d355eb07d9d64305b6322aaf4edac1e3000/0)

### Bug 分支

Git还提供了一个`stash`功能，可以把未提交的内容“储藏”起来，等以后恢复现场后继续工作

修复 bug 后切换回`stash`的分支恢复

```
$ git stash list	//查看 stash 的列表
$ git stash pop		//恢复 stash 的内容并且删除记录
```

### Feature 分支

开发一个新feature，最好新建一个分支；

如果要丢弃一个没有被合并过的分支，可以通过`git branch -D `强行删除。

###　多人协作

[多人协作－廖雪峰](https://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000/0013760174128707b935b0be6fc4fc6ace66c4f15618f8d000)

### 标签管理

commit 和 tag —— IP 和域名

tag 是指向某个特定 commit 的指针，不可移动

- [创建标签](https://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000/001376951758572072ce1dc172b4178b910d31bc7521ee4000)

```
命令git tag 用于新建一个标签，默认为HEAD，也可以指定一个commit id；

git tag -a  -m "blablabla..."可以指定标签信息；

git tag -s  -m "blablabla..."可以用PGP签名标签；

命令git tag可以查看所有标签。
```

- 操作标签

```
命令git push origin 可以推送一个本地标签；

命令git push origin --tags可以推送全部未推送过的本地标签；

命令git tag -d 可以删除一个本地标签；

命令git push origin :refs/tags/可以删除一个远程标签。
```

###　使用 GitHub

- 在GitHub上，可以任意Fork开源仓库；
- 自己拥有Fork后的仓库的读写权限；
- 可以推送pull request给官方仓库来贡献代码。

### 自定义 Git

```
$ git config --global color.ui true		//让Git显示颜色，命令输出看起来更醒目
```

### 忽略特殊文件

- 忽略某些文件时，需要编写`.gitignore`；
- `.gitignore`文件本身要放到版本库里，并且可以对`.gitignore`做版本管理！
- [GitHub配置忽略文件](https://github.com/github/gitignore)

### 配置别名

```
$ git config --global alias.co checkout 
$ git config --global alias.br branch 
$ git config --global alias.ci commit 
$ git config --global alias.st status
$ git config --global alias.unstage 'reset HEAD --'//撤销在暂存区的修改
$ git config --global alias.last 'log -1 HEAD'
$ git config --global alias.lg "log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"
```


