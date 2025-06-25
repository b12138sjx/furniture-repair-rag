import os
from dotenv import load_dotenv

load_dotenv()

# 向量数据库存储路径
VECTOR_DB_PATH = os.getenv('VECTOR_DB_PATH', './data/processed/vectors')

# 默认大模型名称
DEFAULT_LLM_MODEL = os.getenv('DEFAULT_LLM_MODEL', 'gpt-3.5-turbo')

# 文本分块大小
CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', 1000))
# 文本块重叠大小
CHUNK_OVERLAP = int(os.getenv('CHUNK_OVERLAP', 200))