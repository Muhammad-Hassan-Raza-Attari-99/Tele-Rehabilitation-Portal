import streamlit as st
import pandas as pd

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="TeleSynapse | Clinical Tele-Rehab Portal",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. DARK NAVY & TEAL MEDICAL CSS (STRICT COLOR MAP) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@500;600;700;800&display=swap');

    /* Hide Streamlit Default Top Bar & Footer */
    #MainMenu { visibility: hidden !important; }
    footer { visibility: hidden !important; }
    .stDeployButton { display: none !important; }
    header[data-testid="stHeader"] { background-color: transparent !important; }

    /* Main App Body Background (#0D1B2A) & Font */
    html, body, [class*="css"] {
        font-family: 'Poppins', 'Inter', sans-serif;
    }
    .stApp {
        background-color: #0D1B2A !important;
        color: #E0E1DD !important;
    }

    /* Headings Accent (#94D2BD & #0A9396) */
    h1, h2, h3 {
        color: #94D2BD !important;
        font-weight: 700 !important;
    }
    h4, h5, h6 {
        color: #0A9396 !important;
        font-weight: 600 !important;
    }
    p, span, label {
        color: #E0E1DD;
    }
    .stMarkdown p {
        color: #E0E1DD !important;
    }

    /* -----------------------------------------------------------
       SIDEBAR (#1B263B)
       ----------------------------------------------------------- */
    [data-testid="stSidebar"] {
        background-color: #1B263B !important;
        border-right: 1px solid #005F73 !important;
        min-width: 290px !important;
    }
    [data-testid="stSidebar"] * {
        color: #E0E1DD !important;
    }

    /* Sidebar Brand Container */
    .brand-container {
        padding: 16px;
        background: linear-gradient(135deg, #005F73 0%, #0D1B2A 100%);
        border: 1px solid #0A9396;
        border-radius: 10px;
        margin-bottom: 20px;
        text-align: center;
    }
    .brand-title {
        color: #94D2BD !important;
        font-family: 'Poppins', sans-serif;
        font-size: 1.5rem;
        font-weight: 800;
        letter-spacing: 0.5px;
        margin: 0;
    }
    .brand-sub {
        color: #A3B1C6 !important;
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Status Box Sidebar */
    .status-widget {
        background-color: #0D1B2A;
        border: 1px solid #005F73;
        border-radius: 8px;
        padding: 12px;
        margin-top: 20px;
        font-size: 0.8rem;
    }

    /* -----------------------------------------------------------
       HERO BANNER & CARDS (#1B263B)
       ----------------------------------------------------------- */
    .hero-banner {
        background: linear-gradient(135deg, #1B263B 0%, #005F73 100%);
        border: 1px solid #0A9396;
        border-radius: 12px;
        padding: 22px 28px;
        text-align: center;
        margin-bottom: 24px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    .hero-title {
        color: #94D2BD !important;
        font-size: 1.7rem;
        font-weight: 700;
        margin-bottom: 4px;
    }
    .hero-sub {
        color: #A3B1C6 !important;
        font-size: 0.9rem;
    }

    /* Custom Metric Cards */
    .stat-card {
        background-color: #1B263B;
        border: 1px solid #005F73;
        border-top: 4px solid #0A9396;
        border-radius: 10px;
        padding: 18px;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.25);
    }
    .stat-card-title {
        font-size: 0.75rem;
        font-weight: 700;
        color: #A3B1C6;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    .stat-card-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #94D2BD;
        margin-top: 4px;
    }

    /* Patient Roster Cards */
    .card-confirmed {
        background-color: #1B263B !important;
        border-left: 5px solid #0A9396 !important;
        border-top: 1px solid #005F73;
        border-right: 1px solid #005F73;
        border-bottom: 1px solid #005F73;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 12px;
    }
    .card-pending {
        background-color: #1B263B !important;
        border-left: 5px solid #EE9B00 !important;
        border-top: 1px solid #005F73;
        border-right: 1px solid #005F73;
        border-bottom: 1px solid #005F73;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 12px;
    }

    /* Badges */
    .badge-confirmed {
        font-weight: 700;
        font-size: 0.72rem;
        color: #94D2BD;
        background: #0D1B2A;
        padding: 4px 12px;
        border-radius: 20px;
        border: 1px solid #0A9396;
    }
    .badge-pending {
        font-weight: 700;
        font-size: 0.72rem;
        color: #EE9B00;
        background: #0D1B2A;
        padding: 4px 12px;
        border-radius: 20px;
        border: 1px solid #EE9B00;
    }

    /* -----------------------------------------------------------
       BUTTONS & INPUT CONTROL STYLING
       ----------------------------------------------------------- */
    .stButton>button {
        background: linear-gradient(90deg, #0A9396, #005F73) !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        border: 1px solid #94D2BD !important;
        padding: 8px 22px !important;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: #0A9396 !important;
        box-shadow: 0 0 12px rgba(10, 147, 150, 0.5);
        transform: scale(1.01);
    }

    /* Inputs Styling */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stNumberInput>div>div>input, .stDateInput>div>div>input {
        background-color: #0D1B2A !important;
        color: #E0E1DD !important;
        border-radius: 8px !important;
        border: 1px solid #005F73 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE DATA ---
if "appointments" not in st.session_state:
    st.session_state["appointments"] = [
        {"Patient": "Ali Ahmed", "Doctor": "Dr. Shahzaib Mughal", "Date": "2026-09-03", "Time": "10:00 AM", "Type": "Knee ACL Protocol", "Status": "CONFIRMED"},
        {"Patient": "Sara Khan", "Doctor": "Dr. Hassan Raza", "Date": "2026-09-03", "Time": "11:30 AM", "Type": "Shoulder Abduction Index", "Status": "PENDING"},
        {"Patient": "Usman Tariq", "Doctor": "Dr. Ayesha Malik", "Date": "2026-09-04", "Time": "02:00 PM", "Type": "Elbow Mobility Protocol", "Status": "CONFIRMED"}
    ]

# --- 4. SIDEBAR NAVIGATION ---
st.sidebar.markdown("""
    <div class="brand-container">
        <div class="brand-title">TELESYNAPSE</div>
        <div class="brand-sub">Clinical Tele-Rehab</div>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown("<p style='font-size:0.75rem; font-weight:700; color:#0A9396; text-transform:uppercase; letter-spacing:1px;'>Clinical Modules</p>", unsafe_allow_html=True)

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
        <div style="display:flex; justify-space-between; align-items:center; margin-bottom:4px;">
            <span style="font-weight:600; color:#E0E1DD;">System Status:</span>
            <span style="color:#94D2BD; font-weight:700;">● ONLINE</span>
        </div>
        <div style="color:#A3B1C6; font-size:0.75rem;">Backend: TeleSynapse Engine v3.5</div>
        <div style="color:#A3B1C6; font-size:0.75rem;">Latency: 21ms (Dark Mesh)</div>
    </div>
""", unsafe_allow_html=True)


# --- 5. MODULE 1: CLINICIAN DASHBOARD ---
if menu == "📊 Clinician Dashboard":
    st.markdown("""
        <div class="hero-banner">
            <div class="hero-title">🏥 TeleSynapse Clinical Dashboard</div>
            <div class="hero-sub">Real-Time Biomechanical Analytics & Patient Triage System</div>
        </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-card-title">Total Consultations</div>
                <div class="stat-card-value">{len(st.session_state['appointments'])}</div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        confirmed = len([a for a in st.session_state["appointments"] if a["Status"] == "CONFIRMED"])
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-card-title">Confirmed Active Protocols</div>
                <div class="stat-card-value" style="color:#94D2BD;">{confirmed}</div>
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

    st.markdown("<br><h3>📋 Active Patient Roster</h3>", unsafe_allow_html=True)
    
    for app in st.session_state["appointments"]:
        status_class = "card-confirmed" if app["Status"] == "CONFIRMED" else "card-pending"
        badge_class = "badge-confirmed" if app["Status"] == "CONFIRMED" else "badge-pending"
        
        st.markdown(f"""
            <div class="{status_class}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 700; font-size: 1.1rem; color: #94D2BD;">👤 {app['Patient']}</span>
                    <span class="{badge_class}">{app['Status']}</span>
                </div>
                <div style="margin-top: 8px; font-size: 0.88rem; color: #A3B1C6;">
                    <b style="color:#E0E1DD;">Lead Specialist:</b> {app['Doctor']} &nbsp;|&nbsp; 
                    <b style="color:#E0E1DD;">Schedule:</b> {app['Time']} ({app['Date']}) &nbsp;|&nbsp; 
                    <b style="color:#E0E1DD;">Protocol:</b> {app['Type']}
                </div>
            </div>
        """, unsafe_allow_html=True)

# --- 6. MODULE 2: PATIENT REGISTRATION & INTAKE ---
elif menu == "📝 Patient Registration & Intake":
    st.markdown("""
        <div class="hero-banner">
            <div class="hero-title">📝 Patient Intake & Registration</div>
            <div class="hero-sub">Register new patients and assign biomechanical rehabilitation protocols.</div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("<h4>Patient Intake Form</h4>", unsafe_allow_html=True)
        patient_name = st.text_input("Patient Full Name", placeholder="e.g. Fazal Bibi")
        doctor_name = st.selectbox("Assign Lead Specialist", ["Dr. Shahzaib Mughal", "Dr. Hassan Raza", "Dr. Ayesha Malik"])
        rehab_type = st.selectbox("Target Protocol", ["Knee ACL Protocol", "Shoulder Abduction Index", "Elbow Mobility Protocol", "Post-Stroke Assessment"])
        app_date = st.date_input("Consultation Date")
        app_time = st.selectbox("Time Slot", ["09:00 AM", "10:00 AM", "11:30 AM", "02:00 PM", "04:00 PM"])
        
        if st.button("Submit Registration Record"):
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
                st.success(f"Record for {patient_name} submitted successfully!")
            else:
                st.error("Patient name is required.")

    with col2:
        st.markdown("<h4>Intake Registry Overview</h4>", unsafe_allow_html=True)
        df_apps = pd.DataFrame(st.session_state["appointments"])
        st.dataframe(df_apps, use_container_width=True)

# --- 7. MODULE 3: KINEMATIC MOTION AI SUITE ---
elif menu == "📹 Kinematic Motion AI Suite":
    st.markdown("""
        <div class="hero-banner">
            <div class="hero-title">📹 Kinematic Joint & Motion Analysis</div>
            <div class="hero-sub">Computer Vision Range-of-Motion (ROM) & Pose Metrics Engine</div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("<h4>Live Pose Kinematics Feed</h4>", unsafe_allow_html=True)
        st.info("📷 OpenCV / MediaPipe Joint Tracking: Engine Ready.")
        st.file_uploader("Upload Motion Capture File (.mp4, .avi)", type=["mp4", "avi"])
    with col2:
        st.markdown("<h4>Angle Metrics</h4>", unsafe_allow_html=True)
        st.metric("Peak Flexion Angle", "112.4°", delta="4.2° improvement")
        st.metric("Extension Deficit", "3.1°", delta="-1.5° recovery")
        st.metric("Joint Angular Velocity", "42.8 deg/s", delta="Normal Range")

# --- 8. MODULE 4: OFFICIAL PROTOCOL & RX SUITE ---
elif menu == "📋 Official Protocol & Rx Suite":
    st.markdown("""
        <div class="hero-banner">
            <div class="hero-title">📋 Clinical Protocol & Prescription Suite</div>
            <div class="hero-sub">Therapy guidelines and prescription specifications.</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style="background:#1B263B; border-left:5px solid #0A9396; padding:18px; border-radius:8px; margin-bottom:14px; border-top:1px solid #005F73; border-right:1px solid #005F73; border-bottom:1px solid #005F73;">
            <b style="color:#94D2BD;">Diagnosed Condition:</b> Range of Motion Restriction (Post-op Knee Reconstruction).
        </div>
        <div style="background:#1B263B; border-left:5px solid #94D2BD; padding:18px; border-radius:8px; margin-bottom:14px; border-top:1px solid #005F73; border-right:1px solid #005F73; border-bottom:1px solid #005F73;">
            <b style="color:#94D2BD;">Triage Status:</b> ACTIVE CLINICAL REHABILITATION
        </div>
        <div style="background:#1B263B; border-left:5px solid #005F73; padding:18px; border-radius:8px; margin-bottom:14px; border-top:1px solid #005F73; border-right:1px solid #005F73; border-bottom:1px solid #005F73;">
            <b style="color:#94D2BD;">Physiotherapy Plan:</b> Daily 20-min guided flexion therapy with real-time pose tracking.
        </div>
    """, unsafe_allow_html=True)

# --- 9. MODULE 5: PATIENT MOBILITY PROGRESS ---
elif menu == "📈 Patient Mobility Progress":
    st.markdown("""
        <div class="hero-banner">
            <div class="hero-title">📈 Range of Motion (ROM) Progress Analytics</div>
            <div class="hero-sub">Multi-session ROM recovery tracking vs targeted benchmarks.</div>
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
            <div class="hero-title">💬 Encrypted Telehealth Room</div>
            <div class="hero-sub">Secure Peer-to-Peer Virtual Consultation Environment</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.success("🔒 Encrypted Tele-Channel Active: Room #TS-9921")
    st.text_input("Enter Passcode", type="password")
    st.button("Launch Video Consultation Session")

# --- 11. MODULE 7: SYSTEM SETTINGS & NODE CONFIG ---
else:
    st.markdown("""
        <div class="hero-banner">
            <div class="hero-title">⚙️ System Settings & Node Architecture</div>
            <div class="hero-sub">FastAPI Endpoints, OpenCV Parameters & Database Configurations</div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox("FastAPI Node Host", ["Node-01 (Primary Pakistan)", "Node-02 (Backup Sandbox)"])
        st.toggle("Enable Real-Time OpenCV Frame Drop Safeguard", value=True)
        st.toggle("High Contrast Dark Mode", value=True)
    with col2:
        st.text_input("WebRTC Gateway Port", value="8501")
        st.text_input("Database URI", value="postgresql://admin:***@localhost:5432/tele_rehab")
