from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
import os

from app.utils import (
    get_cycle_phase,
    fetch_cycle_advice,
    days_until_next_phase,
    get_upcoming_phase,
    fetch_prep_tips
)

app = FastAPI(title="Cycle-Aware Wellness API")

PREP_THRESHOLD = int(os.getenv("PREP_THRESHOLD", "3"))  # days

class CycleRequest(BaseModel):
    last_period_start: datetime = Field(..., description="YYYY-MM-DD")
    cycle_length: int = Field(28, ge=20, le=40)

class CycleResponse(BaseModel):
    day_of_cycle: int
    phase: str
    advice: str

class NotificationResponse(CycleResponse):
    days_until_next: int
    upcoming_phase: str
    prep_tips: str | None = None

@app.post("/predict", response_model=CycleResponse)
async def predict(req: CycleRequest):
    # (unchanged) compute day & phase
    delta = (datetime.utcnow().date() - req.last_period_start.date()).days % req.cycle_length
    day = delta or req.cycle_length
    phase = get_cycle_phase(day, cycle_length=req.cycle_length)
    try:
        advice = fetch_cycle_advice(day, phase)
    except Exception as e:
        raise HTTPException(502, detail=f"OpenAI API error: {e}")
    return CycleResponse(day_of_cycle=day, phase=phase, advice=advice)

# ── NEW ENDPOINT ──
@app.post("/notify", response_model=NotificationResponse)
async def notify(req: CycleRequest):
    # compute day & phase
    delta = (datetime.utcnow().date() - req.last_period_start.date()).days % req.cycle_length
    day = delta or req.cycle_length
    phase = get_cycle_phase(day, cycle_length=req.cycle_length)

    # days until next phase and name
    days_left = days_until_next_phase(day, cycle_length=req.cycle_length)
    upcoming = get_upcoming_phase(day, cycle_length=req.cycle_length)

    # always fetch current advice
    try:
        advice = fetch_cycle_advice(day, phase)
    except Exception as e:
        raise HTTPException(502, detail=f"OpenAI API error: {e}")

    prep = None
    if days_left <= PREP_THRESHOLD:
        try:
            prep = fetch_prep_tips(days_left, upcoming)
        except Exception as e:
            raise HTTPException(502, detail=f"OpenAI prep-tips error: {e}")

    return NotificationResponse(
        day_of_cycle=day,
        phase=phase,
        advice=advice,
        days_until_next=days_left,
        upcoming_phase=upcoming,
        prep_tips=prep
    )
