#!/usr/bin/env python3
"""
博客分析主脚本

功能：
- 读取所有博客文章
- 进行基础统计分析
- 调用AI进行深度分析
- 整合分析结果
- 生成分析报告
- 支持增量更新和缓存

使用示例：
  python blog_analysis.py
  python blog_analysis.py --force  # 强制重新分析
  python blog_analysis.py --cache-info  # 查看缓存信息
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# 导入自定义模块
from analyzers import BasicAnalyzer, AIAnalyzer, ResultIntegrator
from utils import TextProcessor, CacheManager


class BlogAnalyzer:
    """博客分析器主类"""
    
    def __init__(self, blog_dir: str = "src/content/blog", force_analysis: bool = False):
        """
        初始化博客分析器
        
        Args:
            blog_dir: 博客文章目录
            force_analysis: 是否强制重新分析
        """
        self.blog_dir = Path(blog_dir)
        self.force_analysis = force_analysis
        
        # 检查博客目录是否存在
        if not self.blog_dir.exists():
            raise FileNotFoundError(f"博客目录不存在: {self.blog_dir}")
        
        # 初始化各个模块
        self.text_processor = TextProcessor()
        self.basic_analyzer = BasicAnalyzer()
        self.ai_analyzer = AIAnalyzer()
        self.result_integrator = ResultIntegrator()
        self.cache_manager = CacheManager()
        
        print(f"📚 博客分析器初始化完成")
        print(f"📁 博客目录: {self.blog_dir}")
        print(f"🔄 强制分析: {'是' if force_analysis else '否'}")
    
    def discover_articles(self) -> List[Dict[str, Any]]:
        """
        发现所有博客文章
        
        Returns:
            文章信息列表
        """
        print("🔍 正在发现博客文章...")
        
        articles = []
        
        # 遍历博客目录
        for item in self.blog_dir.iterdir():
            if item.is_file() and item.suffix == '.md':
                # 单文件Markdown文章
                article_info = self._process_single_article(item)
                if article_info:
                    articles.append(article_info)
                    
            elif item.is_dir():
                # 目录格式文章
                index_file = item / "index.md"
                if index_file.exists():
                    article_info = self._process_directory_article(item, index_file)
                    if article_info:
                        articles.append(article_info)
        
        print(f"✅ 发现 {len(articles)} 篇博客文章")
        return articles
    
    def _process_single_article(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """
        处理单文件文章
        
        Args:
            file_path: 文章文件路径
            
        Returns:
            文章信息字典
        """
        try:
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 文本预处理
            cleaned_content, metadata, paragraphs, sentences = self.text_processor.process_article(content)
            
            # 基础统计
            stats = self.text_processor.get_text_statistics(cleaned_content)
            
            # 构建文章信息
            article_info = {
                'file_path': str(file_path),
                'title': metadata.get('title', file_path.stem) if metadata else file_path.stem,
                'publish_date': metadata.get('publishDate', ''),
                'tags': metadata.get('tags', []),
                'content': cleaned_content,
                'paragraphs': paragraphs,
                'sentences': sentences,
                'word_count': stats['total_words'],
                'char_count': stats['total_characters'],
                'paragraph_count': stats['paragraph_count'],
                'sentence_count': stats['sentence_count']
            }
            
            return article_info
            
        except Exception as e:
            print(f"⚠️  处理文章失败 {file_path}: {e}")
            return None
    
    def _process_directory_article(self, dir_path: Path, index_file: Path) -> Optional[Dict[str, Any]]:
        """
        处理目录格式文章
        
        Args:
            dir_path: 文章目录路径
            index_file: 索引文件路径
            
        Returns:
            文章信息字典
        """
        try:
            # 读取索引文件内容
            with open(index_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 文本预处理
            cleaned_content, metadata, paragraphs, sentences = self.text_processor.process_article(content)
            
            # 基础统计
            stats = self.text_processor.get_text_statistics(cleaned_content)
            
            # 构建文章信息
            article_info = {
                'file_path': str(index_file),
                'title': metadata.get('title', dir_path.name) if metadata else dir_path.name,
                'publish_date': metadata.get('publishDate', ''),
                'tags': metadata.get('tags', []),
                'content': cleaned_content,
                'paragraphs': paragraphs,
                'sentences': sentences,
                'word_count': stats['total_words'],
                'char_count': stats['total_characters'],
                'paragraph_count': stats['paragraph_count'],
                'sentence_count': stats['sentence_count']
            }
            
            return article_info
            
        except Exception as e:
            print(f"⚠️  处理文章失败 {index_file}: {e}")
            return None
    
    def analyze_articles(self, articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        分析文章列表
        
        Args:
            articles: 文章信息列表
            
        Returns:
            分析结果字典
        """
        print("📊 开始分析文章...")
        
        if not articles:
            print("⚠️  没有文章需要分析")
            return {}
        
        # 计算文章哈希值
        current_hashes = {}
        for article in articles:
            content = article.get('content', '')
            current_hashes[article['file_path']] = self.cache_manager.get_article_hash(content)
        
        # 检查是否需要增量分析
        if not self.force_analysis:
            articles_to_analyze, cached_results = self.cache_manager.get_incremental_analysis_data(
                articles, current_hashes
            )
            
            if not articles_to_analyze and cached_results:
                # 使用缓存结果
                return cached_results
        else:
            articles_to_analyze = articles
            cached_results = None
        
        # 基础统计分析
        print("📈 正在进行基础统计分析...")
        basic_analysis = self._perform_basic_analysis(articles_to_analyze)
        
        # AI深度分析
        print("🤖 正在进行AI深度分析...")
        ai_analysis = self._perform_ai_analysis(articles_to_analyze, basic_analysis)
        
        # 整合分析结果
        print("🔗 正在整合分析结果...")
        if cached_results and not self.force_analysis:
            # 增量更新：合并缓存结果和新分析结果
            final_results = self.cache_manager.merge_incremental_results(
                cached_results, 
                {'summary': basic_analysis.get('summary', {}), 'ai_insights': ai_analysis}
            )
        else:
            # 完整分析：整合所有结果
            final_results = self.result_integrator.integrate_analysis_results(
                basic_analysis, ai_analysis, articles
            )
        
        # 保存到缓存
        self.cache_manager.save_analysis_cache(final_results)
        
        # 保存文章哈希值
        self.cache_manager.save_article_hashes(current_hashes)
        
        return final_results
    
    def _perform_basic_analysis(self, articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        执行基础统计分析
        
        Args:
            articles: 文章列表
            
        Returns:
            基础分析结果
        """
        # 合并所有文章内容进行分析
        combined_content = ""
        combined_paragraphs = []
        combined_sentences = []
        
        for article in articles:
            combined_content += article.get('content', '') + "\n\n"
            combined_paragraphs.extend(article.get('paragraphs', []))
            combined_sentences.extend(article.get('sentences', []))
        
        # 执行综合分析
        basic_analysis = self.basic_analyzer.comprehensive_analysis(
            combined_content, combined_sentences, combined_paragraphs
        )
        
        # 添加摘要信息
        total_words = sum(article.get('word_count', 0) for article in articles)
        total_chars = sum(article.get('char_count', 0) for article in articles)
        
        basic_analysis['summary'] = {
            'total_articles': len(articles),
            'total_words': total_words,
            'total_characters': total_chars,
            'avg_words_per_article': round(total_words / len(articles), 1) if articles else 0
        }
        
        return basic_analysis
    
    def _perform_ai_analysis(self, articles: List[Dict[str, Any]], 
                           basic_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行AI深度分析
        
        Args:
            articles: 文章列表
            basic_analysis: 基础分析结果
            
        Returns:
            AI分析结果
        """
        # 选择代表性文章样本（前3篇）
        sample_articles = articles[:3]
        text_samples = [article.get('content', '') for article in sample_articles]
        
        # 准备基础统计数据
        basic_stats = {
            'total_words': basic_analysis.get('summary', {}).get('total_words', 0),
            'avg_sentence_length': basic_analysis.get('sentences', {}).get('avg_sentence_length', 0),
            'type_token_ratio': basic_analysis.get('vocabulary', {}).get('type_token_ratio', 0),
            'overall_sentiment': basic_analysis.get('emotions', {}).get('overall_sentiment', 'unknown'),
            'emotion_counts': basic_analysis.get('emotions', {}).get('emotion_counts', {}),
            'main_topic': basic_analysis.get('topics', {}).get('main_topic', 'unknown'),
            'topic_counts': basic_analysis.get('topics', {}).get('topic_counts', {}),
            'keywords': basic_analysis.get('topics', {}).get('keywords', []),
            'opening_patterns': basic_analysis.get('writing_patterns', {}).get('opening_patterns', []),
            'closing_patterns': basic_analysis.get('writing_patterns', {}).get('closing_patterns', []),
            'complexity_ratio': basic_analysis.get('sentences', {}).get('complexity', {}).get('complexity_ratio', 0),
            'paragraph_analysis': basic_analysis.get('writing_patterns', {}).get('paragraph_analysis', {}),
            'quotes': basic_analysis.get('writing_patterns', {}).get('writing_techniques', {}).get('quotes', 0),
            'emphasis': basic_analysis.get('writing_patterns', {}).get('writing_techniques', {}).get('emphasis', 0)
        }
        
        # 执行AI分析
        ai_analysis = self.ai_analyzer.comprehensive_ai_analysis(text_samples, basic_stats)
        
        return ai_analysis
    
    def export_results(self, results: Dict[str, Any], output_path: str = None) -> str:
        """
        导出分析结果
        
        Args:
            results: 分析结果
            output_path: 输出文件路径
            
        Returns:
            输出文件路径
        """
        if not output_path:
            output_path = f"scripts/output/blog_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            # 确保输出目录存在
            output_dir = Path(output_path).parent
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # 导出结果
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 分析结果已导出到: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ 导出结果失败: {e}")
            return None
    
    def generate_summary_report(self, results: Dict[str, Any]) -> str:
        """
        生成摘要报告
        
        Args:
            results: 分析结果
            
        Returns:
            摘要报告文本
        """
        summary = []
        summary.append("=" * 60)
        summary.append("📊 博客分析摘要报告")
        summary.append("=" * 60)
        
        # 基本信息
        summary_info = results.get('summary', {})
        summary.append(f"📚 文章总数: {summary_info.get('total_articles', 0)}")
        summary.append(f"📝 总字数: {summary_info.get('total_words', 0):,}")
        summary.append(f"📅 时间跨度: {summary_info.get('time_span', '未知')}")
        summary.append("")
        
        # 写作风格评分
        style_info = results.get('writing_style', {})
        summary.append("🎨 写作风格评分:")
        summary.append(f"   词汇丰富度: {style_info.get('vocabulary_richness', 0)}/10")
        summary.append(f"   句子复杂度: {style_info.get('sentence_complexity', 0)}/10")
        summary.append(f"   情感表达: {style_info.get('emotional_expression', 0)}/10")
        summary.append(f"   结构组织: {style_info.get('structure_organization', 0)}/10")
        summary.append(f"   总体评分: {style_info.get('overall_style_score', 0)}/10")
        summary.append("")
        
        # 性格特征
        personality_info = results.get('personality_traits', {})
        big_five_scores = personality_info.get('big_five_scores', {})
        if big_five_scores:
            summary.append("🧠 性格特征 (Big Five):")
            trait_labels = {
                'openness': '开放性',
                'conscientiousness': '尽责性',
                'extraversion': '外向性',
                'agreeableness': '宜人性',
                'neuroticism': '神经质'
            }
            for trait, score in big_five_scores.items():
                label = trait_labels.get(trait, trait)
                summary.append(f"   {label}: {score}/100")
            summary.append("")
        
        # 综合评分
        comprehensive_scores = results.get('comprehensive_scores', {})
        if comprehensive_scores:
            summary.append("🏆 综合评分:")
            summary.append(f"   写作能力: {comprehensive_scores.get('writing_ability', 0)}/10")
            summary.append(f"   内容质量: {comprehensive_scores.get('content_quality', 0)}/10")
            summary.append(f"   个性平衡: {comprehensive_scores.get('personality_balance', 0)}/10")
            summary.append(f"   总体评分: {comprehensive_scores.get('overall_score', 0)}/10")
            summary.append("")
            summary.append(f"💡 评分解读: {comprehensive_scores.get('score_interpretation', '')}")
            summary.append("")
        
        # 主题分布
        content_analysis = results.get('content_analysis', {})
        topic_distribution = content_analysis.get('topic_distribution', {})
        if topic_distribution:
            summary.append("📖 主题分布:")
            for topic, ratio in topic_distribution.items():
                summary.append(f"   {topic}: {ratio:.1%}")
            summary.append("")
        
        # 时间趋势
        time_trends = results.get('time_trends', {})
        if time_trends:
            summary.append("📈 时间趋势:")
            word_trend = time_trends.get('word_count_trend', 'unknown')
            summary.append(f"   字数变化趋势: {word_trend}")
            summary.append(f"   分析周期: {time_trends.get('analysis_period', '未知')}")
            summary.append("")
        
        summary.append("=" * 60)
        summary.append("📋 详细分析结果请查看导出的JSON文件")
        summary.append("🌐 建议将结果集成到About页面展示")
        summary.append("=" * 60)
        
        return "\n".join(summary)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='博客分析工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python blog_analysis.py                    # 正常分析（支持增量更新）
  python blog_analysis.py --force            # 强制重新分析
  python blog_analysis.py --cache-info       # 查看缓存信息
  python blog_analysis.py --clear-cache      # 清除缓存
  python blog_analysis.py --output path      # 指定输出路径

环境变量:
  DOUBAO_API_KEY - 火山引擎API密钥
        """
    )
    
    parser.add_argument('--force', action='store_true', 
                       help='强制重新分析，忽略缓存')
    parser.add_argument('--cache-info', action='store_true',
                       help='显示缓存信息')
    parser.add_argument('--clear-cache', action='store_true',
                       help='清除所有缓存')
    parser.add_argument('--output', type=str,
                       help='指定输出文件路径')
    parser.add_argument('--blog-dir', type=str, default='src/content/blog',
                       help='博客文章目录路径')
    
    args = parser.parse_args()
    
    try:
        # 检查环境变量
        if not os.getenv("DOUBAO_API_KEY"):
            print("❌ 错误：未找到环境变量 DOUBAO_API_KEY")
            print("请设置环境变量：export DOUBAO_API_KEY=your_api_key")
            sys.exit(1)
        
        # 创建博客分析器
        analyzer = BlogAnalyzer(args.blog_dir, args.force)
        
        if args.cache_info:
            # 显示缓存信息
            cache_info = analyzer.cache_manager.get_cache_info()
            print("📋 缓存信息:")
            print(json.dumps(cache_info, ensure_ascii=False, indent=2))
            return
        
        if args.clear_cache:
            # 清除缓存
            analyzer.cache_manager.clear_cache()
            print("✅ 缓存已清除")
            return
        
        # 执行分析
        print("🚀 开始博客分析...")
        print("=" * 50)
        
        # 发现文章
        articles = analyzer.discover_articles()
        if not articles:
            print("❌ 未找到任何博客文章")
            sys.exit(1)
        
        # 分析文章
        results = analyzer.analyze_articles(articles)
        if not results:
            print("❌ 分析失败")
            sys.exit(1)
        
        # 导出结果
        output_path = analyzer.export_results(results, args.output)
        
        # 生成摘要报告
        summary = analyzer.generate_summary_report(results)
        print("\n" + summary)
        
        print("\n🎉 博客分析完成！")
        if output_path:
            print(f"📁 结果文件: {output_path}")
        
    except KeyboardInterrupt:
        print("\n⚠️  用户中断操作")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 分析过程中发生错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
