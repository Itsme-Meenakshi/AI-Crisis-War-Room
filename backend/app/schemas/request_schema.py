from pydantic import BaseModel
from typing import List, Optional

class FileAttachment(BaseModel):
    name: str
    size: int

class CrisisAnalyzeRequest(BaseModel):
    title: str
    description: str
    files: Optional[List[FileAttachment]] = []
