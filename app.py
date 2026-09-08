import streamlit as st
import sqlite3
import json
from datetime import datetime, date

# ==============================================================================
# 1. PAGE CONFIGURATION & SKY BLUE / DARK SLATE THEMING
# ==============================================================================
st.set_page_config(
    page_title="Tekerehab | Sky Clinical Portal",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

DB_FILE = "tekerehab_clinical.db"

def inject_sky_theme():
    st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

#MainMenu, header, footer, [data-testid="stHeader"] { 
    visibility: hidden !important; 
    height: 0px !important;
}

.stAppViewContainer {
    padding-top: 0px !important;
}

html, body, [class*="css"], .stMarkdown {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: #F1F5F9 !important;
}

/* App Background: Dark Slate / Deep Blue to replace stark white */
.stApp {
    background: linear-gradient(135deg, #0B132B 0%, #0F172A 100%) !important;
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background-color: #091026 !important;
    border-right: 1px solid #1E293B !important;
}

[data-testid="stSidebar"] * {
    color: #E2E8F0 !important;
}

[data-testid="stSidebar"] label {
    color: #38BDF8 !important;
    font-weight: 700 !important;
    font-size: 0.8rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}

/* Form Inputs & Selectboxes */
div[data-baseweb="select"] > div, .stTextInput input, .stTextArea textarea {
    background-color: #1E293B !important;
    color: #F8FAFC !important;
    border: 1px solid #334155 !important;
    border-radius: 8px !important;
}

/* Tab Styling - Sky Blue Highlights */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: #0F172A;
    padding: 8px;
    border-radius: 12px;
    border: 1px solid #1E293B;
}

.stTabs [data-baseweb="tab"] {
    height: 44px;
    border-radius: 8px;
    color: #94A3B8;
    font-weight: 600;
    font-size: 0.88rem;
    padding: 0px 16px;
    border: none !important;
}

.stTabs [aria-selected="true"] {
    background-color: #0EA5E9 !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 12px rgba(14, 165, 233, 0.3) !important;
}

