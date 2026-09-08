import streamlit as st
import sqlite3
import json
from datetime import datetime, date
import pandas as pd

# ==============================================================================
# 1. PAGE CONFIGURATION & TELESYNAPSE EXACT THEME
# ==============================================================================
st.set_page_config(
    page_title="TeleSynapse | Tele-Rehab Portal",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

DB_FILE = "telesynapse_rehab.db"

def inject_telesynapse_theme():
    st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

/* Hide Streamlit default chrome */
#MainMenu, header, footer, [data-testid="stHeader"] { 
    visibility: hidden !important; 
    height: 0px !important;
}

.stAppViewContainer {
    padding-top: 0px !important;
}

html, body, [class*="css"], .stMarkdown {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* Main Dashboard Background (Light Mint / Soft Gray-Teal) */
.stApp {
    background-color: #F2F8F6 !important;
}

/* Sidebar Custom Styling */
[data-testid="stSidebar"] {
    background-color: #07152B !important;
    border-right: 1px solid #0F2342 !important;
    padding-top: 10px;
}

[data-testid="stSidebar"] * {
    color: #94A3B8 !important;
}

/* Streamlit Radio Buttons disguised as Sidebar Nav */
[data-testid="stSidebar"] .stRadio > div {
    gap: 6px;
}

[data-testid="stSidebar"] .stRadio label {
    background-color: transparent !important;
    color: #94A3B8 !important;
    padding: 12px 16px !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    transition: all 0.2s ease-in-out !important;
    cursor: pointer !important;
    display: flex !important;
    align-items: center !important;
}

[data-testid="stSidebar"] .stRadio label:hover {
    background-color: #0E223D !important;
    color: #FFFFFF !important;
}

[data-testid="stSidebar"] .stRadio div[aria-checked="true"] label {
    background-color: #0C3646 !important;
    color: #00F2FE !important;
    font-weight: 700 !important;
    border-right: 3px solid #00F2FE !important;
}

/* Card Styling & Shadows */
.ts-card {
    background-color: #FFFFFF;
    border-radius: 16px;
    padding: 20px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.02);
}

.stButton > button {
    border-radius: 10px !important;
    font-weight: 700 !important;
    transition: all 0.2s ease !important;
}
</style>""", unsafe_allow_html=True)

inject_telesynapse_theme()

# ==============================================================================
# 2. DATABASE PERSISTENCE & INITIALIZATION
# ==============================================================================
@st.cache_resource
def get_db_connection():
    return sqlite3.connect(DB_FILE, check_same_thread=False)

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        patient_id TEXT PRIMARY KEY, full_name TEXT, date_of_birth TEXT, sex TEXT, country TEXT,
        phone TEXT, email TEXT, diagnosis TEXT, diagnosis_date TEXT, affected_organ TEXT,
        laterality TEXT, assigned_rehabilitator TEXT, clinical_notes TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS clinical_assessments (
        assessment_id INTEGER PRIMARY KEY AUTOINCREMENT, patient_id TEXT, knee_flexion TEXT,
        shoulder_abduction TEXT, gait_symmetry TEXT, sessions_count INT, assessment_date TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS teleconsultations (
        consultation_id INTEGER PRIMARY KEY AUTOINCREMENT, patient_id TEXT, provider TEXT,
        meeting_url TEXT, scheduled_date TEXT, scheduled_time TEXT, host_rehabilitator TEXT
    )
    """)

    cur.execute("SELECT COUNT(*) FROM patients")
    if cur.fetchone()[0] == 0:
        cur.execute("""
        INSERT INTO patients (
            patient_id, full_name, date_of_birth, sex, country, phone, email, diagnosis,
            diagnosis_date, affected_organ, laterality, assigned_rehabilitator, clinical_notes
        ) VALUES (
            'TS-P-811', 'Muhammad Hassan Raza Attari', '2005-10-14', 'Male', 'Pakistan',
            '+92 300 1234567', 'hassan@example.com', 'Post-Op ACL Reconstruction',
            '2026-08-10', 'Knee Joint', 'Left', 'Dr. Shahzaib Mughal',
            'Patient in Phase 2 recovery. Focus on ROM exercises and gait balance.'
        )
        """)

        cur.execute("""
        INSERT INTO clinical_assessments (patient_id, knee_flexion, shoulder_abduction, gait_symmetry, sessions_count, assessment_date)
        VALUES ('TS-P-811', '95° Flexion', '110° Abduction', '88% Symmetry', 0, '2026-09-08')
        """)

        cur.execute("""
        INSERT INTO teleconsultations (patient_id, provider, meeting_url, scheduled_date, scheduled_time, host_rehabilitator)
        VALUES ('TS-P-811', 'TeleSynapse HD Video', 'https://meet.jit.si/TeleSynapse-TS-P-811', '2026-09-12', '14:30', 'Dr. Shahzaib Mughal')
        """)
        conn.commit()

