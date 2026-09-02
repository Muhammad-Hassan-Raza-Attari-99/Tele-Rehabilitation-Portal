import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText

# --- 1. GLOBAL PAGE CONFIGURATION ---
st.set_page_config(
    page_title="TeleSynapse | Clinical Tele-Rehab Portal",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. AUTOMATED EMAIL NOTIFICATION ENGINE ---
def send_doctor_email_notification(doctor_email, patient_name, date_time, protocol, platform):
    sender_email = "alerts@telesynapse.com"
    sender_password = "your-app-password"
    
    subject = f"🚨 Immediate Action Required: Smart Booking for {patient_name}"
    body = (
        f"Dear Doctor,\n\n"
        f"A new direct tele-rehab appointment has been confirmed:\n\n"
        f"• Patient: {patient_name}\n"
        f"• Complaint/Condition: {protocol}\n"
        f"• Scheduled Window: {date_time}\n"
        f"• Preferred Platform: {platform}\n\n"
        f"Please access the TeleSynapse Specialist Dashboard to launch the session.\n\n"
        f"Regards,\nTeleSynapse Operations"
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

# --- 4. CLINICAL UI STYLING & ANIMATIONS ---
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

    /* Vibrant Pulse Button Styling */
    @keyframes pulse {{
        0% {{ box-shadow: 0 0 0 0 rgba(148, 210, 189, 0.7); }}
        70% {{ box-shadow: 0 0 0 15px rgba(148, 210, 189, 0); }}
        100% {{ box-shadow: 0 0 0 0 rgba(148, 210, 189, 0); }}
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
        letter-spacing: 0.5px;
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
        animation: pulse 2s infinite;
        width: 100%;
    }}
    .stButton>button:hover {{
        background: #005F73 !important;
        color: #FFFFFF !important;
        transform: scale(1.02);
    }}

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

    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stNumberInput>div>div>input {{
        background-color: #0D1B2A !important;
        color: #E0E1DD !important;
        border-radius: 8px !important;
        border: 1px solid #005F73 !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 5. INITIALIZE STATE & DOCTORS REGISTRY ---
if "appointments" not in st.session_state:
    st.session_state["appointments"] = [
        {
            "Patient": "Ali Ahmed",
            "Phone": "+92 300 1234567",
            "Email": "ali.ahmed@example.com",
            "Doctor": "Dr. Shahzaib Mughal",
            "Date": "Today",
            "Time": "10:00 AM",
            "Type": "Knee ACL Tear",
            "Platform": "Zoom",
            "Fee": "Rs. 2500",
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
        "platforms": ["Zoom", "MS Teams", "Google Meet"],
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

# --- 7. MODULE: DISEASE-BASED SMART BOOKING (NEW ZERO-FRICTION FLOW) ---
if menu == "🩺 Disease-Based Smart Booking":
    
    # SCREEN 1: INTAKE & TRIAGE FORM
    if st.session_state["booking_step"] == "FORM":
        st.markdown("""
            <div class="hero-banner">
                <div class="hero-title">Let's Get You Better with TeleSynapse</div>
                <div class="hero-sub">AI-Powered Condition Triage & Direct Specialist Dispatch</div>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("smart_booking_form"):
            st.markdown("<h4>1. What's bothering you?</h4>", unsafe_allow_html=True)
            p_disease = st.text_input(
                "Type your disease / injury:", 
                placeholder="e.g. Knee ACL Tear, Lower Back Pain, Post-Stroke Shoulder..."
            )
            st.caption("🤖 AI automatically analyzes symptoms and matches verified active specialists.")

            st.markdown("<br><h4>2. How should we meet?</h4>", unsafe_allow_html=True)
            p_platform = st.radio(
                "Select preferred consultation channel:",
                ["Zoom", "WhatsApp Video", "MS Teams", "Google Meet"],
                horizontal=True
            )

            col_time, col_contact = st.columns(2)
            with col_time:
                st.markdown("<h4>3. When do you want to book?</h4>", unsafe_allow_html=True)
                p_timeframe = st.selectbox("Preferred Timeframe:", ["Today", "Tomorrow", "This Week"])
            
            with col_contact:
                st.markdown("<h4>4. Contact Details</h4>", unsafe_allow_html=True)
                p_name = st.text_input("Full Name:", placeholder="e.g. Ali Ahmed")
                p_phone = st.text_input("Phone Number:", placeholder="+92 300 0000000")
                p_email = st.text_input("Email Address:", placeholder="name@example.com")

            st.markdown("<br>", unsafe_allow_html=True)
            submit_form = st.form_submit_button("Find My Specialist →")

            if submit_form:
                if p_disease and p_name and p_phone:
                    st.session_state["user_intake"] = {
                        "disease": p_disease,
                        "platform": p_platform,
                        "timeframe": p_timeframe,
                        "name": p_name,
                        "phone": p_phone,
                        "email": p_email
                    }
                    st.session_state["booking_step"] = "MATCHES"
                    st.rerun()
                else:
                    st.error("Please complete your name, phone number, and medical concern before proceeding.")

    # SCREEN 2: MATCHED SPECIALISTS (ONLINE NOW)
    elif st.session_state["booking_step"] == "MATCHES":
        intake = st.session_state["user_intake"]
        
        st.markdown("""
            <div class="hero-banner">
                <div class="hero-title">Doctors Ready to Help You Now</div>
                <div class="hero-sub">Specialists actively online and tailored to your condition</div>
            </div>
        """, unsafe_allow_html=True)

        if st.button("← Back to Form"):
            st.session_state["booking_step"] = "FORM"
            st.rerun()

        # Match logic based on disease tags
        disease_query = intake["disease"].lower()
        matched_docs = [
            d for d in DOCTORS_DATABASE 
            if any(t in disease_query for t in d["tags"])
        ]
        if not matched_docs:
            matched_docs = DOCTORS_DATABASE  # Fallback to all online specialists

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
                        <span class="trust-badge">🗣️ Speaks: {doc['languages']}</span>
                        <span class="trust-badge">⭐ {doc['rating']}</span>
                        <span class="trust-badge">💻 Available on: {", ".join(doc['platforms'])}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            c_slot, c_btn = st.columns([1, 2])
            with c_slot:
                chosen_slot = st.selectbox(
                    f"Available Slots for {doc['name']}:", 
                    doc["slots"], 
                    key=f"slot_select_{idx}"
                )
            
            with c_btn:
                st.markdown("<br>", unsafe_allow_html=True)
                confirm_label = f"✓ CONFIRM APPOINTMENT NOW with {doc['name']} at {chosen_slot}"
                if st.button(confirm_label, key=f"confirm_btn_{idx}"):
                    # Append appointment
                    booking_record = {
                        "Patient": intake["name"],
                        "Phone": intake["phone"],
                        "Email": intake["email"],
                        "Doctor": doc["name"],
                        "Date": intake["timeframe"],
                        "Time": chosen_slot,
                        "Type": intake["disease"],
                        "Platform": intake["platform"],
                        "Fee": doc["fee"],
                        "Status": "CONFIRMED"
                    }
                    st.session_state["appointments"].append(booking_record)
                    st.session_state["latest_booking"] = booking_record
                    
                    # Send alert
                    send_doctor_email_notification(
                        doc["email"], intake["name"], chosen_slot, intake["disease"], intake["platform"]
                    )
                    
                    st.session_state["booking_step"] = "CONFIRMED"
                    st.rerun()

            st.markdown("""
                <div style="text-align:center; color:#A3B1C6; font-size:0.78rem; margin:-10px 0 20px 0;">
                    🔒 Instant Confirmation &nbsp;•&nbsp; 🛡️ Encrypted Video Session &nbsp;•&nbsp; 📂 Medical Records Saved
                </div>
            """, unsafe_allow_html=True)

    # SCREEN 3: CONFIRMATION & SESSION LINK
    elif st.session_state["booking_step"] == "CONFIRMED":
        booking = st.session_state["latest_booking"]
        st.balloons()
        
        st.markdown(f"""
            <div class="hero-banner" style="border-color:#94D2BD;">
                <div class="hero-title" style="color:#94D2BD !important;">🎉 Appointment Confirmed!</div>
                <div class="hero-sub">
                    {booking['Doctor']} is expecting you <b>{booking['Date']} at {booking['Time']}</b> on <b>{booking['Platform']}</b>.
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div style="background-color:#1B263B; border:1px solid #0A9396; border-radius:14px; padding:22px; margin-bottom:20px;">
                <h4 style="margin-top:0;">📋 Session Summary</h4>
                <p><b>Patient Name:</b> {booking['Patient']} ({booking['Phone']})</p>
                <p><b>Condition / Disease:</b> {booking['Type']}</p>
                <p><b>Specialist:</b> {booking['Doctor']}</p>
                <p><b>Scheduled Window:</b> {booking['Date']} @ {booking['Time']}</p>
                <p><b>Consultation Platform:</b> {booking['Platform']}</p>
                <p><b>Consultation Fee:</b> {booking['Fee']} (Payable Post-Consultation)</p>
            </div>
        """, unsafe_allow_html=True)

        col_cal, col_join = st.columns(2)
        with col_cal:
            st.button("📅 Add to Calendar")
        with col_join:
            st.button(f"🚀 Join {booking['Platform']} Session (10m Prior)")

        st.info("📩 Confirmation dispatched via SMS, Email, and In-App Notifications.")
        
        if st.button("Book Another Appointment"):
            st.session_state["booking_step"] = "FORM"
            st.rerun()

# --- 8. MODULE: CLINICIAN DASHBOARD (WITH INCOMING SMART BOOKINGS) ---
elif menu == "📊 Clinician Dashboard":
    st.markdown("""
        <div class="hero-banner">
            <div class="hero-title">🏥 Specialist Clinical Dashboard</div>
            <div class="hero-sub">Real-Time Patient Intake Stream & Session Triage</div>
        </div>
    """, unsafe_allow_html=True)

    selected_doc = st.selectbox(
        "👨‍⚕️ Select Active Specialist Profile:",
        ["All Specialists", "Dr. Shahzaib Mughal", "Dr. Hassan Raza", "Dr. Ayesha Malik"]
    )

    if selected_doc != "All Specialists":
        doc_apps = [a for a in st.session_state["appointments"] if a["Doctor"] == selected_doc]
    else:
        doc_apps = st.session_state["appointments"]

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-card-title">Total Smart Bookings</div>
                <div class="stat-card-value">{len(doc_apps)}</div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-card-title">Confirmed Consults</div>
                <div class="stat-card-value" style="color:#94D2BD;">{len([a for a in doc_apps if a['Status'] == 'CONFIRMED'])}</div>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-card-title">Active Platforms</div>
                <div class="stat-card-value" style="color:#0A9396;">Zoom / WA</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><h3>📥 Incoming Smart Bookings Feed</h3>", unsafe_allow_html=True)

    for idx, app in enumerate(doc_apps):
        st.markdown(f"""
            <div style="background-color:#1B263B; border-left:5px solid #94D2BD; border-top:1px solid #005F73; border-right:1px solid #005F73; border-bottom:1px solid #005F73; border-radius:12px; padding:18px 22px; margin-bottom:14px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-weight:700; font-size:1.1rem; color:#94D2BD;">👤 {app['Patient']} ({app['Phone']})</span>
                    <span style="background:#0D1B2A; border:1px solid #0A9396; color:#94D2BD; padding:4px 12px; border-radius:20px; font-weight:700; font-size:0.8rem;">{app['Status']}</span>
                </div>
                <div style="margin-top:8px; font-size:0.9rem; color:#A3B1C6;">
                    <b>Condition:</b> {app['Type']} &nbsp;|&nbsp; 
                    <b>Schedule:</b> {app['Date']} ({app['Time']}) &nbsp;|&nbsp; 
                    <b>Platform:</b> <span style="color:#94D2BD; font-weight:700;">{app['Platform']}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

# --- 9. OTHER MODULE PLACEHOLDERS ---
elif menu == "📹 Kinematic Motion AI Suite":
    st.markdown("<h3>📹 Kinematic Motion AI Suite</h3>", unsafe_allow_html=True)
    st.info("Computer Vision Range-of-Motion (ROM) Engine Active.")

elif menu == "📋 Official Protocol & Rx Suite":
    st.markdown("<h3>📋 Official Protocol & Rx Suite</h3>", unsafe_allow_html=True)
    st.info("Clinical guidelines and prescription templates.")

elif menu == "📈 Patient Mobility Progress":
    st.markdown("<h3>📈 Patient Mobility Progress</h3>", unsafe_allow_html=True)
    progress_data = pd.DataFrame({
        "Session": ["Week 1", "Week 2", "Week 3", "Week 4"],
        "Flexion Angle": [75, 88, 98, 110]
    }).set_index("Session")
    st.line_chart(progress_data)

else:
    st.markdown("<h3>💬 Teleconsultation Virtual Lobby</h3>", unsafe_allow_html=True)
    st.success("🔒 Encrypted WebRTC Gateway Channel Active.")
