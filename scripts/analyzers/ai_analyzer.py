#!/usr/bin/env python3
"""
AI深度分析器

功能：
- 调用火山引擎豆包API进行深度文本分析
- 分析写作风格和个性特征
- 生成Big Five人格特质分析
- 提供思维模式和写作习惯解读
"""

import json
import os
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime


class AIAnalyzer:
    """AI深度分析器"""
    
    def __init__(self):
        """初始化AI分析器"""
        # API配置（复用现有配置）
        self.ark_base_url = "https://ark.cn-beijing.volces.com/api/v3"
        self.text_model = "doubao-1-5-pro-32k-250115"
        
        # 获取API密钥
        self.api_key = os.getenv("DOUBAO_API_KEY")
        if not self.api_key:
            raise ValueError("未找到环境变量 DOUBAO_API_KEY")
        
        # 分析维度配置
        self.analysis_dimensions = [
            'writing_style',
            'personality_traits', 
            'thinking_patterns',
            'content_preferences',
            'emotional_expression'
        ]
    
    def analyze_writing_style(self, text_samples: List[str], basic_stats: Dict) -> Dict[str, Any]:
        """
        分析写作风格
        
        Args:
            text_samples: 文本样本列表
            basic_stats: 基础统计信息
            
        Returns:
            写作风格分析结果
        """
        system_prompt = """你是一位专业的写作风格分析师，擅长分析中文博客的写作特点。

请基于提供的文本样本和统计数据，分析作者的写作风格特征。分析要客观、准确，避免过度解读。

分析维度包括：
1. 语言特色：用词偏好、句式特点、修辞手法
2. 结构特征：段落组织、逻辑层次、过渡方式
3. 表达风格：直接性、情感性、专业性
4. 读者互动：是否考虑读者感受、是否引导思考

请用中文回答，格式要清晰易读。"""
        
        user_prompt = f"""请分析以下博客文章的写作风格：

文本样本（前3篇）：
{chr(10).join([f"样本{i+1}: {sample[:200]}..." for i, sample in enumerate(text_samples[:3])])}

基础统计数据：
- 总字数：{basic_stats.get('total_words', 0)}
- 平均句长：{basic_stats.get('avg_sentence_length', 0)}字符
- 词汇多样性：{basic_stats.get('type_token_ratio', 0)}
- 情感倾向：{basic_stats.get('overall_sentiment', 'unknown')}

请提供详细的写作风格分析。"""
        
        return self._call_ai_api(system_prompt, user_prompt, "writing_style")
    
    def analyze_personality_traits(self, text_samples: List[str], basic_stats: Dict) -> Dict[str, Any]:
        """
        分析性格特征（基于Big Five模型）
        
        Args:
            text_samples: 文本样本列表
            basic_stats: 基础统计信息
            
        Returns:
            性格特征分析结果
        """
        system_prompt = """你是一位专业的文本心理学分析师，擅长通过写作风格分析作者的性格特征。

请基于Big Five人格模型（开放性、尽责性、外向性、宜人性、神经质）来分析作者的个性特征。

分析要求：
1. 每个维度给出0-100的评分
2. 提供评分的具体依据
3. 用中文描述性格特点
4. 避免刻板印象，基于文本证据分析

评分标准：
- 开放性：对新事物的接受度、创新思维、想象力
- 尽责性：组织性、目标导向、自我控制
- 外向性：社交性、表达性、活力水平
- 宜人性：合作性、信任度、同理心
- 神经质：情绪稳定性、压力应对、焦虑水平"""
        
        user_prompt = f"""请基于以下博客文章分析作者的性格特征：

文本样本（前3篇）：
{chr(10).join([f"样本{i+1}: {sample[:200]}..." for i, sample in enumerate(text_samples[:3])])}

基础统计数据：
- 情感词汇使用：{basic_stats.get('emotion_counts', {}).get('positive', 0)}个积极词，{basic_stats.get('emotion_counts', {}).get('negative', 0)}个消极词
- 写作模式：{basic_stats.get('opening_patterns', [])}开头，{basic_stats.get('closing_patterns', [])}结尾
- 主题偏好：{basic_stats.get('main_topic', 'unknown')}

请按照Big Five模型给出评分和详细分析。"""
        
        return self._call_ai_api(system_prompt, user_prompt, "personality_traits")
    
    def analyze_thinking_patterns(self, text_samples: List[str], basic_stats: Dict) -> Dict[str, Any]:
        """
        分析思维模式
        
        Args:
            text_samples: 文本样本列表
            basic_stats: 基础统计信息
            
        Returns:
            思维模式分析结果
        """
        system_prompt = """你是一位认知心理学专家，擅长分析作者的思维模式和认知特征。

请分析作者的思维特点，包括：
1. 思维类型：分析型、直觉型、经验型、理论型
2. 问题解决方式：系统性、创造性、实用性、反思性
3. 学习风格：视觉型、听觉型、动手型、阅读型
4. 决策模式：理性分析、情感驱动、经验依赖、创新尝试

分析要基于文本证据，避免主观臆测。"""
        
        user_prompt = f"""请分析以下博客文章作者的思维模式：

文本样本（前3篇）：
{chr(10).join([f"样本{i+1}: {sample[:200]}..." for i, sample in enumerate(text_samples[:3])])}

基础统计数据：
- 句子复杂度：{basic_stats.get('complexity_ratio', 0)}
- 段落结构：{basic_stats.get('paragraph_analysis', {}).get('avg_paragraph_length', 0)}字符/段
- 写作技巧：引用{basic_stats.get('quotes', 0)}次，强调{basic_stats.get('emphasis', 0)}次

请提供详细的思维模式分析。"""
        
        return self._call_ai_api(system_prompt, user_prompt, "thinking_patterns")
    
    def analyze_content_preferences(self, text_samples: List[str], basic_stats: Dict) -> Dict[str, Any]:
        """
        分析内容偏好
        
        Args:
            text_samples: 文本样本列表
            basic_stats: 基础统计信息
            
        Returns:
            内容偏好分析结果
        """
        system_prompt = """你是一位内容分析专家，擅长分析作者的写作内容和偏好。

请分析作者的内容偏好，包括：
1. 主题选择：技术、生活、读书、总结等
2. 内容深度：浅层介绍、深度分析、实用指导、理论探讨
3. 表达方式：故事化、数据化、对比式、渐进式
4. 价值取向：实用性、启发性、娱乐性、教育性

分析要客观准确，基于文本内容。"""
        
        user_prompt = f"""请分析以下博客文章作者的内容偏好：

文本样本（前3篇）：
{chr(10).join([f"样本{i+1}: {sample[:200]}..." for i, sample in enumerate(text_samples[:3])])}

基础统计数据：
- 主要主题：{basic_stats.get('main_topic', 'unknown')}
- 关键词：{', '.join([word for word, _ in basic_stats.get('keywords', [])[:5]])}
- 技术词汇：{basic_stats.get('topic_counts', {}).get('technology', 0)}个
- 生活词汇：{basic_stats.get('topic_counts', {}).get('life', 0)}个

请提供详细的内容偏好分析。"""
        
        return self._call_ai_api(system_prompt, user_prompt, "content_preferences")
    
    def analyze_emotional_expression(self, text_samples: List[str], basic_stats: Dict) -> Dict[str, Any]:
        """
        分析情感表达
        
        Args:
            text_samples: 文本样本列表
            basic_stats: 基础统计信息
            
        Returns:
            情感表达分析结果
        """
        system_prompt = """你是一位情感分析专家，擅长分析作者的情感表达方式和特点。

请分析作者的情感表达特征，包括：
1. 情感基调：积极、消极、中性、混合
2. 情感深度：表面、深入、复杂、简单
3. 表达方式：直接表达、间接暗示、对比衬托、环境烘托
4. 情感变化：稳定、波动、渐进、跳跃

分析要基于文本中的情感词汇和表达方式。"""
        
        user_prompt = f"""请分析以下博客文章作者的情感表达：

文本样本（前3篇）：
{chr(10).join([f"样本{i+1}: {sample[:200]}..." for i, sample in enumerate(text_samples[:3])])}

基础统计数据：
- 情感倾向：{basic_stats.get('overall_sentiment', 'unknown')}
- 积极词汇：{basic_stats.get('emotion_counts', {}).get('positive', 0)}个
- 消极词汇：{basic_stats.get('emotion_counts', {}).get('negative', 0)}个
- 中性词汇：{basic_stats.get('emotion_counts', {}).get('neutral', 0)}个

请提供详细的情感表达分析。"""
        
        return self._call_ai_api(system_prompt, user_prompt, "emotional_expression")
    
    def comprehensive_ai_analysis(self, text_samples: List[str], basic_stats: Dict) -> Dict[str, Any]:
        """
        综合AI分析
        
        Args:
            text_samples: 文本样本列表
            basic_stats: 基础统计信息
            
        Returns:
            综合AI分析结果
        """
        results = {}
        
        try:
            # 写作风格分析
            print("🤖 正在进行写作风格分析...")
            results['writing_style'] = self.analyze_writing_style(text_samples, basic_stats)
            
            # 性格特征分析
            print("🧠 正在进行性格特征分析...")
            results['personality_traits'] = self.analyze_personality_traits(text_samples, basic_stats)
            
            # 思维模式分析
            print("💭 正在进行思维模式分析...")
            results['thinking_patterns'] = self.analyze_thinking_patterns(text_samples, basic_stats)
            
            # 内容偏好分析
            print("📚 正在进行内容偏好分析...")
            results['content_preferences'] = self.analyze_content_preferences(text_samples, basic_stats)
            
            # 情感表达分析
            print("💖 正在进行情感表达分析...")
            results['emotional_expression'] = self.analyze_emotional_expression(text_samples, basic_stats)
            
            # 添加分析时间戳
            results['analysis_timestamp'] = datetime.now().isoformat()
            results['analysis_status'] = 'completed'
            
        except Exception as e:
            print(f"❌ AI分析过程中发生错误: {e}")
            results['analysis_status'] = 'failed'
            results['error_message'] = str(e)
        
        return results
    
    def _call_ai_api(self, system_prompt: str, user_prompt: str, analysis_type: str) -> Dict[str, Any]:
        """
        调用火山引擎豆包API
        
        Args:
            system_prompt: 系统提示词
            user_prompt: 用户提示词
            analysis_type: 分析类型
            
        Returns:
            API响应结果
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "model": self.text_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "max_tokens": 1024,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(
                f"{self.ark_base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=60
            )
            
            response.raise_for_status()
            result = response.json()
            
            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0]["message"]["content"].strip()
                
                # 尝试解析JSON格式的响应
                try:
                    parsed_content = json.loads(content)
                    return {
                        "analysis_type": analysis_type,
                        "content": parsed_content,
                        "raw_content": content,
                        "status": "success"
                    }
                except json.JSONDecodeError:
                    # 如果不是JSON格式，返回原始文本
                    return {
                        "analysis_type": analysis_type,
                        "content": {"text": content},
                        "raw_content": content,
                        "status": "success"
                    }
            else:
                raise Exception("API响应格式异常")
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"API调用失败: {e}")
        except json.JSONDecodeError as e:
            raise Exception(f"解析API响应失败: {e}")
        except Exception as e:
            raise Exception(f"未知错误: {e}")
    
    def extract_personality_scores(self, personality_analysis: Dict) -> Dict[str, int]:
        """
        从性格分析结果中提取Big Five评分
        
        Args:
            personality_analysis: 性格分析结果
            
        Returns:
            Big Five评分字典
        """
        scores = {
            'openness': 50,
            'conscientiousness': 50,
            'extraversion': 50,
            'agreeableness': 50,
            'neuroticism': 50
        }
        
        try:
            content = personality_analysis.get('content', {})
            
            # 尝试从不同格式的响应中提取评分
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
            
            # 如果无法提取，使用默认值
            if all(score == 50 for score in scores.values()):
                print("⚠️  无法从AI分析中提取具体评分，使用默认值")
                
        except Exception as e:
            print(f"⚠️  提取性格评分时出错: {e}")
        
        return scores
