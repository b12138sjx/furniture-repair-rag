from backend.models.rag_chain import RAGChain
from backend.data_processor.vector_builder import create_vector_db
from backend.data_processor.document_processor import load_documents, split_documents
import os

_rag_chain = None

def get_rag_chain():
    global _rag_chain
    if _rag_chain is None:
        # 加载示例数据
        docs = []
        sample_dir = 'data/samples/furniture_docs'
        for root, _, files in os.walk(sample_dir):
            for file in files:
                file_path = os.path.join(root, file)
                loaded_docs = load_documents(file_path)
                split_docs = split_documents(loaded_docs)
                docs.extend(split_docs)
        vector_db = create_vector_db(docs)
        _rag_chain = RAGChain(vector_db)
    return _rag_chain