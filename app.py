import streamlit as st
import pandas as pd

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="TeleSynapse | Enterprise Rehab Portal",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ADVANCED DARK SLATE, EMERALD & BLUE CSS ---
st.markdown("""
    <style>
    /* -----------------------------------------------------------
       HIDE DEFAULT STREAMLIT HEADER & FOOTER
       ----------------------------------------------------------- */
    #MainMenu { visibility: hidden !important; }
    footer { visibility: hidden !important; }
    .stDeployButton { display: none !important; }
    
    header[data-testid="stHeader"] {
        background-color: transparent !important;
        z-index: 100;
    }

    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Canvas Background */
    .stApp {
        background-color: #0A0E17 !important;
        color: #F8FAFC !important;
    }

    /* -----------------------------------------------------------
       SIDEBAR STYLING - PREMIUM DARK EMERALD NAV
       ----------------------------------------------------------- */
    [data-testid="stSidebar"] {
        background-color: #0F172A !important;
        border-right: 1px solid #1E293B !important;
        min-width: 300px !important;
    }
    [data-testid="stSidebar"] * {
        color: #F8FAFC !important;
    }

    /* Sidebar Brand Card */
    .brand-container {
        padding: 16px 12px;
        background: linear-gradient(135deg, #064E3B 0%, #0F172A 100%);
        border: 1px solid #10B981;
        border-radius: 10px;
        margin-bottom: 20px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.15);
    }
    .brand-title {
        color: #10B981 !important;
        font-size: 1.7rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin: 0;
    }
    .brand-sub {
        color: #6EE7B7 !important;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-top: 4px;
    }

    /* Sidebar System Status Widget */
    .status-widget {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 12px;
        margin-top: 20px;
        font-size: 0.8rem;
    }

    /* Main Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, #1E3A8A 0%, #0F766E 50%, #064E3B 100%);
        border-radius: 12px;
        padding: 26px;
        text-align: center;
        border: 1px solid #10B981;
        box-shadow: 0 10px 25px rgba(16, 185, 129, 0.2);
        margin-bottom: 25px;
    }
    .hero-title {
        color: #FFFFFF !important;
        font-size: 1.9rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-bottom: 4px;
    }
    .hero-sub {
        color: #A7F3D0 !important;
        font-size: 0.9rem;
        font-weight: 600;
    }

    /* Stat Metric Boxes */
    .stat-card-blue {
        background: #1E293B;
        border: 1px solid #3B82F6;
        border-radius: 10px;
        padding: 18px;
        text-align: center;
    }
    .stat-card-emerald {
        background: #064E3B;
        border: 1px solid #10B981;
        border-radius: 10px;
        padding: 18px;
        text-align: center;
    }
    .stat-card-amber {
        background: #451A03;
        border: 1px solid #F59E0B;
        border-radius: 10px;
        padding: 18px;
        text-align: center;
    }

    /* Patient Roster Cards */
    .card-confirmed {
        background-color: #064E3B !important;
        border-left: 6px solid #10B981 !important;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    .card-pending {
        background-color: #451A03 !important;
        border-left: 6px solid #F59E0B !important;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }

    /* Badges */
    .badge-confirmed {
        font-weight: 800;
        font-size: 0.72rem;
        color: #10B981;
        background: rgba(16, 185, 129, 0.2);
        padding: 4px 12px;
        border-radius: 20px;
        border: 1px solid #10B981;
    }
    .badge-pending {
        font-weight: 800;
        font-size: 0.72rem;
        color: #F59E0B;
        background: rgba(245, 158, 11, 0.2);
        padding: 4px 12px;
        border-radius: 20px;
        border: 1px solid #F59E0B;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE STORAGE ---
if "appointments" not in st.session_state:
    st.session_state["appointments"] = [
        {"Patient": "Ali Ahmed", "Doctor": "Dr. Shahzaib Mughal", "Date": "2026-09-03", "Time": "10:00 AM", "Type": "Knee ACL Protocol", "Status": "CONFIRMED"},
        {"Patient": "Sara Khan", "Doctor": "Dr. Hassan Raza", "Date": "2026-09-03", "Time": "11:30 AM", "Type": "Shoulder Abduction", "Status": "PENDING"},
        {"Patient": "Usman Tariq", "Doctor": "Dr. Ayesha Malik", "Date": "2026-09-04", "Time": "02:00 PM", "Type": "Elbow Mobility Protocol", "Status": "CONFIRMED"}
    ]

# --- 4. EXPANDED SIDEBAR NAVIGATION ---
st.sidebar.markdown("""
    <div class="brand-container">
        <div class="brand-title">TELESYNAPSE</div>
        <div class="brand-sub">Enterprise Tele-Rehab</div>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown("<p style='font-size:0.75rem; font-weight:800; color:#9CA3AF; text-transform:uppercase; letter-spacing:1px; margin-bottom:8px;'>Clinical Control Suite</p>", unsafe_allow_html=True)

# 7 Expanded Sidebar Options
menu_options = [
    "📊 Clinician Dashboard",
    "📝 Patient Registration & Intake",
    "📹 Kinematic Motion AI Suite",
    "📋 Official Protocol & Rx Suite",
    "📈 Patient Mobility Progress",
    "💬 Teleconsultation Virtual Lobby",
    "⚙️ System Settings & Node Config"
]

menu = st.sidebar.radio("", menu_options)

# Sidebar Bottom Health Status
st.sidebar.markdown("""
    <div class="status-widget">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
            <span style="font-weight:700; color:#F8FAFC;">Node Status:</span>
            <span style="color:#10B981; font-weight:800;">● ONLINE</span>
        </div>
        <div style="color:#94A3B8; font-size:0.75rem;">Engine: TeleSynapse AI v3.5 Enterprise</div>
        <div style="color:#94A3B8; font-size:0.75rem;">Latency: 24ms (Local Mesh)</div>
    </div>
""", unsafe_allow_html=True)


# --- 5. MODULE 1: CLINICIAN DASHBOARD ---
if menu == "📊 Clinician Dashboard":
    st.markdown("""
        <div class="hero-banner">
            <div class="hero-title">🏥 TeleSynapse Clinical Dashboard & AI Suite</div>
            <div class="hero-sub">Real-time Operations & Biomechanical Diagnostics Engine</div>
        </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
            <div class="stat-card-blue">
                <div style="font-size:0.75rem; font-weight:700; color:#93C5FD; text-transform:uppercase;">Active Tele-Rehab Consults</div>
                <div style="font-size:2.3rem; font-weight:800; color:#60A5FA; margin-top:4px;">{len(st.session_state['appointments'])}</div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        confirmed = len([a for a in st.session_state["appointments"] if a["Status"] == "CONFIRMED"])
        st.markdown(f"""
            <div class="stat-card-emerald">
                <div style="font-size:0.75rem; font-weight:700; color:#A7F3D0; text-transform:uppercase;">Confirmed Protocol Queue</div>
                <div style="font-size:2.3rem; font-weight:800; color:#34D399; margin-top:4px;">{confirmed}</div>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        pending = len([a for a in st.session_state["appointments"] if a["Status"] == "PENDING"])
        st.markdown(f"""
            <div class="stat-card-amber">
                <div style="font-size:0.75rem; font-weight:700; color:#FDE68A; text-transform:uppercase;">Pending Triage Review</div>
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

# --- 6. MODULE 2: PATIENT REGISTRATION & INTAKE ---
elif menu == "📝 Patient Registration & Intake":
    st.markdown("""
        <div class="hero-banner">
            <div class="hero-title">📝 Patient Registration & Intake Portal</div>
            <div class="hero-sub">Register clinical demographics and queue patients for kinematic evaluation.</div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("<h4 style='color:#FFFFFF;'>Patient Intake Form</h4>", unsafe_allow_html=True)
        patient_name = st.text_input("Patient Full Legal Name", placeholder="e.g. Fazal Bibi")
        doctor_name = st.selectbox("Assign Lead Specialist", ["Dr. Shahzaib Mughal", "Dr. Hassan Raza", "Dr. Ayesha Malik"])
        rehab_type = st.selectbox("Target Diagnostic Protocol", ["Knee ACL Protocol", "Shoulder Abduction Index", "Elbow Mobility Protocol", "Post-Stroke Assessment"])
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
        st.markdown("<h4 style='color:#FFFFFF;'>Active Register</h4>", unsafe_allow_html=True)
        df_apps = pd.DataFrame(st.session_state["appointments"])
        st.dataframe(df_apps, use_container_width=True)

# --- 7. MODULE 3: KINEMATIC MOTION AI SUITE ---
elif menu == "📹 Kinematic Motion AI Suite":
    st.markdown("""
        <div class="hero-banner">
            <div class="hero-title">📹 AI Biomechanical & Kinematic Analysis</div>
            <div class="hero-sub">Computer Vision Range-of-Motion (ROM) & Joint Angle Tracking Engine</div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("<h4 style='color:#FFFFFF;'>Live Motion Capture Stream</h4>", unsafe_allow_html=True)
        st.info("📷 OpenCV / MediaPipe Joint Angle Pipeline: Ready for WebRTC input feed.")
        st.file_uploader("Upload Patient Exercise Video for Pose Kinematics (.mp4, .avi)", type=["mp4", "avi"])
    with col2:
        st.markdown("<h4 style='color:#FFFFFF;'>Target Metrics</h4>", unsafe_allow_html=True)
        st.metric("Flexion Angle (Peak)", "112.4°", delta="4.2° improvement")
        st.metric("Extension Deficit", "3.1°", delta="-1.5° recovery")
        st.metric("Joint Velocity", "42.8 deg/s", delta="Optimal")

# --- 8. MODULE 4: OFFICIAL PROTOCOL & RX SUITE ---
elif menu == "📋 Official Protocol & Rx Suite":
    st.markdown("""
        <div class="hero-banner">
            <div class="hero-title">📋 Official Medical Evaluation & Protocol</div>
            <div class="hero-sub">Automated clinical prescriptions and biomechanical therapy blueprints.</div>
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

# --- 9. MODULE 5: PATIENT MOBILITY PROGRESS ---
elif menu == "📈 Patient Mobility Progress":
    st.markdown("""
        <div class="hero-banner">
            <div class="hero-title">📈 Longitudinal Range of Motion Analytics</div>
            <div class="hero-sub">Multi-session compliance tracking and torque recovery curves.</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Sample Trend Data
    progress_data = pd.DataFrame({
        "Session": ["Week 1", "Week 2", "Week 3", "Week 4", "Week 5"],
        "Flexion Angle (Degrees)": [75, 88, 98, 110, 122],
        "Target ROM": [120, 120, 120, 120, 120]
    }).set_index("Session")
    
    st.line_chart(progress_data)

# --- 10. MODULE 6: TELECONSULTATION VIRTUAL LOBBY ---
elif menu == "💬 Teleconsultation Virtual Lobby":
    st.markdown("""
        <div class="hero-banner">
            <div class="hero-title">💬 Encrypted Telehealth Lobby</div>
            <div class="hero-sub">Secure Virtual Consultation Room for Specialists & Patients</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.success("🔒 Peer-to-Peer Encrypted Room Active: Room ID #TS-9921")
    st.text_input("Enter Specialist Passcode", type="password")
    st.button("Launch Virtual Room Session", type="primary")

# --- 11. MODULE 7: SYSTEM SETTINGS & NODE CONFIG ---
else:
    st.markdown("""
        <div class="hero-banner">
            <div class="hero-title">⚙️ Portal Settings & System Architecture</div>
            <div class="hero-sub">API Integration, Database Connectivity & Engine Configurations</div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox("FastAPI Backend Node", ["Node-01 (Primary Pakistan)", "Node-02 (Backup Sandbox)"])
        st.toggle("Enable Real-Time OpenCV Frame Dropping", value=True)
        st.toggle("High Contrast Accessibility Mode", value=True)
    with col2:
        st.text_input("Streamlit WebRTC Gateway Port", value="8501")
        st.text_input("Database Connection URI", value="postgresql://admin:***@localhost:5432/tele_rehab")
