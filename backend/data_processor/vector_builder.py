from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma


def create_vector_db(docs, persist_directory='./data/processed/vectors'):
    embeddings = HuggingFaceEmbeddings(model_name='BAAI/bge-large-zh')
    vectordb = Chroma.from_documents(docs, embeddings, persist_directory=persist_directory)
    vectordb.persist()
    return vectordb