from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import uvicorn
import os
from dotenv import load_dotenv

# Import the logic from agents.py
try:
    from app.agents import run_validation_pipeline
except ImportError:
    from agents import run_validation_pipeline

load_dotenv()

app = FastAPI(
    title="Startup Idea Validator API",
    description="Multi-agent orchestration for validating startup ideas using Groq & Llama 3.",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class IdeaRequest(BaseModel):
    idea_title: str
    target_audience: str
    detailed_description: str

class AgentReport(BaseModel):
    agent_name: str
    role: str
    report: str
    score: int

class ValidationResponse(BaseModel):
    idea_title: str
    individual_reports: List[AgentReport]
    executive_summary: str
    final_score: int

@app.get("/")
async def root():
    return {"message": "Startup Idea Validator API is running"}

@app.post("/api/v1/validate-idea", response_model=ValidationResponse)
async def validate_idea(request: IdeaRequest):
    """
    Endpoint to trigger the multi-agent validation loop.
    """
    if not os.environ.get("GROQ_API_KEY"):
        raise HTTPException(status_code=500, detail="GROQ_API_KEY not configured in environment.")
    
    try:
        # Run the validation pipeline
        results = run_validation_pipeline(
            idea_title=request.idea_title,
            target_audience=request.target_audience,
            description=request.detailed_description
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
