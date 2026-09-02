import streamlit as st
import pandas as pd

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="TeleSynapse Rehab | Executive Portal",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ADVANCED VIBRANT CLINICAL STYLING ---
st.markdown("""
    <style>
    /* Google Font Integration */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Main Canvas Background Gradient */
    .stApp {
        background: linear-gradient(135deg, #F0F4F8 0%, #E2E8F0 100%);
    }

    /* Sidebar - Deep Midnight Slate with Cyan Accents */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0B132B 0%, #1C2541 100%) !important;
        border-right: 2px solid #0EA5E9;
    }
    [data-testid="stSidebar"] * {
        color: #F1F5F9 !important;
    }

    /* Sidebar Title Styling */
    .sidebar-brand {
        font-size: 1.6rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38BDF8 0%, #818CF8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.5px;
        margin-bottom: 0px;
    }

    /* Main Section Header */
    .portal-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: -0.5px;
        margin-bottom: 2px;
    }
    .portal-sub {
        color: #475569;
        font-size: 0.95rem;
        font-weight: 600;
        margin-bottom: 25px;
    }

    /* Custom Metric Cards with Cyan & Indigo Borders */
    .metric-card {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.02);
        border-top: 4px solid #0EA5E9;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    }
    .metric-val {
        font-size: 2.3rem;
        font-weight: 800;
        color: #0EA5E9;
        line-height: 1;
        margin-top: 6px;
    }
    .metric-lbl {
        font-size: 0.78rem;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }

    /* Clinical Patient Cards */
    .roster-card {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 18px 22px;
        margin-bottom: 14px;
        border-left: 6px solid #0EA5E9;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.04);
    }
    .roster-card.pending {
        border-left-color: #F59E0B;
    }

    /* Glowing Status Badges */
    .badge-confirmed {
        background-color: #D1FAE5;
        color: #047857;
        font-weight: 800;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.75rem;
        letter-spacing: 0.5px;
    }
    .badge-pending {
        background-color: #FEF3C7;
        color: #B45309;
        font-weight: 800;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.75rem;
        letter-spacing: 0.5px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE STORAGE ---
if "appointments" not in st.session_state:
    st.session_state["appointments"] = [
        {"Patient": "Ali Ahmed", "Doctor": "Dr. Shahzaib", "Date": "2026-09-03", "Time": "10:00 AM", "Type": "Knee Rehab", "Status": "CONFIRMED"},
        {"Patient": "Sara Khan", "Doctor": "Dr. Hassan", "Date": "2026-09-03", "Time": "11:30 AM", "Type": "Shoulder Flexion", "Status": "PENDING"}
    ]

# --- 4. SIDEBAR NAVIGATION ---
st.sidebar.markdown('<p class="sidebar-brand">TELESYNAPSE</p>', unsafe_allow_html=True)
st.sidebar.markdown("<p style='font-size:0.8rem; color:#38BDF8 !important; margin-bottom:20px; font-weight:600;'>Enterprise Tele-Rehabilitation</p>", unsafe_allow_html=True)

menu = st.sidebar.radio("SYSTEM NAVIGATION", ["Clinician Overview", "Session Scheduler", "Patient Consultation Queue"])

st.sidebar.markdown("---")
st.sidebar.markdown("<p style='font-size:0.75rem; color:#94A3B8 !important;'>System Node: <b>ACTIVE (v2.8 Cyber-Teal)</b></p>", unsafe_allow_html=True)

# --- 5. MODULE 1: CLINICIAN OVERVIEW ---
if menu == "Clinician Overview":
    st.markdown('<p class="portal-header">Clinician Session Overview</p>', unsafe_allow_html=True)
    st.markdown('<p class="portal-sub">Real-time operational analytics & daily consultation roster for attending specialists.</p>', unsafe_allow_html=True)
    
    # Custom Gradient Stat Grid
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-lbl">Total Consults Today</div>
                <div class="metric-val">{len(st.session_state['appointments'])}</div>
            </div>
        """, unsafe_allow_html=True)
        
    with c2:
        confirmed_count = len([a for a in st.session_state["appointments"] if a["Status"] == "CONFIRMED"])
        st.markdown(f"""
            <div class="metric-card" style="border-top-color: #10B981;">
                <div class="metric-lbl">Confirmed Sessions</div>
                <div class="metric-val" style="color: #10B981;">{confirmed_count}</div>
            </div>
        """, unsafe_allow_html=True)
        
    with c3:
        pending_count = len([a for a in st.session_state["appointments"] if a["Status"] == "PENDING"])
        st.markdown(f"""
            <div class="metric-card" style="border-top-color: #F59E0B;">
                <div class="metric-lbl">Pending Queue</div>
                <div class="metric-val" style="color: #F59E0B;">{pending_count}</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><h4 style='color:#0F172A; font-weight:700;'>Scheduled Patient Roster</h4>", unsafe_allow_html=True)
    
    for app in st.session_state["appointments"]:
        badge_style = "badge-confirmed" if app["Status"] == "CONFIRMED" else "badge-pending"
        card_border = "roster-card" if app["Status"] == "CONFIRMED" else "roster-card pending"
        
        st.markdown(f"""
            <div class="{card_border}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 800; font-size: 1.15rem; color: #0F172A;">{app['Patient']}</span>
                    <span class="{badge_style}">{app['Status']}</span>
                </div>
                <div style="margin-top: 10px; color: #475569; font-size: 0.9rem;">
                    <span style="background:#F1F5F9; padding:4px 8px; border-radius:6px;"><b>Specialist:</b> {app['Doctor']}</span> &nbsp;
                    <span style="background:#F1F5F9; padding:4px 8px; border-radius:6px;"><b>Time:</b> {app['Time']} ({app['Date']})</span> &nbsp;
                    <span style="background:#F1F5F9; padding:4px 8px; border-radius:6px;"><b>Protocol:</b> {app['Type']}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

# --- 6. MODULE 2: SESSION SCHEDULER ---
elif menu == "Session Scheduler":
    st.markdown('<p class="portal-header">Session Scheduling Portal</p>', unsafe_allow_html=True)
    st.markdown('<p class="portal-sub">Register new patient profiles and assign rehabilitation specialists.</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("<h4 style='color:#0F172A; font-weight:700;'>Book New Consultation</h4>", unsafe_allow_html=True)
        patient_name = st.text_input("Patient Full Legal Name", placeholder="e.g. Usama Zahid")
        doctor_name = st.selectbox("Assign Specialist", ["Dr. Shahzaib Mughal", "Dr. Hassan Raza", "Dr. Ayesha Malik"])
        rehab_type = st.selectbox("Rehabilitation Focus", ["Knee ACL Protocol", "Shoulder Abduction Index", "Elbow Mobility Protocol", "Post-Stroke Assessment"])
        app_date = st.date_input("Consultation Date")
        app_time = st.selectbox("Time Slot", ["09:00 AM", "10:00 AM", "11:30 AM", "02:00 PM", "04:00 PM"])
        
        if st.button("Confirm Session Booking", type="primary"):
            if patient_name:
                new_app = {
                    "Patient": patient_name,
                    "Doctor": doctor_name,
                    "Date": str(app_date),
                    "Time": app_time,
                    "Type": rehab_type,
                    "Status": "CONFIRMED"
                }
                st.session_state["appointments"].append(new_app)
                st.success(f"Session registered for {patient_name} on {app_date} at {app_time}.")
            else:
                st.error("Patient legal name is required.")

    with col2:
        st.markdown("<h4 style='color:#0F172A; font-weight:700;'>Live System Register</h4>", unsafe_allow_html=True)
        df_apps = pd.DataFrame(st.session_state["appointments"])
        st.dataframe(df_apps, use_container_width=True)

# --- 7. MODULE 3: PATIENT CONSULTATION QUEUE ---
else:
    st.markdown('<p class="portal-header">Live Telehealth Lobby</p>', unsafe_allow_html=True)
    st.markdown('<p class="portal-sub">Virtual consultation rooms ready for real-time video streaming & biomechanical processing.</p>', unsafe_allow_html=True)
    st.info("System Ready: WebRTC video frame integration ready for Day 2 deployment.")
