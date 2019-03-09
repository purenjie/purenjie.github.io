---
title: 利用Python实现文件备份
date: 2018-02-07 10:47:50
tags: python
categories: 编程
---

此脚本可在终端运行，可输入多个路径进行备份，最后输入的路径作为压缩文件的存储位置和解压（备份）位置。

如果需要备份的文件中文件数据量比较小文件的数量又比较多的时候，复制粘贴速度会很慢，所以考虑先将文件打包压缩，再透过解压文件备份到指定的目录。脚本可在终端运行，可输入`python3 backup.py 需要备份的文件路径 备份的位置`进行备份。

用到了 zipfile 模块、os 模块、sys 模块、 time 模块。zipfile 模块进行压缩和解压，os 模块遍历文件夹， time 模块标注备份的时间信息，sys 模块用于在终端接收待压缩文件以及解压（备份）的路径 。

sys 模块中 sys.argv 接收终端输入并存储在一个 list 中，通过对 list 的操作实现多个文件夹的备份

<!--more-->

####  zipfile 模块，可以实现 ZIP 文件的创建、读写、添加。

`class zipfile.ZipFile(file, mode='r', compression=ZIP_STORED, allowZip64=True)`

zipfile.ZipFile()方法创建一个 ZipFile 对象，表示一个 ZipFile 文件。它可以接收四个参数。

1. file：被操作文件/文件夹的路径或类文件对象，生成压缩文件的路径
2. mode：打开 zip 文件的模式，默认值为 ‘r'，还有三种模式

-  'r'：表示读已经存在的zip文档
-  ’w‘：新建一个 zip 文档或覆盖一个已经存在的zip文档
-  ’a'：向一个已经存在的 zip 文档增加数据
-  ‘x'：专门创建并写入一个新的 zip 文件

3. compression：文件的压缩方法，默认即可
4. allowZip64：支持压缩文件大于 4 G，默认即可

`ZipFile.write(filename, arcname=None, compress_type=None)`

write()方法可以实现对文件/文件夹的压缩，它可以接收三个参数。

1. filename：被压缩文件的（路径）名。如果为单个文件，即传入文件的绝对路径；如果为文件夹，则需将文件一个一个地传入才能压缩。
2. arcname：压缩文件解压后的文件名，默认为压缩前文件的路径名
3. compress_type：表示压缩方法，默认即可

`ZipFile.extractall(path=None, members=None, pwd=None)`

解压zip文档中的所有文件。

1. path：默认当前目录，可指定不同目录
2. members：必须为所有被压缩文件名字组成的一个 list 的子集
3. pwd：解压文件的密码

**代码如下**

```python
import os
import sys
import time
import zipfile


# 接收待压缩文件路径并解压到指定位置
def multi_compress(folder_list, zippath):
    for dire in folder_list:
        zip_dir(dire, zippath)
    unZip(zippath + add_time(), zippath)


# 压缩文件
def zip_dir(dire, zippath):
    filelist = []
    if os.path.isfile(dire):
        filelist.append(dire)
    else:
        for root, dir_list, filename in os.walk(dire):
            for name in filename:
                filelist.append(os.path.join(root, name))

    zipFile = zipfile.ZipFile(zippath + add_time(), 'a')
    for zip_file in filelist:
        zipFile.write(zip_file, remove_path(dire, zip_file))
    zipFile.close()


# 移除压缩文件多余目录前缀
def remove_path(dirpath, zippath):
    d_list = dirpath.split(os.sep)
    z_list = zippath.split(os.sep)
    length = len(z_list) - len(d_list) + 1
    z_path = z_list[-length:]
    zip_name = os.sep.join(z_path)
    return zip_name


# 添加压缩时间信息
def add_time():
    return time.strftime('%Y%m%d')


# 解压文件
def unZip(filepath, unzipPath):
    zf = zipfile.ZipFile(filepath)
    zf.extractall(unzipPath)
    zf.close()


if __name__ == '__main__':
    back_folder = sys.argv[1:len(sys.argv)-1]
    zippath = sys.argv[-1]
    multi_compress(back_folder, zippath)
```