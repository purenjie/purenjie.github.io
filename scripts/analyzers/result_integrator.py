#!/usr/bin/env python3
"""
结果整合器

功能：
- 整合基础统计分析和AI分析结果
- 生成结构化的分析报告
- 计算综合评分和趋势分析
- 格式化输出数据
"""

import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from collections import defaultdict


class ResultIntegrator:
    """结果整合器"""
    
    def __init__(self):
        """初始化结果整合器"""
        self.integrated_results = {}
    
    def integrate_analysis_results(self, basic_analysis: Dict, ai_analysis: Dict, 
                                 article_metadata: List[Dict]) -> Dict[str, Any]:
        """
        整合分析结果
        
        Args:
            basic_analysis: 基础统计分析结果
            ai_analysis: AI分析结果
            article_metadata: 文章元数据列表
            
        Returns:
            整合后的分析报告
        """
        print("🔗 正在整合分析结果...")
        
        # 初始化整合结果
        self.integrated_results = {
            'summary': {},
            'writing_style': {},
            'personality_traits': {},
            'content_analysis': {},
            'time_trends': {},
            'ai_insights': {},
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'total_articles': len(article_metadata),
                'analysis_version': '1.0'
            }
        }
        
        # 整合基础统计信息
        self._integrate_basic_summary(basic_analysis, article_metadata)
        
        # 整合写作风格分析
        self._integrate_writing_style(basic_analysis, ai_analysis)
        
        # 整合性格特征分析
        self._integrate_personality_traits(basic_analysis, ai_analysis)
        
        # 整合内容分析
        self._integrate_content_analysis(basic_analysis, ai_analysis)
        
        # 分析时间趋势
        self._analyze_time_trends(article_metadata, basic_analysis)
        
        # 整合AI洞察
        self._integrate_ai_insights(ai_analysis)
        
        # 计算综合评分
        self._calculate_comprehensive_scores()
        
        return self.integrated_results
    
    def _integrate_basic_summary(self, basic_analysis: Dict, article_metadata: List[Dict]):
        """整合基础统计摘要"""
        # 计算总体统计
        total_words = sum(article.get('word_count', 0) for article in article_metadata)
        total_chars = sum(article.get('char_count', 0) for article in article_metadata)
        
        # 时间跨度
        dates = [article.get('publish_date') for article in article_metadata if article.get('publish_date')]
        if dates:
            try:
                start_date = min(dates)
                end_date = max(dates)
                time_span = f"{start_date} - {end_date}"
            except:
                time_span = "未知"
        else:
            time_span = "未知"
        
        # 主题分布
        topic_distribution = defaultdict(int)
        for article in article_metadata:
            topic = article.get('main_topic', 'other')
            topic_distribution[topic] += 1
        
        self.integrated_results['summary'] = {
            'total_articles': len(article_metadata),
            'total_words': total_words,
            'total_characters': total_chars,
            'time_span': time_span,
            'main_topics': dict(topic_distribution),
            'avg_words_per_article': round(total_words / len(article_metadata), 1) if article_metadata else 0,
            'avg_chars_per_article': round(total_chars / len(article_metadata), 1) if article_metadata else 0
        }
    
    def _integrate_writing_style(self, basic_analysis: Dict, ai_analysis: Dict):
        """整合写作风格分析"""
        # 基础统计评分
        style_scores = basic_analysis.get('style_scores', {})
        
        # AI写作风格分析
        ai_writing_style = ai_analysis.get('writing_style', {})
        
        self.integrated_results['writing_style'] = {
            'vocabulary_richness': style_scores.get('vocabulary_richness', 5.0),
            'sentence_complexity': style_scores.get('sentence_complexity', 5.0),
            'emotional_expression': style_scores.get('emotional_expression', 5.0),
            'structure_organization': style_scores.get('structure_organization', 5.0),
            'overall_style_score': style_scores.get('overall_style', 5.0),
            'ai_interpretation': ai_writing_style.get('content', {}).get('text', '暂无AI分析结果'),
            'detailed_analysis': {
                'vocabulary': basic_analysis.get('vocabulary', {}),
                'sentences': basic_analysis.get('sentences', {}),
                'paragraphs': basic_analysis.get('writing_patterns', {}).get('paragraph_analysis', {})
            }
        }
    
    def _integrate_personality_traits(self, basic_analysis: Dict, ai_analysis: Dict):
        """整合性格特征分析"""
        # 从AI分析中提取Big Five评分
        ai_personality = ai_analysis.get('personality_traits', {})
        
        # 尝试提取评分，如果失败则使用默认值
        try:
            personality_scores = self._extract_personality_scores(ai_personality)
        except:
            personality_scores = {
                'openness': 50,
                'conscientiousness': 50,
                'extraversion': 50,
                'agreeableness': 50,
                'neuroticism': 50
            }
        
        # 中文标签映射
        trait_labels = {
            'openness': '开放性',
            'conscientiousness': '尽责性',
            'extraversion': '外向性',
            'agreeableness': '宜人性',
            'neuroticism': '神经质'
        }
        
        # 构建性格特征报告
        personality_report = {}
        for trait, score in personality_scores.items():
            label = trait_labels.get(trait, trait)
            personality_report[trait] = {
                'score': score,
                'label': label,
                'level': self._get_trait_level(score),
                'description': self._get_trait_description(trait, score)
            }
        
        self.integrated_results['personality_traits'] = {
            'big_five_scores': personality_scores,
            'personality_report': personality_report,
            'ai_interpretation': ai_personality.get('content', {}).get('text', '暂无AI分析结果'),
            'analysis_confidence': 'high' if ai_personality.get('status') == 'success' else 'low'
        }
    
    def _integrate_content_analysis(self, basic_analysis: Dict, ai_analysis: Dict):
        """整合内容分析"""
        # 主题分布
        topics = basic_analysis.get('topics', {})
        
        # 情感分析
        emotions = basic_analysis.get('emotions', {})
        
        # AI内容偏好分析
        ai_content = ai_analysis.get('content_preferences', {})
        
        self.integrated_results['content_analysis'] = {
            'topic_distribution': topics.get('topic_distribution', {}),
            'main_topics': topics.get('topic_words', {}),
            'keywords': topics.get('keywords', []),
            'emotional_tone': {
                'overall_sentiment': emotions.get('overall_sentiment', 'neutral'),
                'emotion_ratios': emotions.get('emotion_ratios', {}),
                'emotion_counts': emotions.get('emotion_counts', {})
            },
            'ai_content_analysis': ai_content.get('content', {}).get('text', '暂无AI分析结果'),
            'writing_techniques': basic_analysis.get('writing_patterns', {}).get('writing_techniques', {})
        }
    
    def _analyze_time_trends(self, article_metadata: List[Dict], basic_analysis: Dict):
        """分析时间趋势"""
        # 按年份分组分析
        yearly_stats = defaultdict(lambda: {
            'article_count': 0,
            'total_words': 0,
            'avg_words': 0,
            'topics': defaultdict(int),
            'sentiment': defaultdict(int)
        })
        
        for article in article_metadata:
            publish_date = article.get('publish_date', '')
            if publish_date:
                try:
                    year = publish_date[:4]  # 提取年份
                    yearly_stats[year]['article_count'] += 1
                    yearly_stats[year]['total_words'] += article.get('word_count', 0)
                    
                    # 统计主题
                    topic = article.get('main_topic', 'other')
                    yearly_stats[year]['topics'][topic] += 1
                    
                    # 统计情感
                    sentiment = article.get('overall_sentiment', 'neutral')
                    yearly_stats[year]['sentiment'][sentiment] += 1
                    
                except:
                    continue
        
        # 计算年度平均值
        for year, stats in yearly_stats.items():
            if stats['article_count'] > 0:
                stats['avg_words'] = round(stats['total_words'] / stats['article_count'], 1)
        
        # 趋势分析
        years = sorted(yearly_stats.keys())
        if len(years) >= 2:
            # 计算变化趋势
            word_trend = self._calculate_trend(
                [yearly_stats[year]['avg_words'] for year in years]
            )
            topic_trend = self._analyze_topic_trends(yearly_stats)
        else:
            word_trend = 'insufficient_data'
            topic_trend = {}
        
        self.integrated_results['time_trends'] = {
            'yearly_statistics': dict(yearly_stats),
            'word_count_trend': word_trend,
            'topic_evolution': topic_trend,
            'analysis_period': f"{min(years)} - {max(years)}" if years else "未知"
        }
    
    def _integrate_ai_insights(self, ai_analysis: Dict):
        """整合AI洞察"""
        insights = {}
        
        # 提取各维度的AI分析结果
        for analysis_type, result in ai_analysis.items():
            if analysis_type != 'analysis_timestamp' and analysis_type != 'analysis_status':
                if result.get('status') == 'success':
                    insights[analysis_type] = {
                        'summary': result.get('content', {}).get('text', '暂无分析结果'),
                        'details': result.get('content', {}),
                        'confidence': 'high'
                    }
                else:
                    insights[analysis_type] = {
                        'summary': '分析失败',
                        'details': {},
                        'confidence': 'low'
                    }
        
        self.integrated_results['ai_insights'] = insights
    
    def _calculate_comprehensive_scores(self):
        """计算综合评分"""
        # 写作能力综合评分
        writing_style = self.integrated_results['writing_style']
        writing_score = (
            writing_style['vocabulary_richness'] * 0.25 +
            writing_style['sentence_complexity'] * 0.25 +
            writing_style['emotional_expression'] * 0.25 +
            writing_style['structure_organization'] * 0.25
        )
        
        # 内容质量评分
        content_analysis = self.integrated_results['content_analysis']
        topic_diversity = len(content_analysis.get('main_topics', {}))
        content_score = min(10, topic_diversity * 2 + 5)  # 主题多样性 + 基础分
        
        # 个性特征平衡性评分
        personality = self.integrated_results['personality_traits']
        big_five_scores = personality.get('big_five_scores', {})
        if big_five_scores:
            # 计算各维度的平衡性（越接近50分越平衡）
            balance_score = 10 - sum(abs(score - 50) for score in big_five_scores.values()) / 50
            balance_score = max(0, min(10, balance_score))
        else:
            balance_score = 5.0
        
        # 总体评分
        overall_score = (writing_score * 0.4 + content_score * 0.3 + balance_score * 0.3)
        
        self.integrated_results['comprehensive_scores'] = {
            'writing_ability': round(writing_score, 1),
            'content_quality': round(content_score, 1),
            'personality_balance': round(balance_score, 1),
            'overall_score': round(overall_score, 1),
            'score_interpretation': self._interpret_overall_score(overall_score)
        }
    
    def _extract_personality_scores(self, personality_analysis: Dict) -> Dict[str, int]:
        """从AI分析中提取性格评分"""
        scores = {
            'openness': 50,
            'conscientiousness': 50,
            'extraversion': 50,
            'agreeableness': 50,
            'neuroticism': 50
        }
        
        try:
            content = personality_analysis.get('content', {})
            if isinstance(content, dict):
                for trait in scores.keys():
                    # 查找包含评分的字段
                    for key, value in content.items():
                        if trait in key.lower() and isinstance(value, (int, float)):
                            scores[trait] = min(100, max(0, int(value)))
                        elif isinstance(value, str) and trait in value.lower():
                            # 尝试从文本中提取数字
                            import re
                            numbers = re.findall(r'\d+', value)
                            if numbers:
                                scores[trait] = min(100, max(0, int(numbers[0])))
        except:
            pass
        
        return scores
    
    def _get_trait_level(self, score: int) -> str:
        """获取特质水平描述"""
        if score >= 80:
            return '很高'
        elif score >= 60:
            return '较高'
        elif score >= 40:
            return '中等'
        elif score >= 20:
            return '较低'
        else:
            return '很低'
    
    def _get_trait_description(self, trait: str, score: int) -> str:
        """获取特质描述"""
        descriptions = {
            'openness': {
                'high': '对新事物充满好奇，思维开放，富有想象力',
                'medium': '对新事物有一定接受度，思维相对开放',
                'low': '偏好熟悉的事物，思维相对保守'
            },
            'conscientiousness': {
                'high': '做事认真负责，有组织性，目标导向明确',
                'medium': '做事比较认真，有一定的组织性',
                'low': '做事相对随意，组织性有待提高'
            },
            'extraversion': {
                'high': '性格外向，善于表达，社交活跃',
                'medium': '性格适中，表达和社交能力一般',
                'low': '性格内向，表达和社交相对保守'
            },
            'agreeableness': {
                'high': '为人友善，善于合作，富有同理心',
                'medium': '为人比较友善，合作性一般',
                'low': '为人相对直接，合作性有待提高'
            },
            'neuroticism': {
                'high': '情绪波动较大，容易感到压力和焦虑',
                'medium': '情绪相对稳定，偶尔会有波动',
                'low': '情绪稳定，抗压能力强'
            }
        }
        
        if score >= 60:
            level = 'high'
        elif score >= 40:
            level = 'medium'
        else:
            level = 'low'
        
        return descriptions.get(trait, {}).get(level, '暂无描述')
    
    def _calculate_trend(self, values: List[float]) -> str:
        """计算趋势"""
        if len(values) < 2:
            return 'insufficient_data'
        
        # 计算变化率
        changes = []
        for i in range(1, len(values)):
            if values[i-1] != 0:
                change = (values[i] - values[i-1]) / values[i-1]
                changes.append(change)
        
        if not changes:
            return 'no_change'
        
        avg_change = sum(changes) / len(changes)
        
        if avg_change > 0.1:
            return 'increasing'
        elif avg_change < -0.1:
            return 'decreasing'
        else:
            return 'stable'
    
    def _analyze_topic_trends(self, yearly_stats: Dict) -> Dict:
        """分析主题演变趋势"""
        topic_trends = {}
        
        # 获取所有主题
        all_topics = set()
        for year_stats in yearly_stats.values():
            all_topics.update(year_stats['topics'].keys())
        
        # 分析每个主题的趋势
        for topic in all_topics:
            topic_counts = []
            years = sorted(yearly_stats.keys())
            
            for year in years:
                topic_counts.append(yearly_stats[year]['topics'].get(topic, 0))
            
            trend = self._calculate_trend(topic_counts)
            topic_trends[topic] = {
                'trend': trend,
                'yearly_counts': dict(zip(years, topic_counts))
            }
        
        return topic_trends
    
    def _interpret_overall_score(self, score: float) -> str:
        """解释总体评分"""
        if score >= 8.5:
            return '优秀 - 您的博客写作水平很高，内容质量优秀，个性特征鲜明'
        elif score >= 7.0:
            return '良好 - 您的博客写作水平良好，内容质量较高，个性特征明显'
        elif score >= 5.5:
            return '中等 - 您的博客写作水平中等，内容质量一般，个性特征适中'
        elif score >= 4.0:
            return '待提升 - 您的博客写作水平有待提升，内容质量需要改进'
        else:
            return '需要努力 - 您的博客写作水平需要更多努力和练习'
    
    def export_results(self, output_path: str = None) -> str:
        """
        导出分析结果
        
        Args:
            output_path: 输出文件路径
            
        Returns:
            输出文件路径
        """
        if not output_path:
            output_path = f"scripts/output/blog_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.integrated_results, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 分析结果已导出到: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ 导出结果失败: {e}")
            return None
