import streamlit as st
import sqlite3
import json
from datetime import datetime, date
from pathlib import Path

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="TeleRehabilitation Portal",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

DB_FILE = "tele_rehabilitation.db"

# ==========================================
# 2. DATABASE INITIALIZATION & QUERIES
# ==========================================
def get_connection():
    return sqlite3.connect(DB_FILE, check_same_thread=False)

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    
    # Corrected SQL table schema with valid column names
    cur.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        patient_id TEXT PRIMARY KEY,
        full_name TEXT,
        date_of_birth TEXT,
        sex TEXT,
        phone TEXT,
        email TEXT,
        country TEXT,
        city TEXT,
        preferred_language TEXT,
        emergency_contact TEXT,
        emergency_phone TEXT,
        diagnosis TEXT,
        diagnosis_date TEXT,
        affected_organ TEXT,
        affected_side TEXT,
        diagnosis_notes TEXT,
        status TEXT
    )
    """)
    
    # Seed default record if empty
    cur.execute("SELECT COUNT(*) FROM patients")
    if cur.fetchone()[0] == 0:
        cur.execute("""
        INSERT INTO patients (
            patient_id, full_name, date_of_birth, sex, phone, email, country, city, 
            preferred_language, emergency_contact, emergency_phone, diagnosis, 
            diagnosis_date, affected_organ, affected_side, diagnosis_notes, status
        ) VALUES (
            'TRP-1001', 'Muhammad Hassan Raza Attari', '2005-10-14', 'Male', '+92 300 1234567',
            'hassan@example.com', 'Pakistan', 'Sheikhupura', 'English', 'Family Member',
            '+92 300 7654321', 'Post-Op Knee Flexion Rehab', '2026-08-15', 'Knee Joint',
            'Left', 'Patient requires daily flexion exercises and tele-consultation tracking.', 'Active'
        )
        """)
        conn.commit()
    conn.close()

init_db()

def get_patient(patient_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM patients WHERE patient_id = ?", (patient_id,))
    row = cur.fetchone()
    conn.close()
    if row:
        cols = [
            "patient_id", "full_name", "date_of_birth", "sex", "phone", "email", 
            "country", "city", "preferred_language", "emergency_contact", 
            "emergency_phone", "diagnosis", "diagnosis_date", "affected_organ", 
            "affected_side", "diagnosis_notes", "status"
        ]
        return dict(zip(cols, row))
    return None

# ==========================================
# 3. HIGH-CONTRAST VISUAL FIX (CUSTOM CSS)
# ==========================================
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

/* Global Font & Main Canvas Background */
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

.stApp {
    background-color: #F8FAFC !important;
}

/* Force dark, crisp text on all main container elements */
[data-testid="stMain"] h1, 
[data-testid="stMain"] h2, 
[data-testid="stMain"] h3, 
[data-testid="stMain"] h4, 
[data-testid="stMain"] p, 
[data-testid="stMain"] span, 
[data-testid="stMain"] label {
    color: #0F172A !important;
}

/* Hide Default Streamlit Menu Header */
#MainMenu, header, footer { visibility: hidden !important; }

/* ---------------- SIDEBAR STYLING ---------------- */
[data-testid="stSidebar"] {
    background-color: #0B1727 !important;
    border-right: 1px solid #1E293B !important;
}

[data-testid="stSidebar"] h1, 
[data-testid="stSidebar"] h2, 
[data-testid="stSidebar"] h3, 
[data-testid="stSidebar"] p, 
[data-testid="stSidebar"] span {
    color: #F8FAFC !important;
}

[data-testid="stSidebar"] label {
    color: #94A3B8 !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}

/* ---------------- RADIO NAVIGATION BUTTONS FIX ---------------- */
/* Fixes white-on-white unreadable text in main navigation options */
div[data-testid="stRadio"] > label {
    display: none !important;
}

div[data-testid="stRadio"] div[role="radiogroup"] {
    display: flex !important;
    flex-direction: row !important;
    gap: 12px !important;
    background: #FFFFFF !important;
    padding: 8px 12px !important;
    border-radius: 14px !important;
    border: 1px solid #E2E8F0 !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.02) !important;
    margin-bottom: 20px !important;
}

div[data-testid="stRadio"] div[role="radiogroup"] label {
    background: #F1F5F9 !important;
    border-radius: 10px !important;
    padding: 10px 18px !important;
    border: 1px solid #E2E8F0 !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
}

div[data-testid="stRadio"] div[role="radiogroup"] label p {
    color: #334155 !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
}

div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) {
    background: #0284C7 !important;
    border-color: #0284C7 !important;
}

div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) p {
    color: #FFFFFF !important;
}

/* ---------------- METRIC CARD OVERRIDES ---------------- */
.clinical-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 18px 20px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
    margin-bottom: 15px;
}

.card-label {
    font-size: 0.78rem;
    font-weight: 700;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 4px;
}

.card-value {
    font-size: 1.25rem;
    font-weight: 800;
    color: #0F172A;
}

.card-subtext {
    font-size: 0.8rem;
    color: #00BFA6;
    font-weight: 600;
    margin-top: 4px;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ==========================================
# 4. SIDEBAR CONTROLS
# ==========================================
with st.sidebar:
    st.markdown("""
    <div style="padding: 10px 0 20px 0;">
        <h2 style="color:#FFFFFF; font-size:1.4rem; font-weight:800; margin:0;">TeleRehabilitation</h2>
        <p style="color:#00BFA6; font-size:0.75rem; font-weight:700; margin:2px 0 0 0;">CLINICAL CARE PORTAL</p>
    </div>
    """, unsafe_allow_html=True)
    
    portal_role = st.selectbox("Portal Role", ["Patient", "Doctor", "Administrator"])
    patient_selection = st.selectbox("Patient Record", ["TRP-1001"])
    
    st.markdown("<hr style='border-color: #1E293B;'>", unsafe_allow_html=True)
    st.markdown(f"**Logged in as:** {portal_role}")

# ==========================================
# 5. MAIN CONTENT DISPLAY
# ==========================================
patient_data = get_patient(patient_selection)

if patient_data:
    # Header Title
    st.markdown("""
    <div style="margin-bottom: 10px;">
        <h1 style="font-size: 1.8rem; font-weight: 800; color: #0F172A; margin:0;">TeleRehabilitation Portal</h1>
        <p style="color: #64748B; font-size: 0.95rem; margin: 2px 0 0 0;">Clinical care coordination and secure tele-rehabilitation management</p>
    </div>
    """, unsafe_allow_html=True)

    # Navigation Tabs (Rendered with Fixed Visible Contrast CSS)
    active_tab = st.radio(
        "Navigation",
        ["Overview", "My Clinical Record", "Teleconsultation", "Care Plan"],
        horizontal=True
    )

    st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)

    if active_tab == "Overview":
        # Metric Cards Row
        c1, c2, c3, c4 = st.columns(4)
        
        with c1:
            st.markdown(f"""
            <div class="clinical-card">
                <div class="card-label">Patient Name</div>
                <div class="card-value">{patient_data['full_name'].split()[0]}</div>
                <div class="card-subtext">ID: {patient_data['patient_id']}</div>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown(f"""
            <div class="clinical-card">
                <div class="card-label">Diagnosis</div>
                <div class="card-value">{patient_data['diagnosis']}</div>
                <div class="card-subtext">Since {patient_data['diagnosis_date']}</div>
            </div>
            """, unsafe_allow_html=True)

        with c3:
            st.markdown(f"""
            <div class="clinical-card">
                <div class="card-label">Affected Region</div>
                <div class="card-value">{patient_data['affected_side']} {patient_data['affected_organ']}</div>
                <div class="card-subtext">Active Monitoring</div>
            </div>
            """, unsafe_allow_html=True)

        with c4:
            st.markdown(f"""
            <div class="clinical-card">
                <div class="card-label">Preferred Language</div>
                <div class="card-value">{patient_data['preferred_language']}</div>
                <div class="card-subtext">Status: {patient_data['status']}</div>
            </div>
            """, unsafe_allow_html=True)

        # Overview Detail Sections
        col_left, col_right = st.columns([2, 1])

        with col_left:
            st.markdown("### 📋 Primary Clinical Notes")
            st.info(patient_data["diagnosis_notes"])
            
            st.markdown("### 📈 Recent Recovery Goals")
            st.progress(0.75)
            st.caption("75% of scheduled motion rehab tasks completed this week.")

        with col_right:
            st.markdown("### 👤 Quick Contact")
            st.markdown(f"**Phone:** {patient_data['phone']}")
            st.markdown(f"**Email:** {patient_data['email']}")
            st.markdown(f"**Emergency Contact:** {patient_data['emergency_contact']} ({patient_data['emergency_phone']})")

    elif active_tab == "My Clinical Record":
        st.markdown("### 📂 Complete Patient Record")
        st.json(patient_data)

    elif active_tab == "Teleconsultation":
        st.markdown("### 📹 Video Tele-consultation Launcher")
        st.success("Doctor is available for live consultation.")
        if st.button("Start Encrypted Call", type="primary"):
            st.toast("Connecting to video server...")

    elif active_tab == "Care Plan":
        st.markdown("### 🏋️ Rehabilitation Task Checklist")
        st.checkbox("Morning Knee Extension Sets (15 reps)", value=True)
        st.checkbox("Afternoon Range of Motion Tracking", value=True)
        st.checkbox("Evening Ice Pack Compression (20 mins)", value=False)
