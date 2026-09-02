import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="TeleSynapse Rehab | Health Portal",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CUSTOM MEDICAL CSS STYLING ---
st.markdown("""
    <style>
    .main { background-color: #F8FAFC; }
    .stApp { font-family: 'Inter', sans-serif; }
    .main-title {
        color: #0F172A;
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 5px;
    }
    .sub-title {
        color: #475569;
        font-size: 1rem;
        margin-bottom: 25px;
    }
    .card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #2563EB;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE FOR APPOINTMENTS ---
if "appointments" not in st.session_state:
    st.session_state["appointments"] = [
        {"Patient": "Ali Ahmed", "Doctor": "Dr. Shahzaib", "Date": "2026-09-03", "Time": "10:00 AM", "Type": "Knee Rehab", "Status": "Confirmed"},
        {"Patient": "Sara Khan", "Doctor": "Dr. Hassan", "Date": "2026-09-03", "Time": "11:30 AM", "Type": "Shoulder Flexion", "Status": "Pending"}
    ]

# --- 4. SIDEBAR NAVIGATION ---
st.sidebar.title("🩺 TeleSynapse")
st.sidebar.caption("Enterprise Tele-Rehabilitation")
st.sidebar.markdown("---")

menu = st.sidebar.radio("Navigation", ["📅 Schedule Appointment", "👨‍⚕️ Clinician View", "📋 Session Queue"])

# --- 5. MODULE 1: APPOINTMENT SCHEDULER ---
if menu == "📅 Schedule Appointment":
    st.markdown('<p class="main-title">📅 Patient Session Scheduler</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Book new tele-rehabilitation sessions and manage consults.</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="card"><b>Book New Tele-Rehab Session</b></div>', unsafe_allow_html=True)
        patient_name = st.text_input("Patient Full Name", placeholder="e.g. Usama Zahid")
        doctor_name = st.selectbox("Assign Specialist", ["Dr. Shahzaib Mughal", "Dr. Hassan Raza", "Dr. Ayesha Malik"])
        rehab_type = st.selectbox("Rehabilitation Category", ["Knee ACL Rehab", "Shoulder Abduction", "Elbow Mobility", "Post-Stroke Assessment"])
        app_date = st.date_input("Consultation Date")
        app_time = st.selectbox("Time Slot", ["09:00 AM", "10:00 AM", "11:30 AM", "02:00 PM", "04:00 PM"])
        
        if st.button("Confirm & Book Session", type="primary"):
            if patient_name:
                new_app = {
                    "Patient": patient_name,
                    "Doctor": doctor_name,
                    "Date": str(app_date),
                    "Time": app_time,
                    "Type": rehab_type,
                    "Status": "Confirmed"
                }
                st.session_state["appointments"].append(new_app)
                st.success(f"Session successfully booked for {patient_name} on {app_date} at {app_time}!")
            else:
                st.error("Please enter the patient's name.")

    with col2:
        st.markdown('<div class="card"><b>Active Appointments Schedule</b></div>', unsafe_allow_html=True)
        df_apps = pd.DataFrame(st.session_state["appointments"])
        st.dataframe(df_apps, use_container_width=True)

# --- 6. MODULE 2: CLINICIAN DASHBOARD VIEW ---
elif menu == "👨‍⚕️ Clinician View":
    st.markdown('<p class="main-title">👨‍⚕️ Clinician Session Overview</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Real-time daily roster for attending physical therapists.</p>', unsafe_allow_html=True)
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Appointments Today", len(st.session_state["appointments"]))
    m2.metric("Confirmed Consults", len([a for a in st.session_state["appointments"] if a["Status"] == "Confirmed"]))
    m3.metric("Pending Confirmations", len([a for a in st.session_state["appointments"] if a["Status"] == "Pending"]))
    
    st.markdown("---")
    st.subheader("Scheduled Patient Roster")
    for app in st.session_state["appointments"]:
        st.info(f"👤 **Patient:** {app['Patient']} | 🩺 **Doctor:** {app['Doctor']} | 🕒 **Time:** {app['Time']} ({app['Date']}) | 🎯 **Focus:** {app['Type']}")

# --- 7. MODULE 3: SESSION QUEUE ---
else:
    st.markdown('<p class="main-title">📋 Live Rehabilitation Queue</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Patients waiting in virtual lobby for biomechanical assessment.</p>', unsafe_allow_html=True)
    st.warning("Virtual consultation rooms are operational. Ready for video integration.")
