from fastapi import APIRouter, HTTPException

from backend.schemas import DocumentRequest
from ai_core.gemini_generator import GeminiDocumentGenerator


router = APIRouter()

generator = GeminiDocumentGenerator()


@router.get("/health")
def health_check():

    return {
        "status": "ok",
        "service": "LegalEase API"
    }


@router.post("/generate")
def generate_document(request: DocumentRequest):

    try:

        generated_document = generator.generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            effective_date=request.effective_date
        )

        return {
            "success": True,
            "document_type": request.document_type,
            "content": generated_document
        }

    except Exception as error:

        raise HTTPException(
            status_code=502,
            detail=f"Document generation failed: {error}"
        )
