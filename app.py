import streamlit as st
import pandas as pd

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="TeleSynapse | Clinical Tele-Rehab Portal",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. MEDICAL TRUST COLOR SCHEME & UI CSS ---
st.markdown("""
    <style>
    /* Google Fonts: Inter & Poppins */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@500;600;700;800&display=swap');

    /* Hide Default Streamlit Chrome */
    #MainMenu { visibility: hidden !important; }
    footer { visibility: hidden !important; }
    .stDeployButton { display: none !important; }
    header[data-testid="stHeader"] {
        background-color: transparent !important;
        z-index: 100;
    }

    /* Base Body & Canvas - Soft Gray Background (#F8F9FA) */
    html, body, [class*="css"] {
        font-family: 'Inter', 'Poppins', sans-serif;
    }
    .stApp {
        background-color: #F8F9FA !important;
        color: #005F73 !important;
    }

    /* -----------------------------------------------------------
       SIDEBAR - DARK NAVY (#005F73) & TEAL ACCENTS
       ----------------------------------------------------------- */
    [data-testid="stSidebar"] {
        background-color: #005F73 !important;
        border-right: 1px solid #0A9396 !important;
        min-width: 300px !important;
    }
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }

    /* Sidebar Brand Box */
    .brand-container {
        padding: 18px 14px;
        background: linear-gradient(135deg, #0A9396 0%, #005F73 100%);
        border: 1px solid #94D2BD;
        border-radius: 12px;
        margin-bottom: 22px;
        text-align: center;
        box-shadow: 0 4px 14px rgba(10, 147, 150, 0.25);
    }
    .brand-title {
        color: #FFFFFF !important;
        font-family: 'Poppins', sans-serif;
        font-size: 1.6rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin: 0;
    }
    .brand-sub {
        color: #E0F2F1 !important;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-top: 4px;
    }

    /* System Status Box */
    .status-widget {
        background-color: #004D5A;
        border: 1px solid #0A9396;
        border-radius: 8px;
        padding: 12px;
        margin-top: 24px;
        font-size: 0.8rem;
    }

    /* -----------------------------------------------------------
       MAIN HERO BANNER - TEAL & NAVY GRADIENT
       ----------------------------------------------------------- */
    .hero-banner {
        background: linear-gradient(135deg, #005F73 0%, #0A9396 100%);
        border-radius: 12px;
        padding: 24px 30px;
        text-align: center;
        color: #FFFFFF;
        box-shadow: 0 6px 18px rgba(10, 147, 150, 0.15);
        margin-bottom: 25px;
        border: 1px solid #94D2BD;
    }
    .hero-title {
        color: #FFFFFF !important;
        font-family: 'Poppins', sans-serif;
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 4px;
    }
    .hero-sub {
        color: #E0F2F1 !important;
        font-size: 0.92rem;
        font-weight: 500;
    }

    /* Stat Cards - Clean Clinical White Boxes */
    .stat-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-top: 4px solid #0A9396;
        border-radius: 10px;
        padding: 18px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .stat-card-title {
        font-size: 0.75rem;
        font-weight: 700;
        color: #005F73;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    .stat-card-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #0A9396;
        margin-top: 4px;
    }

    /* Patient Roster Cards */
    .card-confirmed {
        background-color: #FFFFFF !important;
        border-left: 5px solid #0A9396 !important;
        border-top: 1px solid #E2E8F0;
        border-right: 1px solid #E2E8F0;
        border-bottom: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 12px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.03);
    }
    .card-pending {
        background-color: #FFFFFF !important;
        border-left: 5px solid #E9D8A6 !important;
        border-top: 1px solid #E2E8F0;
        border-right: 1px solid #E2E8F0;
        border-bottom: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 12px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.03);
    }

    /* Badges */
    .badge-confirmed {
        font-weight: 700;
        font-size: 0.72rem;
        color: #005F73;
        background: #E0F2F1;
        padding: 4px 12px;
        border-radius: 20px;
        border: 1px solid #94D2BD;
    }
    .badge-pending {
        font-weight: 700;
        font-size: 0.72rem;
        color: #9B2C2C;
        background: #FFF5F5;
        padding: 4px 12px;
        border-radius: 20px;
        border: 1px solid #FEB2B2;
    }

    /* Primary Buttons */
    .stButton>button {
        background-color: #0A9396 !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 8px 18px !important;
    }
    .stButton>button:hover {
        background-color: #005F73 !important;
        color: #FFFFFF !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE DATA STORAGE ---
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
        <div class="brand-sub">Clinical Tele-Rehab</div>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown("<p style='font-size:0.75rem; font-weight:700; color:#94D2BD; text-transform:uppercase; letter-spacing:1px; margin-bottom:8px;'>Clinical Operations</p>", unsafe_allow_html=True)

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

st.sidebar.markdown("""
    <div class="status-widget">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
            <span style="font-weight:600; color:#FFFFFF;">Node Status:</span>
            <span style="color:#94D2BD; font-weight:700;">● ONLINE</span>
        </div>
        <div style="color:#E0F2F1; font-size:0.75rem;">Engine: TeleSynapse AI v3.5</div>
        <div style="color:#E0F2F1; font-size:0.75rem;">Latency: 24ms (Local Mesh)</div>
    </div>
""", unsafe_allow_html=True)


# --- 5. MODULE 1: CLINICIAN DASHBOARD ---
if menu == "📊 Clinician Dashboard":
    st.markdown("""
        <div class="hero-banner">
            <div class="hero-title">🏥 TeleSynapse Clinical Dashboard</div>
            <div class="hero-sub">Real-time Patient Monitoring & Biomechanical Diagnostics Engine</div>
        </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-card-title">Active Consultations</div>
                <div class="stat-card-value">{len(st.session_state['appointments'])}</div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        confirmed = len([a for a in st.session_state["appointments"] if a["Status"] == "CONFIRMED"])
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-card-title">Confirmed Protocols</div>
                <div class="stat-card-value" style="color:#0A9396;">{confirmed}</div>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        pending = len([a for a in st.session_state["appointments"] if a["Status"] == "PENDING"])
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-card-title">Pending Triage Review</div>
                <div class="stat-card-value" style="color:#EE9B00;">{pending}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><h3 style='color:#005F73; font-weight:700;'>📋 Patient Roster</h3>", unsafe_allow_html=True)
    
    for app in st.session_state["appointments"]:
        status_class = "card-confirmed" if app["Status"] == "CONFIRMED" else "card-pending"
        badge_class = "badge-confirmed" if app["Status"] == "CONFIRMED" else "badge-pending"
        
        st.markdown(f"""
            <div class="{status_class}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 700; font-size: 1.1rem; color: #005F73;">👤 {app['Patient']}</span>
                    <span class="{badge_class}">{app['Status']}</span>
                </div>
                <div style="margin-top: 8px; font-size: 0.9rem; color: #4A5568;">
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
            <div class="hero-title">📝 Patient Registration Portal</div>
            <div class="hero-sub">Enter patient clinical details and assign rehabilitation protocols.</div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("<h4 style='color:#005F73;'>Patient Intake Form</h4>", unsafe_allow_html=True)
        patient_name = st.text_input("Patient Full Name", placeholder="e.g. Fazal Bibi")
        doctor_name = st.selectbox("Assign Lead Specialist", ["Dr. Shahzaib Mughal", "Dr. Hassan Raza", "Dr. Ayesha Malik"])
        rehab_type = st.selectbox("Target Diagnostic Protocol", ["Knee ACL Protocol", "Shoulder Abduction Index", "Elbow Mobility Protocol", "Post-Stroke Assessment"])
        app_date = st.date_input("Consultation Date")
        app_time = st.selectbox("Time Slot", ["09:00 AM", "10:00 AM", "11:30 AM", "02:00 PM", "04:00 PM"])
        
        if st.button("Submit Patient Intake Record"):
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
                st.error("Patient full name is required.")

    with col2:
        st.markdown("<h4 style='color:#005F73;'>Active Intake Registry</h4>", unsafe_allow_html=True)
        df_apps = pd.DataFrame(st.session_state["appointments"])
        st.dataframe(df_apps, use_container_width=True)

# --- 7. MODULE 3: KINEMATIC MOTION AI SUITE ---
elif menu == "📹 Kinematic Motion AI Suite":
    st.markdown("""
        <div class="hero-banner">
            <div class="hero-title">📹 Kinematic Joint & Motion Analysis</div>
            <div class="hero-sub">Computer Vision Range-of-Motion (ROM) & Pose Estimation Metrics</div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("<h4 style='color:#005F73;'>Live Motion Capture Feed</h4>", unsafe_allow_html=True)
        st.info("📷 OpenCV / MediaPipe Joint Angle Pipeline: Ready for WebRTC input feed.")
        st.file_uploader("Upload Patient Exercise Video for Pose Kinematics (.mp4, .avi)", type=["mp4", "avi"])
    with col2:
        st.markdown("<h4 style='color:#005F73;'>Kinematic Metrics</h4>", unsafe_allow_html=True)
        st.metric("Flexion Angle (Peak)", "112.4°", delta="4.2° improvement")
        st.metric("Extension Deficit", "3.1°", delta="-1.5° recovery")
        st.metric("Joint Velocity", "42.8 deg/s", delta="Optimal")

# --- 8. MODULE 4: OFFICIAL PROTOCOL & RX SUITE ---
elif menu == "📋 Official Protocol & Rx Suite":
    st.markdown("""
        <div class="hero-banner">
            <div class="hero-title">📋 Medical Protocol & Prescription Suite</div>
            <div class="hero-sub">Clinical therapy guidelines and biomechanical blueprints.</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style="background:#FFFFFF; border-left:5px solid #005F73; padding:18px; border-radius:8px; margin-bottom:14px; box-shadow:0 2px 6px rgba(0,0,0,0.03);">
            <b style="color:#005F73;">Diagnosed Condition:</b> Range of Motion Restriction (Post-op Knee Reconstruction).
        </div>
        <div style="background:#FFFFFF; border-left:5px solid #0A9396; padding:18px; border-radius:8px; margin-bottom:14px; box-shadow:0 2px 6px rgba(0,0,0,0.03);">
            <b style="color:#0A9396;">Triage Category:</b> ACTIVE CLINICAL REHABILITATION
        </div>
        <div style="background:#FFFFFF; border-left:5px solid #94D2BD; padding:18px; border-radius:8px; margin-bottom:14px; box-shadow:0 2px 6px rgba(0,0,0,0.03);">
            <b style="color:#005F73;">Physiotherapy Plan:</b> Progressive mobilization therapy with real-time video feedback.
        </div>
    """, unsafe_allow_html=True)

# --- 9. MODULE 5: PATIENT MOBILITY PROGRESS ---
elif menu == "📈 Patient Mobility Progress":
    st.markdown("""
        <div class="hero-banner">
            <div class="hero-title">📈 Range of Motion (ROM) Progress Analytics</div>
            <div class="hero-sub">Multi-session ROM recovery tracking and compliance curves.</div>
        </div>
    """, unsafe_allow_html=True)
    
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
            <div class="hero-title">💬 Encrypted Telehealth Virtual Room</div>
            <div class="hero-sub">Secure Virtual Consultation Room for Specialists & Patients</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.success("🔒 Peer-to-Peer Encrypted Room Active: Room ID #TS-9921")
    st.text_input("Enter Specialist Passcode", type="password")
    st.button("Launch Virtual Room Session")

# --- 11. MODULE 7: SYSTEM SETTINGS & NODE CONFIG ---
else:
    st.markdown("""
        <div class="hero-banner">
            <div class="hero-title">⚙️ Portal Settings & Architecture</div>
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
