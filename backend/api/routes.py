from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from pydantic import BaseModel
from api.models import UploadResponse, QAResponse, ErrorResponse
from api.rag_chain_helper import get_rag_chain
import os
import uuid

router = APIRouter()

class CollectRequest(BaseModel):
    url: str

@router.post('/upload', response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    try:
        file_id = str(uuid.uuid4())
        file_ext = os.path.splitext(file.filename)[1]
        save_path = os.path.join('data/raw/user_uploads', f"{file_id}{file_ext}")
        
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        contents = await file.read()
        
        with open(save_path, 'wb') as f:
            f.write(contents)
            
        return UploadResponse(
            success=True,
            message=f'文件 {file.filename} 上传成功',
            file_id=file_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/qa', response_model=QAResponse)
async def get_answer(
    query: str = Query(..., description="用户的问题"),
    context_size: int = Query(3, description="返回的相关上下文数量")
):
    try:
        rag_chain = get_rag_chain()
        # 修改为同步调用，因为rag_chain可能不支持异步
        result = rag_chain.qa({"query": query})
        answer = result.get('result', '抱歉，无法找到相关答案')
        
        # 获取源文档
        sources = []
        if 'source_documents' in result:
            sources = [doc.metadata.get('source', '') for doc in result['source_documents'][:context_size]]
        
        return QAResponse(
            answer=answer,
            sources=sources,
            confidence=0.8
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")

@router.post('/collect')
async def collect_data(request: CollectRequest):
    try:
        # 这里可以调用爬虫功能
        # 简单返回模拟数据
        return {
            'success': True,
            'message': f'成功采集网址: {request.url}',
            'pages': 1,
            'data_count': 10
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))