import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.rag_chain import RAGChain
from data_processor.vector_builder import create_vector_db
from data_processor.document_processor import load_documents, split_documents

_rag_chain = None

def get_rag_chain():
    global _rag_chain
    if _rag_chain is None:
        try:
            docs = []
            sample_dir = 'data/samples/furniture_docs'
            
            # 如果样本目录不存在，使用已有的手机维修数据
            if not os.path.exists(sample_dir):
                sample_dir = 'data/raw'
            
            for root, _, files in os.walk(sample_dir):
                for file in files:
                    if file.endswith(('.txt', '.md', '.pdf', '.json')):
                        file_path = os.path.join(root, file)
                        try:
                            loaded_docs = load_documents(file_path)
                            split_docs = split_documents(loaded_docs)
                            docs.extend(split_docs)
                        except Exception as e:
                            print(f"处理文件 {file_path} 时出错: {e}")
                            continue
            
            if not docs:
                # 如果没有文档，创建一个默认文档
                from langchain.schema import Document
                docs = [Document(
                    page_content="这是一个家具维修知识库系统，可以回答关于家具维修、保养等问题。",
                    metadata={"source": "default"}
                )]
            
            vector_db = create_vector_db(docs)
            _rag_chain = RAGChain(vector_db)
        except Exception as e:
            print(f"初始化RAG链时出错: {e}")
            # 返回一个简单的模拟对象
            class MockRAGChain:
                def qa(self, inputs):
                    return {
                        'result': f"关于'{inputs['query']}'的问题，这是一个模拟回答。请确保后端服务正常运行。",
                        'source_documents': []
                    }
            _rag_chain = MockRAGChain()
    
    return _rag_chain