init_db()

def fetch_patient_data(patient_id="TS-P-811"):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM patients WHERE patient_id = ?", (patient_id,))
    row = cur.fetchone()
    p = dict(zip([col[0] for col in cur.description], row)) if row else {}
    
    cur.execute("SELECT * FROM clinical_assessments WHERE patient_id = ? ORDER BY assessment_id DESC LIMIT 1", (patient_id,))
    row_a = cur.fetchone()
    a = dict(zip([col[0] for col in cur.description], row_a)) if row_a else {}

    cur.execute("SELECT * FROM teleconsultations WHERE patient_id = ? ORDER BY consultation_id DESC LIMIT 1", (patient_id,))
    row_t = cur.fetchone()
    t = dict(zip([col[0] for col in cur.description], row_t)) if row_t else {}

    return p, a, t

patient, assessment, tele_session = fetch_patient_data()

# ==============================================================================
# 3. SIDEBAR NAVIGATION & USER PROFILE PILL
# ==============================================================================
with st.sidebar:
    # TeleSynapse Logo Header
    st.markdown("""<div style="display: flex; align-items: center; gap: 12px; padding: 10px 8px 20px 8px;">
<div style="background-color: #00CDBE; width: 38px; height: 38px; border-radius: 10px; display: flex; align-items: center; justify-content: center;">
<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#07152B" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
</div>
<div>
<h2 style="color: #FFFFFF !important; font-size: 1.15rem; font-weight: 800; margin: 0; letter-spacing: -0.3px;">TeleSynapse</h2>
<p style="color: #00CDBE !important; font-size: 0.68rem; font-weight: 800; margin: 0; letter-spacing: 1px; text-transform: uppercase;">TELE-REHAB</p>
</div>
</div>""", unsafe_allow_html=True)

    # User Profile Pill Card
    st.markdown(f"""<div style="background-color: #0C1E38; border: 1px solid #142C4F; border-radius: 12px; padding: 12px; margin-bottom: 24px; display: flex; align-items: center; gap: 12px;">
<div style="background-color: #0284C7; color: #FFFFFF; width: 36px; height: 36px; border-radius: 50%; font-weight: 800; font-size: 1rem; display: flex; align-items: center; justify-content: center;">
M
</div>
<div style="overflow: hidden;">
<h4 style="color: #FFFFFF !important; font-size: 0.85rem; font-weight: 700; margin: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{patient.get('full_name', 'Muhammad Hassan')}</h4>
<span style="color: #00CDBE !important; font-size: 0.68rem; font-weight: 800; letter-spacing: 0.5px; text-transform: uppercase;">PATIENT</span>
<p style="color: #64748B !important; font-size: 0.72rem; margin: 0;">{patient.get('patient_id', 'TS-P-811')}</p>
</div>
</div>""", unsafe_allow_html=True)

    # Sidebar Navigation Selection
    st.markdown("<p style='font-size: 0.7rem; font-weight: 800; color: #475569 !important; text-transform: uppercase; letter-spacing: 0.8px; margin-left: 8px;'>MAIN NAVIGATION</p>", unsafe_allow_html=True)
    
    nav_option = st.radio(
        label="Navigation",
        options=[" My Dashboard", " Video Call", " My Progress", " My Reports"],
        index=0,
        label_visibility="collapsed"
    )

    st.markdown("<div style='height: 120px;'></div>", unsafe_allow_html=True)
    
    st.markdown("""<div style="padding: 12px 16px; color: #EF4444 !important; font-weight: 700; font-size: 0.9rem; cursor: pointer; display: flex; align-items: center; gap: 10px;">
<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#EF4444" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
Sign Out
</div>""", unsafe_allow_html=True)

