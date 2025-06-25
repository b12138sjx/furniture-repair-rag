from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from .llm_interface import LLMInterface


# 设计家具维修领域专用的 Prompt 模板
prompt_template = '''你是一名专业的家具维修专家。请根据以下提供的背景信息，回答用户关于家具维修的问题。

背景信息：{context}

问题：{question}
回答：'''  # noqa: E501
PROMPT = PromptTemplate(template=prompt_template, input_variables=['context', 'question'])


class RAGChain:
    def __init__(self, vector_db, model_name='gpt-3.5-turbo'):
        self.llm_interface = LLMInterface(model_name)
        self.qa = RetrievalQA.from_chain_type(
            llm=self.llm_interface.llm,
            chain_type='stuff',
            retriever=vector_db.as_retriever(),
            chain_type_kwargs={'prompt': PROMPT}
        )

    def run(self, query):
        return self.qa.run(query)