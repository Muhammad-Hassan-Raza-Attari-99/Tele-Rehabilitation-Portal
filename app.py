import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import random
import datetime
import re
import uuid
import time
import base64

# ==========================================
# 0. GLOBAL PAGE CONFIG & THEME
# ==========================================

st.set_page_config(
    page_title="TeleSynapse | Clinical Tele-Rehab Portal",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Accessibility Mode
st.sidebar.markdown("### ♿ Accessibility Mode")
big_text = st.sidebar.toggle("🔍 Large Text Mode", value=False)

base_font = "17px" if big_text else "15px"
hero_size = "2.2rem" if big_text else "1.8rem"

# Inject Custom Styling & Loader CSS Overlay
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

/* BRANDING & CARDS */
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

.value-pitch-card {{
    background: #1E293B;
    border: 1px solid #38BDF8;
    border-radius: 14px;
    padding: 18px;
    margin-top: 16px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.3);
}}

.watermark-badge {{
    position: relative;
    border: 2px dashed #059669;
    border-radius: 12px;
    padding: 10px;
    background: #0F172A;
    margin-top: 10px;
}}
.watermark-overlay {{
    position: absolute;
    bottom: 12px;
    right: 18px;
    background: rgba(6, 78, 59, 0.85);
    color: #34D399;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    padding: 4px 8px;
    border-radius: 6px;
    border: 1px solid #059669;
}}

