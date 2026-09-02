import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="TeleSynapse | Clinical Tele-Rehab Portal",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. AUTOMATED EMAIL NOTIFICATION FUNCTION ---
def send_doctor_email_notification(doctor_email, patient_name, date_time, protocol):
    sender_email = "alerts@telesynapse.com"       # Replace with your sender email
    sender_password = "your-app-password"         # Replace with Gmail App Password (16-digit)
    
    subject = f"🚨 New Tele-Rehab Appointment: {patient_name}"
    body = f"Hello Doctor,\n\nNew patient appointment request received:\n\nPatient: {patient_name}\nProtocol: {protocol}\nTime: {date_time}\n\nPlease log in to TeleSynapse Portal to confirm."
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = doctor_email
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, doctor_email, msg.as_string())

# --- 3. ACCESSIBILITY TOGGLE & DYNAMIC FONT SIZES ---
st.sidebar.markdown("### ♿ Accessibility Mode")
big_text = st.sidebar.toggle("🔍 Big Text Mode (Buzurgon Ke Liye)", value=False)

base_font_size = "18px" if big_text else "16px"
hero_title_size = "2.1rem" if big_text else "1.7rem"
body_p_size = "1.05rem" if big_text else "0.9rem"

# --- 4. DARK NAVY & MINT GREEN CUSTOM CSS ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

    /* Hide Streamlit Chrome */
    #MainMenu {{ visibility: hidden !important; }}
    footer {{ visibility: hidden !important; }}
    .stDeployButton {{ display: none !important; }}
    header[data-testid="stHeader"] {{ background-color: transparent !important; }}

    /* Global Body Styling */
    html, body, [class*="css"] {{
        font-family: 'Poppins', sans-serif !important;
        font-size: {base_font_size} !important;
    }}
    .stApp {{
        background-color: #0D1B2A !important;
        color: #E0E1DD !important;
    }}

    /* Typography Accent */
    h1, h2, h3 {{
        color: #94D2BD !important;
        font-weight: 700 !important;
        letter-spacing: -0.3px;
    }}
    h4, h5, h6 {{
        color: #0A9396 !important;
        font-weight: 600 !important;
    }}
    p, span, label {{
        color: #E0E1DD;
        font-size: {body_p_size};
    }}

    /* Sidebar Styling (#1B263B) */
    [data-testid="stSidebar"] {{
        background-color: #1B263B !important;
        border-right: 1px solid #005F73 !important;
        min-width: 300px !important;
    }}
    [data-testid="stSidebar"] * {{
        color: #E0E1DD !important;
    }}

    /* Brand Container Logo & Tagline */
    .brand-container {{
        padding: 18px 14px;
        background: linear-gradient(135deg, #005F73 0%, #0D1B2A 100%);
        border: 1px solid #0A9396;
        border-radius: 12px;
        margin-bottom: 22px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }}
    .brand-title {{
        color: #94D2BD !important;
        font-size: 1.6rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: 0.5px;
    }}
    .brand-sub {{
        color: #A3B1C6 !important;
        font-size: 0.76rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-top: 4px;
    }}

    /* Hero Banner */
    .hero-banner {{
        background: linear-gradient(135deg, #1B263B 0%, #005F73 100%);
        border: 1px solid #0A9396;
        border-radius: 14px;
        padding: 24px 30px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35);
    }}
    .hero-title {{
        color: #94D2BD !important;
        font-size: {hero_title_size};
        font-weight: 700;
        margin-bottom: 4px;
    }}
    .hero-sub {{
        color: #A3B1C6 !important;
        font-size: {body_p_size};
    }}

    /* Stat Cards */
    .stat-card {{
        background-color: #1B263B;
        border: 1px solid #005F73;
        border-top: 4px solid #0A9396;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.25);
    }}
    .stat-card-title {{
        font-size: 0.78rem;
        font-weight: 700;
        color: #A3B1C6;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    .stat-card-value {{
        font-size: 2.3rem;
        font-weight: 800;
        color: #94D2BD;
        margin-top: 4px;
    }}

    /* Patient Roster Cards */
    .card-confirmed {{
        background-color: #1B263B !important;
        border-left: 5px solid #0A9396 !important;
        border-top: 1px solid #005F73;
        border-right: 1px solid #005F73;
        border-bottom: 1px solid #005F73;
        border-radius: 12px;
        padding: 18px 22px;
        margin-bottom: 14px;
    }}
    .card-pending {{
        background-color: #1B263B !important;
        border-left: 5px solid #EE9B00 !important;
        border-top: 1px solid #005F73;
        border-right: 1px solid #005F73;
        border-bottom: 1px solid #005F73;
        border-radius: 12px;
        padding: 18px 22px;
        margin-bottom: 14px;
    }}

    /* Status Badges */
    .badge-confirmed {{
        font-weight: 700;
        font-size: 0.78rem;
        color: #94D2BD;
        background: #0D1B2A;
        padding: 5px 14px;
        border-radius: 20px;
        border: 1px solid #0A9396;
    }}
    .badge-pending {{
        font-weight: 700;
        font-size: 0.78rem;
        color: #EE9B00;
        background: #0D1B2A;
        padding: 5px 14px;
        border-radius: 20px;
        border: 1px solid #EE9B00;
    }}

    /* Buttons: Mint Green CTA */
    .stButton>button {{
        background: linear-gradient(90deg, #94D2BD, #0A9396) !important;
        color: #0D1B2A !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 10px 24px !important;
        font-size: 0.98rem !important;
        transition: all 0.3s ease;
    }}
    .stButton>button:hover {{
        background: #005F73 !important;
        color: #FFFFFF !important;
        transform: scale(1.02);
    }}

    /* Input Controls Styling */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stNumberInput>div>div>input, .stDateInput>div>div>input {{
        background-color: #0D1B2A !important;
        color: #E0E1DD !important;
        border-radius: 8px !important;
        border: 1px solid #005F73 !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 5. INITIALIZE SESSION STATE ---
if "appointments" not in st.session_state:
    st.session_state["appointments"] = [
        {"Patient": "Ali Ahmed", "Doctor": "Dr. Shahzaib Mughal", "Date": "2026-09-03", "Time": "10:00 AM", "Type": "Knee ACL Protocol", "Status": "CONFIRMED"},
        {"Patient": "Sara Khan", "Doctor": "Dr. Hassan Raza", "Date": "2026-09-03", "Time": "11:30 AM", "Type": "Shoulder Abduction Index", "Status": "PENDING"},
        {"Patient": "Usman Tariq", "Doctor": "Dr. Ayesha Malik", "Date": "2026-09-04", "Time": "02:00 PM", "Type": "Elbow Mobility Protocol", "Status": "CONFIRMED"}
    ]

# --- 6. SIDEBAR BRANDING & NAVIGATION ---
st.sidebar.markdown("""
    <div class="brand-container">
        <div class="brand-title">🩺 Tele-Synapse</div>
        <div class="brand-sub">Rehab Anywhere, Anytime</div>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown("<p style='font-size:0.75rem; font-weight:700; color:#0A9396; text-transform:uppercase; letter-spacing:1px;'>Navigation Menu</p>", unsafe_allow_html=True)

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

# --- 7. MODULE 1: CLINICIAN DASHBOARD ---
if menu == "📊 Clinician Dashboard":
    st.markdown("""
        <div class="hero-banner">
            <div class="hero-title">🏥 Specialist Clinical Dashboard</div>
            <div class="hero-sub">Real-Time Biomechanical Analytics & Doctor Notification Stream</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Doctor Logged-in Profile Selector
    selected_doctor = st.selectbox(
        "👨‍⚕️ Select Logged-in Specialist Profile:", 
        ["All Doctors", "Dr. Shahzaib Mughal", "Dr. Hassan Raza", "Dr. Ayesha Malik"]
    )
    
    # Filter Appointments
    if selected_doctor != "All Doctors":
        doctor_apps = [a for a in st.session_state["appointments"] if a["Doctor"] == selected_doctor]
    else:
        doctor_apps = st.session_state["appointments"]

    pending_count = len([a for a in doctor_apps if a["Status"] == "PENDING"])
    confirmed_count = len([a for a in doctor_apps if a["Status"] == "CONFIRMED"])
    
    if pending_count > 0:
        st.warning(f"🔔 **Notification:** Aap ke paas {pending_count} new pending patient appointment request(s) hain!")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-card-title">Assigned Patients</div>
                <div class="stat-card-value">{len(doctor_apps)}</div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-card-title">Confirmed Schedule</div>
                <div class="stat-card-value" style="color:#94D2BD;">{confirmed_count}</div>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-card-title">Pending Action Required</div>
                <div class="stat-card-value" style="color:#EE9B00;">{pending_count}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><h3>📋 Active Patient Roster</h3>", unsafe_allow_html=True)
    
    for idx, app in enumerate(doctor_apps):
        status_class = "card-confirmed" if app["Status"] == "CONFIRMED" else "card-pending"
        badge_class = "badge-confirmed" if app["Status"] == "CONFIRMED" else "badge-pending"
        
        st.markdown(f"""
            <div class="{status_class}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 700; font-size: 1.1rem; color: #94D2BD;">👤 Patient: {app['Patient']}</span>
                    <span class="{badge_class}">{app['Status']}</span>
                </div>
                <div style="margin-top: 8px; font-size: 0.88rem; color: #A3B1C6;">
                    <b style="color:#E0E1DD;">Lead Doctor:</b> {app['Doctor']} &nbsp;|&nbsp; 
                    <b style="color:#E0E1DD;">Schedule:</b> {app['Time']} ({app['Date']}) &nbsp;|&nbsp; 
                    <b style="color:#E0E1DD;">Protocol:</b> {app['Type']}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Doctor Action Button to Confirm Pending Requests
        if app["Status"] == "PENDING":
            if st.button(f"✅ Accept & Confirm Appointment ({app['Patient']})", key=f"accept_{idx}"):
                app["Status"] = "CONFIRMED"
                st.success(f"Appointment confirmed for {app['Patient']}!")
                st.rerun()

# --- 8. MODULE 2: PATIENT REGISTRATION & INTAKE ---
elif menu == "📝 Patient Registration & Intake":
    st.markdown("""
        <div class="hero-banner">
            <div class="hero-title">📝 Patient Intake & Booking Suite</div>
            <div class="hero-sub">Book therapy sessions and trigger instant notifications to assigned specialists.</div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("<h4>💪 Book Session Form</h4>", unsafe_allow_html=True)
        patient_name = st.text_input("Patient Full Name", placeholder="e.g. Fazal Bibi")
        doctor_name = st.selectbox("Assign Specialist Doctor", ["Dr. Shahzaib Mughal", "Dr. Hassan Raza", "Dr. Ayesha Malik"])
        rehab_type = st.selectbox("Target Protocol", ["Knee ACL Protocol", "Shoulder Abduction Index", "Elbow Mobility Protocol", "Post-Stroke Assessment"])
        app_date = st.date_input("Consultation Date")
        app_time = st.selectbox("Time Slot", ["09:00 AM", "10:00 AM", "11:30 AM", "02:00 PM", "04:00 PM"])
        
        if st.button("💪 Book Session Now"):
            if patient_name:
                new_app = {
                    "Patient": patient_name,
                    "Doctor": doctor_name,
                    "Date": str(app_date),
                    "Time": app_time,
                    "Type": rehab_type,
                    "Status": "PENDING"
                }
                st.session_state["appointments"].append(new_app)
                
                # Automated Email Attempt
                try:
                    doctor_emails = {
                        "Dr. Shahzaib Mughal": "shahzaib@example.com",
                        "Dr. Hassan Raza": "hassan@example.com",
                        "Dr. Ayesha Malik": "ayesha@example.com"
                    }
                    target_email = doctor_emails.get(doctor_name, "alerts@telesynapse.com")
                    send_doctor_email_notification(
                        doctor_email=target_email,
                        patient_name=patient_name,
                        date_time=f"{app_date} at {app_time}",
                        protocol=rehab_type
                    )
                    st.success(f"Session booked for {patient_name}! Email alert sent to {doctor_name}.")
                except Exception:
                    st.success(f"Session booked for {patient_name}! Request forwarded to {doctor_name}'s dashboard.")
            else:
                st.error("Patient name is required.")

    with col2:
        st.markdown("<h4>📋 Intake Registry Overview</h4>", unsafe_allow_html=True)
        df_apps = pd.DataFrame(st.session_state["appointments"])
        st.dataframe(df_apps, use_container_width=True)

# --- 9. MODULE 3: KINEMATIC MOTION AI SUITE ---
elif menu == "📹 Kinematic Motion AI Suite":
    st.markdown("""
        <div class="hero-banner">
            <div class="hero-title">📹 Kinematic Joint & Motion Analysis</div>
            <div class="hero-sub">Computer Vision Range-of-Motion (ROM) & Joint Tracking Engine</div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("<h4>📹 Live Motion Capture Feed</h4>", unsafe_allow_html=True)
        st.info("📷 OpenCV / MediaPipe Joint Angle Pipeline: Ready for WebRTC video feed.")
        st.file_uploader("Upload Motion Video (.mp4, .avi)", type=["mp4", "avi"])
    with col2:
        st.markdown("<h4>📊 Angle Metrics</h4>", unsafe_allow_html=True)
        st.metric("Peak Flexion Angle", "112.4°", delta="4.2° improvement")
        st.metric("Extension Deficit", "3.1°", delta="-1.5° recovery")
        st.metric("Joint Velocity", "42.8 deg/s", delta="Normal")

# --- 10. MODULE 4: OFFICIAL PROTOCOL & RX SUITE ---
elif menu == "📋 Official Protocol & Rx Suite":
    st.markdown("""
        <div class="hero-banner">
            <div class="hero-title">💊 Prescription & Rehab Protocol Suite</div>
            <div class="hero-sub">Official therapy guidelines and clinical blueprints.</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style="background:#1B263B; border-left:5px solid #0A9396; padding:18px; border-radius:12px; margin-bottom:14px; border-top:1px solid #005F73; border-right:1px solid #005F73; border-bottom:1px solid #005F73;">
            <b style="color:#94D2BD;">🩺 Diagnosed Condition:</b> Range of Motion Restriction (Post-op Knee Reconstruction).
        </div>
        <div style="background:#1B263B; border-left:5px solid #94D2BD; padding:18px; border-radius:12px; margin-bottom:14px; border-top:1px solid #005F73; border-right:1px solid #005F73; border-bottom:1px solid #005F73;">
            <b style="color:#94D2BD;">💊 Triage Category:</b> ACTIVE CLINICAL REHABILITATION
        </div>
        <div style="background:#1B263B; border-left:5px solid #005F73; padding:18px; border-radius:12px; margin-bottom:14px; border-top:1px solid #005F73; border-right:1px solid #005F73; border-bottom:1px solid #005F73;">
            <b style="color:#94D2BD;">💪 Physiotherapy Plan:</b> Daily 20-min guided flexion therapy with pose estimation feedback.
        </div>
    """, unsafe_allow_html=True)

# --- 11. MODULE 5: PATIENT MOBILITY PROGRESS ---
elif menu == "📈 Patient Mobility Progress":
    st.markdown("""
        <div class="hero-banner">
            <div class="hero-title">📈 Range of Motion (ROM) Progress Analytics</div>
            <div class="hero-sub">Multi-session ROM recovery curves vs target benchmarks.</div>
        </div>
    """, unsafe_allow_html=True)
    
    progress_data = pd.DataFrame({
        "Session": ["Week 1", "Week 2", "Week 3", "Week 4", "Week 5"],
        "Flexion Angle (Degrees)": [75, 88, 98, 110, 122],
        "Target ROM": [120, 120, 120, 120, 120]
    }).set_index("Session")
    
    st.line_chart(progress_data)

# --- 12. MODULE 6: TELECONSULTATION VIRTUAL LOBBY ---
elif menu == "💬 Teleconsultation Virtual Lobby":
    st.markdown("""
        <div class="hero-banner">
            <div class="hero-title">💬 Encrypted Telehealth Lobby</div>
            <div class="hero-sub">Secure Virtual Consultation Room for Specialists & Patients</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.success("🔒 Encrypted Room Active: Channel #TS-9921")
    st.text_input("Enter Specialist Passcode", type="password")
    st.button("Launch Virtual Consultation Session")

# --- 13. MODULE 7: SYSTEM SETTINGS & NODE CONFIG ---
else:
    st.markdown("""
        <div class="hero-banner">
            <div class="hero-title">⚙️ Portal Settings & System Architecture</div>
            <div class="hero-sub">FastAPI Backend Gateway, OpenCV Pipelines & Database Connectors</div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox("FastAPI Node Host", ["Node-01 (Primary Pakistan)", "Node-02 (Backup Sandbox)"])
        st.toggle("Enable OpenCV Frame Drop Safeguard", value=True)
        st.toggle("High Contrast Accessibility Filter", value=True)
    with col2:
        st.text_input("WebRTC Gateway Port", value="8501")
        st.text_input("Database URI", value="postgresql://admin:***@localhost:5432/tele_rehab")
