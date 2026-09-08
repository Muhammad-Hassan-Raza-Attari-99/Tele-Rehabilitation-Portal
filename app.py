import streamlit as st
import sqlite3
import json
from datetime import datetime, date

# ==========================================
# 1. PAGE CONFIGURATION & ENTERPRISE CSS
# ==========================================
st.set_page_config(
    page_title="TeleRehabilitation Portal",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

DB_FILE = "tele_rehabilitation_clinical.db"

# CSS for Enterprise Medical Branding & High Contrast (Req 1)
def inject_enterprise_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* Hide Streamlit Default Headers & Footers */
    #MainMenu, header, footer, [data-testid="stHeader"] { 
        visibility: hidden !important; 
        height: 0px !important;
    }
    
    .stAppViewContainer {
        padding-top: 0px !important;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: #0F172A !important;
    }

    .stApp {
        background-color: #F8FAFC !important;
    }

    /* Sidebar Customization */
    [data-testid="stSidebar"] {
        background-color: #0F172A !important;
        border-right: 1px solid #1E293B !important;
    }

    [data-testid="stSidebar"] * {
        color: #F8FAFC !important;
    }

    [data-testid="stSidebar"] label {
        color: #94A3B8 !important;
        font-weight: 600 !important;
        font-size: 0.8rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }

    /* Clinical Cards */
    .clinical-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        margin-bottom: 16px;
    }

    .clinical-card-header {
        font-size: 0.85rem;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        margin-bottom: 8px;
    }

    .clinical-card-value {
        font-size: 1.4rem;
        font-weight: 800;
        color: #0F172A;
    }

    /* Clinical Status Badges (Req 9) */
    .status-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .status-completed { background-color: #DEF7EC; color: #03543F; }
    .status-pending { background-color: #FEF08A; color: #713F12; }
    .status-scheduled { background-color: #E0F2FE; color: #0369A1; }
    .status-not-assessed { background-color: #F1F5F9; color: #475569; }

    /* Pathway Display (Req 8) */
    .pathway-container {
        display: flex;
        justify-content: space-between;
        background: #FFFFFF;
        padding: 18px 24px;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        margin-bottom: 24px;
    }
    .pathway-step {
        flex: 1;
        text-align: center;
        padding: 8px;
        font-weight: 600;
        font-size: 0.88rem;
        color: #64748B;
        border-bottom: 3px solid #CBD5E1;
    }
    .pathway-step.active {
        color: #0284C7;
        border-bottom: 3px solid #0284C7;
        font-weight: 700;
    }
    .pathway-step.completed {
        color: #059669;
        border-bottom: 3px solid #059669;
    }

    /* Custom Radio Navigation */
    div[data-testid="stRadio"] > label { display: none !important; }
    div[data-testid="stRadio"] div[role="radiogroup"] {
        display: flex !important;
        gap: 10px !important;
        background: #FFFFFF !important;
        padding: 6px !important;
        border-radius: 10px !important;
        border: 1px solid #E2E8F0 !important;
        margin-bottom: 20px !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] label {
        background: transparent !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        border: none !important;
        cursor: pointer !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) {
        background: #0284C7 !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] label p {
        color: #334155 !important;
        font-weight: 600 !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) p {
        color: #FFFFFF !important;
    }
    </style>
    """, unsafe_allow_html=True)

inject_enterprise_styles()

# ==========================================
# 2. INTERNATIONALIZATION (i18n) DICTIONARY (Req 6)
# ==========================================
TRANSLATIONS = {
    "English": {
        "portal_title": "TeleRehabilitation Portal",
        "subtitle": "Enterprise Clinical Rehabilitation Management",
        "profile_completion": "Profile Completion",
        "patient_info": "Patient Information",
        "clinical_diagnosis": "Clinical Diagnosis",
        "affected_region": "Affected Body Region",
        "medical_records": "Medical Records",
        "rehab_assessment": "Rehabilitation Assessment",
        "teleconsultation": "Teleconsultation",
        "complete": "Complete",
        "incomplete": "Incomplete",
        "scheduled": "Scheduled",
        "not_scheduled": "Not Scheduled",
        "not_assessed": "Not assessed yet",
        "join_meeting": "Join Teleconsultation",
        "assigned_by": "Assigned by",
        "effective_from": "Effective from",
        "phase": "Current Phase",
        "rehab_pathway": "Rehabilitation Pathway",
        "nav_profile": "Clinical Profile",
        "nav_assessment": "Rehabilitation Assessment",
        "nav_plan": "Clinical Care Plan",
        "nav_teleconsult": "Teleconsultation Portal",
        "nav_editor": "Rehabilitator Console"
    },
    "Urdu": {
        "portal_title": "ٹیلی ری ہیبیلیٹیشن پورٹل",
        "subtitle": "پیشہ ورانہ کلینکل بحالی کا نظام",
        "profile_completion": "پروفائل کی تکمیل",
        "patient_info": "مریض کی معلومات",
        "clinical_diagnosis": "کلینکل تشخیص",
        "affected_region": "متاثرہ جسمانی حصہ",
        "medical_records": "طبی ریکارڈ",
        "rehab_assessment": "بحالی کا جائزہ",
        "teleconsultation": "ٹیلی مشاورت",
        "complete": "مکمل",
        "incomplete": "غیر مکمل",
        "scheduled": "شیڈول شدہ",
        "not_scheduled": "شیڈول نہیں ہے",
        "not_assessed": "ابھی تک جائزہ نہیں لیا گیا",
        "join_meeting": "ٹیلی مشاورت میں شامل ہوں",
        "assigned_by": "تعینات کردہ",
        "effective_from": "سے نافذ العمل",
        "phase": "موجودہ مرحلہ",
        "rehab_pathway": "بحالی کا راستہ",
        "nav_profile": "کلینکل پروفائل",
        "nav_assessment": "بحالی کی تشخیص",
        "nav_plan": "کلینکل کیئر پلان",
        "nav_teleconsult": "ٹیلی پورٹل",
        "nav_editor": "معالج کا کنسول"
    },
    "Arabic": {
        "portal_title": "بوابة إعادة التأهيل عن بُعد",
        "subtitle": "نظام إدارة إعادة التأهيل الطبي السريري",
        "profile_completion": "إکمال الملف الشخصي",
        "patient_info": "معلومات المريض",
        "clinical_diagnosis": "التشخيص السريري",
        "affected_region": "المنطقة المصابة",
        "medical_records": "السجلات الطبية",
        "rehab_assessment": "تقييم إعادة التأهيل",
        "teleconsultation": "الاستشارة عن بُعد",
        "complete": "مكتمل",
        "incomplete": "غير مكتمل",
        "scheduled": "مجدول",
        "not_scheduled": "غير مجدول",
        "not_assessed": "لم يتم التقييم بعد",
        "join_meeting": "الانضمام إلى الاستشارة",
        "assigned_by": "المعالج المسؤول",
        "effective_from": "ساري من",
        "phase": "المرحلة الحالية",
        "rehab_pathway": "مسار إعادة التأهيل",
        "nav_profile": "الملف السريري",
        "nav_assessment": "تقييم التأهيل",
        "nav_plan": "خطة الرعاية",
        "nav_teleconsult": "بوابة الاستشارة",
        "nav_editor": "لوحة المعالج"
    },
    "Spanish": {
        "portal_title": "Portal de TeleRehabilitación",
        "subtitle": "Gestión Clínica de Tele-Rehabilitación Empresarial",
        "profile_completion": "Completitud del Perfil",
        "patient_info": "Información del Paciente",
        "clinical_diagnosis": "Diagnóstico Clínico",
        "affected_region": "Región Corporal Afectada",
        "medical_records": "Registros Médicos",
        "rehab_assessment": "Evaluación de Rehabilitación",
        "teleconsultation": "Teleconsulta",
        "complete": "Completo",
        "incomplete": "Incompleto",
        "scheduled": "Programado",
        "not_scheduled": "No Programado",
        "not_assessed": "Aún no evaluado",
        "join_meeting": "Unirse a la Teleconsulta",
        "assigned_by": "Asignado por",
        "effective_from": "Efectivo desde",
        "phase": "Fase Actual",
        "rehab_pathway": "Vía de Rehabilitación",
        "nav_profile": "Perfil Clínico",
        "nav_assessment": "Evaluación de Rehabilitación",
        "nav_plan": "Plan de Cuidado Clínico",
        "nav_teleconsult": "Portal de Teleconsulta",
        "nav_editor": "Consola del Rehabilitador"
    },
    "French": {
        "portal_title": "Portail de TéléRéadaptation",
        "subtitle": "Gestion Clinique de Télé-Réadaptation",
        "profile_completion": "Complétion du Profil",
        "patient_info": "Informations du Patient",
        "clinical_diagnosis": "Diagnostic Clinique",
        "affected_region": "Région Corporelle Touchée",
        "medical_records": "Dossiers Médicaux",
        "rehab_assessment": "Évaluation de Réadaptation",
        "teleconsultation": "Téléconsultation",
        "complete": "Complet",
        "incomplete": "Incomplet",
        "scheduled": "Programmé",
        "not_scheduled": "Non Programmé",
        "not_assessed": "Pas encore évalué",
        "join_meeting": "Rejoindre la Téléconsultation",
        "assigned_by": "Assigné par",
        "effective_from": "Effectif depuis",
        "phase": "Phase Actuelle",
        "rehab_pathway": "Parcours de Réadaptation",
        "nav_profile": "Profil Clinique",
        "nav_assessment": "Évaluation de Réadaptation",
        "nav_plan": "Plan de Soins Cliniques",
        "nav_teleconsult": "Portail de Téléconsultation",
        "nav_editor": "Console du Réadaptateur"
    }
}

# ==========================================
# 3. DATABASE SCHEMA & PERSISTENCE (Req 2)
# ==========================================
@st.cache_resource
def get_db_connection():
    return sqlite3.connect(DB_FILE, check_same_thread=False)

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Complete Patient Clinical Record Table (30+ fields)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        patient_id TEXT PRIMARY KEY,
        full_name TEXT,
        date_of_birth TEXT,
        sex TEXT,
        country TEXT,
        preferred_language TEXT,
        phone TEXT,
        email TEXT,
        emergency_contact_name TEXT,
        emergency_contact_phone TEXT,
        diagnosis TEXT,
        diagnosis_date TEXT,
        affected_organ TEXT,
        laterality TEXT,
        injury_type TEXT,
        cause_mechanism TEXT,
        medical_history TEXT,
        surgery_history TEXT,
        current_medications TEXT,
        allergies TEXT,
        previous_rehab TEXT,
        functional_limitations TEXT,
        pain_info TEXT,
        mobility_limitations TEXT,
        referring_physician TEXT,
        assigned_rehabilitator TEXT,
        clinical_notes TEXT,
        medical_reports_uploaded TEXT,
        document_links TEXT,
        consent_authorization INT
    )
    """)

    # Clinical Measurements Table (No defaults!) (Req 3)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS clinical_assessments (
        assessment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id TEXT,
        rom_degrees TEXT DEFAULT NULL,
        pain_score TEXT DEFAULT NULL,
        strength_grade TEXT DEFAULT NULL,
        gait_status TEXT DEFAULT NULL,
        functional_score TEXT DEFAULT NULL,
        swelling_status TEXT DEFAULT NULL,
        balance_score TEXT DEFAULT NULL,
        assessment_date TEXT,
        FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
    )
    """)

    # Rehabilitation Plan Table (Req 4)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS rehab_plans (
        plan_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id TEXT,
        assigned_by TEXT,
        phase_name TEXT,
        effective_date TEXT,
        activities_json TEXT,
        FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
    )
    """)

    # Teleconsultation Table (Req 5)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS teleconsultations (
        consultation_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id TEXT,
        provider TEXT,
        meeting_url TEXT,
        meeting_id TEXT,
        scheduled_date TEXT,
        scheduled_time TEXT,
        timezone TEXT,
        host_rehabilitator TEXT,
        notes TEXT,
        FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
    )
    """)

    # Seed initial test patient record if database is empty
    cur.execute("SELECT COUNT(*) FROM patients")
    if cur.fetchone()[0] == 0:
        cur.execute("""
        INSERT INTO patients (
            patient_id, full_name, date_of_birth, sex, country, preferred_language,
            phone, email, emergency_contact_name, emergency_contact_phone,
            diagnosis, diagnosis_date, affected_organ, laterality, injury_type,
            cause_mechanism, medical_history, surgery_history, current_medications,
            allergies, previous_rehab, functional_limitations, pain_info, mobility_limitations,
            referring_physician, assigned_rehabilitator, clinical_notes, medical_reports_uploaded,
            document_links, consent_authorization
        ) VALUES (
            'TRP-1001', 'Muhammad Hassan Raza Attari', '2005-10-14', 'Male', 'Pakistan', 'English',
            '+92 300 1234567', 'hassan@example.com', 'Family Member', '+92 300 7654321',
            'Post-Op Anterior Cruciate Ligament (ACL) Reconstruction', '2026-08-10', 'Knee Joint', 'Left',
            'Surgical Post-Op', 'Sports Injury', 'None', 'Left Knee ACL Reconstruction (Aug 2026)',
            'Analgesics (as needed)', 'None reported', 'None', 'Inability to fully flex knee past 90 degrees',
            'Moderate discomfort on weight bearing', 'Requires single crutch support',
            'Dr. Shahzaib Mughal', 'Dr. Ahmed Khan (PT)', 'Patient demonstrating steady post-op recovery. Avoid forced extension.',
            'MRI_PreOp_Knee.pdf, PostOp_XRay.pdf', 'https://clinical-records.example.com/TRP-1001', 1
        )
        """)

        # Seed plan assigned by Rehabilitator
        activities = json.dumps([
            {"task": "Passive Knee Extension on Bolster", "reps": "3 sets of 10 reps", "frequency": "2x Daily"},
            {"task": "Seated Heel Slides to Tolerance", "reps": "15 reps", "frequency": "3x Daily"},
            {"task": "Isometric Quadriceps Setting", "reps": "10-second holds x 10", "frequency": "2x Daily"}
        ])
        cur.execute("""
        INSERT INTO rehab_plans (patient_id, assigned_by, phase_name, effective_date, activities_json)
        VALUES ('TRP-1001', 'Dr. Ahmed Khan', 'Phase 2 — Mobility & Strength', '2026-09-01', ?)
        """, (activities,))

        # Seed teleconsultation meeting details
        cur.execute("""
        INSERT INTO teleconsultations (
            patient_id, provider, meeting_url, meeting_id, scheduled_date, scheduled_time, timezone, host_rehabilitator, notes
        ) VALUES (
            'TRP-1001', 'Enterprise Video Portal', 'https://meet.jit.si/TeleRehab-TRP-1001-Clinical',
            'TRP-CONF-8821', '2026-09-12', '14:30', 'PKT (UTC+5)', 'Dr. Ahmed Khan',
            'Review range of motion progress and adjust quadriceps loading.'
        )
        """)
        conn.commit()

init_db()

# Data Access Helper Functions
def fetch_patient_record(patient_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM patients WHERE patient_id = ?", (patient_id,))
    row = cur.fetchone()
    if not row:
        return None
    cols = [col[0] for col in cur.description]
    return dict(zip(cols, row))

def fetch_latest_assessment(patient_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM clinical_assessments WHERE patient_id = ? ORDER BY assessment_id DESC LIMIT 1", (patient_id,))
    row = cur.fetchone()
    if not row:
        return None
    cols = [col[0] for col in cur.description]
    return dict(zip(cols, row))

def fetch_rehab_plan(patient_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM rehab_plans WHERE patient_id = ? ORDER BY plan_id DESC LIMIT 1", (patient_id,))
    row = cur.fetchone()
    if not row:
        return None
    cols = [col[0] for col in cur.description]
    res = dict(zip(cols, row))
    if res and res.get('activities_json'):
        res['activities'] = json.loads(res['activities_json'])
    return res

def fetch_teleconsultation(patient_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM teleconsultations WHERE patient_id = ? ORDER BY consultation_id DESC LIMIT 1", (patient_id,))
    row = cur.fetchone()
    if not row:
        return None
    cols = [col[0] for col in cur.description]
    return dict(zip(cols, row))

# ==========================================
# 4. SIDEBAR & CONTEXT CONTROLS
# ==========================================
with st.sidebar:
    st.markdown("""
    <div style="padding: 10px 0 15px 0;">
        <h2 style="color:#FFFFFF; font-size:1.3rem; font-weight:800; margin:0;">TeleRehabilitation</h2>
        <p style="color:#0284C7; font-size:0.75rem; font-weight:700; margin:2px 0 0 0; letter-spacing: 0.5px;">CLINICAL SYSTEM</p>
    </div>
    """, unsafe_allow_html=True)

    # Language Selector (Req 6)
    selected_language = st.selectbox(
        "Preferred Language",
        ["English", "Urdu", "Arabic", "Spanish", "French"],
        index=0
    )
    t = TRANSLATIONS[selected_language]

    # Localization Parameters (Req 6)
    st.markdown("<hr style='border-color: #1E293B; margin: 12px 0;'>", unsafe_allow_html=True)
    country_setting = st.selectbox("Country / Locale", ["Pakistan", "United States", "Saudi Arabia", "United Kingdom", "Spain"])
    timezone_setting = st.selectbox("Time Zone", ["PKT (UTC+5)", "EST (UTC-5)", "AST (UTC+3)", "GMT (UTC+0)", "CET (UTC+1)"])
    unit_setting = st.selectbox("Measurement Units", ["Metric (Degrees / cm)", "Imperial (Degrees / in)"])

    st.markdown("<hr style='border-color: #1E293B; margin: 12px 0;'>", unsafe_allow_html=True)

    # Role Access Control (Req 2)
    portal_role = st.selectbox("Portal Role", ["Patient", "Rehabilitator / Doctor"])

    if portal_role == "Patient":
        # Strict isolation: Patient is locked to their authorized ID
        logged_patient_id = "TRP-1001"
        st.info(f"Authorized Account: **{logged_patient_id}**")
    else:
        # Doctor can select or manage patients
        logged_patient_id = st.selectbox("Active Patient Record", ["TRP-1001"])

# Fetch Patient Data strictly by patient_id
p = fetch_patient_record(logged_patient_id)
assessment = fetch_latest_assessment(logged_patient_id)
plan = fetch_rehab_plan(logged_patient_id)
tele = fetch_teleconsultation(logged_patient_id)

# ==========================================
# 5. PROFILE COMPLETION CALCULATION (Req 7)
# ==========================================
def calculate_profile_completion(p, assessment, tele):
    if not p:
        return 0, {}
    
    sections = {
        "patient_info": bool(p.get('full_name') and p.get('date_of_birth') and p.get('phone')),
        "clinical_diagnosis": bool(p.get('diagnosis') and p.get('diagnosis_date')),
        "affected_region": bool(p.get('affected_organ') and p.get('laterality')),
        "medical_records": bool(p.get('medical_reports_uploaded') or p.get('surgery_history')),
        "rehab_assessment": bool(assessment and assessment.get('rom_degrees') is not None),
        "teleconsultation": bool(tele and tele.get('meeting_url'))
    }
    
    completed_count = sum(sections.values())
    total_count = len(sections)
    percentage = int((completed_count / total_count) * 100)
    return percentage, sections

completion_pct, completion_status = calculate_profile_completion(p, assessment, tele)

# ==========================================
# 6. MAIN DASHBOARD CONTENT
# ==========================================

# Enterprise Header
st.markdown(f"""
<div style="background: #FFFFFF; padding: 20px 24px; border-radius: 12px; border: 1px solid #E2E8F0; margin-bottom: 20px;">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 style="font-size: 1.6rem; font-weight: 800; color: #0F172A; margin: 0;">{t['portal_title']}</h1>
            <p style="color: #64748B; font-size: 0.88rem; margin: 4px 0 0 0;">{t['subtitle']}</p>
        </div>
        <div style="text-align: right;">
            <span style="font-size: 0.8rem; font-weight: 700; color: #64748B;">PATIENT RECORD</span><br>
            <span style="font-size: 1.1rem; font-weight: 800; color: #0284C7;">{logged_patient_id}</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Requirement 7: First Dashboard Top Section - "Complete Clinical Profile"
