import requests
from bs4 import BeautifulSoup
import re
import os
import json
import urllib3
from .utils import clean_text

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class FurnitureCrawler:
    def __init__(self, start_urls=None, base_domain="https://zh.ifixit.com"):
        self.start_urls = start_urls or ["/Device/Huawei_P"]
        self.base_domain = base_domain
        self.visited_pages = set()
        self.saved_links = set()
        
        self.valid_crawl_prefixes = ["/Device/", "/Guide/", "/Wiki/"]
        self.valid_save_prefixes = ["/Guide/", "/Wiki/"]
        self.excluded_keywords = [
            "/edit/", "/translate/", "/history/",
            "/Edit/", "/Translate/", "/History/"
        ]
        
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/114.0.0.0 Safari/537.36"
        }

    def should_visit(self, href):
        return (
            href.startswith("/") and
            any(href.startswith(prefix) for prefix in self.valid_crawl_prefixes) and
            not any(excluded in href for excluded in self.excluded_keywords)
        )

    def is_valid_save_url(self, href):
        return (
            any(href.startswith(prefix) for prefix in self.valid_save_prefixes) and
            not any(x in href for x in self.excluded_keywords) and
            re.search(r"/\d+$", href)
        )

    def crawl_page(self, path):
        if any(excluded in path for excluded in self.excluded_keywords):
            print(f"⛔ 跳过禁止访问页面: {path}")
            return

        full_url = self.base_domain + path
        if full_url in self.visited_pages:
            return
        print(f"📄 正在访问: {full_url}")
        self.visited_pages.add(full_url)

        try:
            response = requests.get(full_url, headers=self.headers, timeout=10, verify=False)
            response.raise_for_status()
        except Exception as e:
            print(f"❌ 抓取失败: {full_url} 原因: {e}")
            return

        soup = BeautifulSoup(response.text, "html.parser")
        for a_tag in soup.find_all("a", href=True):
            href = a_tag['href'].split("#")[0].strip()
            if not self.should_visit(href):
                continue

            if self.is_valid_save_url(href):
                url = self.base_domain + href
                if "lang=" not in url:
                    url += "?lang=en"
                self.saved_links.add(url)
            else:
                self.crawl_page(href)

    def fetch_clean_text_and_title(self, url: str):
        try:
            response = requests.get(url, headers=self.headers, timeout=10, verify=False)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            title = soup.title.string.strip() if soup.title and soup.title.string else ""
            main_content = soup.find("article") or soup.find("main") or soup.body

            for tag in main_content(['script', 'style', 'noscript', 'footer', 'nav', 'aside']):
                tag.decompose()

            raw_text = main_content.get_text(separator="\n", strip=True)
            lines = [line.strip() for line in raw_text.splitlines() if line.strip()]

            # 使用 utils 中的清洗功能
            clean_lines = [clean_text(line) for line in lines if not self._is_noise(line)]
            clean_text_content = "\n".join(clean_lines)

            return {"url": url, "title": title, "content": clean_text_content}

        except Exception as e:
            print(f"[ERROR] 抓取失败：{url}  原因：{e}")
            return None

    def _is_noise(self, line: str) -> bool:
        exact_phrases = [
            "由衷感谢以下译者：", "修复你的物品", "跳转到主内容", "社区", "商店", "翻译",
            "回复", "添加评论", "取消", "发帖评论"
        ]

        partial_keywords = [
            "作者", "与", "的会员", "团队", "徽章", "创作了", "声望", "注册", "名成员",
            "Author", "Registered on", "reputation", "Created", "guides",
            "Badges", "more badges", "Team", "member of", "Community", "members",
            "Thanks", "thank you", "Grazie", "grandissimo lavoro", "special thanks",
            "Harry Mao", "Ennis", "Alisha C", "Vincenzo Garletti", "Tozyel Lagaffe"
        ]

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

        if line in exact_phrases:
            return True
        if any(keyword in line for keyword in partial_keywords):
            return True
        if any(pat.search(line) for pat in regex_patterns):
            return True
        return False

    def crawl(self, output_json="clean_results_cleaned.json", output_urls="urls.txt"):
        # 开始爬取
        for start_path in self.start_urls:
            self.crawl_page(start_path)

        # 保存链接
        new_links = sorted(self.saved_links)
        os.makedirs(os.path.dirname(output_urls) if os.path.dirname(output_urls) else '.', exist_ok=True)
        
        with open(output_urls, "w", encoding="utf-8") as f:
            for url in new_links:
                f.write(url + "\n")

        print(f"\n✅ 共保存 {len(new_links)} 条可抓取内容链接到：{output_urls}")

        # 抓取内容并清洗
        results = []
        for idx, url in enumerate(new_links, 1):
            print(f"\n[{idx}/{len(new_links)}] 正在抓取并清洗：{url}")
            item = self.fetch_clean_text_and_title(url)
            if item and item["content"]:
                results.append(item)
                print(f"✔️ 抓取成功：{len(item['content'])} 字符")
            else:
                print("⚠️ 跳过空页面或失败页面")

        # 保存结果
        os.makedirs(os.path.dirname(output_json) if os.path.dirname(output_json) else '.', exist_ok=True)
        with open(output_json, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        print(f"\n🎉 所有处理结果已保存为：{output_json}")
        return results