from ollama import chat
from pydantic import BaseModel, ValidationError
from typing import Type
from .schemas import EmailContent, MeetingProposal, QAResponse, ResumeAnalysis, NewsAnalysis, CodeAnalysis

def structured_ollama_call(
    prompt: str,
    response_model: Type[BaseModel],
    model: str = "gemma3"
) -> BaseModel:
    """
    Makes structured call to Ollama with Pydantic validation.
    On any error, returns a response_model instance with safe defaults.
    """
    try:
        response = chat(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            format=response_model.model_json_schema(),
        )
        return response_model.model_validate_json(response['message']['content'])
    except (ValidationError, Exception) as e:
        print(f"[OllamaError] {e!r} — falling back to defaults for {response_model.__name__}")

        # Hard‐coded defaults per model
        name = response_model.__name__
        if name == "ResumeAnalysis":
            return ResumeAnalysis(
                name="",
                match_score=0,
                strengths=[],
                weaknesses=[],
                missing_keywords=[],
                score_breakdown={}
            )
        elif name == "NewsAnalysis":
            return NewsAnalysis(
                is_fake=False,
                confidence=0,
                reasons=[],
                related_entities=[],
                source_credibility=0,
                supporting_evidence=[]
            )
        elif name == "CodeAnalysis":
            return CodeAnalysis(
                overall_score=0,
                bugs=[],
                optimizations=[],
                security_issues=[],
                complexity_analysis={}
            )
        elif name == "QAResponse":
            return QAResponse(
                answer="Unable to generate response",
                confidence=0,
                sources=[],
                related_questions=[]
            )
        elif name == "EmailContent":
            return EmailContent(
                subject="",
                body="",
                tone_score=0,
                clarity_score=0
            )
        elif name == "MeetingProposal":
            return MeetingProposal(
                suggested_time="",
                agenda_items=[],
                duration_optimization="",
                follow_up_actions=""
            )
        else:
            # Generic fallback: instantiate with no args (will still error if model has required fields!)
            return response_model()
