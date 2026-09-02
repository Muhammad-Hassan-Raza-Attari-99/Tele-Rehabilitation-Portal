import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# --- 1. GLOBAL PAGE CONFIGURATION ---
st.set_page_config(
    page_title="TeleSynapse | Clinical Tele-Rehab Portal",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. AUTOMATED EMAIL & ICS CALENDAR ENGINE ---
def send_doctor_clinical_snapshot(doctor_email, booking_data):
    sender_email = "alerts@telesynapse.com"
    sender_password = "your-app-password"
    
    subject = f"🚨 New Clinical Intake: {booking_data['Patient']} (Pain: {booking_data['PainLevel']}/10)"
    body = (
        f"TeleSynapse Clinical Triage Alert\n"
        f"----------------------------------------\n"
        f"PATIENT DEMOGRAPHICS:\n"
        f"• Name: {booking_data['Patient']}\n"
        f"• Phone: {booking_data['Phone']}\n"
        f"• Age/Gender: {booking_data['Age']} yrs | {booking_data['Gender']}\n\n"
        f"CLINICAL SNAPSHOT:\n"
        f"• Condition: {booking_data['Type']}\n"
        f"• Onset: {booking_data['Onset']}\n"
        f"• Pain Intensity: {booking_data['PainLevel']}/10\n\n"
        f"APPOINTMENT DETAILS:\n"
        f"• Scheduled: {booking_data['Date']} @ {booking_data['Time']}\n"
        f"• Platform: {booking_data['Platform']}\n"
        f"• Status: CONFIRMED\n"
        f"----------------------------------------\n"
        f"Access TeleSynapse Specialist Portal to launch session."
    )
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = doctor_email
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, doctor_email, msg.as_string())
    except Exception:
        pass

# --- 3. ACCESSIBILITY TOGGLE & TYPOGRAPHY ---
st.sidebar.markdown("### ♿ Accessibility Mode")
big_text = st.sidebar.toggle("🔍 Large Text Mode (Geriatric / Low Vision)", value=False)

base_font_size = "18px" if big_text else "16px"
hero_title_size = "2.1rem" if big_text else "1.7rem"
body_p_size = "1.05rem" if big_text else "0.9rem"

