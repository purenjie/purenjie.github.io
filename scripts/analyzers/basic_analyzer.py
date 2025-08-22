#!/usr/bin/env python3
"""
基础文本统计分析器

功能：
- 词频统计和词汇多样性分析
- 句子复杂度和结构分析
- 情感词汇识别和统计
- 主题关键词提取
- 写作模式分析
"""

import re
import jieba
import jieba.analyse
from collections import Counter, defaultdict
from typing import Dict, List, Tuple, Any
from datetime import datetime


class BasicAnalyzer:
    """基础文本统计分析器"""
    
    def __init__(self):
        """初始化分析器"""
        # 情感词汇词典（简化版，实际使用时可扩展）
        self.emotion_words = {
            'positive': [
                '开心', '快乐', '高兴', '兴奋', '激动', '满意', '满足', '幸福', '温暖',
                '感动', '感激', '感谢', '喜欢', '爱', '美好', '精彩', '优秀', '成功',
                '进步', '成长', '希望', '期待', '憧憬', '梦想', '理想', '目标'
            ],
            'negative': [
                '难过', '伤心', '痛苦', '悲伤', '沮丧', '失望', '绝望', '愤怒', '生气',
                '焦虑', '担心', '害怕', '恐惧', '紧张', '压力', '疲惫', '累', '痛苦',
                '失败', '挫折', '困难', '问题', '麻烦', '困扰', '纠结', '犹豫'
            ],
            'neutral': [
                '思考', '考虑', '分析', '研究', '学习', '工作', '生活', '经历', '体验',
                '感受', '感觉', '认为', '觉得', '发现', '了解', '知道', '明白', '理解'
            ]
        }
        
        # 技术词汇词典
        self.tech_words = [
            '编程', '代码', '开发', '技术', '算法', '数据结构', 'API', '框架', '库',
            '数据库', '服务器', '前端', '后端', '全栈', '部署', '测试', '调试', '优化',
            '性能', '安全', '架构', '设计模式', '版本控制', 'Git', 'Docker', '云服务'
        ]
        
        # 生活词汇词典
        self.life_words = [
            '生活', '工作', '学习', '读书', '旅行', '美食', '运动', '健康', '家庭',
            '朋友', '爱情', '感情', '心情', '情绪', '时间', '计划', '目标', '梦想',
            '成长', '改变', '选择', '决定', '努力', '坚持', '成功', '失败', '经验'
        ]
        
        # 初始化jieba
        jieba.initialize()
        
    def analyze_vocabulary(self, text: str) -> Dict[str, Any]:
        """
        词汇分析
        
        Args:
            text: 文本内容
            
        Returns:
            词汇分析结果
        """
        # 使用jieba进行中文分词
        words = jieba.lcut(text)
        
        # 过滤停用词和标点符号
        filtered_words = []
        for word in words:
            word = word.strip()
            if (word and 
                len(word) > 1 and 
                not re.match(r'^[^\u4e00-\u9fa5a-zA-Z0-9]+$', word)):
                filtered_words.append(word)
        
        # 词频统计
        word_freq = Counter(filtered_words)
        top_words = word_freq.most_common(20)
        
        # 词汇多样性计算（Type-Token Ratio）
        unique_words = len(set(filtered_words))
        total_words = len(filtered_words)
        ttr = unique_words / total_words if total_words > 0 else 0
        
        # 词汇长度分布
        word_lengths = [len(word) for word in filtered_words]
        avg_word_length = sum(word_lengths) / len(word_lengths) if word_lengths else 0
        
        return {
            'total_words': total_words,
            'unique_words': unique_words,
            'type_token_ratio': round(ttr, 3),
            'avg_word_length': round(avg_word_length, 2),
            'top_words': top_words,
            'word_length_distribution': Counter(word_lengths)
        }
    
    def analyze_sentences(self, sentences: List[str]) -> Dict[str, Any]:
        """
        句子分析
        
        Args:
            sentences: 句子列表
            
        Returns:
            句子分析结果
        """
        if not sentences:
            return {}
        
        # 句子长度统计
        sentence_lengths = [len(sentence) for sentence in sentences]
        avg_sentence_length = sum(sentence_lengths) / len(sentence_lengths)
        
        # 句子复杂度分析
        complex_sentences = 0
        simple_sentences = 0
        
        for sentence in sentences:
            # 检查是否包含从句标记
            if any(marker in sentence for marker in ['因为', '所以', '虽然', '但是', '如果', '那么', '当', '时']):
                complex_sentences += 1
            else:
                simple_sentences += 1
        
        # 句子类型分布
        sentence_types = {
            'declarative': 0,  # 陈述句
            'interrogative': 0,  # 疑问句
            'exclamatory': 0,   # 感叹句
            'imperative': 0     # 祈使句
        }
        
        for sentence in sentences:
            if sentence.endswith('？'):
                sentence_types['interrogative'] += 1
            elif sentence.endswith('！'):
                sentence_types['exclamatory'] += 1
            elif sentence.endswith('。'):
                sentence_types['declarative'] += 1
            else:
                sentence_types['declarative'] += 1
        
        return {
            'total_sentences': len(sentences),
            'avg_sentence_length': round(avg_sentence_length, 2),
            'sentence_length_distribution': {
                'short': len([l for l in sentence_lengths if l <= 20]),
                'medium': len([l for l in sentence_lengths if 20 < l <= 50]),
                'long': len([l for l in sentence_lengths if l > 50])
            },
            'complexity': {
                'simple': simple_sentences,
                'complex': complex_sentences,
                'complexity_ratio': round(complex_sentences / len(sentences), 3)
            },
            'sentence_types': sentence_types
        }
    
    def analyze_emotions(self, text: str) -> Dict[str, Any]:
        """
        情感分析
        
        Args:
            text: 文本内容
            
        Returns:
            情感分析结果
        """
        words = jieba.lcut(text)
        
        emotion_counts = {
            'positive': 0,
            'negative': 0,
            'neutral': 0
        }
        
        emotion_word_details = {
            'positive': [],
            'negative': [],
            'neutral': []
        }
        
        # 统计情感词汇
        for word in words:
            for emotion_type, emotion_list in self.emotion_words.items():
                if word in emotion_list:
                    emotion_counts[emotion_type] += 1
                    emotion_word_details[emotion_type].append(word)
        
        # 计算情感比例
        total_emotion_words = sum(emotion_counts.values())
        if total_emotion_words > 0:
            emotion_ratios = {
                emotion: round(count / total_emotion_words, 3)
                for emotion, count in emotion_counts.items()
            }
        else:
            emotion_ratios = {'positive': 0, 'negative': 0, 'neutral': 0}
        
        # 判断整体情感倾向
        if emotion_counts['positive'] > emotion_counts['negative']:
            overall_sentiment = 'positive'
        elif emotion_counts['negative'] > emotion_counts['positive']:
            overall_sentiment = 'negative'
        else:
            overall_sentiment = 'neutral'
        
        return {
            'emotion_counts': emotion_counts,
            'emotion_ratios': emotion_ratios,
            'overall_sentiment': overall_sentiment,
            'emotion_word_details': emotion_word_details,
            'total_emotion_words': total_emotion_words
        }
    
    def analyze_topics(self, text: str) -> Dict[str, Any]:
        """
        主题分析
        
        Args:
            text: 文本内容
            
        Returns:
            主题分析结果
        """
        # 使用jieba提取关键词
        keywords = jieba.analyse.extract_tags(text, topK=20, withWeight=True)
        
        # 主题分类统计
        topic_counts = {
            'technology': 0,
            'life': 0,
            'reading': 0,
            'summary': 0,
            'other': 0
        }
        
        topic_words = {
            'technology': [],
            'life': [],
            'reading': [],
            'summary': [],
            'other': []
        }
        
        # 根据关键词分类主题
        for word, weight in keywords:
            if any(tech_word in word for tech_word in self.tech_words):
                topic_counts['technology'] += 1
                topic_words['technology'].append(word)
            elif any(life_word in word for life_word in self.life_words):
                topic_counts['life'] += 1
                topic_words['life'].append(word)
            elif any(reading_word in word for reading_word in ['读书', '阅读', '书籍', '作者', '读后感']):
                topic_counts['reading'] += 1
                topic_words['reading'].append(word)
            elif any(summary_word in word for summary_word in ['总结', '回顾', '年度', '计划', '目标']):
                topic_counts['summary'] += 1
                topic_words['summary'].append(word)
            else:
                topic_counts['other'] += 1
                topic_words['other'].append(word)
        
        # 确定主要主题
        main_topic = max(topic_counts, key=topic_counts.get)
        
        return {
            'main_topic': main_topic,
            'topic_counts': topic_counts,
            'topic_words': topic_words,
            'keywords': keywords[:10],  # 只返回前10个关键词
            'topic_distribution': {
                topic: round(count / sum(topic_counts.values()), 3)
                for topic, count in topic_counts.items()
            }
        }
    
    def analyze_writing_patterns(self, text: str, paragraphs: List[str]) -> Dict[str, Any]:
        """
        写作模式分析
        
        Args:
            text: 文本内容
            paragraphs: 段落列表
            
        Returns:
            写作模式分析结果
        """
        # 段落长度分析
        para_lengths = [len(para) for para in paragraphs]
        avg_para_length = sum(para_lengths) / len(para_lengths) if para_lengths else 0
        
        # 开头和结尾模式分析
        opening_patterns = []
        closing_patterns = []
        
        if paragraphs:
            # 分析开头段落
            first_para = paragraphs[0]
            if len(first_para) > 50:
                opening_patterns.append('detailed_intro')
            elif '？' in first_para:
                opening_patterns.append('question_start')
            elif any(word in first_para for word in ['今天', '昨天', '最近', '现在']):
                opening_patterns.append('time_based_start')
            else:
                opening_patterns.append('direct_start')
            
            # 分析结尾段落
            last_para = paragraphs[-1]
            if '？' in last_para:
                closing_patterns.append('question_end')
            elif any(word in last_para for word in ['希望', '期待', '相信', '加油']):
                closing_patterns.append('hopeful_end')
            elif any(word in last_para for word in ['总结', '总之', '总的来说']):
                closing_patterns.append('summary_end')
            else:
                closing_patterns.append('natural_end')
        
        # 引用和强调模式
        quote_count = text.count('"') // 2 + text.count('"') // 2
        emphasis_count = text.count('**') // 2 + text.count('*') // 2
        
        # 数字和数据的引用
        number_pattern = r'\d+'
        numbers = re.findall(number_pattern, text)
        
        return {
            'paragraph_analysis': {
                'total_paragraphs': len(paragraphs),
                'avg_paragraph_length': round(avg_para_length, 2),
                'paragraph_length_distribution': {
                    'short': len([l for l in para_lengths if l <= 100]),
                    'medium': len([l for l in para_lengths if 100 < l <= 300]),
                    'long': len([l for l in para_lengths if l > 300])
                }
            },
            'opening_patterns': opening_patterns,
            'closing_patterns': closing_patterns,
            'writing_techniques': {
                'quotes': quote_count,
                'emphasis': emphasis_count,
                'numbers': len(numbers),
                'has_code_blocks': '```' in text,
                'has_images': '![' in text
            }
        }
    
    def comprehensive_analysis(self, text: str, sentences: List[str], 
                             paragraphs: List[str]) -> Dict[str, Any]:
        """
        综合分析
        
        Args:
            text: 清理后的文本内容
            sentences: 句子列表
            paragraphs: 段落列表
            
        Returns:
            综合分析结果
        """
        results = {}
        
        # 词汇分析
        results['vocabulary'] = self.analyze_vocabulary(text)
        
        # 句子分析
        results['sentences'] = self.analyze_sentences(sentences)
        
        # 情感分析
        results['emotions'] = self.analyze_emotions(text)
        
        # 主题分析
        results['topics'] = self.analyze_topics(text)
        
        # 写作模式分析
        results['writing_patterns'] = self.analyze_writing_patterns(text, paragraphs)
        
        # 计算写作风格评分
        results['style_scores'] = self._calculate_style_scores(results)
        
        return results
    
    def _calculate_style_scores(self, analysis_results: Dict) -> Dict[str, float]:
        """
        计算写作风格评分
        
        Args:
            analysis_results: 分析结果
            
        Returns:
            风格评分
        """
        scores = {}
        
        # 词汇丰富度评分 (0-10)
        ttr = analysis_results['vocabulary']['type_token_ratio']
        scores['vocabulary_richness'] = min(10, ttr * 20)
        
        # 句子复杂度评分 (0-10)
        complexity_ratio = analysis_results['sentences'].get('complexity', {}).get('complexity_ratio', 0)
        scores['sentence_complexity'] = min(10, complexity_ratio * 20)
        
        # 情感表达评分 (0-10)
        emotion_words = analysis_results['emotions']['total_emotion_words']
        total_words = analysis_results['vocabulary']['total_words']
        if total_words > 0:
            emotion_ratio = emotion_words / total_words
            scores['emotional_expression'] = min(10, emotion_ratio * 100)
        else:
            scores['emotional_expression'] = 0
        
        # 结构组织评分 (0-10)
        para_count = analysis_results['writing_patterns']['paragraph_analysis']['total_paragraphs']
        if para_count > 0:
            avg_para_length = analysis_results['writing_patterns']['paragraph_analysis']['avg_paragraph_length']
            # 段落长度适中得分高
            if 100 <= avg_para_length <= 300:
                scores['structure_organization'] = 8
            elif 50 <= avg_para_length <= 500:
                scores['structure_organization'] = 6
            else:
                scores['structure_organization'] = 4
        else:
            scores['structure_organization'] = 5
        
        # 总体风格评分
        scores['overall_style'] = sum(scores.values()) / len(scores)
        
        return {k: round(v, 1) for k, v in scores.items()}