# ==============================================================================
# 4. TOP NAVBAR (Search, Notifications, Patient Avatar Header)
# ==============================================================================
st.markdown(f"""<div style="display: flex; justify-content: space-between; align-items: center; background-color: #FFFFFF; padding: 14px 28px; border-radius: 16px; border: 1px solid #E2E8F0; margin-bottom: 24px; box-shadow: 0 2px 10px rgba(0,0,0,0.01);">
<div style="display: flex; align-items: center; gap: 12px;">
<h2 style="font-size: 1.25rem; font-weight: 800; color: #0F172A !important; margin: 0;">Clinical Dashboard</h2>
<span style="display: inline-flex; align-items: center; gap: 6px; background-color: #ECFDF5; color: #059669 !important; font-size: 0.75rem; font-weight: 700; padding: 4px 10px; border-radius: 20px;">
<span style="width: 7px; height: 7px; background-color: #10B981; border-radius: 50%;"></span>
Secure session active 🛡️
</span>
</div>
<div style="display: flex; align-items: center; gap: 20px;">
<div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 8px 16px; border-radius: 10px; display: flex; align-items: center; gap: 10px; width: 260px;">
<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#94A3B8" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
<span style="color: #94A3B8; font-size: 0.85rem;">Search patients, session...</span>
</div>
<div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; width: 38px; height: 38px; border-radius: 10px; display: flex; align-items: center; justify-content: center; position: relative; cursor: pointer;">
<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#475569" stroke-width="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
<span style="position: absolute; top: 8px; right: 8px; width: 6px; height: 6px; background-color: #10B981; border-radius: 50%;"></span>
</div>
<div style="display: flex; align-items: center; gap: 10px; padding-left: 10px; border-left: 1px solid #E2E8F0;">
<div style="text-align: right;">
<div style="font-size: 0.85rem; font-weight: 800; color: #0F172A !important;">{patient.get('full_name', 'Muhammad Hassan Raza Attari')}</div>
<div style="font-size: 0.7rem; font-weight: 800; color: #00CDBE !important; text-transform: uppercase;">PATIENT</div>
</div>
<div style="background-color: #0284C7; color: #FFFFFF; width: 36px; height: 36px; border-radius: 10px; font-weight: 800; font-size: 0.95rem; display: flex; align-items: center; justify-content: center;">
M
</div>
</div>
</div>
</div>""", unsafe_allow_html=True)