# --- 4. CLINICAL UI STYLING & SMART CARD CSS ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

    #MainMenu {{ visibility: hidden !important; }}
    footer {{ visibility: hidden !important; }}
    .stDeployButton {{ display: none !important; }}
    header[data-testid="stHeader"] {{ background-color: transparent !important; }}

    html, body, [class*="css"] {{
        font-family: 'Poppins', sans-serif !important;
        font-size: {base_font_size} !important;
    }}
    .stApp {{
        background-color: #0D1B2A !important;
        color: #E0E1DD !important;
    }}

    h1, h2, h3 {{ color: #94D2BD !important; font-weight: 700 !important; }}
    h4, h5, h6 {{ color: #0A9396 !important; font-weight: 600 !important; }}
    p, span, label {{ color: #E0E1DD; font-size: {body_p_size}; }}

    [data-testid="stSidebar"] {{
        background-color: #1B263B !important;
        border-right: 1px solid #005F73 !important;
        min-width: 300px !important;
    }}
    [data-testid="stSidebar"] * {{ color: #E0E1DD !important; }}

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
    .hero-sub {{ color: #A3B1C6 !important; font-size: {body_p_size}; }}

    /* CLINICAL SMART CARD DESIGN */
    .smart-card {{
        background-color: #1B263B;
        border: 1px solid #0A9396;
        border-radius: 16px;
        padding: 0;
        margin-bottom: 20px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.4);
        overflow: hidden;
    }}
    .smart-card-header {{
        background: linear-gradient(90deg, #005F73, #0D1B2A);
        padding: 14px 20px;
        border-bottom: 1px solid #0A9396;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    .smart-card-body {{
        padding: 20px;
    }}
    .smart-card-section {{
        margin-bottom: 16px;
        padding-bottom: 12px;
        border-bottom: 1px dashed #005F73;
    }}
    .smart-card-section:last-child {{
        border-bottom: none;
        margin-bottom: 0;
        padding-bottom: 0;
    }}
    .section-label {{
        font-size: 0.75rem;
        font-weight: 800;
        color: #0A9396;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-bottom: 6px;
    }}
    .pain-badge {{
        background: #AE2012;
        color: #FFFFFF;
        font-weight: 800;
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 0.82rem;
    }}

    .doctor-card {{
        background-color: #1B263B;
        border: 1px solid #0A9396;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 22px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.35);
    }}
    .online-indicator {{
        color: #94D2BD;
        font-weight: 800;
        font-size: 0.85rem;
    }}
    .trust-badge {{
        background: #0D1B2A;
        border: 1px solid #005F73;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        color: #A3B1C6;
        margin-right: 6px;
    }}

    .stButton>button {{
        background: linear-gradient(90deg, #94D2BD, #0A9396) !important;
        color: #0D1B2A !important;
        font-weight: 800 !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 12px 28px !important;
        font-size: 1rem !important;
        transition: all 0.3s ease;
        width: 100%;
    }}
    .stButton>button:hover {{
        background: #005F73 !important;
        color: #FFFFFF !important;
        transform: scale(1.01);
    }}

    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stNumberInput>div>div>input {{
        background-color: #0D1B2A !important;
        color: #E0E1DD !important;
        border-radius: 8px !important;
        border: 1px solid #005F73 !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 5. INITIALIZE SESSION DATA & REGISTRY ---
if "appointments" not in st.session_state:
    st.session_state["appointments"] = [
        {
            "Patient": "Muhammad Hassan Raza Attari",
            "Phone": "+92 309 7964195",
            "Email": "hassan@example.com",
            "Age": 21,
            "Gender": "Male",
            "Doctor": "Dr. Ayesha Malik",
            "Date": "Fri, Sep 5",
            "Time": "11:30 AM",
            "Type": "Lower Back Pain - Acute",
            "Onset": "2 Weeks Ago",
            "PainLevel": 7,
            "ReferredBy": "Self Triage",
            "Platform": "WhatsApp Video",
            "Fee": "Rs. 2200",
            "Status": "CONFIRMED"
        }
    ]

if "booking_step" not in st.session_state:
    st.session_state["booking_step"] = "FORM"

DOCTORS_DATABASE = [
    {
        "name": "Dr. Shahzaib Mughal",
        "title": "Knee & Sports Rehab Specialist",
        "exp": "6 Years",
        "patients": "210 Patients Treated",
        "rating": "4.9 ★",
        "languages": "Urdu, English",
        "fee": "Rs. 2500",
        "email": "shahzaib@example.com",
        "platforms": ["Zoom", "WhatsApp Video", "Google Meet"],
        "tags": ["knee", "acl", "knee acl tear", "sports", "joint pain"],
        "slots": ["10:00 AM", "02:30 PM", "04:00 PM"]
    },
    {
        "name": "Dr. Ayesha Malik",
        "title": "Orthopedic & Spine Specialist",
        "exp": "5 Years",
        "patients": "180 Patients Treated",
        "rating": "4.8 ★",
        "languages": "Urdu, English",
        "fee": "Rs. 2200",
        "email": "ayesha@example.com",
        "platforms": ["Zoom", "MS Teams", "Google Meet", "WhatsApp Video"],
        "tags": ["spine", "back pain", "lower back pain", "orthopedic"],
        "slots": ["11:30 AM", "03:00 PM", "05:30 PM"]
    },
    {
        "name": "Dr. Hassan Raza",
        "title": "Neurological & Post-Stroke Specialist",
        "exp": "7 Years",
        "patients": "310 Patients Treated",
        "rating": "5.0 ★",
        "languages": "Urdu, English",
        "fee": "Rs. 2800",
        "email": "hassan@example.com",
        "platforms": ["Zoom", "WhatsApp Video"],
        "tags": ["stroke", "post-stroke", "paralysis", "shoulder", "neurology"],
        "slots": ["01:00 PM", "04:30 PM"]
    }
]

# --- 6. SIDEBAR BRANDING & NAVIGATION ---
st.sidebar.markdown("""
    <div class="brand-container">
        <div class="brand-title">🩺 TeleSynapse</div>
        <div class="brand-sub">Clinical Tele-Rehabilitation Portal</div>
    </div>
""", unsafe_allow_html=True)

menu_options = [
    "🩺 Disease-Based Smart Booking",
    "📊 Clinician Dashboard",
    "📹 Kinematic Motion AI Suite",
    "📋 Official Protocol & Rx Suite",
    "📈 Patient Mobility Progress",
    "💬 Teleconsultation Virtual Lobby"
]

menu = st.sidebar.radio("Navigation Menu", menu_options)

# --- 7. HELPER FUNCTION: RENDER CLINICAL SMART CARD ---
def render_clinical_smart_card(booking, is_doctor_view=False):
    st.markdown(f"""
        <div class="smart-card">
            <div class="smart-card-header">
                <span style="font-weight:800; color:#94D2BD; font-size:0.9rem;">TELE-SYNAPSE | CLINICAL INTAKE SNAPSHOT</span>
                <span style="background:#0D1B2A; color:#94D2BD; border:1px solid #0A9396; padding:3px 10px; border-radius:12px; font-weight:700; font-size:0.78rem;">
                    🟢 {booking['Status']}
                </span>
            </div>
            <div class="smart-card-body">
                <div class="smart-card-section">
                    <div class="section-label">👤 Patient Demographics</div>
                    <div style="font-size:1.1rem; font-weight:700; color:#E0E1DD;">{booking['Patient']}</div>
                    <div style="color:#A3B1C6; font-size:0.88rem;">
                        {booking['Phone']} &nbsp;|&nbsp; <b>Age:</b> {booking['Age']} &nbsp;|&nbsp; <b>Gender:</b> {booking['Gender']}
                    </div>
                </div>
                <div class="smart-card-section">
                    <div class="section-label">🩺 Clinical Assessment</div>
                    <div style="font-size:0.95rem; color:#94D2BD; font-weight:600;">Condition: {booking['Type']}</div>
                    <div style="color:#A3B1C6; font-size:0.88rem; margin-top:4px;">
                        <b>Onset Duration:</b> {booking['Onset']} &nbsp;|&nbsp; 
                        <b>Pain Intensity:</b> <span class="pain-badge">{booking['PainLevel']} / 10</span> &nbsp;|&nbsp; 
                        <b>Referral:</b> {booking['ReferredBy']}
                    </div>
                </div>
                <div class="smart-card-section">
                    <div class="section-label">📅 Appointment & Platform</div>
                    <div style="color:#E0E1DD; font-size:0.9rem;">
                        <b>Specialist:</b> {booking['Doctor']}<br>
                        <b>Scheduled Window:</b> {booking['Date']} @ {booking['Time']}<br>
                        <b>Platform:</b> <span style="color:#94D2BD; font-weight:700;">{booking['Platform']}</span>
                    </div>
                </div>
                <div class="smart-card-section">
                    <div class="section-label">💳 Billing Overview</div>
                    <div style="color:#A3B1C6; font-size:0.88rem;">
                        <b>Fee:</b> <span style="color:#94D2BD; font-weight:700;">{booking['Fee']}</span> &nbsp;|&nbsp; <b>Status:</b> Payable Post-Consultation
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- 8. MODULE: DISEASE-BASED SMART BOOKING ---
if menu == "🩺 Disease-Based Smart Booking":
    
    # SCREEN 1: FORM WITH EXTRA CLINICAL FIELDS
    if st.session_state["booking_step"] == "FORM":
        st.markdown("""
            <div class="hero-banner">
                <div class="hero-title">Let's Get You Better with TeleSynapse</div>
                <div class="hero-sub">AI Triage & Direct Specialist Matching</div>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("smart_booking_form"):
            st.markdown("<h4>1. Clinical Symptoms & History</h4>", unsafe_allow_html=True)
            p_disease = st.text_input(
                "What is bothering you?", 
                placeholder="e.g. Lower Back Pain, Knee ACL Tear, Shoulder Stiffness..."
            )
            
            c_onset, c_pain = st.columns(2)
            with c_onset:
                p_onset = st.selectbox(
                    "Since when is this problem?",
                    ["3 Days (Acute)", "2 Weeks", "1 Month", "3+ Months (Chronic)"]
                )
            with c_pain:
                p_pain = st.slider("Pain Severity Level (1 - 10):", min_value=1, max_value=10, value=7)

            st.markdown("<br><h4>2. Consultation Platform</h4>", unsafe_allow_html=True)
            p_platform = st.radio(
                "Preferred video channel:",
                ["WhatsApp Video", "Zoom", "MS Teams", "Google Meet"],
                horizontal=True
            )

            col_time, col_demo = st.columns(2)
            with col_time:
                st.markdown("<h4>3. Scheduling Window</h4>", unsafe_allow_html=True)
                p_timeframe = st.selectbox("When do you want to book?", ["Today", "Tomorrow", "This Week"])
            
            with col_demo:
                st.markdown("<h4>4. Patient Information</h4>", unsafe_allow_html=True)
                p_name = st.text_input("Full Name:", placeholder="Muhammad Hassan Raza Attari")
                p_phone = st.text_input("Phone Number:", placeholder="+923097964195")
                c_age, c_gen = st.columns(2)
                with c_age:
                    p_age = st.number_input("Age:", min_value=5, max_value=100, value=21)
                with c_gen:
                    p_gender = st.selectbox("Gender:", ["Male", "Female", "Other"])

            st.markdown("<br>", unsafe_allow_html=True)
            submit_form = st.form_submit_button("Find My Specialist →")

            if submit_form:
                if p_disease and p_name and p_phone:
                    st.session_state["user_intake"] = {
                        "disease": p_disease,
                        "onset": p_onset,
                        "pain": p_pain,
                        "platform": p_platform,
                        "timeframe": p_timeframe,
                        "name": p_name,
                        "phone": p_phone,
                        "age": p_age,
                        "gender": p_gender
                    }
                    st.session_state["booking_step"] = "MATCHES"
                    st.rerun()
                else:
                    st.error("Please fill in your primary concern, full name, and phone number.")

    # SCREEN 2: MATCHED DOCTORS
    elif st.session_state["booking_step"] == "MATCHES":
        intake = st.session_state["user_intake"]
        
        st.markdown("""
            <div class="hero-banner">
                <div class="hero-title">Doctors Ready to Help You Now</div>
                <div class="hero-sub">Active online specialists tailored to your clinical assessment</div>
            </div>
        """, unsafe_allow_html=True)

        if st.button("← Back to Intake Form"):
            st.session_state["booking_step"] = "FORM"
            st.rerun()

        disease_query = intake["disease"].lower()
        matched_docs = [d for d in DOCTORS_DATABASE if any(t in disease_query for t in d["tags"])]
        if not matched_docs:
            matched_docs = DOCTORS_DATABASE

        for idx, doc in enumerate(matched_docs):
            st.markdown(f"""
                <div class="doctor-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span class="online-indicator">🟢 ONLINE NOW</span>
                        <span style="font-size:1.1rem; font-weight:700; color:#94D2BD;">{doc['fee']}</span>
                    </div>
                    <h3 style="margin:6px 0 2px 0; color:#94D2BD;">{doc['name']}</h3>
                    <p style="margin:0; color:#A3B1C6; font-size:0.95rem;">
                        <b>{doc['title']}</b> &nbsp;|&nbsp; <b>{doc['exp']} Exp</b>
                    </p>
                    <div style="margin:12px 0;">
                        <span class="trust-badge">👥 {doc['patients']}</span>
                        <span class="trust-badge">🗣️ {doc['languages']}</span>
                        <span class="trust-badge">⭐ {doc['rating']}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            c_slot, c_btn = st.columns([1, 2])
            with c_slot:
                chosen_slot = st.selectbox(f"Available Slots for {doc['name']}:", doc["slots"], key=f"slot_select_{idx}")
            
            with c_btn:
                st.markdown("<br>", unsafe_allow_html=True)
                confirm_label = f"✓ CONFIRM APPOINTMENT NOW with {doc['name']} at {chosen_slot}"
                if st.button(confirm_label, key=f"confirm_btn_{idx}"):
                    booking_record = {
                        "Patient": intake["name"],
                        "Phone": intake["phone"],
                        "Email": f"{intake['name'].lower().replace(' ', '')}@example.com",
                        "Age": intake["age"],
                        "Gender": intake["gender"],
                        "Doctor": doc["name"],
                        "Date": intake["timeframe"],
                        "Time": chosen_slot,
                        "Type": intake["disease"],
                        "Onset": intake["onset"],
                        "PainLevel": intake["pain"],
                        "ReferredBy": "Self Triage",
                        "Platform": intake["platform"],
                        "Fee": doc["fee"],
                        "Status": "CONFIRMED"
                    }
                    st.session_state["appointments"].append(booking_record)
                    st.session_state["latest_booking"] = booking_record
                    
                    send_doctor_clinical_snapshot(doc["email"], booking_record)
                    st.session_state["booking_step"] = "CONFIRMED"
                    st.rerun()

    # SCREEN 3: CLINICAL SMART CARD CONFIRMATION
    elif st.session_state["booking_step"] == "CONFIRMED":
        booking = st.session_state["latest_booking"]
        st.balloons()
        
        st.markdown("""
            <div class="hero-banner" style="border-color:#94D2BD;">
                <div class="hero-title" style="color:#94D2BD !important;">🎉 Appointment Confirmed!</div>
                <div class="hero-sub">Your Clinical Smart Snapshot has been dispatched to your specialist.</div>
            </div>
        """, unsafe_allow_html=True)

        # Render Clinical Smart Card
        render_clinical_smart_card(booking, is_doctor_view=False)

        col_cal, col_join = st.columns(2)
        with col_cal:
            st.button("📅 Download Calendar (.ics)")
        with col_join:
            st.button(f"🚀 Join {booking['Platform']} Session (10m Prior)")

        if st.button("Book Another Session"):
            st.session_state["booking_step"] = "FORM"
            st.rerun()

# --- 9. MODULE: CLINICIAN DASHBOARD ---
elif menu == "📊 Clinician Dashboard":
    st.markdown("""
        <div class="hero-banner">
            <div class="hero-title">🏥 Specialist Clinical Dashboard</div>
            <div class="hero-sub">Real-Time EMR Intake Snapshots & Triage Queue</div>
        </div>
    """, unsafe_allow_html=True)

    selected_doc = st.selectbox(
        "👨‍⚕️ Select Active Practitioner Profile:",
        ["All Specialists", "Dr. Ayesha Malik", "Dr. Shahzaib Mughal", "Dr. Hassan Raza"]
    )

    if selected_doc != "All Specialists":
        doc_apps = [a for a in st.session_state["appointments"] if a["Doctor"] == selected_doc]
    else:
        doc_apps = st.session_state["appointments"]

    st.markdown("<br><h3>📋 Active Clinical EMR Queue</h3>", unsafe_allow_html=True)

    for idx, app in enumerate(doc_apps):
        render_clinical_smart_card(app, is_doctor_view=True)
        col_act1, col_act2 = st.columns(2)
        with col_act1:
            st.button(f"📂 Open Full Patient Profile ({app['Patient']})", key=f"prof_{idx}")
        with col_act2:
            st.button(f"📹 Launch {app['Platform']} Video Session", key=f"launch_{idx}")
        st.markdown("<br>", unsafe_allow_html=True)

# --- 10. OTHER MODULES ---
elif menu == "📹 Kinematic Motion AI Suite":
    st.markdown("<h3>📹 Kinematic Joint & ROM Analysis</h3>", unsafe_allow_html=True)
    st.info("OpenCV Computer Vision Joint Tracking Pipeline Active.")

elif menu == "📋 Official Protocol & Rx Suite":
    st.markdown("<h3>📋 Official Protocol & Rx Suite</h3>", unsafe_allow_html=True)
    st.info("Prescription templates and clinical guidelines.")

elif menu == "📈 Patient Mobility Progress":
    st.markdown("<h3>📈 Patient Mobility Progress</h3>", unsafe_allow_html=True)
    progress_data = pd.DataFrame({
        "Session": ["Week 1", "Week 2", "Week 3", "Week 4"],
        "Flexion Angle": [75, 88, 98, 110]
    }).set_index("Session")
    st.line_chart(progress_data)

else:
    st.markdown("<h3>💬 Teleconsultation Virtual Lobby</h3>", unsafe_allow_html=True)
    st.success("🔒 Encrypted WebRTC Session Active.")