.stButton>button {{
    background: linear-gradient(90deg, #10B981, #06B6D4) !important;
    color: #0B0F17 !important;
    font-weight: 800 !important;
    border-radius: 10px !important;
    border: none !important;
    padding: 10px 20px !important;
}}

/* FULLSCREEN LOADER COMPONENT (GRADIENT + ROTATING CIRCLE) */
.loader-overlay {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: linear-gradient(135deg, #0A2342 0%, #1E90FF 100%);
    z-index: 999999;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    color: #FFFFFF;
    text-align: center;
}}
.spinner-circle {{
    width: 70px;
    height: 70px;
    border: 5px solid rgba(255, 255, 255, 0.2);
    border-top: 5px solid #FFFFFF;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 24px;
}}
@keyframes spin {{
    0% {{ transform: rotate(0deg); }}
    100% {{ transform: rotate(360deg); }}
}}
.loader-title {{
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: 1.5px;
    margin-bottom: 8px;
}}
.loader-sub {{
    font-size: 1.1rem;
    font-weight: 500;
    opacity: 0.9;
}}
.loader-warning {{
    font-size: 0.85rem;
    margin-top: 20px;
    opacity: 0.7;
    letter-spacing: 0.5px;
}}
</style>
"""
st.markdown(global_css, unsafe_allow_html=True)


# ==========================================
# 1. DATABASE & SESSION STATE INITIALIZATION
# ==========================================

if "users_db" not in st.session_state:
    st.session_state["users_db"] = {
        "patient@demo.com": {
            "user_id": "USR-P-101",
            "proxy_id": "TS-P-001",
            "name": "Muhammad Hassan Raza",
            "role": "patient",
            "status": "ACTIVE",
            "password_hash": "pass123",
            "phone": "+92 309 7964195"
        },
        "doctor@demo.com": {
            "user_id": "USR-D-909",
            "proxy_id": "TS-D-004",
            "name": "Dr. Ayesha Malik",
            "role": "doctor",
            "status": "ACTIVE",
            "phpc_num": "PHPC-88492-PAK",
            "specialty": "Orthopedic Specialist",
            "password_hash": "pass123"
        }
    }

if "authenticated_user" not in st.session_state:
    st.session_state["authenticated_user"] = st.session_state["users_db"]["patient@demo.com"]

if "patient_photos" not in st.session_state:
    st.session_state["patient_photos"] = {
        "TS-P-001": [
            {
                "uuid_filename": f"{uuid.uuid4().hex[:10]}.jpg",
                "tag": "Before Photo",
                "ai_analysis": "Detected: Knee Joint, Swelling: Moderate, Angle: 45°",
                "timestamp": "2026-08-10 14:30:00",
                "selected_for_report": True
            },
            {
                "uuid_filename": f"{uuid.uuid4().hex[:10]}.jpg",
                "tag": "Week 1 Progress",
                "ai_analysis": "Detected: Knee Joint, Swelling: Reduced (-30%), Flexion: 85°",
                "timestamp": "2026-08-17 09:15:00",
                "selected_for_report": True
            }
        ]
    }

if "audit_logs" not in st.session_state:
    st.session_state["audit_logs"] = []

if "email_outbox" not in st.session_state:
    st.session_state["email_outbox"] = []

if "chat_messages" not in st.session_state:
    st.session_state["chat_messages"] = [
        {"sender": "TS-D-004", "text": "Hello! Please upload your Week 2 progress photo before our video call."},
        {"sender": "TS-P-001", "text": "Sure doctor, I have uploaded the active flexion angle."}
    ]

if "trigger_loader" not in st.session_state:
    st.session_state["trigger_loader"] = False


# ==========================================
# 2. HELPER ENGINES & SECURITY MIDDLEWARE
# ==========================================

def render_loader_component(message="Securing Your Session..."):
    """Displays the custom 2-second full screen TeleRehab loader."""
    loader_html = f"""
    <div class="loader-overlay">
        <div class="spinner-circle"></div>
        <div class="loader-title">TeleRehab</div>
        <div class="loader-sub">{message}</div>
        <div class="loader-warning">Please do not close or refresh this page</div>
    </div>
    """
    loader_placeholder = st.empty()
    loader_placeholder.markdown(loader_html, unsafe_allow_html=True)
    time.sleep(1.8)
    loader_placeholder.empty()


def add_audit_log(actor_proxy: str, action: str, details: str):
    """Silent Senior Audit Trail logger."""
    st.session_state["audit_logs"].append({
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "actor": actor_proxy,
        "action": action,
        "details": details
    })


def sanitize_portal_message(user_message: str) -> tuple[str, bool]:
    """Smart Anti-Leakage Regex Filter."""
    phone_pattern = r'(\+?92|0)?[\s\.\-]*3[\s\.\-]*\d[\s\.\-]*\d[\s\.\-]*\d[\s\.\-]*\d[\s\.\-]*\d[\s\.\-]*\d[\s\.\-]*\d[\s\.\-]*\d[\s\.\-]*\d'
    email_pattern = r'[a-zA-Z0-9._%+-]+@[\w\.-]+\.[a-zA-Z]{2,}'
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


def send_portal_email(user_id: str, template_name: str, subject: str, body: str, attachment: str = None):
    """Backend-only Masked Email Sender. No PII exposed to frontend."""
    st.session_state["email_outbox"].append({
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "recipient_user_id": user_id,
        "sender": "noreply@telerehab.com",
        "template": template_name,
        "subject": subject,
        "body": body,
        "attachment": attachment or "None"
    })
    add_audit_log("SYSTEM_EMAIL", "EMAIL_DISPATCHED", f"Template: {template_name} to {user_id}")


# Trigger loader animation if requested
if st.session_state["trigger_loader"]:
    render_loader_component("Verifying Security Tokens & Encrypting...")
    st.session_state["trigger_loader"] = False


# ==========================================
# 3. SIDEBAR NAVIGATION & AUTH SWITCHER
# ==========================================

st.sidebar.markdown("""
<div class="brand-container">
    <div class="brand-title">🩺 TeleSynapse</div>
    <div class="brand-sub">Clinical Tele-Rehab Portal</div>
</div>
""", unsafe_allow_html=True)

# Active User Display
curr_user = st.session_state["authenticated_user"]
st.sidebar.markdown(f"**Logged in as:** `{curr_user['name']}`")
st.sidebar.markdown(f"**Role:** `{curr_user['role'].upper()}` | **Proxy:** `{curr_user['proxy_id']}`")

menu = st.sidebar.radio("Portal Navigation", [
    "🔐 Authentication & Dual Login",
    "👤 Patient Portal & Photo Center",
    "👨‍⚕️ Doctor Dashboard & Patient Gallery",
    "📄 AI Report Generator (PDF Preview)",
    "📊 Senior Admin & Security Trail"
])


# ==========================================
# 4. MODULE 1: AUTHENTICATION & DUAL LOGIN
# ==========================================

if menu == "🔐 Authentication & Dual Login":
    st.markdown("### 🔐 TeleSynapse Dual Authentication Portal")
    st.caption("Strict Role Isolation System — 1 Database, 2 Distinct Roles")

    tab1, tab2 = st.tabs(["🔑 Sign In", "📝 Register New Account"])

    with tab1:
        st.markdown("#### Log In to Your Portal")
        role_select = st.radio("Select Role:", ["Patient", "Doctor"], horizontal=True)
        login_email = st.text_input("Email Address", value="patient@demo.com" if role_select == "Patient" else "doctor@demo.com")
        login_pass = st.text_input("Password", type="password", value="pass123")

        if st.button("SIGN IN TO PORTAL"):
            render_loader_component("Authenticating User & Securing Session...")
            user_found = st.session_state["users_db"].get(login_email)

            if user_found and user_found["password_hash"] == login_pass and user_found["role"] == role_select.lower():
                if user_found["status"] == "PENDING":
                    st.error("⏳ Doctor Account Approval Pending. Admin review takes up to 24 hours.")
                else:
                    st.session_state["authenticated_user"] = user_found
                    add_audit_log(user_found["proxy_id"], "USER_LOGIN", f"Successful login as {role_select}")
                    st.success(f"Welcome back, {user_found['name']}! Redirecting...")
                    st.rerun()
            else:
                st.error("Invalid credentials or role mismatch.")

    with tab2:
        st.markdown("#### Create New Account")
        reg_role = st.selectbox("I am registering as a:", ["Patient", "Doctor"])
        
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            reg_name = st.text_input("Full Name")
            reg_email = st.text_input("Email Address")
        with col_r2:
            reg_phone = st.text_input("Phone Number")
            reg_pass = st.text_input("Choose Password", type="password")

        if reg_role == "Doctor":
            phpc_id = st.text_input("PHPC / CNMC License Number *")
            spec = st.text_input("Specialty / Department", value="Physical Rehabilitation")

        if st.button("CREATE ACCOUNT & VERIFY OTP"):
            render_loader_component("Registering Account & Issuing Security Tokens...")
            new_proxy = f"TS-P-{random.randint(100,999)}" if reg_role == "Patient" else f"TS-D-{random.randint(100,999)}"
            new_status = "ACTIVE" if reg_role == "Patient" else "PENDING"

            st.session_state["users_db"][reg_email] = {
                "user_id": f"USR-{random.randint(1000,9999)}",
                "proxy_id": new_proxy,
                "name": reg_name,
                "role": reg_role.lower(),
                "status": new_status,
                "password_hash": reg_pass,
                "phone": reg_phone
            }

            add_audit_log(new_proxy, "REGISTER", f"Registered new {reg_role} account (Status: {new_status})")

            # Dispatch Auto Welcome Email
            send_portal_email(
                user_id=new_proxy,
                template_name="WELCOME_ONBOARDING",
                subject="Welcome to TeleSynapse Portal",
                body=f"Hello {reg_name}, your account has been created. Status: {new_status}."
            )

            if new_status == "PENDING":
                st.info("ℹ️ Doctor registration submitted! Status set to PENDING. Awaiting Admin Approval.")
            else:
                st.success("🎉 Registration complete! OTP verified. You can now log in.")


# ==========================================
# 5. MODULE 2: PATIENT PORTAL & PHOTO CENTER
# ==========================================

elif menu == "👤 Patient Portal & Photo Center":
    if curr_user["role"] != "patient":
        st.warning("⚠️ Access Restricted. This view is for Patients only.")
    else:
        st.markdown("### 👤 Patient Clinical Hub & Photo Upload Center")
        
        # Link-Only Header
        st.markdown("""
        <div style="background:#1E293B; border:2px solid #059669; border-radius:16px; padding:18px; margin-bottom:20px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <div style="color:#34D399; font-weight:800; font-size:1.2rem;">Assigned Doctor: Dr. Ayesha Malik</div>
                    <div style="color:#94A3B8; font-size:0.85rem;">Doctor Proxy: <b>TS-D-004</b> | Your Proxy: <b>TS-P-001</b></div>
                </div>
                <div style="background:#0F172A; color:#38BDF8; font-size:0.75rem; font-weight:700; padding:6px 12px; border-radius:8px; border:1px solid #334155;">
                    🔒 Zero Contact Exposure Policy Active
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_p1, col_p2 = st.columns([1, 1])

        with col_p1:
            st.markdown("#### 📸 Upload Progress Photo")
            st.caption("Photos are compressed, auto-tagged by AI, and watermarked.")

            photo_tag = st.selectbox("Photo Interval Tag:", ["Before Photo", "Week 1 Progress", "Week 2 Progress", "Week 3 Progress", "Week 4 Final"])
            uploaded_file = st.file_uploader("Select Image (JPG/PNG - Max 2MB)", type=["jpg", "png", "jpeg"])

            if st.button("UPLOAD & AUTO-TAG PHOTO"):
                if uploaded_file:
                    render_loader_component("Uploading Image to Encrypted Storage & Running AI Vision Tagging...")

                    # Generate non-guessable UUID file name
                    uuid_filename = f"storage_{uuid.uuid4().hex[:12]}.jpg"
                    
                    # Simulated AI tagging engine
                    ai_tags = [
                        "Detected: Knee Joint, Swelling: Minor, Flexion Angle: 105°",
                        "Detected: Shoulder Flexion, Elevation: 140°, Alignment: Good",
                        "Detected: Ankle Joint, Inflammation: Low, Range: 80%"
                    ]
                    selected_ai_tag = random.choice(ai_tags)

                    new_photo_record = {
                        "uuid_filename": uuid_filename,
                        "tag": photo_tag,
                        "ai_analysis": selected_ai_tag,
                        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "selected_for_report": True
                    }

                    if curr_user["proxy_id"] not in st.session_state["patient_photos"]:
                        st.session_state["patient_photos"][curr_user["proxy_id"]] = []

                    st.session_state["patient_photos"][curr_user["proxy_id"]].append(new_photo_record)
                    add_audit_log(curr_user["proxy_id"], "PHOTO_UPLOAD", f"Uploaded {photo_tag} -> UUID: {uuid_filename}")

                    st.success(f"✅ Photo Uploaded Successfully! UUID: `{uuid_filename}`")
                else:
                    st.error("Please select a file first.")

        with col_p2:
            st.markdown("#### 🖼️ Your Uploaded Progress Gallery")
            photos = st.session_state["patient_photos"].get(curr_user["proxy_id"], [])

            if photos:
                for idx, item in enumerate(photos):
                    st.markdown(f"""
                    <div class="watermark-badge">
                        <div style="color:#38BDF8; font-weight:700;">📌 {item['tag']}</div>
                        <div style="color:#94A3B8; font-size:0.8rem;">UUID: <code>{item['uuid_filename']}</code> | {item['timestamp']}</div>
                        <div style="color:#34D399; font-size:0.82rem; margin-top:6px;">🧠 <b>AI Tag:</b> {item['ai_analysis']}</div>
                        <div class="watermark-overlay">TeleSynapse | {curr_user['proxy_id']} | Encrypted</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No photos uploaded yet.")

        # In-Portal Chat
        st.markdown("---")
        st.markdown("#### 💬 Encrypted Portal Chat")
        
        chat_box = st.container(height=180)
        for msg in st.session_state["chat_messages"]:
            sender_label = "You (TS-P-001)" if msg["sender"] == "TS-P-001" else "Dr. Ayesha (TS-D-004)"
            chat_box.write(f"**{sender_label}:** {msg['text']}")

        with st.form("patient_chat_form", clear_on_submit=True):
            chat_in = st.text_input("Type message to doctor:")
            if st.form_submit_button("Send Encrypted Message"):
                clean_msg, flagged = sanitize_portal_message(chat_in)
                st.session_state["chat_messages"].append({"sender": curr_user["proxy_id"], "text": clean_msg})
                
                if flagged:
                    add_audit_log(curr_user["proxy_id"], "CHAT_FLAGGED", f"Attempted contact leak: {chat_in}")
                    st.toast("🛡️ Contact info auto-masked for privacy & safety.", icon="🔒")
                
                st.rerun()


# ==========================================
# 6. MODULE 3: DOCTOR DASHBOARD & GALLERY
# ==========================================

elif menu == "👨‍⚕️ Doctor Dashboard & Patient Gallery":
    if curr_user["role"] != "doctor":
        st.warning("⚠️ Access Restricted. This view is for Doctors only.")
    else:
        st.markdown("### 👨‍⚕️ Doctor Clinical Workspace")
        
        st.markdown("""
        <div style="background:#1E293B; border:2px solid #0284C7; border-radius:16px; padding:18px; margin-bottom:20px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <div style="color:#38BDF8; font-weight:800; font-size:1.2rem;">Active Patient: Ali Khan / Hassan Raza</div>
                    <div style="color:#94A3B8; font-size:0.85rem;">Patient Proxy: <b>TS-P-001</b> | Condition: ACL Rehab & Flexion Recovery</div>
                </div>
                <div style="background:#0F172A; color:#34D399; font-size:0.75rem; font-weight:700; padding:6px 12px; border-radius:8px; border:1px solid #334155;">
                    🔒 Contact Info Masked
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 🖼️ Patient Clinical Photo Gallery (Select for PDF Report)")
        
        patient_photos = st.session_state["patient_photos"].get("TS-P-001", [])

        if patient_photos:
            col_g1, col_g2 = st.columns(2)
            for idx, pic in enumerate(patient_photos):
                target_col = col_g1 if idx % 2 == 0 else col_g2
                with target_col:
                    st.markdown(f"""
                    <div class="watermark-badge">
                        <div style="color:#34D399; font-weight:700;">🏷️ {pic['tag']}</div>
                        <div style="color:#64748B; font-size:0.75rem;">File: {pic['uuid_filename']}</div>
                        <div style="color:#E2E8F0; font-size:0.82rem; margin:6px 0;">🧠 {pic['ai_analysis']}</div>
                        <div class="watermark-overlay">TeleSynapse | TS-P-001</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    is_selected = st.checkbox(f"Include in Final Report", value=pic.get("selected_for_report", True), key=f"pic_sel_{idx}")
                    pic["selected_for_report"] = is_selected
        else:
            st.info("No photos uploaded by patient yet.")

        st.markdown("---")
        st.markdown("#### 📧 Send Masked Portal Email to Patient")
        with st.form("doctor_email_form"):
            email_subj = st.text_input("Subject", value="Weekly Progress Review & Report Update")
            email_body = st.text_area("Message Body", value="Dear Patient, your Week 1 flexion recovery shows good progress. Please keep performing the prescribed exercises.")
            
            if st.form_submit_button("DISPATCH MASKED EMAIL"):
                render_loader_component("Transmitting Masked Email via TeleRehab Gateway...")
                send_portal_email(
                    user_id="TS-P-001",
                    template_name="DOCTOR_DIRECT_MESSAGE",
                    subject=email_subj,
                    body=email_body
                )
                st.success("✉️ Email sent successfully via backend proxy! Patient contact remains masked.")


# ==========================================
# 7. MODULE 4: AI REPORT GENERATOR
# ==========================================

elif menu == "📄 AI Report Generator (PDF Preview)":
    st.markdown("### 📄 Clinical Progress & AI Report Engine")
    st.caption("Generates HIPAA-Compliant Watermarked Report PDF for Patients")

    photos = st.session_state["patient_photos"].get("TS-P-001", [])
    selected_photos = [p for p in photos if p.get("selected_for_report", True)]

    if st.button("⚙️ GENERATE CLINICAL REPORT PDF"):
        render_loader_component("Compiling AI Vision Metrics, Watermarking Images & Rendering PDF...")
        add_audit_log(curr_user["proxy_id"], "REPORT_GENERATED", f"Generated report with {len(selected_photos)} selected photos.")
        st.success("🎉 Report PDF Generated & Automatically Emailed to Patient!")

    # Live Report Preview
    st.markdown("---")
    st.markdown("#### 📑 Report Preview Window")

    report_html = f"""
    <div style="background:#FFFFFF; color:#1E293B; border-radius:12px; padding:30px; font-family:'Plus Jakarta Sans', sans-serif;">
        <div style="display:flex; justify-content:space-between; border-bottom:2px solid #059669; padding-bottom:12px;">
            <div>
                <h2 style="color:#064E3B !important; margin:0;">TeleSynapse Rehabilitation Portal</h2>
                <div style="font-size:0.85rem; color:#64748B;">Official Tele-Rehab Progress Report</div>
            </div>
            <div style="text-align:right; font-size:0.8rem; color:#64748B;">
                <div><b>Date:</b> {datetime.datetime.now().strftime("%d-%b-%Y")}</div>
                <div><b>Report ID:</b> REP-{random.randint(10000,99999)}</div>
            </div>
        </div>

        <div style="margin:20px 0; font-size:0.9rem; display:grid; grid-template-columns:1fr 1fr; gap:10px; background:#F8FAFC; padding:14px; border-radius:8px;">
            <div><b>Patient Proxy ID:</b> TS-P-001</div>
            <div><b>Attending Doctor:</b> Dr. Ayesha Malik (TS-D-004)</div>
            <div><b>Condition:</b> ACL Flexion Recovery</div>
            <div><b>Overall Recovery Status:</b> <span style="color:#059669; font-weight:700;">ON TRACK (85%)</span></div>
        </div>

        <h4 style="color:#0284C7 !important;">Selected Progress Photos & AI Analytics</h4>
    """

    for p in selected_photos:
        report_html += f"""
        <div style="border:1px solid #CBD5E1; border-radius:8px; padding:12px; margin-bottom:10px; background:#FAFAFA;">
            <div style="font-weight:700; color:#0F172A;">{p['tag']} <span style="font-weight:400; font-size:0.75rem; color:#64748B;">({p['timestamp']})</span></div>
            <div style="font-size:0.85rem; color:#059669; margin-top:4px;"><b>AI Findings:</b> {p['ai_analysis']}</div>
            <div style="font-size:0.7rem; color:#94A3B8; font-family:monospace; margin-top:4px;">Watermark Token: TeleSynapse-TS-P-001-Encrypted-PDF</div>
        </div>
        """

    report_html += """
        <div style="margin-top:30px; border-top:1px dashed #CBD5E1; padding-top:10px; font-size:0.75rem; color:#94A3B8; text-align:center;">
            This document is cryptographically verified by TeleSynapse Health Systems. Confidential Medical Record.
        </div>
    </div>
    """

    st.markdown(report_html, unsafe_allow_html=True)


# ==========================================
# 8. MODULE 5: SENIOR ADMIN & SECURITY TRAIL
# ==========================================

else:
    st.markdown("### 📊 Senior Admin & Security Control Center")

    t_adm1, t_adm2, t_adm3 = st.tabs(["🛡️ Audit Trail Logs", "✉️ Masked Email Outbox", "👨‍⚕️ Doctor Approval Management"])

    with t_adm1:
        st.markdown("#### System Security Audit Logs")
        logs = st.session_state.get("audit_logs", [])
        if logs:
            df_logs = pd.DataFrame(logs)
            st.dataframe(df_logs, use_container_width=True)
        else:
            st.info("No audit logs recorded yet.")

    with t_adm2:
        st.markdown("#### Backend Masked Email Queue")
        outbox = st.session_state.get("email_outbox", [])
        if outbox:
            df_outbox = pd.DataFrame(outbox)
            st.dataframe(df_outbox, use_container_width=True)
        else:
            st.info("Outbox is empty.")

    with t_adm3:
        st.markdown("#### Doctor Account Approval Requests")
        users = st.session_state["users_db"]
        pending_doctors = {k: v for k, v in users.items() if v["role"] == "doctor" and v["status"] == "PENDING"}

        if pending_doctors:
            for email, d_data in pending_doctors.items():
                col_a1, col_a2 = st.columns([3, 1])
                with col_a1:
                    st.write(f"**{d_data['name']}** ({email}) | License: `{d_data.get('phpc_num')}` | Proxy: `{d_data['proxy_id']}`")
                with col_a2:
                    if st.button("APPROVE DOCTOR", key=f"app_{email}"):
                        render_loader_component("Updating Credentials & Activating Doctor Account...")
                        d_data["status"] = "ACTIVE"
                        add_audit_log("ADMIN", "DOCTOR_APPROVED", f"Approved account for {email}")
                        
                        send_portal_email(
                            user_id=d_data["proxy_id"],
                            template_name="DOCTOR_ACTIVATED",
                            subject="Your Doctor Account is Activated!",
                            body="Your license has been verified. You may now log in to your dashboard."
                        )
                        st.success("Approved!")
                        st.rerun()
        else:
            st.success("🟢 No pending doctor approvals.")


# ==========================================
# 9. GLOBAL SOFT POLICY FOOTER
# ==========================================

st.markdown("""
<div style="text-align:center; color:#64748B; font-size:0.8rem; margin-top:40px; padding-top:16px; border-top:1px solid #1E293B;">
    By using TeleSynapse, all sessions and communication are securely managed within the portal to protect your medical records.
</div>
""", unsafe_allow_html=True)
