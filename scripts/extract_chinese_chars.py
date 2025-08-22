#!/usr/bin/env python3
import os
import re
import glob

def extract_chinese_chars(directory):
    """提取目录下所有markdown文件中的汉字"""
    chinese_chars = set()
    
    # 汉字Unicode范围
    chinese_pattern = re.compile(r'[\u4e00-\u9fff]+')
    
    # 查找所有markdown文件
    md_files = glob.glob(os.path.join(directory, '**/*.md'), recursive=True)
    
    for file_path in md_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                matches = chinese_pattern.findall(content)
                for match in matches:
                    chinese_chars.update(match)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    
    return chinese_chars

if __name__ == "__main__":
    # 提取博客中的汉字
    chars = extract_chinese_chars('src/content/blog')
    
    # 添加常用标点符号
    common_punctuation = '，。！？；：""''（）【】《》、·—…'
    chars.update(common_punctuation)
    
    # 转换为字符串并保存
    char_string = ''.join(sorted(chars))
    
    with open('blog_chinese_chars.txt', 'w', encoding='utf-8') as f:
        f.write(char_string)
    
    print(f"提取了 {len(chars)} 个汉字和标点符号")
    print(f"已保存到 blog_chinese_chars.txt")
    print(f"前20个字符: {char_string[:20]}")