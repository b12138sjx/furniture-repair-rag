import os
import json
import subprocess
import sys
from typing import List, Dict

class CrawlerService:
    """爬虫服务类"""
    
    def __init__(self, data_dir="data/raw"):
        self.data_dir = data_dir
        self.crawler_script = os.path.join(data_dir, "web scrap.py")
        
    def run_crawler(self) -> Dict:
        """运行爬虫获取最新数据"""
        try:
            print("🕷️ 启动爬虫服务...")
            
            # 切换到数据目录
            original_dir = os.getcwd()
            os.chdir(self.data_dir)
            
            # 运行爬虫脚本
            result = subprocess.run([
                sys.executable, "web scrap.py"
            ], capture_output=True, text=True, timeout=300)
            
            # 恢复目录
            os.chdir(original_dir)
            
            if result.returncode == 0:
                print("✅ 爬虫运行成功")
                return {
                    "success": True,
                    "message": "爬虫运行成功",
                    "output": result.stdout,
                    "files_updated": self.get_updated_files()
                }
            else:
                print(f"❌ 爬虫运行失败: {result.stderr}")
                return {
                    "success": False,
                    "message": "爬虫运行失败",
                    "error": result.stderr
                }
                
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "message": "爬虫运行超时"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"爬虫运行错误: {str(e)}"
            }
    
    def get_updated_files(self) -> List[str]:
        """获取更新的文件列表"""
        files = []
        for filename in ["phone.json", "phone urls.txt"]:
            filepath = os.path.join(self.data_dir, filename)
            if os.path.exists(filepath):
                files.append(filepath)
        return files
    
    def load_crawled_data(self) -> List[Dict]:
        """加载爬取的数据"""
        json_file = os.path.join(self.data_dir, "phone.json")
        
        if not os.path.exists(json_file):
            print(f"⚠️ 爬取数据文件不存在: {json_file}")
            return []
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"✅ 成功加载 {len(data)} 条爬取数据")
                return data
        except Exception as e:
            print(f"❌ 加载爬取数据失败: {e}")
            return []
    
    def get_crawler_status(self) -> Dict:
        """获取爬虫状态"""
        json_file = os.path.join(self.data_dir, "phone.json")
        urls_file = os.path.join(self.data_dir, "phone urls.txt")
        
        status = {
            "data_file_exists": os.path.exists(json_file),
            "urls_file_exists": os.path.exists(urls_file),
            "data_count": 0,
            "urls_count": 0,
            "last_updated": None
        }
        
        if status["data_file_exists"]:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    status["data_count"] = len(data)
                status["last_updated"] = os.path.getmtime(json_file)
            except:
                pass
        
        if status["urls_file_exists"]:
            try:
                with open(urls_file, 'r', encoding='utf-8') as f:
                    urls = [line.strip() for line in f if line.strip()]
                    status["urls_count"] = len(urls)
            except:
                pass
        
        return status

# 全局爬虫服务实例
crawler_service = CrawlerService()
