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
# 0. GLOBAL PAGE CONFIG & CRISP LIGHT THEME
# ==========================================

st.set_page_config(
    page_title="TeleSynapse | Clinical Tele-Rehab Portal",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session States
if "drawer_open" not in st.session_state:
    st.session_state["drawer_open"] = False

if "active_call" not in st.session_state:
    st.session_state["active_call"] = False

if "chat_messages" not in st.session_state:
    st.session_state["chat_messages"] = [
        {"sender": "TS-D-004", "text": "Hello! Please share your flexion progress image before our video session."},
        {"sender": "TS-P-001", "text": "Sure doctor, uploading right now."}
    ]

# Background Dimming when Drawer is Open
drawer_dim_css = ""
if st.session_state["drawer_open"]:
    drawer_dim_css = """
    .stApp > div:nth-child(2), [data-testid="stSidebar"] {
        filter: blur(6px) brightness(0.7) !important;
        pointer-events: none !important;
        transition: all 0.3s ease-in-out !important;
    }
    """

# COMPLETE LIGHT THEME & INPUT / RADIO FIXES
global_css = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

#MainMenu {{ visibility: hidden !important; }}
footer {{ visibility: hidden !important; }}
.stDeployButton {{ display: none !important; }}
header[data-testid="stHeader"] {{ background-color: transparent !important; }}

{drawer_dim_css}

html, body, [class*="css"] {{
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}}

/* GLOBAL APP LIGHT BACKGROUND */
.stApp {{
    background-color: #F8FAFC !important;
    color: #0F172A !important;
}}

/* ALL INPUT FIELDS (TEXT, PASSWORD, SELECTBOX) FORCE WHITE */
div[data-baseweb="input"], 
div[data-baseweb="base-input"],
div[data-baseweb="input"] > div,
input[data-testid="stTextInput"],
input[type="text"],
input[type="password"] {{
    background-color: #FFFFFF !important;
    color: #0F172A !important;
    border: 1.5px solid #94A3B8 !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}}

div[data-baseweb="input"] input {{
    color: #0F172A !important;
    background-color: #FFFFFF !important;
}}

/* RADIO BUTTON ACCENT STYLING */
div[data-testid="stRadio"] label span p {{
    color: #0F172A !important;
    font-weight: 700 !important;
}}

div[data-baseweb="radio"] div {{
    background-color: #FFFFFF !important;
    border-color: #0284C7 !important;
}}

/* HEADINGS & LABELS */
h1, h2, h3 {{ color: #1E3A8A !important; font-weight: 800 !important; }}
h4, h5, h6 {{ color: #0284C7 !important; font-weight: 700 !important; }}

div[data-testid="stWidgetLabel"] p, 
label[data-testid="stWidgetLabel"] p {{
    color: #1E293B !important;
    font-weight: 700 !important;
}}

/* BUTTON STYLING */
div.stButton > button {{
    background: linear-gradient(135deg, #0284C7 0%, #1E3A8A 100%) !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 22px !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 14px rgba(2, 132, 199, 0.25) !important;
}}

div.stButton > button:hover {{
    background: linear-gradient(135deg, #0369A1 0%, #1D4ED8 100%) !important;
    transform: translateY(-1px) !important;
}}

/* SIDEBAR LIGHT STYLE */
[data-testid="stSidebar"] {{
    background-color: #FFFFFF !important;
    border-right: 1px solid #E2E8F0 !important;
}}

/* TOP LIGHT BRAND CARD */
.brand-container {{
    padding: 18px 16px;
    background: linear-gradient(135deg, #EFF6FF 0%, #E0F2FE 100%) !important;
    border: 1.5px solid #BAE6FD !important;
    border-radius: 16px;
    margin-bottom: 20px;
    text-align: center;
}}
.brand-title {{
    color: #1E3A8A !important;
    font-size: 1.45rem !important;
    font-weight: 800 !important;
}}
.brand-sub {{
    color: #0284C7 !important;
    font-size: 0.72rem !important;
    font-weight: 800 !important;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}}

/* USER SESSION CARD */
.user-info-card {{
    background: #F1F5F9;
    border: 1px solid #CBD5E1;
    border-radius: 10px;
    padding: 12px;
    margin-bottom: 20px;
}}

/* LIGHT THEME VERTICAL DASHBOARD OVERLAY */
.vertical-drawer-overlay {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: #F8FAFC;
    z-index: 999999;
    overflow-y: auto;
    padding: 30px;
    box-sizing: border-box;
}}

.drawer-card-light {{
    background: #FFFFFF;
    border: 1.5px solid #E2E8F0;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 16px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.03);
}}

.drawer-header-banner {{
    background: linear-gradient(135deg, #0284C7 0%, #1E3A8A 100%);
    color: #FFFFFF;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 24px;
    box-shadow: 0 8px 24px rgba(2, 132, 199, 0.2);
}}

/* TOP RIGHT PROFILE HEADER CARD */
.top-profile-badge {{
    display: flex;
    align-items: center;
    gap: 12px;
    background: #FFFFFF;
    border: 1px solid #CBD5E1;
    padding: 6px 16px;
    border-radius: 40px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}}
</style>
"""
st.markdown(global_css, unsafe_allow_html=True)


# ==========================================
# 1. DATABASE & USER SESSION
# ==========================================

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
# 2. TOP HEADER & NAVIGATION BAR
# ==========================================

def render_top_header():
    u = st.session_state["authenticated_user"]
    c_left, c_right = st.columns([2.5, 1.5])
    with c_left:
        if st.button("☰ Open Smart Drawer Dashboard", key="btn_open_drawer"):
            st.session_state["drawer_open"] = True
            st.rerun()

    with c_right:
        st.markdown(f"""
        <div style="display:flex; justify-content:flex-end;">
            <div class="top-profile-badge">
                <span style="font-size:1.5rem;">👤</span>
                <div style="text-align:left;">
                    <div style="font-weight:800; color:#1E3A8A; font-size:0.88rem; line-height:1.1;">{u['name']}</div>
                    <div style="color:#0284C7; font-size:0.75rem; font-weight:700;">{u['role'].upper()} | {u['proxy_id']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ==========================================
# 3. LIGHT-THEMED WORKING VERTICAL DRAWER
# ==========================================

if st.session_state["drawer_open"]:
    u_name = st.session_state["authenticated_user"]["name"]
    u_role = st.session_state["authenticated_user"]["role"].upper()
    
    st.markdown('<div class="vertical-drawer-overlay">', unsafe_allow_html=True)
    
    # Drawer Header
    c_dh1, c_dh2 = st.columns([4, 1])
    with c_dh1:
        st.markdown(f"""
        <div class="drawer-header-banner">
            <div style="font-size:0.85rem; text-transform:uppercase; font-weight:800; letter-spacing:1px; opacity:0.9;">Clinical Control Center</div>
            <div style="font-size:1.8rem; font-weight:800; margin-top:4px;">Welcome, {u_name}</div>
            <div style="font-size:0.95rem; margin-top:6px; opacity:0.95; font-weight:600;">
                🟢 Active Session | Role: {u_role} | 📑 2 Tele-Rehab Tasks Pending
            </div>
        </div>
        """, unsafe_allow_html=True)
    with c_dh2:
        if st.button("✖ Close Drawer", key="close_drawer_btn_top"):
            st.session_state["drawer_open"] = False
            st.rerun()

    # Drawer Actions
    st.markdown("### ⚡ Quick Interactive Actions")
    col_a1, col_a2, col_a3 = st.columns(3)
    
    with col_a1:
        st.markdown("""
        <div class="drawer-card-light">
            <h4 style="margin-top:0;">📹 Live Tele-Call</h4>
            <p style="font-size:0.88rem; color:#64748B;">Launch real-time video consultation with AI motion tracking.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("▶️ Launch Video Call Now", key="dw_action_call"):
            st.session_state["drawer_open"] = False
            st.session_state["active_call"] = True
            st.rerun()

    with col_a2:
        st.markdown("""
        <div class="drawer-card-light">
            <h4 style="margin-top:0;">📅 Book Appointment</h4>
            <p style="font-size:0.88rem; color:#64748B;">Schedule next physical therapy or evaluation slot.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📆 Schedule Slot", key="dw_action_book"):
            st.success("Appointment booking drawer slot reserved!")

    with col_a3:
        st.markdown("""
        <div class="drawer-card-light">
            <h4 style="margin-top:0;">📊 AI Insights</h4>
            <p style="font-size:0.88rem; color:#64748B;">View knee/shoulder flexion angles and recovery stats.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📈 View Recovery Metrics", key="dw_action_insights"):
            st.info("Knee Flexion angle improved +12° over last 7 days.")

    # Recent Patient Feed Section
    st.markdown("### 🔔 Active Portal Live Feed")
    st.markdown("""
    <div class="drawer-card-light" style="border-left: 5px solid #0284C7;">
        <div style="font-weight:800; color:#1E3A8A;">✅ Patient Motion Assessment Verified</div>
        <div style="color:#475569; font-size:0.9rem; margin-top:4px;">Gait balance score achieved <b>94% symmetry</b> in latest test.</div>
    </div>
    <div class="drawer-card-light" style="border-left: 5px solid #F59E0B;">
        <div style="font-weight:800; color:#1E3A8A;">⏰ Upcoming Video Call Session</div>
        <div style="color:#475569; font-size:0.9rem; margin-top:4px;">Scheduled with Dr. Ayesha Malik today at <b>04:00 PM PKT</b>.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()


# ==========================================
# 4. SIDEBAR NAVIGATION
# ==========================================

st.sidebar.markdown("""
<div class="brand-container">
    <div style="font-size:1.6rem; font-weight:800; color:#1E3A8A;">🩺 TeleSynapse</div>
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
    "📹 Live Tele-Rehab Call Suite",
    "👑 Super Admin Portal (/admin/login)",
    "👤 Patient Portal & Photo Suite",
    "👨‍⚕️ Doctor Dashboard & Gallery",
    "📄 AI Clinical Report Builder"
])

render_top_header()


# ==========================================
# 5. MODULE 1: LOGIN & REGISTRATION
# ==========================================

if menu == "🔐 Login & Quick Registration":
    st.markdown("### 🔐 Multi-Role Authentication Gateway")
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        if st.button("👩‍⚕️ Switch to Doctor (Dr. Ayesha)"):
            st.session_state["authenticated_user"] = st.session_state["users_db"]["doctor@demo.com"]
            st.success("Loaded Doctor Account!")
            st.rerun()
    with col_p2:
        if st.button("👨‍💼 Switch to Patient (Hassan Raza)"):
            st.session_state["authenticated_user"] = st.session_state["users_db"]["patient@demo.com"]
            st.success("Loaded Patient Account!")
            st.rerun()

    st.markdown("---")
    tab_login, tab_reg = st.tabs(["🔑 Sign In", "📝 Register New Account"])

    with tab_login:
        role_select = st.radio("Select Login Mode:", ["Patient", "Doctor", "Super Admin"], horizontal=True)
        login_email = st.text_input("Email Address", value="patient@demo.com" if role_select == "Patient" else ("doctor@demo.com" if role_select == "Doctor" else "admin@telerehab.com"))
        login_pass = st.text_input("Password", type="password", value="pass123" if role_select != "Super Admin" else "admin123")

        if st.button("SIGN IN TO PORTAL"):
            user_entry = st.session_state["users_db"].get(login_email)
            if user_entry and user_entry["password_hash"] == login_pass:
                st.session_state["authenticated_user"] = user_entry
                st.success(f"Welcome back, {user_entry['name']}!")
                st.rerun()
            else:
                st.error("Invalid Email or Password.")

    with tab_reg:
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


# ==========================================
# 6. MODULE 2: LIVE TELE-REHAB VIDEO CALL SUITE
# ==========================================

elif menu == "📹 Live Tele-Rehab Call Suite" or st.session_state["active_call"]:
    st.markdown("### 📹 Encrypted Tele-Rehab Video Consultation")
    st.write("Live WebRTC encrypted video stream with AI joint angle HUD overlay.")

    col_v1, col_v2 = st.columns([3, 1])

    with col_v1:
        # REAL WEBRTC WEBCAM FEED INTEGRATION
        webrtc_call_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { margin: 0; background-color: #0F172A; font-family: sans-serif; color: white; border-radius: 16px; overflow: hidden; }
                .call-container { position: relative; width: 100%; height: 420px; background: #1E293B; display: flex; align-items: center; justify-content: center; }
                video { width: 100%; height: 100%; object-fit: cover; }
                .hud-overlay {
                    position: absolute; top: 16px; left: 16px;
                    background: rgba(15, 23, 42, 0.75); backdrop-filter: blur(8px);
                    padding: 10px 16px; border-radius: 12px; border: 1px solid rgba(56, 189, 248, 0.3);
                }
                .controls-bar {
                    position: absolute; bottom: 16px; display: flex; gap: 12px;
                    background: rgba(15, 23, 42, 0.85); padding: 8px 16px; border-radius: 30px;
                }
                .btn {
                    background: #334155; color: white; border: none; padding: 10px 16px;
                    border-radius: 20px; font-weight: bold; cursor: pointer; display: flex; align-items: center; gap: 6px;
                }
                .btn-danger { background: #EF4444; }
                .btn-active { background: #0284C7; }
            </style>
        </head>
        <body>
            <div class="call-container">
                <video id="webcam" autoplay playsinline muted></video>
                <div class="hud-overlay">
                    <div style="color: #38BDF8; font-weight: bold; font-size: 0.85rem;">🟢 LIVE REHAB MOTION TRACKER</div>
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
                    } catch (err) {
                        console.log("Webcam access denied or unavailable", err);
                    }
                }
                startCamera();

                // Angle simulation
                setInterval(() => {
                    const angle = (85 + Math.random() * 8).toFixed(1);
                    document.getElementById('angle').innerText = angle + "°";
                }, 1200);

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
                    if (stream) {
                        stream.getTracks().forEach(track => track.stop());
                    }
                    video.srcObject = null;
                    alert("Call Ended Successfully.");
                }
            </script>
        </body>
        </html>
        """
        components.html(webrtc_call_html, height=430)

    with col_v2:
        st.markdown("#### 💬 Live In-Call Chat")
        for m in st.session_state["chat_messages"]:
            st.write(f"**{m['sender']}:** {m['text']}")
        
        new_m = st.text_input("Send message in call...", key="call_chat_in")
        if st.button("Send Message"):
            if new_m:
                st.session_state["chat_messages"].append({"sender": curr_user["proxy_id"], "text": new_m})
                st.rerun()


# ==========================================
# 7. OTHER MODULES (SUPER ADMIN / PATIENT / DOCTOR / REPORT)
# ==========================================

elif menu == "👑 Super Admin Portal (/admin/login)":
    if curr_user["role"] != "super_admin":
        st.warning("🔒 Access Denied. Super Admin privileges required.")
    else:
        st.markdown("### 👑 Super Admin Command Panel")
        st.success("🟢 All System Protocols & Data Enclaves Online.")

elif menu == "👤 Patient Portal & Photo Suite":
    st.markdown("### 👤 Patient Clinical Portal")
    st.info("Knee Flexion & Joint Pose Progress Dashboard Active.")

elif menu == "👨‍⚕️ Doctor Dashboard & Gallery":
    st.markdown("### 👨‍⚕️ Doctor Workspace")
    st.success("Dr. Ayesha Malik — Patient Queue Active.")

else:
    st.markdown("### 📄 AI Progress Report Generator")
    if st.button("⚙️ GENERATE CLINICAL REPORT PDF"):
        st.success("🎉 Report PDF Generated & Sent to Patient Inbox!")


# ==========================================
# 8. FOOTER
# ==========================================

st.markdown("""
<div style="text-align:center; color:#64748B; font-size:0.8rem; margin-top:40px; padding-top:16px; border-top:1px solid #CBD5E1;">
    TeleSynapse — Secured Clinical Architecture & Data Enclave
</div>
""", unsafe_allow_html=True)
