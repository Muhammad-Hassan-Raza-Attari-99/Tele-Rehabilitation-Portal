import streamlit as st
import streamlit.components.v1 as components
import random

# ==========================================
# 0. GLOBAL CONFIG & POPPINS FONT
# ==========================================

st.set_page_config(
    page_title="TeleSynapse | Clinical Tele-Rehab Portal",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Session state initialization
if "drawer_open" not in st.session_state:
    st.session_state["drawer_open"] = False

if "active_call" not in st.session_state:
    st.session_state["active_call"] = False

if "chat_messages" not in st.session_state:
    st.session_state["chat_messages"] = [
        {"sender": "TS-D-004", "text": "Hello! Please share your flexion progress image before our video session."},
        {"sender": "TS-P-001", "text": "Sure doctor, uploading right now."}
    ]

# RULE 4: DASHBOARD BEHAVIOR (DIMMING BACKGROUND WHEN DRAWER OPEN)
drawer_dim_css = ""
if st.session_state["drawer_open"]:
    drawer_dim_css = """
    .stApp > div:nth-child(2), [data-testid="stSidebar"] {
        filter: blur(6px) brightness(60%) !important;
        pointer-events: none !important;
        transition: all 0.3s ease-in-out !important;
    }
    """

# RULE 1, 2, 5: MEDICAL PREMIUM BLUE THEME & GLOBAL STYLING
global_css = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

#MainMenu {{ visibility: hidden !important; }}
footer {{ visibility: hidden !important; }}
.stDeployButton {{ display: none !important; }}
header[data-testid="stHeader"] {{ background-color: transparent !important; }}

{drawer_dim_css}

/* RULE 5: FONT & SPACING */
html, body, [class*="css"] {{
    font-family: 'Poppins', sans-serif !important;
}}

/* RULE 2: LOGIN PAGE BACKGROUND GRADIENT */
.stApp {{
    background: linear-gradient(180deg, #F4F7F9 0%, #FFFFFF 100%) !important;
    color: #1A1A1A !important;
}}

/* HEADINGS & TEXT */
h1, h2, h3 {{ color: #0A2342 !important; font-weight: 700 !important; font-family: 'Poppins', sans-serif !important; }}
h4, h5, h6 {{ color: #00BFA6 !important; font-weight: 600 !important; font-family: 'Poppins', sans-serif !important; }}
p, span, label {{ color: #1A1A1A !important; font-family: 'Poppins', sans-serif !important; }}

.sub-text {{
    color: #6C7A89 !important;
    font-size: 0.9rem;
}}

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
    padding: 6px 10px !important;
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
    font-size: 0.95rem !important;
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
    padding: 12px 26px !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
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

[data-testid="stSidebar"] * {{
    color: #FFFFFF !important;
}}

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

/* RULE 2.2: WHITE CARD CONTAINER */
.white-card {{
    background: #FFFFFF;
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 8px 24px rgba(10, 35, 66, 0.1);
    border: 1px solid #F0F4F8;
    margin-bottom: 20px;
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

/* BRAND HEADER CARD */
.brand-container {{
    padding: 20px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    margin-bottom: 24px;
    text-align: center;
}}

/* RULE 4: VERTICAL DRAWER OVERLAY */
.vertical-drawer-overlay {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
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
# 1. DATABASE & SESSION STATE
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
# 2. TOP HEADER BAR
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
            <div style="background:#FFFFFF; border:1px solid #E0E0E0; padding:8px 20px; border-radius:40px; box-shadow:0 4px 12px rgba(10,35,66,0.06); display:flex; align-items:center; gap:12px;">
                <span style="font-size:1.4rem;">👤</span>
                <div>
                    <div style="font-weight:700; color:#0A2342; font-size:0.9rem; line-height:1.1;">{u['name']}</div>
                    <div style="color:#00BFA6; font-size:0.75rem; font-weight:600;">{u['role'].upper()} | {u['proxy_id']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ==========================================
# 3. RULE 4: VERTICAL DRAWER DASHBOARD
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
            <p class="sub-text">Launch real-time video consultation with AI motion tracking.</p>
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
            <p class="sub-text">Schedule next physical therapy or evaluation slot.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📆 Schedule Slot", key="dw_action_book"):
            st.success("Appointment slot reserved successfully!")

    with col_a3:
        st.markdown("""
        <div class="white-card">
            <h4 style="margin-top:0;">📊 AI Insights</h4>
            <p class="sub-text">View knee/shoulder flexion angles and recovery stats.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📈 View Recovery Metrics", key="dw_action_insights"):
            st.info("Knee Flexion angle improved +12° over last 7 days.")

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()


# ==========================================
# 4. SIDEBAR NAVIGATION
# ==========================================

st.sidebar.markdown("""
<div class="brand-container">
    <div style="font-size:1.6rem; font-weight:700; color:#FFFFFF;">🩺 TeleSynapse</div>
    <div style="font-size:0.75rem; color:#00BFA6; font-weight:600; text-transform:uppercase; letter-spacing:1.5px; margin-top:4px;">Medical Tele-Rehab</div>
</div>
""", unsafe_allow_html=True)

curr_user = st.session_state["authenticated_user"]

st.sidebar.markdown(f"""
<div style="background: rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.1); border-radius:12px; padding:14px; margin-bottom:20px;">
    <div style="font-size: 0.72rem; color: #6C7A89; font-weight: 700; text-transform: uppercase;">Active User</div>
    <div style="font-size: 0.98rem; color: #FFFFFF; font-weight: 700; margin-top:2px;">{curr_user['name']}</div>
    <div style="font-size: 0.8rem; color: #00BFA6; font-weight: 600; margin-top:2px;">Role: {curr_user['role'].upper()}</div>
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
# 5. RULE 2 & 3: LOGIN PAGE + SWIPER.JS CAROUSEL
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

    # RULE 3: LOGIN MODE SELECTOR WITH SWIPER.JS V11 COVERFLOW & BLUR TRANSITION
    st.markdown("#### 🎯 Select Login Profile (*Swipe / Centered Coverflow*)")

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
                cursor: pointer;
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
                width: 10px;
                height: 10px;
                transition: all 0.3s ease;
            }
            .swiper-pagination-bullet-active {
                background: #00BFA6 !important;
                width: 26px !important;
                border-radius: 10px !important;
            }
            .role-badge {
                display: inline-block;
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 0.75rem;
                font-weight: 700;
                color: #FFFFFF;
                background: #0A2342;
                margin-bottom: 8px;
            }
            .role-title { font-weight: 700; color: #0A2342; font-size: 1.1rem; margin-bottom: 4px; }
            .role-desc { font-size: 0.82rem; color: #6C7A89; }
        </style>
    </head>
    <body>
        <div class="swiper mySwiper">
            <div class="swiper-wrapper">
                <div class="swiper-slide">
                    <div class="role-badge" style="background:#00BFA6;">PATIENT</div>
                    <div style="font-size: 2.2rem; margin: 4px 0;">👨‍💼</div>
                    <div class="role-title">Patient Portal</div>
                    <div class="role-desc">Access personal rehab plans, upload photos & join call</div>
                </div>
                <div class="swiper-slide">
                    <div class="role-badge">DOCTOR</div>
                    <div style="font-size: 2.2rem; margin: 4px 0;">👩‍⚕️</div>
                    <div class="role-title">Clinical Doctor Suite</div>
                    <div class="role-desc">Monitor joint angles, review uploads & conduct sessions</div>
                </div>
                <div class="swiper-slide">
                    <div class="role-badge" style="background:#0A2342;">SUPER ADMIN</div>
                    <div style="font-size: 2.2rem; margin: 4px 0;">👑</div>
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

    # LOGIN / REGISTRATION TABS
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
# 6. LIVE TELE-REHAB CALL SUITE
# ==========================================

elif menu == "📹 Live Tele-Rehab Call Suite" or st.session_state["active_call"]:
    st.markdown("### 📹 Encrypted Tele-Rehab Video Consultation")
    st.write("Live WebRTC encrypted video stream with AI joint angle HUD overlay.")

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
                    <div style="color: #00BFA6; font-weight: bold; font-size: 0.85rem;">🟢 LIVE REHAB MOTION TRACKER</div>
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
                        console.log("Webcam access denied", err);
                    }
                }
                startCamera();

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
                    if (stream) stream.getTracks().forEach(t => t.stop());
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
# 7. RULE 3: PATIENT PORTAL & SWIPER RECOVERY SLIDER
# ==========================================

elif menu == "👤 Patient Portal & Photo Suite":
    st.markdown("### 👤 Patient Clinical Progress Suite")
    st.markdown("#### 🎯 Recovery Pose & Flexion Slider (*Swiper.js v11 Coverflow*)")

    swiper_gallery_html = """
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
                width: 10px;
                height: 10px;
            }
            .swiper-pagination-bullet-active {
                background: #00BFA6 !important;
                width: 26px !important;
                border-radius: 10px !important;
            }
            .card-tag {
                background: #0A2342;
                color: #FFFFFF;
                font-size: 0.72rem;
                font-weight: 700;
                padding: 4px 12px;
                border-radius: 20px;
                display: inline-block;
                margin-bottom: 10px;
                text-transform: uppercase;
            }
            .card-stat { font-size: 1.5rem; font-weight: 700; color: #00BFA6; margin: 8px 0 4px 0; }
            .card-title { font-size: 1.1rem; font-weight: 700; color: #0A2342; }
            .card-desc { font-size: 0.85rem; color: #6C7A89; }
        </style>
    </head>
    <body>
        <div class="swiper gallerySwiper">
            <div class="swiper-wrapper">
                <div class="swiper-slide">
                    <div class="card-tag" style="background:#00BFA6;">ACL Week 2</div>
                    <div style="font-size: 2.5rem;">🦵</div>
                    <div class="card-title">Knee Flexion Angle</div>
                    <div class="card-stat">88.5° / 90°</div>
                    <div class="card-desc">Target angle almost reached. Mobility +12%</div>
                </div>
                <div class="swiper-slide">
                    <div class="card-tag">Active Therapy</div>
                    <div style="font-size: 2.5rem;">🏋️‍♂️</div>
                    <div class="card-title">Quadriceps Extension</div>
                    <div class="card-stat">3 Sets x 15 Reps</div>
                    <div class="card-desc">EMG Muscle activation score: 94%</div>
                </div>
                <div class="swiper-slide">
                    <div class="card-tag" style="background:#00BFA6;">AI Gait Test</div>
                    <div style="font-size: 2.5rem;">🏃‍♂️</div>
                    <div class="card-title">Gait Symmetry</div>
                    <div class="card-stat">92% Balance</div>
                    <div class="card-desc">Zero lateral limp detected in walk cycle</div>
                </div>
                <div class="swiper-slide">
                    <div class="card-tag">Rotator Cuff</div>
                    <div style="font-size: 2.5rem;">💪</div>
                    <div class="card-title">Shoulder Abduction</div>
                    <div class="card-stat">110° Angle</div>
                    <div class="card-desc">Full range overhead lift verified by AI</div>
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
    components.html(swiper_gallery_html, height=270)

    st.markdown("---")
    st.markdown("#### 💬 Encrypted Portal Chat")
    for msg in st.session_state["chat_messages"]:
        st.write(f"**{msg['sender']}:** {msg['text']}")


# ==========================================
# 8. OTHER PORTAL MODULES
# ==========================================

elif menu == "👑 Super Admin Portal (/admin/login)":
    if curr_user["role"] != "super_admin":
        st.warning("🔒 Access Denied. Super Admin privileges required.")
    else:
        st.markdown("### 👑 Super Admin Command Panel")
        st.success("🟢 All System Protocols & Data Enclaves Online.")

elif menu == "👨‍⚕️ Doctor Dashboard & Gallery":
    st.markdown("### 👨‍⚕️ Doctor Workspace")
    st.success("Dr. Ayesha Malik — Patient Queue Active.")

else:
    st.markdown("### 📄 AI Progress Report Generator")
    if st.button("⚙️ GENERATE CLINICAL REPORT PDF"):
        st.success("🎉 Report PDF Generated & Sent to Patient Inbox!")


# ==========================================
# 9. FOOTER
# ==========================================

st.markdown("""
<div style="text-align:center; color:#6C7A89; font-size:0.8rem; margin-top:40px; padding-top:16px; border-top:1px solid #E0E0E0;">
    TeleSynapse — Secured Clinical Architecture & Data Enclave
</div>
""", unsafe_allow_html=True)
