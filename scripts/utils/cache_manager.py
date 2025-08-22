#!/usr/bin/env python3
"""
缓存管理器

功能：
- 管理分析结果的缓存
- 支持增量更新
- 缓存文件管理
- 缓存有效性验证
"""

import json
import os
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta


class CacheManager:
    """缓存管理器"""
    
    def __init__(self, cache_dir: str = "scripts/output/cache"):
        """
        初始化缓存管理器
        
        Args:
            cache_dir: 缓存目录路径
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # 缓存文件路径
        self.analysis_cache_file = self.cache_dir / "analysis_cache.json"
        self.article_hashes_file = self.cache_dir / "article_hashes.json"
        self.cache_metadata_file = self.cache_dir / "cache_metadata.json"
    
    def get_article_hash(self, content: str) -> str:
        """
        计算文章内容的哈希值
        
        Args:
            content: 文章内容
            
        Returns:
            内容哈希值
        """
        return hashlib.md5(content.encode('utf-8')).hexdigest()
    
    def load_article_hashes(self) -> Dict[str, str]:
        """
        加载文章哈希值缓存
        
        Returns:
            文章路径到哈希值的映射
        """
        if self.article_hashes_file.exists():
            try:
                with open(self.article_hashes_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  加载文章哈希缓存失败: {e}")
                return {}
        return {}
    
    def save_article_hashes(self, article_hashes: Dict[str, str]):
        """
        保存文章哈希值缓存
        
        Args:
            article_hashes: 文章路径到哈希值的映射
        """
        try:
            with open(self.article_hashes_file, 'w', encoding='utf-8') as f:
                json.dump(article_hashes, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️  保存文章哈希缓存失败: {e}")
    
    def get_changed_articles(self, current_hashes: Dict[str, str]) -> List[str]:
        """
        获取发生变化的文章列表
        
        Args:
            current_hashes: 当前文章哈希值
            
        Returns:
            发生变化的文章路径列表
        """
        cached_hashes = self.load_article_hashes()
        changed_articles = []
        
        for article_path, current_hash in current_hashes.items():
            cached_hash = cached_hashes.get(article_path)
            if cached_hash != current_hash:
                changed_articles.append(article_path)
        
        # 检查是否有删除的文章
        for cached_path in cached_hashes.keys():
            if cached_path not in current_hashes:
                print(f"📝 检测到删除的文章: {cached_path}")
        
        return changed_articles
    
    def load_analysis_cache(self) -> Optional[Dict[str, Any]]:
        """
        加载分析结果缓存
        
        Returns:
            缓存的分析结果，如果不存在或过期则返回None
        """
        if not self.analysis_cache_file.exists():
            return None
        
        try:
            with open(self.analysis_cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            # 检查缓存是否过期
            if self._is_cache_valid(cache_data):
                print("📋 使用缓存的分析结果")
                return cache_data
            else:
                print("⏰ 缓存已过期，需要重新分析")
                return None
                
        except Exception as e:
            print(f"⚠️  加载分析缓存失败: {e}")
            return None
    
    def save_analysis_cache(self, analysis_results: Dict[str, Any]):
        """
        保存分析结果到缓存
        
        Args:
            analysis_results: 分析结果
        """
        try:
            # 添加缓存元数据
            cache_data = {
                'analysis_results': analysis_results,
                'cached_at': datetime.now().isoformat(),
                'cache_version': '1.0'
            }
            
            with open(self.analysis_cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
            
            print("💾 分析结果已缓存")
            
        except Exception as e:
            print(f"⚠️  保存分析缓存失败: {e}")
    
    def _is_cache_valid(self, cache_data: Dict[str, Any]) -> bool:
        """
        检查缓存是否有效
        
        Args:
            cache_data: 缓存数据
            
        Returns:
            缓存是否有效
        """
        try:
            cached_at = cache_data.get('cached_at')
            if not cached_at:
                return False
            
            # 解析缓存时间
            cache_time = datetime.fromisoformat(cached_at)
            current_time = datetime.now()
            
            # 缓存有效期：7天
            cache_validity = timedelta(days=7)
            
            return (current_time - cache_time) < cache_validity
            
        except Exception:
            return False
    
    def get_cache_info(self) -> Dict[str, Any]:
        """
        获取缓存信息
        
        Returns:
            缓存信息字典
        """
        cache_info = {
            'cache_dir': str(self.cache_dir),
            'analysis_cache_exists': self.analysis_cache_file.exists(),
            'article_hashes_exists': self.article_hashes_file.exists(),
            'cache_metadata_exists': self.cache_metadata_file.exists()
        }
        
        if self.analysis_cache_file.exists():
            try:
                with open(self.analysis_cache_file, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)
                
                cached_at = cache_data.get('cached_at', '')
                if cached_at:
                    cache_time = datetime.fromisoformat(cached_at)
                    current_time = datetime.now()
                    age = current_time - cache_time
                    
                    cache_info.update({
                        'cached_at': cached_at,
                        'cache_age_hours': round(age.total_seconds() / 3600, 1),
                        'is_valid': self._is_cache_valid(cache_data)
                    })
                    
            except Exception as e:
                cache_info['error'] = str(e)
        
        return cache_info
    
    def clear_cache(self):
        """清除所有缓存"""
        try:
            if self.analysis_cache_file.exists():
                os.remove(self.analysis_cache_file)
                print("🗑️  已清除分析结果缓存")
            
            if self.article_hashes_file.exists():
                os.remove(self.article_hashes_file)
                print("🗑️  已清除文章哈希缓存")
            
            if self.cache_metadata_file.exists():
                os.remove(self.cache_metadata_file)
                print("🗑️  已清除缓存元数据")
                
        except Exception as e:
            print(f"⚠️  清除缓存失败: {e}")
    
    def update_cache_metadata(self, metadata: Dict[str, Any]):
        """
        更新缓存元数据
        
        Args:
            metadata: 元数据字典
        """
        try:
            # 添加更新时间
            metadata['updated_at'] = datetime.now().isoformat()
            
            with open(self.cache_metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"⚠️  更新缓存元数据失败: {e}")
    
    def get_incremental_analysis_data(self, all_articles: List[Dict], 
                                     current_hashes: Dict[str, str]) -> Tuple[List[Dict], Optional[Dict]]:
        """
        获取增量分析所需的数据
        
        Args:
            all_articles: 所有文章列表
            current_hashes: 当前文章哈希值
            
        Returns:
            (需要分析的文章列表, 缓存的分析结果)
        """
        # 加载缓存
        cached_results = self.load_analysis_cache()
        
        if not cached_results:
            # 没有缓存，需要分析所有文章
            print("🔄 无缓存，将分析所有文章")
            return all_articles, None
        
        # 检查哪些文章发生了变化
        changed_articles = self.get_changed_articles(current_hashes)
        
        if not changed_articles:
            print("✅ 所有文章均无变化，使用缓存结果")
            return [], cached_results.get('analysis_results')
        
        # 只分析发生变化的文章
        print(f"🔄 检测到 {len(changed_articles)} 篇文章发生变化，进行增量分析")
        
        # 筛选需要分析的文章
        articles_to_analyze = [
            article for article in all_articles 
            if article.get('file_path') in changed_articles
        ]
        
        return articles_to_analyze, cached_results.get('analysis_results')
    
    def merge_incremental_results(self, cached_results: Dict[str, Any], 
                                new_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        合并增量分析结果
        
        Args:
            cached_results: 缓存的分析结果
            new_analysis: 新的分析结果
            
        Returns:
            合并后的结果
        """
        print("🔗 正在合并增量分析结果...")
        
        # 深拷贝缓存结果
        merged_results = json.loads(json.dumps(cached_results))
        
        # 更新元数据
        merged_results['metadata']['updated_at'] = datetime.now().isoformat()
        merged_results['metadata']['incremental_update'] = True
        
        # 更新摘要信息（需要重新计算）
        if 'summary' in new_analysis:
            merged_results['summary'] = new_analysis['summary']
        
        # 更新AI洞察（使用最新的AI分析结果）
        if 'ai_insights' in new_analysis:
            merged_results['ai_insights'] = new_analysis['ai_insights']
        
        # 更新综合评分
        if 'comprehensive_scores' in new_analysis:
            merged_results['comprehensive_scores'] = new_analysis['comprehensive_scores']
        
        # 更新时间趋势（需要重新计算）
        if 'time_trends' in new_analysis:
            merged_results['time_trends'] = new_analysis['time_trends']
        
        return merged_results
    
    def export_cache_report(self, output_path: str = None) -> str:
        """
        导出缓存报告
        
        Args:
            output_path: 输出文件路径
            
        Returns:
            输出文件路径
        """
        if not output_path:
            output_path = f"scripts/output/cache_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            cache_info = self.get_cache_info()
            
            report = {
                'cache_info': cache_info,
                'generated_at': datetime.now().isoformat(),
                'cache_directory': str(self.cache_dir),
                'files': []
            }
            
            # 列出缓存目录中的所有文件
            for file_path in self.cache_dir.iterdir():
                if file_path.is_file():
                    file_info = {
                        'name': file_path.name,
                        'size_bytes': file_path.stat().st_size,
                        'modified_at': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                    }
                    report['files'].append(file_info)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            
            print(f"📊 缓存报告已导出到: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ 导出缓存报告失败: {e}")
            return None
