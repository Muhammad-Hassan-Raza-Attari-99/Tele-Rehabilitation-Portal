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
# 0. GLOBAL PAGE CONFIG & HIGH-CONTRAST THEME
# ==========================================

st.set_page_config(
    page_title="TeleSynapse | Clinical Tele-Rehab Portal",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Accessibility Mode Toggle
st.sidebar.markdown("### ♿ Accessibility Mode")
big_text = st.sidebar.toggle("🔍 Large Text Mode", value=False)

base_font = "17px" if big_text else "15px"

# Inject International Grade Medical White & Blue High-Contrast Styling
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

/* GLOBAL BACKGROUND */
.stApp {{
    background-color: #F8FAFC !important;
    color: #0F172A !important;
}}

h1, h2, h3 {{ color: #1E3A8A !important; font-weight: 800 !important; }}
h4, h5, h6 {{ color: #0284C7 !important; font-weight: 700 !important; }}

/* STREAMLIT SIDEBAR FIX - HIGH CONTRAST GUARANTEE */
[data-testid="stSidebar"] {{
    background-color: #FFFFFF !important;
    border-right: 1px solid #CBD5E1 !important;
}}

/* Force ALL text, paragraphs, labels, spans, and markdown in sidebar to dark visible colors */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] .stMarkdown {{
    color: #0F172A !important;
    font-weight: 600 !important;
}}

/* Radio Button Specific Labels in Sidebar */
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {{
    color: #1E3A8A !important;
    font-weight: 800 !important;
    font-size: 0.95rem !important;
}}

[data-testid="stSidebar"] [role="radiogroup"] label p {{
    color: #1E293B !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
}}

/* Selected Radio Option Highlight */
[data-testid="stSidebar"] [role="radiogroup"] label[data-checked="true"] p {{
    color: #0284C7 !important;
    font-weight: 800 !important;
}}

/* Toggle Switch Label Fix */
[data-testid="stSidebar"] [data-testid="stCheckbox"] label p {{
    color: #1E293B !important;
    font-weight: 700 !important;
}}

/* BRANDING CONTAINER */
.brand-container {{
    padding: 18px 14px;
    background: linear-gradient(135deg, #1E3A8A 0%, #0284C7 100%);
    border-radius: 14px;
    margin-bottom: 20px;
    text-align: center;
    box-shadow: 0 6px 16px rgba(30, 58, 138, 0.15);
}}
.brand-title {{
    color: #FFFFFF !important;
    font-size: 1.6rem;
    font-weight: 800;
}}
.brand-sub {{
    color: #E0F2FE !important;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.2px;
}}

/* USER SESSION CARD IN SIDEBAR */
.user-info-card {{
    background: #F1F5F9;
    border: 1px solid #CBD5E1;
    border-radius: 10px;
    padding: 12px;
    margin-bottom: 20px;
}}

/* TOP RIGHT PROFILE HEADER CARD */
.top-profile-badge {{
    display: flex;
    align-items: center;
    gap: 12px;
    background: #FFFFFF;
    border: 1px solid #CBD5E1;
    padding: 8px 16px;
    border-radius: 40px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.06);
}}
.profile-avatar-img {{
    width: 44px;
    height: 44px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid #0284C7;
}}

/* STATUS BADGES */
.status-badge-active {{
    background: #DCFCE7;
    color: #15803D !important;
    border: 1px solid #86EFAC;
    padding: 4px 10px;
    border-radius: 8px;
    font-size: 0.75rem;
    font-weight: 700;
}}
.status-badge-pending {{
    background: #FEF3C7;
    color: #B45309 !important;
    border: 1px solid #FCD34D;
    padding: 4px 10px;
    border-radius: 8px;
    font-size: 0.75rem;
    font-weight: 700;
}}

/* CLINICAL WHITE CARDS */
.clinical-card {{
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 16px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.04);
}}

.stButton>button {{
    background: linear-gradient(90deg, #1E3A8A 0%, #0284C7 100%) !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    border-radius: 10px !important;
    border: none !important;
    padding: 10px 22px !important;
}}

/* FULLSCREEN TELEREHAB LOADER OVERLAY */
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
    width: 75px;
    height: 75px;
    border: 6px solid rgba(255, 255, 255, 0.2);
    border-top: 6px solid #FFFFFF;
    border-radius: 50%;
    animation: spin 0.9s linear infinite;
    margin-bottom: 22px;
}}
@keyframes spin {{
    0% {{ transform: rotate(0deg); }}
    100% {{ transform: rotate(360deg); }}
}}
.loader-title {{
    font-size: 2.2rem;
    font-weight: 800;
    letter-spacing: 2px;
    margin-bottom: 6px;
}}
.loader-sub {{
    font-size: 1.05rem;
    font-weight: 500;
}}
</style>
"""
st.markdown(global_css, unsafe_allow_html=True)


# ==========================================
# 1. DEFAULT AVATAR ASSETS (BASE64 SVG / IMAGES)
# ==========================================

LADY_DOCTOR_AVATAR = "https://cdn-icons-png.flaticon.com/512/387/387561.png"
MALE_PATIENT_AVATAR = "https://cdn-icons-png.flaticon.com/512/4140/4140048.png"
ADMIN_AVATAR = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"


# ==========================================
# 2. DATABASE & SESSION STATE INITIALIZATION
# ==========================================

if "users_db" not in st.session_state:
    st.session_state["users_db"] = {
        "admin@telerehab.com": {
            "user_id": "ADM-001",
            "proxy_id": "SUPER-ADMIN",
            "name": "Portal Super Admin",
            "role": "super_admin",
            "status": "ACTIVE",
            "password_hash": "admin123",
            "profile_pic": ADMIN_AVATAR
        },
        "patient@demo.com": {
            "user_id": "USR-P-101",
            "proxy_id": "TS-P-001",
            "name": "Muhammad Hassan Raza",
            "role": "patient",
            "status": "ACTIVE",
            "password_hash": "pass123",
            "phone": "+92 309 7964195",
            "profile_pic": MALE_PATIENT_AVATAR
        },
        "doctor@demo.com": {
            "user_id": "USR-D-909",
            "proxy_id": "TS-D-004",
            "name": "Dr. Ayesha Malik",
            "role": "doctor",
            "status": "ACTIVE",
            "phpc_num": "PHPC-88492-PAK",
            "specialty": "Orthopedic Specialist",
            "password_hash": "pass123",
            "profile_pic": LADY_DOCTOR_AVATAR
        },
        "hassanazabih@gmail.com": {
            "user_id": "USR-D-771",
            "proxy_id": "TS-D-112",
            "name": "Hassan Zabih",
            "role": "doctor",
            "status": "PENDING",
            "phpc_num": "12345",
            "specialty": "Neuro Rehabilitation",
            "password_hash": "pass123",
            "profile_pic": LADY_DOCTOR_AVATAR
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
                "ai_analysis": "Detected: Knee Joint, Swelling: Moderate, Flexion: 45°",
                "timestamp": "2026-08-10 14:30:00",
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
        {"sender": "TS-D-004", "text": "Hello! Please share your flexion progress image before our video session."},
        {"sender": "TS-P-001", "text": "Sure doctor, uploading right now."}
    ]


# ==========================================
# 3. HELPER ENGINES & UTILITIES
# ==========================================

def render_loader_component(message="Securing Your Session..."):
    loader_html = f"""
    <div class="loader-overlay">
        <div class="spinner-circle"></div>
        <div class="loader-title">TeleRehab</div>
        <div class="loader-sub">{message}</div>
    </div>
    """
    ph = st.empty()
    ph.markdown(loader_html, unsafe_allow_html=True)
    time.sleep(1.8)
    ph.empty()


def add_audit_log(actor_proxy: str, action: str, details: str):
    st.session_state["audit_logs"].append({
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "actor": actor_proxy,
        "action": action,
        "details": details
    })


def sanitize_portal_message(user_message: str) -> tuple[str, bool]:
    phone_pattern = r'(\+?92|0)?[\s\.\-]*3[\s\.\-]*\d[\s\.\-]*\d[\s\.\-]*\d[\s\.\-]*\d[\s\.\-]*\d[\s\.\-]*\d[\s\.\-]*\d[\s\.\-]*\d[\s\.\-]*\d'
    email_pattern = r'[a-zA-Z0-9._%+-]+@[\w\.-]+\.[a-zA-Z]{2,}'
    link_pattern = r'(whatsapp\.com|wa\.me|zoom\.us|meet\.google|teams\.microsoft)'

    flagged = False
    cleaned_msg = user_message

    if re.search(phone_pattern, cleaned_msg, re.IGNORECASE):
        cleaned_msg = re.sub(phone_pattern, '[🔒 Contact info masked]', cleaned_msg)
        flagged = True

    if re.search(email_pattern, cleaned_msg, re.IGNORECASE):
        cleaned_msg = re.sub(email_pattern, '[🔒 Email masked]', cleaned_msg)
        flagged = True

    if re.search(link_pattern, cleaned_msg, re.IGNORECASE):
        cleaned_msg = re.sub(link_pattern, '[🔒 External link masked]', cleaned_msg)
        flagged = True

    return cleaned_msg, flagged


def send_portal_email(user_id: str, template_name: str, subject: str, body: str):
    st.session_state["email_outbox"].append({
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "recipient_user_id": user_id,
        "sender": "noreply@telerehab.com",
        "template": template_name,
        "subject": subject,
        "body": body
    })


def render_top_right_profile_header():
    u = st.session_state["authenticated_user"]
    pic = u.get("profile_pic", MALE_PATIENT_AVATAR)

    c_left, c_right = st.columns([3, 1])
    with c_right:
        st.markdown(f"""
        <div style="display:flex; justify-content:flex-end; margin-bottom:15px;">
            <div class="top-profile-badge">
                <img src="{pic}" class="profile-avatar-img" />
                <div style="text-align:left;">
                    <div style="font-weight:800; color:#1E3A8A; font-size:0.88rem; line-height:1.1;">{u['name']}</div>
                    <div style="color:#64748B; font-size:0.75rem; font-weight:600;">{u['role'].upper()} | {u['proxy_id']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ==========================================
# 4. SIDEBAR NAVIGATION & USER INFO
# ==========================================

st.sidebar.markdown("""
<div class="brand-container">
    <div class="brand-title">🩺 TeleSynapse</div>
    <div class="brand-sub">Clinical Tele-Rehab Portal</div>
</div>
""", unsafe_allow_html=True)

curr_user = st.session_state["authenticated_user"]

# High Contrast User Info Card
st.sidebar.markdown(f"""
<div class="user-info-card">
    <div style="font-size: 0.72rem; color: #64748B; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px;">Active Session</div>
    <div style="font-size: 0.98rem; color: #1E3A8A; font-weight: 800; margin-top:2px;">{curr_user['name']}</div>
    <div style="font-size: 0.8rem; color: #0284C7; font-weight: 700; margin-top:2px;">Role: {curr_user['role'].upper()}</div>
</div>
""", unsafe_allow_html=True)

menu = st.sidebar.radio("Portal Navigation", [
    "🔐 Login & Quick Registration",
    "👑 Super Admin Portal (/admin/login)",
    "👤 Patient Portal & Photo Suite",
    "👨‍⚕️ Doctor Dashboard & Gallery",
    "📄 AI Clinical Report Builder"
])


# Render Top Right Profile Header Across Portal
render_top_right_profile_header()


# ==========================================
# 5. MODULE 1: LOGIN & QUICK REGISTRATION
# ==========================================

if menu == "🔐 Login & Quick Registration":
    st.markdown("### 🔐 Multi-Role Authentication Gateway")
    st.caption("Supports Direct Profile Picture Upload & 1-Click Quick Avatars")

    st.markdown("#### ⚡ Urgent / Fast Registration Presets")
    st.caption("Click any avatar below to instantly complete registration details:")

    col_av1, col_av2 = st.columns(2)
    
    with col_av1:
        if st.button("👩‍⚕️ Quick Select: Lady Doctor Suit (Dr. Ayesha)"):
            st.session_state["preset_role"] = "Doctor"
            st.session_state["preset_name"] = "Dr. Ayesha Malik"
            st.session_state["preset_email"] = f"ayesha_{random.randint(100,999)}@telerehab.com"
            st.session_state["preset_pic"] = LADY_DOCTOR_AVATAR
            st.toast("Applied Lady Doctor Suit Preset!", icon="👩‍⚕️")

    with col_av2:
        if st.button("👨‍💼 Quick Select: Male Patient Suit (Hassan Raza)"):
            st.session_state["preset_role"] = "Patient"
            st.session_state["preset_name"] = "Muhammad Hassan Raza"
            st.session_state["preset_email"] = f"hassan_{random.randint(100,999)}@gmail.com"
            st.session_state["preset_pic"] = MALE_PATIENT_AVATAR
            st.toast("Applied Male Patient Suit Preset!", icon="👨‍💼")

    st.markdown("---")

    tab_login, tab_reg, tab_verify = st.tabs(["🔑 Sign In", "📝 Register & Upload Photo", "📧 Email Verification Simulator"])

    with tab_login:
        st.markdown("#### Access Your Portal")
        role_select = st.radio("Select Login Mode:", ["Patient", "Doctor", "Super Admin"], horizontal=True)
        
        login_email = st.text_input("Email Address", value="patient@demo.com" if role_select == "Patient" else ("doctor@demo.com" if role_select == "Doctor" else "admin@telerehab.com"))
        login_pass = st.text_input("Password", type="password", value="pass123" if role_select != "Super Admin" else "admin123")

        if st.button("SIGN IN TO PORTAL"):
            render_loader_component("Verifying Credentials & Session Tokens...")
            user_entry = st.session_state["users_db"].get(login_email)

            if user_entry and user_entry["password_hash"] == login_pass:
                target_role = role_select.lower().replace(" ", "_")
                
                if user_entry["role"] != target_role:
                    st.error(f"Role Mismatch! Account is '{user_entry['role']}', not '{role_select}'.")
                
                elif user_entry["role"] == "doctor":
                    if user_entry["status"] == "EMAIL_UNVERIFIED":
                        st.warning("✉️ Email Verification Required! Verify via email simulator tab first.")
                    elif user_entry["status"] == "PENDING":
                        st.error("Doctor Account Approval Pending. Admin review takes up to 24 hours.")
                    elif user_entry["status"] == "ACTIVE":
                        st.session_state["authenticated_user"] = user_entry
                        add_audit_log(user_entry["proxy_id"], "LOGIN", "Doctor logged in successfully")
                        st.success(f"Welcome Dr. {user_entry['name']}! Photo loaded to top-right.")
                        st.rerun()
                else:
                    st.session_state["authenticated_user"] = user_entry
                    add_audit_log(user_entry["proxy_id"], "LOGIN", f"Logged in as {role_select}")
                    st.success(f"Welcome back, {user_entry['name']}!")
                    st.rerun()
            else:
                st.error("Invalid Email or Password.")

    with tab_reg:
        st.markdown("#### Create Account & Upload Profile Photo")
        
        default_role = st.session_state.get("preset_role", "Patient")
        reg_role = st.selectbox("Registering as:", ["Patient", "Doctor"], index=0 if default_role == "Patient" else 1)
        
        c_r1, c_r2 = st.columns(2)
        with c_r1:
            r_name = st.text_input("Full Name", value=st.session_state.get("preset_name", ""))
            r_email = st.text_input("Email Address", value=st.session_state.get("preset_email", ""))
        with c_r2:
            r_phone = st.text_input("Phone Number", value="+92 300 1234567")
            r_pass = st.text_input("Create Password", type="password", value="pass123")

        if reg_role == "Doctor":
            r_phpc = st.text_input("PHPC / CNMC License # *", value="12345")

        st.markdown("##### 🖼️ Upload Profile Photo (Displays at Top Right)")
        uploaded_profile_file = st.file_uploader("Upload Profile Image (JPG/PNG)", type=["jpg", "png", "jpeg"])
        
        final_profile_pic = st.session_state.get("preset_pic", MALE_PATIENT_AVATAR if reg_role == "Patient" else LADY_DOCTOR_AVATAR)

        if uploaded_profile_file:
            bytes_data = uploaded_profile_file.getvalue()
            b64_str = base64.b64encode(bytes_data).decode()
            final_profile_pic = f"data:image/jpeg;base64,{b64_str}"

        if st.button("SUBMIT REGISTRATION FORM"):
            render_loader_component("Processing Account & Setting Profile Photo...")
            new_proxy = f"TS-P-{random.randint(100,999)}" if reg_role == "Patient" else f"TS-D-{random.randint(100,999)}"
            init_status = "ACTIVE" if reg_role == "Patient" else "EMAIL_UNVERIFIED"

            st.session_state["users_db"][r_email] = {
                "user_id": f"USR-{random.randint(1000,9999)}",
                "proxy_id": new_proxy,
                "name": r_name,
                "role": reg_role.lower(),
                "status": init_status,
                "password_hash": r_pass,
                "phpc_num": r_phpc if reg_role == "Doctor" else "N/A",
                "phone": r_phone,
                "profile_pic": final_profile_pic
            }

            if reg_role == "Doctor":
                send_portal_email(
                    user_id=new_proxy,
                    template_name="VERIFY_EMAIL",
                    subject="Verify your TeleRehab Email",
                    body=f"Hello {r_name}, click link to verify email."
                )
                st.info("📩 Verification Email Sent! Proceed to 'Email Verification Simulator' tab.")
            else:
                st.success("🎉 Patient Account Created & Auto-Approved! Profile Photo Updated.")

    with tab_verify:
        st.markdown("#### 📧 Email Verification Simulator (Step B)")
        unverified_doctors = {k: v for k, v in st.session_state["users_db"].items() if v["role"] == "doctor" and v["status"] == "EMAIL_UNVERIFIED"}
        
        if unverified_doctors:
            for em, doc in unverified_doctors.items():
                st.markdown(f"**Doctor:** {doc['name']} (`{em}`) | Status: `EMAIL_UNVERIFIED`")
                if st.button(f"VERIFY EMAIL LINK FOR {doc['name']}", key=f"v_{em}"):
                    render_loader_component("Verifying Email Token...")
                    doc["status"] = "PENDING"
                    st.success("✅ Email Verified! Status updated to PENDING (Awaiting Super Admin Approval).")
                    st.rerun()
        else:
            st.info("🟢 No doctors waiting for email verification.")


# ==========================================
# 6. MODULE 2: SUPER ADMIN PORTAL (/admin/login)
# ==========================================

elif menu == "👑 Super Admin Portal (/admin/login)":
    if curr_user["role"] != "super_admin":
        st.warning("🔒 Access Denied. Super Admin privileges required.")
    else:
        st.markdown("### 👑 Super Admin Command Panel")
        
        doctors_db = st.session_state["users_db"]
        pending_docs = {k: v for k, v in doctors_db.items() if v["role"] == "doctor" and v["status"] == "PENDING"}

        st.markdown("#### New Doctor Approval Requests")
        if pending_docs:
            for doc_email, doc_info in pending_docs.items():
                st.markdown(f"""
                <div class="clinical-card">
                    <div style="display:flex; align-items:center; gap:12px;">
                        <img src="{doc_info.get('profile_pic', LADY_DOCTOR_AVATAR)}" style="width:50px; height:50px; border-radius:50%;" />
                        <div>
                            <div style="color:#1E3A8A; font-weight:800; font-size:1.1rem;">Dr. {doc_info['name']}</div>
                            <div style="color:#64748B; font-size:0.85rem;">Email: {doc_email} | PHPC #: <b>{doc_info.get('phpc_num')}</b></div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                b1, b2, _ = st.columns([1, 1, 3])
                with b1:
                    if st.button(f"✅ APPROVE", key=f"app_{doc_email}"):
                        render_loader_component("Approving Doctor & Activating Account...")
                        doc_info["status"] = "ACTIVE"
                        add_audit_log("SUPER_ADMIN", "DOCTOR_APPROVED", f"Approved {doc_email}")
                        st.success(f"Doctor {doc_info['name']} Approved!")
                        st.rerun()
                with b2:
                    if st.button(f"❌ REJECT", key=f"rej_{doc_email}"):
                        doc_info["status"] = "REJECTED"
                        st.error("Application Rejected.")
                        st.rerun()
        else:
            st.success("🟢 No pending doctor approval requests.")


# ==========================================
# 7. MODULE 3: PATIENT PORTAL
# ==========================================

elif menu == "👤 Patient Portal & Photo Suite":
    if curr_user["role"] != "patient":
        st.warning("⚠️ Access Restricted to Patient accounts.")
    else:
        st.markdown("### 👤 Patient Clinical Portal")
        
        st.markdown("""
        <div class="clinical-card" style="border-left: 5px solid #0284C7;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <div style="color:#1E3A8A; font-weight:800; font-size:1.2rem;">Assigned Doctor: Dr. Ayesha Malik</div>
                    <div style="color:#64748B; font-size:0.85rem;">Doctor Proxy: <b>TS-D-004</b> | Your Proxy: <b>TS-P-001</b></div>
                </div>
                <div class="status-badge-active">🔒 Zero Contact Exposure Active</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### 📸 Upload Progress Photo")
            tag = st.selectbox("Interval Tag:", ["Before Photo", "Week 1 Progress", "Week 2 Progress", "Week 3 Progress"])
            up_f = st.file_uploader("Select Image", type=["jpg", "png", "jpeg"])

            if st.button("UPLOAD PHOTO"):
                if up_f:
                    render_loader_component("Compressing & Auto-Tagging via AI...")
                    uuid_fn = f"storage_{uuid.uuid4().hex[:10]}.jpg"
                    rec = {
                        "uuid_filename": uuid_fn,
                        "tag": tag,
                        "ai_analysis": "Detected: Knee Flexion, Flexion Angle: 85°",
                        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "selected_for_report": True
                    }
                    if curr_user["proxy_id"] not in st.session_state["patient_photos"]:
                        st.session_state["patient_photos"][curr_user["proxy_id"]] = []
                    st.session_state["patient_photos"][curr_user["proxy_id"]].append(rec)
                    st.success("✅ Uploaded!")

        with c2:
            st.markdown("#### 🖼️ Uploaded Progress Gallery")
            photos = st.session_state["patient_photos"].get(curr_user["proxy_id"], [])
            for p in photos:
                st.markdown(f"📌 **{p['tag']}** — `{p['uuid_filename']}`\n\n🧠 {p['ai_analysis']}")

        st.markdown("---")
        st.markdown("#### 💬 Encrypted Chat")
        for msg in st.session_state["chat_messages"]:
            st.write(f"**{msg['sender']}:** {msg['text']}")

        with st.form("chat_form", clear_on_submit=True):
            cin = st.text_input("Type message to doctor:")
            if st.form_submit_button("Send"):
                clean, flagged = sanitize_portal_message(cin)
                st.session_state["chat_messages"].append({"sender": curr_user["proxy_id"], "text": clean})
                st.rerun()


# ==========================================
# 8. MODULE 4: DOCTOR DASHBOARD
# ==========================================

elif menu == "👨‍⚕️ Doctor Dashboard & Gallery":
    if curr_user["role"] != "doctor":
        st.warning("⚠️ Access Restricted to Doctor accounts.")
    else:
        st.markdown("### 👨‍⚕️ Doctor Workspace")
        st.markdown("Patient: **Hassan Raza** (`TS-P-001`) | ACL Recovery")

        pat_photos = st.session_state["patient_photos"].get("TS-P-001", [])
        for idx, pic in enumerate(pat_photos):
            st.markdown(f"🏷️ **{pic['tag']}** | 🧠 {pic['ai_analysis']}")
            pic["selected_for_report"] = st.checkbox("Include in PDF Report", value=pic.get("selected_for_report", True), key=f"sel_{idx}")


# ==========================================
# 9. MODULE 5: AI REPORT BUILDER
# ==========================================

else:
    st.markdown("### 📄 AI Progress Report Generator")
    photos = st.session_state["patient_photos"].get("TS-P-001", [])
    selected_pics = [p for p in photos if p.get("selected_for_report", True)]

    if st.button("⚙️ GENERATE CLINICAL REPORT PDF"):
        render_loader_component("Compiling AI Vision Metrics & Watermarking PDF...")
        st.success("🎉 Report PDF Generated & Sent to Patient Inbox!")


# ==========================================
# 10. FOOTER POLICY
# ==========================================

st.markdown("""
<div style="text-align:center; color:#64748B; font-size:0.8rem; margin-top:40px; padding-top:16px; border-top:1px solid #CBD5E1;">
    By using TeleSynapse, all sessions and communication are securely managed within the portal to protect your medical records.
</div>
""", unsafe_allow_html=True)
