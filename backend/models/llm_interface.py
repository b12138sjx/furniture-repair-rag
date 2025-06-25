from langchain.llms import HuggingFaceHub
from langchain.chat_models import ChatOpenAI
import os

class LLMInterface:
    def __init__(self, model_name='gpt-3.5-turbo'):
        if model_name == 'gpt-3.5-turbo':
            self.llm = ChatOpenAI(openai_api_key=os.getenv('OPENAI_API_KEY'))
        elif model_name.startswith('huggingface/'):
            repo_id = model_name.split('huggingface/')[1]
            self.llm = HuggingFaceHub(repo_id=repo_id, huggingfacehub_api_token=os.getenv('HUGGINGFACEHUB_API_TOKEN'))
        else:
            raise ValueError('Unsupported model name')

    def generate(self, prompt):
        return self.llm(prompt)