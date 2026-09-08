import streamlit as st
import streamlit.components.v1 as components
import random
import time
import json
from datetime import datetime, date, timedelta

# ============================================================
# TELE SYNAPSE v2
# Clinical Tele-Rehabilitation Portal
# ============================================================

st.set_page_config(
    page_title="TeleSynapse | Tele-Rehabilitation",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(21, 190, 170, .12), transparent 25%),
        radial-gradient(circle at 90% 10%, rgba(60, 120, 255, .10), transparent 25%),
        #07111f;
    color: #f5f7fb;
}

.block-container {
    padding-top: 1.5rem;
    max-width: 1450px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #091525 0%, #07101c 100%);
    border-right: 1px solid rgba(255,255,255,.08);
}

section[data-testid="stSidebar"] * {
    color: #eaf2ff !important;
}

/* Cards */
.ts-card {
    background: linear-gradient(
        145deg,
        rgba(19,35,56,.96),
        rgba(9,20,35,.96)
    );
    border: 1px solid rgba(100,180,255,.13);
    border-radius: 20px;
    padding: 22px;
    margin-bottom: 18px;
    box-shadow: 0 12px 35px rgba(0,0,0,.20);
}

.hero {
    background:
        linear-gradient(120deg, rgba(0,205,180,.18), rgba(40,110,255,.16)),
        #0a1728;
    border: 1px solid rgba(67,220,205,.25);
    border-radius: 26px;
    padding: 30px;
    margin-bottom: 25px;
}

.hero-title {
    font-size: 38px;
    font-weight: 800;
    margin-bottom: 8px;
}

.hero-subtitle {
    color: #a9bfd8;
    font-size: 16px;
}

.metric {
    background: rgba(255,255,255,.035);
    border: 1px solid rgba(255,255,255,.07);
    padding: 18px;
    border-radius: 17px;
}

.metric-label {
    color: #91a8c0;
    font-size: 13px;
}

.metric-value {
    font-size: 29px;
    font-weight: 800;
    margin-top: 5px;
}

.metric-green {
    color: #36e0b6;
}

.metric-blue {
    color: #66a8ff;
}

.metric-orange {
    color: #ffbd69;
}

.metric-red {
    color: #ff7272;
}

.badge {
    display: inline-block;
    padding: 5px 11px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
    margin-right: 5px;
}

.badge-green {
    background: rgba(45,220,175,.14);
    color: #39e2b5;
}

.badge-blue {
    background: rgba(65,140,255,.14);
    color: #6aa9ff;
}

.badge-orange {
    background: rgba(255,170,60,.14);
    color: #ffbd69;
}

.badge-red {
    background: rgba(255,70,70,.14);
    color: #ff8585;
}

.section-title {
    font-size: 22px;
    font-weight: 800;
    margin-top: 15px;
    margin-bottom: 15px;
}

.small-muted {
    color: #8298b0;
    font-size: 13px;
}

.chat-user {
    background: rgba(50,120,255,.12);
    border-radius: 15px;
    padding: 12px;
    margin: 7px 0;
}

.chat-doctor {
    background: rgba(30,210,175,.10);
    border-radius: 15px;
    padding: 12px;
    margin: 7px 0;
}

.alert-box {
    border-left: 4px solid #ffbd69;
    background: rgba(255,189,105,.08);
    border-radius: 10px;
    padding: 15px;
}

.success-box {
    border-left: 4px solid #36e0b6;
    background: rgba(54,224,182,.08);
    border-radius: 10px;
    padding: 15px;
}

.danger-box {
    border-left: 4px solid #ff6565;
    background: rgba(255,101,101,.08);
    border-radius: 10px;
    padding: 15px;
}

