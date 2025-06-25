import json
import os
from typing import List, Dict, Optional
from .utils import clean_text, is_valid_furniture_content

class DataLoader:
    """加载和处理已有的爬虫数据"""
    
    @staticmethod
    def load_urls_from_file(file_path: str) -> List[str]:
        """从txt文件加载URL列表"""
        urls = []
        if not os.path.exists(file_path):
            print(f"文件不存在: {file_path}")
            return urls
            
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                url = line.strip()
                if url:
                    urls.append(url)
        return urls
    
    @staticmethod
    def load_content_from_json(file_path: str) -> List[Dict]:
        """从JSON文件加载内容数据"""
        if not os.path.exists(file_path):
            print(f"文件不存在: {file_path}")
            return []
            
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @staticmethod
    def convert_to_documents(json_data: List[Dict], content_type: str = "repair_guide") -> List[Dict]:
        """将JSON数据转换为文档格式，适配RAG系统"""
        documents = []
        for i, item in enumerate(json_data):
            # 清洗和验证内容
            content = item.get('content', '')
            title = item.get('title', '')
            
            if not content or len(content.strip()) < 50:
                continue
                
            # 进一步清洗内容
            clean_content = clean_text(content)
            
            # 检查是否为有效的维修内容
            if not is_valid_furniture_content(clean_content):
                print(f"跳过非相关内容: {title[:50]}...")
                continue
            
            doc = {
                'content': clean_content,
                'metadata': {
                    'source': item.get('url', f'document_{i}'),
                    'title': title,
                    'type': content_type,
                    'doc_id': f"{content_type}_{i}",
                    'length': len(clean_content)
                }
            }
            documents.append(doc)
        return documents
    
    @staticmethod
    def merge_data_sources(phone_json_path: str, phone_urls_path: str) -> Dict:
        """合并多个数据源"""
        result = {
            'documents': [],
            'urls': [],
            'stats': {}
        }
        
        # 加载JSON内容数据
        if os.path.exists(phone_json_path):
            json_data = DataLoader.load_content_from_json(phone_json_path)
            documents = DataLoader.convert_to_documents(json_data, "phone_repair_guide")
            result['documents'].extend(documents)
            result['stats']['json_documents'] = len(documents)
        
        # 加载URL列表
        if os.path.exists(phone_urls_path):
            urls = DataLoader.load_urls_from_file(phone_urls_path)
            result['urls'].extend(urls)
            result['stats']['total_urls'] = len(urls)
        
        result['stats']['total_documents'] = len(result['documents'])
        return result
    
    @staticmethod
    def save_processed_data(data: Dict, output_path: str):
        """保存处理后的数据"""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"已保存处理后的数据到: {output_path}")
