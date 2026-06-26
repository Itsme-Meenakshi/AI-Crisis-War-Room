import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import settings
from app.schemas.request_schema import CrisisAnalyzeRequest
from app.schemas.response_schema import CrisisAnalyzeResponse
from app.services.orchestrator import analyze_crisis_event
from app.services.persistence import get_all_crises, get_crisis_by_id, save_crisis

app = FastAPI(
    title="AI Crisis War Room API",
    description="Intelligent Crisis Management and Decision Support System Backend",
    version="1.0.0"
)

# Setup CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    return {"status": "ok", "app": "AI Crisis War Room", "version": "1.0.0"}

@app.get("/api/crises", response_model=list[CrisisAnalyzeResponse])
def fetch_crises():
    try:
        return get_all_crises()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database read error: {str(e)}")

@app.get("/api/crises/{crisis_id}", response_model=CrisisAnalyzeResponse)
def fetch_crisis_details(crisis_id: str):
    try:
        crisis = get_crisis_by_id(crisis_id)
        if not crisis:
            raise HTTPException(status_code=404, detail="Incident record not found")
        return crisis
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database read error: {str(e)}")

@app.post("/api/analyze", response_model=CrisisAnalyzeResponse)
def analyze_crisis(payload: CrisisAnalyzeRequest):
    try:
        # Run orchestrator service to invoke the LangGraph flow
        response = analyze_crisis_event(
            title=payload.title,
            description=payload.description,
            files=[f.model_dump() for f in payload.files] if payload.files else []
        )
        # Persist results in local database
        save_crisis(response.model_dump())
        return response
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during crisis analysis: {str(e)}"
        )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )
