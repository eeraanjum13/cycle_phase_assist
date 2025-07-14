import streamlit as st
import requests
from datetime import date

# Title
st.title("🍃 Cycle-Aware Wellness")

# Sidebar inputs
st.sidebar.header("Your Cycle Info")
last_period = st.sidebar.date_input("Last period start", value=date.today().replace(day=1))
cycle_len = st.sidebar.number_input("Cycle length (days)", min_value=20, max_value=40, value=28)

# Fetch and display on button click
if st.sidebar.button("Get My Advice"):
    payload = {
        "last_period_start": last_period.isoformat(),
        "cycle_length": cycle_len
    }
    with st.spinner("Fetching your cycle insights..."):
        resp = requests.post("http://localhost:8000/notify", json=payload)
    
    if resp.status_code == 200:
        data = resp.json()
        
        # Display current phase and advice
        st.subheader(f"📆 Day {data['day_of_cycle']} — {data['phase']} Phase")
        st.markdown(data["advice"])
        
        # Notification for upcoming phase
        days_left = data["days_until_next"]
        if data.get("prep_tips"):
            st.warning(f"🔔 Upcoming phase: **{data['upcoming_phase']}** in **{days_left} days**")
            st.markdown(data["prep_tips"])
        else:
            st.info(f"Next phase (**{data['upcoming_phase']}**) in **{days_left} days**. No prep-tips needed yet.")
    else:
        st.error(f"Error fetching data: {resp.text}")
