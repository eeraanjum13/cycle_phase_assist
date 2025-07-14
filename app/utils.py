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
