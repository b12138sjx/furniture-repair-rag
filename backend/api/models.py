from pydantic import BaseModel
from typing import Optional, List

class UploadResponse(BaseModel):
    success: bool
    message: str
    file_id: Optional[str] = None

class QAResponse(BaseModel):
    answer: str
    sources: Optional[List[str]] = None
    confidence: Optional[float] = None

class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    detail: Optional[str] = None
