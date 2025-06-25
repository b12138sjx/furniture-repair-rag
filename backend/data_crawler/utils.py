import re


def clean_text(text):
    # 去除多余的空白字符
    cleaned = re.sub('\s+', ' ', text).strip()
    return cleaned