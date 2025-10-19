#!/usr/bin/env python3
"""
博客封面图生成脚本

功能：
- 根据文章标题读取博客内容（目录结构：/content/blog/TITLE/index.md）
- 调用火山引擎豆包API提炼适合AI绘图的描述
- 调用文生图API生成封面图片
- 将图片保存到博客文章目录下

依赖安装：
  pip install requests

环境变量设置：
  export DOUBAO_API_KEY=your_api_key

使用示例：
  python generate_cover_image.py "astro博客迁移"
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Optional, Tuple
from urllib.parse import urlparse

import requests


# API配置常量
ARK_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
TEXT_MODEL = "doubao-seed-1-6-251015"
IMAGE_MODEL = "doubao-seedream-3-0-t2i-250415"
IMAGE_SIZE = "1024x1024"

# 获取API密钥
DOUBAO_API_KEY = os.getenv("DOUBAO_API_KEY")
if not DOUBAO_API_KEY:
    print("错误：未找到环境变量 DOUBAO_API_KEY")
    print("请设置环境变量：export DOUBAO_API_KEY=your_api_key")
    sys.exit(1)


def find_article_path(article_title: str) -> Optional[Path]:
    """
    根据文章标题查找对应的文章路径
    
    Args:
        article_title: 文章标题
        
    Returns:
        文章路径，如果未找到返回None
    """
    blog_dir = Path("src/content/blog")
    
    if not blog_dir.exists():
        print(f"错误：博客目录 {blog_dir} 不存在")
        return None
    
    # 查找包含文章标题的目录
    for item in blog_dir.iterdir():
        if item.is_dir() and article_title in item.name:
            index_file = item / "index.md"
            if index_file.exists():
                return index_file
    
    # 如果没有找到，尝试查找直接匹配的目录
    potential_dirs = [d for d in blog_dir.iterdir() 
                     if d.is_dir() and article_title.lower() in d.name.lower()]
    
    if potential_dirs:
        index_file = potential_dirs[0] / "index.md"
        if index_file.exists():
            return index_file
    
    return None


def read_article_content(article_title: str) -> str:
    """
    读取文章内容
    
    Args:
        article_title: 文章标题
        
    Returns:
        文章内容字符串
    """
    article_path = find_article_path(article_title)
    
    if not article_path:
        raise FileNotFoundError(f"未找到文章: {article_title}")
    
    print(f"找到文章文件: {article_path}")
    
    try:
        with open(article_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 移除frontmatter（---之间的内容）
        content = re.sub(r'^---.*?---\s*', '', content, flags=re.DOTALL)
        
        # 移除过多的空行
        content = re.sub(r'\n\s*\n', '\n\n', content)
        
        return content.strip()
    
    except Exception as e:
        raise Exception(f"读取文章失败: {e}")


def generate_description(content: str) -> str:
    """
    调用文本API生成适合AI绘图的描述
    
    Args:
        content: 文章内容
        
    Returns:
        生成的图片描述
    """
    # 构建prompt
    system_prompt = """- Role: 情绪叙事与视觉转化专家
- Background: 用户需要将博客内容提炼为一个适合AI文生图的总结描述，用于生成文章封面图。用户希望更多地关注情绪流，而不是具体的文本内容，同时保留文章的主题、情绪和象征性元素，让模型有画面感，兼顾一种叙事氛围。
- Profile: 你是一位情绪叙事与视觉转化专家，擅长从文字中捕捉情绪流动，并将其转化为具有强烈视觉冲击力和叙事氛围的描述。你对情绪的细微变化有着敏锐的感知能力，能够将抽象的情绪转化为具体的画面，赋予文字以生动的视觉形象。
- Skills: 你具备情绪捕捉、叙事构建、视觉转化和画面感营造的综合能力，能够将博客的情绪流转化为富有画面感和叙事氛围的描述，同时确保其与文章主题高度契合。
- Goals: 从博客内容的情绪流中提炼关键信息，生成一个适合AI文生图的总结描述，保留文章主题、情绪和象征性元素，同时赋予其画面感和叙事氛围。
- Constrains: 描述应简洁明了，富有画面感和叙事氛围，避免过于具体的内容细节，专注于情绪的传达，确保AI模型能够准确理解和生成封面图。
- 风格：根据内容，自动选择莫奈风、像素风、伦勃朗、巴洛克风格
- OutputFormat: 文字描述，适合AI文生图模型输入。
- Workflow:
  1. 仔细阅读博客内容，捕捉整体的情绪流动和氛围。
  2. 提炼与情绪相关的象征性元素和主题，转化为具有画面感的描述。
  3. 确保描述简洁明了，专注于情绪的传达，避免具体细节。