# ==============================================================================
# 5. DASHBOARD MAIN VIEW
# ==============================================================================
if "My Dashboard" in nav_option:
    
    # HERO BANNER
    st.markdown(f"""<div style="background: linear-gradient(135deg, #1D68D8 0%, #1E40AF 100%); border-radius: 20px; padding: 28px 32px; color: #FFFFFF; margin-bottom: 24px; position: relative; box-shadow: 0 10px 25px rgba(29, 104, 216, 0.25);">
<div style="display: flex; justify-content: space-between; align-items: center;">
<div>
<div style="color: #93C5FD !important; font-size: 0.85rem; font-weight: 700; margin-bottom: 6px;">Tuesday, September 8, 2026</div>
<h1 style="color: #FFFFFF !important; font-size: 1.85rem; font-weight: 800; margin: 0 0 8px 0; letter-spacing: -0.5px;">Assalam O Alaikum, Muhammad</h1>
<p style="color: #DBEAFE !important; font-size: 0.95rem; margin: 0; font-weight: 500;">2 rehab tasks pending — keep up your recovery streak!</p>
</div>
<div>
<a href="{tele_session.get('meeting_url', '#')}" target="_blank" style="background-color: rgba(255, 255, 255, 0.15); backdrop-filter: blur(8px); border: 1px solid rgba(255, 255, 255, 0.3); color: #FFFFFF !important; padding: 12px 24px; border-radius: 12px; font-weight: 700; font-size: 0.95rem; text-decoration: none; display: inline-flex; align-items: center; gap: 8px;">
<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2"><path d="M23 7l-7 5 7 5V7z"/><rect x="1" y="5" width="15" height="14" rx="2" ry="2"/></svg>
Join Call
</a>
</div>
</div>
</div>""", unsafe_allow_html=True)

    # 4 KPI MEASUREMENT CARDS ROW
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    with kpi1:
        st.markdown(f"""<div class="ts-card" style="position: relative;">
<div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 14px;">
<div style="background-color: #E6F7F5; width: 42px; height: 42px; border-radius: 12px; display: flex; align-items: center; justify-content: center;">
<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#00CDBE" stroke-width="2.5"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
</div>
<span style="color: #CBD5E1; font-size: 1rem;">↗</span>
</div>
<div style="width: 24px; height: 3px; background-color: #0F172A; border-radius: 2px; margin-bottom: 12px;"></div>
<div style="font-size: 0.95rem; font-weight: 700; color: #334155 !important;">Knee Flexion</div>
<div style="font-size: 0.8rem; font-weight: 600; color: #00CDBE !important; margin-top: 2px;">{assessment.get('knee_flexion', 'No data yet')}</div>
</div>""", unsafe_allow_html=True)

    with kpi2:
        st.markdown(f"""<div class="ts-card" style="position: relative;">
<div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 14px;">
<div style="background-color: #E0F2FE; width: 42px; height: 42px; border-radius: 12px; display: flex; align-items: center; justify-content: center;">
<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#0284C7" stroke-width="2.5"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>
</div>
<span style="color: #CBD5E1; font-size: 1rem;">↗</span>
</div>
<div style="width: 24px; height: 3px; background-color: #0F172A; border-radius: 2px; margin-bottom: 12px;"></div>
<div style="font-size: 0.95rem; font-weight: 700; color: #334155 !important;">Shoulder Abduction</div>
<div style="font-size: 0.8rem; font-weight: 600; color: #0284C7 !important; margin-top: 2px;">{assessment.get('shoulder_abduction', 'No data yet')}</div>
</div>""", unsafe_allow_html=True)

    with kpi3:
        st.markdown(f"""<div class="ts-card" style="position: relative;">
<div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 14px;">
<div style="background-color: #E6F7F5; width: 42px; height: 42px; border-radius: 12px; display: flex; align-items: center; justify-content: center;">
<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#00CDBE" stroke-width="2.5"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
</div>
<span style="color: #CBD5E1; font-size: 1rem;">↗</span>
</div>
<div style="width: 24px; height: 3px; background-color: #0F172A; border-radius: 2px; margin-bottom: 12px;"></div>
<div style="font-size: 0.95rem; font-weight: 700; color: #334155 !important;">Gait Symmetry</div>
<div style="font-size: 0.8rem; font-weight: 600; color: #00CDBE !important; margin-top: 2px;">{assessment.get('gait_symmetry', 'No data yet')}</div>
</div>""", unsafe_allow_html=True)

    with kpi4:
        st.markdown(f"""<div class="ts-card" style="position: relative;">
<div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 14px;">
<div style="background-color: #FEF3C7; width: 42px; height: 42px; border-radius: 12px; display: flex; align-items: center; justify-content: center;">
<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#D97706" stroke-width="2.5"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
</div>
<span style="color: #CBD5E1; font-size: 1rem;">↗</span>
</div>
<div style="font-size: 1.6rem; font-weight: 800; color: #0F172A !important; line-height: 1;">{assessment.get('sessions_count', 0)}</div>
<div style="font-size: 0.95rem; font-weight: 700; color: #334155 !important; margin-top: 4px;">Sessions</div>
<div style="font-size: 0.78rem; font-weight: 600; color: #D97706 !important;">Total recorded</div>
</div>""", unsafe_allow_html=True)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # MAIN CONTENT GRID: RECENT SESSIONS + QUICK ACTIONS
    col_left, col_right = st.columns([2.2, 1])

    with col_left:
        st.markdown("""<div class="ts-card" style="height: 380px; display: flex; flex-direction: column; justify-content: space-between;">
<div style="display: flex; justify-content: space-between; align-items: center;">
<h3 style="font-size: 1.1rem; font-weight: 800; color: #0F172A !important; margin: 0;">Recent Sessions</h3>
<span style="font-size: 0.85rem; font-weight: 700; color: #00CDBE !important; cursor: pointer;">View all</span>
</div>
<div style="text-align: center; margin: auto;">
<div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; width: 64px; height: 64px; border-radius: 16px; display: flex; align-items: center; justify-content: center; margin: 0 auto 16px auto;">
<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#CBD5E1" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
</div>
<h4 style="font-size: 0.95rem; font-weight: 700; color: #94A3B8 !important; margin: 0 0 4px 0;">No sessions recorded yet.</h4>
<p style="font-size: 0.82rem; color: #CBD5E1 !important; margin: 0;">Your doctor will schedule your first session.</p>
</div>
<div></div>
</div>""", unsafe_allow_html=True)

    with col_right:
        # Action Card 1: Start Video Call (Teal Gradient)
        st.markdown(f"""<a href="{tele_session.get('meeting_url', '#')}" target="_blank" style="text-decoration: none;">
<div style="background: linear-gradient(135deg, #00CDBE 0%, #059669 100%); border-radius: 16px; padding: 18px 20px; color: #FFFFFF; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 15px rgba(0,205,190,0.25);">
<div style="display: flex; align-items: center; gap: 14px;">
<div style="background-color: rgba(255,255,255,0.2); width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center;">
<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5"><path d="M23 7l-7 5 7 5V7z"/><rect x="1" y="5" width="15" height="14" rx="2" ry="2"/></svg>
</div>
<span style="font-size: 1rem; font-weight: 800; color: #FFFFFF !important;">Start Video Call</span>
</div>
<span style="font-size: 1.1rem; color: #FFFFFF;">↗</span>
</div>
</a>""", unsafe_allow_html=True)

        # Action Card 2: View My Progress (Vivid Blue)
        st.markdown("""<div style="background: linear-gradient(135deg, #1D68D8 0%, #1E40AF 100%); border-radius: 16px; padding: 18px 20px; color: #FFFFFF; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 15px rgba(29,104,216,0.25); cursor: pointer;">
<div style="display: flex; align-items: center; gap: 14px;">
<div style="background-color: rgba(255,255,255,0.2); width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center;">
<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>
</div>
<span style="font-size: 1rem; font-weight: 800; color: #FFFFFF !important;">View My Progress</span>
</div>
<span style="font-size: 1.1rem; color: #FFFFFF;">↗</span>
</div>""", unsafe_allow_html=True)

        # Action Card 3: Secure Chat (Orange / Red Gradient)
        st.markdown("""<div style="background: linear-gradient(135deg, #F97316 0%, #EF4444 100%); border-radius: 16px; padding: 18px 20px; color: #FFFFFF; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 15px rgba(249,115,22,0.25); cursor: pointer;">
<div style="display: flex; align-items: center; gap: 14px;">
<div style="background-color: rgba(255,255,255,0.2); width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center;">
<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
</div>
<span style="font-size: 1rem; font-weight: 800; color: #FFFFFF !important;">Secure Chat</span>
</div>
<span style="font-size: 1.1rem; color: #FFFFFF;">↗</span>
</div>""", unsafe_allow_html=True)

        # Action Card 4: Generate Report (Purple Gradient)
        st.markdown("""<div style="background: linear-gradient(135deg, #8B5CF6 0%, #4F46E5 100%); border-radius: 16px; padding: 18px 20px; color: #FFFFFF; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 15px rgba(139,92,246,0.25); cursor: pointer;">
<div style="display: flex; align-items: center; gap: 14px;">
<div style="background-color: rgba(255,255,255,0.2); width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center;">
<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
</div>
<span style="font-size: 1rem; font-weight: 800; color: #FFFFFF !important;">Generate Report</span>
</div>
<span style="font-size: 1.1rem; color: #FFFFFF;">↗</span>
</div>""", unsafe_allow_html=True)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # BOTTOM RECOVERY TIP OF THE DAY BANNER
    st.markdown("""<div style="background-color: #E6F7F5; border: 1px solid #B2EBF2; border-radius: 16px; padding: 20px 24px; display: flex; align-items: center; gap: 16px;">
<div style="background-color: #00CDBE; width: 44px; height: 44px; border-radius: 12px; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
</div>
<div>
<h4 style="font-size: 0.95rem; font-weight: 800; color: #07152B !important; margin: 0 0 4px 0;">Recovery Tip of the Day</h4>
<p style="font-size: 0.88rem; color: #334155 !important; margin: 0; font-weight: 500;">
For ACL rehabilitation, consistent active range-of-motion exercises performed 3x daily significantly reduces joint stiffness and accelerates quadriceps activation.
</p>
</div>
</div>""", unsafe_allow_html=True)