.login-box {
    max-width: 520px;
    margin: 70px auto;
    background: rgba(12,27,45,.95);
    padding: 35px;
    border-radius: 28px;
    border: 1px solid rgba(100,180,255,.16);
    box-shadow: 0 25px 70px rgba(0,0,0,.35);
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "role" not in st.session_state:
    st.session_state.role = None

if "username" not in st.session_state:
    st.session_state.username = None

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if "active_call" not in st.session_state:
    st.session_state.active_call = False

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {
            "sender": "Dr. Ahmed",
            "text": "Welcome to TeleSynapse. Please upload your latest rehabilitation progress photo."
        },
        {
            "sender": "Patient",
            "text": "Thank you doctor. I will upload it today."
        }
    ]

if "uploaded_photo" not in st.session_state:
    st.session_state.uploaded_photo = None

if "exercise_completed" not in st.session_state:
    st.session_state.exercise_completed = 3


# ============================================================
# DEMO DATABASE
# ============================================================

USERS = {
    "patient": {
        "password": "1234",
        "role": "Patient",
        "name": "Muhammad Hassan Raza",
        "patient_id": "TS-P-001",
        "condition": "Knee Rehabilitation",
        "doctor": "Dr. Ahmed Khan"
    },

    "doctor": {
        "password": "1234",
        "role": "Doctor",
        "name": "Dr. Ahmed Khan",
        "doctor_id": "TS-D-004",
        "speciality": "Physical Medicine & Rehabilitation"
    }
}

