import streamlit as st
import pandas as pd

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="TeleSynapse | Clinical Dashboard",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CUSTOM CSS: DARK SLATE, EMERALD GREEN & ROYAL BLUE PALETTE ---
st.markdown("""
    <style>
    /* -----------------------------------------------------------
       1. SECURITY & UI CLEANUP: HIDE STREAMLIT TOP TOOLBAR & MENU
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

    /* Overall Dark Slate Background Canvas */
    .stApp {
        background-color: #0A0E17 !important;
        color: #F8FAFC !important;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #111827 !important;
        border-right: 1px solid #1F2937 !important;
    }
    [data-testid="stSidebar"] * {
        color: #F8FAFC !important;
    }

    /* Top-Left Dashboard Brand Badge */
    .brand-container {
        padding: 12px 0px 18px 0px;
        border-bottom: 1px solid #1F2937;
        margin-bottom: 22px;
    }
    .brand-title {
        color: #10B981 !important; /* Emerald Green */
        font-size: 1.65rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin: 0;
    }
    .brand-sub {
        color: #34D399 !important;
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-top: 3px;
    }

    /* Hero Banner: Blue to Emerald Gradient */
    .hero-banner {
        background: linear-gradient(135deg, #1E3A8A 0%, #0F766E 50%, #064E3B 100%);
        border-radius: 12px;
        padding: 28px;
        text-align: center;
        border: 1px solid #10B981;
        box-shadow: 0 10px 25px rgba(16, 185, 129, 0.2);
        margin-bottom: 25px;
    }
    .hero-title {
        color: #FFFFFF !important;
        font-size: 2rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-bottom: 6px;
    }
    .hero-sub {
        color: #A7F3D0 !important;
        font-size: 0.95rem;
        font-weight: 600;
    }

    /* Stat Cards */
    .stat-card-blue {
        background: #1E293B;
        border: 1px solid #3B82F6;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
    }
    .stat-card-emerald {
        background: #064E3B;
        border: 1px solid #10B981;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
    }
    .stat-card-amber {
        background: #451A03;
        border: 1px solid #F59E0B;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
    }

    /* Custom Patient Cards matching Reference Screenshots */
    .card-confirmed {
        background-color: #064E3B !important;
        border-left: 6px solid #10B981 !important;
        border-radius: 8px;
        padding: 18px 22px;
        margin-bottom: 14px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    .card-pending {
        background-color: #451A03 !important;
        border-left: 6px solid #F59E0B !important;
        border-radius: 8px;
        padding: 18px 22px;
        margin-bottom: 14px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }

    /* Glowing Pill Badges */
    .badge-confirmed {
        font-weight: 800;
        font-size: 0.75rem;
        color: #10B981;
        background: rgba(16, 185, 129, 0.18);
        padding: 5px 14px;
        border-radius: 20px;
        border: 1px solid #10B981;
        letter-spacing: 0.5px;
    }
    .badge-pending {
        font-weight: 800;
        font-size: 0.75rem;
        color: #F59E0B;
        background: rgba(245, 158, 11, 0.18);
        padding: 5px 14px;
        border-radius: 20px;
        border: 1px solid #F59E0B;
        letter-spacing: 0.5px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE FOR APPOINTMENTS ---
if "appointments" not in st.session_state:
    st.session_state["appointments"] = [
        {"Patient": "Ali Ahmed", "Doctor": "Dr. Shahzaib Mughal", "Date": "2026-09-03", "Time": "10:00 AM", "Type": "Knee ACL Protocol", "Status": "CONFIRMED"},
        {"Patient": "Sara Khan", "Doctor": "Dr. Hassan Raza", "Date": "2026-09-03", "Time": "11:30 AM", "Type": "Shoulder Abduction", "Status": "PENDING"}
    ]

# --- 4. SIDEBAR BRANDING & NAVIGATION ---
st.sidebar.markdown("""
    <div class="brand-container">
        <div class="brand-title">TELESYNAPSE</div>
        <div class="brand-sub">Clinical Dashboard</div>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown("<p style='font-size:0.75rem; font-weight:800; color:#9CA3AF; text-transform:uppercase; letter-spacing:1px; margin-bottom:10px;'>System Navigation</p>", unsafe_allow_html=True)
menu = st.sidebar.radio("", ["Clinician Overview", "Patient Registration & Scheduler", "Official Protocol Suite"])

st.sidebar.markdown("---")
st.sidebar.markdown("<p style='font-size:0.75rem; color:#6B7280;'>System Status: <b style='color:#10B981;'>ONLINE (v3.2 Emerald)</b></p>", unsafe_allow_html=True)

# --- 5. MODULE 1: CLINICIAN OVERVIEW ---
if menu == "Clinician Overview":
    # Hero Banner
    st.markdown("""
        <div class="hero-banner">
            <div class="hero-title">🏥 TeleSynapse Clinical Dashboard & AI Suite</div>
            <div class="hero-sub">Advanced Biomedical Engineering & Tele-Rehabilitation Diagnostic Engine</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Stat Metrics
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
            <div class="stat-card-blue">
                <div style="font-size:0.75rem; font-weight:700; color:#93C5FD; text-transform:uppercase; letter-spacing:0.8px;">Active Tele-Rehab Consults</div>
                <div style="font-size:2.3rem; font-weight:800; color:#60A5FA; margin-top:4px;">{len(st.session_state['appointments'])}</div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        confirmed = len([a for a in st.session_state["appointments"] if a["Status"] == "CONFIRMED"])
        st.markdown(f"""
            <div class="stat-card-emerald">
                <div style="font-size:0.75rem; font-weight:700; color:#A7F3D0; text-transform:uppercase; letter-spacing:0.8px;">Confirmed Protocol Queue</div>
                <div style="font-size:2.3rem; font-weight:800; color:#34D399; margin-top:4px;">{confirmed}</div>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        pending = len([a for a in st.session_state["appointments"] if a["Status"] == "PENDING"])
        st.markdown(f"""
            <div class="stat-card-amber">
                <div style="font-size:0.75rem; font-weight:700; color:#FDE68A; text-transform:uppercase; letter-spacing:0.8px;">Pending Triage Review</div>
                <div style="font-size:2.3rem; font-weight:800; color:#FBBF24; margin-top:4px;">{pending}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><h3 style='color:#FFFFFF; font-weight:800;'>📋 Active Clinical Patient Roster</h3>", unsafe_allow_html=True)
    
    for app in st.session_state["appointments"]:
        if app["Status"] == "CONFIRMED":
            st.markdown(f"""
                <div class="card-confirmed">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: 800; font-size: 1.15rem; color: #FFFFFF;">👤 Patient Name: {app['Patient']}</span>
                        <span class="badge-confirmed">{app['Status']}</span>
                    </div>
                    <div style="margin-top: 10px; font-size: 0.92rem; color: #D1FAE5;">
                        <b>Specialist:</b> {app['Doctor']} &nbsp;|&nbsp; 
                        <b>Schedule:</b> {app['Time']} ({app['Date']}) &nbsp;|&nbsp; 
                        <b>Protocol Focus:</b> {app['Type']}
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="card-pending">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: 800; font-size: 1.15rem; color: #FFFFFF;">👤 Patient Name: {app['Patient']}</span>
                        <span class="badge-pending">{app['Status']}</span>
                    </div>
                    <div style="margin-top: 10px; font-size: 0.92rem; color: #FEF3C7;">
                        <b>Specialist:</b> {app['Doctor']} &nbsp;|&nbsp; 
                        <b>Schedule:</b> {app['Time']} ({app['Date']}) &nbsp;|&nbsp; 
                        <b>Protocol Focus:</b> {app['Type']}
                    </div>
                </div>
            """, unsafe_allow_html=True)

# --- 6. MODULE 2: PATIENT REGISTRATION & SCHEDULER ---
elif menu == "Patient Registration & Scheduler":
    st.markdown("""
        <div class="hero-banner">
            <div class="hero-title">📝 Patient Registration & Intake</div>
            <div class="hero-sub">Register clinical demographics and queue patients for kinematic evaluation.</div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("<h4 style='color:#FFFFFF;'>Patient Intake Form</h4>", unsafe_allow_html=True)
        patient_name = st.text_input("Patient Full Legal Name", placeholder="e.g. Fazal Bibi")
        doctor_name = st.selectbox("Assign Lead Specialist", ["Dr. Shahzaib Mughal", "Dr. Hassan Raza", "Dr. Ayesha Malik"])
        rehab_type = st.selectbox("Target Diagnostic Protocol", ["Knee ACL Protocol", "Shoulder Abduction", "Elbow Mobility Protocol", "Post-Stroke Assessment"])
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
                st.success(f"Patient intake record for {patient_name} registered successfully.")
            else:
                st.error("Patient legal name is required.")

    with col2:
        st.markdown("<h4 style='color:#FFFFFF;'>Active Roster Register</h4>", unsafe_allow_html=True)
        df_apps = pd.DataFrame(st.session_state["appointments"])
        st.dataframe(df_apps, use_container_width=True)

# --- 7. MODULE 3: OFFICIAL PROTOCOL SUITE ---
else:
    st.markdown("""
        <div class="hero-banner">
            <div class="hero-title">📋 Official Medical Evaluation & Protocol</div>
            <div class="hero-sub">Targeted diagnostic evaluation and automated prescription recommendations.</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style="background:#1E293B; border-left:6px solid #3B82F6; padding:18px; border-radius:8px; margin-bottom:14px; color:#F8FAFC;">
            <b>Diagnosed Condition:</b> Targeted Diagnostic Evaluation for Biomechanical Range of Motion Restriction.
        </div>
        <div style="background:#451A03; border-left:6px solid #F59E0B; padding:18px; border-radius:8px; margin-bottom:14px; color:#FEF3C7;">
            <b>Triage Category:</b> CLINICAL EVALUATION & MANAGEMENT
        </div>
        <div style="background:#064E3B; border-left:6px solid #10B981; padding:18px; border-radius:8px; margin-bottom:14px; color:#ECFDF5;">
            <b>Physiotherapy & Rehab Plan:</b> Adaptive Mobilization Therapy & targeted joint angle exercises tailored for active recovery.
        </div>
    """, unsafe_allow_html=True)
