import os
import shutil
from typing import Dict, List
from .data_loader import DataLoader
from .furniture_crawler import FurnitureCrawler

class DataIntegration:
    """整合现有数据和新爬虫功能"""
    
    def __init__(self, base_dir: str = "data"):
        self.base_dir = base_dir
        self.raw_data_dir = os.path.join(base_dir, "raw")
        self.processed_data_dir = os.path.join(base_dir, "processed")
        self.ensure_directories()
    
    def ensure_directories(self):
        """确保目录存在"""
        os.makedirs(self.raw_data_dir, exist_ok=True)
        os.makedirs(self.processed_data_dir, exist_ok=True)
    
    def migrate_our_data(self, our_data_path: str = "our_data"):
        """迁移our_data目录下的数据"""
        if not os.path.exists(our_data_path):
            print(f"源目录不存在: {our_data_path}")
            return
        
        # 复制文件到新的数据目录
        for filename in os.listdir(our_data_path):
            src_path = os.path.join(our_data_path, filename)
            dst_path = os.path.join(self.raw_data_dir, filename)
            
            if os.path.isfile(src_path):
                shutil.copy2(src_path, dst_path)
                print(f"已迁移: {filename}")
    
    def process_existing_data(self) -> Dict:
        """处理现有数据"""
        phone_json_path = os.path.join(self.raw_data_dir, "phone.json")
        phone_urls_path = os.path.join(self.raw_data_dir, "phone urls.txt")
        
        # 合并数据源
        merged_data = DataLoader.merge_data_sources(phone_json_path, phone_urls_path)
        
        # 保存处理后的数据
        output_path = os.path.join(self.processed_data_dir, "integrated_repair_data.json")
        DataLoader.save_processed_data(merged_data, output_path)
        
        return merged_data
    
    def run_new_crawl(self, start_urls: List[str] = None) -> Dict:
        """运行新的爬虫任务"""
        if start_urls is None:
            start_urls = ["/Device/Furniture"]  # 可以改为家具相关的起始URL
        
        crawler = FurnitureCrawler(start_urls)
        
        # 设置输出路径
        output_json = os.path.join(self.processed_data_dir, "new_crawl_results.json")
        output_urls = os.path.join(self.raw_data_dir, "new_urls.txt")
        
        # 执行爬取
        results = crawler.crawl(output_json, output_urls)
        
        return {
            'documents': DataLoader.convert_to_documents(results, "new_furniture_guide"),
            'urls': list(crawler.saved_links),
            'stats': {
                'total_documents': len(results),
                'total_urls': len(crawler.saved_links)
            }
        }
    
    def create_unified_dataset(self) -> Dict:
        """创建统一的数据集"""
        print("🔄 开始整合数据...")
        
        # 1. 迁移现有数据
        self.migrate_our_data()
        
        # 2. 处理现有数据
        existing_data = self.process_existing_data()
        
        # 3. 创建统一数据集
        unified_data = {
            'metadata': {
                'source': 'integrated_dataset',
                'version': '1.0',
                'description': '整合的家具/设备维修知识库'
            },
            'documents': existing_data['documents'],
            'urls': existing_data['urls'],
            'stats': existing_data['stats']
        }
        
        # 4. 保存统一数据集
        unified_path = os.path.join(self.processed_data_dir, "unified_repair_dataset.json")
        DataLoader.save_processed_data(unified_data, unified_path)
        
        print(f"✅ 数据整合完成!")
        print(f"📊 统计信息:")
        print(f"   - 文档数量: {unified_data['stats']['total_documents']}")
        print(f"   - URL数量: {unified_data['stats']['total_urls']}")
        print(f"   - 数据文件: {unified_path}")
        
        return unified_data

def main():
    """主函数 - 执行数据整合"""
    integration = DataIntegration()
    result = integration.create_unified_dataset()
    return result

if __name__ == "__main__":
    main()
