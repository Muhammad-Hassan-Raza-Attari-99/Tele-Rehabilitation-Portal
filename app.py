import streamlit as st
import pandas as pd
import random
import datetime
import smtplib
import base64
import time
from email.mime.text import MIMEText

# --- 0. BULLETPROOF HTML CLEANER ENGINE ---
def clean_html(raw_html: str) -> str:
    """Strips leading/trailing spaces to prevent Streamlit code-block parsing bugs."""
    return "".join(line.strip() for line in raw_html.splitlines())

# --- 1. GLOBAL PAGE CONFIGURATION ---
st.set_page_config(
    page_title="TeleSynapse | Strict Verification Tele-Rehab Portal",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. AUTOMATED EMAIL ENGINE ---
def send_doctor_clinical_snapshot(doctor_email, booking_data):
    sender_email = "alerts@telesynapse.com"
    sender_password = "your-app-password"
    
    subject = f"🚨 Payment Verified & Slip Generated #{booking_data['SlipNo']}: {booking_data['Patient']}"
    body = f"""
    TELE-SYNAPSE APPOINTMENT CONFIRMATION (PAID)
    --------------------------------------------------
    SLIP NO: {booking_data['SlipNo']} | REF ID: {booking_data['RefID']}
    STATUS: {booking_data['Status']}
    VERIFIED BY: {booking_data.get('VerifiedBy', 'Admin')} @ {booking_data.get('VerifiedAt', 'N/A')}
    
    PATIENT: {booking_data['Patient']} ({booking_data['Age']} yrs, {booking_data['Gender']})
    PHONE: {booking_data['Phone']} | EMAIL: {booking_data.get('Email', 'N/A')}
    
    CLINICAL DETAILS:
    Condition: {booking_data['Type']}
    Onset: {booking_data['Onset']} | Pain Level: {booking_data['PainLevel']}/10
    
    APPOINTMENT SCHEDULE:
    Doctor: {booking_data['Doctor']}
    Date/Time: {booking_data['Date']} @ {booking_data['Time']}
    Platform: {booking_data['Platform']}
    Fee Paid: {booking_data['Fee']}
    --------------------------------------------------
    Join Link: https://meet.jit.si/TeleSynapse-{booking_data['SlipNo']}
    (Link active 10 mins prior to session)
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

# --- 4. HIGH-CONTRAST COLOR SYSTEM & GLOBAL CSS ---
global_css = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

#MainMenu {{ visibility: hidden !important; }}
footer {{ visibility: hidden !important; }}
.stDeployButton {{ display: none !important; }}
header[data-testid="stHeader"] {{ background-color: transparent !important; }}
div[data-testid="stStatusWidget"] {{ display: none !important; }}

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

.pay-card {{
    background: #1E293B;
    border: 1px solid #334155;
    border-radius: 14px;
    padding: 16px;
    margin-bottom: 12px;
}}
.pay-title {{
    color: #38BDF8;
    font-weight: 700;
    font-size: 0.9rem;
    margin-bottom: 4px;
}}
.pay-val {{
    font-family: 'JetBrains Mono', monospace;
    color: #F8FAFC;
    font-size: 1.1rem;
    font-weight: 700;
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
    width: 100%;
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

.stat-card {{
    background: #1E293B;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 14px;
    text-align: center;
}}
.stat-val {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.8rem;
    font-weight: 800;
    color: #34D399;
}}
.stat-lbl {{
    font-size: 0.75rem;
    color: #94A3B8;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 700;
}}
</style>
"""

st.markdown(clean_html(global_css), unsafe_allow_html=True)

# --- 5. INITIALIZE SESSION STATE ---
if "appointments" not in st.session_state:
    st.session_state["appointments"] = [
        {
            "SlipNo": "TS-98475",
            "RefID": "TS-P-1122",
            "Patient": "Muhammad Hassan Raza",
            "Phone": "+92 309 7964195",
            "Email": "hassan@example.com",
            "Age": 21,
            "Gender": "Male",
            "Doctor": "Dr. Ayesha Malik",
            "Specialty": "Orthopedic & Spine Specialist",
            "Date": "Fri, 05 Sep 2026",
            "Time": "11:30 AM",
            "Type": "Lower Back Pain - Acute",
            "Onset": "2 Weeks Ago",
            "PainLevel": 7,
            "Platform": "WhatsApp Video",
            "Fee": "Rs. 2,200",
            "Status": "PAID ✓",
            "VerifiedBy": "Dr. Ayesha Malik (Verified)",
            "VerifiedAt": "02-Sep-2026 02:14 PM",
            "Proof": "Payment_Proof_Hassan.png",
            "RejectReason": None
        }
    ]

if "booking_step" not in st.session_state:
    st.session_state["booking_step"] = "STEP_1_BOOK"

if "show_proof_error" not in st.session_state:
    st.session_state["show_proof_error"] = False

if "ghost_mode" not in st.session_state:
    st.session_state["ghost_mode"] = True

if "ai_session_running" not in st.session_state:
    st.session_state["ai_session_running"] = True

if "current_reps" not in st.session_state:
    st.session_state["current_reps"] = 3

DOCTORS_DATABASE = [
    {
        "name": "Dr. Ayesha Malik",
        "title": "Orthopedic & Spine Specialist",
        "exp": "5 Years",
        "patients": "180+ Treated",
        "rating": "4.8 ★",
        "fee": "Rs. 2,200",
        "email": "ayesha@example.com",
        "jazzcash": "0309-7964195",
        "easypaisa": "0309-7964195",
        "bank": "HBL A/C: 00427901234503 (Title: Dr Ayesha Malik)",
        "tags": ["spine", "back pain", "lower back pain", "orthopedic"],
        "slots": ["11:30 AM", "03:00 PM", "05:30 PM"]
    },
    {
        "name": "Dr. Shahzaib Mughal",
        "title": "Knee & Sports Rehab Specialist",
        "exp": "6 Years",
        "patients": "210+ Treated",
        "rating": "4.9 ★",
        "fee": "Rs. 2,500",
        "email": "shahzaib@example.com",
        "jazzcash": "0301-8889911",
        "easypaisa": "0301-8889911",
        "bank": "Meezan Bank A/C: 0201010998877 (Title: Dr Shahzaib)",
        "tags": ["knee", "acl", "sports", "joint pain"],
        "slots": ["10:00 AM", "02:30 PM", "04:00 PM"]
    },
    {
        "name": "Dr. Hassan Raza",
        "title": "Neurological & Post-Stroke Specialist",
        "exp": "7 Years",
        "patients": "310+ Treated",
        "rating": "5.0 ★",
        "fee": "Rs. 2,800",
        "email": "hassan@example.com",
        "jazzcash": "0300-5554433",
        "easypaisa": "0300-5554433",
        "bank": "Faysal Bank A/C: 301011223344 (Title: Dr Hassan Raza)",
        "tags": ["stroke", "post-stroke", "paralysis", "neurology"],
        "slots": ["01:00 PM", "04:30 PM"]
    }
]

# --- 6. SIDEBAR NAVIGATION ---
sidebar_html = """
<div class="brand-container">
    <div class="brand-title">🩺 TeleSynapse</div>
    <div class="brand-sub">Clinical Tele-Rehab Portal</div>
</div>
"""
st.sidebar.markdown(clean_html(sidebar_html), unsafe_allow_html=True)

menu = st.sidebar.radio("Navigation Menu", [
    "🩺 TeleSynapse 3-Step Secure Booking",
    "📊 Clinician & Admin Dashboard",
    "📹 Kinematic Motion AI Suite",
    "📈 Patient Mobility Progress"
])

# --- 7. HELPER: OFFICIAL PAID ATM SLIP RENDERER ---
def render_official_paid_slip(booking):
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=110x110&data=TeleSynapse-PaidSlip-{booking['SlipNo']}"

    slip_html = f"""
    <div style="background:#0F172A; border:2px dashed #10B981; border-radius:16px; padding:24px; max-width:460px; margin:20px auto; font-family:'JetBrains Mono', monospace; color:#E5E7EB; box-shadow:0 10px 30px rgba(0,0,0,0.5);">
        
        <div style="text-align:center; border-bottom:2px solid #334155; padding-bottom:12px; margin-bottom:14px;">
            <div style="color:#38BDF8; font-size:1.25rem; font-weight:800; letter-spacing:1px;">TELE-SYNAPSE HEALTH</div>
            <div style="color:#34D399; font-size:0.75rem; letter-spacing:2px; font-weight:700;">OFFICIAL PAID APPOINTMENT SLIP</div>
        </div>

        <div style="display:flex; justify-content:space-between; margin-bottom:6px; font-size:0.85rem;">
            <span style="color:#64748B;">SLIP NO:</span>
            <span style="color:#38BDF8; font-weight:700;">{booking['SlipNo']}</span>
        </div>
        <div style="display:flex; justify-content:space-between; margin-bottom:6px; font-size:0.85rem;">
            <span style="color:#64748B;">REF ID:</span>
            <span style="color:#F8FAFC; font-weight:700;">{booking['RefID']}</span>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px; font-size:0.85rem;">
            <span style="color:#64748B;">STATUS:</span>
            <span style="background:#064E3B; color:#34D399; border:1px solid #10B981; padding:3px 10px; border-radius:6px; font-weight:800; font-size:0.8rem;">PAID ✓</span>
        </div>
        
        <div style="font-size:0.72rem; color:#34D399; background:#064E3B; padding:6px 10px; border-radius:6px; margin-bottom:12px;">
            VERIFIED BY: {booking.get('VerifiedBy', 'Doctor Approved')}<br>
            STAMP TIME: {booking.get('VerifiedAt', 'N/A')}
        </div>

        <div style="color:#34D399; font-size:0.75rem; font-weight:800; border-bottom:1px solid #1E293B; margin:14px 0 6px 0; padding-bottom:2px;">PATIENT DETAILS</div>
        <div style="display:flex; justify-content:space-between; margin-bottom:4px; font-size:0.85rem;">
            <span style="color:#64748B;">Patient Name:</span>
            <span style="color:#F8FAFC; font-weight:700;">{booking['Patient']}</span>
        </div>
        <div style="display:flex; justify-content:space-between; margin-bottom:4px; font-size:0.85rem;">
            <span style="color:#64748B;">Contact:</span>
            <span style="color:#F8FAFC; font-weight:700;">{booking['Phone']}</span>
        </div>

        <div style="color:#34D399; font-size:0.75rem; font-weight:800; border-bottom:1px solid #1E293B; margin:14px 0 6px 0; padding-bottom:2px;">CLINICAL & SCHEDULE</div>
        <div style="display:flex; justify-content:space-between; margin-bottom:4px; font-size:0.85rem;">
            <span style="color:#64748B;">Condition:</span>
            <span style="color:#34D399; font-weight:700;">{booking['Type']}</span>
        </div>
        <div style="display:flex; justify-content:space-between; margin-bottom:4px; font-size:0.85rem;">
            <span style="color:#64748B;">Attending Doctor:</span>
            <span style="color:#F8FAFC; font-weight:700;">{booking['Doctor']}</span>
        </div>
        <div style="display:flex; justify-content:space-between; margin-bottom:12px; font-size:0.85rem;">
            <span style="color:#64748B;">Date & Time:</span>
            <span style="color:#F8FAFC; font-weight:700;">{booking['Date']} @ {booking['Time']}</span>
        </div>

        <div style="background:#1E293B; border:1px solid #10B981; border-radius:10px; padding:12px; margin-top:14px; text-align:center;">
            <div style="color:#38BDF8; font-size:0.75rem; font-weight:800; letter-spacing:0.5px; margin-bottom:4px;">UNLOCKED CLINICAL JOIN LINK</div>
            <a href="https://meet.jit.si/TeleSynapse-{booking['SlipNo']}" target="_blank" style="color:#34D399; font-weight:800; text-decoration:underline; font-size:0.9rem;">https://meet.jit.si/TeleSynapse-{booking['SlipNo']}</a>
            <div style="color:#94A3B8; font-size:0.68rem; margin-top:4px;">🟢 Active for session on {booking['Date']}</div>
        </div>

        <div style="text-align:center; margin-top:16px; padding-top:12px; border-top:2px dashed #334155;">
            <img src="{qr_url}" width="95" style="border-radius:8px; border:2px solid #334155;" />
            <div style="font-size:0.7rem; color:#94A3B8; margin-top:6px;">Scan QR to verify authentic TeleSynapse receipt</div>
        </div>
    </div>
    """
    st.markdown(clean_html(slip_html), unsafe_allow_html=True)

# --- 8. MODULE 1: TELE-SYNAPSE 3-STEP SECURE BOOKING FLOW ---
if menu == "🩺 TeleSynapse 3-Step Secure Booking":
    
    step_indicator = """
    <div style="display:flex; justify-content:space-between; margin-bottom:24px; background:#1E293B; padding:12px 20px; border-radius:12px; border:1px solid #334155;">
        <div style="color:#34D399; font-weight:800;">STEP 1: Book Slot</div>
        <div style="color:#94A3B8;">➔</div>
        <div style="color:#38BDF8; font-weight:800;">STEP 2: Pay & Upload Proof</div>
        <div style="color:#94A3B8;">➔</div>
        <div style="color:#A78BFA; font-weight:800;">STEP 3: Verification & Slip</div>
    </div>
    """
    st.markdown(clean_html(step_indicator), unsafe_allow_html=True)

    # --- STEP 1: BOOK YOUR SLOT ---
    if st.session_state["booking_step"] == "STEP_1_BOOK":
        banner_html = """
        <div class="hero-banner">
            <div class="hero-title">STEP 1: BOOK YOUR SLOT</div>
            <div class="hero-sub">Fill details, select specialist & schedule session.</div>
        </div>
        """
        st.markdown(clean_html(banner_html), unsafe_allow_html=True)

        with st.form("step1_booking_form"):
            st.markdown("<h4>1. Patient Details & Condition</h4>", unsafe_allow_html=True)
            c_n, c_p, c_e = st.columns([2, 2, 2])
            with c_n:
                p_name = st.text_input("Full Name *", value="Muhammad Hassan Raza")
            with c_p:
                p_phone = st.text_input("WhatsApp Phone *", value="+92 309 7964195")
            with c_e:
                p_email = st.text_input("Email Address *", value="hassan@example.com")

            c_a, c_g, c_d = st.columns([1, 1, 3])
            with c_a:
                p_age = st.number_input("Age", 5, 100, 21)
            with c_g:
                p_gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            with c_d:
                p_disease = st.text_input("Medical Condition / Primary Symptoms *", value="Lower Back Pain - Acute")

            c_onset, c_pain = st.columns(2)
            with c_onset:
                p_onset = st.selectbox("Duration / Onset:", ["3 Days (Acute)", "2 Weeks", "1 Month", "3+ Months"])
            with c_pain:
                p_pain = st.slider("Pain Severity (1 - 10):", 1, 10, 7)

            st.markdown("<h4>2. Choose Attending Doctor & Schedule</h4>", unsafe_allow_html=True)
            doc_names = [d["name"] + " (" + d["title"] + " - " + d["fee"] + ")" for d in DOCTORS_DATABASE]
            chosen_doc_str = st.selectbox("Select Specialist:", doc_names)
            
            chosen_doc = next(d for d in DOCTORS_DATABASE if d["name"] in chosen_doc_str)

            c_plat, c_date, c_slot = st.columns(3)
            with c_plat:
                p_platform = st.selectbox("Preferred Platform:", ["WhatsApp Video", "Zoom", "MS Teams", "Google Meet"])
            with c_date:
                p_date = st.selectbox("Select Date:", ["Fri, 05 Sep 2026", "Sat, 06 Sep 2026", "Mon, 08 Sep 2026"])
            with c_slot:
                p_slot = st.selectbox("Available Time Slot:", chosen_doc["slots"])

            st.markdown("<br>", unsafe_allow_html=True)
            submit_step1 = st.form_submit_button("PROCEED TO PAYMENT →")

            if submit_step1:
                if p_name and p_phone and p_disease:
                    st.session_state["temp_booking"] = {
                        "Patient": p_name,
                        "Phone": p_phone,
                        "Email": p_email,
                        "Age": p_age,
                        "Gender": p_gender,
                        "Type": p_disease,
                        "Onset": p_onset,
                        "PainLevel": p_pain,
                        "DoctorObj": chosen_doc,
                        "Doctor": chosen_doc["name"],
                        "Specialty": chosen_doc["title"],
                        "Fee": chosen_doc["fee"],
                        "Platform": p_platform,
                        "Date": p_date,
                        "Time": p_slot
                    }
                    st.session_state["booking_step"] = "STEP_2_PAYMENT"
                    st.session_state["show_proof_error"] = False
                    st.rerun()
                else:
                    st.error("Please fill in all required fields.")

    # --- STEP 2: PAY TO DOCTOR & UPLOAD PROOF ---
    elif st.session_state["booking_step"] == "STEP_2_PAYMENT":
        temp = st.session_state["temp_booking"]
        doc = temp["DoctorObj"]

        banner_html = """
        <div class="hero-banner">
            <div class="hero-title">STEP 2: PAY TO DOCTOR & UPLOAD SCREENSHOT</div>
            <div class="hero-sub">Directly transfer fee to doctor's account and attach proof.</div>
        </div>
        """
        st.markdown(clean_html(banner_html), unsafe_allow_html=True)

        if st.session_state.get("show_proof_error", False):
            alert_modal_html = """
            <div style="background:#2A0808; border:2px solid #EF4444; border-radius:14px; padding:20px; margin-bottom:20px; font-family:'JetBrains Mono', monospace; text-align:center; box-shadow:0 10px 25px rgba(239,68,68,0.2);">
                <div style="color:#EF4444; font-size:1.2rem; font-weight:800; letter-spacing:1px; margin-bottom:6px;">
                    ⚠️ PAYMENT PROOF REQUIRED
                </div>
                <div style="border-bottom:1px solid #7F1D1D; margin-bottom:12px;"></div>
                <div style="color:#F8FAFC; font-size:0.92rem; margin-bottom:8px;">
                    Please upload the screenshot of your JazzCash / EasyPaisa / Bank payment to proceed.
                </div>
                <div style="color:#FCA5A5; font-size:0.82rem; font-weight:700;">
                    Without payment proof, your slot cannot be confirmed and slip will NOT be generated.
                </div>
            </div>
            """
            st.markdown(clean_html(alert_modal_html), unsafe_allow_html=True)

        c_left, c_right = st.columns([1, 1])

        with c_left:
            st.markdown(f"### 💳 Pay {temp['Fee']} to {doc['name']}")
            
            st.markdown(clean_html(f"""
            <div class="pay-card">
                <div class="pay-title">🔴 JAZZCASH ACCOUNT</div>
                <div class="pay-val">{doc['jazzcash']}</div>
                <div style="color:#94A3B8; font-size:0.75rem; margin-top:2px;">Title: {doc['name']}</div>
            </div>
            <div class="pay-card">
                <div class="pay-title">🟢 EASYPAISA ACCOUNT</div>
                <div class="pay-val">{doc['easypaisa']}</div>
                <div style="color:#94A3B8; font-size:0.75rem; margin-top:2px;">Title: {doc['name']}</div>
            </div>
            <div class="pay-card">
                <div class="pay-title">🏦 BANK TRANSFER DETAILS</div>
                <div class="pay-val">{doc['bank']}</div>
            </div>
            """), unsafe_allow_html=True)

        with c_right:
            st.markdown("### 📤 Upload Payment Proof <span style='color:#EF4444;'>*</span>", unsafe_allow_html=True)
            
            uploaded_file = st.file_uploader(
                "Select Payment Screenshot / PDF (Max 5MB)", 
                type=["jpg", "jpeg", "png", "pdf"],
                help="Allowed extensions: JPG, PNG, PDF. File size up to 5MB."
            )
            
            st.markdown("""
            <div style="background:#451A03; border:1px solid #F59E0B; border-radius:10px; padding:10px 14px; margin:14px 0; color:#FDE047; font-size:0.8rem;">
                ⏱️ <b>Auto-Expiry Timer:</b> Unverified requests automatically expire after 30 minutes.
            </div>
            """, unsafe_allow_html=True)

            c_btn1, c_btn2 = st.columns(2)
            with c_btn1:
                if st.button("← Back to Step 1"):
                    st.session_state["show_proof_error"] = False
                    st.session_state["booking_step"] = "STEP_1_BOOK"
                    st.rerun()

            with c_btn2:
                if st.button("I HAVE PAID - SUBMIT →"):
                    if uploaded_file is None:
                        st.session_state["show_proof_error"] = True
                        st.rerun()
                    else:
                        st.session_state["show_proof_error"] = False
                        slip_num = f"TS-{random.randint(80000, 99999)}"
                        ref_num = f"TS-P-{random.randint(1000, 9999)}"

                        new_booking = {
                            "SlipNo": slip_num,
                            "RefID": ref_num,
                            "Patient": temp["Patient"],
                            "Phone": temp["Phone"],
                            "Email": temp["Email"],
                            "Age": temp["Age"],
                            "Gender": temp["Gender"],
                            "Doctor": temp["Doctor"],
                            "Specialty": temp["Specialty"],
                            "Date": temp["Date"],
                            "Time": temp["Time"],
                            "Type": temp["Type"],
                            "Onset": temp["Onset"],
                            "PainLevel": temp["PainLevel"],
                            "Platform": temp["Platform"],
                            "Fee": temp["Fee"],
                            "Status": "PENDING VERIFICATION",
                            "VerifiedBy": None,
                            "VerifiedAt": None,
                            "Proof": uploaded_file.name,
                            "RejectReason": None
                        }

                        st.session_state["appointments"].append(new_booking)
                        st.session_state["current_slip_num"] = slip_num
                        st.session_state["booking_step"] = "STEP_3_VERIFICATION"
                        st.rerun()

    # --- STEP 3: STRICT VERIFICATION & SLIP UNLOCK SCREEN ---
    elif st.session_state["booking_step"] == "STEP_3_VERIFICATION":
        slip_num = st.session_state["current_slip_num"]
        booking = next(a for a in st.session_state["appointments"] if a["SlipNo"] == slip_num)

        if booking["Status"] == "PENDING VERIFICATION":
            pending_box = f"""
            <div style="background:#1E293B; border:2px dashed #F59E0B; border-radius:16px; padding:28px; max-width:550px; margin:20px auto; text-align:center;">
                <div style="font-size:3rem; margin-bottom:10px;">🕒</div>
                <div style="color:#FDE047; font-size:1.3rem; font-weight:800;">PAYMENT VERIFICATION IN PROGRESS</div>
                <div style="color:#D1D5DB; font-size:0.9rem; margin-top:8px; line-height:1.5;">
                    Your transaction screenshot (<b>{booking['Proof']}</b>) has been dispatched directly to <b>{booking['Doctor']}</b>.
                </div>
                
                <div style="background:#0F172A; border:1px solid #334155; border-radius:12px; padding:16px; margin:20px 0; text-align:left;">
                    <div style="color:#38BDF8; font-weight:700; font-size:0.85rem;">BOOKING REQUEST SUMMARY</div>
                    <div style="color:#F8FAFC; margin-top:4px;"><b>Ref ID:</b> {booking['RefID']} | <b>Amount:</b> {booking['Fee']}</div>
                    <div style="color:#F8FAFC;"><b>Patient:</b> {booking['Patient']} ({booking['Phone']})</div>
                    <div style="color:#F8FAFC;"><b>Slot:</b> {booking['Date']} @ {booking['Time']}</div>
                </div>

                <div style="color:#EF4444; font-size:0.82rem; font-weight:700; background:#451A03; padding:8px 12px; border-radius:8px;">
                    🔒 SLIP & CLINICAL JOIN LINK ARE LOCKED UNTIL DOCTOR APPROVES PAYMENT
                </div>
            </div>
            """
            st.markdown(clean_html(pending_box), unsafe_allow_html=True)

            c_ref, c_dash = st.columns(2)
            with c_ref:
                if st.button("🔄 Check Verification Status"):
                    st.rerun()
            with c_dash:
                st.info("💡 Open 'Clinician & Admin Dashboard' menu in sidebar to simulate Doctor Approving payment.")

        elif booking["Status"] == "PAID ✓":
            st.success("🎉 PAYMENT VERIFIED BY DOCTOR! OFFICIAL SLIP & JOIN LINK UNLOCKED.")
            render_official_paid_slip(booking)

            c_a1, c_a2 = st.columns(2)
            with c_a1:
                st.button("📥 Download Official Slip PDF")
            with c_a2:
                st.button("📲 Resend to WhatsApp")

            if st.button("Book Another Appointment"):
                st.session_state["booking_step"] = "STEP_1_BOOK"
                st.rerun()

        else:
            st.error(f"❌ PAYMENT REJECTED BY DOCTOR: {booking.get('RejectReason', 'Invalid Payment')}")
            if st.button("← Re-upload Screenshot"):
                st.session_state["booking_step"] = "STEP_2_PAYMENT"
                st.rerun()

# --- 9. MODULE 2: CLINICIAN & ADMIN DASHBOARD ---
elif menu == "📊 Clinician & Admin Dashboard":
    st.markdown("<h3>🏥 Doctor & Admin Payment Verification Portal</h3>", unsafe_allow_html=True)

    tab_verify, tab_all = st.tabs(["💳 Payment Verification Queue", "📋 All Confirmed Patients"])

    with tab_verify:
        st.markdown("#### Pending Payment Screenshot Requests")
        
        pending_list = [a for a in st.session_state["appointments"] if a["Status"] == "PENDING VERIFICATION"]

        if not pending_list:
            st.success("🎉 All payment screenshots verified! Queue is clear.")
        else:
            for idx, item in enumerate(pending_list):
                with st.expander(f"🚨 New Payment: {item['Patient']} — {item['Fee']} ({item['Doctor']})", expanded=True):
                    c_det, c_proof, c_action = st.columns([2, 2, 2])
                    
                    with c_det:
                        st.markdown(f"**Ref ID:** `{item['RefID']}`")
                        st.markdown(f"**Patient:** {item['Patient']} ({item['Phone']})")
                        st.markdown(f"**Condition:** {item['Type']}")
                        st.markdown(f"**Schedule:** {item['Date']} @ {item['Time']}")

                    with c_proof:
                        st.markdown(f"**Uploaded Proof File:** `{item['Proof']}`")
                        st.image("https://via.placeholder.com/320x180/1E293B/38BDF8?text=JazzCash+Receipt+Verified", caption="Uploaded Receipt View")

                    with c_action:
                        st.markdown("**Doctor Action:**")
                        if st.button(f"✔ VERIFY & UNLOCK SLIP", key=f"app_{idx}"):
                            now_str = datetime.datetime.now().strftime("%d-%b-%Y %I:%M %p")
                            item["Status"] = "PAID ✓"
                            item["VerifiedBy"] = f"{item['Doctor']} (Doctor Verified)"
                            item["VerifiedAt"] = now_str
                            send_doctor_clinical_snapshot(item["Doctor"], item)
                            st.success(f"Verified payment for {item['Patient']}! Paid Slip generated.")
                            st.rerun()

                        rej_reason = st.text_input("Reason if rejecting:", value="Amount Mismatch", key=f"rr_{idx}")
                        if st.button(f"❌ REJECT SCREENSHOT", key=f"rej_{idx}"):
                            item["Status"] = "REJECTED"
                            item["RejectReason"] = rej_reason
                            st.error("Payment rejected.")
                            st.rerun()

    with tab_all:
        for app in reversed(st.session_state["appointments"]):
            if app["Status"] == "PAID ✓":
                render_official_paid_slip(app)
                st.markdown("---")

# --- 10. MODULE 3: KINEMATIC MOTION AI SUITE ---
elif menu == "📹 Kinematic Motion AI Suite":
    
    # --- HEADER & REAL-TIME STATUS BAR ---
    status_bar_html = f"""
    <div style="background:#1E293B; border:1px solid #334155; border-radius:14px; padding:14px 22px; margin-bottom:20px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
        <div style="display:flex; align-items:center; gap:12px;">
            <span style="color:#10B981; font-size:1.2rem; animation: pulse 1s infinite;">●</span>
            <span style="color:#34D399; font-weight:800; font-size:1.1rem; letter-spacing:0.5px;">KINEMATIC MOTION ANALYSIS ENGINE</span>
        </div>
        <div style="display:flex; gap:18px; font-family:'JetBrains Mono', monospace; font-size:0.85rem; color:#94A3B8;">
            <span>STATUS: <b style="color:#34D399;">LIVE CAMERA ON</b></span>
            <span>GPU: <b style="color:#38BDF8;">ACTIVE (WebGL)</b></span>
            <span>FPS: <b style="color:#F8FAFC;">30</b></span>
            <span>GHOST MODE: <b style="color:{'#34D399' if st.session_state['ghost_mode'] else '#64748B'};">{'ENABLED' if st.session_state['ghost_mode'] else 'OFF'}</b></span>
        </div>
    </div>
    """
    st.markdown(clean_html(status_bar_html), unsafe_allow_html=True)

    c_viz, c_side = st.columns([7, 5])

    with c_viz:
        st.markdown("#### 📷 AI Color Skeleton & Pain Heatmap Feed")

        # HTML5 Canvas + MediaPipe GPU Simulation Visualizer Box
        canvas_html = f"""
        <div style="position:relative; width:100%; height:420px; background:#0F172A; border:2px solid #334155; border-radius:16px; overflow:hidden; box-shadow:0 12px 30px rgba(0,0,0,0.6);">
            
            <!-- Background Camera Feed Graphic -->
            <div style="position:absolute; width:100%; height:100%; background:radial-gradient(circle, #1E293B 0%, #0B0F17 100%); display:flex; justify-content:center; align-items:center;">
                <svg width="220" height="340" viewBox="0 0 200 320" style="opacity:0.25;">
                    <circle cx="100" cy="40" r="22" fill="none" stroke="#64748B" stroke-width="4"/>
                    <line x1="100" y1="62" x2="100" y2="170" stroke="#64748B" stroke-width="6"/>
                    <line x1="100" y1="85" x2="50" y2="140" stroke="#64748B" stroke-width="5"/>
                    <line x1="100" y1="85" x2="150" y2="140" stroke="#64748B" stroke-width="5"/>
                    <line x1="100" y1="170" x2="60" y2="280" stroke="#64748B" stroke-width="5"/>
                    <line x1="100" y1="170" x2="140" y2="280" stroke="#64748B" stroke-width="5"/>
                </svg>
            </div>

            <!-- GHOST OVERLAY SILHOUETTE (BEFORE SESSION) -->
            {'<svg width="100%" height="100%" style="position:absolute; top:0; left:0; opacity:0.35; filter:drop-shadow(0 0 8px #38BDF8);"><circle cx="50%" cy="80" r="20" fill="none" stroke="#38BDF8" stroke-width="3" stroke-dasharray="4"/><line x1="50%" y1="100" x2="50%" y2="200" stroke="#38BDF8" stroke-width="4" stroke-dasharray="4"/><line x1="50%" y1="200" x2="42%" y2="310" stroke="#38BDF8" stroke-width="4" stroke-dasharray="4"/><line x1="50%" y1="200" x2="58%" y2="310" stroke="#38BDF8" stroke-width="4" stroke-dasharray="4"/><text x="20" y="35" fill="#38BDF8" font-size="12" font-weight="bold">👻 GHOST OVERLAY: AUG 26 SESSION (110° MAX)</text></svg>' if st.session_state['ghost_mode'] else ''}

            <!-- REAL-TIME AI COLOR SKELETON & HEATMAP OVERLAY -->
            <svg width="100%" height="100%" style="position:absolute; top:0; left:0;">
                <!-- Head & Torso Joints (Green = Normal ROM) -->
                <circle cx="50%" cy="80" r="8" fill="#10B981"/>
                <line x1="50%" y1="88" x2="50%" y2="190" stroke="#10B981" stroke-width="5"/>
                
                <!-- Shoulder & Arms (Green = Normal) -->
                <circle cx="40%" cy="110" r="7" fill="#10B981"/>
                <circle cx="60%" cy="110" r="7" fill="#10B981"/>
                <line x1="50%" y1="110" x2="40%" y2="110" stroke="#10B981" stroke-width="4"/>
                <line x1="50%" y1="110" x2="60%" y2="110" stroke="#10B981" stroke-width="4"/>
                <line x1="40%" y1="110" x2="32%" y2="160" stroke="#10B981" stroke-width="4"/>
                <line x1="60%" y1="110" x2="68%" y2="160" stroke="#10B981" stroke-width="4"/>
                
                <!-- Hips (Yellow = Stiff 50%) -->
                <circle cx="45%" cy="190" r="8" fill="#F59E0B"/>
                <circle cx="55%" cy="190" r="8" fill="#F59E0B"/>
                <line x1="45%" y1="190" x2="55%" y2="190" stroke="#F59E0B" stroke-width="5"/>

                <!-- Right Leg (Green = Good) -->
                <line x1="55%" y1="190" x2="58%" y2="260" stroke="#10B981" stroke-width="4"/>
                <circle cx="58%" cy="260" r="7" fill="#10B981"/>
                <line x1="58%" y1="260" x2="60%" y2="330" stroke="#10B981" stroke-width="4"/>

                <!-- Left Leg / Knee (RED PAIN HEATMAP AREA = LOW ROM) -->
                <line x1="45%" y1="190" x2="38%" y2="255" stroke="#EF4444" stroke-width="5"/>
                
                <!-- PAIN HEATMAP GLOW -->
                <circle cx="38%" cy="255" r="22" fill="#EF4444" opacity="0.35"/>
                <circle cx="38%" cy="255" r="10" fill="#EF4444"/>
                <text x="24%" y="260" fill="#EF4444" font-size="11" font-weight="bold" font-family="sans-serif">⚠️ PAIN HEATMAP (92°)</text>

                <line x1="38%" y1="255" x2="35%" y2="330" stroke="#EF4444" stroke-width="4"/>
            </svg>

            <!-- LIVE FORM COACH VOICE / TEXT BANNER -->
            <div style="position:absolute; bottom:14px; left:14px; right:14px; background:rgba(15, 23, 42, 0.9); border:1px solid #EF4444; border-radius:10px; padding:10px 14px; display:flex; align-items:center; gap:12px; backdrop-filter:blur(8px);">
                <span style="font-size:1.4rem;">🔊</span>
                <div>
                    <div style="color:#EF4444; font-weight:800; font-size:0.8rem; letter-spacing:0.5px;">AI FORM COACH (LIVE VOICE & TEXT)</div>
                    <div style="color:#F8FAFC; font-size:0.88rem; font-weight:600;">"Rep {st.session_state['current_reps']} of 10 — Left knee collapsing inward by 12°. Straighten joint!"</div>
                </div>
            </div>

            <div style="position:absolute; top:14px; right:14px; background:#064E3B; border:1px solid #10B981; border-radius:8px; padding:6px 12px; color:#34D399; font-size:0.75rem; font-weight:800; font-family:'JetBrains Mono';">
                ANGLE: 92.4° FLEXION
            </div>
        </div>
        """
        st.markdown(clean_html(canvas_html), unsafe_allow_html=True)

        # BOTTOM ACTION CONTROL BUTTONS
        st.markdown("<br>", unsafe_allow_html=True)
        c_b1, c_b2, c_b3 = st.columns(3)
        with c_b1:
            if st.button("▶ START / RESUME SESSION"):
                st.session_state["ai_session_running"] = True
                st.toast("AI Kinematic Tracker Activated!")
        with c_b2:
            if st.button("👻 TOGGLE GHOST OVERLAY"):
                st.session_state["ghost_mode"] = not st.session_state["ghost_mode"]
                st.rerun()
        with c_b3:
            if st.button("➕ SIMULATE COMPLETED REP"):
                st.session_state["current_reps"] = min(10, st.session_state["current_reps"] + 1)
                st.rerun()

    with c_side:
        st.markdown("#### 📊 Real-Time Kinematic Metrics")

        # LIVE METRICS HUD CARDS
        c_m1, c_m2 = st.columns(2)
        with c_m1:
            st.markdown(clean_html(f"""
            <div class="stat-card">
                <div class="stat-val" style="color:#34D399;">{st.session_state['current_reps']}/10</div>
                <div class="stat-lbl">REPETITIONS</div>
            </div>
            """), unsafe_allow_html=True)
        with c_m2:
            st.markdown(clean_html("""
            <div class="stat-card">
                <div class="stat-val" style="color:#38BDF8;">92.4°</div>
                <div class="stat-lbl">PEAK FLEXION</div>
            </div>
            """), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        c_m3, c_m4 = st.columns(2)
        with c_m3:
            st.markdown(clean_html("""
            <div class="stat-card">
                <div class="stat-val" style="color:#A78BFA;">B+</div>
                <div class="stat-lbl">FORM SCORE (87%)</div>
            </div>
            """), unsafe_allow_html=True)
        with c_m4:
            st.markdown(clean_html("""
            <div class="stat-card">
                <div class="stat-val" style="color:#34D399;">+22%</div>
                <div class="stat-lbl">ROM IMPROVEMENT</div>
            </div>
            """), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 🟢 Joint Health Status Breakdown")
        
        joint_status_html = """
        <div style="background:#1E293B; border:1px solid #334155; border-radius:12px; padding:14px; font-size:0.85rem;">
            <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                <span>🟢 Right Knee Extension:</span>
                <b style="color:#34D399;">168° (Normal)</b>
            </div>
            <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                <span>🟡 Lumbar Hip Flexion:</span>
                <b style="color:#F59E0B;">110° (50% Stiff)</b>
            </div>
            <div style="display:flex; justify-content:space-between;">
                <span>🔴 Left Knee Joint (Pain Area):</span>
                <b style="color:#EF4444;">92° (Pain Threshold)</b>
            </div>
        </div>
        """
        st.markdown(clean_html(joint_status_html), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        # 1-CLICK CLINICAL REPORT GENERATOR
        st.markdown("#### 📄 1-Click Clinical Doctor PDF")
        
        report_data = f"""
        TELE-SYNAPSE CLINICAL KINEMATIC REPORT
        ----------------------------------------------------
        PATIENT: Muhammad Hassan Raza | AGE: 21 | GENDER: Male
        ATTENDING DOCTOR: Dr. Ayesha Malik
        SESSION DATE: {datetime.datetime.now().strftime('%d-%b-%Y')}
        CONDITION: Lower Back Pain - Acute
        ----------------------------------------------------
        KINEMATIC METRICS SUMMARY:
        - Completed Repetitions: {st.session_state['current_reps']}/10
        - Peak Joint Flexion Angle: 92.4°
        - Range of Motion Improvement: +22% vs Baseline
        - Form Quality Grade: B+ (87%)
        - Primary Restriction: Left Knee Inward Valgus (12°)
        ----------------------------------------------------
        CLINICAL RECOMMENDATION:
        Continue quadriceps strengthening & lumbar mobilization 3x weekly.
        Next evaluation scheduled for Fri, 05 Sep 2026.
        """
        
        b64_report = base64.b64encode(report_data.encode()).decode()
        href = f'<a href="data:file/txt;base64,{b64_report}" download="TeleSynapse_Kinematic_Report_HassanRaza.txt" style="display:block; text-align:center; background:linear-gradient(90deg, #10B981, #06B6D4); color:#0B0F17; font-weight:800; border-radius:12px; padding:12px; text-decoration:none; box-shadow:0 4px 15px rgba(16,185,129,0.3);">📄 GENERATE & DOWNLOAD CLINICAL REPORT PDF</a>'
        st.markdown(href, unsafe_allow_html=True)

# --- 11. MODULE 4: PATIENT MOBILITY PROGRESS ---
else:
    st.markdown("<h3>📈 Patient Mobility Progress & Longitudinal Analytics</h3>", unsafe_allow_html=True)
    
    st.markdown("#### Joint Flexion Range of Motion (ROM) Over 4 Weeks")
    rom_df = pd.DataFrame({
        "Left Knee Flexion (°)": [60, 75, 88, 105],
        "Lumbar Spine Angle (°)": [45, 55, 68, 80],
        "Target Baseline (°)": [120, 120, 120, 120]
    }, index=["Week 1", "Week 2", "Week 3", "Week 4"])

    st.line_chart(rom_df)

    c_p1, c_p2 = st.columns(2)
    with c_p1:
        st.info("🟢 **Mobility Trend:** Patient demonstrates a **+75% cumulative improvement** in left knee flexion since Week 1.")
    with c_p2:
        st.success("✔ **Adherence Rate:** 94% compliance with prescribed home exercise protocols.")
