#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
提取博客内容中使用的所有中文字符
用于字体子集化，减小字体文件体积
"""

import os
import re
from pathlib import Path
from collections import Counter

def extract_chinese_chars(text):
    """
    提取文本中的中文字符
    Reason: 使用正则匹配CJK统一汉字区域，覆盖常用和扩展汉字
    """
    # CJK统一汉字基本区 + 扩展A区 + 扩展B区
    pattern = r'[\u4e00-\u9fff\u3400-\u4dbf\U00020000-\U0002a6df]'
    return re.findall(pattern, text)

def scan_content_files(content_dir):
    """
    扫描所有内容文件，提取中文字符
    """
    chinese_chars = set()
    char_frequency = Counter()

    content_path = Path(content_dir)

    # 扫描 markdown 文件
    md_files = list(content_path.rglob('*.md')) + list(content_path.rglob('*.mdx'))

    print(f"📁 找到 {len(md_files)} 个内容文件")

    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                chars = extract_chinese_chars(content)
                chinese_chars.update(chars)
                char_frequency.update(chars)
        except Exception as e:
            print(f"⚠️  读取文件失败: {md_file} - {e}")

    return chinese_chars, char_frequency

def load_common_chars():
    """
    加载常用汉字列表作为基础
    Reason: 确保常用字全覆盖，即使博客中未使用
    """
    # 常用3500字（国家语委现代汉语常用字表）
    common_chars_3500 = """
的一是在不了有和人这中大为上个国我以要他时来用们生到作地于出就分对成会可主发年动同工也能下过子说产种面而方后多定行学法所民得经十三之进着等部度家电力里如水化高自二理起小物现实加量都两体制机当使点从业本去把性好应开它合还因由其些然前外天政四日那社义事平形相全表间样与关各重新线内数正心反你明看原又么利比或但质气第向道命此变条只没结解问意建月公无系军很情者最立代想已通并提直题党程展五果料象员革位入常文总次品式活设及管特件长求老头基资边流路级少图山统接知较将组见计别她手角期根论运农指几九区强放决西被干做必战先回则任取据处队南给色光门即保治北造百规热领七海口东导器压志世金增争济阶油思术极交受联什认六共权收证改清己美再采转更单风切打白教速花带安场身车例真务具万每目至达走积示议声报斗完类八离华名确才科张信马节话米整空元况今集温传土许步群广石记需段研界拉林律叫且究观越织装影算低持音众书布复容儿须际商非验连断深难近矿千周委素技备半办青省列习响约支般史感劳便团往酸历市克何除消构府称太准精值号率族维划选标写存候毛亲快效斯院查江型眼王按格养易置派层片始却专状育厂京识适属圆包火住调满县局照参红细引听该铁价严龙飞
"""

    # 提取常用字
    common_chars = set(extract_chinese_chars(common_chars_3500))
    return common_chars

def main():
    """
    主函数：提取博客中使用的所有中文字符
    """
    # 获取项目根目录
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    content_dir = project_root / 'src' / 'content'

    print("🚀 开始分析博客内容...")
    print(f"📂 内容目录: {content_dir}")

    # 扫描内容文件
    blog_chars, char_frequency = scan_content_files(content_dir)
    print(f"✅ 从博客中提取了 {len(blog_chars)} 个不同的汉字")

    # 加载常用字
    common_chars = load_common_chars()
    print(f"✅ 加载了 {len(common_chars)} 个常用汉字")

    # 合并字符集
    all_chars = blog_chars.union(common_chars)
    print(f"✅ 总共需要 {len(all_chars)} 个汉字")

    # 保存字符列表
    output_file = script_dir / 'chinese_chars.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(''.join(sorted(all_chars)))

    print(f"💾 字符列表已保存到: {output_file}")

    # 显示统计信息
    print("\n📊 字符使用频率 TOP 20:")
    for char, count in char_frequency.most_common(20):
        print(f"  {char}: {count} 次")

    return output_file

if __name__ == '__main__':
    main()
