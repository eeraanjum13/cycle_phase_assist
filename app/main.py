from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
from app.utils import get_cycle_phase, fetch_cycle_advice

app = FastAPI(title="Cycle-Aware Wellness API")

class CycleRequest(BaseModel):
    last_period_start: datetime = Field(..., description="YYYY-MM-DD")
    cycle_length: int = Field(28, ge=20, le=40)

class CycleResponse(BaseModel):
    day_of_cycle: int
    phase: str
    advice: str

@app.post("/predict", response_model=CycleResponse)
async def predict(req: CycleRequest):
    # compute day of cycle
    delta_days = (datetime.utcnow().date() - req.last_period_start.date()).days % req.cycle_length
    day = delta_days if delta_days != 0 else req.cycle_length
    phase = get_cycle_phase(day, cycle_length=req.cycle_length)

    try:
        advice = fetch_cycle_advice(day, phase)
    except Exception as e:
        raise HTTPException(502, detail=f"OpenAI API error: {e}")

    return CycleResponse(day_of_cycle=day, phase=phase, advice=advice)
