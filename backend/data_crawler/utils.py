import re
import os
from typing import List, Dict, Optional


def clean_text(text):
    """去除多余的空白字符"""
    cleaned = re.sub(r'\s+', ' ', text).strip()
    return cleaned


def should_remove_block(text_block: str) -> bool:
    """判断是否应该移除文本块（UI元素等噪音）"""
    ui_keywords = ["编辑", "添加一条评论", "编辑指南", "显示更多", "上一页", "下一页", "小——", "中——", "大——"]
    pixel_pattern = re.compile(r"[小中大][—\-–—]{1,2}\s*\d{2,4}\s*像素")
    return any(kw in text_block for kw in ui_keywords) or pixel_pattern.search(text_block)


def extract_main_content(soup):
    """从BeautifulSoup对象中提取主要内容"""
    main_content = soup.find("article") or soup.find("main") or soup.body
    
    # 移除不需要的标签
    for tag in main_content(['script', 'style', 'noscript', 'footer', 'nav', 'aside']):
        tag.decompose()
    
    return main_content


def normalize_url(url, base_domain):
    """标准化URL格式"""
    if not url.startswith("http"):
        url = base_domain + url
    if "lang=" not in url:
        url += "?lang=en"
    return url


def is_valid_furniture_content(text):
    """判断文本是否包含有效的家具维修内容"""
    # 扩展关键词以包含更多维修相关术语
    furniture_keywords = [
        "维修", "修理", "保养", "家具", "沙发", "桌子", "椅子", "床", "柜子",
        "repair", "fix", "maintenance", "furniture", "sofa", "table", "chair", "bed", "cabinet",
        "replacement", "battery", "screen", "camera", "speaker", "antenna", "engine",
        "拆解", "安装", "更换", "步骤", "工具", "螺丝", "adhesive", "assembly"
    ]
    text_lower = text.lower()
    return any(keyword.lower() in text_lower for keyword in furniture_keywords)


def extract_repair_steps(content: str) -> List[str]:
    """提取维修步骤"""
    step_pattern = re.compile(r'步骤\s*\d+|Step\s*\d+|^\d+\.', re.MULTILINE)
    steps = []
    
    lines = content.split('\n')
    current_step = []
    
    for line in lines:
        line = line.strip()
        if step_pattern.match(line):
            if current_step:
                steps.append('\n'.join(current_step))
                current_step = []
            current_step.append(line)
        elif current_step and line:
            current_step.append(line)
    
    if current_step:
        steps.append('\n'.join(current_step))
    
    return steps


def get_file_stats(file_path: str) -> Dict:
    """获取文件统计信息"""
    if not os.path.exists(file_path):
        return {}
    
    stat = os.stat(file_path)
    return {
        'size_bytes': stat.st_size,
        'size_mb': round(stat.st_size / 1024 / 1024, 2),
        'modified_time': stat.st_mtime
    }


def create_summary_report(data: Dict) -> str:
    """创建数据摘要报告"""
    report = []
    report.append("📋 数据整合摘要报告")
    report.append("=" * 40)
    
    if 'stats' in data:
        stats = data['stats']
        report.append(f"📄 文档总数: {stats.get('total_documents', 0)}")
        report.append(f"🔗 URL总数: {stats.get('total_urls', 0)}")
        if 'json_documents' in stats:
            report.append(f"📱 JSON文档数: {stats['json_documents']}")
    
    if 'documents' in data:
        docs = data['documents']
        if docs:
            avg_length = sum(doc['metadata'].get('length', 0) for doc in docs) / len(docs)
            report.append(f"📏 平均文档长度: {int(avg_length)} 字符")
            
            types = {}
            for doc in docs:
                doc_type = doc['metadata'].get('type', 'unknown')
                types[doc_type] = types.get(doc_type, 0) + 1
            
            report.append("📊 文档类型分布:")
            for doc_type, count in types.items():
                report.append(f"   - {doc_type}: {count}")
    
    return '\n'.join(report)