import requests
from bs4 import BeautifulSoup
import re
import os
import json
import urllib3
import time
from typing import List, Dict, Optional

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_DOMAIN = "https://zh.ifixit.com"
START_PATHS = ["/Device/Huawei_P"]

visited_pages = set()
saved_links = set()

VALID_CRAWL_PREFIXES = ["/Device/", "/Guide/", "/Wiki/"]
VALID_SAVE_PREFIXES = ["/Guide/", "/Wiki/"]
EXCLUDED_KEYWORDS = [
    "/edit/", "/translate/", "/history/",
    "/Edit/", "/Translate/", "/History/"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/114.0.0.0 Safari/537.36"
}

def should_visit(href):
    return (
        href.startswith("/") and
        any(href.startswith(prefix) for prefix in VALID_CRAWL_PREFIXES) and
        not any(excluded in href for excluded in EXCLUDED_KEYWORDS)
    )

def is_valid_save_url(href):
    return (
        any(href.startswith(prefix) for prefix in VALID_SAVE_PREFIXES) and
        not any(x in href for x in EXCLUDED_KEYWORDS) and
        re.search(r"/\d+$", href)
    )

def crawl_page(path):
    if any(excluded in path for excluded in EXCLUDED_KEYWORDS):
        print(f"⛔ 跳过禁止访问页面: {path}")
        return

    full_url = BASE_DOMAIN + path
    if full_url in visited_pages:
        return
    print(f"📄 正在访问: {full_url}")
    visited_pages.add(full_url)

    try:
        response = requests.get(full_url, headers=HEADERS, timeout=10, verify=False)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ 抓取失败: {full_url} 原因: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    for a_tag in soup.find_all("a", href=True):
        href = a_tag['href'].split("#")[0].strip()
        if not should_visit(href):
            continue

        if is_valid_save_url(href):
            url = BASE_DOMAIN + href
            if "lang=" not in url:
                url += "?lang=zh"
            saved_links.add(url)
        else:
            crawl_page(href)

def load_urls_from_file(file_path: str = "phone urls.txt") -> List[str]:
    """从文件加载已有的URL列表"""
    urls = []
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                url = line.strip()
                if url and url.startswith('http'):
                    urls.append(url)
        print(f"📂 从文件加载了 {len(urls)} 个URL")
    return urls

def fetch_clean_text_and_title(url: str) -> Optional[Dict]:
    """抓取并清洗单个URL的内容"""
    try:
        print(f"🔄 正在抓取: {url}")
        response = requests.get(url, headers=HEADERS, timeout=15, verify=False)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        # 提取标题
        title = ""
        title_selectors = [
            "h1.pagetitle",
            "h1",
            "title"
        ]
        for selector in title_selectors:
            title_elem = soup.select_one(selector)
            if title_elem:
                title = title_elem.get_text(strip=True)
                break

        # 提取主要内容
        main_content = None
        content_selectors = [
            "article",
            ".guide-content", 
            ".wiki-content",
            "main",
            "#main-content",
            ".content"
        ]
        
        for selector in content_selectors:
            main_content = soup.select_one(selector)
            if main_content:
                break
        
        if not main_content:
            main_content = soup.body

        # 移除不需要的元素
        unwanted_selectors = [
            'script', 'style', 'noscript', 'footer', 'nav', 'aside',
            '.advertisement', '.ads', '.social-share', '.comments',
            '.breadcrumb', '.sidebar', '.header', '.navigation'
        ]
        
        for selector in unwanted_selectors:
            for element in main_content.select(selector):
                element.decompose()

        # 提取文本
        raw_text = main_content.get_text(separator="\n", strip=True)
        lines = [line.strip() for line in raw_text.splitlines() if line.strip()]

        # 清理噪音文本
        clean_lines = clean_text_lines(lines)
        clean_text = "\n".join(clean_lines)

        # 验证内容质量
        if len(clean_text) < 100:
            print(f"⚠️  内容太短，跳过: {url}")
            return None

        result = {
            "url": url,
            "title": title,
            "content": clean_text
        }
        
        print(f"✅ 成功抓取: {title} ({len(clean_text)} 字符)")
        return result

    except Exception as e:
        print(f"❌ 抓取失败: {url} - {e}")
        return None