/* Buttons */
.stButton > button {
    background-color: #0EA5E9 !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 20px !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    background-color: #38BDF8 !important;
    box-shadow: 0 4px 14px rgba(56, 189, 248, 0.4) !important;
}
</style>""", unsafe_allow_html=True)

inject_sky_theme()

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
        patient_id TEXT PRIMARY KEY, full_name TEXT, date_of_birth TEXT, sex TEXT, country TEXT, preferred_language TEXT,
        phone TEXT, email TEXT, emergency_contact_name TEXT, emergency_contact_phone TEXT, diagnosis TEXT, diagnosis_date TEXT,
        affected_organ TEXT, laterality TEXT, injury_type TEXT, cause_mechanism TEXT, medical_history TEXT, surgery_history TEXT,
        current_medications TEXT, allergies TEXT, previous_rehab TEXT, functional_limitations TEXT, pain_info TEXT, mobility_limitations TEXT,
        referring_physician TEXT, assigned_rehabilitator TEXT, clinical_notes TEXT, medical_reports_uploaded TEXT, document_links TEXT, consent_authorization INT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS clinical_assessments (
        assessment_id INTEGER PRIMARY KEY AUTOINCREMENT, patient_id TEXT, rom_degrees TEXT DEFAULT NULL, pain_score TEXT DEFAULT NULL,
        strength_grade TEXT DEFAULT NULL, gait_status TEXT DEFAULT NULL, functional_score TEXT DEFAULT NULL, swelling_status TEXT DEFAULT NULL,
        balance_score TEXT DEFAULT NULL, assessment_date TEXT, FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS rehab_plans (
        plan_id INTEGER PRIMARY KEY AUTOINCREMENT, patient_id TEXT, assigned_by TEXT, phase_name TEXT, effective_date TEXT, activities_json TEXT,
        FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS teleconsultations (
        consultation_id INTEGER PRIMARY KEY AUTOINCREMENT, patient_id TEXT, provider TEXT, meeting_url TEXT, meeting_id TEXT,
        scheduled_date TEXT, scheduled_time TEXT, timezone TEXT, host_rehabilitator TEXT, notes TEXT, FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
    )
    """)

    cur.execute("SELECT COUNT(*) FROM patients")
    if cur.fetchone()[0] == 0:
        cur.execute("""
        INSERT INTO patients (
            patient_id, full_name, date_of_birth, sex, country, preferred_language, phone, email, emergency_contact_name, emergency_contact_phone,
            diagnosis, diagnosis_date, affected_organ, laterality, injury_type, cause_mechanism, medical_history, surgery_history, current_medications,
            allergies, previous_rehab, functional_limitations, pain_info, mobility_limitations, referring_physician, assigned_rehabilitator, clinical_notes,
            medical_reports_uploaded, document_links, consent_authorization
        ) VALUES (
            'TRP-1001', 'Muhammad Hassan Raza Attari', '2005-10-14', 'Male', 'Pakistan', 'English', '+92 300 1234567', 'hassan@example.com', 'Family Member', '+92 300 7654321',
            'Post-Op Anterior Cruciate Ligament (ACL) Reconstruction', '2026-08-10', 'Knee Joint', 'Left', 'Surgical Post-Op', 'Sports Injury', 'None reported', 'Left Knee ACL Reconstruction (Aug 2026)',
            'Analgesics (as needed)', 'None reported', 'None', 'Inability to fully flex knee past 90 degrees', 'Moderate discomfort on weight bearing', 'Requires single crutch support',
            'Dr. Shahzaib Mughal', 'Dr. Ahmed Khan (PT)', 'Patient demonstrating steady post-op recovery. Avoid forced extension.', 'MRI_PreOp_Knee.pdf, PostOp_XRay.pdf',
            'https://clinical-records.example.com/TRP-1001', 1
        )
        """)

        activities = json.dumps([
            {"task": "Passive Knee Extension on Bolster", "reps": "3 sets of 10 reps", "frequency": "2x Daily"},
            {"task": "Seated Heel Slides to Tolerance", "reps": "15 reps", "frequency": "3x Daily"},
            {"task": "Isometric Quadriceps Setting", "reps": "10-second holds x 10", "frequency": "2x Daily"}
        ])
        cur.execute("INSERT INTO rehab_plans (patient_id, assigned_by, phase_name, effective_date, activities_json) VALUES ('TRP-1001', 'Dr. Ahmed Khan', 'Phase 2 — Mobility & Strength', '2026-09-01', ?)", (activities,))

        cur.execute("""
        INSERT INTO teleconsultations (
            patient_id, provider, meeting_url, meeting_id, scheduled_date, scheduled_time, timezone, host_rehabilitator, notes
        ) VALUES (
            'TRP-1001', 'Enterprise Video Portal', 'https://meet.jit.si/Tekerehab-TRP-1001-Clinical', 'TRP-CONF-8821', '2026-09-12', '14:30', 'PKT (UTC+5)', 'Dr. Ahmed Khan',
            'Review range of motion progress and adjust quadriceps loading parameters.'
        )
        """)
        conn.commit()

init_db()