# ==============================================================================
# 6. OTHER SUB-PAGES (VIDEO CALL, MY PROGRESS, MY REPORTS)
# ==============================================================================
elif "Video Call" in nav_option:
    st.markdown("### 📹 TeleSynapse HD Video Consultation")
    st.markdown(f"**Host Doctor:** {tele_session.get('host_rehabilitator', 'Dr. Shahzaib Mughal')}")
    st.components.v1.iframe(tele_session.get('meeting_url', 'https://meet.jit.si/'), height=600, scrolling=True)

elif "My Progress" in nav_option:
    st.markdown("### 📊 Recovery Progress & Range of Motion Tracking")
    df_chart = pd.DataFrame({
        "Week": ["Week 1", "Week 2", "Week 3", "Week 4"],
        "Flexion (Degrees)": [45, 65, 80, 95]
    })
    st.line_chart(df_chart.set_index("Week"))
    st.json(assessment)

elif "My Reports" in nav_option:
    st.markdown("### 📋 Downloadable Medical & Clinical Reports")
    st.markdown(f"""<div class="ts-card">
<h4>Patient Clinical File - {patient.get('patient_id')}</h4>
<p><strong>Diagnosis:</strong> {patient.get('diagnosis')}</p>
<p><strong>Attending Physician:</strong> {patient.get('assigned_rehabilitator')}</p>
<p><strong>Clinical Summary:</strong> {patient.get('clinical_notes')}</p>
</div>""", unsafe_allow_html=True)
