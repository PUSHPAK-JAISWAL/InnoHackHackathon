# utils/schemas.py
from pydantic import BaseModel
from typing import Dict, List, Optional

class ResumeAnalysis(BaseModel):
    name: str
    contact_info: str
    experience_summary: str
    match_score: int
    is_good_fit: bool
    strengths: List[str]
    weaknesses: List[str]
    missing_keywords: List[str]
    score_breakdown: Dict[str, float]
    detailed_report: str

class NewsAnalysis(BaseModel):
    is_fake: bool
    confidence: int
    reasons: List[str]
    related_entities: List[str]
    source_credibility: int
    supporting_evidence: List[str]

class CodeBug(BaseModel):
    description: str
    severity: str  # low/medium/high
    line_number: Optional[int]
    fix_suggestion: str

class CodeAnalysis(BaseModel):
    overall_score: int
    bugs: List[CodeBug]
    optimizations: List[str]
    security_issues: List[str]
    complexity_analysis: dict

class QAResponse(BaseModel):
    answer: str
    confidence: int
    sources: List[str]
    related_questions: List[str]

class EmailContent(BaseModel):
    subject: str
    body: str
    tone_score: int
    clarity_score: int

class MeetingProposal(BaseModel):
    suggested_time: str
    agenda_items: List[str]
    duration_optimization: str
    follow_up_actions: str