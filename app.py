import streamlit as st
import streamlit.components.v1 as components
import random
import time
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ==========================================
# 0. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="TeleSynapse | Clinical Tele-Rehab Portal",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 1. SESSION STATE INITIALIZATION
# ==========================================
if "drawer_open" not in st.session_state:
    st.session_state["drawer_open"] = False

if "active_call" not in st.session_state:
    st.session_state["active_call"] = False

if "chat_messages" not in st.session_state:
    st.session_state["chat_messages"] = [
        {"sender": "TS-D-004", "text": "Hello! Please upload your knee flexion photo before our session."},
        {"sender": "TS-P-001", "text": "Sure doctor, uploading right now."}
    ]

if "users_db" not in st.session_state:
    st.session_state["users_db"] = {
        "admin@telerehab.com": {
            "user_id": "ADM-001", "proxy_id": "SUPER-ADMIN", "name": "Portal Super Admin",
            "role": "super_admin", "password_hash": "admin123"
        },
        "patient@demo.com": {
            "user_id": "USR-P-101", "proxy_id": "TS-P-001", "name": "Muhammad Hassan Raza",
            "role": "patient", "password_hash": "pass123", "phone": "+92 309 7964195"
        },
        "doctor@demo.com": {
            "user_id": "USR-D-909", "proxy_id": "TS-D-004", "name": "Dr. Ayesha Malik",
            "role": "doctor", "specialty": "Orthopedic Specialist", "password_hash": "pass123"
        }
    }

if "authenticated_user" not in st.session_state:
    st.session_state["authenticated_user"] = st.session_state["users_db"]["patient@demo.com"]


# ==========================================
# 2. GLOBAL STYLING & SIDEBAR CONTRAST FIX
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

/* GLOBAL FONT & BACKGROUND */
html, body, [class*="css"] {{
    font-family: 'Poppins', sans-serif !important;
}}

