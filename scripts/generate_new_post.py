#!/usr/bin/env python3
"""
博客文章生成脚本

功能：
- 支持两种模式：单文件模式和目录模式
- 自动生成前置元数据
- 随机莫兰迪配色
- 自动填充当前日期
"""

import argparse
import datetime
import os
import random
import sys

# 莫兰迪配色数组
MORANDI_COLORS = [
    '#64574D',  # 温暖棕色
    '#D58388',  # 粉红色
    '#9698C1',  # 淡紫色
    '#B5A88F',  # 卡其色
    '#A8B5A0',  # 薄荷绿
    '#C9A96E',  # 沙色
    '#8B9BB8',  # 雾霾蓝
    '#C4A484',  # 驼色
    '#A6978A',  # 灰褐色
    '#B8A5A0',  # 玫瑰灰
    '#9DB5A0',  # 鼠尾草绿
    '#C8B5A6',  # 米色
]


def generate_morandi_color():
    """随机生成莫兰迪配色"""
    return random.choice(MORANDI_COLORS)


def get_today_date():
    """获取今天的日期，格式为 YYYY-MM-DD"""
    return datetime.date.today().strftime('%Y-%m-%d')


def generate_frontmatter(title):
    """生成文章前置元数据"""
    color = generate_morandi_color()
    today = get_today_date()
    
    frontmatter = f"""---
title: {title}
publishDate: {today}
description: '待补充'
tags:
  - 未分类
"""
    frontmatter += f"""
heroImage: {{ src: './thumbnail.jpg', color: '{color}' }}
heroImage:
  {{ src: 'http://static.simpledesktops.com/uploads/desktops/2017/06/02/bg-wallpaper.png.625x385_q100.png', inferSize: true, color: '{color}'  }}
language: 'Chinese'
---

"""
    return frontmatter


def create_single_file(title):
    """创建单文件模式的博客文章"""
    # 文件路径
    blog_dir = "src/content/blog"
    file_path = os.path.join(blog_dir, f"{get_today_date()}-{title}.md")
    
    # 检查文件是否已存在
    if os.path.exists(file_path):
        print(f"错误：文件 {file_path} 已存在")
        return False
    
    # 生成内容
    content = generate_frontmatter(title)
    content += f"# {title}\n\n文章内容待补充...\n"
    
    try:
        # 确保目录存在
        os.makedirs(blog_dir, exist_ok=True)
        
        # 写入文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"成功创建单文件: {file_path}")
        return True
    except Exception as e:
        print(f"创建文件失败: {e}")
        return False


def create_directory_structure(title):
    """创建目录模式的博客文章"""
    # 目录路径
    blog_dir = "src/content/blog"
    article_dir = os.path.join(blog_dir, f"{get_today_date()}-{title}")
    index_path = os.path.join(article_dir, "index.md")
    
    # 检查目录是否已存在
    if os.path.exists(article_dir):
        print(f"错误：目录 {article_dir} 已存在")
        return False
    
    # 生成内容
    content = generate_frontmatter(title)
    content += f"# {title}\n\n文章内容待补充...\n"
    
    try:
        # 创建目录
        os.makedirs(article_dir, exist_ok=True)
        
        # 写入 index.md
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"成功创建目录结构:")
        print(f"  - 目录: {article_dir}")
        print(f"  - 文件: {index_path}")
        print(f"  - 提示: 可在目录中添加 thumbnail.jpg 等资源文件")
        return True
    except Exception as e:
        print(f"创建目录结构失败: {e}")
        return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='博客文章生成工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 创建单文件模式
  python generate_new_post.py "我的新文章" --mode file
  
  # 创建目录模式
  python generate_new_post.py "我的新文章" --mode dir
        """
    )
    
    # 必需参数
    parser.add_argument('title', help='文章标题')
    
    # 可选参数
    parser.add_argument('--mode', choices=['file', 'dir'], default='dir',
                       help='生成模式: file=单文件模式, dir=目录模式 (默认: dir)')
    
    args = parser.parse_args()
    
    # 参数验证
    if not args.title.strip():
        print("错误：文章标题不能为空")
        sys.exit(1)
    
    title = args.title.strip()
    
    print(f"生成博客文章: {title}")
    print(f"模式: {'单文件' if args.mode == 'file' else '目录'}")
    print("-" * 50)
    
    # 执行对应模式的创建函数
    if args.mode == 'file':
        success = create_single_file(title)
    else:
        success = create_directory_structure(title)
    
    if success:
        print("\n✅ 博客文章生成成功!")
    else:
        print("\n❌ 博客文章生成失败!")
        sys.exit(1)


if __name__ == "__main__":
    main()
