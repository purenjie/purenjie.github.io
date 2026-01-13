#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
字体子集化脚本
使用 fonttools 提取指定字符集，减小字体文件体积
"""

import sys
from pathlib import Path
from fontTools import subset

def create_font_subset(input_font, output_font, chars_file):
    """
    创建字体子集

    Args:
        input_font: 输入字体文件路径
        output_font: 输出字体文件路径
        chars_file: 字符列表文件路径

    Reason: 使用 fonttools.subset 进行字体子集化，保留指定字符
    """
    print(f"📖 读取字符列表: {chars_file}")

    # 读取字符列表
    with open(chars_file, 'r', encoding='utf-8') as f:
        chars = f.read()

    print(f"✅ 加载了 {len(chars)} 个字符")
    print(f"📝 输入字体: {input_font}")
    print(f"💾 输出字体: {output_font}")

    # 创建子集化选项
    options = subset.Options()

    # Reason: 保留字体提示信息，提升渲染质量
    options.hinting = True

    # Reason: 保留字形名称，便于调试
    options.glyph_names = True

    # Reason: 保留推荐的表，确保字体功能完整
    options.recommended_glyphs = True

    # Reason: 保留布局特性，支持复杂文本渲染
    options.layout_features = ['*']

    # Reason: 去除未使用的表，减小文件体积
    options.drop_tables = ['DSIG']

    # 创建 Subsetter 对象
    font = subset.load_font(input_font, options)
    subsetter = subset.Subsetter(options=options)

    # 添加字符到子集
    subsetter.populate(text=chars)

    print("🔨 开始生成字体子集...")

    # 执行子集化
    subsetter.subset(font)

    # 保存子集字体
    subset.save_font(font, output_font, options)

    print("✅ 字体子集化完成！")

    # 显示文件大小对比
    input_size = Path(input_font).stat().st_size / (1024 * 1024)
    output_size = Path(output_font).stat().st_size / (1024 * 1024)
    reduction = (1 - output_size / input_size) * 100

    print(f"\n📊 文件大小对比:")
    print(f"  原始文件: {input_size:.2f} MB")
    print(f"  子集文件: {output_size:.2f} MB")
    print(f"  减小: {reduction:.1f}%")

def main():
    """
    主函数：执行字体子集化
    """
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    # 输入输出路径
    input_font = project_root / 'public' / 'fonts' / '仓耳今楷04-W04.woff2'
    output_font = project_root / 'public' / 'fonts' / '仓耳今楷04-W04-subset.woff2'
    chars_file = script_dir / 'chinese_chars.txt'

    # 检查文件是否存在
    if not input_font.exists():
        print(f"❌ 错误: 输入字体文件不存在: {input_font}")
        sys.exit(1)

    if not chars_file.exists():
        print(f"❌ 错误: 字符列表文件不存在: {chars_file}")
        print("请先运行 extract_chinese_chars.py 生成字符列表")
        sys.exit(1)

    # 执行子集化
    create_font_subset(str(input_font), str(output_font), str(chars_file))

if __name__ == '__main__':
    main()
