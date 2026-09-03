import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import random
import datetime
import re
import uuid
import time

# ==========================================
# 0. GLOBAL PAGE CONFIG & CLINICAL THEME
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
hero_size = "2.2rem" if big_text else "1.8rem"

# Inject High-End Clinical Cyan & Slate Blue Styling
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

/* CLINICAL SLATE & CYAN THEME BACKGROUND */
.stApp {{
    background: radial-gradient(circle at top right, #0F172A 0%, #080E1A 100%) !important;
    color: #F8FAFC !important;
}}

h1, h2, h3 {{ color: #00F5D4 !important; font-weight: 800 !important; }}
h4, h5, h6 {{ color: #38BDF8 !important; font-weight: 700 !important; }}

[data-testid="stSidebar"] {{
    background-color: #0B132B !important;
    border-right: 1px solid #1E2E52 !important;
}}

/* DOCTORAL BRANDING CONTAINER */
.brand-container {{
    padding: 20px 16px;
    background: linear-gradient(135deg, #0284C7 0%, #0B132B 100%);
    border: 1px solid #0EA5E9;
    border-radius: 16px;
    margin-bottom: 22px;
    text-align: center;
    box-shadow: 0 8px 24px rgba(2, 132, 199, 0.2);
}}
.brand-title {{
    color: #00F5D4 !important;
    font-size: 1.65rem;
    font-weight: 800;
    letter-spacing: -0.5px;
}}
.brand-sub {{
    color: #94A3B8 !important;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.4px;
}}

/* STATUS BADGES */
.status-badge-active {{
    background: rgba(16, 185, 129, 0.15);
    color: #10B981;
    border: 1px solid #10B981;
    padding: 4px 10px;
    border-radius: 8px;
    font-size: 0.75rem;
    font-weight: 700;
}}
.status-badge-pending {{
    background: rgba(245, 158, 11, 0.15);
    color: #F59E0B;
    border: 1px solid #F59E0B;
    padding: 4px 10px;
    border-radius: 8px;
    font-size: 0.75rem;
    font-weight: 700;
}}
.status-badge-unverified {{
    background: rgba(56, 189, 248, 0.15);
    color: #38BDF8;
    border: 1px solid #38BDF8;
    padding: 4px 10px;
    border-radius: 8px;
    font-size: 0.75rem;
    font-weight: 700;
}}
.status-badge-rejected {{
    background: rgba(239, 68, 68, 0.15);
    color: #EF4444;
    border: 1px solid #EF4444;
    padding: 4px 10px;
    border-radius: 8px;
    font-size: 0.75rem;
    font-weight: 700;
}}

/* CARDS & PANELS */
.clinical-card {{
    background: #111C35;
    border: 1px solid #1E2E52;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 16px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
}}

.stButton>button {{
    background: linear-gradient(90deg, #0EA5E9 0%, #00F5D4 100%) !important;
    color: #080E1A !important;
    font-weight: 800 !important;
    border-radius: 10px !important;
    border: none !important;
    padding: 10px 22px !important;
    transition: all 0.3s ease !important;
}}

/* FULLSCREEN TELEREHAB LOADER OVERLAY */
.loader-overlay {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: linear-gradient(135deg, #080E1A 0%, #0284C7 100%);
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
    border: 6px solid rgba(255, 255, 255, 0.15);
    border-top: 6px solid #00F5D4;
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
    color: #00F5D4;
    margin-bottom: 6px;
}}
.loader-sub {{
    font-size: 1.05rem;
    font-weight: 500;
    color: #E2E8F0;
}}
.loader-warning {{
    font-size: 0.82rem;
    margin-top: 18px;
    color: #94A3B8;
}}
</style>
"""
st.markdown(global_css, unsafe_allow_html=True)


# ==========================================
# 1. DATABASE & SESSION STATE INITIALIZATION
# ==========================================

if "users_db" not in st.session_state:
    st.session_state["users_db"] = {
        # Pre-seeded Super Admin Account
        "admin@telerehab.com": {
            "user_id": "ADM-001",
            "proxy_id": "SUPER-ADMIN",
            "name": "Portal Super Admin",
            "role": "super_admin",
            "status": "ACTIVE",
            "password_hash": "admin123"
        },
        # Demo Active Patient
        "patient@demo.com": {
            "user_id": "USR-P-101",
            "proxy_id": "TS-P-001",
            "name": "Muhammad Hassan Raza",
            "role": "patient",
            "status": "ACTIVE",
            "password_hash": "pass123",
            "phone": "+92 309 7964195"
        },
        # Demo Active Doctor
        "doctor@demo.com": {
            "user_id": "USR-D-909",
            "proxy_id": "TS-D-004",
            "name": "Dr. Ayesha Malik",
            "role": "doctor",
            "status": "ACTIVE",
            "phpc_num": "PHPC-88492-PAK",
            "specialty": "Orthopedic Specialist",
            "password_hash": "pass123"
        },
        # Sample Pending Doctor for Admin Approval Testing
        "hassanazabih@gmail.com": {
            "user_id": "USR-D-771",
            "proxy_id": "TS-D-112",
            "name": "Hassan Zabih",
            "role": "doctor",
            "status": "PENDING",
            "phpc_num": "12345",
            "specialty": "Neuro Rehabilitation",
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
# 2. HELPER ENGINES & SECURITY MIDDLEWARE
# ==========================================

def render_loader_component(message="Securing Your Session..."):
    """Renders the custom 2-second TeleRehab screen overlay."""
    loader_html = f"""
    <div class="loader-overlay">
        <div class="spinner-circle"></div>
        <div class="loader-title">TeleRehab</div>
        <div class="loader-sub">{message}</div>
        <div class="loader-warning">Please do not close or refresh this page</div>
    </div>
    """
    ph = st.empty()
    ph.markdown(loader_html, unsafe_allow_html=True)
    time.sleep(1.8)
    ph.empty()


def add_audit_log(actor_proxy: str, action: str, details: str):
    """Senior Audit Trail Logger."""
    st.session_state["audit_logs"].append({
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "actor": actor_proxy,
        "action": action,
        "details": details
    })


def sanitize_portal_message(user_message: str) -> tuple[str, bool]:
    """Smart Anti-Leakage Contact Masking Filter."""
    phone_pattern = r'(\+?92|0)?[\s\.\-]*3[\s\.\-]*\d[\s\.\-]*\d[\s\.\-]*\d[\s\.\-]*\d[\s\.\-]*\d[\s\.\-]*\d[\s\.\-]*\d[\s\.\-]*\d[\s\.\-]*\d'
    email_pattern = r'[a-zA-Z0-9._%+-]+@[\w\.-]+\.[a-zA-Z]{2,}'
    link_pattern = r'(whatsapp\.com|wa\.me|zoom\.us|meet\.google|teams\.microsoft)'

    flagged = False
    cleaned_msg = user_message

    if re.search(phone_pattern, cleaned_msg, re.IGNORECASE):
        cleaned_msg = re.sub(phone_pattern, '[🔒 Contact info masked for your safety]', cleaned_msg)
        flagged = True

    if re.search(email_pattern, cleaned_msg, re.IGNORECASE):
        cleaned_msg = re.sub(email_pattern, '[🔒 Email address masked for safety]', cleaned_msg)
        flagged = True

    if re.search(link_pattern, cleaned_msg, re.IGNORECASE):
        cleaned_msg = re.sub(link_pattern, '[🔒 External link disabled. Use In-Portal Call]', cleaned_msg)
        flagged = True

    return cleaned_msg, flagged


def send_portal_email(user_id: str, template_name: str, subject: str, body: str):
    """Backend Masked Email Service (SMTP/SendGrid Proxy)."""
    st.session_state["email_outbox"].append({
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "recipient_user_id": user_id,
        "sender": "noreply@telerehab.com",
        "template": template_name,
        "subject": subject,
        "body": body
    })
    add_audit_log("SYSTEM_EMAIL", "DISPATCH", f"Email '{subject}' sent to {user_id}")


# ==========================================
# 3. SIDEBAR NAVIGATION & BRANDING
# ==========================================

st.sidebar.markdown("""
<div class="brand-container">
    <div class="brand-title">🩺 TeleSynapse</div>
    <div class="brand-sub">Clinical Tele-Rehab Portal</div>
</div>
""", unsafe_allow_html=True)

# Active User Display
curr_user = st.session_state["authenticated_user"]
st.sidebar.markdown(f"**Logged in:** `{curr_user['name']}`")
st.sidebar.markdown(f"**Role:** `{curr_user['role'].upper()}` | **Proxy ID:** `{curr_user['proxy_id']}`")

menu = st.sidebar.radio("Portal Navigation", [
    "🔐 Login & Registration Portal",
    "👑 Super Admin Portal (/admin/login)",
    "👤 Patient Portal & Photo Suite",
    "👨‍⚕️ Doctor Dashboard & Gallery",
    "📄 AI Clinical Report Builder"
])


# ==========================================
# 4. MODULE 1: LOGIN & REGISTRATION
# ==========================================

if menu == "🔐 Login & Registration Portal":
    st.markdown("### 🔐 Multi-Role Authentication Gateway")
    st.caption("Secure Single-Database Dual Role Isolation System")

    tab_login, tab_reg, tab_verify = st.tabs(["🔑 Sign In", "📝 Doctor & Patient Register", "📧 Email Verification Simulator"])

    # LOGIN TAB
    with tab_login:
        st.markdown("#### Access Portal")
        role_select = st.radio("Select Login Mode:", ["Patient", "Doctor", "Super Admin"], horizontal=True)
        login_email = st.text_input("Email Address", value="patient@demo.com" if role_select == "Patient" else ("doctor@demo.com" if role_select == "Doctor" else "admin@telerehab.com"))
        login_pass = st.text_input("Password", type="password", value="pass123" if role_select != "Super Admin" else "admin123")

        if st.button("SIGN IN TO PORTAL"):
            render_loader_component("Verifying Credentials & Session Encryption...")
            user_entry = st.session_state["users_db"].get(login_email)

            if user_entry and user_entry["password_hash"] == login_pass:
                target_role = role_select.lower().replace(" ", "_")
                if user_entry["role"] != target_role:
                    st.error(f"Role Mismatch! Selected '{role_select}' but account is registered as '{user_entry['role']}'.")
                
                # DOCTOR APPROVAL & VERIFICATION BLOCKING LOGIC
                elif user_entry["role"] == "doctor":
                    if user_entry["status"] == "EMAIL_UNVERIFIED":
                        st.warning("✉️ Email Verification Required! Please verify your email via the simulator tab first.")
                    elif user_entry["status"] == "PENDING":
                        # EXACT SENIOR SPECIFICATION ERROR
                        st.error(" Doctor Account Approval Pending. Admin review takes up to 24 hours.")
                    elif user_entry["status"] == "REJECTED":
                        st.error("❌ Your Doctor account application was rejected by Super Admin.")
                    elif user_entry["status"] == "ACTIVE":
                        st.session_state["authenticated_user"] = user_entry
                        add_audit_log(user_entry["proxy_id"], "LOGIN", "Doctor successfully logged in")
                        st.success(f"Welcome back, {user_entry['name']}! Redirecting to /doctor/dashboard...")
                        st.rerun()
                else:
                    # Patient / Super Admin Auto-Login
                    st.session_state["authenticated_user"] = user_entry
                    add_audit_log(user_entry["proxy_id"], "LOGIN", f"Successful login as {role_select}")
                    st.success(f"Welcome back, {user_entry['name']}!")
                    st.rerun()
            else:
                st.error("Invalid email or password.")

    # REGISTER TAB
    with tab_reg:
        st.markdown("#### New Account Onboarding")
        reg_role = st.selectbox("I am applying as a:", ["Patient", "Doctor"])
        
        c_r1, c_r2 = st.columns(2)
        with c_r1:
            r_name = st.text_input("Full Name")
            r_email = st.text_input("Email Address")
        with c_r2:
            r_phone = st.text_input("Phone Number")
            r_pass = st.text_input("Create Password", type="password")

        if reg_role == "Doctor":
            r_phpc = st.text_input("PHPC / CNMC License # *", value="12345")
            r_spec = st.text_input("Medical Specialty", value="Physiotherapist")

        if st.button("SUBMIT REGISTRATION"):
            render_loader_component("Creating Account & Issuing Verification Tokens...")
            new_proxy = f"TS-P-{random.randint(100,999)}" if reg_role == "Patient" else f"TS-D-{random.randint(100,999)}"
            
            # Patients = Auto-Approve (ACTIVE), Doctors = EMAIL_UNVERIFIED
            init_status = "ACTIVE" if reg_role == "Patient" else "EMAIL_UNVERIFIED"

            st.session_state["users_db"][r_email] = {
                "user_id": f"USR-{random.randint(1000,9999)}",
                "proxy_id": new_proxy,
                "name": r_name,
                "role": reg_role.lower(),
                "status": init_status,
                "password_hash": r_pass,
                "phpc_num": r_phpc if reg_role == "Doctor" else "N/A",
                "phone": r_phone
            }

            if reg_role == "Doctor":
                send_portal_email(
                    user_id=new_proxy,
                    template_name="VERIFY_EMAIL",
                    subject="Verify your TeleRehab Email",
                    body=f"Hello {r_name}, please click here to verify your email address: https://telerehab.com/verify?token={uuid.uuid4().hex[:8]}"
                )
                st.info("📩 Verification Email Dispatched! Step 1 Complete. Go to 'Email Verification Simulator' tab.")
            else:
                st.success("🎉 Patient Account Created & Auto-Approved! You can log in immediately.")

    # SIMULATED EMAIL VERIFICATION TAB
    with tab_verify:
        st.markdown("#### ✉️ Doctor Email Verification Simulation (Step B)")
        st.caption("In production, the doctor clicks the verification link in their email inbox.")
        
        unverified_doctors = {k: v for k, v in st.session_state["users_db"].items() if v["role"] == "doctor" and v["status"] == "EMAIL_UNVERIFIED"}
        
        if unverified_doctors:
            for em, doc in unverified_doctors.items():
                st.markdown(f"""
                <div class="clinical-card">
                    <div style="color:#00F5D4; font-weight:700;">Doctor: {doc['name']} ({em})</div>
                    <div style="color:#94A3B8; font-size:0.82rem;">PHPC License: {doc['phpc_num']} | Status: <span class="status-badge-unverified">EMAIL_UNVERIFIED</span></div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"VERIFY EMAIL FOR {doc['name']}", key=f"v_{em}"):
                    render_loader_component("Verifying Email Link Token...")
                    doc["status"] = "PENDING"
                    add_audit_log(doc["proxy_id"], "EMAIL_VERIFIED", "Email token verified. Status set to PENDING.")
                    st.success("✅ Email Verified! Account status updated to PENDING (Awaiting Super Admin Approval).")
                    st.rerun()
        else:
            st.info("🟢 No doctors awaiting email verification.")


# ==========================================
# 5. MODULE 2: SUPER ADMIN PORTAL (/admin/login)
# ==========================================

elif menu == "👑 Super Admin Portal (/admin/login)":
    if curr_user["role"] != "super_admin":
        st.warning("🔒 Access Denied. Super Admin privileges required.")
    else:
        st.markdown("### 👑 TeleSynapse Super Admin Command Panel")
        st.caption("Manage Doctor Approval Pipeline, Security Trail, and System Outbox")

        admin_tab1, admin_tab2, admin_tab3 = st.tabs(["🩺 Doctor Approval Requests", "🛡️ Audit Trail Logs", "📤 Masked Email Queue"])

        # DOCTOR APPROVAL QUEUE
        with admin_tab1:
            st.markdown("#### New Doctor Registration Requests")
            doctors_db = st.session_state["users_db"]
            pending_docs = {k: v for k, v in doctors_db.items() if v["role"] == "doctor" and v["status"] == "PENDING"}

            if pending_docs:
                for doc_email, doc_info in pending_docs.items():
                    st.markdown(f"""
                    <div class="clinical-card">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <div>
                                <div style="color:#00F5D4; font-weight:800; font-size:1.15rem;">Doctor: {doc_info['name']}</div>
                                <div style="color:#CBD5E1; font-size:0.88rem;">Email: <code>{doc_email}</code> | PHPC License #: <b style="color:#38BDF8;">{doc_info.get('phpc_num')}</b></div>
                                <div style="color:#94A3B8; font-size:0.8rem; margin-top:4px;">Proxy ID: <code>{doc_info['proxy_id']}</code> | Status: <span class="status-badge-pending">PENDING APPROVAL</span></div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    btn_c1, btn_c2, _ = st.columns([1, 1, 3])
                    with btn_c1:
                        if st.button(f"✅ APPROVE", key=f"app_{doc_email}"):
                            render_loader_component("Approving Doctor & Activating Account...")
                            doc_info["status"] = "ACTIVE"
                            add_audit_log("SUPER_ADMIN", "DOCTOR_APPROVED", f"Approved {doc_email}")
                            
                            send_portal_email(
                                user_id=doc_info["proxy_id"],
                                template_name="DOCTOR_ACTIVATED",
                                subject="Your TeleSynapse Doctor Account is Activated!",
                                body=f"Congratulations Dr. {doc_info['name']}, your license has been verified. You can now log in."
                            )
                            st.success(f"Doctor {doc_info['name']} Approved!")
                            st.rerun()

                    with btn_c2:
                        if st.button(f"❌ REJECT", key=f"rej_{doc_email}"):
                            render_loader_component("Rejecting Application...")
                            doc_info["status"] = "REJECTED"
                            add_audit_log("SUPER_ADMIN", "DOCTOR_REJECTED", f"Rejected {doc_email}")
                            st.error(f"Doctor Application Rejected.")
                            st.rerun()
            else:
                st.success("🟢 No pending doctor approval requests. All doctors processed!")

            # Display All Registered Doctors Status
            st.markdown("---")
            st.markdown("#### All Registered Doctors Status Summary")
            all_docs = [v for k, v in doctors_db.items() if v["role"] == "doctor"]
            if all_docs:
                st.dataframe(pd.DataFrame(all_docs)[["name", "proxy_id", "status", "phpc_num"]], use_container_width=True)

        # AUDIT TRAIL LOGS
        with admin_tab2:
            st.markdown("#### System Security Audit Logs")
            logs = st.session_state.get("audit_logs", [])
            if logs:
                st.dataframe(pd.DataFrame(logs), use_container_width=True)
            else:
                st.info("No audit logs recorded yet.")

        # EMAIL OUTBOX
        with admin_tab3:
            st.markdown("#### Masked Email Dispatch Outbox")
            outbox = st.session_state.get("email_outbox", [])
            if outbox:
                st.dataframe(pd.DataFrame(outbox), use_container_width=True)
            else:
                st.info("Outbox is empty.")


# ==========================================
# 6. MODULE 3: PATIENT PORTAL
# ==========================================

elif menu == "👤 Patient Portal & Photo Suite":
    if curr_user["role"] != "patient":
        st.warning("⚠️ Access Restricted to Patient accounts.")
    else:
        st.markdown("### 👤 Patient Clinical Portal & Photo Center")
        
        st.markdown("""
        <div class="clinical-card" style="border-left: 5px solid #00F5D4;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <div style="color:#00F5D4; font-weight:800; font-size:1.2rem;">Assigned Doctor: Dr. Ayesha Malik</div>
                    <div style="color:#94A3B8; font-size:0.85rem;">Doctor Proxy: <b>TS-D-004</b> | Your Proxy: <b>TS-P-001</b></div>
                </div>
                <div style="background:#080E1A; color:#38BDF8; font-size:0.75rem; font-weight:700; padding:6px 12px; border-radius:8px; border:1px solid #1E2E52;">
                    🔒 Zero Contact Exposure Active
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        c_p1, c_p2 = st.columns(2)
        with c_p1:
            st.markdown("#### 📸 Upload Progress Photo")
            tag_choice = st.selectbox("Interval Tag:", ["Before Photo", "Week 1 Progress", "Week 2 Progress", "Week 3 Progress", "Week 4 Final"])
            up_img = st.file_uploader("Upload Image (JPG/PNG)", type=["jpg", "png", "jpeg"])

            if st.button("UPLOAD & AUTO-TAG PHOTO"):
                if up_img:
                    render_loader_component("Encrypting Photo & Auto-Tagging via AI Vision Engine...")
                    uuid_fn = f"storage_{uuid.uuid4().hex[:10]}.jpg"
                    ai_tags = [
                        "Detected: Knee Joint, Flexion: 95°, Swelling: Reduced",
                        "Detected: Shoulder Joint, Elevation: 130°, Progress: Optimal"
                    ]
                    
                    record = {
                        "uuid_filename": uuid_fn,
                        "tag": tag_choice,
                        "ai_analysis": random.choice(ai_tags),
                        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "selected_for_report": True
                    }

                    if curr_user["proxy_id"] not in st.session_state["patient_photos"]:
                        st.session_state["patient_photos"][curr_user["proxy_id"]] = []

                    st.session_state["patient_photos"][curr_user["proxy_id"]].append(record)
                    add_audit_log(curr_user["proxy_id"], "PHOTO_UPLOAD", f"Uploaded {tag_choice}")
                    st.success(f"✅ Photo Uploaded! UUID: `{uuid_fn}`")

        with c_p2:
            st.markdown("#### 🖼️ Encrypted Photo Gallery")
            p_photos = st.session_state["patient_photos"].get(curr_user["proxy_id"], [])
            if p_photos:
                for item in p_photos:
                    st.markdown(f"""
                    <div style="background:#0B132B; border:1px dashed #00F5D4; border-radius:10px; padding:12px; margin-bottom:10px;">
                        <div style="color:#00F5D4; font-weight:700;">📌 {item['tag']}</div>
                        <div style="color:#94A3B8; font-size:0.78rem;">UUID: {item['uuid_filename']}</div>
                        <div style="color:#38BDF8; font-size:0.82rem; margin-top:4px;">🧠 {item['ai_analysis']}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No photos uploaded yet.")


# ==========================================
# 7. MODULE 4: DOCTOR DASHBOARD
# ==========================================

elif menu == "👨‍⚕️ Doctor Dashboard & Gallery":
    if curr_user["role"] != "doctor":
        st.warning("⚠️ Access Restricted to Doctor accounts.")
    else:
        st.markdown("### 👨‍⚕️ Doctor Clinical Hub")
        
        st.markdown("""
        <div class="clinical-card" style="border-left: 5px solid #0EA5E9;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <div style="color:#38BDF8; font-weight:800; font-size:1.2rem;">Patient: Hassan Raza</div>
                    <div style="color:#94A3B8; font-size:0.85rem;">Patient Proxy: <b>TS-P-001</b> | Condition: ACL Flexion Recovery</div>
                </div>
                <div style="background:#080E1A; color:#00F5D4; font-size:0.75rem; font-weight:700; padding:6px 12px; border-radius:8px; border:1px solid #1E2E52;">
                    🔒 Masked Contact Mode
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 🖼️ Patient Photo Review & Report Selection")
        pat_photos = st.session_state["patient_photos"].get("TS-P-001", [])

        if pat_photos:
            for idx, pic in enumerate(pat_photos):
                st.markdown(f"""
                <div class="clinical-card">
                    <div style="color:#00F5D4; font-weight:700;">🏷️ {pic['tag']}</div>
                    <div style="color:#CBD5E1; font-size:0.85rem;">🧠 {pic['ai_analysis']}</div>
                </div>
                """, unsafe_allow_html=True)
                pic["selected_for_report"] = st.checkbox("Select for PDF Report", value=pic.get("selected_for_report", True), key=f"sel_{idx}")
        else:
            st.info("No photos available for review.")


# ==========================================
# 8. MODULE 5: AI REPORT BUILDER
# ==========================================

else:
    st.markdown("### 📄 AI Progress Report Generator")
    st.caption("Generates HIPAA-Compliant Watermarked Report PDF")

    photos = st.session_state["patient_photos"].get("TS-P-001", [])
    selected_pics = [p for p in photos if p.get("selected_for_report", True)]

    if st.button("⚙️ GENERATE REPORT PDF"):
        render_loader_component("Compiling AI Vision Metrics & Watermarking PDF...")
        add_audit_log(curr_user["proxy_id"], "REPORT_GENERATED", f"Generated report with {len(selected_pics)} images.")
        st.success("🎉 Report PDF Generated & Sent to Patient Inbox!")

    st.markdown("---")
    st.markdown("#### 📑 PDF Preview Frame")
    st.markdown(f"""
    <div style="background:#FFFFFF; color:#0F172A; border-radius:12px; padding:26px;">
        <h3 style="color:#0284C7 !important;">TeleSynapse Clinical Recovery Report</h3>
        <div><b>Patient Proxy:</b> TS-P-001 | <b>Doctor:</b> Dr. Ayesha Malik (TS-D-004)</div>
        <hr>
        <div><b>Active Images Included:</b> {len(selected_pics)}</div>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# 9. GLOBAL SOFT POLICY FOOTER
# ==========================================

st.markdown("""
<div style="text-align:center; color:#64748B; font-size:0.8rem; margin-top:40px; padding-top:16px; border-top:1px solid #1E2E52;">
    By using TeleSynapse, all sessions and communication are securely managed within the portal to protect your medical records.
</div>
""", unsafe_allow_html=True)
