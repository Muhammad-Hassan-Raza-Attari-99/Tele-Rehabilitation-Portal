import streamlit as st
import pandas as pd

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="TeleSynapse Rehab | Clinical Portal",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. EXECUTIVE COLOR PALETTE & CSS ---
st.markdown("""
    <style>
    /* Main Background */
    .main { 
        background-color: #F8FAFC; 
    }
    
    /* Executive Sidebar - Deep Slate Navy */
    [data-testid="stSidebar"] {
        background-color: #0F172A !important;
    }
    [data-testid="stSidebar"] * {
        color: #F8FAFC !important;
    }
    
    /* Brand Titles */
    .brand-title {
        font-size: 1.8rem;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: -0.5px;
        margin-bottom: 2px;
    }
    .brand-subtitle {
        font-size: 0.95rem;
        color: #64748B;
        margin-bottom: 24px;
    }
    
    /* Professional Card Containers */
    .enterprise-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
        margin-bottom: 16px;
    }
    .card-header {
        font-weight: 700;
        font-size: 1rem;
        color: #1E293B;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 12px;
        border-bottom: 2px solid #F1F5F9;
        padding-bottom: 8px;
    }
    
    /* Metrics Styling Override */
    [data-testid="stMetricValue"] {
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        color: #2563EB !important;
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.8rem !important;
        font-weight: 700 !important;
        color: #475569 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Custom Status Badges */
    .badge-confirmed {
        background-color: #DCFCE7;
        color: #15803D;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    .badge-pending {
        background-color: #FEF3C7;
        color: #B45309;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE FOR DATA STORAGE ---
if "appointments" not in st.session_state:
    st.session_state["appointments"] = [
        {"Patient": "Ali Ahmed", "Doctor": "Dr. Shahzaib", "Date": "2026-09-03", "Time": "10:00 AM", "Type": "Knee Rehab", "Status": "CONFIRMED"},
        {"Patient": "Sara Khan", "Doctor": "Dr. Hassan", "Date": "2026-09-03", "Time": "11:30 AM", "Type": "Shoulder Flexion", "Status": "PENDING"}
    ]

# --- 4. EXECUTIVE SIDEBAR NAVIGATION ---
st.sidebar.markdown("<h2 style='margin-bottom:2px;'>TELESYNAPSE</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='font-size:0.8rem; color:#94A3B8 !important; margin-bottom:20px;'>CLINICAL TELE-REHABILITATION</p>", unsafe_allow_html=True)

menu = st.sidebar.radio("SYSTEM NAVIGATION", ["Clinician Overview", "Session Scheduler", "Patient Consultation Queue"])

st.sidebar.markdown("---")
st.sidebar.markdown("<p style='font-size:0.75rem; color:#64748B !important;'>System Status: <b>ONLINE (v2.4 Enterprise)</b></p>", unsafe_allow_html=True)

# --- 5. MODULE 1: CLINICIAN OVERVIEW ---
if menu == "Clinician Overview":
    st.markdown('<p class="brand-title">Clinical Session Overview</p>', unsafe_allow_html=True)
    st.markdown('<p class="brand-subtitle">Real-time daily roster and operational analytics for attending physical therapists.</p>', unsafe_allow_html=True)
    
    # Executive Metrics Row
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Consults Today", len(st.session_state["appointments"]))
    m2.metric("Confirmed Sessions", len([a for a in st.session_state["appointments"] if a["Status"] == "CONFIRMED"]))
    m3.metric("Pending Queue", len([a for a in st.session_state["appointments"] if a["Status"] == "PENDING"]))
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="card-header">Scheduled Patient Roster</div>', unsafe_allow_html=True)
    
    for app in st.session_state["appointments"]:
        status_class = "badge-confirmed" if app["Status"] == "CONFIRMED" else "badge-pending"
        st.markdown(f"""
            <div class="enterprise-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 700; font-size: 1.1rem; color: #0F172A;">{app['Patient']}</span>
                    <span class="{status_class}">{app['Status']}</span>
                </div>
                <div style="margin-top: 8px; color: #475569; font-size: 0.9rem;">
                    <b>Attending Specialist:</b> {app['Doctor']} &nbsp;|&nbsp; 
                    <b>Schedule:</b> {app['Time']} ({app['Date']}) &nbsp;|&nbsp; 
                    <b>Focus Area:</b> {app['Type']}
                </div>
            </div>
        """, unsafe_allow_html=True)

# --- 6. MODULE 2: SESSION SCHEDULER ---
elif menu == "Session Scheduler":
    st.markdown('<p class="brand-title">Session Scheduling Portal</p>', unsafe_allow_html=True)
    st.markdown('<p class="brand-subtitle">Register new tele-rehabilitation consults and assign specialized clinicians.</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="card-header">Book New Clinical Session</div>', unsafe_allow_html=True)
        patient_name = st.text_input("Patient Legal Name", placeholder="e.g. Usama Zahid")
        doctor_name = st.selectbox("Assign Lead Specialist", ["Dr. Shahzaib Mughal", "Dr. Hassan Raza", "Dr. Ayesha Malik"])
        rehab_type = st.selectbox("Clinical Focus Area", ["Knee ACL Rehabilitation", "Shoulder Abduction Protocol", "Elbow Mobility Index", "Post-Stroke Assessment"])
        app_date = st.date_input("Consultation Date")
        app_time = st.selectbox("Time Slot", ["09:00 AM", "10:00 AM", "11:30 AM", "02:00 PM", "04:00 PM"])
        
        if st.button("Confirm Session Booking", type="primary"):
            if patient_name:
                new_app = {
                    "Patient": patient_name,
                    "Doctor": doctor_name,
                    "Date": str(app_date),
                    "Time": app_time,
                    "Type": rehab_type,
                    "Status": "CONFIRMED"
                }
                st.session_state["appointments"].append(new_app)
                st.success(f"Session successfully recorded for {patient_name} on {app_date} at {app_time}.")
            else:
                st.error("Patient legal name is required.")

    with col2:
        st.markdown('<div class="card-header">System Appointment Register</div>', unsafe_allow_html=True)
        df_apps = pd.DataFrame(st.session_state["appointments"])
        st.dataframe(df_apps, use_container_width=True)

# --- 7. MODULE 3: PATIENT CONSULTATION QUEUE ---
else:
    st.markdown('<p class="brand-title">Live Telehealth Queue</p>', unsafe_allow_html=True)
    st.markdown('<p class="brand-subtitle">Virtual consultation rooms ready for real-time video stream & kinematic data processing.</p>', unsafe_allow_html=True)
    
    st.info("System Ready: WebRTC video frame integration ready for Day 2 deployment.")
