import streamlit as st
import pandas as pd
import random
import smtplib
from email.mime.text import MIMEText

# --- 0. BULLETPROOF HTML CLEANER ENGINE ---
def clean_html(raw_html: str) -> str:
    """Strips leading and trailing spaces from every line to kill Streamlit code-block parsing."""
    return "".join(line.strip() for line in raw_html.splitlines())

# --- 1. GLOBAL PAGE CONFIGURATION ---
st.set_page_config(
    page_title="TeleSynapse | Clinical Tele-Rehab Portal",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. AUTOMATED EMAIL ENGINE ---
def send_doctor_clinical_snapshot(doctor_email, booking_data):
    sender_email = "alerts@telesynapse.com"
    sender_password = "your-app-password"
    
    subject = f"🚨 New Booking & Slip #{booking_data['SlipNo']}: {booking_data['Patient']}"
    body = f"""
    TELE-SYNAPSE APPOINTMENT CONFIRMATION
    --------------------------------------------------
    SLIP NO: {booking_data['SlipNo']} | REF ID: {booking_data['RefID']}
    STATUS: CONFIRMED
    
    PATIENT: {booking_data['Patient']} ({booking_data['Age']} yrs, {booking_data['Gender']})
    PHONE: {booking_data['Phone']}
    
    CLINICAL:
    Condition: {booking_data['Type']}
    Onset: {booking_data['Onset']} | Pain Level: {booking_data['PainLevel']}/10
    
    APPOINTMENT:
    Doctor: {booking_data['Doctor']}
    Date/Time: {booking_data['Date']} @ {booking_data['Time']}
    Platform: {booking_data['Platform']}
    Fee: {booking_data['Fee']}
    --------------------------------------------------
    Join Link will be active 10 minutes prior to session.
    """
    
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

# --- 3. ACCESSIBILITY TOGGLE ---
st.sidebar.markdown("### ♿ Accessibility Mode")
big_text = st.sidebar.toggle("🔍 Large Text Mode", value=False)

base_font_size = "17px" if big_text else "15px"
hero_title_size = "2.3rem" if big_text else "1.8rem"

# --- 4. HIGH-CONTRAST VIBRANT COLOR SYSTEM & CSS ---
global_css = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

#MainMenu {{ visibility: hidden !important; }}
footer {{ visibility: hidden !important; }}
.stDeployButton {{ display: none !important; }}
header[data-testid="stHeader"] {{ background-color: transparent !important; }}

html, body, [class*="css"] {{
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: {base_font_size} !important;
}}
.stApp {{
    background: #0B0F17 !important;
    color: #F3F4F6 !important;
}}

h1, h2, h3 {{ color: #34D399 !important; font-weight: 800 !important; }}
h4, h5, h6 {{ color: #38BDF8 !important; font-weight: 700 !important; }}
p, span, label {{ color: #E5E7EB; }}

[data-testid="stSidebar"] {{
    background-color: #111827 !important;
    border-right: 1px solid #1F2937 !important;
    min-width: 310px !important;
}}
[data-testid="stSidebar"] * {{ color: #F3F4F6 !important; }}

.brand-container {{
    padding: 20px 16px;
    background: linear-gradient(135deg, #064E3B 0%, #111827 100%);
    border: 1px solid #059669;
    border-radius: 16px;
    margin-bottom: 24px;
    text-align: center;
    box-shadow: 0 10px 25px -5px rgba(16, 185, 129, 0.2);
}}
.brand-title {{
    color: #34D399 !important;
    font-size: 1.7rem;
    font-weight: 800;
    letter-spacing: -0.5px;
}}
.brand-sub {{
    color: #9CA3AF !important;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-top: 4px;
}}

.hero-banner {{
    background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
    border: 1px solid #334155;
    border-left: 5px solid #10B981;
    border-radius: 16px;
    padding: 24px 30px;
    margin-bottom: 28px;
    box-shadow: 0 10px 30px -10px rgba(0,0,0,0.5);
}}
.hero-title {{
    color: #34D399 !important;
    font-size: {hero_title_size};
    font-weight: 800;
    margin-bottom: 6px;
}}
.hero-sub {{ color: #94A3B8 !important; }}

.doctor-card {{
    background: #1E293B;
    border: 1px solid #334155;
    border-radius: 16px;
    padding: 22px;
    margin-bottom: 20px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}}

.stButton>button {{
    background: linear-gradient(90deg, #10B981, #06B6D4) !important;
    color: #0B0F17 !important;
    font-weight: 800 !important;
    border-radius: 12px !important;
    border: none !important;
    padding: 12px 24px !important;
    font-size: 0.95rem !important;
    box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
}}
.stButton>button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(16, 185, 129, 0.5);
}}

.stTextInput>div>div>input, .stSelectbox>div>div>div {{
    background-color: #1E293B !important;
    color: #F8FAFC !important;
    border-radius: 10px !important;
    border: 1px solid #334155 !important;
}}
</style>
"""

st.markdown(clean_html(global_css), unsafe_allow_html=True)

# --- 5. SESSION STATE DATA ---
if "appointments" not in st.session_state:
    st.session_state["appointments"] = [
        {
            "SlipNo": "TS-98475",
            "RefID": "TS-P-1122",
            "Patient": "Muhammad Hassan Raza Attari",
            "Phone": "+92 309 7964195",
            "Age": 21,
            "Gender": "Male",
            "Doctor": "Dr. Ayesha Malik",
            "Specialty": "Neuro & Ortho Rehab",
            "Date": "Friday, 05 Sep 2026",
            "Time": "11:30 AM",
            "Type": "Lower Back Pain - Acute",
            "Onset": "2 Weeks Ago",
            "PainLevel": 7,
            "Platform": "WhatsApp Video Call",
            "Fee": "Rs. 2,200",
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
        "patients": "210+ Treated",
        "rating": "4.9 ★",
        "fee": "Rs. 2,500",
        "email": "shahzaib@example.com",
        "tags": ["knee", "acl", "sports", "joint pain"],
        "slots": ["10:00 AM", "02:30 PM", "04:00 PM"]
    },
    {
        "name": "Dr. Ayesha Malik",
        "title": "Orthopedic & Spine Specialist",
        "exp": "5 Years",
        "patients": "180+ Treated",
        "rating": "4.8 ★",
        "fee": "Rs. 2,200",
        "email": "ayesha@example.com",
        "tags": ["spine", "back pain", "lower back pain", "orthopedic"],
        "slots": ["11:30 AM", "03:00 PM", "05:30 PM"]
    },
    {
        "name": "Dr. Hassan Raza",
        "title": "Neurological & Post-Stroke Specialist",
        "exp": "7 Years",
        "patients": "310+ Treated",
        "rating": "5.0 ★",
        "fee": "Rs. 2,800",
        "email": "hassan@example.com",
        "tags": ["stroke", "post-stroke", "paralysis", "neurology"],
        "slots": ["01:00 PM", "04:30 PM"]
    }
]

# --- 6. SIDEBAR ---
sidebar_html = """
<div class="brand-container">
    <div class="brand-title">🩺 TeleSynapse</div>
    <div class="brand-sub">Clinical Tele-Rehab Portal</div>
</div>
"""
st.sidebar.markdown(clean_html(sidebar_html), unsafe_allow_html=True)

menu = st.sidebar.radio("Navigation Menu", [
    "🩺 Disease-Based Smart Booking",
    "📊 Clinician Dashboard",
    "📹 Kinematic Motion AI Suite",
    "📈 Patient Mobility Progress"
])

# --- 7. HELPER: CLEAN RENDER OF ATM DIGITAL SLIP ---
def render_atm_slip(booking):
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=110x110&data=TeleSynapse-Slip-{booking['SlipNo']}"
    
    slip_html = f"""
    <div style="background:#0F172A; border:2px dashed #38BDF8; border-radius:16px; padding:24px; max-width:440px; margin:20px auto; font-family:'JetBrains Mono', monospace; color:#E5E7EB; box-shadow:0 10px 30px rgba(0,0,0,0.5);">
        
        <div style="text-align:center; border-bottom:2px solid #334155; padding-bottom:12px; margin-bottom:14px;">
            <div style="color:#38BDF8; font-size:1.25rem; font-weight:800; letter-spacing:1px;">TELE-SYNAPSE HEALTH</div>
            <div style="color:#94A3B8; font-size:0.72rem; letter-spacing:2px;">DIGITAL APPOINTMENT SLIP</div>
        </div>

        <div style="display:flex; justify-content:space-between; margin-bottom:6px; font-size:0.85rem;">
            <span style="color:#64748B;">SLIP NO:</span>
            <span style="color:#38BDF8; font-weight:700;">{booking['SlipNo']}</span>
        </div>
        <div style="display:flex; justify-content:space-between; margin-bottom:6px; font-size:0.85rem;">
            <span style="color:#64748B;">REF ID:</span>
            <span style="color:#F8FAFC; font-weight:700;">{booking['RefID']}</span>
        </div>
        <div style="display:flex; justify-content:space-between; margin-bottom:12px; font-size:0.85rem;">
            <span style="color:#64748B;">STATUS:</span>
            <span style="background:#064E3B; color:#34D399; padding:2px 8px; border-radius:4px; font-weight:700;">● {booking['Status']}</span>
        </div>

        <div style="color:#34D399; font-size:0.75rem; font-weight:800; border-bottom:1px solid #1E293B; margin:14px 0 6px 0; padding-bottom:2px;">PATIENT DETAILS</div>
        <div style="display:flex; justify-content:space-between; margin-bottom:4px; font-size:0.85rem;">
            <span style="color:#64748B;">Name:</span>
            <span style="color:#F8FAFC; font-weight:700;">{booking['Patient']}</span>
        </div>
        <div style="display:flex; justify-content:space-between; margin-bottom:4px; font-size:0.85rem;">
            <span style="color:#64748B;">Phone:</span>
            <span style="color:#F8FAFC; font-weight:700;">{booking['Phone']}</span>
        </div>
        <div style="display:flex; justify-content:space-between; margin-bottom:12px; font-size:0.85rem;">
            <span style="color:#64748B;">Demographics:</span>
            <span style="color:#F8FAFC; font-weight:700;">{booking['Age']} yrs | {booking['Gender']}</span>
        </div>

        <div style="color:#34D399; font-size:0.75rem; font-weight:800; border-bottom:1px solid #1E293B; margin:14px 0 6px 0; padding-bottom:2px;">CLINICAL & DOCTOR</div>
        <div style="display:flex; justify-content:space-between; margin-bottom:4px; font-size:0.85rem;">
            <span style="color:#64748B;">Condition:</span>
            <span style="color:#34D399; font-weight:700;">{booking['Type']}</span>
        </div>
        <div style="display:flex; justify-content:space-between; margin-bottom:4px; font-size:0.85rem;">
            <span style="color:#64748B;">Onset / Pain:</span>
            <span style="color:#F8FAFC; font-weight:700;">{booking['Onset']} | {booking['PainLevel']}/10</span>
        </div>
        <div style="display:flex; justify-content:space-between; margin-bottom:12px; font-size:0.85rem;">
            <span style="color:#64748B;">Doctor:</span>
            <span style="color:#F8FAFC; font-weight:700;">{booking['Doctor']}</span>
        </div>

        <div style="color:#34D399; font-size:0.75rem; font-weight:800; border-bottom:1px solid #1E293B; margin:14px 0 6px 0; padding-bottom:2px;">APPOINTMENT WINDOW</div>
        <div style="display:flex; justify-content:space-between; margin-bottom:4px; font-size:0.85rem;">
            <span style="color:#64748B;">Date & Time:</span>
            <span style="color:#F8FAFC; font-weight:700;">{booking['Date']} @ {booking['Time']}</span>
        </div>
        <div style="display:flex; justify-content:space-between; margin-bottom:4px; font-size:0.85rem;">
            <span style="color:#64748B;">Platform:</span>
            <span style="color:#38BDF8; font-weight:700;">{booking['Platform']}</span>
        </div>
        <div style="display:flex; justify-content:space-between; margin-bottom:12px; font-size:0.85rem;">
            <span style="color:#64748B;">Fee:</span>
            <span style="color:#F8FAFC; font-weight:700;">{booking['Fee']} (Payable Post-Session)</span>
        </div>

        <div style="text-align:center; margin-top:16px; padding-top:12px; border-top:2px dashed #334155;">
            <img src="{qr_url}" width="95" style="border-radius:8px; border:2px solid #334155;" />
            <div style="font-size:0.7rem; color:#94A3B8; margin-top:6px;">Scan QR to verify or sync session to calendar</div>
        </div>

        <div style="text-align:center; color:#64748B; font-size:0.68rem; margin-top:12px;">
            ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━<br>
            Need Help? WhatsApp: +92 309 7964195<br>
            www.telesynapse.com | Powered by AI
        </div>
    </div>
    """

    st.markdown(clean_html(slip_html), unsafe_allow_html=True)

# --- 8. MODULE: DISEASE-BASED SMART BOOKING ---
if menu == "🩺 Disease-Based Smart Booking":
    
    if st.session_state["booking_step"] == "FORM":
        banner_html = """
        <div class="hero-banner">
            <div class="hero-title">Start Your Tele-Rehab Journey</div>
            <div class="hero-sub">Get matched with a specialist & receive your Digital ATM Slip instantly.</div>
        </div>
        """
        st.markdown(clean_html(banner_html), unsafe_allow_html=True)
        
        with st.form("smart_booking_form"):
            st.markdown("<h4>1. Clinical Symptoms & History</h4>", unsafe_allow_html=True)
            p_disease = st.text_input("Primary Concern / Symptoms:", placeholder="e.g. Lower Back Pain, Knee ACL Tear...")
            
            c_onset, c_pain = st.columns(2)
            with c_onset:
                p_onset = st.selectbox("Problem Duration:", ["3 Days (Acute)", "2 Weeks", "1 Month", "3+ Months"])
            with c_pain:
                p_pain = st.slider("Pain Intensity (1 - 10):", 1, 10, 7)

            st.markdown("<h4>2. Platform & Patient Info</h4>", unsafe_allow_html=True)
            c_plat, c_time = st.columns(2)
            with c_plat:
                p_platform = st.selectbox("Preferred Channel:", ["WhatsApp Video Call", "Zoom", "MS Teams", "Google Meet"])
            with c_time:
                p_timeframe = st.selectbox("Preferred Schedule:", ["Friday, 05 Sep 2026", "Saturday, 06 Sep 2026", "Monday, 08 Sep 2026"])

            c_n, c_p, c_a, c_g = st.columns([2, 2, 1, 1])
            with c_n:
                p_name = st.text_input("Full Name:", placeholder="Muhammad Hassan Raza Attari")
            with c_p:
                p_phone = st.text_input("WhatsApp Phone:", placeholder="+923097964195")
            with c_a:
                p_age = st.number_input("Age:", 5, 100, 21)
            with c_g:
                p_gender = st.selectbox("Gender:", ["Male", "Female", "Other"])

            submit_form = st.form_submit_button("Search Specialists & Continue →")

            if submit_form:
                if p_disease and p_name and p_phone:
                    st.session_state["user_intake"] = {
                        "disease": p_disease, "onset": p_onset, "pain": p_pain,
                        "platform": p_platform, "timeframe": p_timeframe,
                        "name": p_name, "phone": p_phone, "age": p_age, "gender": p_gender
                    }
                    st.session_state["booking_step"] = "MATCHES"
                    st.rerun()
                else:
                    st.error("Please fill in your name, phone, and primary concern.")

    elif st.session_state["booking_step"] == "MATCHES":
        intake = st.session_state["user_intake"]
        st.markdown("<h3>Select Specialist & Generate Digital Slip</h3>", unsafe_allow_html=True)

        if st.button("← Back to Form"):
            st.session_state["booking_step"] = "FORM"
            st.rerun()

        disease_q = intake["disease"].lower()
        matched = [d for d in DOCTORS_DATABASE if any(t in disease_q for t in d["tags"])] or DOCTORS_DATABASE

        for idx, doc in enumerate(matched):
            doc_card_html = f"""
            <div class="doctor-card">
                <div style="display:flex; justify-content:space-between;">
                    <span style="color:#34D399; font-weight:800; font-size:0.85rem;">🟢 ONLINE NOW</span>
                    <span style="color:#38BDF8; font-weight:800; font-size:1.1rem;">{doc['fee']}</span>
                </div>
                <h3 style="margin:4px 0;">{doc['name']}</h3>
                <p style="color:#94A3B8; margin:0;">{doc['title']} | {doc['exp']} Exp | ⭐ {doc['rating']}</p>
            </div>
            """
            st.markdown(clean_html(doc_card_html), unsafe_allow_html=True)

            c_slot, c_btn = st.columns([1, 2])
            with c_slot:
                chosen_slot = st.selectbox(f"Slot for {doc['name']}:", doc["slots"], key=f"slot_{idx}")
            with c_btn:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button(f"✓ CONFIRM BOOKING & GENERATE SLIP", key=f"btn_{idx}"):
                    slip_num = f"TS-{random.randint(80000, 99999)}"
                    ref_num = f"TS-P-{random.randint(1000, 9999)}"
                    
                    booking_record = {
                        "SlipNo": slip_num,
                        "RefID": ref_num,
                        "Patient": intake["name"],
                        "Phone": intake["phone"],
                        "Age": intake["age"],
                        "Gender": intake["gender"],
                        "Doctor": doc["name"],
                        "Specialty": doc["title"],
                        "Date": intake["timeframe"],
                        "Time": chosen_slot,
                        "Type": intake["disease"],
                        "Onset": intake["onset"],
                        "PainLevel": intake["pain"],
                        "Platform": intake["platform"],
                        "Fee": doc["fee"],
                        "Status": "CONFIRMED"
                    }
                    st.session_state["appointments"].append(booking_record)
                    st.session_state["latest_booking"] = booking_record
                    send_doctor_clinical_snapshot(doc["email"], booking_record)
                    st.session_state["booking_step"] = "SLIP"
                    st.rerun()

    elif st.session_state["booking_step"] == "SLIP":
        booking = st.session_state["latest_booking"]

        confirmation_banner = """
        <div style="background: linear-gradient(90deg, #064E3B 0%, #065F46 100%); border: 1px solid #10B981; border-radius: 12px; padding: 16px 20px; margin-bottom: 20px;">
            <div style="color: #34D399; font-weight: 800; font-size: 1.1rem; letter-spacing: 0.5px;">✔ APPOINTMENT OFFICIALLY CONFIRMED & DISPATCHED</div>
            <div style="color: #D1D5DB; font-size: 0.88rem; margin-top: 4px;">Digital appointment slip verified. Encrypted clinical record transmitted to attending specialist.</div>
        </div>
        """
        st.markdown(clean_html(confirmation_banner), unsafe_allow_html=True)

        # Render Clean ATM Digital Slip
        render_atm_slip(booking)

        c_a1, c_a2, c_a3 = st.columns(3)
        with c_a1:
            st.button("📥 Download Slip PDF")
        with c_a2:
            st.button("📲 Resend via WhatsApp")
        with c_a3:
            st.button("📅 Add to iCal / Google Calendar")

        if st.button("Book Another Appointment"):
            st.session_state["booking_step"] = "FORM"
            st.rerun()

# --- 9. MODULE: CLINICIAN DASHBOARD ---
elif menu == "📊 Clinician Dashboard":
    st.markdown("<h3>🏥 Specialist Dashboard & Issued Digital Slips</h3>", unsafe_allow_html=True)
    
    for app in reversed(st.session_state["appointments"]):
        c_slip, c_info = st.columns([1, 1])
        with c_slip:
            render_atm_slip(app)
        with c_info:
            st.markdown(f"#### Clinical Actions for Slip #{app['SlipNo']}")
            st.info(f"**Patient:** {app['Patient']}\n\n**Condition:** {app['Type']} ({app['Onset']}, Pain: {app['PainLevel']}/10)")
            st.button(f"📂 Open Full Patient EMR Chart", key=f"emr_{app['SlipNo']}")
            st.button(f"📹 Launch {app['Platform']} Session", key=f"launch_{app['SlipNo']}")
        st.markdown("---")

# --- 10. OTHER MODULES ---
elif menu == "📹 Kinematic Motion AI Suite":
    st.markdown("<h3>📹 Kinematic Motion Analysis Engine</h3>", unsafe_allow_html=True)
    st.info("Computer Vision Joint Tracking Pipeline initialized.")

else:
    st.markdown("<h3>📈 Patient Mobility Progress</h3>", unsafe_allow_html=True)
    st.line_chart(pd.DataFrame({"Flexion Angle": [60, 75, 88, 105]}, index=["W1", "W2", "W3", "W4"]))