st.markdown(f"""
<div class="clinical-card" style="border-left: 5px solid #0284C7;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
        <h3 style="margin:0; font-size: 1.1rem; font-weight: 700;">Clinical Profile Overview</h3>
        <span style="font-size: 1rem; font-weight: 800; color: #0284C7;">{t['profile_completion']}: {completion_pct}%</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.progress(completion_pct / 100.0)

# Section Completion Status Grid (Req 7)
sc1, sc2, sc3, sc4, sc5, sc6 = st.columns(6)
with sc1:
    st.markdown(f"**{t['patient_info']}**")
    st.markdown(f"<span class='status-badge {'status-completed' if completion_status['patient_info'] else 'status-pending'}'>{'Complete' if completion_status['patient_info'] else 'Incomplete'}</span>", unsafe_allow_html=True)
with sc2:
    st.markdown(f"**{t['clinical_diagnosis']}**")
    st.markdown(f"<span class='status-badge {'status-completed' if completion_status['clinical_diagnosis'] else 'status-pending'}'>{'Complete' if completion_status['clinical_diagnosis'] else 'Incomplete'}</span>", unsafe_allow_html=True)
with sc3:
    st.markdown(f"**{t['affected_region']}**")
    st.markdown(f"<span class='status-badge {'status-completed' if completion_status['affected_region'] else 'status-pending'}'>{'Complete' if completion_status['affected_region'] else 'Incomplete'}</span>", unsafe_allow_html=True)
with sc4:
    st.markdown(f"**{t['medical_records']}**")
    st.markdown(f"<span class='status-badge {'status-completed' if completion_status['medical_records'] else 'status-pending'}'>{'Complete' if completion_status['medical_records'] else 'Incomplete'}</span>", unsafe_allow_html=True)
with sc5:
    st.markdown(f"**{t['rehab_assessment']}**")
    st.markdown(f"<span class='status-badge {'status-completed' if completion_status['rehab_assessment'] else 'status-not-assessed'}'>{'Complete' if completion_status['rehab_assessment'] else 'Not Assessed'}</span>", unsafe_allow_html=True)
with sc6:
    st.markdown(f"**{t['teleconsultation']}**")
    st.markdown(f"<span class='status-badge {'status-scheduled' if completion_status['teleconsultation'] else 'status-not-assessed'}'>{'Scheduled' if completion_status['teleconsultation'] else 'Not Scheduled'}</span>", unsafe_allow_html=True)

st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)

# Navigation Options
nav_options = [t['nav_profile'], t['nav_assessment'], t['nav_plan'], t['nav_teleconsult']]
if portal_role == "Rehabilitator / Doctor":
    nav_options.append(t['nav_editor'])

selected_tab = st.radio("Navigation", nav_options, horizontal=True)

# ==========================================
# TAB 1: CLINICAL PROFILE & RECORD (Req 2)
# ==========================================
if selected_tab == t['nav_profile']:
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

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("#### Medical History & Functional Status")
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

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("#### Uploaded Medical Reports & Authorization")
        st.markdown(f"**Uploaded Documents:** {p['medical_reports_uploaded']}")
        st.markdown(f"**Document Link:** [{p['document_links']}]({p['document_links']})")
        st.markdown(f"**Consent & Authorization Status:** {'Granted' if p['consent_authorization'] else 'Pending'}")

# ==========================================
# TAB 2: REHABILITATION ASSESSMENT (Req 3 & 8)
# ==========================================
elif selected_tab == t['nav_assessment']:
    st.markdown("### Clinical Assessment & Measurement Metrics")
    
    # Requirement 8: Professional Rehabilitation Pathway
    st.markdown(f"#### {t['rehab_pathway']}")
    current_phase_name = plan['phase_name'] if plan else "Initial Assessment"
    
    steps = ["Initial Assessment", "Mobility & Strength", "Functional Training", "Return to Activity"]
    
    pathway_html = "<div class='pathway-container'>"
    for step in steps:
        if step in current_phase_name:
            pathway_html += f"<div class='pathway-step active'>{step} (Active)</div>"
        else:
            pathway_html += f"<div class='pathway-step'>{step}</div>"
    pathway_html += "</div>"
    st.markdown(pathway_html, unsafe_allow_html=True)

    # Requirement 3: NO fabricated values. Show "Not assessed yet" if null.
    st.markdown("#### Active Clinical Measurements")
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown("<div class='clinical-card'>", unsafe_allow_html=True)
        st.markdown("<div class='clinical-card-header'>Range of Motion (ROM)</div>", unsafe_allow_html=True)
        rom_val = assessment['rom_degrees'] if (assessment and assessment.get('rom_degrees')) else "Not assessed yet"
        st.markdown(f"<div class='clinical-card-value'>{rom_val}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='clinical-card'>", unsafe_allow_html=True)
        st.markdown("<div class='clinical-card-header'>Pain Score (VAS)</div>", unsafe_allow_html=True)
        pain_val = assessment['pain_score'] if (assessment and assessment.get('pain_score')) else "Not assessed yet"
        st.markdown(f"<div class='clinical-card-value'>{pain_val}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c3:
        st.markdown("<div class='clinical-card'>", unsafe_allow_html=True)
        st.markdown("<div class='clinical-card-header'>Muscle Strength</div>", unsafe_allow_html=True)
        str_val = assessment['strength_grade'] if (assessment and assessment.get('strength_grade')) else "Not assessed yet"
        st.markdown(f"<div class='clinical-card-value'>{str_val}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c4:
        st.markdown("<div class='clinical-card'>", unsafe_allow_html=True)
        st.markdown("<div class='clinical-card-header'>Functional Score</div>", unsafe_allow_html=True)
        fn_val = assessment['functional_score'] if (assessment and assessment.get('functional_score')) else "Not assessed yet"
        st.markdown(f"<div class='clinical-card-value'>{fn_val}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("#### Additional Clinical Indicators")
    c5, c6, c7 = st.columns(3)
    with c5:
        st.markdown(f"**Gait Assessment:** {assessment['gait_status'] if (assessment and assessment.get('gait_status')) else 'Not assessed yet'}")
    with c6:
        st.markdown(f"**Swelling / Edema:** {assessment['swelling_status'] if (assessment and assessment.get('swelling_status')) else 'Not assessed yet'}")
    with c7:
        st.markdown(f"**Balance Grade:** {assessment['balance_score'] if (assessment and assessment.get('balance_score')) else 'Not assessed yet'}")

# ==========================================
# TAB 3: CLINICAL CARE PLAN (Req 4)
# ==========================================
elif selected_tab == t['nav_plan']:
    st.markdown("### Clinical Rehabilitation Plan")
    
    if plan:
        st.markdown(f"""
        <div style="background: #FFFFFF; padding: 20px; border-radius: 12px; border-left: 5px solid #0284C7; border: 1px solid #E2E8F0; margin-bottom: 20px;">
            <p style="margin: 0; font-size: 0.9rem; font-weight: 700; color: #64748B;">{t['assigned_by'].upper()}: <span style="color:#0F172A;">{plan['assigned_by']}</span></p>
            <p style="margin: 4px 0; font-size: 0.9rem; font-weight: 700; color: #64748B;">CONDITION: <span style="color:#0F172A;">{p['diagnosis']}</span></p>
            <p style="margin: 4px 0; font-size: 0.9rem; font-weight: 700; color: #64748B;">AFFECTED REGION: <span style="color:#0F172A;">{p['laterality']} {p['affected_organ']}</span></p>
            <p style="margin: 4px 0; font-size: 0.9rem; font-weight: 700; color: #64748B;">{t['phase'].upper()}: <span style="color:#0284C7;">{plan['phase_name']}</span></p>
            <p style="margin: 4px 0 0 0; font-size: 0.85rem; color: #64748B;">{t['effective_from']}: {plan['effective_date']}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### Prescribed Clinical Activities")
        if plan.get('activities'):
            for idx, act in enumerate(plan['activities'], start=1):
                st.markdown(f"""
                <div class="clinical-card" style="margin-bottom: 10px; padding: 14px 18px;">
                    <strong style="font-size: 1rem; color: #0F172A;">{idx}. {act['task']}</strong><br>
                    <span style="font-size: 0.85rem; color: #475569;">Prescribed Dosage: {act['reps']} | Frequency: {act['frequency']}</span>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No rehabilitation plan assigned yet by your rehabilitator.")

# ==========================================
# TAB 4: TELECONSULTATION PORTAL (Req 5)
# ==========================================
elif selected_tab == t['nav_teleconsult']:
    st.markdown("### Teleconsultation Session")
    
    if tele and tele.get('meeting_url'):
        st.markdown(f"""
        <div class="clinical-card" style="border-top: 4px solid #0284C7;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h3 style="margin: 0; font-size: 1.2rem; color: #0F172A;">Scheduled Clinical Teleconsultation</h3>
                    <p style="margin: 4px 0 0 0; color: #64748B; font-size: 0.9rem;">Host: {tele['host_rehabilitator']}</p>
                </div>
                <span class="status-badge status-scheduled">Scheduled</span>
            </div>
            <hr style="border-color: #E2E8F0; margin: 16px 0;">
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; margin-bottom: 16px;">
                <div><strong>Provider:</strong><br>{tele['provider']}</div>
                <div><strong>Date & Time:</strong><br>{tele['scheduled_date']} at {tele['scheduled_time']} ({tele['timezone']})</div>
                <div><strong>Meeting ID:</strong><br>{tele['meeting_id']}</div>
            </div>
            <p><strong>Clinical Notes:</strong> {tele['notes']}</p>
            <div style="margin-top: 20px;">
                <a href="{tele['meeting_url']}" target="_blank" style="background-color: #0284C7; color: white; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: 700; display: inline-block;">
                    {t['join_meeting']}
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("No active teleconsultation session scheduled.")

# ==========================================
# TAB 5: REHABILITATOR CONSOLE (Doctor Edit)
# ==========================================
elif selected_tab == t.get('nav_editor'):
    st.markdown("### Clinical Record & Teleconsultation Management")
    st.caption("Authorized Rehabilitator Console for recording actual clinical measurements and plans.")

    with st.expander("1. Record Actual Clinical Assessment (No Defaults)", expanded=True):
        with st.form("assessment_form"):
            rom_input = st.text_input("Range of Motion (e.g. 95 degrees Flexion)", value=assessment['rom_degrees'] if assessment else "")
            pain_input = st.text_input("Pain Score (e.g. 3/10 VAS)", value=assessment['pain_score'] if assessment else "")
            strength_input = st.text_input("Muscle Strength (e.g. 4/5 Medical Research Council)", value=assessment['strength_grade'] if assessment else "")
            functional_input = st.text_input("Functional Score (e.g. Lower Extremity Functional Scale 45/80)", value=assessment['functional_score'] if assessment else "")
            
            submit_assess = st.form_submit_button("Save Assessment")
            if submit_assess:
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute("""
                INSERT INTO clinical_assessments (patient_id, rom_degrees, pain_score, strength_grade, functional_score, assessment_date)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (logged_patient_id, rom_input, pain_input, strength_input, functional_input, datetime.now().strftime("%Y-%m-%d")))
                conn.commit()
                st.success("Clinical assessment successfully saved.")
                st.rerun()

    with st.expander("2. Schedule / Update Teleconsultation Meeting"):
        with st.form("teleconsult_form"):
            t_provider = st.text_input("Provider", value="Enterprise Video Portal")
            t_url = st.text_input("Meeting URL", value=tele['meeting_url'] if tele else "https://meet.jit.si/")
            t_id = st.text_input("Meeting ID", value=tele['meeting_id'] if tele else "CONF-1001")
            t_date = st.date_input("Scheduled Date", value=date.today())
            t_time = st.time_input("Scheduled Time")
            t_tz = st.text_input("Timezone", value="PKT (UTC+5)")
            t_host = st.text_input("Host Rehabilitator Name", value="Dr. Ahmed Khan")
            t_notes = st.text_area("Session Notes", value="Review range of motion progress.")

            submit_tele = st.form_submit_button("Update Teleconsultation")
            if submit_tele:
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute("""
                INSERT INTO teleconsultations (patient_id, provider, meeting_url, meeting_id, scheduled_date, scheduled_time, timezone, host_rehabilitator, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (logged_patient_id, t_provider, t_url, t_id, str(t_date), str(t_time), t_tz, t_host, t_notes))
                conn.commit()
                st.success("Teleconsultation meeting updated.")
                st.rerun()
