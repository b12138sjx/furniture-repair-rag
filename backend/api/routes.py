from fastapi import APIRouter, UploadFile, File
from .rag_chain_helper import get_rag_chain
import os

router = APIRouter()

@router.post('/upload')
def upload_file(file: UploadFile = File(...)):
    save_path = os.path.join('data/raw/user_uploads', file.filename)
    with open(save_path, 'wb') as f:
        f.write(file.file.read())
    return {'message': 'File uploaded successfully'}

@router.get('/qa')
def get_answer(query: str):
    rag_chain = get_rag_chain()
    answer = rag_chain.run(query)
    return {'answer': answer}