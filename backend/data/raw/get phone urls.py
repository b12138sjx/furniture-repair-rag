import requests
from bs4 import BeautifulSoup
import re
import time
import os

BASE_DOMAIN = "https://zh.ifixit.com"
START_PATHS = [#"/Device/Huawei_Mate",
               "/Device/Huawei_Honor",
               "/Device/Sony_Phone_E_Series",
               "/Device/Sony_Phone_X_Series",
               "/Device/Sony_Phone_XA_Series",
               "/Device/Sony_Phone_XZ_Series",
               "/Device/Sony_Phone_Z_Series",
               "/Device/Google_Phone",
               "/Device/Jolla",
               "/Device/Pine64_PinePhone",
               ]

visited_pages = set()
saved_links = set()

# 允许访问的前缀
VALID_CRAWL_PREFIXES = ["/Device/", "/Guide/", "/Wiki/"]

# 允许保存的前缀
VALID_SAVE_PREFIXES = ["/Guide/", "/Wiki/"]

# 排除保存和访问的关键词
EXCLUDED_KEYWORDS = [
    "/edit/",
    "/translate/",
    "/history/",
    "/Edit/",
    "/Translate/",
    "/History/",
]

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
        response = requests.get(full_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ 抓取失败: {full_url} 原因: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    for a_tag in soup.find_all("a", href=True):
        href = a_tag['href'].split("#")[0].strip()  # 去除锚点和空白
        if not should_visit(href):
            continue

        if is_valid_save_url(href):
            url = BASE_DOMAIN + href
            if "lang=" not in url:
                url += "?lang=zh"
            saved_links.add(url)
        else:
            crawl_page(href)

def main(output_file="urls.txt"):
    existing_links = set()
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            existing_links = set(line.strip() for line in f if line.strip())

    for start_path in START_PATHS:
        crawl_page(start_path)

    new_links = sorted(saved_links - existing_links)

    with open(output_file, "a", encoding="utf-8") as f:
        for url in new_links:
            f.write(url + "\n")

    print(f"\n✅ 本次新增链接数：{len(new_links)}，已追加至：{output_file}")

if __name__ == "__main__":
    main()
