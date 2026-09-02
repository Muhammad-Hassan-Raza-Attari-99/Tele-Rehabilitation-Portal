import streamlit as st
import pandas as pd

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="TeleSynapse Rehab | Executive Suite",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ADVANCED DARK SLATE, ROYAL BLUE & EMERALD CSS ---
st.markdown("""
    <style>
    /* -----------------------------------------------------------
       CRITICAL SECURITY & UI CLEANUP: HIDE STREAMLIT TOP TOOLBAR
       ----------------------------------------------------------- */
    header[data-testid="stHeader"] {
        visibility: hidden !important;
        height: 0px !important;
    }
    #MainMenu { visibility: hidden !important; }
    footer { visibility: hidden !important; }
    .stDeployButton { display: none !important; }
    
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Overall Dark Slate Canvas */
    .stApp {
        background-color: #0E131F !important;
        color: #F8FAFC !important;
    }

    /* Sidebar Styling - Deep Control Panel */
    [data-testid="stSidebar"] {
        background-color: #161D2F !important;
        border-right: 1px solid #2A364F !important;
    }
    [data-testid="stSidebar"] * {
        color: #F8FAFC !important;
    }

    /* Profile Badge Card in Sidebar */
    .profile-card {
        background: #FFFFFF;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
    }
    .profile-name {
        color: #1E3A8A;
        font-size: 1.05rem;
        font-weight: 800;
        margin-bottom: 4px;
    }
    .profile-dept {
        color: #2563EB;
        font-size: 0.82rem;
        font-weight: 700;
        margin-bottom: 4px;
    }
    .profile-role {
        color: #475569;
        font-size: 0.75rem;
        font-weight: 600;
    }

    /* Main Royal Blue Header Card */
    .hero-header {
        background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 100%);
        border-radius: 14px;
        padding: 30px;
        text-align: center;
        border: 1px solid #3B82F6;
        box-shadow: 0 10px 25px rgba(37, 99, 235, 0.25);
        margin-bottom: 25px;
    }
    .hero-title {
        color: #FFFFFF;
        font-size: 2rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-bottom: 8px;
    }
    .hero-sub {
        color: #93C5FD;
        font-size: 0.95rem;
        font-weight: 600;
    }

    /* Clinical Evaluation & Protocol Containers */
    .protocol-card-blue {
        background-color: #1E293B;
        border-left: 5px solid #3B82F6;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .protocol-card-emerald {
        background-color: #064E3B;
        border-left: 5px solid #10B981;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
        color: #ECFDF5;
    }
    .protocol-card-amber {
        background-color: #451A03;
        border-left: 5px solid #F59E0B;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
        color: #FEF3C7;
    }

    /* Metric Cards */
    .dark-stat-box {
        background: #161D2F;
        border: 1px solid #2A364F;
        border-radius: 10px;
        padding: 18px;
        text-align: center;
    }
    .dark-stat-val {
        font-size: 2.2rem;
        font-weight: 800;
        color: #38BDF8;
    }
    .dark-stat-lbl {
        font-size: 0.75rem;
        font-weight: 700;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE FOR APPOINTMENTS ---
if "appointments" not in st.session_state:
    st.session_state["appointments"] = [
        {"Patient": "Ali Ahmed", "Doctor": "Dr. Shahzaib Mughal", "Date": "2026-09-03", "Time": "10:00 AM", "Type": "Knee ACL Protocol", "Status": "CONFIRMED"},
        {"Patient": "Sara Khan", "Doctor": "Dr. Hassan Raza", "Date": "2026-09-03", "Time": "11:30 AM", "Type": "Shoulder Abduction", "Status": "PENDING"}
    ]

# --- 4. CONTROL PANEL SIDEBAR ---
st.sidebar.markdown("<h3 style='margin-bottom:15px; color:#FFFFFF;'>⚙️ Control Panel</h3>", unsafe_allow_html=True)

# Architect Profile Card
st.sidebar.markdown("""
    <div class="profile-card">
        <div class="profile-name">Muhammad Hassan Raza Attari</div>
        <div class="profile-dept">Biomedical Engineering (BME)</div>
        <div class="profile-role">Role: Lead Architect & AI System Designer</div>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown("<p style='font-size:0.8rem; font-weight:700; color:#94A3B8;'>SYSTEM NAVIGATION</p>", unsafe_allow_html=True)
menu = st.sidebar.radio("", ["Clinician Overview", "Patient Registration & Scheduler", "Official Protocol Suite"])

st.sidebar.markdown("---")
st.sidebar.markdown("<p style='font-size:0.75rem; color:#64748B;'>Engine: <b>TeleSynapse v3.0 Dark Mode</b></p>", unsafe_allow_html=True)

# --- 5. MODULE 1: CLINICIAN OVERVIEW ---
if menu == "Clinician Overview":
    # Royal Blue Hero Banner
    st.markdown("""
        <div class="hero-header">
            <div class="hero-title">🏥 TeleSynapse Clinical Dashboard & AI Suite</div>
            <div class="hero-sub">Advanced Biomedical Engineering & Tele-Rehabilitation Diagnostic Engine</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Stat Cards
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
            <div class="dark-stat-box">
                <div class="dark-stat-lbl">Active Tele-Rehab Consults</div>
                <div class="dark-stat-val">{len(st.session_state['appointments'])}</div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        confirmed = len([a for a in st.session_state["appointments"] if a["Status"] == "CONFIRMED"])
        st.markdown(f"""
            <div class="dark-stat-box" style="border-color: #10B981;">
                <div class="dark-stat-lbl">Confirmed Protocol Queue</div>
                <div class="dark-stat-val" style="color:#10B981;">{confirmed}</div>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        pending = len([a for a in st.session_state["appointments"] if a["Status"] == "PENDING"])
        st.markdown(f"""
            <div class="dark-stat-box" style="border-color: #F59E0B;">
                <div class="dark-stat-lbl">Pending Triage Review</div>
                <div class="dark-stat-val" style="color:#F59E0B;">{pending}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><h3 style='color:#FFFFFF;'>📋 Active Clinical Patient Roster</h3>", unsafe_allow_html=True)
    
    for app in st.session_state["appointments"]:
        card_type = "protocol-card-emerald" if app["Status"] == "CONFIRMED" else "protocol-card-amber"
        st.markdown(f"""
            <div class="{card_type}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 800; font-size: 1.1rem;">👤 Patient Name: {app['Patient']}</span>
                    <span style="font-weight: 800; font-size: 0.8rem; background:rgba(255,255,255,0.2); padding:4px 10px; border-radius:6px;">{app['Status']}</span>
                </div>
                <div style="margin-top: 8px; font-size: 0.9rem;">
                    <b>Specialist:</b> {app['Doctor']} &nbsp;|&nbsp; 
                    <b>Schedule:</b> {app['Time']} ({app['Date']}) &nbsp;|&nbsp; 
                    <b>Protocol Focus:</b> {app['Type']}
                </div>
            </div>
        """, unsafe_allow_html=True)

# --- 6. MODULE 2: PATIENT REGISTRATION & SCHEDULER ---
elif menu == "Patient Registration & Scheduler":
    st.markdown("""
        <div class="hero-header">
            <div class="hero-title">📝 Patient Registration & Intake</div>
            <div class="hero-sub">Register clinical demographics and queue patients for kinematic evaluation.</div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("<h4 style='color:#FFFFFF;'>Patient Registration</h4>", unsafe_allow_html=True)
        patient_name = st.text_input("Patient Full Legal Name", placeholder="e.g. Fazal Bibi")
        doctor_name = st.selectbox("Assign Lead Specialist", ["Dr. Shahzaib Mughal", "Dr. Hassan Raza", "Dr. Ayesha Malik"])
        rehab_type = st.selectbox("Target Diagnostic Protocol", ["Knee ACL Rehabilitation", "Shoulder Abduction Index", "Elbow Mobility Protocol", "Post-Stroke Assessment"])
        app_date = st.date_input("Consultation Date")
        app_time = st.selectbox("Time Slot", ["09:00 AM", "10:00 AM", "11:30 AM", "02:00 PM", "04:00 PM"])
        
        if st.button("Submit Patient Intake Record", type="primary"):
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
                st.success(f"Patient intake record for {patient_name} submitted successfully.")
            else:
                st.error("Patient legal name is required.")

    with col2:
        st.markdown("<h4 style='color:#FFFFFF;'>Registered Patient Register</h4>", unsafe_allow_html=True)
        df_apps = pd.DataFrame(st.session_state["appointments"])
        st.dataframe(df_apps, use_container_width=True)

# --- 7. MODULE 3: OFFICIAL PROTOCOL SUITE ---
else:
    st.markdown("""
        <div class="hero-header">
            <div class="hero-title">📋 Official Medical Evaluation & Protocol</div>
            <div class="hero-sub">Targeted diagnostic evaluation and automated prescription recommendations.</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="protocol-card-blue">
            <b>Diagnosed Condition:</b> Targeted Diagnostic Evaluation for Biomechanical Range of Motion Restriction.
        </div>
        <div class="protocol-card-amber">
            <b>Triage Category:</b> CLINICAL EVALUATION & MANAGEMENT
        </div>
        <div class="protocol-card-emerald">
            <b>Physiotherapy & Rehab Plan:</b> Adaptive Mobilization Therapy & targeted joint angle exercises tailored for active recovery.
        </div>
    """, unsafe_allow_html=True)