- Examples:
  - 例子1：博客主题是“孤独的旅行者在荒漠中的自我探索”，描述为：“在无垠的荒漠中，孤独的情绪如沙尘般弥漫，落日的余晖洒在旅行者的身上，他的身影被拉得很长，仿佛在与内心的孤独对话，每一步都显得沉重而坚定。”
  - 例子2：博客主题是“春天的希望与新生”，描述为：“春日的暖阳穿透薄雾，洒在湿润的土地上，新生的绿意在空气中弥漫，希望的气息如微风般轻拂，一只蝴蝶在光影中舞动，象征着生命的复苏与希望。”
  - 例子3：博客主题是“城市的喧嚣与孤独”，描述为：“城市的灯火在夜空中闪烁，喧嚣声如潮水般涌动，但在人群中，孤独的情绪如影随形，一位身影在霓虹灯下显得格外渺小，眼神中透露出对宁静的渴望。”
文章内容：
{文章内容}
"""
    
    user_prompt = f"文章内容：\n{content[:1500]}..."  # 限制长度避免超出token限制
    
    # 构建请求
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DOUBAO_API_KEY}"
    }
    
    data = {
        "model": TEXT_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "max_tokens": 512,
        "temperature": 0.8
    }
    
    print("正在生成图片描述...")
    
    try:
        response = requests.post(
            f"{ARK_BASE_URL}/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        response.raise_for_status()
        result = response.json()
        
        if "choices" in result and len(result["choices"]) > 0:
            description = result["choices"][0]["message"]["content"].strip()
            print(f"生成的描述: {description}")
            return description
        else:
            raise Exception("API响应格式异常")
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"文本API调用失败: {e}")
    except json.JSONDecodeError as e:
        raise Exception(f"解析API响应失败: {e}")


def generate_image(description: str) -> str:
    """
    调用图像API生成图片
    
    Args:
        description: 图片描述
        
    Returns:
        图片URL
    """
    headers = {
        "Content-Type": "application/json", 
        "Authorization": f"Bearer {DOUBAO_API_KEY}"
    }
    
    data = {
        "model": IMAGE_MODEL,
        "prompt": description,
        "response_format": "url",
        "size": IMAGE_SIZE,
        "guidance_scale": 2.5,
        "watermark": False
    }
    
    print("正在生成封面图片...")
    
    try:
        response = requests.post(
            f"{ARK_BASE_URL}/images/generations",
            headers=headers,
            json=data,
            timeout=60
        )
        
        response.raise_for_status()
        result = response.json()
        
        if "data" in result and len(result["data"]) > 0:
            image_url = result["data"][0]["url"]
            print(f"图片生成成功: {image_url}")
            return image_url
        else:
            raise Exception("API响应格式异常")
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"图像API调用失败: {e}")
    except json.JSONDecodeError as e:
        raise Exception(f"解析API响应失败: {e}")


def download_and_save_image(image_url: str, article_title: str) -> bool:
    """
    下载图片并保存到文章目录
    
    Args:
        image_url: 图片URL
        article_title: 文章标题
        
    Returns:
        是否保存成功
    """
    # 找到文章目录
    article_path = find_article_path(article_title)
    if not article_path:
        print(f"错误：未找到文章目录")
        return False
    
    # 确定保存路径
    article_dir = article_path.parent
    
    # 从URL获取文件扩展名，默认使用jpg
    parsed_url = urlparse(image_url)
    file_extension = os.path.splitext(parsed_url.path)[1] or '.jpg'
    save_path = article_dir / f"cover{file_extension}"
    
    print(f"正在下载图片到: {save_path}")
    
    try:
        # 下载图片
        response = requests.get(image_url, timeout=30)
        response.raise_for_status()
        
        # 保存文件
        with open(save_path, 'wb') as f:
            f.write(response.content)
        
        print(f"✅ 封面图片保存成功: {save_path}")
        print(f"📝 建议在文章frontmatter中添加: heroImage: {{ src: './cover{file_extension}', color: '#9698C1' }}")
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"下载图片失败: {e}")
        return False
    except Exception as e:
        print(f"保存图片失败: {e}")
        return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='博客封面图生成工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python generate_cover_image.py "astro博客迁移"
  
环境变量:
  ARK_API_KEY - 火山引擎API密钥
        """
    )
    
    # 必需参数
    parser.add_argument('title', help='文章标题（目录名称的一部分）')
    
    args = parser.parse_args()
    
    # 参数验证
    if not args.title.strip():
        print("错误：文章标题不能为空")
        sys.exit(1)
    
    title = args.title.strip()
    
    print(f"🎨 开始为文章生成封面图: {title}")
    print("=" * 50)
    
    try:
        # 步骤1：读取文章内容
        print("📖 步骤1: 读取文章内容...")
        content = read_article_content(title)
        if len(content) < 100:
            print("⚠️  警告：文章内容较短，可能影响描述生成质量")
        
        # 步骤2：生成图片描述
        print("\n🤖 步骤2: 生成图片描述...")
        description = generate_description(content)
        
        # 步骤3：生成图片
        print("\n🎨 步骤3: 生成封面图片...")
        image_url = generate_image(description)
        
        # 步骤4：下载保存图片
        print("\n💾 步骤4: 下载并保存图片...")
        success = download_and_save_image(image_url, title)
        
        if success:
            print("\n🎉 封面图生成完成！")
        else:
            print("\n❌ 封面图生成失败！")
            sys.exit(1)
    
    except Exception as e:
        print(f"\n❌ 处理过程中发生错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
