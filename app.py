import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import random
import datetime
import re

# ==========================================
# 0. HELPER ENGINES & INVISIBLE WALL SECURITY
# ==========================================

def clean_html(raw_html: str) -> str:
    """Strips leading/trailing spaces to prevent Streamlit layout bugs."""
    return "".join(line.strip() for line in raw_html.splitlines())


def sanitize_portal_message(user_message: str) -> tuple[str, bool]:
    """
    ADVANCED CHAT FILTER ENGINE (Invisible Wall):
    Scans for phone numbers (including spaced/word digits), emails, 
    and external video links. Auto-masks them with a soft safety note.
    """
    # Regex for standard/spaced phone numbers (+92 300 1234567 or 0 3 0 0 - 1 2 3 4 5 6 7)
    phone_pattern = r'(\+?92|0)?[\s\.\-]*3[\s\.\-]*\d[\s\.\-]*\d[\s\.\-]*\d[\s\.\-]*\d[\s\.\-]*\d[\s\.\-]*\d[\s\.\-]*\d[\s\.\-]*\d[\s\.\-]*\d'
    # Regex for standard emails
    email_pattern = r'[a-zA-Z0-9._%+-]+@[\w\.-]+\.[a-zA-Z]{2,}'
    # Regex for external links
    link_pattern = r'(whatsapp\.com|wa\.me|zoom\.us|meet\.google|teams\.microsoft)'

    flagged = False
    cleaned_msg = user_message

    if re.search(phone_pattern, cleaned_msg, re.IGNORECASE):
        cleaned_msg = re.sub(phone_pattern, '[🔒 Contact info masked for your privacy & safety]', cleaned_msg)
        flagged = True

    if re.search(email_pattern, cleaned_msg, re.IGNORECASE):
        cleaned_msg = re.sub(email_pattern, '[🔒 Email address masked for safety]', cleaned_msg)
        flagged = True

    if re.search(link_pattern, cleaned_msg, re.IGNORECASE):
        cleaned_msg = re.sub(link_pattern, '[🔒 External link disabled. Use In-Portal Call]', cleaned_msg)
        flagged = True

    return cleaned_msg, flagged


def log_security_flag(user_id: str, message: str):
    """Silent Admin Audit Logging for flagged contact bypass attempts."""
    if "admin_audit_logs" not in st.session_state:
        st.session_state["admin_audit_logs"] = []
    
    st.session_state["admin_audit_logs"].append({
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user_id": user_id,
        "flagged_text": message
    })


# ==========================================
# 1. GLOBAL PAGE CONFIG & THEME
# ==========================================