if "patients" not in st.session_state:
    st.session_state.patients = [
        {
            "id": "TS-P-001",
            "name": "Muhammad Hassan Raza",
            "age": 24,
            "condition": "Knee Rehabilitation",
            "pain": 3,
            "rom": 112,
            "adherence": 86,
            "risk": "Low"
        },
        {
            "id": "TS-P-002",
            "name": "Ali Raza",
            "age": 42,
            "condition": "Shoulder Rehabilitation",
            "pain": 5,
            "rom": 86,
            "adherence": 72,
            "risk": "Medium"
        },
        {
            "id": "TS-P-003",
            "name": "Fatima Noor",
            "age": 31,
            "condition": "Post-Surgical Knee Rehab",
            "pain": 2,
            "rom": 121,
            "adherence": 94,
            "risk": "Low"
        },
        {
            "id": "TS-P-004",
            "name": "Usman Tariq",
            "age": 55,
            "condition": "Back Rehabilitation",
            "pain": 7,
            "rom": 64,
            "adherence": 61,
            "risk": "High"
        }
    ]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def metric_card(label, value, color="green", icon="●"):
    st.markdown(
        f"""
        <div class="metric">
            <div class="metric-label">{icon} {label}</div>
            <div class="metric-value metric-{color}">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def page_header(title, subtitle):
    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-title">{title}</div>
            <div class="hero-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def logout():
    st.session_state.authenticated = False
    st.session_state.role = None
    st.session_state.username = None
    st.session_state.page = "Dashboard"
    st.rerun()


# ============================================================
# LOGIN
# ============================================================

if not st.session_state.authenticated:

    st.markdown(
        """
        <div class="login-box">
            <h1 style="font-size:38px;">🩺 TeleSynapse</h1>
            <p style="color:#8fa8c1;">
                Intelligent Global Tele-Rehabilitation Platform
            </p>
            <hr>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.form("login_form"):

        role = st.selectbox(
            "Account Type",
            ["Patient", "Doctor"]
        )

        username = st.text_input(
            "Username",
            placeholder="patient / doctor"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Demo password: 1234"
        )

        submitted = st.form_submit_button(
            "🔐 Secure Login",
            use_container_width=True
        )

        if submitted:

            user = USERS.get(username.lower())

            if (
                user
                and user["password"] == password
                and user["role"] == role
            ):

                st.session_state.authenticated = True
                st.session_state.role = role
                st.session_state.username = username.lower()

                st.success("Login successful.")
                time.sleep(.5)
                st.rerun()

            else:
                st.error(
                    "Invalid demo credentials. "
                    "Try patient / 1234 or doctor / 1234."
                )

    st.markdown(
        """
        <div style="text-align:center;color:#7890aa;margin-top:20px;">
        🔒 Production version should use proper authentication,
        encrypted sessions and a real database.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

user = USERS[st.session_state.username]

with st.sidebar:

    st.markdown(
        """
        <h1 style="color:#3de1ba;">🩺 TeleSynapse</h1>
        <p style="color:#809ab5;">Tele-Rehabilitation OS</p>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown(
        f"""
        <div class="ts-card">
            <b>{user['name']}</b><br>
            <span class="small-muted">
                {user.get('patient_id', user.get('doctor_id'))}
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.session_state.role == "Patient":

        menu = [
            "Dashboard",
            "My Rehabilitation",
            "Exercises",
            "Progress Photos",
            "Appointments",
            "Teleconsultation",
            "Messages",
            "Billing & Payments",
            "My Profile"
        ]

    else:

        menu = [
            "Dashboard",
            "Patient Command Center",
            "Clinical Assessment",
            "Teleconsultation",
            "Messages",
            "Appointments",
            "Billing & Payments",
            "Reports"
        ]

    st.session_state.page = st.radio(
        "Navigation",
        menu,
        index=menu.index(st.session_state.page)
        if st.session_state.page in menu else 0
    )

    st.divider()

    st.markdown(
        """
        **System Status**

        🟢 Portal Online  
        🟢 Video Service Ready  
        🟢 Secure Messaging Ready
        """,
        unsafe_allow_html=True
    )

    if st.button("🚪 Logout", use_container_width=True):
        logout()


# ============================================================
# PATIENT DASHBOARD
# ============================================================

if st.session_state.role == "Patient" and st.session_state.page == "Dashboard":

    page_header(
        "Good morning, Muhammad 👋",
        "Your personalized rehabilitation command center."
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_card("Rehab Score", "87%", "green", "✦")

    with col2:
        metric_card("Exercise Adherence", "86%", "blue", "✓")

    with col3:
        metric_card("Pain Level", "3/10", "orange", "♥")

    with col4:
        metric_card("Knee ROM", "112°", "green", "↗")

    st.markdown("## Today's Rehabilitation Plan")

    c1, c2 = st.columns([2, 1])

    with c1:

        st.markdown(
            """
            <div class="ts-card">
                <h3>🦵 Knee Strengthening Program</h3>

                <span class="badge badge-green">ACTIVE</span>
                <span class="badge badge-blue">Week 6</span>

                <br><br>

                <b>Today's targets</b>

                <ul>
                    <li>Quadriceps activation — 3 × 12</li>
                    <li>Heel slides — 3 × 15</li>
                    <li>Straight leg raise — 3 × 10</li>
                    <li>5-minute mobility session</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button("▶ Start Today's Program", type="primary"):
            st.session_state.page = "Exercises"
            st.rerun()

    with c2:

        st.markdown(
            """
            <div class="ts-card">
                <h3>🧠 AI Rehab Insight</h3>
                <p>
                Your adherence is strong this week.
                Your recorded pain level has decreased.
                Continue your prescribed program and
                discuss any new symptoms with your clinician.
                </p>
                <span class="badge badge-green">
                POSITIVE TREND
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("## Recovery Analytics")

    a, b, c = st.columns(3)

    with a:
        st.metric("7-day average pain", "3.4", "-1.2")

    with b:
        st.metric("ROM improvement", "+18°", "12%")

    with c:
        st.metric("Weekly exercises", "21", "+4")

    st.markdown(
        """
        <div class="success-box">
        <b>✓ Rehabilitation milestone</b><br>
        You have completed 86% of your assigned exercises this week.
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# MY REHABILITATION
# ============================================================

elif st.session_state.role == "Patient" and st.session_state.page == "My Rehabilitation":

    page_header(
        "My Rehabilitation",
        "Your individualized rehabilitation pathway."
    )

    st.markdown(
        """
        <div class="ts-card">
        <h3>🦵 Diagnosis / Rehabilitation Pathway</h3>

        <b>Primary pathway:</b> Knee Rehabilitation

        <br><br>

        <span class="badge badge-blue">Phase 2</span>
        <span class="badge badge-green">Improving</span>

        <p class="small-muted">
        Treatment goals include mobility restoration,
        strength development, pain reduction and safe return
        to normal activity.
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    phases = [
        ("Phase 1", "Pain Control", "Completed"),
        ("Phase 2", "Mobility + Strength", "Current"),
        ("Phase 3", "Functional Training", "Upcoming"),
        ("Phase 4", "Return to Activity", "Upcoming")
    ]

    for phase, title, status in phases:

        col1, col2, col3 = st.columns([1, 3, 1])

        with col1:
            st.markdown(f"### {phase}")

        with col2:
            st.markdown(f"**{title}**")

        with col3:
            if status == "Completed":
                st.success("✓ Done")
            elif status == "Current":
                st.info("● Current")
            else:
                st.warning("Upcoming")


# ============================================================
# EXERCISES
# ============================================================

elif st.session_state.role == "Patient" and st.session_state.page == "Exercises":

    page_header(
        "Exercise Studio",
        "Complete your prescribed exercises and record your response."
    )

    exercises = [
        ("Quadriceps Activation", "3 × 12", "Beginner"),
        ("Heel Slides", "3 × 15", "Beginner"),
        ("Straight Leg Raise", "3 × 10", "Intermediate"),
        ("Knee Mobility", "5 minutes", "Beginner")
    ]

    for name, reps, level in exercises:

        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

        with col1:
            st.markdown(f"### 🏃 {name}")

        with col2:
            st.write(reps)

        with col3:
            st.write(level)

        with col4:
            if st.button("Complete", key=name):
                st.session_state.exercise_completed += 1
                st.success("Recorded!")

    st.markdown("### Daily Completion")

    progress = min(
        st.session_state.exercise_completed / 7,
        1.0
    )

    st.progress(progress)

    st.write(
        f"{st.session_state.exercise_completed}/7 rehabilitation activities recorded."
    )

    pain = st.slider(
        "How did your body feel after today's program?",
        0,
        10,
        3
    )

    notes = st.text_area(
        "Optional rehabilitation note"
    )

    if st.button("Save Session", type="primary"):

        st.success(
            f"Session saved. Reported discomfort: {pain}/10."
        )


# ============================================================
# PROGRESS PHOTOS
# ============================================================

elif st.session_state.role == "Patient" and st.session_state.page == "Progress Photos":

    page_header(
        "Progress Photo Lab",
        "Upload rehabilitation images for clinician review."
    )

    st.markdown(
        """
        <div class="alert-box">
        <b>Privacy reminder</b><br>
        Only upload images appropriate for your rehabilitation
        assessment. Production deployments should encrypt
        medical files and enforce role-based access.
        </div>
        """,
        unsafe_allow_html=True
    )

    uploaded = st.file_uploader(
        "Upload knee / rehabilitation photo",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded:

        st.session_state.uploaded_photo = uploaded

        col1, col2 = st.columns(2)

        with col1:
            st.image(
                uploaded,
                caption="Uploaded rehabilitation image",
                use_container_width=True
            )

        with col2:

            st.markdown(
                """
                <div class="ts-card">
                <h3>Clinical Submission</h3>

                <p>
                Image is ready for clinician review.
                </p>

                <span class="badge badge-blue">
                PENDING REVIEW
                </span>
                </div>
                """,
                unsafe_allow_html=True
            )

            body_side = st.selectbox(
                "Body side",
                ["Right", "Left", "Both"]
            )

            movement = st.selectbox(
                "Assessment type",
                [
                    "Knee Flexion",
                    "Knee Extension",
                    "Shoulder Range",
                    "Posture",
                    "Gait"
                ]
            )

            if st.button(
                "📤 Send to Clinician",
                type="primary"
            ):
                st.success(
                    "Progress photo submitted for clinician review."
                )


# ============================================================
# APPOINTMENTS
# ============================================================

elif st.session_state.page == "Appointments":

    page_header(
        "Appointments",
        "Manage your remote rehabilitation sessions."
    )

    st.markdown(
        """
        <div class="ts-card">
        <h3>📅 Upcoming Session</h3>

        <b>Dr. Ahmed Khan</b><br>
        Physical Medicine & Rehabilitation

        <br><br>

        📅 Tuesday, 15 September 2026<br>
        ⏰ 4:30 PM<br>
        🌐 Teleconsultation

        <br><br>

        <span class="badge badge-green">CONFIRMED</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("Request New Appointment")

    col1, col2, col3 = st.columns(3)

    with col1:
        appointment_date = st.date_input(
            "Preferred date",
            date.today() + timedelta(days=2)
        )

    with col2:
        appointment_time = st.selectbox(
            "Preferred time",
            ["10:00 AM", "12:00 PM", "3:00 PM", "4:30 PM", "6:00 PM"]
        )

    with col3:
        appointment_type = st.selectbox(
            "Session type",
            ["Follow-up", "Initial Assessment", "Exercise Review"]
        )

    if st.button("Request Appointment", type="primary"):

        st.success(
            f"Appointment request created for "
            f"{appointment_date} at {appointment_time}."
        )


# ============================================================
# TELECONSULTATION
# ============================================================

elif st.session_state.page == "Teleconsultation":

    page_header(
        "Tele-Rehabilitation Room",
        "Secure virtual rehabilitation session workspace."
    )

    if not st.session_state.active_call:

        st.markdown(
            """
            <div class="ts-card" style="text-align:center;">
                <div style="font-size:70px;">🎥</div>
                <h2>TeleSynapse Virtual Clinic</h2>
                <p class="small-muted">
                Your video consultation workspace is ready.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "📞 Start Teleconsultation",
            type="primary",
            use_container_width=True
        ):

            st.session_state.active_call = True
            st.rerun()

    else:

        st.markdown(
            """
            <div class="ts-card" style="text-align:center;">
            <div style="font-size:80px;">👨‍⚕️</div>
            <h2>Live Consultation</h2>
            <span class="badge badge-green">
            ● SESSION ACTIVE
            </span>
            </div>
            """,
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.button("🎤 Mute")

        with col2:
            st.button("📹 Camera")

        with col3:
            if st.button("🔴 End Session"):
                st.session_state.active_call = False
                st.rerun()

        st.info(
            "Demo teleconsultation interface. "
            "Connect a production WebRTC/video provider for real calls."
        )


# ============================================================
# MESSAGES
# ============================================================

elif st.session_state.page == "Messages":

    page_header(
        "Secure Messages",
        "Communication between patient and rehabilitation team."
    )

    for message in st.session_state.chat_messages:

        if message["sender"] == "Patient":

            st.markdown(
                f"""
                <div class="chat-user">
                <b>You</b><br>
                {message['text']}
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f"""
                <div class="chat-doctor">
                <b>{message['sender']}</b><br>
                {message['text']}
                </div>
                """,
                unsafe_allow_html=True
            )

    new_message = st.chat_input(
        "Write a message to your rehabilitation team..."
    )

    if new_message:

        st.session_state.chat_messages.append(
            {
                "sender": "Patient",
                "text": new_message
            }
        )

        st.rerun()


# ============================================================
# BILLING & PAYMENTS
# ============================================================

elif st.session_state.page == "Billing & Payments":

    page_header(
        "Billing & Payments",
        "Transparent rehabilitation billing and payment management."
    )

    # --------------------------------------------------------
    # PAYMENT SUMMARY
    # --------------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card(
            "Current Balance",
            "$45.00",
            "orange",
            "$"
        )

    with c2:
        metric_card(
            "Paid This Year",
            "$320",
            "green",
            "✓"
        )

    with c3:
        metric_card(
            "Invoices",
            "6",
            "blue",
            "▤"
        )

    with c4:
        metric_card(
            "Payment Status",
            "ACTIVE",
            "green",
            "●"
        )

    # --------------------------------------------------------
    # PAYMENT METHOD
    # --------------------------------------------------------

    st.markdown("## 💳 Payment Method")

    st.markdown(
        """
        <div class="ts-card">

        <span class="badge badge-green">SECURE</span>

        <h3>Visa •••• 4821</h3>

        <p class="small-muted">
        Default payment method
        </p>

        <p>
        TeleSynapse never stores your CVV or full card number.
        Production payments should be handled by a PCI-compliant
        payment provider.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("＋ Add / Change Payment Method"):

        st.info(
            "Production implementation: redirect to your "
            "PCI-compliant payment provider's hosted checkout."
        )

    # --------------------------------------------------------
    # PAYMENT
    # --------------------------------------------------------

    st.markdown("## 💰 Make a Payment")

    amount = st.selectbox(
        "Select invoice",
        [
            "$45.00 — Rehabilitation Follow-up",
            "$75.00 — Initial Assessment",
            "$30.00 — Exercise Review"
        ]
    )

    payment_method = st.selectbox(
        "Payment channel",
        [
            "Card",
            "Bank Transfer",
            "Insurance",
            "Provider Payment Link"
        ]
    )

    if st.button(
        "🔐 Proceed to Secure Payment",
        type="primary"
    ):

        st.success(
            "Payment request created. "
            "Connect Stripe/another payment processor "
            "to open the real hosted checkout."
        )

    # --------------------------------------------------------
    # INVOICES
    # --------------------------------------------------------

    st.markdown("## 🧾 Invoice History")

    invoices = [
        ["INV-1006", "15 Sep 2026", "$45.00", "Pending"],
        ["INV-1005", "01 Sep 2026", "$55.00", "Paid"],
        ["INV-1004", "15 Aug 2026", "$45.00", "Paid"],
        ["INV-1003", "01 Aug 2026", "$55.00", "Paid"]
    ]

    st.dataframe(
        invoices,
        column_config={
            0: "Invoice",
            1: "Date",
            2: "Amount",
            3: "Status"
        },
        hide_index=True,
        use_container_width=True
    )


# ============================================================
# PROFILE
# ============================================================

elif st.session_state.page == "My Profile":

    page_header(
        "My Profile",
        "Manage your TeleSynapse rehabilitation profile."
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            """
            <div class="ts-card">
            <h3>👤 Patient Information</h3>

            <b>Name</b><br>
            Muhammad Hassan Raza

            <br><br>

            <b>Patient ID</b><br>
            TS-P-001

            <br><br>

            <b>Rehabilitation pathway</b><br>
            Knee Rehabilitation

            <br><br>

            <b>Assigned clinician</b><br>
            Dr. Ahmed Khan
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        age = st.number_input(
            "Age",
            1,
            120,
            24
        )

        emergency = st.text_input(
            "Emergency contact"
        )

        language = st.selectbox(
            "Preferred language",
            [
                "English",
                "Urdu",
                "Arabic",
                "Hindi"
            ]
        )

        if st.button("Save Profile"):

            st.success("Profile updated.")


# ============================================================
# DOCTOR DASHBOARD
# ============================================================

elif st.session_state.role == "Doctor" and st.session_state.page == "Dashboard":

    page_header(
        "Clinical Command Center",
        "TeleSynapse rehabilitation operations dashboard."
    )

    total = len(st.session_state.patients)

    high_risk = len(
        [
            p for p in st.session_state.patients
            if p["risk"] == "High"
        ]
    )

    avg_adherence = int(
        sum(
            p["adherence"]
            for p in st.session_state.patients
        ) / total
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card("Active Patients", total, "blue", "👥")

    with c2:
        metric_card("High Risk", high_risk, "red", "⚠")

    with c3:
        metric_card("Avg Adherence", f"{avg_adherence}%", "green", "✓")

    with c4:
        metric_card("Today's Sessions", "8", "orange", "📅")

    st.markdown("## Patient Monitoring")

    for patient in st.session_state.patients:

        if patient["risk"] == "High":
            badge = "badge-red"
        elif patient["risk"] == "Medium":
            badge = "badge-orange"
        else:
            badge = "badge-green"

        st.markdown(
            f"""
            <div class="ts-card">

            <h3>{patient['name']}</h3>

            <span class="badge badge-blue">
            {patient['id']}
            </span>

            <span class="badge {badge}">
            {patient['risk']} Risk
            </span>

            <br><br>

            <b>Condition:</b> {patient['condition']}<br>
            <b>Pain:</b> {patient['pain']}/10<br>
            <b>ROM:</b> {patient['rom']}°<br>
            <b>Adherence:</b> {patient['adherence']}%

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# PATIENT COMMAND CENTER
# ============================================================

elif st.session_state.role == "Doctor" and st.session_state.page == "Patient Command Center":

    page_header(
        "Patient Command Center",
        "Monitor rehabilitation outcomes across your caseload."
    )

    selected = st.selectbox(
        "Select patient",
        [
            f"{p['id']} — {p['name']}"
            for p in st.session_state.patients
        ]
    )

    patient_id = selected.split(" — ")[0]

    patient = next(
        p for p in st.session_state.patients
        if p["id"] == patient_id
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card(
            "Pain",
            f"{patient['pain']}/10",
            "orange"
        )

    with c2:
        metric_card(
            "ROM",
            f"{patient['rom']}°",
            "green"
        )

    with c3:
        metric_card(
            "Adherence",
            f"{patient['adherence']}%",
            "blue"
        )

    with c4:
        metric_card(
            "Risk",
            patient["risk"],
            "red" if patient["risk"] == "High" else "green"
        )

    st.markdown("## Clinical Notes")

    note = st.text_area(
        "Add clinician note",
        placeholder="Document rehabilitation findings..."
    )

    if st.button("Save Clinical Note", type="primary"):
        st.success("Clinical note saved.")


# ============================================================
# CLINICAL ASSESSMENT
# ============================================================

elif st.session_state.role == "Doctor" and st.session_state.page == "Clinical Assessment":

    page_header(
        "Clinical Assessment Workspace",
        "Review patient-reported outcomes and rehabilitation measurements."
    )

    patient = st.selectbox(
        "Patient",
        [p["name"] for p in st.session_state.patients]
    )

    st.markdown("### Assessment")

    col1, col2 = st.columns(2)

    with col1:

        pain = st.slider(
            "Pain score",
            0,
            10,
            3
        )

        rom = st.number_input(
            "Range of Motion (degrees)",
            0,
            200,
            112
        )

    with col2:

        swelling = st.select_slider(
            "Swelling",
            options=["None", "Mild", "Moderate", "Severe"]
        )

        mobility = st.select_slider(
            "Functional mobility",
            options=[
                "Very limited",
                "Limited",
                "Moderate",
                "Good",
                "Excellent"
            ]
        )

    clinical_note = st.text_area(
        "Clinical assessment"
    )

    if st.button(
        "Save Assessment",
        type="primary"
    ):

        st.success(
            f"Assessment saved for {patient}."
        )


# ============================================================
# DOCTOR TELECONSULTATION
# ============================================================

elif st.session_state.role == "Doctor" and st.session_state.page == "Teleconsultation":

    page_header(
        "Virtual Clinic",
        "Start or manage scheduled patient consultations."
    )

    upcoming = st.selectbox(
        "Today's patient",
        [
            "Muhammad Hassan Raza — 4:30 PM",
            "Ali Raza — 5:00 PM",
            "Fatima Noor — 5:30 PM"
        ]
    )

    if not st.session_state.active_call:

        st.markdown(
            """
            <div class="ts-card" style="text-align:center;">
            <div style="font-size:70px;">🎥</div>
            <h2>Waiting Room</h2>
            <p class="small-muted">
            Patient connection is ready.
            </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "📞 Start Consultation",
            type="primary"
        ):

            st.session_state.active_call = True
            st.rerun()

    else:

        st.markdown(
            """
            <div class="ts-card" style="text-align:center;">
            <div style="font-size:75