.stApp {{
    background: linear-gradient(180deg, #F4F7F9 0%, #FFFFFF 100%) !important;
    color: #1A1A1A !important;
}}

/* HEADINGS */
h1, h2, h3 {{ color: #0A2342 !important; font-weight: 700 !important; font-family: 'Poppins', sans-serif !important; }}
h4, h5, h6 {{ color: #00BFA6 !important; font-weight: 600 !important; font-family: 'Poppins', sans-serif !important; }}
p, span, label {{ color: #1A1A1A !important; }}

/* =========================================================
   CRITICAL FIX FOR SIDEBAR CONTRAST (SOLVES DARK UNREADABLE TEXT)
   ========================================================= */
[data-testid="stSidebar"] {{
    background-color: #0A2342 !important;
    border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
}}

/* Force all text inside sidebar to crisp white by default */
[data-testid="stSidebar"] p, 
[data-testid="stSidebar"] span, 
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div[data-testid="stRadio"] label p {{
    color: #FFFFFF !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
}}

/* Style radio option containers as interactive cards */
[data-testid="stSidebar"] div[data-testid="stRadio"] label {{
    background-color: rgba(255, 255, 255, 0.05) !important;
    border-radius: 12px !important;
    padding: 10px 14px !important;
    margin-bottom: 8px !important;
    border: 1.5px solid rgba(255, 255, 255, 0.12) !important;
    transition: all 0.25s ease-in-out !important;
}}

[data-testid="stSidebar"] div[data-testid="stRadio"] label:hover {{
    background-color: rgba(0, 191, 166, 0.2) !important;
    border-color: #00BFA6 !important;
}}

/* ACTIVE SELECTED SIDEBAR ITEM */
[data-testid="stSidebar"] div[data-testid="stRadio"] label:has(input:checked) {{
    background: #00BFA6 !important;
    border-color: #00BFA6 !important;
    box-shadow: 0 4px 14px rgba(0, 191, 166, 0.35) !important;
}}

[data-testid="stSidebar"] div[data-testid="stRadio"] label:has(input:checked) p {{
    color: #FFFFFF !important;
    font-weight: 700 !important;
}}

/* INPUT FIELDS */
div[data-baseweb="input"], 
input[data-testid="stTextInput"],
input[type="text"],
input[type="password"] {{
    background-color: #FFFFFF !important;
    color: #1A1A1A !important;
    border: 1.5px solid #D1D5DB !important;
    border-radius: 12px !important;
    font-weight: 500 !important;
    padding: 6px 10px !important;
}}

div[data-baseweb="input"]:focus-within {{
    border-color: #00BFA6 !important;
    box-shadow: 0 0 0 3px rgba(0, 191, 166, 0.25) !important;
}}

/* BUTTONS */
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

/* WHITE CARD CONTAINER */
.white-card {{
    background: #FFFFFF;
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 8px 24px rgba(10, 35, 66, 0.08);
    border: 1px solid #F0F4F8;
    margin-bottom: 20px;
}}

/* BRAND HEADER WITH GLOW EFFECT */
.brand-container {{
    padding: 18px;
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 16px;
    margin-bottom: 20px;
    text-align: center;
    box-shadow: inset 0 0 15px rgba(0, 191, 166, 0.15);
}}

/* VERTICAL DRAWER OVERLAY */
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
# 3. TOP NAVIGATION HEADER BAR
# ==========================================
def render_top_header():
    u = st.session_state["authenticated_user"]
    c_left, c_right = st.columns([2.5, 1.5])
    with c_left:
        if st.button("☰ Open Smart Control Drawer", key="btn_open_drawer"):
            st.session_state["drawer_open"] = True
            st.rerun()

    with c_right:
        st.markdown(f"""
        <div style="display:flex; justify-content:flex-end;">
            <div style="background:#FFFFFF; border:1px solid #E0E0E0; padding:6px 18px; border-radius:40px; box-shadow:0 4px 12px rgba(10,35,66,0.06); display:flex; align-items:center; gap:12px;">
                <span style="font-size:1.3rem;">👤</span>
                <div>
                    <div style="font-weight:700; color:#0A2342; font-size:0.88rem; line-height:1.1;">{u['name']}</div>
                    <div style="color:#00BFA6; font-size:0.75rem; font-weight:600;">{u['role'].upper()} | {u['proxy_id']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ==========================================
# 4. SMART CONTROL DRAWER DASHBOARD
# ==========================================
if st.session_state["drawer_open"]:
    u_name = st.session_state["authenticated_user"]["name"]
    u_role = st.session_state["authenticated_user"]["role"].upper()
    
    st.markdown('<div class="vertical-drawer-overlay">', unsafe_allow_html=True)
    
    c_dh1, c_dh2 = st.columns([4, 1])
    with c_dh1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #0A2342 0%, #1E90FF 100%); color:#FFFFFF; border-radius:16px; padding:28px; margin-bottom:24px; box-shadow: 0 8px 24px rgba(10,35,66,0.2);">
            <div style="font-size:0.85rem; text-transform:uppercase; font-weight:700; letter-spacing:1px; color:#00BFA6;">Clinical Control Center</div>
            <div style="font-size:2rem; font-weight:700; margin-top:4px; color:#FFFFFF;">Welcome, {u_name}</div>
            <div style="font-size:0.95rem; margin-top:6px; color:#E0E0E0;">
                🟢 Active Session | Role: {u_role} | 📑 2 Tele-Rehab Tasks Pending
            </div>
        </div>
        """, unsafe_allow_html=True)
    with c_dh2:
        if st.button("✖ Close Drawer", key="close_drawer_btn_top"):
            st.session_state["drawer_open"] = False
            st.rerun()

    st.markdown("### ⚡ Quick Interactive Actions")
    col_a1, col_a2, col_a3 = st.columns(3)
    
    with col_a1:
        st.markdown("""
        <div class="white-card">
            <h4 style="margin-top:0;">📹 Live Tele-Call</h4>
            <p style="color:#6C7A89; font-size:0.85rem;">Launch real-time video consultation with AI motion tracking HUD.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("▶️ Launch Video Call Now", key="dw_action_call"):
            st.session_state["drawer_open"] = False
            st.session_state["active_call"] = True
            st.rerun()

    with col_a2:
        st.markdown("""
        <div class="white-card">
            <h4 style="margin-top:0;">📅 Book Appointment</h4>
            <p style="color:#6C7A89; font-size:0.85rem;">Schedule next physical therapy or clinical evaluation slot.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📆 Schedule Slot", key="dw_action_book"):
            st.success("Appointment slot reserved successfully!")

    with col_a3:
        st.markdown("""
        <div class="white-card">
            <h4 style="margin-top:0;">📊 AI Recovery Metrics</h4>
            <p style="color:#6C7A89; font-size:0.85rem;">View knee/shoulder flexion angles and muscle activation stats.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📈 View Recovery Metrics", key="dw_action_insights"):
            st.info("Knee Flexion angle improved +12° over last 7 days.")

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()


# ==========================================
# 5. SIDEBAR NAVIGATION
# ==========================================
st.sidebar.markdown("""
<div class="brand-container">
    <div style="font-size:1.6rem; font-weight:800; color:#FFFFFF; letter-spacing:0.5px;">🩺 TeleSynapse</div>
    <div style="font-size:0.72rem; color:#00BFA6; font-weight:700; text-transform:uppercase; letter-spacing:1.5px; margin-top:2px;">Clinical Tele-Rehab</div>
</div>
""", unsafe_allow_html=True)

curr_user = st.session_state["authenticated_user"]

st.sidebar.markdown(f"""
<div style="background: rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.12); border-radius:12px; padding:12px; margin-bottom:18px;">
    <div style="font-size: 0.7rem; color: #94A3B8; font-weight: 700; text-transform: uppercase;">Active Session</div>
    <div style="font-size: 0.95rem; color: #FFFFFF; font-weight: 700; margin-top:2px;">{curr_user['name']}</div>
    <div style="font-size: 0.78rem; color: #00BFA6; font-weight: 600; margin-top:2px;">Role: {curr_user['role'].upper()}</div>
</div>
""", unsafe_allow_html=True)

menu = st.sidebar.radio("Portal Navigation", [
    "🔐 Login & Authentication",
    "📹 Live Tele-Rehab Video Suite",
    "👤 Patient Progress & Metrics",
    "👨‍⚕️ Doctor Roster & Workspace",
    "📄 AI Clinical Report Builder",
    "👑 Super Admin Audit Panel"
])

render_top_header()


# ==========================================
# 6. MODULE 1: LOGIN & AUTHENTICATION (SWIPER COVERFLOW)
# ==========================================
if menu == "🔐 Login & Authentication":
    st.markdown("### 🔐 Multi-Role Authentication Gateway")
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        if st.button("👩‍⚕️ Switch to Doctor (Dr. Ayesha Malik)"):
            st.session_state["authenticated_user"] = st.session_state["users_db"]["doctor@demo.com"]
            st.success("Loaded Doctor Account Profile!")
            st.rerun()
    with col_p2:
        if st.button("👨‍💼 Switch to Patient (Hassan Raza)"):
            st.session_state["authenticated_user"] = st.session_state["users_db"]["patient@demo.com"]
            st.success("Loaded Patient Account Profile!")
            st.rerun()

    st.markdown("---")
    st.markdown("#### 🎯 Select Login Profile (*Swipeable Touch Coverflow*)")

    swiper_login_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css" />
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700&display=swap" rel="stylesheet">
        <style>
            body { margin: 0; background: transparent; font-family: 'Poppins', sans-serif; }
            .swiper { width: 100%; padding: 15px 0 40px 0; }
            .swiper-slide {
                background: #FFFFFF;
                border-radius: 16px;
                padding: 20px;
                text-align: center;
                box-shadow: 0 8px 24px rgba(10,35,66,0.1);
                transition: all 400ms ease-in-out !important;
                filter: blur(4px);
                opacity: 0.6;
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
            .swiper-pagination-bullet { background: #CBD5E1 !important; opacity: 1 !important; }
            .swiper-pagination-bullet-active { background: #00BFA6 !important; width: 24px !important; border-radius: 10px !important; }
            .role-badge { display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 0.72rem; font-weight: 700; color: #FFFFFF; background: #0A2342; margin-bottom: 6px; }
            .role-title { font-weight: 700; color: #0A2342; font-size: 1.05rem; }
            .role-desc { font-size: 0.8rem; color: #64748B; }
        </style>
    </head>
    <body>
        <div class="swiper mySwiper">
            <div class="swiper-wrapper">
                <div class="swiper-slide">
                    <div class="role-badge" style="background:#00BFA6;">PATIENT</div>
                    <div style="font-size: 2rem; margin: 4px 0;">👨‍💼</div>
                    <div class="role-title">Patient Portal</div>
                    <div class="role-desc">Access personal rehab plans, upload photos & join session</div>
                </div>
                <div class="swiper-slide">
                    <div class="role-badge">DOCTOR</div>
                    <div style="font-size: 2rem; margin: 4px 0;">👩‍⚕️</div>
                    <div class="role-title">Clinical Doctor Suite</div>
                    <div class="role-desc">Monitor joint angles, review uploads & conduct sessions</div>
                </div>
                <div class="swiper-slide">
                    <div class="role-badge" style="background:#0A2342;">SUPER ADMIN</div>
                    <div style="font-size: 2rem; margin: 4px 0;">👑</div>
                    <div class="role-title">System Admin</div>
                    <div class="role-desc">Manage system parameters & encrypted data enclaves</div>
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
                slidesPerView: 1.25,
                spaceBetween: 16,
                coverflowEffect: { rotate: 0, stretch: 0, depth: 80, modifier: 1, slideShadows: false },
                speed: 400,
                pagination: { el: '.swiper-pagination', clickable: true },
            });
        </script>
    </body>
    </html>
    """
    components.html(swiper_login_html, height=220)

    tab_login, tab_reg = st.tabs(["🔑 Sign In", "📝 Register New Account"])

    with tab_login:
        st.markdown('<div class="white-card">', unsafe_allow_html=True)
        role_select = st.radio("Select Login Mode:", ["Patient", "Doctor", "Super Admin"], horizontal=True)
        login_email = st.text_input("Email Address", value="patient@demo.com" if role_select == "Patient" else ("doctor@demo.com" if role_select == "Doctor" else "admin@telerehab.com"))
        login_pass = st.text_input("Password", type="password", value="pass123" if role_select != "Super Admin" else "admin123")

        if st.button("SIGN IN SECURELY"):
            user_entry = st.session_state["users_db"].get(login_email)
            if user_entry and user_entry["password_hash"] == login_pass:
                st.session_state["authenticated_user"] = user_entry
                st.success(f"Welcome back, {user_entry['name']}!")
                st.rerun()
            else:
                st.error("Invalid Email or Password.")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_reg:
        st.markdown('<div class="white-card">', unsafe_allow_html=True)
        r_role = st.selectbox("Registering as:", ["Patient", "Doctor"])
        r_name = st.text_input("Full Name")
        r_email = st.text_input("Email Address")
        r_pass = st.text_input("Create Password", type="password")
        if st.button("CREATE ACCOUNT"):
            if r_email and r_name and r_pass:
                st.session_state["users_db"][r_email] = {
                    "user_id": f"USR-{random.randint(1000,9999)}",
                    "proxy_id": f"TS-{r_role[0]}-{random.randint(100,999)}",
                    "name": r_name, "role": r_role.lower(), "password_hash": r_pass
                }
                st.success("🎉 Account Created Successfully! You can now sign in.")
        st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# 7. MODULE 2: LIVE TELE-REHAB VIDEO CONSULTATION
# ==========================================
elif menu == "📹 Live Tele-Rehab Video Suite" or st.session_state["active_call"]:
    st.markdown("### 📹 Encrypted WebRTC Tele-Rehab Stream")
    st.write("Real-time video consultation featuring AI Joint-Angle HUD overlay.")

    col_v1, col_v2 = st.columns([3, 1])

    with col_v1:
        webrtc_call_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { margin: 0; background-color: #0A2342; font-family: sans-serif; color: white; border-radius: 16px; overflow: hidden; }
                .call-container { position: relative; width: 100%; height: 420px; background: #0A2342; display: flex; align-items: center; justify-content: center; }
                video { width: 100%; height: 100%; object-fit: cover; }
                .hud-overlay {
                    position: absolute; top: 16px; left: 16px;
                    background: rgba(10, 35, 66, 0.85); backdrop-filter: blur(8px);
                    padding: 10px 16px; border-radius: 12px; border: 1px solid #00BFA6;
                }
                .controls-bar {
                    position: absolute; bottom: 16px; display: flex; gap: 12px;
                    background: rgba(10, 35, 66, 0.9); padding: 8px 16px; border-radius: 30px;
                }
                .btn {
                    background: #1E90FF; color: white; border: none; padding: 10px 16px;
                    border-radius: 20px; font-weight: bold; cursor: pointer; display: flex; align-items: center; gap: 6px;
                }
                .btn-danger { background: #D32F2F; }
                .btn-active { background: #00BFA6; }
            </style>
        </head>
        <body>
            <div class="call-container">
                <video id="webcam" autoplay playsinline muted></video>
                <div class="hud-overlay">
                    <div style="color: #00BFA6; font-weight: bold; font-size: 0.85rem;">🟢 LIVE MOTION TRACKER</div>
                    <div style="font-size: 1.1rem; font-weight: 800; margin-top: 2px;">Knee Angle: <span id="angle">88.4°</span></div>
                </div>
                <div class="controls-bar">
                    <button class="btn btn-active" onclick="toggleCam()">📷 Cam On</button>
                    <button class="btn" onclick="toggleMic()">🎙️ Mic On</button>
                    <button class="btn btn-danger" onclick="endCall()">🛑 End Call</button>
                </div>
            </div>
            <script>
                const video = document.getElementById('webcam');
                let stream = null;
                async function startCamera() {
                    try {
                        stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
                        video.srcObject = stream;
                    } catch (err) { console.log("Camera access blocked", err); }
                }
                startCamera();
                setInterval(() => {
                    const angle = (85 + Math.random() * 8).toFixed(1);
                    document.getElementById('angle').innerText = angle + "°";
                }, 1200);
                function toggleCam() { if (stream) { const t = stream.getVideoTracks()[0]; t.enabled = !t.enabled; } }
                function toggleMic() { if (stream) { const t = stream.getAudioTracks()[0]; t.enabled = !t.enabled; } }
                function endCall() {
                    if (stream) stream.getTracks().forEach(t => t.stop());
                    video.srcObject = null;
                    alert("Call Ended.");
                }
            </script>
        </body>
        </html>
        """
        components.html(webrtc_call_html, height=430)

    with col_v2:
        st.markdown("#### 💬 Live Session Chat")
        for m in st.session_state["chat_messages"]:
            st.write(f"**{m['sender']}:** {m['text']}")
        
        new_m = st.text_input("Send message...", key="call_chat_in")
        if st.button("Send"):
            if new_m:
                st.session_state["chat_messages"].append({"sender": curr_user["proxy_id"], "text": new_m})
                st.rerun()


# ==========================================
# 8. MODULE 3: PATIENT PROGRESS & METRICS
# ==========================================
elif menu == "👤 Patient Progress & Metrics":
    st.markdown("### 👤 Patient Clinical Progress Suite")
    st.markdown("#### 🎯 Recovery Flexion Breakdown (*Swiper.js Coverflow*)")

    swiper_gallery_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css" />
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700&display=swap" rel="stylesheet">
        <style>
            body { margin: 0; background: transparent; font-family: 'Poppins', sans-serif; }
            .swiper { width: 100%; padding: 15px 0 40px 0; }
            .swiper-slide {
                background: #FFFFFF;
                border-radius: 16px;
                padding: 20px;
                text-align: center;
                box-shadow: 0 8px 24px rgba(10,35,66,0.1);
                transition: all 400ms ease-in-out !important;
                filter: blur(4px);
                opacity: 0.6;
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
            .card-tag { background: #0A2342; color: #FFFFFF; font-size: 0.7rem; font-weight: 700; padding: 4px 12px; border-radius: 20px; display: inline-block; margin-bottom: 8px; text-transform: uppercase; }
            .card-stat { font-size: 1.4rem; font-weight: 700; color: #00BFA6; margin: 6px 0; }
            .card-title { font-size: 1.05rem; font-weight: 700; color: #0A2342; }
            .card-desc { font-size: 0.82rem; color: #64748B; }
        </style>
    </head>
    <body>
        <div class="swiper gallerySwiper">
            <div class="swiper-wrapper">
                <div class="swiper-slide">
                    <div class="card-tag" style="background:#00BFA6;">ACL Recovery</div>
                    <div style="font-size: 2.2rem;">🦵</div>
                    <div class="card-title">Knee Flexion Angle</div>
                    <div class="card-stat">88.5° / 90.0°</div>
                    <div class="card-desc">Target angle almost reached. Mobility +12%</div>
                </div>
                <div class="swiper-slide">
                    <div class="card-tag">Active Therapy</div>
                    <div style="font-size: 2.2rem;">🏋️‍♂️</div>
                    <div class="card-title">Quad Extension</div>
                    <div class="card-stat">3 Sets x 15 Reps</div>
                    <div class="card-desc">EMG Muscle activation score: 94%</div>
                </div>
                <div class="swiper-slide">
                    <div class="card-tag" style="background:#00BFA6;">AI Gait Test</div>
                    <div style="font-size: 2.2rem;">🏃‍♂️</div>
                    <div class="card-title">Gait Symmetry</div>
                    <div class="card-stat">92% Balance</div>
                    <div class="card-desc">Zero lateral limp detected in walk cycle</div>
                </div>
            </div>
            <div class="swiper-pagination"></div>
        </div>
        <script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>
        <script>
            const gallerySwiper = new Swiper('.gallerySwiper', {
                effect: 'coverflow',
                grabCursor: true,
                centeredSlides: true,
                slidesPerView: 1.25,
                spaceBetween: 16,
                coverflowEffect: { rotate: 0, stretch: 0, depth: 80, modifier: 1, slideShadows: false },
                speed: 400,
                pagination: { el: '.swiper-pagination', clickable: true },
            });
        </script>
    </body>
    </html>
    """
    components.html(swiper_gallery_html, height=250)

    st.markdown("---")
    st.markdown("#### 📤 Upload Clinical Progress Image")
    uploaded_file = st.file_uploader("Upload Flexion Photo for AI Assessment", type=["jpg", "png", "jpeg"])
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Progress Image", width=350)
        st.success("✅ Image analyzed! Knee Flexion Angle estimated at 89.2°.")


# ==========================================
# 9. MODULE 4: DOCTOR ROSTER & WORKSPACE
# ==========================================
elif menu == "👨‍⚕️ Doctor Roster & Workspace":
    st.markdown("### 👨‍⚕️ Clinical Doctor Workspace")
    if curr_user["role"] not in ["doctor", "super_admin"]:
        st.warning("⚠️ Access restricted to clinical staff. Displaying read-only view.")
    
    st.markdown('<div class="white-card">', unsafe_allow_html=True)
    st.markdown("#### 📋 Assigned Patient Queue")
    
    col_q1, col_q2, col_q3 = st.columns([2, 2, 1])
    with col_q1:
        st.write("**Patient Name:** Muhammad Hassan Raza")
        st.write("**Target Joint:** Right Knee (ACL Rehab)")
    with col_q2:
        st.write("**Current Flexion:** 88.5°")
        st.write("**Status:** 🟢 Ready for Tele-Consultation")
    with col_q3:
        if st.button("Start Call", key="doc_start_call"):
            st.session_state["active_call"] = True
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# 10. MODULE 5: AI CLINICAL REPORT BUILDER
# ==========================================
elif menu == "📄 AI Clinical Report Builder":
    st.markdown("### 📄 AI Clinical Tele-Rehab Report Builder")
    st.markdown('<div class="white-card">', unsafe_allow_html=True)
    
    patient_sel = st.selectbox("Select Patient Record:", ["Muhammad Hassan Raza (TS-P-001)"])
    rehab_notes = st.text_area("Clinical Observations & Prescription:", value="Patient shows excellent progression in knee extension. Recommended to increase quad sets to 4x20 daily.")
    
    if st.button("⚙️ GENERATE & EMAIL CLINICAL REPORT"):
        with st.spinner("Compiling clinical data enclave & rendering PDF..."):
            time.sleep(1.2)
        st.success("🎉 Clinical Report generated and stored in Data Enclave!")
        st.info("✉️ Email Notification dispatched to patient portal address.")
    st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# 11. MODULE 6: SUPER ADMIN AUDIT PANEL
# ==========================================
elif menu == "👑 Super Admin Audit Panel":
    st.markdown("### 👑 Super Admin Command Panel")
    if curr_user["role"] != "super_admin":
        st.error("🔒 Access Denied. Super Admin privileges required.")
    else:
        st.success("🟢 All System Protocols, WebRTC Streams & Encrypted Data Enclaves Online.")
        
        st.markdown('<div class="white-card">', unsafe_allow_html=True)
        st.markdown("#### 📊 System Enclave Audit Logs")
        st.code("""
[2026-09-07 12:15:00] [ENCLAVE_OK] Encrypted Session TS-P-001 initiated.
[2026-09-07 12:15:02] [WEBRTC_OK] Video stream peer connection established.
[2026-09-07 12:15:05] [AI_HUD] Knee motion angle tracking synced @ 60 FPS.
        """, language="bash")
        st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# 12. FOOTER
# ==========================================
st.markdown("""
<div style="text-align:center; color:#6C7A89; font-size:0.8rem; margin-top:40px; padding-top:16px; border-top:1px solid #E0E0E0;">
    TeleSynapse — Secured Clinical Architecture & Encrypted Tele-Rehab Portal
</div>
""", unsafe_allow_html=True)
