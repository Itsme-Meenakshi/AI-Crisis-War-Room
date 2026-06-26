from pydantic import BaseModel
from typing import List, Optional

class Stakeholder(BaseModel):
    name: str
    impact: int
    sentiment: str

class RiskItem(BaseModel):
    category: str
    likelihood: int
    impact: int

class PerspectiveInsight(BaseModel):
    perspective: str
    summary: str
    recommendations: List[str]

class CrisisAction(BaseModel):
    time: str
    title: str
    owner: str
    priority: str

class FileAttachment(BaseModel):
    name: str
    size: int

class CrisisAnalyzeResponse(BaseModel):
    id: str
    title: str
    description: str
    createdAt: str
    status: str
    severity: int
    category: str
    stakeholders: List[Stakeholder]
    risks: List[RiskItem]
    perspectives: List[PerspectiveInsight]
    timeline: List[CrisisAction]
    attachments: List[FileAttachment]
