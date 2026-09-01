import requests
import streamlit as st

st.title("🩺 Tele-Rehabilitation Assessment Portal")

st.header("Patient Mobility Assessment")
patient_id = st.text_input("Patient ID", value="PAT-101")
knee_angle = st.slider("Knee Angle (Degrees)", 0, 180, 90)
pain_score = st.slider("Pain Score (1-10)", 1, 10, 4)

API_URL = "http://127.0.0.1:8000/assess"

if st.button("Evaluate Session"):
  payload = {
      "patient_id": patient_id,
      "knee_angle": knee_angle,
      "pain_score": pain_score,
  }
  try:
    response = requests.post(API_URL, json=payload)
    if response.status_code == 200:
      result = response.json()
      st.success(f"Status: {result['mobility_status']}")
      if result["flag_doctor"]:
        st.warning("⚠️ High Pain Score: Flagged for Clinical Review.")
    else:
      st.error("API error response.")
  except Exception as e:
    st.error(f"Could not connect to API: {e}")