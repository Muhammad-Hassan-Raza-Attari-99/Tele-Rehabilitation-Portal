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

# Drawer Session State Trigger
if "drawer_open" not in st.session_state:
    st.session_state["drawer_open"] = False

# Background Blur & Dimming Logic when Drawer is Open
drawer_dim_css = ""
if st.session_state["drawer_open"]:
    drawer_dim_css = """
    .stApp > div:nth-child(2), [data-testid="stSidebar"] {
        filter: blur(8px) brightness(0.45) !important;
        pointer-events: none !important;
        transition: all 0.3s ease-in-out !important;
    }
    """

# Inject CSS Styling
global_css = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

#MainMenu {{ visibility: hidden !important; }}
footer {{ visibility: hidden !important; }}
.stDeployButton {{ display: none !important; }}
header[data-testid="stHeader"] {{ background-color: transparent !important; }}

{drawer_dim_css}

html, body, [class*="css"] {{
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: {base_font} !important;
}}

/* GLOBAL BACKGROUND */
.stApp {{
    background-color: #F8FAFC !important;
    color: #0F172A !important;
    transition: filter 0.3s ease-in-out;
}}

h1, h2, h3 {{ color: #1E3A8A !important; font-weight: 800 !important; }}
h4, h5, h6 {{ color: #0284C7 !important; font-weight: 700 !important; }}

/* STREAMLIT SIDEBAR - HIGH CONTRAST */
[data-testid="stSidebar"] {{
    background-color: #FFFFFF !important;
    border-right: 1px solid #CBD5E1 !important;
}}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] .stMarkdown {{
    color: #0F172A !important;
    font-weight: 600 !important;
}}

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

[data-testid="stSidebar"] [role="radiogroup"] label[data-checked="true"] p {{
    color: #0284C7 !important;
    font-weight: 800 !important;
}}

/* PURE BLACK SLEEK BRANDING CONTAINER (AS REQUESTED) */
.brand-container {{
    padding: 22px 16px;
    background: #0A0D14 !important; /* PURE OBSIDIAN BLACK */
    border: 1px solid #1E293B;
    border-radius: 16px;
    margin-bottom: 20px;
    text-align: center;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
}}
.brand-title-wrap {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
}}
.brand-title {{
    color: #FFFFFF !important;
    font-size: 1.55rem;
    font-weight: 800;
    letter-spacing: -0.5px;
}}
.brand-sub {{
    color: #38BDF8 !important; /* ELECTRIC CYAN THEME ACCENT */
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.8px;
    margin-top: 6px;
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

/* CLINICAL CARDS */
.clinical-card {{
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 16px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.04);
}}

/* SMART VERTICAL DASHBOARD OVERLAY PANEL */
.vertical-drawer-overlay {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: #090D16;
    z-index: 999999;
    overflow-y: auto;
    padding: 24px;
    color: #FFFFFF;
    box-sizing: border-box;
}}

.drawer-welcome-card {{
    background: linear-gradient(135deg, #1E3A8A 0%, #0284C7 100%);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 8px 20px rgba(2, 132, 199, 0.25);
}}

.drawer-quick-btn {{
    background: #1E293B;
    border: 1px solid #334155;
    color: #F8FAFC !important;
    padding: 14px 18px;
    border-radius: 12px;
    margin-bottom: 10px;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 0.98rem;
    cursor: pointer;
}}

.drawer-feed-card {{
    background: #111827;
    border: 1px solid #1F2937;
    border-radius: 12px;
    padding: 14px 16px;
    margin-bottom: 12px;
}}

.drawer-bottom-nav {{
    display: flex;
    justify-content: space-around;
    background: #0F172A;
    border-top: 1px solid #1E293B;
    padding: 14px 0;
    position: sticky;
    bottom: 0;
    margin-top: 30px;
    border-radius: 12px;
}}

.stButton>button {{
    background: linear-gradient(90deg, #1E3A8A 0%, #0284C7 100%) !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    border-radius: 10px !important;
    border: none !important;
    padding: 10px 22px !important;
}}

/* FULLSCREEN LOADER OVERLAY */
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
.loader-title {{ font-size: 2.2rem; font-weight: 800; letter-spacing: 2px; }}
.loader-sub {{ font-size: 1.05rem; font-weight: 500; }}
</style>
"""
st.markdown(global_css, unsafe_allow_html=True)


# ==========================================
# 1. AVATAR ASSETS & INITIAL DATABASE
# ==========================================

LADY_DOCTOR_AVATAR = "https://cdn-icons-png.flaticon.com/512/387/387561.png"
MALE_PATIENT_AVATAR = "https://cdn-icons-png.flaticon.com/512/4140/4140048.png"
ADMIN_AVATAR = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"

if "users_db" not in st.session_state:
    st.session_state["users_db"] = {
        "admin@telerehab.com": {
            "user_id": "ADM-001", "proxy_id": "SUPER-ADMIN", "name": "Portal Super Admin",
            "role": "super_admin", "status": "ACTIVE", "password_hash": "admin123", "profile_pic": ADMIN_AVATAR
        },
        "patient@demo.com": {
            "user_id": "USR-P-101", "proxy_id": "TS-P-001", "name": "Muhammad Hassan Raza",
            "role": "patient", "status": "ACTIVE", "password_hash": "pass123", "phone": "+92 309 7964195", "profile_pic": MALE_PATIENT_AVATAR
        },
        "doctor@demo.com": {
            "user_id": "USR-D-909", "proxy_id": "TS-D-004", "name": "Dr. Ayesha Malik",
            "role": "doctor", "status": "ACTIVE", "phpc_num": "PHPC-88492-PAK", "specialty": "Orthopedic Specialist",
            "password_hash": "pass123", "profile_pic": LADY_DOCTOR_AVATAR
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

if "chat_messages" not in st.session_state:
    st.session_state["chat_messages"] = [
        {"sender": "TS-D-004", "text": "Hello! Please share your flexion progress image before our video session."},
        {"sender": "TS-P-001", "text": "Sure doctor, uploading right now."}
    ]


# ==========================================
# 2. HELPER UTILITIES & LOADERS
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
    time.sleep(1.2)
    ph.empty()


def add_audit_log(actor_proxy: str, action: str, details: str):
    st.session_state["audit_logs"].append({
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "actor": actor_proxy, "action": action, "details": details
    })


def render_top_right_profile_header():
    u = st.session_state["authenticated_user"]
    pic = u.get("profile_pic", MALE_PATIENT_AVATAR)

    c_left, c_right = st.columns([2.5, 1.5])
    with c_left:
        # DRAWER TRIGGER BUTTON TOP LEFT
        if st.button("☰ Smart Drawer Dashboard", key="btn_open_drawer"):
            st.session_state["drawer_open"] = True
            st.rerun()

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
# 3. VERTICAL DASHBOARD DRAWER OVERLAY
# ==========================================

if st.session_state["drawer_open"]:
    u_name = st.session_state["authenticated_user"]["name"]
    
    # Drawer Overlay Content
    st.markdown(f"""
    <div class="vertical-drawer-overlay">
        <!-- HEADER CLOSE BAR -->
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 20px;">
            <div style="font-weight:800; font-size:1.3rem; color:#38BDF8;">🩺 TeleRehab Smart Vertical Portal</div>
        </div>

        <!-- SECTION 1: WELCOME CARD -->
        <div class="drawer-welcome-card">
            <div style="font-size:0.85rem; text-transform:uppercase; opacity:0.8; font-weight:700;">Welcome Back</div>
            <div style="font-size:1.6rem; font-weight:800; margin-top:2px;">Good Morning, {u_name}</div>
            <div style="font-size:0.95rem; margin-top:8px; opacity:0.95; font-weight:600;">
                🟢 3 Patients Today | 📑 2 Pending Reports
            </div>
        </div>

        <!-- SECTION 2: QUICK ACTIONS VERTICAL BUTTONS -->
        <div style="margin-bottom: 22px;">
            <div style="font-size:0.85rem; color:#94A3B8; font-weight:700; text-transform:uppercase; margin-bottom:10px;">Quick Actions</div>
            <div class="drawer-quick-btn">▶️ Start New Tele-Rehab Session</div>
            <div class="drawer-quick-btn">📅 Book Patient Appointment</div>
            <div class="drawer-quick-btn">📊 View AI Rehabilitation Insights</div>
        </div>

        <!-- SECTION 3: AI HEALTH FEED -->
        <div style="margin-bottom: 22px;">
            <div style="font-size:0.85rem; color:#94A3B8; font-weight:700; text-transform:uppercase; margin-bottom:10px;">AI Health Feed</div>
            <div class="drawer-feed-card">
                <div style="color:#38BDF8; font-weight:700;">Patient Amina</div>
                <div style="color:#E2E8F0; font-size:0.9rem; margin-top:2px;">Shoulder mobility increased by <b>+20%</b> this week 📈</div>
            </div>
            <div class="drawer-feed-card">
                <div style="color:#F59E0B; font-weight:700;">Patient Ali</div>
                <div style="color:#E2E8F0; font-size:0.9rem; margin-top:2px;">Missed 2 assigned exercises. Send push reminder? 🔔</div>
            </div>
            <div class="drawer-feed-card">
                <div style="color:#10B981; font-weight:700;">Registration Alert</div>
                <div style="color:#E2E8F0; font-size:0.9rem; margin-top:2px;">New Doctor Registration Pending Approval in Admin Panel</div>
            </div>
        </div>

        <!-- SECTION 4: BOTTOM NAV INSIDE DASHBOARD -->
        <div class="drawer-bottom-nav">
            <span style="color:#38BDF8; font-weight:800;">🏠 Home</span>
            <span style="color:#94A3B8; font-weight:600;">👥 Patients</span>
            <span style="color:#94A3B8; font-weight:600;">📄 Reports</span>
            <span style="color:#94A3B8; font-weight:600;">⚙️ Settings</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("✖ Close Dashboard & Return", key="close_drawer_btn"):
        st.session_state["drawer_open"] = False
        st.rerun()

    st.stop()


# ==========================================
# 4. SIDEBAR NAVIGATION & BLACK BRANDING CARD
# ==========================================

# Sleek Black Header Container
st.sidebar.markdown("""
<div class="brand-container">
    <div class="brand-title-wrap">
        <span style="font-size: 1.6rem;">🩺</span>
        <span class="brand-title">TeleSynapse</span>
    </div>
    <div class="brand-sub">Clinical Tele-Rehab Portal</div>
</div>
""", unsafe_allow_html=True)

curr_user = st.session_state["authenticated_user"]

st.sidebar.markdown(f"""
<div class="user-info-card">
    <div style="font-size: 0.72rem; color: #64748B; font-weight: 800; text-transform: uppercase;">Active Session</div>
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

render_top_right_profile_header()


# ==========================================
# 5. MODULE 1: LOGIN & QUICK REGISTRATION
# ==========================================

if menu == "🔐 Login & Quick Registration":
    st.markdown("### 🔐 Multi-Role Authentication Gateway")
    st.caption("Supports Direct Profile Picture Upload & Fast Presets")

    col_av1, col_av2 = st.columns(2)
    with col_av1:
        if st.button("👩‍⚕️ Preset: Lady Doctor (Dr. Ayesha)"):
            st.session_state["preset_role"] = "Doctor"
            st.session_state["preset_name"] = "Dr. Ayesha Malik"
            st.session_state["preset_email"] = "doctor@demo.com"
            st.session_state["preset_pic"] = LADY_DOCTOR_AVATAR
            st.toast("Loaded Lady Doctor Preset!", icon="👩‍⚕️")

    with col_av2:
        if st.button("👨‍💼 Preset: Male Patient (Hassan Raza)"):
            st.session_state["preset_role"] = "Patient"
            st.session_state["preset_name"] = "Muhammad Hassan Raza"
            st.session_state["preset_email"] = "patient@demo.com"
            st.session_state["preset_pic"] = MALE_PATIENT_AVATAR
            st.toast("Loaded Male Patient Preset!", icon="👨‍💼")

    st.markdown("---")

    tab_login, tab_reg = st.tabs(["🔑 Sign In", "📝 Register & Upload Photo"])

    with tab_login:
        role_select = st.radio("Select Login Mode:", ["Patient", "Doctor", "Super Admin"], horizontal=True)
        login_email = st.text_input("Email Address", value="patient@demo.com" if role_select == "Patient" else ("doctor@demo.com" if role_select == "Doctor" else "admin@telerehab.com"))
        login_pass = st.text_input("Password", type="password", value="pass123" if role_select != "Super Admin" else "admin123")

        if st.button("SIGN IN TO PORTAL"):
            render_loader_component("Verifying Credentials...")
            user_entry = st.session_state["users_db"].get(login_email)

            if user_entry and user_entry["password_hash"] == login_pass:
                st.session_state["authenticated_user"] = user_entry
                add_audit_log(user_entry["proxy_id"], "LOGIN", f"Logged in as {role_select}")
                st.success(f"Welcome back, {user_entry['name']}!")
                st.rerun()
            else:
                st.error("Invalid Email or Password.")

    with tab_reg:
        r_name = st.text_input("Full Name", value=st.session_state.get("preset_name", ""))
        r_email = st.text_input("Email Address", value=st.session_state.get("preset_email", ""))
        r_pass = st.text_input("Create Password", type="password", value="pass123")
        
        uploaded_profile_file = st.file_uploader("Upload Profile Image", type=["jpg", "png", "jpeg"])
        final_pic = MALE_PATIENT_AVATAR
        if uploaded_profile_file:
            b64_str = base64.b64encode(uploaded_profile_file.getvalue()).decode()
            final_pic = f"data:image/jpeg;base64,{b64_str}"

        if st.button("CREATE ACCOUNT"):
            render_loader_component("Registering...")
            st.session_state["users_db"][r_email] = {
                "user_id": f"USR-{random.randint(1000,9999)}",
                "proxy_id": f"TS-P-{random.randint(100,999)}",
                "name": r_name, "role": "patient", "status": "ACTIVE",
                "password_hash": r_pass, "profile_pic": final_pic
            }
            st.success("🎉 Account Created!")


# ==========================================
# 6. MODULE 2: SUPER ADMIN PORTAL
# ==========================================

elif menu == "👑 Super Admin Portal (/admin/login)":
    if curr_user["role"] != "super_admin":
        st.warning("🔒 Access Denied. Super Admin privileges required.")
    else:
        st.markdown("### 👑 Super Admin Command Panel")
        st.success("🟢 All System Protocols & Data Enclaves Online.")


# ==========================================
# 7. MODULE 3: PATIENT PORTAL & SWIPER CAROUSEL
# ==========================================

elif menu == "👤 Patient Portal & Photo Suite":
    if curr_user["role"] != "patient":
        st.warning("⚠️ Access Restricted to Patient accounts.")
    else:
        st.markdown("### 👤 Patient Clinical Portal")
        
        # HORIZONTAL BLUR SLIDE CAROUSEL (SWIPER.JS ENGINE INTEGRATION)
        st.markdown("#### 🎯 Interactive Rehab Pose Gallery (Blur Slide Carousel)")
        
        carousel_html = """
        <!-- Swiper CSS -->
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css" />
        
        <style>
        body { margin: 0; background: transparent; font-family: sans-serif; }
        .swiper { width: 100%; padding-top: 20px; padding-bottom: 40px; }
        
        .swiper-slide {
            background-position: center;
            background-size: cover;
            width: 280px;
            height: 220px;
            background: #0F172A;
            border: 2px solid #0284C7;
            border-radius: 18px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            color: #FFFFFF;
            text-align: center;
            padding: 16px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            
            /* BLUR SLIDE CAROUSEL SPEC */
            transition: all 0.5s ease-in-out !important;
            filter: blur(6px) !important;
            opacity: 0.5 !important;
            transform: scale(0.88) !important;
        }

        .swiper-slide-active {
            filter: blur(0px) !important;
            opacity: 1 !important;
            transform: scale(1) !important;
            border-color: #38BDF8 !important;
            box-shadow: 0 12px 30px rgba(56, 189, 248, 0.3) !important;
        }

        .slide-title { font-size: 1.1rem; font-weight: 800; color: #38BDF8; margin-bottom: 6px; }
        .slide-desc { font-size: 0.85rem; color: #94A3B8; font-weight: 600; }
        .slide-badge { background: #0284C7; padding: 4px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 700; margin-top: 10px; }
        </style>

        <div class="swiper mySwiper">
            <div class="swiper-wrapper">
                <div class="swiper-slide">
                    <div style="font-size:2rem;">🦵</div>
                    <div class="slide-title">Knee Flexion Angle</div>
                    <div class="slide-desc">Target: 90° | Achieved: 85°</div>
                    <div class="slide-badge">Week 1 Frame</div>
                </div>
                <div class="swiper-slide">
                    <div style="font-size:2rem;">🏋️‍♂️</div>
                    <div class="slide-title">Quadriceps Extension</div>
                    <div class="slide-desc">15 Reps x 3 Sets</div>
                    <div class="slide-badge">Active Rehab</div>
                </div>
                <div class="swiper-slide">
                    <div style="font-size:2rem;">🏃‍♂️</div>
                    <div class="slide-title">Gait Symmetry Test</div>
                    <div class="slide-desc">Balance Index: 92%</div>
                    <div class="slide-badge">AI Verified</div>
                </div>
                <div class="swiper-slide">
                    <div style="font-size:2rem;">🧘‍♂️</div>
                    <div class="slide-title">Hamstring Stretch</div>
                    <div class="slide-desc">Flexibility +18%</div>
                    <div class="slide-badge">Completed</div>
                </div>
            </div>
            <div class="swiper-pagination"></div>
        </div>

        <!-- Swiper JS -->
        <script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css"></script>
        <script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>
        <script>
        var swiper = new Swiper(".mySwiper", {
            effect: "coverflow",
            grabCursor: true,
            centeredSlides: true,
            slidesPerView: "auto",
            coverflowEffect: {
                rotate: 0,
                stretch: 0,
                depth: 100,
                modifier: 1,
                slideShadows: false,
            },
            loop: true,
            pagination: {
                el: ".swiper-pagination",
                clickable: true,
            },
        });
        </script>
        """
        components.html(carousel_html, height=310)

        st.markdown("---")
        st.markdown("#### 💬 Encrypted Portal Chat")
        for msg in st.session_state["chat_messages"]:
            st.write(f"**{msg['sender']}:** {msg['text']}")


# ==========================================
# 8. MODULE 4 & 5: DOCTOR & REPORT BUILDER
# ==========================================

elif menu == "👨‍⚕️ Doctor Dashboard & Gallery":
    st.markdown("### 👨‍⚕️ Doctor Workspace")
    st.info("Patient Hassan Raza (`TS-P-001`) ACL Recovery Gallery Active.")

else:
    st.markdown("### 📄 AI Progress Report Generator")
    if st.button("⚙️ GENERATE CLINICAL REPORT PDF"):
        render_loader_component("Compiling AI Vision Metrics & Watermarking PDF...")
        st.success("🎉 Report PDF Generated & Sent to Patient Inbox!")


# ==========================================
# 9. FOOTER POLICY
# ==========================================

st.markdown("""
<div style="text-align:center; color:#64748B; font-size:0.8rem; margin-top:40px; padding-top:16px; border-top:1px solid #CBD5E1;">
    TeleSynapse — Secured Clinical Architecture & Data Enclave
</div>
""", unsafe_allow_html=True)