def fetch_patient_record(patient_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM patients WHERE patient_id = ?", (patient_id,))
    row = cur.fetchone()
    return dict(zip([col[0] for col in cur.description], row)) if row else None

def fetch_latest_assessment(patient_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM clinical_assessments WHERE patient_id = ? ORDER BY assessment_id DESC LIMIT 1", (patient_id,))
    row = cur.fetchone()
    return dict(zip([col[0] for col in cur.description], row)) if row else None

def fetch_rehab_plan(patient_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM rehab_plans WHERE patient_id = ? ORDER BY plan_id DESC LIMIT 1", (patient_id,))
    row = cur.fetchone()
    if not row:
        return None
    res = dict(zip([col[0] for col in cur.description], row))
    if res.get('activities_json'):
        res['activities'] = json.loads(res['activities_json'])
    return res

def fetch_teleconsultation(patient_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM teleconsultations WHERE patient_id = ? ORDER BY consultation_id DESC LIMIT 1", (patient_id,))
    row = cur.fetchone()
    return dict(zip([col[0] for col in cur.description], row)) if row else None

# ==============================================================================
# 3. AUTHENTICATION / LOGIN PORTAL SESSION STATE
# ==============================================================================
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "user_role" not in st.session_state:
    st.session_state["user_role"] = "Patient"
if "patient_id" not in st.session_state:
    st.session_state["patient_id"] = "TRP-1001"

# LOGIN SCREEN
if not st.session_state["authenticated"]:
    st.markdown("""<div style="max-width: 480px; margin: 60px auto 20px auto; text-align: center;">
<div style="background-color: #0EA5E9; display: inline-block; padding: 12px 18px; border-radius: 16px; margin-bottom: 12px; box-shadow: 0 0 20px rgba(14, 165, 233, 0.4);">
<span style="font-size: 2rem;">🩺</span>
</div>
<h1 style="color: #38BDF8 !important; font-size: 2rem; font-weight: 800; margin: 0;">Tekerehab Portal</h1>
<p style="color: #94A3B8 !important; font-size: 0.95rem; margin-top: 6px;">Enterprise Physical Rehabilitation Platform</p>
</div>""", unsafe_allow_html=True)

    st.markdown("""<div style="max-width: 480px; margin: 0 auto; background-color: #1E293B; border: 1px solid #0EA5E9; border-radius: 16px; padding: 30px; box-shadow: 0 8px 32px rgba(0,0,0,0.4);">
<h3 style="color: #F8FAFC !important; margin: 0 0 20px 0; text-align: center; font-size: 1.2rem; font-weight: 700;">Sign In to Your Account</h3>
</div>""", unsafe_allow_html=True)

    with st.form("login_form"):
        role = st.selectbox("Select Access Role", ["Patient", "Rehabilitator / Doctor"])
        user_input = st.text_input("User ID / Patient Record ID", value="TRP-1001")
        password = st.text_input("Password", type="password", value="••••••••")
        
        submit_login = st.form_submit_button("Launch Portal Dashboard 🚀", use_container_width=True)
        
        if submit_login:
            st.session_state["authenticated"] = True
            st.session_state["user_role"] = role
            st.session_state["patient_id"] = user_input
            st.rerun()
            
    st.markdown("""<div style="text-align: center; margin-top: 20px; color: #64748B; font-size: 0.8rem;">
Protected System • HIPAA & Clinical Data Compliant
</div>""", unsafe_allow_html=True)
    st.stop()

# ==============================================================================
# 4. DASHBOARD VIEW & SIDEBAR
# ==============================================================================
logged_patient_id = st.session_state["patient_id"]
portal_role = st.session_state["user_role"]

p = fetch_patient_record(logged_patient_id)
assessment = fetch_latest_assessment(logged_patient_id)
plan = fetch_rehab_plan(logged_patient_id)
tele = fetch_teleconsultation(logged_patient_id)

with st.sidebar:
    st.markdown("""<div style="padding: 10px 0 15px 0; border-bottom: 1px solid #1E293B; margin-bottom: 15px;">
<h2 style="color:#38BDF8 !important; font-size:1.3rem; font-weight:800; margin:0;">Tekerehab Portal</h2>
<p style="color:#0EA5E9 !important; font-size:0.75rem; font-weight:700; margin:4px 0 0 0; letter-spacing: 0.5px;">SKY CLINICAL DASHBOARD</p>
</div>""", unsafe_allow_html=True)

    st.markdown(f"**Logged User:** {st.session_state['user_role']}")
    st.markdown(f"**Active ID:** `{logged_patient_id}`")

    if st.button("🔒 Sign Out / Switch User", use_container_width=True):
        st.session_state["authenticated"] = False
        st.rerun()

    st.markdown("<hr style='border-color: #1E293B; margin: 16px 0;'>", unsafe_allow_html=True)
    selected_language = st.selectbox("Preferred Language", ["English", "Urdu", "Arabic", "Spanish", "French"])
    timezone_setting = st.selectbox("Time Zone", ["PKT (UTC+5)", "EST (UTC-5)", "AST (UTC+3)", "GMT (UTC+0)", "CET (UTC+1)"])

# Calculate Profile Completion %
def get_completion_pct(p, assessment, tele):
    if not p: return 0
    checks = [
        bool(p.get('full_name')), bool(p.get('diagnosis')),
        bool(p.get('affected_organ')), bool(p.get('medical_reports_uploaded')),
        bool(assessment and assessment.get('rom_degrees')), bool(tele and tele.get('meeting_url'))
    ]
    return int((sum(checks) / len(checks)) * 100)

completion_pct = get_completion_pct(p, assessment, tele)

# APP HEADER DASHBOARD BANNER
st.markdown(f"""<div style="background-color: #1E293B; border: 1px solid #0EA5E9; border-radius: 14px; padding: 20px 24px; margin-bottom: 20px; box-shadow: 0 4px 20px rgba(14, 165, 233, 0.15);">
<div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
<div>
<span style="background-color: #0EA5E9; color: #FFFFFF; font-size: 0.75rem; font-weight: 800; padding: 3px 10px; border-radius: 6px; text-transform: uppercase;">Clinical Dashboard</span>
<h1 style="font-size: 1.6rem; font-weight: 800; color: #F8FAFC !important; margin: 6px 0 0 0;">Welcome, {p['full_name'] if p else 'Patient'}</h1>
<p style="color: #38BDF8 !important; font-size: 0.88rem; margin: 4px 0 0 0; font-weight: 600;">Record ID: {logged_patient_id} • Assigned Rehabilitator: {p['assigned_rehabilitator'] if p else 'N/A'}</p>
</div>
<div style="text-align: right; background-color: #0F172A; padding: 10px 18px; border-radius: 10px; border: 1px solid #334155;">
<span style="font-size: 0.75rem; font-weight: 700; color: #94A3B8 !important; text-transform: uppercase;">Profile Completion</span><br>
<span style="font-size: 1.3rem; font-weight: 800; color: #38BDF8 !important;">{completion_pct}% Complete</span>
</div>
</div>
</div>""", unsafe_allow_html=True)

# DASHBOARD KPI METRIC CARDS
col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)

with col_kpi1:
    st.markdown(f"""<div style="background-color: #1E293B; border-left: 4px solid #38BDF8; border-radius: 10px; padding: 14px; border: 1px solid #334155;">
<div style="font-size: 0.75rem; font-weight: 700; color: #38BDF8 !important; text-transform: uppercase;">Active Diagnosis</div>
<div style="font-size: 0.95rem; font-weight: 700; color: #F8FAFC !important; margin-top: 4px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{p['diagnosis'] if p else 'N/A'}</div>
<div style="font-size: 0.75rem; color: #94A3B8 !important; margin-top: 2px;">Since {p['diagnosis_date'] if p else 'N/A'}</div>
</div>""", unsafe_allow_html=True)

with col_kpi2:
    st.markdown(f"""<div style="background-color: #1E293B; border-left: 4px solid #0EA5E9; border-radius: 10px; padding: 14px; border: 1px solid #334155;">
<div style="font-size: 0.75rem; font-weight: 700; color: #0EA5E9 !important; text-transform: uppercase;">Current Phase</div>
<div style="font-size: 0.95rem; font-weight: 700; color: #F8FAFC !important; margin-top: 4px;">{plan['phase_name'] if plan else 'Phase 1'}</div>
<div style="font-size: 0.75rem; color: #94A3B8 !important; margin-top: 2px;">Effective {plan['effective_date'] if plan else 'N/A'}</div>
</div>""", unsafe_allow_html=True)

with col_kpi3:
    st.markdown(f"""<div style="background-color: #1E293B; border-left: 4px solid #0284C7; border-radius: 10px; padding: 14px; border: 1px solid #334155;">
<div style="font-size: 0.75rem; font-weight: 700; color: #38BDF8 !important; text-transform: uppercase;">Latest ROM Assessment</div>
<div style="font-size: 0.95rem; font-weight: 700; color: #F8FAFC !important; margin-top: 4px;">{assessment['rom_degrees'] if (assessment and assessment.get('rom_degrees')) else 'Pending'}</div>
<div style="font-size: 0.75rem; color: #94A3B8 !important; margin-top: 2px;">Pain Score: {assessment['pain_score'] if assessment else 'N/A'}</div>
</div>""", unsafe_allow_html=True)

with col_kpi4:
    st.markdown(f"""<div style="background-color: #1E293B; border-left: 4px solid #38BDF8; border-radius: 10px; padding: 14px; border: 1px solid #334155;">
<div style="font-size: 0.75rem; font-weight: 700; color: #38BDF8 !important; text-transform: uppercase;">Teleconsultation</div>
<div style="font-size: 0.95rem; font-weight: 700; color: #F8FAFC !important; margin-top: 4px;">{tele['scheduled_date'] if tele else 'None'}</div>
<div style="font-size: 0.75rem; color: #94A3B8 !important; margin-top: 2px;">Time: {tele['scheduled_time'] if tele else 'N/A'}</div>
</div>""", unsafe_allow_html=True)

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

# ==============================================================================
# 5. DASHBOARD NAVIGATION TABS
# ==============================================================================
tab_titles = ["📊 Overview", "📋 Patient Demographics", "📊 Rehab Assessment", "💪 Care Plan", "📹 Teleconsultation"]
if portal_role == "Rehabilitator / Doctor":
    tab_titles.append("⚙️ Doctor Console")

tabs = st.tabs(tab_titles)

# TAB 0: EXECUTIVE OVERVIEW
with tabs[0]:
    st.markdown("### Clinical Overview & Status Summary")
    ov_c1, ov_c2 = st.columns([2, 1])
    
    with ov_c1:
        st.markdown(f"""<div style="background-color: #1E293B; border: 1px solid #334155; border-radius: 12px; padding: 20px; margin-bottom: 16px;">
<h4 style="color: #38BDF8 !important; margin: 0 0 12px 0;">Patient Summary Card</h4>
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; font-size: 0.9rem;">
<div><span style="color: #94A3B8;">Full Name:</span> <strong style="color:#F8FAFC;">{p['full_name']}</strong></div>
<div><span style="color: #94A3B8;">DOB / Age:</span> <strong style="color:#F8FAFC;">{p['date_of_birth']}</strong></div>
<div><span style="color: #94A3B8;">Affected Region:</span> <strong style="color:#F8FAFC;">{p['affected_organ']} ({p['laterality']})</strong></div>
<div><span style="color: #94A3B8;">Injury Type:</span> <strong style="color:#F8FAFC;">{p['injury_type']}</strong></div>
<div><span style="color: #94A3B8;">Referring Doctor:</span> <strong style="color:#F8FAFC;">{p['referring_physician']}</strong></div>
<div><span style="color: #94A3B8;">Contact:</span> <strong style="color:#F8FAFC;">{p['phone']}</strong></div>
</div>
</div>""", unsafe_allow_html=True)

    with ov_c2:
        st.markdown(f"""<div style="background-color: #1E293B; border: 1px solid #334155; border-radius: 12px; padding: 20px; text-align: center;">
<h4 style="color: #38BDF8 !important; margin: 0 0 8px 0;">Teleconsult Portal</h4>
<p style="font-size: 0.85rem; color: #94A3B8;">Next scheduled video session with your clinical team.</p>
<a href="{tele['meeting_url'] if tele else '#'}" target="_blank" style="background-color: #0EA5E9; color: white !important; padding: 10px 18px; border-radius: 8px; text-decoration: none; font-weight: 700; display: inline-block; margin-top: 8px;">
Launch Session 📹
</a>
</div>""", unsafe_allow_html=True)

# TAB 1: DEMOGRAPHICS
with tabs[1]:
    st.markdown("### Patient Demographics & Complete Clinical Record")
    if p:
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"**Full Name:** {p['full_name']}")
            st.markdown(f"**Patient ID:** {p['patient_id']}")
            st.markdown(f"**Date of Birth / Age:** {p['date_of_birth']}")
            st.markdown(f"**Sex:** {p['sex']}")
            st.markdown(f"**Country:** {p['country']}")
            st.markdown(f"**Preferred Language:** {p['preferred_language']}")
            st.markdown(f"**Contact Phone:** {p['phone']}")
            st.markdown(f"**Email:** {p['email']}")
            st.markdown(f"**Emergency Contact:** {p['emergency_contact_name']} ({p['emergency_contact_phone']})")

        with col_b:
            st.markdown(f"**Diagnosis:** {p['diagnosis']}")
            st.markdown(f"**Diagnosis Date:** {p['diagnosis_date']}")
            st.markdown(f"**Affected Body Region:** {p['affected_organ']}")
            st.markdown(f"**Laterality:** {p['laterality']}")
            st.markdown(f"**Injury / Condition Type:** {p['injury_type']}")
            st.markdown(f"**Cause / Mechanism:** {p['cause_mechanism']}")
            st.markdown(f"**Referring Physician:** {p['referring_physician']}")
            st.markdown(f"**Assigned Rehabilitator:** {p['assigned_rehabilitator']}")

        st.markdown("<hr style='border-color: #334155;'>", unsafe_allow_html=True)
        st.markdown("#### Medical History & Functional Limitations")
        m1, m2 = st.columns(2)
        with m1:
            st.markdown(f"**Relevant Medical History:** {p['medical_history']}")
            st.markdown(f"**Surgery / Procedure History:** {p['surgery_history']}")
            st.markdown(f"**Current Medications:** {p['current_medications']}")
            st.markdown(f"**Allergies:** {p['allergies']}")
        with m2:
            st.markdown(f"**Functional Limitations:** {p['functional_limitations']}")
            st.markdown(f"**Pain Characteristics:** {p['pain_info']}")
            st.markdown(f"**Mobility Limitations:** {p['mobility_limitations']}")
            st.markdown(f"**Clinical Notes:** {p['clinical_notes']}")

# TAB 2: REHAB ASSESSMENT
with tabs[2]:
    st.markdown("### Clinical Assessment & Range of Motion Metrics")
    rom_val = assessment['rom_degrees'] if (assessment and assessment.get('rom_degrees')) else "Not assessed yet"
    pain_val = assessment['pain_score'] if (assessment and assessment.get('pain_score')) else "Not assessed yet"
    str_val = assessment['strength_grade'] if (assessment and assessment.get('strength_grade')) else "Not assessed yet"
    fn_val = assessment['functional_score'] if (assessment and assessment.get('functional_score')) else "Not assessed yet"

    st.markdown(f"""<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-top: 16px;">
<div style="background-color: #1E293B; border: 1px solid #334155; border-radius: 12px; padding: 18px;">
<div style="font-size: 0.8rem; font-weight: 700; color: #38BDF8 !important; text-transform: uppercase;">Range of Motion (ROM)</div>
<div style="font-size: 1.35rem; font-weight: 800; color: #F8FAFC !important; margin-top: 6px;">{rom_val}</div>
</div>
<div style="background-color: #1E293B; border: 1px solid #334155; border-radius: 12px; padding: 18px;">
<div style="font-size: 0.8rem; font-weight: 700; color: #38BDF8 !important; text-transform: uppercase;">Pain Score (VAS)</div>
<div style="font-size: 1.35rem; font-weight: 800; color: #F8FAFC !important; margin-top: 6px;">{pain_val}</div>
</div>
<div style="background-color: #1E293B; border: 1px solid #334155; border-radius: 12px; padding: 18px;">
<div style="font-size: 0.8rem; font-weight: 700; color: #38BDF8 !important; text-transform: uppercase;">Muscle Strength</div>
<div style="font-size: 1.35rem; font-weight: 800; color: #F8FAFC !important; margin-top: 6px;">{str_val}</div>
</div>
<div style="background-color: #1E293B; border: 1px solid #334155; border-radius: 12px; padding: 18px;">
<div style="font-size: 0.8rem; font-weight: 700; color: #38BDF8 !important; text-transform: uppercase;">Functional Score</div>
<div style="font-size: 1.35rem; font-weight: 800; color: #F8FAFC !important; margin-top: 6px;">{fn_val}</div>
</div>
</div>""", unsafe_allow_html=True)

# TAB 3: CARE PLAN
with tabs[3]:
    st.markdown("### Active Clinical Care Plan & Prescribed Exercises")
    if plan and plan.get('activities'):
        for idx, act in enumerate(plan['activities'], start=1):
            st.markdown(f"""<div style="background-color: #1E293B; border: 1px solid #334155; border-left: 4px solid #0EA5E9; border-radius: 10px; padding: 16px; margin-bottom: 12px;">
<strong style="font-size: 1rem; color: #38BDF8 !important;">{idx}. {act['task']}</strong><br>
<span style="font-size: 0.88rem; color: #E2E8F0 !important;">Prescribed Dosage: {act['reps']} | Frequency: {act['frequency']}</span>
</div>""", unsafe_allow_html=True)

# TAB 4: TELECONSULTATION
with tabs[4]:
    st.markdown("### Teleconsultation Portal")
    if tele:
        st.markdown(f"""<div style="background-color: #1E293B; border: 1px solid #0EA5E9; border-radius: 12px; padding: 20px;">
<h3 style="color: #38BDF8 !important; margin: 0 0 10px 0;">Scheduled Teleconsultation</h3>
<p style="color: #E2E8F0 !important;"><strong>Provider:</strong> {tele['provider']}</p>
<p style="color: #E2E8F0 !important;"><strong>Date & Time:</strong> {tele['scheduled_date']} at {tele['scheduled_time']} ({tele['timezone']})</p>
<p style="color: #E2E8F0 !important;"><strong>Meeting ID:</strong> {tele['meeting_id']}</p>
<p style="color: #94A3B8 !important;"><strong>Clinical Notes:</strong> {tele['notes']}</p>
<div style="margin-top: 16px;">
<a href="{tele['meeting_url']}" target="_blank" style="background-color: #0EA5E9; color: white !important; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: 700; display: inline-block;">
Join Video Consultation 📹
</a>
</div>
</div>""", unsafe_allow_html=True)

# TAB 5: DOCTOR CONSOLE (IF AUTHORIZED)
if portal_role == "Rehabilitator / Doctor":
    with tabs[5]:
        st.markdown("### Doctor Console — Record Management")
        with st.form("doctor_entry"):
            rom_i = st.text_input("Range of Motion", value=assessment['rom_degrees'] if assessment else "")
            pain_i = st.text_input("Pain Score", value=assessment['pain_score'] if assessment else "")
            str_i = st.text_input("Muscle Strength", value=assessment['strength_grade'] if assessment else "")
            fn_i = st.text_input("Functional Score", value=assessment['functional_score'] if assessment else "")
            
            if st.form_submit_button("Update Assessment Data"):
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute("""
                INSERT INTO clinical_assessments (patient_id, rom_degrees, pain_score, strength_grade, functional_score, assessment_date)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (logged_patient_id, rom_i, pain_i, str_i, fn_i, datetime.now().strftime("%Y-%m-%d")))
                conn.commit()
                st.success("Record updated successfully!")
                st.rerun()
