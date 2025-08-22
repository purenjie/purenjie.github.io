#!/usr/bin/env python3
"""
将博客分析结果集成到About页面的脚本

功能：
- 读取博客分析结果JSON文件
- 将分析结果集成到About页面中
- 保持现有UI风格和排版
"""

import json
import re
from pathlib import Path
from typing import Dict, Any, Optional


class AboutPageIntegrator:
    """About页面集成器"""
    
    def __init__(self, about_file_path: str = "src/pages/about/index.astro"):
        """
        初始化集成器
        
        Args:
            about_file_path: About页面文件路径
        """
        self.about_file_path = Path(about_file_path)
        self.analysis_data = None
        
    def load_analysis_data(self, analysis_file_path: str) -> bool:
        """
        加载分析数据
        
        Args:
            analysis_file_path: 分析结果文件路径
            
        Returns:
            是否成功加载
        """
        try:
            with open(analysis_file_path, 'r', encoding='utf-8') as f:
                self.analysis_data = json.load(f)
            print(f"✅ 成功加载分析数据: {analysis_file_path}")
            return True
        except Exception as e:
            print(f"❌ 加载分析数据失败: {e}")
            return False
    
    def read_about_page(self) -> Optional[str]:
        """
        读取About页面内容
        
        Returns:
            页面内容字符串
        """
        try:
            with open(self.about_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"✅ 成功读取About页面: {self.about_file_path}")
            return content
        except Exception as e:
            print(f"❌ 读取About页面失败: {e}")
            return None
    
    def integrate_analysis_section(self, content: str) -> str:
        """
        集成分析部分到About页面
        
        Args:
            content: 原始页面内容
            
        Returns:
            集成后的页面内容
        """
        if not self.analysis_data:
            print("⚠️  没有分析数据，跳过集成")
            return content
        
        # 查找插入位置（在About Blog部分之后）
        insert_pattern = r'(<h2 id=\'about-blog\'>About Blog</h2>.*?</ul>\s*</PageLayout>)'
        match = re.search(insert_pattern, content, re.DOTALL)
        
        if not match:
            print("⚠️  未找到About Blog部分，在页面末尾添加")
            # 在</PageLayout>之前添加
            insert_pattern = r'(</PageLayout>)'
            match = re.search(insert_pattern, content, re.DOTALL)
            
            if not match:
                print("❌ 未找到页面结束标签")
                return content
        
        # 生成分析部分内容
        analysis_section = self._generate_analysis_section()
        
        # 替换内容
        if 'about-blog' in match.group(1):
            # 在About Blog部分之后插入
            replacement = match.group(1).replace('</PageLayout>', f'\n\n{analysis_section}\n\n</PageLayout>')
        else:
            # 在页面末尾插入
            replacement = f'{analysis_section}\n\n{match.group(1)}'
        
        updated_content = content.replace(match.group(1), replacement)
        
        print("✅ 成功集成分析部分到About页面")
        return updated_content
    
    def _generate_analysis_section(self) -> str:
        """
        生成分析部分内容
        
        Returns:
            分析部分HTML内容
        """
        # 提取关键数据
        summary = self.analysis_data.get('summary', {})
        writing_style = self.analysis_data.get('writing_style', {})
        personality_traits = self.analysis_data.get('personality_traits', {})
        content_analysis = self.analysis_data.get('content_analysis', {})
        comprehensive_scores = self.analysis_data.get('comprehensive_scores', {})
        ai_insights = self.analysis_data.get('ai_insights', {})
        
        # 转义模板字符串中的反引号
        escape_backtick = lambda text: text.replace('`', '\\`') if text else '暂无分析结果'
        
        # 获取转义后的文本
        writing_ai_interpretation = escape_backtick(writing_style.get('ai_interpretation', '暂无AI分析结果'))
        personality_ai_interpretation = escape_backtick(personality_traits.get('ai_interpretation', '暂无AI分析结果'))
        writing_insights_summary = escape_backtick(ai_insights.get('writing_style', {}).get('summary', '暂无分析结果'))
        personality_insights_summary = escape_backtick(ai_insights.get('personality_traits', {}).get('summary', '暂无分析结果'))
        thinking_insights_summary = escape_backtick(ai_insights.get('thinking_patterns', {}).get('summary', '暂无分析结果'))
        content_insights_summary = escape_backtick(ai_insights.get('content_preferences', {}).get('summary', '暂无分析结果'))
        
        # 生成分析部分 - 使用正确的 Astro JSX 语法
        analysis_section = f"""
  <!-- AI博客分析 -->
  <h2 id='ai-blog-analysis'>AI博客分析</h2>
  <p>
    基于AI对博客文章的深度分析，为您展示我的写作风格、性格特征和内容偏好。
  </p>
  
  <BlogAnalysis analysisData={{{{
    summary: {{
      total_articles: {summary.get('total_articles', 0)},
      total_words: {summary.get('total_words', 0)},
      time_span: "{summary.get('time_span', '未知')}",
      main_topics: {json.dumps(summary.get('main_topics', {}), ensure_ascii=False)}
    }},
    writing_style: {{
      vocabulary_richness: {writing_style.get('vocabulary_richness', 5.0)},
      sentence_complexity: {writing_style.get('sentence_complexity', 5.0)},
      emotional_expression: {writing_style.get('emotional_expression', 5.0)},
      structure_organization: {writing_style.get('structure_organization', 5.0)},
      overall_style_score: {writing_style.get('overall_style_score', 5.0)},
      ai_interpretation: `{writing_ai_interpretation}`
    }},
    personality_traits: {{
      big_five_scores: {json.dumps(personality_traits.get('big_five_scores', {}), ensure_ascii=False)},
      ai_interpretation: `{personality_ai_interpretation}`
    }},
    content_analysis: {{
      topic_distribution: {json.dumps(content_analysis.get('topic_distribution', {}), ensure_ascii=False)},
      keywords: {json.dumps(content_analysis.get('keywords', [])[:15], ensure_ascii=False)},
      emotional_tone: {{
        overall_sentiment: "{content_analysis.get('emotional_tone', {}).get('overall_sentiment', 'neutral')}",
        emotion_ratios: {json.dumps(content_analysis.get('emotional_tone', {}).get('emotion_ratios', {}), ensure_ascii=False)}
      }}
    }},
    comprehensive_scores: {{
      writing_ability: {comprehensive_scores.get('writing_ability', 5.0)},
      content_quality: {comprehensive_scores.get('content_quality', 5.0)},
      personality_balance: {comprehensive_scores.get('personality_balance', 5.0)},
      overall_score: {comprehensive_scores.get('overall_score', 5.0)},
      score_interpretation: "{comprehensive_scores.get('score_interpretation', '暂无评分解读')}"
    }},
    ai_insights: {{
      writing_style: {{
        summary: `{writing_insights_summary}`
      }},
      personality_traits: {{
        summary: `{personality_insights_summary}`
      }},
      thinking_patterns: {{
        summary: `{thinking_insights_summary}`
      }},
      content_preferences: {{
        summary: `{content_insights_summary}`
      }}
    }},
    metadata: {{
      generated_at: "{self.analysis_data.get('metadata', {}).get('generated_at', '')}"
    }}
  }}}} />
"""
        
        return analysis_section
    
    def update_headings(self, content: str) -> str:
        """
        更新页面标题列表
        
        Args:
            content: 页面内容
            
        Returns:
            更新后的页面内容
        """
        # 查找headings数组
        headings_pattern = r'(const headings = \[.*?\])'
        match = re.search(headings_pattern, content, re.DOTALL)
        
        if match:
            # 在headings数组末尾添加新的标题
            new_heading = '  { depth: 2, slug: \'ai-blog-analysis\', text: \'AI博客分析\' }'
            
            # 检查是否已经存在
            if 'ai-blog-analysis' not in match.group(1):
                # 在最后一个元素后添加逗号和新的标题
                updated_headings = match.group(1).replace(']', f',\n{new_heading}\n]')
                content = content.replace(match.group(1), updated_headings)
                print("✅ 成功更新页面标题列表")
            else:
                print("ℹ️  AI博客分析标题已存在")
        
        return content
    
    def update_imports(self, content: str) -> str:
        """
        更新导入语句
        
        Args:
            content: 页面内容
            
        Returns:
            更新后的页面内容
        """
        # 检查是否已经导入了BlogAnalysis组件
        if 'BlogAnalysis' not in content:
            # 在现有的import语句后添加
            import_pattern = r'(import.*?from.*?[\'"]astro-pure/user[\'"]\s*)'
            match = re.search(import_pattern, content, re.DOTALL)
            
            if match:
                new_import = 'import BlogAnalysis from \'@/components/about/BlogAnalysis.astro\'\n'
                updated_import = match.group(1) + new_import
                content = content.replace(match.group(1), updated_import)
                print("✅ 成功添加BlogAnalysis组件导入")
            else:
                print("⚠️  未找到astro-pure/user导入语句")
        
        return content
    
    def save_about_page(self, content: str) -> bool:
        """
        保存更新后的About页面
        
        Args:
            content: 页面内容
            
        Returns:
            是否成功保存
        """
        try:
            # 创建备份
            backup_path = self.about_file_path.with_suffix('.astro.backup')
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(self.read_about_page() or '')
            print(f"📋 已创建备份文件: {backup_path}")
            
            # 保存更新后的内容
            with open(self.about_file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ 成功保存更新后的About页面: {self.about_file_path}")
            return True
            
        except Exception as e:
            print(f"❌ 保存About页面失败: {e}")
            return False
    
    def integrate_analysis(self, analysis_file_path: str) -> bool:
        """
        执行完整的集成流程
        
        Args:
            analysis_file_path: 分析结果文件路径
            
        Returns:
            是否成功集成
        """
        print("🚀 开始集成博客分析结果到About页面...")
        
        # 1. 加载分析数据
        if not self.load_analysis_data(analysis_file_path):
            return False
        
        # 2. 读取About页面
        content = self.read_about_page()
        if not content:
            return False
        
        # 3. 更新导入语句
        content = self.update_imports(content)
        
        # 4. 更新标题列表
        content = self.update_headings(content)
        
        # 5. 集成分析部分
        content = self.integrate_analysis_section(content)
        
        # 6. 保存页面
        if self.save_about_page(content):
            print("🎉 博客分析结果集成完成！")
            print("📝 请检查About页面是否正确显示分析结果")
            return True
        else:
            return False


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='将博客分析结果集成到About页面',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python integrate_analysis_to_about.py scripts/output/blog_analysis_20250818_110906.json
  
参数说明:
  analysis_file - 博客分析结果JSON文件路径
        """
    )
    
    parser.add_argument('analysis_file', help='博客分析结果JSON文件路径')
    parser.add_argument('--about-file', default='src/pages/about/index.astro',
                       help='About页面文件路径 (默认: src/pages/about/index.astro)')
    
    args = parser.parse_args()
    
    # 检查分析文件是否存在
    analysis_file_path = Path(args.analysis_file)
    if not analysis_file_path.exists():
        print(f"❌ 分析文件不存在: {analysis_file_path}")
        return
    
    # 创建集成器并执行集成
    integrator = AboutPageIntegrator(args.about_file)
    
    if integrator.integrate_analysis(str(analysis_file_path)):
        print("\n📋 集成完成！")
        print("🔍 请检查以下内容:")
        print("   1. About页面是否正确显示AI分析结果")
        print("   2. 页面样式是否正常")
        print("   3. 所有数据是否正确显示")
        print("\n💡 如果需要恢复原始页面，可以使用备份文件: .astro.backup")
    else:
        print("\n❌ 集成失败，请检查错误信息")


if __name__ == "__main__":
    main()
