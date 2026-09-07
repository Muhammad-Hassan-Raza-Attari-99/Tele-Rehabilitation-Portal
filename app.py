import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import datetime
import random
import base64
import io

# ReportLab imports for clinical PDF report generation
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


# ==========================================
# 1. GLOBAL CONFIG & SESSION STATE
# ==========================================

st.set_page_config(
    page_title="TeleSynapse | Clinical Tele-Rehab Portal",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State Variables
if "preloaded" not in st.session_state:
    st.session_state["preloaded"] = False

if "drawer_open" not in st.session_state:
    st.session_state["drawer_open"] = False

if "active_call" not in st.session_state:
    st.session_state["active_call"] = False

# Database Mock
if "users_db" not in st.session_state:
    st.session_state["users_db"] = {
        "patient@demo.com": {
            "user_id": "USR-P-101",
            "proxy_id": "TS-P-001",
            "name": "Muhammad Hassan Raza",
            "role": "patient",
            "password_hash": "pass123",
            "phone": "+92 309 7964195",
            "diagnosis": "Right Knee ACL Reconstruction (Phase 2 Recovery)",
            "doctor_assigned": "Dr. Ayesha Malik"
        },
        "doctor@demo.com": {
            "user_id": "USR-D-909",
            "proxy_id": "TS-D-004",
            "name": "Dr. Ayesha Malik",
            "role": "doctor",
            "specialty": "Orthopedic Tele-Rehabilitation",
            "password_hash": "pass123"
        },
        "admin@telerehab.com": {
            "user_id": "ADM-001",
            "proxy_id": "SUPER-ADMIN",
            "name": "Portal Super Admin",
            "role": "super_admin",
            "password_hash": "admin123"
        }
    }

if "authenticated_user" not in st.session_state:
    st.session_state["authenticated_user"] = st.session_state["users_db"]["patient@demo.com"]

if "chat_messages" not in st.session_state:
    st.session_state["chat_messages"] = [
        {"sender": "TS-D-004 (Dr. Ayesha)", "text": "Assalamu Alaikum! Please check your flexion progress before our live session."},
        {"sender": "TS-P-001 (Hassan)", "text": "Walaikum Assalam Doctor, ready for the angle tracking test."}
    ]

if "clinical_history" not in st.session_state:
    st.session_state["clinical_history"] = pd.DataFrame([
        {"Date": "2026-09-01", "Knee Flexion (°)": 72.0, "Shoulder Abduction (°)": 105.0, "Gait Symmetry (%)": 82.0, "Pain Level (1-10)": 5},
        {"Date": "2026-09-03", "Knee Flexion (°)": 78.5, "Shoulder Abduction (°)": 110.0, "Gait Symmetry (%)": 86.5, "Pain Level (1-10)": 4},
        {"Date": "2026-09-05", "Knee Flexion (°)": 84.0, "Shoulder Abduction (°)": 118.0, "Gait Symmetry (%)": 89.0, "Pain Level (1-10)": 3},
        {"Date": "2026-09-07", "Knee Flexion (°)": 88.5, "Shoulder Abduction (°)": 125.0, "Gait Symmetry (%)": 92.0, "Pain Level (1-10)": 2},
    ])


# ==========================================
# 2. ANIMATED CLINICAL ECG PRELOADER
# ==========================================

if not st.session_state["preloaded"]:
    preloader_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@600;700&display=swap" rel="stylesheet">
        <style>
            body {
                margin: 0; background-color: #0A2342;
                display: flex; flex-direction: column; align-items: center; justify-content: center;
                height: 100vh; font-family: 'Poppins', sans-serif; color: #FFFFFF; overflow: hidden;
            }
            .ecg-box { position: relative; width: 320px; height: 100px; }
            .ecg-line {
                fill: none; stroke: #00BFA6; stroke-width: 3;
                stroke-dasharray: 1000; stroke-dashoffset: 1000;
                animation: dash 2.2s linear infinite;
            }
            @keyframes dash {
                to { stroke-dashoffset: 0; }
            }
            .pulse-ring {
                width: 60px; height: 60px; border: 3px solid #00BFA6; border-radius: 50%;
                position: absolute; animation: pulse 1.5s infinite;
            }
            @keyframes pulse {
                0% { transform: scale(0.8); opacity: 1; }
                100% { transform: scale(2.2); opacity: 0; }
            }
            .title { font-size: 1.4rem; font-weight: 700; margin-top: 20px; letter-spacing: 1px; color: #FFFFFF; }
            .sub { font-size: 0.85rem; color: #00BFA6; font-weight: 600; text-transform: uppercase; margin-top: 4px; }
            .progress-bar { width: 260px; height: 4px; background: rgba(255,255,255,0.1); border-radius: 4px; margin-top: 24px; overflow: hidden; }
            .progress-fill { width: 0%; height: 100%; background: #00BFA6; animation: fill 2s forwards; }
            @keyframes fill { to { width: 100%; } }
        </style>
    </head>
    <body>
        <div style="position:relative; display:flex; align-items:center; justify-content:center;">
            <div class="pulse-ring"></div>
            <div style="font-size:2rem; z-index:2;">🩺</div>
        </div>
        <div class="ecg-box">
            <svg viewBox="0 0 500 150" width="100%" height="100%">
                <path class="ecg-line" d="M0,75 L100,75 L120,40 L140,110 L160,10 L180,130 L200,75 L220,75 L240,50 L260,95 L280,75 L500,75" />
            </svg>
        </div>
        <div class="title">TELESYNAPSE CLINICAL PORTAL</div>
        <div class="sub">INITIALIZING ENCRYPTED TELE-REHAB ENCLAVE...</div>
        <div class="progress-bar"><div class="progress-fill"></div></div>
    </body>
    </html>
    """
    components.html(preloader_html, height=500)
    st.session_state["preloaded"] = True
    st.button("⚡ Click to Enter Portal System", key="skip_preload")
    st.stop()


# ==========================================
# 3. RULE 1, 2, 4, 5: STYLING & CUSTOM THEME
# ==========================================

drawer_dim_css = ""
if st.session_state["drawer_open"]:
    drawer_dim_css = """
    .stApp > div:nth-child(2), [data-testid="stSidebar"] {
        filter: blur(6px) brightness(60%) !important;
        pointer-events: none !important;
        transition: all 0.3s ease-in-out !important;
    }
    """

global_css = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

#MainMenu {{ visibility: hidden !important; }}
footer {{ visibility: hidden !important; }}
.stDeployButton {{ display: none !important; }}
header[data-testid="stHeader"] {{ background-color: transparent !important; }}

{drawer_dim_css}

/* RULE 5: FONT FAMILY & SPACING */
html, body, [class*="css"] {{
    font-family: 'Poppins', sans-serif !important;
}}

/* RULE 2: BACKGROUND GRADIENT */
.stApp {{
    background: linear-gradient(180deg, #F4F7F9 0%, #FFFFFF 100%) !important;
    color: #1A1A1A !important;
}}

/* HEADINGS & TYPOGRAPHY */
h1, h2, h3 {{ color: #0A2342 !important; font-weight: 700 !important; font-family: 'Poppins', sans-serif !important; }}
h4, h5, h6 {{ color: #00BFA6 !important; font-weight: 600 !important; font-family: 'Poppins', sans-serif !important; }}
p, span, label {{ color: #1A1A1A !important; font-family: 'Poppins', sans-serif !important; }}

.sub-text {{ color: #6C7A89 !important; font-size: 0.88rem; }}

/* RULE 2.4: INPUT FIELDS */
div[data-baseweb="input"], 
div[data-baseweb="base-input"],
input[data-testid="stTextInput"],
input[type="text"],
input[type="password"] {{
    background-color: #FFFFFF !important;
    color: #1A1A1A !important;
    border: 1.5px solid #D1D5DB !important;
    border-radius: 12px !important;
    font-weight: 500 !important;
    padding: 6px 12px !important;
    transition: all 0.3s ease-in-out !important;
}}

div[data-baseweb="input"]:focus-within {{
    border-color: #00BFA6 !important;
    box-shadow: 0 0 0 3px rgba(0, 191, 166, 0.25) !important;
}}

/* RULE 1 & 3: RADIO BUTTONS - NO RED/BLACK DOTS. ACTIVE = TEAL (#00BFA6), INACTIVE = #E0E0E0 */
div[data-testid="stRadio"] label p,
div[role="radiogroup"] label p {{
    color: #1A1A1A !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
}}

div[data-baseweb="radio"] > div:first-child {{
    border-color: #E0E0E0 !important;
    background-color: #FFFFFF !important;
}}

div[data-baseweb="radio"][aria-checked="true"] > div:first-child {{
    border-color: #00BFA6 !important;
    background-color: #00BFA6 !important;
}}

div[data-baseweb="radio"] div div {{
    background-color: #FFFFFF !important;
}}

/* RULE 2.5: BUTTON STYLING */
div.stButton > button {{
    background: linear-gradient(135deg, #0A2342 0%, #1E90FF 100%) !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 10px 24px !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    box-shadow: 0 4px 14px rgba(10, 35, 66, 0.2) !important;
    transition: all 0.3s ease !important;
}}

div.stButton > button:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(0, 191, 166, 0.3) !important;
}}

/* RULE 2.6: LEFT SIDEBAR */
[data-testid="stSidebar"] {{
    background-color: #0A2342 !important;
    border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
}}

[data-testid="stSidebar"] * {{ color: #FFFFFF !important; }}

[data-testid="stSidebar"] div[data-testid="stRadio"] label {{
    padding: 10px 14px;
    border-radius: 12px;
    transition: background 0.2s ease-in-out;
    margin-bottom: 4px;
}}

[data-testid="stSidebar"] div[data-testid="stRadio"] label:has(input:checked) {{
    background-color: #00BFA6 !important;
}}

[data-testid="stSidebar"] div[data-testid="stRadio"] label:has(input:checked) p {{
    color: #FFFFFF !important;
    font-weight: 700 !important;
}}

/* RULE 2.2: CARD CONTAINER */
.white-card {{
    background: #FFFFFF;
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 8px 24px rgba(10, 35, 66, 0.1);
    border: 1px solid #F0F4F8;
    margin-bottom: 20px;
}}

.stat-card {{
    background: #FFFFFF;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 4px 16px rgba(10, 35, 66, 0.08);
    border-left: 5px solid #00BFA6;
    margin-bottom: 16px;
}}

/* RULE 2.3: TAB OVERRIDES */
button[data-baseweb="tab"] {{
    color: #6C7A89 !important;
    font-weight: 600 !important;
}}

button[aria-selected="true"] {{
    color: #0A2342 !important;
    border-bottom-color: #00BFA6 !important;
    border-bottom-width: 3px !important;
}}

/* RULE 4: VERTICAL DRAWER OVERLAY */
.vertical-drawer-overlay {{
    position: fixed;
    top: 0; left: 0;
    width: 100vw; height: 100vh;
    background: #FFFFFF;
    z-index: 999999;
    overflow-y: auto;
    padding: 32px;
    box-sizing: border-box;
}}
</style>
"""
st.markdown(global_css, unsafe_allow_html=True)


# ==========================================
# 4. TOP HEADER BAR
# ==========================================

def render_top_header():
    u = st.session_state["authenticated_user"]
    c_left, c_right = st.columns([2.5, 1.5])
    with c_left:
        if st.button("☰ Open Dashboard Drawer Overlay", key="btn_open_drawer"):
            st.session_state["drawer_open"] = True
            st.rerun()

    with c_right:
        st.markdown(f"""
        <div style="display:flex; justify-content:flex-end;">
            <div style="background:#FFFFFF; border:1px solid #E0E0E0; padding:8px 20px; border-radius:40px; box-shadow:0 4px 12px rgba(10,35,66,0.06); display:flex; align-items:center; gap:12px;">
                <span style="font-size:1.3rem;">🩺</span>
                <div>
                    <div style="font-weight:700; color:#0A2342; font-size:0.88rem; line-height:1.1;">{u['name']}</div>
                    <div style="color:#00BFA6; font-size:0.75rem; font-weight:600;">{u['role'].upper()} | {u['proxy_id']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ==========================================
# 5. RULE 4: VERTICAL DRAWER OVERLAY
# ==========================================

if st.session_state["drawer_open"]:
    u = st.session_state["authenticated_user"]
    
    st.markdown('<div class="vertical-drawer-overlay">', unsafe_allow_html=True)
    
    c_dh1, c_dh2 = st.columns([4, 1])
    with c_dh1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #0A2342 0%, #1E90FF 100%); color:#FFFFFF; border-radius:16px; padding:28px; margin-bottom:24px; box-shadow: 0 8px 24px rgba(10,35,66,0.2);">
            <div style="font-size:0.8rem; text-transform:uppercase; font-weight:700; letter-spacing:1px; color:#00BFA6;">Clinical Tele-Rehab Drawer Dashboard</div>
            <div style="font-size:2.2rem; font-weight:700; margin-top:4px; color:#FFFFFF;">Welcome, {u['name']}</div>
            <div style="font-size:0.92rem; margin-top:6px; color:#E0E0E0;">
                🟢 System Online | Assigned ID: {u['proxy_id']} | Status: Active Protocol
            </div>
        </div>
        """, unsafe_allow_html=True)
    with c_dh2:
        if st.button("✖ Close Drawer", key="close_drawer_btn_top"):
            st.session_state["drawer_open"] = False
            st.rerun()

    st.markdown("### ⚡ Quick Clinical Actions")
    col_a1, col_a2, col_a3 = st.columns(3)
    
    with col_a1:
        st.markdown("""
        <div class="white-card">
            <h4 style="margin-top:0;">📹 Live Video Tele-Session</h4>
            <p class="sub-text">Launch real-time encrypted consultation with AI motion tracking HUD.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("▶️ Launch Video Suite", key="dw_action_call"):
            st.session_state["drawer_open"] = False
            st.session_state["active_call"] = True
            st.rerun()

    with col_a2:
        st.markdown("""
        <div class="white-card">
            <h4 style="margin-top:0;">📊 Motion Metrics Log</h4>
            <p class="sub-text">Log knee flexion, shoulder abduction, and gait balance scores.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📈 Open Patient Progress", key="dw_action_progress"):
            st.session_state["drawer_open"] = False
            st.rerun()

    with col_a3:
        st.markdown("""
        <div class="white-card">
            <h4 style="margin-top:0;">📄 PDF Report Generator</h4>
            <p class="sub-text">Compile progress logs and AI diagnosis into a printable PDF report.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📄 Build Report PDF", key="dw_action_report"):
            st.session_state["drawer_open"] = False
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()


# ==========================================
# 6. SIDEBAR NAVIGATION
# ==========================================

st.sidebar.markdown("""
<div style="padding:16px; background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); border-radius:16px; margin-bottom:20px; text-align:center;">
    <div style="font-size:1.5rem; font-weight:700; color:#FFFFFF;">🩺 TeleSynapse</div>
    <div style="font-size:0.75rem; color:#00BFA6; font-weight:600; text-transform:uppercase; letter-spacing:1px; margin-top:4px;">Clinical Tele-Rehab Portal</div>
</div>
""", unsafe_allow_html=True)

curr_u = st.session_state["authenticated_user"]

st.sidebar.markdown(f"""
<div style="background: rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.1); border-radius:12px; padding:12px; margin-bottom:16px;">
    <div style="font-size: 0.7rem; color: #6C7A89; font-weight: 700; text-transform: uppercase;">Active Session</div>
    <div style="font-size: 0.95rem; color: #FFFFFF; font-weight: 700;">{curr_u['name']}</div>
    <div style="font-size: 0.78rem; color: #00BFA6; font-weight: 600;">Role: {curr_u['role'].upper()}</div>
</div>
""", unsafe_allow_html=True)

menu = st.sidebar.radio("Navigation Menu", [
    "🔐 Login & Authentication",
    "📹 Live Tele-Rehab Video Suite",
    "👤 Patient Progress & Metrics",
    "👨‍⚕️ Doctor Roster & Workspace",
    "📄 AI Clinical Report Builder",
    "👑 Super Admin Audit Panel"
])

render_top_header()


# ==========================================
# 7. LOGIN PAGE & RULE 3: COVERFLOW CAROUSEL
# ==========================================

if menu == "🔐 Login & Authentication":
    st.markdown("### 🔐 Secure Multi-Role Portal Authentication")
    
    # Quick Switcher for Testing
    st.markdown("#### ⚡ Quick Switch Profiles (Developer Sandbox)")
    cq1, cq2, cq3 = st.columns(3)
    with cq1:
        if st.button("👨‍💼 Hassan Raza (Patient)"):
            st.session_state["authenticated_user"] = st.session_state["users_db"]["patient@demo.com"]
            st.success("Loaded Patient Account!")
            st.rerun()
    with cq2:
        if st.button("👩‍⚕️ Dr. Ayesha (Doctor)"):
            st.session_state["authenticated_user"] = st.session_state["users_db"]["doctor@demo.com"]
            st.success("Loaded Doctor Account!")
            st.rerun()
    with cq3:
        if st.button("👑 System Super Admin"):
            st.session_state["authenticated_user"] = st.session_state["users_db"]["admin@telerehab.com"]
            st.success("Loaded Admin Account!")
            st.rerun()

    st.markdown("---")

    # RULE 3: COVERFLOW CAROUSEL WITH BLUR TRANSITIONS & SNAP SCROLL
    st.markdown("#### 🎯 Clinical Access Modes (*Swipe / Coverflow Snap*)")

    swiper_login_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css" />
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700&display=swap" rel="stylesheet">
        <style>
            body { margin: 0; background: transparent; font-family: 'Poppins', sans-serif; }
            .swiper { width: 100%; padding: 20px 0 45px 0; }
            .swiper-slide {
                background: #FFFFFF;
                border-radius: 16px;
                padding: 20px;
                text-align: center;
                box-shadow: 0 8px 24px rgba(10,35,66,0.1);
                transition: all 500ms ease-in-out !important;
                filter: blur(6px);
                opacity: 0.5;
                transform: scale(0.9);
                border: 2px solid #E0E0E0;
                box-sizing: border-box;
            }
            .swiper-slide-active {
                filter: blur(0px) !important;
                opacity: 1 !important;
                transform: scale(1.0) !important;
                border-color: #00BFA6 !important;
            }
            /* RULE 3.6: INDICATOR DOTS ACTIVE = #00BFA6, INACTIVE = #E0E0E0 */
            .swiper-pagination-bullet {
                background: #E0E0E0 !important;
                opacity: 1 !important;
                width: 10px; height: 10px;
                transition: all 0.3s ease;
            }
            .swiper-pagination-bullet-active {
                background: #00BFA6 !important;
                width: 26px !important;
                border-radius: 10px !important;
            }
            .badge {
                display: inline-block; padding: 4px 12px; border-radius: 20px;
                font-size: 0.72rem; font-weight: 700; color: #FFFFFF; background: #0A2342;
                margin-bottom: 8px; text-transform: uppercase;
            }
            .title { font-weight: 700; color: #0A2342; font-size: 1.1rem; margin-bottom: 4px; }
            .desc { font-size: 0.82rem; color: #6C7A89; }
        </style>
    </head>
    <body>
        <div class="swiper mySwiper">
            <div class="swiper-wrapper">
                <div class="swiper-slide">
                    <div class="badge" style="background:#00BFA6;">PATIENT ACCESS</div>
                    <div style="font-size: 2.2rem; margin: 4px 0;">👨‍💼</div>
                    <div class="title">Patient Rehabilitation</div>
                    <div class="desc">Log joint angles, track flexion targets & join encrypted tele-consultations</div>
                </div>
                <div class="swiper-slide">
                    <div class="badge">DOCTOR ACCESS</div>
                    <div style="font-size: 2.2rem; margin: 4px 0;">👩‍⚕️</div>
                    <div class="title">Clinical Workspace</div>
                    <div class="desc">Manage patient rosters, review diagnostic history & evaluate AI motion tracking</div>
                </div>
                <div class="swiper-slide">
                    <div class="badge" style="background:#0A2342;">SUPER ADMIN</div>
                    <div style="font-size: 2.2rem; margin: 4px 0;">👑</div>
                    <div class="title">System Governance</div>
                    <div class="desc">Audit database compliance, manage credentials & review system logs</div>
                </div>
            </div>
            <div class="swiper-pagination"></div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>
        <script>
            const swiper = new Swiper('.mySwiper', {
                effect: 'coverflow',
                grabCursor: true,
                centeredSlides: true,
                slidesPerView: 1.2,
                spaceBetween: 20,
                coverflowEffect: {
                    rotate: 0,
                    stretch: 0,
                    depth: 80,
                    modifier: 1,
                    slideShadows: false,
                },
                speed: 500,
                pagination: {
                    el: '.swiper-pagination',
                    clickable: true,
                },
            });
        </script>
    </body>
    </html>
    """
    components.html(swiper_login_html, height=230)

    # LOGIN / REGISTER CARD
    tab_login, tab_reg = st.tabs(["🔑 Sign In", "📝 Register New User"])

    with tab_login:
        st.markdown('<div class="white-card">', unsafe_allow_html=True)
        role_sel = st.radio("Select Portal Role:", ["Patient", "Doctor", "Super Admin"], horizontal=True)
        
        default_email = "patient@demo.com"
        if role_sel == "Doctor": default_email = "doctor@demo.com"
        elif role_sel == "Super Admin": default_email = "admin@telerehab.com"
        
        email_input = st.text_input("Email Address", value=default_email)
        pass_input = st.text_input("Password", type="password", value="pass123" if role_sel != "Super Admin" else "admin123")

        if st.button("SIGN IN SECURELY"):
            user_rec = st.session_state["users_db"].get(email_input)
            if user_rec and user_rec["password_hash"] == pass_input:
                st.session_state["authenticated_user"] = user_rec
                st.success(f"Authenticated as {user_rec['name']} ({user_rec['role'].upper()})!")
                st.rerun()
            else:
                st.error("Invalid Email or Password.")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_reg:
        st.markdown('<div class="white-card">', unsafe_allow_html=True)
        r_role = st.selectbox("Role Type:", ["Patient", "Doctor"])
        r_name = st.text_input("Full Legal Name")
        r_email = st.text_input("Email Address for Registration")
        r_pass = st.text_input("Create Strong Password", type="password")
        
        if st.button("REGISTER ACCOUNT"):
            if r_email and r_name and r_pass:
                st.session_state["users_db"][r_email] = {
                    "user_id": f"USR-{random.randint(1000,9999)}",
                    "proxy_id": f"TS-{r_role[0]}-{random.randint(100,999)}",
                    "name": r_name,
                    "role": r_role.lower(),
                    "password_hash": r_pass
                }
                st.success("🎉 Account created successfully! Proceed to Sign In.")
            else:
                st.error("Please fill in all required registration fields.")
        st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# 8. LIVE TELE-REHAB VIDEO CALL SUITE
# ==========================================

elif menu == "📹 Live Tele-Rehab Video Suite" or st.session_state["active_call"]:
    st.markdown("### 📹 Encrypted WebRTC Video Consultation Suite")
    st.write("Live webcam stream with real-time simulated AI Knee Flexion HUD tracker and encrypted chat.")

    c_v1, c_v2 = st.columns([3, 1])

    with c_v1:
        webrtc_call_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { margin: 0; background-color: #0A2342; font-family: 'Poppins', sans-serif; color: white; border-radius: 16px; overflow: hidden; }
                .call-container { position: relative; width: 100%; height: 430px; background: #0A2342; display: flex; align-items: center; justify-content: center; }
                video { width: 100%; height: 100%; object-fit: cover; }
                .hud-overlay {
                    position: absolute; top: 16px; left: 16px;
                    background: rgba(10, 35, 66, 0.88); backdrop-filter: blur(8px);
                    padding: 12px 18px; border-radius: 14px; border: 1.5px solid #00BFA6;
                    box-shadow: 0 4px 16px rgba(0,0,0,0.3);
                }
                .hud-title { color: #00BFA6; font-weight: 700; font-size: 0.78rem; letter-spacing: 1px; text-transform: uppercase; }
                .hud-value { font-size: 1.3rem; font-weight: 800; margin-top: 2px; color: #FFFFFF; }
                .controls-bar {
                    position: absolute; bottom: 18px; display: flex; gap: 12px;
                    background: rgba(10, 35, 66, 0.92); padding: 10px 20px; border-radius: 30px;
                    border: 1px solid rgba(255,255,255,0.1);
                }
                .btn {
                    background: linear-gradient(135deg, #0A2342 0%, #1E90FF 100%); color: white; border: none; padding: 8px 16px;
                    border-radius: 20px; font-weight: 600; cursor: pointer; font-size: 0.85rem;
                }
                .btn-active { background: #00BFA6 !important; color: #FFFFFF !important; }
                .btn-danger { background: #D32F2F !important; }
            </style>
        </head>
        <body>
            <div class="call-container">
                <video id="webcam" autoplay playsinline muted></video>
                <div class="hud-overlay">
                    <div class="hud-title">🟢 AI MOTION TRACKER OVERLAY</div>
                    <div class="hud-value">Knee Angle: <span id="angle" style="color:#00BFA6;">88.5°</span></div>
                    <div style="font-size:0.75rem; color:#E0E0E0; margin-top:2px;">Target: 90.0° | Extension: 175.2°</div>
                </div>
                <div class="controls-bar">
                    <button class="btn btn-active" onclick="toggleCam()">📷 Camera</button>
                    <button class="btn btn-active" onclick="toggleMic()">🎙️ Mic</button>
                    <button class="btn btn-danger" onclick="endCall()">🛑 End Consult</button>
                </div>
            </div>

            <script>
                const video = document.getElementById('webcam');
                let stream = null;

                async function startCamera() {
                    try {
                        stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
                        video.srcObject = stream;
                    } catch (err) {
                        console.log("Webcam permission denied or unavailable", err);
                    }
                }
                startCamera();

                setInterval(() => {
                    const angle = (86 + Math.random() * 5).toFixed(1);
                    document.getElementById('angle').innerText = angle + "°";
                }, 1000);

                function toggleCam() {
                    if (stream) {
                        const track = stream.getVideoTracks()[0];
                        track.enabled = !track.enabled;
                    }
                }
                function toggleMic() {
                    if (stream) {
                        const track = stream.getAudioTracks()[0];
                        track.enabled = !track.enabled;
                    }
                }
                function endCall() {
                    if (stream) stream.getTracks().forEach(t => t.stop());
                    video.srcObject = null;
                    alert("Consultation ended.");
                }
            </script>
        </body>
        </html>
        """
        components.html(webrtc_call_html, height=440)

    with c_v2:
        st.markdown("#### 💬 Encrypted Call Chat")
        for m in st.session_state["chat_messages"]:
            st.write(f"**{m['sender']}:** {m['text']}")
        
        chat_in = st.text_input("Message...", key="in_call_chat_input")
        if st.button("Send", key="send_chat_btn"):
            if chat_in:
                st.session_state["chat_messages"].append({"sender": curr_u["proxy_id"], "text": chat_in})
                st.rerun()


# ==========================================
# 9. PATIENT PROGRESS & RULE 3 SLIDER
# ==========================================

elif menu == "👤 Patient Progress & Metrics":
    st.markdown("### 👤 Patient Clinical Progress & Angle Tracking")
    
    # RULE 3: RECOVERY METRICS CAROUSEL
    st.markdown("#### 🎯 Active Recovery Metrics (*Swiper Coverflow*)")

    swiper_metrics_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css" />
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700&display=swap" rel="stylesheet">
        <style>
            body { margin: 0; background: transparent; font-family: 'Poppins', sans-serif; }
            .swiper { width: 100%; padding: 20px 0 45px 0; }
            .swiper-slide {
                background: #FFFFFF;
                border-radius: 16px;
                padding: 24px;
                text-align: center;
                box-shadow: 0 8px 24px rgba(10,35,66,0.1);
                transition: all 500ms ease-in-out !important;
                filter: blur(6px);
                opacity: 0.5;
                transform: scale(0.9);
                border: 2px solid #E0E0E0;
                box-sizing: border-box;
            }
            .swiper-slide-active {
                filter: blur(0px) !important;
                opacity: 1 !important;
                transform: scale(1.0) !important;
                border-color: #00BFA6 !important;
            }
            .swiper-pagination-bullet {
                background: #E0E0E0 !important;
                opacity: 1 !important;
                width: 10px; height: 10px;
            }
            .swiper-pagination-bullet-active {
                background: #00BFA6 !important;
                width: 26px !important;
                border-radius: 10px !important;
            }
            .tag {
                background: #0A2342; color: #FFFFFF; font-size: 0.72rem; font-weight: 700;
                padding: 4px 12px; border-radius: 20px; display: inline-block; margin-bottom: 8px; text-transform: uppercase;
            }
            .val { font-size: 1.6rem; font-weight: 800; color: #00BFA6; margin: 4px 0; }
            .title { font-size: 1.05rem; font-weight: 700; color: #0A2342; }
            .desc { font-size: 0.82rem; color: #6C7A89; }
        </style>
    </head>
    <body>
        <div class="swiper metricsSwiper">
            <div class="swiper-wrapper">
                <div class="swiper-slide">
                    <div class="tag" style="background:#00BFA6;">ACL RECONSTRUCTION</div>
                    <div style="font-size: 2.2rem;">🦵</div>
                    <div class="title">Knee Flexion Angle</div>
                    <div class="val">88.5° / 90.0°</div>
                    <div class="desc">98.3% of target angle achieved</div>
                </div>
                <div class="swiper-slide">
                    <div class="tag">UPPER EXTREMITY</div>
                    <div style="font-size: 2.2rem;">💪</div>
                    <div class="title">Shoulder Abduction</div>
                    <div class="val">125.0° / 140.0°</div>
                    <div class="desc">Overhead mobility improving steadily</div>
                </div>
                <div class="swiper-slide">
                    <div class="tag" style="background:#00BFA6;">AI GAIT ANALYSIS</div>
                    <div style="font-size: 2.2rem;">🏃‍♂️</div>
                    <div class="title">Gait Symmetry</div>
                    <div class="val">92.0% Balance</div>
                    <div class="desc">Minimal limp detected during stride</div>
                </div>
            </div>
            <div class="swiper-pagination"></div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>
        <script>
            const metricsSwiper = new Swiper('.metricsSwiper', {
                effect: 'coverflow',
                grabCursor: true,
                centeredSlides: true,
                slidesPerView: 1.2,
                spaceBetween: 20,
                coverflowEffect: { rotate: 0, stretch: 0, depth: 80, modifier: 1, slideShadows: false },
                speed: 500,
                pagination: { el: '.swiper-pagination', clickable: true },
            });
        </script>
    </body>
    </html>
    """
    components.html(swiper_metrics_html, height=260)

    st.markdown('<div class="white-card">', unsafe_allow_html=True)
    st.markdown("#### 📝 Log New Motion Measurements")
    
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        new_knee = st.number_input("Knee Flexion Angle (°)", min_value=0.0, max_value=180.0, value=88.5)
    with col_m2:
        new_shoulder = st.number_input("Shoulder Abduction (°)", min_value=0.0, max_value=180.0, value=125.0)
    with col_m3:
        new_gait = st.number_input("Gait Symmetry (%)", min_value=0.0, max_value=100.0, value=92.0)

    if st.button("SAVE MEASUREMENTS TO ENCLAVE"):
        new_row = {
            "Date": datetime.date.today().strftime("%Y-%m-%d"),
            "Knee Flexion (°)": new_knee,
            "Shoulder Abduction (°)": new_shoulder,
            "Gait Symmetry (%)": new_gait,
            "Pain Level (1-10)": 2
        }
        st.session_state["clinical_history"] = pd.concat([
            st.session_state["clinical_history"],
            pd.DataFrame([new_row])
        ], ignore_index=True)
        st.success("✅ Measurement logged successfully!")
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("#### 📊 Clinical Measurement History")
    st.dataframe(st.session_state["clinical_history"], use_container_width=True)


# ==========================================
# 10. DOCTOR ROSTER & WORKSPACE
# ==========================================

elif menu == "👨‍⚕️ Doctor Roster & Workspace":
    st.markdown("### 👨‍⚕️ Clinical Doctor Workspace")
    st.write("Manage assigned patient recovery protocols and evaluate AI angle progression.")

    st.markdown('<div class="white-card">', unsafe_allow_html=True)
    st.markdown("#### 📋 Assigned Patients Roster")
    
    patients_df = pd.DataFrame([
        {"Proxy ID": "TS-P-001", "Patient Name": "Muhammad Hassan Raza", "Diagnosis": "ACL Reconstruction Phase 2", "Knee Angle": "88.5°", "Status": "Active Protocol"},
        {"Proxy ID": "TS-P-004", "Patient Name": "Ameer Hamza", "Diagnosis": "Rotator Cuff Tendinopathy", "Shoulder Angle": "112.0°", "Status": "Pending Session"},
    ])
    st.dataframe(patients_df, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="white-card">', unsafe_allow_html=True)
    st.markdown("#### 📑 Add Clinical Diagnosis & Session Notes")
    doc_notes = st.text_area("Clinical Notes & Progress Assessment", value="Patient exhibits strong knee flexion recovery (+16° over 14 days). Quad activation exercises prescribed.")
    if st.button("UPDATE CLINICAL FILE"):
        st.success("Saved clinical notes to patient enclave!")
    st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# 11. AI CLINICAL REPORT BUILDER (PDF)
# ==========================================

elif menu == "📄 AI Clinical Report Builder":
    st.markdown("### 📄 AI Clinical Report Generator & PDF Export")
    st.write("Compile real-time joint angle data and AI diagnostic assessments into an official printable PDF document.")

    st.markdown('<div class="white-card">', unsafe_allow_html=True)
    st.markdown("#### 📋 Report Configuration Settings")
    
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        rep_patient = st.text_input("Patient Name", value=curr_u["name"])
        rep_doctor = st.text_input("Attending Specialist", value="Dr. Ayesha Malik")
    with col_r2:
        rep_diagnosis = st.text_input("Clinical Diagnosis", value="Right Knee ACL Reconstruction (Phase 2 Recovery)")
        rep_recommendations = st.text_area("AI Clinical Recommendations", value="1. Increase knee flexion repetitions to 3 sets x 15 reps.\n2. Maintain gait symmetry above 90% during walking exercises.\n3. Re-evaluate flexion target in 7 days.")

    st.markdown('</div>', unsafe_allow_html=True)

    def generate_pdf():
        buffer = io.BytesIO()
        if REPORTLAB_AVAILABLE:
            doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
            styles = getSampleStyleSheet()
            story = []

            # Custom ReportLab Styles
            title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=20, textColor=colors.HexColor('#0A2342'), spaceAfter=6)
            sub_style = ParagraphStyle('SubStyle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor('#00BFA6'), spaceAfter=14)
            body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontName='Helvetica', fontSize=10, textColor=colors.HexColor('#1A1A1A'), spaceAfter=8)
            bold_style = ParagraphStyle('BoldStyle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor('#0A2342'))

            # Header
            story.append(Paragraph("TELESYNAPSE CLINICAL TELE-REHAB REPORT", title_style))
            story.append(Paragraph("OFFICIAL ENCRYPTED MEDICAL EVALUATION SUMMARY", sub_style))
            story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#00BFA6'), spaceAfter=14))

            # Patient Meta Table
            meta_data = [
                [Paragraph("<b>Patient Name:</b>", bold_style), Paragraph(rep_patient, body_style), Paragraph("<b>Date:</b>", bold_style), Paragraph(datetime.date.today().strftime("%Y-%m-%d"), body_style)],
                [Paragraph("<b>Specialist:</b>", bold_style), Paragraph(rep_doctor, body_style), Paragraph("<b>Diagnosis:</b>", bold_style), Paragraph(rep_diagnosis, body_style)]
            ]
            t_meta = Table(meta_data, colWidths=[110, 180, 80, 170])
            t_meta.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F4F7F9')),
                ('PADDING', (0,0), (-1,-1), 8),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ]))
            story.append(t_meta)
            story.append(Spacer(1, 16))

            # Metrics Table
            story.append(Paragraph("<b>Recorded Joint Angle Progress Metrics:</b>", bold_style))
            story.append(Spacer(1, 6))
            
            table_data = [["Date", "Knee Flexion (°)", "Shoulder Abduction (°)", "Gait Symmetry (%)", "Pain Score"]]
            for _, row in st.session_state["clinical_history"].iterrows():
                table_data.append([str(row["Date"]), str(row["Knee Flexion (°)"]), str(row["Shoulder Abduction (°)"]), str(row["Gait Symmetry (%)"]), str(row["Pain Level (1-10)"])])
            
            t_metrics = Table(table_data, colWidths=[100, 110, 120, 110, 100])
            t_metrics.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0A2342')),
                ('TEXTCOLOR', (0,0), (-1,0), colors.white),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E0E0E0')),
                ('PADDING', (0,0), (-1,-1), 6),
            ]))
            story.append(t_metrics)
            story.append(Spacer(1, 16))

            # AI Recommendations
            story.append(Paragraph("<b>AI & Clinical Recommendations:</b>", bold_style))
            story.append(Paragraph(rep_recommendations.replace('\n', '<br/>'), body_style))
            story.append(Spacer(1, 20))

            # Footer / Signatures
            story.append(Paragraph("<b>Attending Specialist Signature:</b> ___________________________", body_style))
            story.append(Paragraph("<i>TeleSynapse Cryptographic Audit Hash: TS-EVAL-909283742-SEC</i>", ParagraphStyle('Sub', fontName='Helvetica-Oblique', fontSize=8, textColor=colors.HexColor('#6C7A89'))))

            doc.build(story)
            buffer.seek(0)
            return buffer.getvalue()
        else:
            return b"ReportLab library not available. Please run `pip install reportlab`."

    pdf_bytes = generate_pdf()
    b64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
    
    st.download_button(
        label="📥 DOWNLOAD OFFICIAL CLINICAL REPORT PDF",
        data=pdf_bytes,
        file_name=f"TeleRehab_Report_{curr_u['name'].replace(' ', '_')}.pdf",
        mime="application/pdf"
    )


# ==========================================
# 12. SUPER ADMIN AUDIT PANEL
# ==========================================

elif menu == "👑 Super Admin Audit Panel":
    if curr_u["role"] != "super_admin":
        st.warning("🔒 Restricted Enclave. Super Admin authorization required.")
    else:
        st.markdown("### 👑 Portal Security & User Governance")
        st.markdown('<div class="white-card">', unsafe_allow_html=True)
        st.markdown("#### 👥 Registered Accounts & Roles Database")
        
        users_list = []
        for email, details in st.session_state["users_db"].items():
            users_list.append({
                "Email": email,
                "Name": details["name"],
                "Role": details["role"].upper(),
                "Proxy ID": details["proxy_id"],
                "Security Enclave": "🟢 Encrypted"
            })
        st.dataframe(pd.DataFrame(users_list), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# 13. GLOBAL FOOTER
# ==========================================

st.markdown("""
<div style="text-align:center; color:#6C7A89; font-size:0.8rem; margin-top:40px; padding-top:16px; border-top:1px solid #E0E0E0;">
    TeleSynapse — Secured Clinical Architecture & Data Enclave
</div>
""", unsafe_allow_html=True)
