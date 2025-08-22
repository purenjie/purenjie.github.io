#!/usr/bin/env python3
"""
文本预处理工具

功能：
- 移除Markdown frontmatter
- 清理HTML标签
- 文本标准化和清理
- 中文文本预处理
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import yaml


class TextProcessor:
    """文本预处理工具类"""
    
    def __init__(self):
        """初始化文本处理器"""
        # 常见的中文标点符号
        self.chinese_punctuation = '，。！？；：""''（）【】《》、'
        # 英文标点符号
        self.english_punctuation = ',.!?;:"\'()[]<>/'
        
    def remove_frontmatter(self, content: str) -> Tuple[str, Optional[Dict]]:
        """
        移除Markdown frontmatter并提取元数据
        
        Args:
            content: 原始文本内容
            
        Returns:
            (清理后的内容, 元数据字典)
        """
        # 匹配frontmatter模式
        frontmatter_pattern = r'^---\s*\n(.*?)\n---\s*\n'
        match = re.search(frontmatter_pattern, content, re.DOTALL)
        
        if match:
            try:
                # 解析YAML格式的frontmatter
                frontmatter_text = match.group(1)
                metadata = yaml.safe_load(frontmatter_text)
                
                # 移除frontmatter
                cleaned_content = re.sub(frontmatter_pattern, '', content, flags=re.DOTALL)
                return cleaned_content.strip(), metadata
            except yaml.YAMLError:
                # 如果YAML解析失败，只移除frontmatter
                cleaned_content = re.sub(frontmatter_pattern, '', content, flags=re.DOTALL)
                return cleaned_content.strip(), None
        else:
            return content.strip(), None
    
    def clean_html_tags(self, content: str) -> str:
        """
        清理HTML标签
        
        Args:
            content: 包含HTML标签的文本
            
        Returns:
            清理后的纯文本
        """
        # 移除HTML标签
        content = re.sub(r'<[^>]+>', '', content)
        # 移除HTML实体
        content = re.sub(r'&[a-zA-Z]+;', '', content)
        return content
    
    def clean_markdown_formatting(self, content: str) -> str:
        """
        清理Markdown格式标记
        
        Args:
            content: 包含Markdown格式的文本
            
        Returns:
            清理后的纯文本
        """
        # 移除标题标记
        content = re.sub(r'^#{1,6}\s+', '', content, flags=re.MULTILINE)
        # 移除粗体和斜体标记
        content = re.sub(r'\*\*(.*?)\*\*', r'\1', content)
        content = re.sub(r'\*(.*?)\*', r'\1', content)
        # 移除代码块标记
        content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
        content = re.sub(r'`([^`]+)`', r'\1', content)
        # 移除链接标记
        content = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', content)
        # 移除图片标记
        content = re.sub(r'!\[([^\]]*)\]\([^)]+\)', '', content)
        # 移除引用标记
        content = re.sub(r'^>\s+', '', content, flags=re.MULTILINE)
        # 移除列表标记
        content = re.sub(r'^[\s]*[-*+]\s+', '', content, flags=re.MULTILINE)
        content = re.sub(r'^[\s]*\d+\.\s+', '', content, flags=re.MULTILINE)
        
        return content
    
    def normalize_text(self, content: str) -> str:
        """
        文本标准化
        
        Args:
            content: 原始文本
            
        Returns:
            标准化后的文本
        """
        # 统一换行符
        content = content.replace('\r\n', '\n').replace('\r', '\n')
        
        # 移除多余的空行
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        
        # 移除行首行尾空白
        content = re.sub(r'^\s+|\s+$', '', content, flags=re.MULTILINE)
        
        # 统一中英文标点符号间距
        content = re.sub(r'([a-zA-Z])([，。！？；：])', r'\1 \2', content)
        content = re.sub(r'([，。！？；：])([a-zA-Z])', r'\1 \2', content)
        
        return content
    
    def extract_paragraphs(self, content: str) -> List[str]:
        """
        提取段落
        
        Args:
            content: 文本内容
            
        Returns:
            段落列表
        """
        # 按双换行符分割段落
        paragraphs = re.split(r'\n\s*\n', content)
        # 清理每个段落
        cleaned_paragraphs = []
        for para in paragraphs:
            para = para.strip()
            if para and len(para) > 10:  # 过滤太短的段落
                cleaned_paragraphs.append(para)
        
        return cleaned_paragraphs
    
    def extract_sentences(self, content: str) -> List[str]:
        """
        提取句子
        
        Args:
            content: 文本内容
            
        Returns:
            句子列表
        """
        # 中文句子分割（考虑中英文混合）
        sentence_pattern = r'[^。！？.!?]*[。！？.!?]'
        sentences = re.findall(sentence_pattern, content)
        
        # 清理句子
        cleaned_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and len(sentence) > 5:  # 过滤太短的句子
                cleaned_sentences.append(sentence)
        
        return cleaned_sentences
    
    def process_article(self, content: str) -> Tuple[str, Optional[Dict], List[str], List[str]]:
        """
        完整的文章预处理流程
        
        Args:
            content: 原始文章内容
            
        Returns:
            (清理后的内容, 元数据, 段落列表, 句子列表)
        """
        # 1. 移除frontmatter
        content, metadata = self.remove_frontmatter(content)
        
        # 2. 清理HTML标签
        content = self.clean_html_tags(content)
        
        # 3. 清理Markdown格式
        content = self.clean_markdown_formatting(content)
        
        # 4. 文本标准化
        content = self.normalize_text(content)
        
        # 5. 提取段落和句子
        paragraphs = self.extract_paragraphs(content)
        sentences = self.extract_sentences(content)
        
        return content, metadata, paragraphs, sentences
    
    def get_text_statistics(self, content: str) -> Dict:
        """
        获取基础文本统计信息
        
        Args:
            content: 清理后的文本内容
            
        Returns:
            统计信息字典
        """
        paragraphs = self.extract_paragraphs(content)
        sentences = self.extract_sentences(content)
        
        # 计算字符数（去除空格和换行）
        char_count = len(re.sub(r'\s', '', content))
        # 计算词数（简单按空格分割，后续可用jieba优化）
        word_count = len(content.split())
        
        stats = {
            'total_characters': char_count,
            'total_words': word_count,
            'paragraph_count': len(paragraphs),
            'sentence_count': len(sentences),
            'avg_paragraph_length': char_count / len(paragraphs) if paragraphs else 0,
            'avg_sentence_length': char_count / len(sentences) if sentences else 0,
            'avg_words_per_sentence': word_count / len(sentences) if sentences else 0
        }
        
        return stats
