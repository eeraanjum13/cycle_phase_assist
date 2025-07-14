import streamlit as st
import requests
from datetime import date

st.title("🍃 Cycle-Aware Wellness")

# 1. Inputs
col1, col2 = st.columns(2)
with col1:
    last_period = st.date_input("Last period start", value=date.today().replace(day=1))
with col2:
    cycle_len = st.number_input("Cycle length (days)", min_value=20, max_value=40, value=28)

if st.button("Get My Advice"):
    payload = {
        "last_period_start": last_period.isoformat(),
        "cycle_length": cycle_len
    }
    with st.spinner("Fetching advice…"):
        resp = requests.post("http://localhost:8000/predict", json=payload)
    if resp.status_code == 200:
        data = resp.json()
        st.markdown(f"**Day {data['day_of_cycle']} — {data['phase']} Phase**")
        st.markdown(data["advice"])
    else:
        st.error(f"Error: {resp.text}")