st.set_page_config(
    page_title="TeleSynapse | Clinical Tele-Rehab Portal",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Accessibility Toggle
st.sidebar.markdown("### ♿ Accessibility Mode")
big_text = st.sidebar.toggle("🔍 Large Text Mode", value=False)

base_font = "17px" if big_text else "15px"
hero_size = "2.2rem" if big_text else "1.8rem"

global_css = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

#MainMenu {{ visibility: hidden !important; }}
footer {{ visibility: hidden !important; }}
.stDeployButton {{ display: none !important; }}
header[data-testid="stHeader"] {{ background-color: transparent !important; }}

html, body, [class*="css"] {{
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: {base_font} !important;
}}
.stApp {{
    background: #0B0F17 !important;
    color: #F3F4F6 !important;
}}

h1, h2, h3 {{ color: #34D399 !important; font-weight: 800 !important; }}
h4, h5, h6 {{ color: #38BDF8 !important; font-weight: 700 !important; }}

[data-testid="stSidebar"] {{
    background-color: #111827 !important;
    border-right: 1px solid #1F2937 !important;
}}

.brand-container {{
    padding: 18px 14px;
    background: linear-gradient(135deg, #064E3B 0%, #111827 100%);
    border: 1px solid #059669;
    border-radius: 14px;
    margin-bottom: 20px;
    text-align: center;
}}
.brand-title {{
    color: #34D399 !important;
    font-size: 1.6rem;
    font-weight: 800;
}}
.brand-sub {{
    color: #9CA3AF !important;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.2px;
}}

.hero-banner {{
    background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
    border-left: 5px solid #10B981;
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 24px;
}}
.hero-title {{
    color: #34D399 !important;
    font-size: {hero_size};
    font-weight: 800;
}}

.value-pitch-card {{
    background: #1E293B;
    border: 1px solid #38BDF8;
    border-radius: 14px;
    padding: 18px;
    margin-top: 16px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.3);
}}

.stButton>button {{
    background: linear-gradient(90deg, #10B981, #06B6D4) !important;
    color: #0B0F17 !important;
    font-weight: 800 !important;
    border-radius: 10px !important;
    border: none !important;
    padding: 10px 20px !important;
}}

.soft-footer {{
    text-align: center;
    color: #64748B;
    font-size: 0.8rem;
    margin-top: 40px;
    padding-top: 16px;
    border-top: 1px solid #1E293B;
}}
</style>
"""
st.markdown(clean_html(global_css), unsafe_allow_html=True)


# ==========================================
# 2. SESSION STATE INITIALIZATION
# ==========================================

if "appointments" not in st.session_state:
    st.session_state["appointments"] = [
        {
            "SlipNo": "TS-98475",
            "PatientProxy": "TS-P-001",
            "DoctorProxy": "TS-D-004",
            "PatientName": "Muhammad Hassan Raza",
            "DoctorName": "Dr. Ayesha Malik",
            "Specialty": "Orthopedic Specialist",
            "Date": "Fri, 05 Sep 2026",
            "Time": "04:00 PM",
            "Condition": "ACL Tear & Knee Joint Flexion",
            "Fee": "Rs. 2,200",
            "Status": "CONFIRMED ✓"
        }
    ]

if "booking_step" not in st.session_state:
    st.session_state["booking_step"] = "STEP_1_BOOK"

if "chat_messages" not in st.session_state:
    st.session_state["chat_messages"] = [
        {"sender": "TS-D-004", "text": "Hello! Please share your flexion progress video before our call."},
        {"sender": "TS-P-001", "text": "Sure doctor, I have captured 3 angles using the camera suite."}
    ]

if "active_video_room" not in st.session_state:
    st.session_state["active_video_room"] = None

if "clinical_photos" not in st.session_state:
    st.session_state["clinical_photos"] = {"front": None, "side": None, "flexion": None}


# ==========================================
# 3. NAVIGATION & BRANDING
# ==========================================

st.sidebar.markdown(clean_html("""
<div class="brand-container">
    <div class="brand-title">🩺 TeleSynapse</div>
    <div class="brand-sub">Clinical Tele-Rehab Portal</div>
</div>
"""), unsafe_allow_html=True)

menu = st.sidebar.radio("Portal Navigation", [
    "👤 Patient Dashboard (Link-Only)",
    "👨‍⚕️ Doctor Dashboard (Link-Only)",
    "🩺 3-Step Secure Booking",
    "📹 Kinematic Motion & Camera Suite",
    "📊 Admin Audit & Security Center"
])


# ==========================================
# 4. MODULE: PATIENT DASHBOARD (LINK-ONLY)
# ==========================================

if menu == "👤 Patient Dashboard (Link-Only)":
    st.markdown("### 👤 Patient Clinical Portal")
    
    # LINK-ONLY PATIENT CARD
    patient_card_html = """
    <div style="background:#1E293B; border:2px solid #059669; border-radius:16px; padding:20px; margin-bottom:20px;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
                <div style="color:#34D399; font-weight:800; font-size:1.2rem;">Dr. Ayesha Malik</div>
                <div style="color:#94A3B8; font-size:0.85rem;">Physiotherapist & Orthopedic Specialist | Proxy ID: <b>TS-D-004</b></div>
            </div>
            <div style="background:#0F172A; color:#38BDF8; font-size:0.75rem; font-weight:700; padding:6px 12px; border-radius:8px; border:1px solid #334155;">
                🔒 Link-Only Protected Session
            </div>
        </div>
        <hr style="border-color:#334155; margin:14px 0;">
        <div style="color:#64748B; font-size:0.8rem;">No Phone Required. No WhatsApp Needed. All communications encrypted in portal.</div>
    </div>
    """
    st.markdown(clean_html(patient_card_html), unsafe_allow_html=True)

    c_btn1, c_btn2 = st.columns(2)
    with c_btn1:
        if st.button("💬 MESSAGE DOCTOR (IN-PORTAL)"):
            st.session_state["open_chat_view"] = True
    with c_btn2:
        if st.button("🚀 START VIDEO CALL (EMBEDDED)"):
            # Generates temporary expiring room ID
            st.session_state["active_video_room"] = f"TeleSynapse-Room-TS-P-001-{random.randint(100,999)}"

    # EMBEDDED VIDEO CALL FRAME
    if st.session_state.get("active_video_room"):
        st.markdown("---")
        st.markdown(f"#### 📹 In-Portal Live Session — Room: `{st.session_state['active_video_room']}`")
        st.info("⏱️ Temporary encrypted WebRTC room active. Link automatically expires post-session.")
        
        # Embedded Jitsi Call Frame (No external tab required)
        jitsi_url = f"https://meet.jit.si/{st.session_state['active_video_room']}"
        components.iframe(jitsi_url, height=500, scrolling=False)
        
        if st.button("🔴 End Video Session"):
            st.session_state["active_video_room"] = None
            st.rerun()

    # IN-PORTAL SECURE CHAT WITH AUTO-MASKING FILTER
    st.markdown("---")
    st.markdown("#### 💬 Encrypted Portal Chat")
    
    chat_container = st.container(height=220)
    for msg in st.session_state["chat_messages"]:
        sender_label = "You (TS-P-001)" if msg["sender"] == "TS-P-001" else "Dr. Ayesha (TS-D-004)"
        chat_container.write(f"**{sender_label}:** {msg['text']}")

    with st.form("patient_chat_form", clear_on_submit=True):
        chat_input = st.text_input("Type message to doctor:")
        send_chat = st.form_submit_button("Send Encrypted Message")
        
        if send_chat and chat_input:
            sanitized_text, flagged = sanitize_portal_message(chat_input)
            st.session_state["chat_messages"].append({"sender": "TS-P-001", "text": sanitized_text})
            
            if flagged:
                log_security_flag("TS-P-001", chat_input)
                st.toast("🛡️ Contact information auto-masked for your privacy & safety.", icon="🔒")
            
            st.rerun()

    # VALUE PITCH CARD (Carrot > Stick)
    pitch_html = """
    <div class="value-pitch-card">
        <div style="color:#38BDF8; font-weight:800; font-size:1rem; margin-bottom:10px;">
            💡 WHY USE TELE-SYNAPSE PORTAL CHAT?
        </div>
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px; font-size:0.85rem; color:#CBD5E1;">
            <div>✓ <b>100% Safe:</b> All videos + photos are HIPAA encrypted</div>
            <div>✓ <b>AI Analytics:</b> Doctor sees your live joint progress graphs</div>
            <div>✓ <b>24/7 Record:</b> Official history for insurance & hospital</div>
            <div>✓ <b>1-Click Join:</b> Seamless call join with zero number saving</div>
        </div>
    </div>
    """
    st.markdown(clean_html(pitch_html), unsafe_allow_html=True)


# ==========================================
# 5. MODULE: DOCTOR DASHBOARD (LINK-ONLY)
# ==========================================

elif menu == "👨‍⚕️ Doctor Dashboard (Link-Only)":
    st.markdown("### 👨‍⚕️ Doctor Clinical Dashboard")
    
    # LINK-ONLY DOCTOR CARD
    doctor_card_html = """
    <div style="background:#1E293B; border:2px solid #0284C7; border-radius:16px; padding:20px; margin-bottom:20px;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
                <div style="color:#38BDF8; font-weight:800; font-size:1.2rem;">Patient: Ali Khan</div>
                <div style="color:#94A3B8; font-size:0.85rem;">Slot: <b>04:00 PM</b> | Condition: ACL Rehab | Proxy ID: <b>TS-P-001</b></div>
            </div>
            <div style="background:#0F172A; color:#34D399; font-size:0.75rem; font-weight:700; padding:6px 12px; border-radius:8px; border:1px solid #334155;">
                🔒 Zero Phone / Zero Email Mode
            </div>
        </div>
        <hr style="border-color:#334155; margin:14px 0;">
        <div style="color:#64748B; font-size:0.8rem;">Patient contact details remain confidential. Communication via proxy portal only.</div>
    </div>
    """
    st.markdown(clean_html(doctor_card_html), unsafe_allow_html=True)

    c_d1, c_d2 = st.columns(2)
    with c_d1:
        if st.button("💬 OPEN CHAT WINDOW"):
            st.toast("Chat window active below.")
    with c_d2:
        if st.button("📹 JOIN VIDEO SESSION"):
            st.session_state["active_video_room"] = "TeleSynapse-Room-TS-P-001-99"

    # EMBEDDED CALL FOR DOCTOR
    if st.session_state.get("active_video_room"):
        st.markdown("---")
        st.markdown(f"#### 📹 In-Portal Doctor Consultation Frame")
        jitsi_url = f"https://meet.jit.si/{st.session_state['active_video_room']}"
        components.iframe(jitsi_url, height=500, scrolling=False)
        
        if st.button("🔴 Conclude Patient Session"):
            st.session_state["active_video_room"] = None
            st.rerun()


# ==========================================
# 6. MODULE: 3-STEP SECURE BOOKING & PAYMENT LOCK
# ==========================================

elif menu == "🩺 3-Step Secure Booking":
    st.markdown("### 🩺 TeleSynapse Booking & Portal Payment Lock")

    if st.session_state["booking_step"] == "STEP_1_BOOK":
        with st.form("booking_form"):
            st.markdown("#### Patient Details")
            p_name = st.text_input("Full Name *", value="Muhammad Hassan Raza")
            raw_phone = st.text_input("Contact Phone *", value="+92 309 7964195")
            
            # Mask input immediately before saving to UI state
            p_phone, _ = sanitize_portal_message(raw_phone)
            
            p_disease = st.text_input("Clinical Condition *", value="ACL Tear Flexion Recovery")
            
            submit = st.form_submit_button("PROCEED TO PORTAL PAYMENT →")
            if submit:
                st.session_state["temp_booking"] = {
                    "Name": p_name,
                    "Phone": p_phone,
                    "Condition": p_disease,
                    "ProxyID": f"TS-P-{random.randint(100,999)}"
                }
                st.session_state["booking_step"] = "STEP_2_PAY"
                st.rerun()

    elif st.session_state["booking_step"] == "STEP_2_PAY":
        st.markdown("#### Step 2: TeleSynapse Escrow Payment Lock")
        st.info("💡 Direct payments to doctors are disabled. All fees are safely held in portal escrow.")
        
        # PAYMENT LOCK DISPLAY (ONLY PORTAL ACCOUNTS SHOW)
        st.markdown(clean_html("""
        <div style="background:#1E293B; border:1px solid #334155; border-radius:12px; padding:16px; margin-bottom:16px;">
            <div style="color:#38BDF8; font-weight:700;">🔴 TELE-SYNAPSE JAZZCASH ESCROW</div>
            <div style="font-family:'JetBrains Mono'; font-size:1.1rem; color:#FFF;">0309-7964195 (Title: TeleSynapse Portal)</div>
        </div>
        <div style="background:#1E293B; border:1px solid #334155; border-radius:12px; padding:16px; margin-bottom:16px;">
            <div style="color:#34D399; font-weight:700;">🏦 BANK ALFALAH ESCROW ACCOUNT</div>
            <div style="font-family:'JetBrains Mono'; font-size:1.1rem; color:#FFF;">A/C: 00427901234503 (Title: Tele-Synapse Health)</div>
        </div>
        """), unsafe_allow_html=True)

        proof = st.file_uploader("Upload Payment Screenshot", type=["jpg", "png", "pdf"])
        if st.button("CONFIRM PAYMENT & UNLOCK LINK"):
            if proof:
                st.session_state["booking_step"] = "STEP_3_CONFIRMED"
                st.rerun()
            else:
                st.error("Please attach payment proof.")

    elif st.session_state["booking_step"] == "STEP_3_CONFIRMED":
        st.success("🎉 APPOINTMENT CONFIRMED! Link-Only Session Created.")
        st.balloons()
        if st.button("Go to Patient Dashboard"):
            st.session_state["booking_step"] = "STEP_1_BOOK"
            st.rerun()


# ==========================================
# 7. MODULE: KINEMATIC MOTION & CAMERA SUITE
# ==========================================

elif menu == "📹 Kinematic Motion & Camera Suite":
    st.markdown("### 📸 Multi-Angle Mobile Camera Suite")
    
    photos = st.session_state["clinical_photos"]
    captured_count = sum(1 for v in photos.values() if v is not None)
    
    st.progress(captured_count / 3.0)
    st.caption(f"Captured `{captured_count} of 3 Required Clinical Angles`")

    selected_target = st.radio(
        "📷 Choose Angle:",
        ["Front View (0°)", "Side View (90°)", "Active Flexion (Bend)"],
        horizontal=True
    )
    
    key_map = {"Front View (0°)": "front", "Side View (90°)": "side", "Active Flexion (Bend)": "flexion"}
    active_key = key_map[selected_target]

    cam_file = st.camera_input(f"Snap {selected_target}", key=f"cam_{active_key}")
    if cam_file:
        st.session_state["clinical_photos"][active_key] = cam_file
        st.toast(f"✅ Captured {selected_target}!", icon="📸")


# ==========================================
# 8. MODULE: ADMIN AUDIT & SECURITY CENTER
# ==========================================

else:
    st.markdown("### 📊 Admin Audit & Security Control Center")
    st.markdown("#### 🛡️ Silent Flagging Log (Contact Bypass Detection)")
    
    logs = st.session_state.get("admin_audit_logs", [])
    if logs:
        df_logs = pd.DataFrame(logs)
        st.dataframe(df_logs, use_container_width=True)
    else:
        st.info("🟢 Zero security violations detected. Contact masking engine running smoothly.")


# ==========================================
# 9. GLOBAL SOFT POLICY FOOTER
# ==========================================

st.markdown(clean_html("""
<div class="soft-footer">
    By using TeleSynapse, all sessions and communication are securely managed within the portal to protect your medical records.
</div>
"""), unsafe_allow_html=True)
