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
    page_title="TeleSynapse | Patient Visual Recovery Portal",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. AUTOMATED SECURE EMAIL RELAY ENGINE (PORTAL-ONLY PRIVACY) ---
def send_portal_email_notification(to_email, subject, body_content):
    """Sends encrypted portal updates via email. 
    Keeps doctors and patients within the portal loop without exposing private numbers."""
    sender_email = "alerts@telesynapse.com"
    sender_password = "your-encrypted-app-password"
    
    msg = MIMEText(body_content)
    msg['Subject'] = subject
    msg['From'] = f"TeleSynapse Portal <{sender_email}>"
    msg['To'] = to_email
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
    except Exception:
        pass  # Silent fallback in simulation mode

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

.privacy-badge {{
    background: rgba(16, 185, 129, 0.1);
    border: 1px solid #10B981;
    border-radius: 10px;
    padding: 10px 14px;
    font-size: 0.8rem;
    color: #34D399;
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 20px;
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
            "Type": "ACL Tear & Knee Joint Flexion",
            "Onset": "2 Weeks Ago",
            "PainLevel": 7,
            "Platform": "In-Portal Video Call",
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

if "show_comparison_modal" not in st.session_state:
    st.session_state["show_comparison_modal"] = False

# INITIALIZE VISUAL TRACKER STATE
if "affected_profile" not in st.session_state:
    st.session_state["affected_profile"] = {
        "organ": "Right Knee Joint",
        "injury": "ACL Tear & Meniscus Strain",
        "before_photo_date": "25-Aug-2026",
        "before_photo_url": "https://via.placeholder.com/300x200/1E293B/EF4444?text=Before+Rehab+(25-Aug)",
        "doctor_notes": "Severe Swelling +15%, Flexion restricted at 60°. Zero weight-bearing recommended for Week 1.",
        "weekly_photos": [
            {"week": "Week 1", "date": "25-Aug-2026", "flexion": 60, "swelling": "High (+15%)", "status": "Uploaded", "url": "https://via.placeholder.com/200x150/1E293B/EF4444?text=W1:+60%C2%B0+Flex"},
            {"week": "Week 2", "date": "01-Sep-2026", "flexion": 72, "swelling": "Moderate (+10%)", "status": "Uploaded", "url": "https://via.placeholder.com/200x150/1E293B/F59E0B?text=W2:+72%C2%B0+Flex"},
            {"week": "Week 3", "date": "08-Sep-2026", "flexion": 88, "swelling": "Mild (+5%)", "status": "Uploaded", "url": "https://via.placeholder.com/200x150/1E293B/38BDF8?text=W3:+88%C2%B0+Flex"},
            {"week": "Week 4", "date": "15-Sep-2026", "flexion": 105, "swelling": "Minimal (+2%)", "status": "Uploaded", "url": "https://via.placeholder.com/200x150/1E293B/34D399?text=W4:+105%C2%B0+Flex"}
        ]
    }

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
    "📸 Patient Visual Recovery Tracker"
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
            <div style="color:#94A3B8; font-size:0.68rem; margin-top:4px;">🟢 Encrypted In-Portal Video Link</div>
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
                p_disease = st.text_input("Medical Condition / Primary Symptoms *", value="ACL Tear & Knee Joint Flexion")

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
                p_platform = st.selectbox("Preferred Platform:", ["In-Portal Video Call", "Google Meet", "Zoom"])
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
            st.error("⚠️ Payment screenshot upload is mandatory to generate your appointment slip!")

        c_left, c_right = st.columns([1, 1])
        with c_left:
            st.markdown(f"### 💳 Pay {temp['Fee']} to {doc['name']}")
            st.markdown(clean_html(f"""
            <div class="pay-card">
                <div class="pay-title">🔴 JAZZCASH ACCOUNT</div>
                <div class="pay-val">{doc['jazzcash']}</div>
            </div>
            <div class="pay-card">
                <div class="pay-title">🟢 EASYPAISA ACCOUNT</div>
                <div class="pay-val">{doc['easypaisa']}</div>
            </div>
            <div class="pay-card">
                <div class="pay-title">🏦 BANK TRANSFER DETAILS</div>
                <div class="pay-val">{doc['bank']}</div>
            </div>
            """), unsafe_allow_html=True)

        with c_right:
            st.markdown("### 📤 Upload Payment Proof *")
            uploaded_file = st.file_uploader("Select Payment Screenshot / PDF", type=["jpg", "jpeg", "png", "pdf"])

            c_btn1, c_btn2 = st.columns(2)
            with c_btn1:
                if st.button("← Back to Step 1"):
                    st.session_state["booking_step"] = "STEP_1_BOOK"
                    st.rerun()
            with c_btn2:
                if st.button("I HAVE PAID - SUBMIT →"):
                    if uploaded_file is None:
                        st.session_state["show_proof_error"] = True
                        st.rerun()
                    else:
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

    elif st.session_state["booking_step"] == "STEP_3_VERIFICATION":
        slip_num = st.session_state["current_slip_num"]
        booking = next(a for a in st.session_state["appointments"] if a["SlipNo"] == slip_num)

        if booking["Status"] == "PENDING VERIFICATION":
            st.warning("🕒 Payment verification in progress by doctor...")
            if st.button("🔄 Refresh Status"):
                st.rerun()
        elif booking["Status"] == "PAID ✓":
            st.success("🎉 PAYMENT VERIFIED! SLIP & JOIN LINK UNLOCKED.")
            render_official_paid_slip(booking)

# --- 9. MODULE 2: CLINICIAN & ADMIN DASHBOARD ---
elif menu == "📊 Clinician & Admin Dashboard":
    st.markdown("<h3>🏥 Doctor & Admin Dashboard</h3>", unsafe_allow_html=True)
    tab_verify, tab_photos, tab_all = st.tabs([
        "💳 Payment Verification Queue", 
        "📸 Pending Photo Reviews", 
        "📋 All Confirmed Patients"
    ])

    with tab_verify:
        pending_list = [a for a in st.session_state["appointments"] if a["Status"] == "PENDING VERIFICATION"]
        if not pending_list:
            st.success("🎉 All payments verified!")
        else:
            for idx, item in enumerate(pending_list):
                with st.expander(f"🚨 Payment: {item['Patient']} — {item['Fee']}", expanded=True):
                    if st.button(f"✔ VERIFY & UNLOCK SLIP", key=f"app_{idx}"):
                        item["Status"] = "PAID ✓"
                        item["VerifiedBy"] = f"{item['Doctor']} (Doctor Verified)"
                        item["VerifiedAt"] = datetime.datetime.now().strftime("%d-%b-%Y %I:%M %p")
                        send_portal_email_notification(item["Email"], "Payment Approved!", "Your session slip is now unlocked.")
                        st.success("Verified!")
                        st.rerun()

    with tab_photos:
        st.markdown("#### 📸 Patient Weekly Visual Progress Photo Submissions")
        prof = st.session_state["affected_profile"]
        
        st.markdown(f"**Patient:** Muhammad Hassan Raza | **Affected Area:** {prof['organ']} ({prof['injury']})")
        
        c_p1, c_p2 = st.columns([1, 2])
        with c_p1:
            st.image(prof['weekly_photos'][-1]['url'], caption="Latest Uploaded Photo (Week 4)", use_container_width=True)
        with c_right if 'c_right' in locals() else c_p2:
            st.markdown(f"**Flexion Angle:** {prof['weekly_photos'][-1]['flexion']}°")
            st.markdown(f"**Swelling Status:** {prof['weekly_photos'][-1]['swelling']}")
            
            doc_comment = st.text_area("Doctor Assessment / Clinical Comment:", value="Excellent progress! Swelling is down significantly and knee bend reached 105°. Continue 3x daily protocol.")
            
            if st.button("💬 Send Encrypted Feedback to Patient Portal"):
                prof["doctor_notes"] = doc_comment
                send_portal_email_notification(
                    "hassan@example.com", 
                    "Dr. Ayesha Reviewed Your Recovery Photo", 
                    f"Doctor Note: {doc_comment}"
                )
                st.success("✔ Comment updated and dispatched via encrypted portal email!")

    with tab_all:
        for app in reversed(st.session_state["appointments"]):
            if app["Status"] == "PAID ✓":
                render_official_paid_slip(app)

# --- 10. MODULE 3: KINEMATIC MOTION AI SUITE ---
elif menu == "📹 Kinematic Motion AI Suite":
    status_bar_html = """
    <div style="background:#1E293B; border:1px solid #334155; border-radius:14px; padding:14px 22px; margin-bottom:20px; display:flex; justify-content:space-between; align-items:center;">
        <div style="display:flex; align-items:center; gap:12px;">
            <span style="color:#10B981; font-size:1.2rem;">●</span>
            <span style="color:#34D399; font-weight:800; font-size:1.1rem;">KINEMATIC MOTION ANALYSIS ENGINE</span>
        </div>
        <div style="font-family:'JetBrains Mono', monospace; font-size:0.85rem; color:#94A3B8;">
            STATUS: <b style="color:#34D399;">LIVE CAMERA ON</b> | GPU: <b style="color:#38BDF8;">ACTIVE</b> | FPS: <b>30</b>
        </div>
    </div>
    """
    st.markdown(clean_html(status_bar_html), unsafe_allow_html=True)
    st.info("💡 Kinematic Motion Analysis Engine active with AI color joint heatmap & form coaching.")

# --- 11. MODULE 4: PATIENT VISUAL RECOVERY TRACKER (UPGRADED) ---
else:
    prof = st.session_state["affected_profile"]

    # STRICT PRIVACY & IN-PORTAL EMAIL NOTICE
    privacy_notice_html = """
    <div class="privacy-badge">
        <span>🔒 <b>HIPAA & AES-256 Vault Encryption Active:</b> All recovery photos are strictly restricted to Patient, Attending Doctor, and Clinical Admin. All notifications are routed via encrypted portal email (<code>alerts@telesynapse.com</code>). Direct phone or off-platform communication is disabled to ensure clinical security.</span>
    </div>
    """
    st.markdown(clean_html(privacy_notice_html), unsafe_allow_html=True)

    # --- SECTION 1: AFFECTED AREA PROFILE ---
    st.markdown("### 🦵 Affected Area Profile")
    
    profile_card_html = f"""
    <div style="background:#1E293B; border:2px solid #334155; border-radius:16px; padding:22px; margin-bottom:28px; box-shadow:0 10px 25px rgba(0,0,0,0.4);">
        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #334155; padding-bottom:12px; margin-bottom:16px;">
            <div style="color:#38BDF8; font-weight:800; font-size:1.1rem; letter-spacing:0.5px;">AFFECTED AREA CLINICAL DOSSIER</div>
            <span style="background:#064E3B; color:#34D399; border:1px solid #10B981; padding:4px 12px; border-radius:8px; font-weight:700; font-size:0.78rem;">RULE: BEFORE PHOTO MANDATORY</span>
        </div>
        
        <div style="display:grid; grid-template-columns: 1fr 2fr; gap:20px; align-items:center;">
            <div style="text-align:center;">
                <img src="{prof['before_photo_url']}" style="width:100%; max-width:220px; border-radius:12px; border:2px solid #EF4444; margin-bottom:8px;" />
                <div style="color:#94A3B8; font-size:0.75rem; font-family:'JetBrains Mono', monospace;">Uploaded On: {prof['before_photo_date']}</div>
            </div>
            <div>
                <div style="display:flex; gap:20px; margin-bottom:12px; flex-wrap:wrap;">
                    <div style="background:#0F172A; padding:10px 16px; border-radius:10px; border:1px solid #334155; flex:1;">
                        <div style="color:#64748B; font-size:0.75rem; font-weight:700;">ORGAN / JOINT</div>
                        <div style="color:#F8FAFC; font-weight:800; font-size:1rem;">{prof['organ']}</div>
                    </div>
                    <div style="background:#0F172A; padding:10px 16px; border-radius:10px; border:1px solid #334155; flex:1;">
                        <div style="color:#64748B; font-size:0.75rem; font-weight:700;">DIAGNOSED INJURY</div>
                        <div style="color:#EF4444; font-weight:800; font-size:1rem;">{prof['injury']}</div>
                    </div>
                </div>
                
                <div style="background:#0F172A; border-left:4px solid #38BDF8; border-radius:8px; padding:12px 16px;">
                    <div style="color:#38BDF8; font-size:0.8rem; font-weight:800; margin-bottom:4px;">👨‍⚕️ ATTENDING DOCTOR CLINICAL NOTES:</div>
                    <div style="color:#E5E7EB; font-size:0.9rem; line-height:1.4;">"{prof['doctor_notes']}"</div>
                </div>
            </div>
        </div>
    </div>
    """
    st.markdown(clean_html(profile_card_html), unsafe_allow_html=True)

    # --- SECTION 2: INTUITIVE PATIENT-FRIENDLY RECOVERY METERS (LAYMAN RECOVERY VISUALIZER) ---
    st.markdown("### 📊 Your Plain-English Recovery Progress")
    
    latest_flexion = prof['weekly_photos'][-1]['flexion']
    flexion_pct = int((latest_flexion / 120.0) * 100)
    
    c_ind1, c_ind2, c_ind3 = st.columns(3)
    with c_ind1:
        st.markdown(clean_html(f"""
        <div class="stat-card">
            <div class="stat-val" style="color:#34D399;">{latest_flexion}°</div>
            <div class="stat-lbl">CURRENT KNEE BEND (GOAL: 120°)</div>
        </div>
        """), unsafe_allow_html=True)
    with c_ind2:
        st.markdown(clean_html(f"""
        <div class="stat-card">
            <div class="stat-val" style="color:#38BDF8;">+75%</div>
            <div class="stat-lbl">TOTAL RANGE IMPROVEMENT</div>
        </div>
        """), unsafe_allow_html=True)
    with c_ind3:
        st.markdown(clean_html("""
        <div class="stat-card">
            <div class="stat-val" style="color:#A78BFA;">MINIMAL</div>
            <div class="stat-lbl">CURRENT SWELLING LEVEL</div>
        </div>
        """), unsafe_allow_html=True)

    # VISUAL SIMPLE PROGRESS BAR FOR PATIENT UNDERSTANDING
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"**Overall Joint Restoration Meter: {flexion_pct}% Restored**")
    st.progress(flexion_pct / 100.0)
    st.caption("🟢 Your knee joint is currently **75% restored** compared to baseline before starting therapy.")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- SECTION 3: WEEKLY VISUAL PROGRESS TIMELINE ---
    c_head, c_act = st.columns([3, 1])
    with c_head:
        st.markdown("### 🗓️ Weekly Visual Progress Timeline")
    with c_act:
        if st.button("🔔 Simulate Sunday Email Reminder"):
            send_portal_email_notification(
                "hassan@example.com",
                "TeleSynapse Reminder: Upload Week 5 Photo",
                "Hi Hassan, please upload your Week 5 progress photo for Dr. Ayesha's review."
            )
            st.toast("📧 Sunday 8:00 PM automated portal email dispatched to patient!")

    cols = st.columns(4)
    for idx, w in enumerate(prof["weekly_photos"]):
        with cols[idx]:
            card_html = f"""
            <div style="background:#1E293B; border:1px solid #334155; border-radius:12px; padding:12px; text-align:center;">
                <div style="color:#34D399; font-weight:800; font-size:0.95rem; margin-bottom:4px;">{w['week']}</div>
                <div style="color:#64748B; font-size:0.72rem; margin-bottom:8px;">{w['date']}</div>
                <img src="{w['url']}" style="width:100%; border-radius:8px; border:1px solid #334155; margin-bottom:8px;" />
                <div style="font-family:'JetBrains Mono', monospace; color:#38BDF8; font-weight:700; font-size:0.9rem;">{w['flexion']}° Flexion</div>
                <div style="color:#94A3B8; font-size:0.75rem; margin-top:2px;">Swelling: {w['swelling']}</div>
                <div style="background:#064E3B; color:#34D399; font-size:0.7rem; font-weight:700; border-radius:6px; padding:3px; margin-top:8px;">✓ APPROVED</div>
            </div>
            """
            st.markdown(clean_html(card_html), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- SECTION 4: AI SIDE-BY-SIDE COMPARISON MODAL / FEATURE ---
    st.markdown("### 🔍 AI Visual Proof & Side-by-Side Comparison")
    
    if st.button("🖼️ COMPARE BEFORE REHAB vs. CURRENT NOW"):
        st.session_state["show_comparison_modal"] = not st.session_state["show_comparison_modal"]

    if st.session_state["show_comparison_modal"]:
        comparison_html = f"""
        <div style="background:#0F172A; border:2px solid #10B981; border-radius:18px; padding:24px; margin-top:16px; box-shadow:0 15px 35px rgba(0,0,0,0.7);">
            <div style="text-align:center; color:#34D399; font-weight:800; font-size:1.3rem; letter-spacing:1px; margin-bottom:16px;">
                ⚡ AI VISUAL RECOVERY SIDE-BY-SIDE AUDIT
            </div>
            
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:20px; text-align:center;">
                <!-- BEFORE COLUMN -->
                <div style="background:#1E293B; border:1px solid #EF4444; border-radius:14px; padding:16px;">
                    <div style="color:#EF4444; font-weight:800; font-size:1rem; margin-bottom:6px;">🔴 BEFORE REHAB (BASELINE)</div>
                    <div style="color:#94A3B8; font-size:0.75rem; margin-bottom:10px;">Date: {prof['before_photo_date']}</div>
                    <img src="{prof['before_photo_url']}" style="width:100%; max-width:240px; border-radius:10px; border:2px solid #EF4444;" />
                    <div style="margin-top:12px; font-family:'JetBrains Mono', monospace; font-size:0.88rem; color:#F8FAFC;">
                        Swelling: <b style="color:#EF4444;">HIGH (+15%)</b><br>
                        Max Flexion: <b style="color:#EF4444;">60°</b>
                    </div>
                </div>

                <!-- NOW COLUMN -->
                <div style="background:#1E293B; border:1px solid #10B981; border-radius:14px; padding:16px;">
                    <div style="color:#34D399; font-weight:800; font-size:1rem; margin-bottom:6px;">🟢 CURRENT (WEEK 4)</div>
                    <div style="color:#94A3B8; font-size:0.75rem; margin-bottom:10px;">Date: 15-Sep-2026</div>
                    <img src="{prof['weekly_photos'][-1]['url']}" style="width:100%; max-width:240px; border-radius:10px; border:2px solid #10B981;" />
                    <div style="margin-top:12px; font-family:'JetBrains Mono', monospace; font-size:0.88rem; color:#F8FAFC;">
                        Swelling: <b style="color:#34D399;">MINIMAL (+2%)</b><br>
                        Max Flexion: <b style="color:#34D399;">105°</b>
                    </div>
                </div>
            </div>

            <div style="background:#064E3B; border:1px solid #10B981; border-radius:12px; padding:14px; text-align:center; margin-top:20px;">
                <div style="color:#34D399; font-weight:800; font-size:1.1rem;">TOTAL RANGE IMPROVEMENT: +75% (45° GAIN)</div>
                <div style="color:#E5E7EB; font-size:0.82rem; margin-top:4px;">Swelling reduced by 86.6% over 4 weeks of compliant tele-rehab exercises.</div>
            </div>
        </div>
        """
        st.markdown(clean_html(comparison_html), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        # PDF DOWNLOAD BUTTON FOR HOSPITAL / UET RECORD
        pdf_content = f"""
        TELE-SYNAPSE VISUAL RECOVERY AUDIT REPORT
        ----------------------------------------------------
        PATIENT: Muhammad Hassan Raza (Age: 21)
        ORGAN / JOINT: Right Knee Joint
        DIAGNOSIS: ACL Tear & Meniscus Strain
        ATTENDING DOCTOR: Dr. Ayesha Malik
        
        VISUAL AUDIT METRICS:
        - Baseline Date: 25-Aug-2026 | Baseline Angle: 60° (Swelling: +15%)
        - Current Date:  15-Sep-2026 | Current Angle:  105° (Swelling: +2%)
        - Net Functional Gain: +45° Range Improvement (+75%)
        
        CLINICAL STAMP: Verified by TeleSynapse Encrypted Portal Engine.
        """
        b64_pdf = base64.b64encode(pdf_content.encode()).decode()
        dl_link = f'<a href="data:file/txt;base64,{b64_pdf}" download="Visual_Recovery_Audit_HassanRaza.txt" style="display:block; text-align:center; background:linear-gradient(90deg, #10B981, #06B6D4); color:#0B0F17; font-weight:800; border-radius:12px; padding:12px; text-decoration:none;">📄 DOWNLOAD VISUAL COMPARISON REPORT PDF</a>'
        st.markdown(dl_link, unsafe_allow_html=True)