def clean_text_lines(lines: List[str]) -> List[str]:
    """清理文本行，移除噪音"""
    
    # 要完全移除的短语
    exact_phrases = [
        "由衷感谢以下译者：", "修复你的物品", "跳转到主内容", "社区", "商店", "翻译",
        "回复", "添加评论", "取消", "发帖评论", "编辑", "历史", "工具", "零件",
        "难度", "步骤", "时间要求", "iPhone", "Android", "Mac", "PC"
    ]

    # 部分关键词
    partial_keywords = [
        "作者", "与", "的会员", "团队", "徽章", "创作了", "声望", "注册", "名成员",
        "Author", "Registered on", "reputation", "Created", "guides",
        "Badges", "more badges", "Team", "member of", "Community", "members",
        "Thanks", "thank you", "Grazie", "grandissimo lavoro", "special thanks"
    ]

    # 正则表达式模式
    regex_patterns = [
        re.compile(r"浏览统计数据[:：]?$"),
        re.compile(r"过去\s*(24\s*小时|7\s*天|30\s*天)[：:]?$"),
        re.compile(r"^总计[：:]?$"),
        re.compile(r"(过去\s?\d+\s?[天小时]+|总计)\s?[：:]\s?[\d,]+"),
        re.compile(r"^\s*[\d,]+\s*$"),
        re.compile(r"^\s*\d+%?\s*$"),
        re.compile(r"^\s*(en|zh)\s*$", re.IGNORECASE),
        re.compile(r"^\d{4}[年/-]\d{1,2}[月/-]\d{1,2}"),
        re.compile(r"^\w+\s+\w+\s*-\s*\d{4}"),
        re.compile(r"于\d{1,2}/\d{1,2}/\d{2,4}注册"),
        re.compile(r"\d{1,3}(,\d{3})*\s*声望"),
        re.compile(r"\d{1,3}(,\d{3})*\s*reputation", re.I),
        re.compile(r"创作了\d+\s*篇指南"),
        re.compile(r"Created\s+\d+\s+guides", re.I),
        re.compile(r"\+?\s*\d+\s*更多徽章"),
        re.compile(r"Badges[:：]?\s*\+?\d+\s+more", re.I),
        re.compile(r"\d+\s*名成员"),
        re.compile(r"\d+\s*members", re.I),
    ]

    def is_noise(line: str) -> bool:
        line_lower = line.lower()
        
        # 检查完全匹配
        if line in exact_phrases:
            return True
            
        # 检查部分关键词
        if any(keyword.lower() in line_lower for keyword in partial_keywords):
            return True
            
        # 检查正则表达式
        if any(pattern.search(line) for pattern in regex_patterns):
            return True
            
        # 过滤过短的行
        if len(line) < 3:
            return True
            
        return False

    return [line for line in lines if not is_noise(line)]

def batch_crawl_from_urls(url_file: str = "phone urls.txt", 
                         output_file: str = "phone.json",
                         start_index: int = 0,
                         max_urls: int = 50) -> List[Dict]:
    """批量抓取URL列表中的内容"""
    
    # 加载URL列表
    urls = load_urls_from_file(url_file)
    if not urls:
        print("❌ 没有找到可用的URL")
        return []
    
    # 限制抓取数量
    urls_to_crawl = urls[start_index:start_index + max_urls]
    print(f"📋 准备抓取 {len(urls_to_crawl)} 个URL (索引 {start_index} 到 {start_index + len(urls_to_crawl)})")
    
    results = []
    success_count = 0
    
    for i, url in enumerate(urls_to_crawl, 1):
        print(f"\n[{i}/{len(urls_to_crawl)}] 处理URL...")
        
        # 抓取内容
        item = fetch_clean_text_and_title(url)
        if item and item["content"]:
            # 进一步过滤
            filtered_lines = [line for line in item["content"].splitlines() 
                            if not should_remove_block(line)]
            item["content"] = "\n".join(filtered_lines).strip()
            
            if len(item["content"]) > 200:  # 确保内容足够长
                results.append(item)
                success_count += 1
                print(f"✅ 成功处理第 {success_count} 条数据")
            else:
                print(f"⚠️  内容过短，跳过")
        else:
            print(f"❌ 抓取失败或内容为空")
        
        # 添加延时避免被封
        if i % 5 == 0:  # 每5个请求休息一下
            print("😴 休息 2 秒...")
            time.sleep(2)
        else:
            time.sleep(0.5)
    
    # 保存结果
    if results:
        # 读取现有数据
        existing_data = []
        if os.path.exists(output_file):
            try:
                with open(output_file, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
            except:
                existing_data = []
        
        # 合并数据（避免重复）
        existing_urls = {item.get('url', '') for item in existing_data}
        new_results = [item for item in results if item['url'] not in existing_urls]
        
        if new_results:
            all_data = existing_data + new_results
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(all_data, f, ensure_ascii=False, indent=2)
            
            print(f"\n🎉 成功保存 {len(new_results)} 条新数据到 {output_file}")
            print(f"📊 文件总计包含 {len(all_data)} 条数据")
        else:
            print(f"\n⚠️  没有新数据需要保存")
    else:
        print(f"\n❌ 没有成功抓取到任何数据")
    
    return results

def should_remove_block(text_block: str) -> bool:
    ui_keywords = ["编辑", "添加一条评论", "编辑指南", "显示更多", "上一页", "下一页", "小——", "中——", "大——"]
    pixel_pattern = re.compile(r"[小中大][—\-–—]{1,2}\s*\d{2,4}\s*像素")
    return any(kw in text_block for kw in ui_keywords) or pixel_pattern.search(text_block)

def run_full_process(output_json="phone.json", output_urls="phone urls.txt"):
    """运行完整的爬取流程"""
    print("🚀 开始完整爬取流程...")
    
    # 选择运行模式
    print("\n选择运行模式:")
    print("1. 从已有URL文件批量抓取 (推荐)")
    print("2. 重新爬取URL然后抓取内容")
    
    choice = input("请选择 (1 或 2): ").strip()
    
    if choice == "1":
        # 从已有URL抓取
        start_index = int(input("起始索引 (默认0): ") or "0")
        max_urls = int(input("最大抓取数量 (默认20): ") or "20")
        batch_crawl_from_urls(output_urls, output_json, start_index, max_urls)
    else:
        # 重新爬取URL
        for start_path in START_PATHS:
            crawl_page(start_path)

        new_links = sorted(saved_links)
        with open(output_urls, "w", encoding="utf-8") as f:
            for url in new_links:
                f.write(url + "\n")

        print(f"\n✅ 共保存 {len(new_links)} 条链接到：{output_urls}")
        
        # 然后抓取内容
        if new_links:
            max_urls = int(input("抓取多少个URL的内容 (默认10): ") or "10")
            batch_crawl_from_urls(output_urls, output_json, 0, max_urls)

if __name__ == "__main__":
    run_full_process()
