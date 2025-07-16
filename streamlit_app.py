# streamlit_app.py
import streamlit as st
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import openai

# ── Config ──
st.set_page_config(page_title="🍃 Cycle-Aware Wellness", layout="centered")
OPENAI_KEY = st.secrets["OPENAI_API_KEY"]
PREP_THRESHOLD = st.secrets.get("PREP_THRESHOLD", 3)
openai.api_key = OPENAI_KEY

# ── Helpers ──
def get_cycle_phase(day, cycle_length=28, period_length=5):
    if day <= period_length:
        return "Menstrual"
    elif day <= 13:
        return "Follicular"
    elif day == 14:
        return "Ovulation"
    else:
        return "Luteal"

def days_until_next_phase(day, cycle_length=28, period_length=5):
    boundaries = [period_length+1, 14, 15, cycle_length+1]
    for b in boundaries:
        if day < b:
            return b - day
    return 0

def get_upcoming_phase(day, cycle_length=28, period_length=5):
    d = days_until_next_phase(day, cycle_length, period_length)
    next_day = (day + d - 1) % cycle_length + 1
    return get_cycle_phase(next_day, cycle_length, period_length)

PROMPT_BASE = """
You are an expert wellness coach. A user is on day {day} of their cycle ({phase}).
1. What types of work/activities are ideal?
2. How much energy (low/medium/high)?
3. What to avoid?
4. Suggest 3 foods to eat & 2 to avoid.
Give bullet points.
"""

PREP_PROMPT = """
You are an expert wellness coach. The user is about to enter {upcoming_phase} in {days_left} days.
1. How should they prepare now?
2. Any warnings or activities to avoid?
Provide bullet points.
"""

def call_openai(prompt):
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        temperature=0.7, max_tokens=300
    )
    return resp.choices[0].message.content.strip()

# ── UI ──
st.title("🍃 Cycle-Aware Wellness")
st.sidebar.header("Your Cycle Info")
last_period = st.sidebar.date_input("Last period start", date.today().replace(day=1))
cycle_len   = st.sidebar.number_input("Cycle length", 20, 40, 28)

if st.sidebar.button("Get My Advice"):
    # compute day & phases
    today = datetime.utcnow().date()
    delta = (today - last_period).days % cycle_len or cycle_len
    phase = get_cycle_phase(delta, cycle_len)
    upcoming = get_upcoming_phase(delta, cycle_len)
    days_left = days_until_next_phase(delta, cycle_len)

    # fetch current-phase advice
    prompt = PROMPT_BASE.format(day=delta, phase=phase)
    advice = call_openai(prompt)

    # fetch prep-tips if within threshold
    prep = None
    if days_left <= PREP_THRESHOLD:
        prep = call_openai(PREP_PROMPT.format(upcoming_phase=upcoming, days_left=days_left))

    # render
    st.subheader(f"📆 Day {delta} — {phase} Phase")
    st.markdown(advice)
    if prep:
        st.warning(f"🔔 Upcoming: **{upcoming}** in **{days_left} days**")
        st.markdown(prep)
    else:
        st.info(f"Next phase **{upcoming}** in **{days_left} days**. No prep-tips yet.")
