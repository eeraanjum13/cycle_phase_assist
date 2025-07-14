# app/utils.py
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
import openai
from dotenv import load_dotenv

load_dotenv()  # loads .env

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_cycle_phase(day: int, cycle_length: int = 28, period_length: int = 5) -> str:
    if day <= period_length:
        return "Menstrual"
    elif day <= 13:
        return "Follicular"
    elif day == 14:
        return "Ovulation"
    else:
        return "Luteal"

PROMPT_TEMPLATE = """
You are an expert wellness coach. A user is on day {day} of their menstrual cycle, which is the {phase} phase.
1. What types of work or activities are ideal right now?
2. How much energy can they expect (low/medium/high)?
3. What activities should they avoid?
4. Suggest 3 foods to eat and 2 foods to avoid in this phase.
Provide a concise, bullet-point list.
"""

def fetch_cycle_advice(day: int, phase: str) -> str:
    prompt = PROMPT_TEMPLATE.format(day=day, phase=phase)
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=300
    )
    return resp.choices[0].message.content.strip()

def get_cycle_phase(day: int, cycle_length: int = 28, period_length: int = 5) -> str:
    if day <= period_length:
        return "Menstrual"
    elif day <= 13:
        return "Follicular"
    elif day == 14:
        return "Ovulation"
    else:
        return "Luteal"

# ── NEW ──
def days_until_next_phase(day: int, cycle_length: int = 28, period_length: int = 5) -> int:
    """
    Returns how many days from `day` until the next phase boundary.
    Boundaries: 
      - Follicular starts on day (period_length + 1)
      - Ovulation on day 14
      - Luteal on day 15
      - Menstrual next cycle on day cycle_length + 1 (i.e. day 29 -> day 1)
    """
    # define boundaries in ascending order
    boundaries = [
        period_length + 1,  # end of Menstrual → Follicular
        14,                 # end of Follicular → Ovulation
        15,                 # end of Ovulation → Luteal
        cycle_length + 1    # end of Luteal → Menstrual next cycle
    ]
    # find the next boundary > day
    for b in boundaries:
        if day < b:
            return b - day
    # never reaches here
    return 0

# ── NEW ──
def get_upcoming_phase(day: int, cycle_length: int = 28, period_length: int = 5) -> str:
    """
    Given today’s `day`, returns the name of the next phase.
    """
    d = days_until_next_phase(day, cycle_length, period_length)
    next_day = (day + d - 1) % cycle_length + 1
    return get_cycle_phase(next_day, cycle_length, period_length)

# ── NEW ──
PREP_PROMPT = """
You are an expert wellness coach. The user is about to enter the {upcoming_phase} phase in {days_left} days.
1. What should they do now to prepare?
2. Any warnings or activities to avoid?
Provide a concise, bullet-point list.
"""

def fetch_prep_tips(days_left: int, upcoming_phase: str) -> str:
    prompt = PREP_PROMPT.format(days_left=days_left, upcoming_phase=upcoming_phase)
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user",   "content": prompt}
        ],
        temperature=0.7,
        max_tokens=200
    )
    return resp.choices[0].message.content.strip()