import requests
from bs4 import BeautifulSoup

class FurnitureCrawler:
    def __init__(self, start_urls):
        self.start_urls = start_urls

    def crawl(self):
        for url in self.start_urls:
            try:
                response = requests.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                # 这里添加 HTML 解析、文本提取和基本清洗功能
                print('Crawled:', url)
            except Exception as e:
                print('Error crawling', url, ':', e)