import streamlit as st
import sqlite3
import json
from datetime import datetime, date

# ==============================================================================
# 1. SYSTEM PAGE CONFIGURATION & ENTERPRISE STYLESHEET
# ==============================================================================
st.set_page_config(
    page_title="Tekerehab Portal | Enterprise Rehabilitation System",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

DB_FILE = "tekerehab_clinical.db"

def inject_enterprise_styles():
    """
    Injects high-contrast CSS overrides to fix Streamlit white-on-white bugs,
    enforces dark slate typography (#0F172A), and styles sidebar and containers.
    """
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* Hide Streamlit default chrome headers and footers */
    #MainMenu, header, footer, [data-testid="stHeader"] { 
        visibility: hidden !important; 
        height: 0px !important;
    }
    
    .stAppViewContainer {
        padding-top: 0px !important;
    }

    html, body, [class*="css"], .stMarkdown {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: #0F172A !important;
    }

    .stApp {
        background-color: #F8FAFC !important;
    }

    /* Guaranteed Dark High-Contrast Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0F172A !important;
        border-right: 1px solid #1E293B !important;
    }

    [data-testid="stSidebar"] * {
        color: #F8FAFC !important;
    }

    [data-testid="stSidebar"] label {
        color: #94A3B8 !important;
        font-weight: 700 !important;
        font-size: 0.8rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }

    /* High-Contrast Clinical Card Containers */
    .clinical-card {
        background-color: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 12px !important;
        padding: 20px !important;
        box-shadow: 0 2px 4px rgba(15, 23, 42, 0.03) !important;
        margin-bottom: 16px !important;
    }

    /* Native Tab Styling Improvements */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #FFFFFF;
        padding: 8px;
        border-radius: 12px;
        border: 1px solid #CBD5E1;
    }

    .stTabs [data-baseweb="tab"] {
        height: 44px;
        white-space: pre;
        border-radius: 8px;
        color: #475569;
        font-weight: 600;
        font-size: 0.9rem;
        padding: 0px 16px;
    }

    .stTabs [aria-selected="true"] {
        background-color: #0284C7 !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }
    </style>
    """, unsafe_allow_html=True)

inject_enterprise_styles()

# ==============================================================================
# 2. INTERNATIONALIZATION (i18n) DICTIONARY
# ==============================================================================
TRANSLATIONS = {
    "English": {
        "portal_title": "Tekerehab Portal",
        "subtitle": "Enterprise Physical Rehabilitation & Teleconsultation System",
        "profile_completion": "Profile Completion",
        "patient_info": "Patient Information",
        "clinical_diagnosis": "Clinical Diagnosis",
        "affected_region": "Affected Region",
        "medical_records": "Medical Records",
        "rehab_assessment": "Rehab Assessment",
        "teleconsultation": "Teleconsultation",
        "complete": "Complete",
        "incomplete": "Incomplete",
        "scheduled": "Scheduled",
        "not_scheduled": "Not Scheduled",
        "not_assessed": "Not assessed yet",
        "join_meeting": "Launch Video Portal",
        "assigned_by": "Assigned by",
        "effective_from": "Effective from",
        "phase": "Current Phase",
        "rehab_pathway": "Rehabilitation Pathway",
        "tab_profile": "📋 Clinical Profile",
        "tab_assessment": "📊 Rehab Assessment",
        "tab_plan": "💪 Care Plan",
        "tab_teleconsult": "📹 Teleconsultation",
        "tab_editor": "⚙️ Doctor Console"
    },
    "Urdu": {
        "portal_title": "ٹیکی ری ہیب پورٹل",
        "subtitle": "پیشہ ورانہ کلینکل بحالی اور ٹیلی مشاورت کا نظام",
        "profile_completion": "پروفائل کی تکمیل",
        "patient_info": "مریض کی معلومات",
        "clinical_diagnosis": "کلینکل تشخیص",
        "affected_region": "متاثرہ حصہ",
        "medical_records": "طبی ریکارڈ",
        "rehab_assessment": "بحالی کا جائزہ",
        "teleconsultation": "ٹیلی مشاورت",
        "complete": "مکمل",
        "incomplete": "غیر مکمل",
        "scheduled": "شیڈول شدہ",
        "not_scheduled": "شیڈول نہیں",
        "not_assessed": "جائزہ باقی",
        "join_meeting": "ویڈیو پورٹل کھولیں",
        "assigned_by": "تعینات کردہ",
        "effective_from": "سے نافذ العمل",
        "phase": "موجودہ مرحلہ",
        "rehab_pathway": "بحالی کا راستہ",
        "tab_profile": "📋 کلینکل پروفائل",
        "tab_assessment": "📊 بحالی کا جائزہ",
        "tab_plan": "💪 کیئر پلان",
        "tab_teleconsult": "📹 ٹیلی پورٹل",
        "tab_editor": "⚙️ معالج کنسول"
    },
    "Arabic": {
        "portal_title": "بوابة تيكي ريهاب",
        "subtitle": "نظام إدارة إعادة التأهيل الطبي واستشارات العلاج الطبيعي",
        "profile_completion": "إكمال الملف",
        "patient_info": "معلومات المريض",
        "clinical_diagnosis": "التشخيص السريري",
        "affected_region": "المنطقة المصابة",
        "medical_records": "السجلات الطبية",
        "rehab_assessment": "تقييم التأهيل",
        "teleconsultation": "الاستشارة عن بُعد",
        "complete": "مكتمل",
        "incomplete": "غير مكتمل",
        "scheduled": "مجدول",
        "not_scheduled": "غير مجدول",
        "not_assessed": "لم يتم التقييم",
        "join_meeting": "الانضمام للمكالمة",
        "assigned_by": "المعالج المسؤول",
        "effective_from": "ساري من",
        "phase": "المرحلة الحالية",
        "rehab_pathway": "مسار التأهيل",
        "tab_profile": "📋 الملف السريري",
        "tab_assessment": "📊 تقييم التأهيل",
        "tab_plan": "💪 خطة الرعاية",
        "tab_teleconsult": "📹 بوابة الاستشارة",
        "tab_editor": "⚙️ لوحة المعالج"
    },
    "Spanish": {
        "portal_title": "Portal Tekerehab",
        "subtitle": "Gestión Clínica de Tele-Rehabilitación y Fisioterapia",
        "profile_completion": "Completitud del Perfil",
        "patient_info": "Información",
        "clinical_diagnosis": "Diagnóstico",
        "affected_region": "Región Afectada",
        "medical_records": "Registros Médicos",
        "rehab_assessment": "Evaluación Rehab",
        "teleconsultation": "Teleconsulta",
        "complete": "Completo",
        "incomplete": "Incompleto",
        "scheduled": "Programado",
        "not_scheduled": "No Programado",
        "not_assessed": "Aún no evaluado",
        "join_meeting": "Unirse a la Sesión",
        "assigned_by": "Asignado por",
        "effective_from": "Efectivo desde",
        "phase": "Fase Actual",
        "rehab_pathway": "Vía de Rehabilitación",
        "tab_profile": "📋 Perfil Clínico",
        "tab_assessment": "📊 Evaluación",
        "tab_plan": "💪 Plan de Cuidado",
        "tab_teleconsult": "📹 Teleconsulta",
        "tab_editor": "⚙️ Consola Doctor"
    },
    "French": {
        "portal_title": "Portail Tekerehab",
        "subtitle": "Système Clinique de Télé-Réadaptation et Physiothérapie",
        "profile_completion": "Complétion du Profil",
        "patient_info": "Informations",
        "clinical_diagnosis": "Diagnostic",
        "affected_region": "Région Touchée",
        "medical_records": "Dossiers Médicaux",
        "rehab_assessment": "Évaluation",
        "teleconsultation": "Téléconsultation",
        "complete": "Complet",
        "incomplete": "Incomplet",
        "scheduled": "Programmé",
        "not_scheduled": "Non Programmé",
        "not_assessed": "Pas encore évalué",
        "join_meeting": "Rejoindre la Session",
        "assigned_by": "Assigné par",
        "effective_from": "Effectif depuis",
        "phase": "Phase Actuelle",
        "rehab_pathway": "Parcours Réadaptation",
        "tab_profile": "📋 Profil Clinique",
        "tab_assessment": "📊 Évaluation",
        "tab_plan": "💪 Plan de Soins",
        "tab_teleconsult": "📹 Téléconsultation",
        "tab_editor": "⚙️ Console Médecin"
    }
}

# ==============================================================================
# 3. DATABASE SCHEMA & PERSISTENCE LAYER
# ==============================================================================
@st.cache_resource
def get_db_connection():
    return sqlite3.connect(DB_FILE, check_same_thread=False)

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    
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

    # Seed record
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
            'Surgical Post-Op', 'Sports Injury', 'None reported', 'Left Knee ACL Reconstruction (Aug 2026)',
            'Analgesics (as needed)', 'None reported', 'None', 'Inability to fully flex knee past 90 degrees',
            'Moderate discomfort on weight bearing', 'Requires single crutch support',
            'Dr. Shahzaib Mughal', 'Dr. Ahmed Khan (PT)', 'Patient demonstrating steady post-op recovery. Avoid forced extension.',
            'MRI_PreOp_Knee.pdf, PostOp_XRay.pdf', 'https://clinical-records.example.com/TRP-1001', 1
        )
        """)

        activities = json.dumps([
            {"task": "Passive Knee Extension on Bolster", "reps": "3 sets of 10 reps", "frequency": "2x Daily"},
            {"task": "Seated Heel Slides to Tolerance", "reps": "15 reps", "frequency": "3x Daily"},
            {"task": "Isometric Quadriceps Setting", "reps": "10-second holds x 10", "frequency": "2x Daily"}
        ])
        cur.execute("""
        INSERT INTO rehab_plans (patient_id, assigned_by, phase_name, effective_date, activities_json)
        VALUES ('TRP-1001', 'Dr. Ahmed Khan', 'Phase 2 — Mobility & Strength', '2026-09-01', ?)
        """, (activities,))

        cur.execute("""
        INSERT INTO teleconsultations (
            patient_id, provider, meeting_url, meeting_id, scheduled_date, scheduled_time, timezone, host_rehabilitator, notes
        ) VALUES (
            'TRP-1001', 'Enterprise Video Portal', 'https://meet.jit.si/Tekerehab-TRP-1001-Clinical',
            'TRP-CONF-8821', '2026-09-12', '14:30', 'PKT (UTC+5)', 'Dr. Ahmed Khan',
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

# ==============================================================================
# 4. SIDEBAR & CONTEXT CONTROLS
# ==============================================================================
with st.sidebar:
    st.markdown("""
    <div style="padding: 10px 0 15px 0; border-bottom: 1px solid #1E293B; margin-bottom: 15px;">
        <h2 style="color:#FFFFFF !important; font-size:1.4rem; font-weight:800; margin:0;">Tekerehab Portal</h2>
        <p style="color:#38BDF8 !important; font-size:0.75rem; font-weight:700; margin:4px 0 0 0; letter-spacing: 0.5px;">CLINICAL REHABILITATION</p>
    </div>
    """, unsafe_allow_html=True)

    selected_language = st.selectbox(
        "Preferred Language",
        ["English", "Urdu", "Arabic", "Spanish", "French"],
        index=0
    )
    t = TRANSLATIONS[selected_language]

    st.markdown("<hr style='border-color: #1E293B; margin: 12px 0;'>", unsafe_allow_html=True)
    country_setting = st.selectbox("Country / Locale", ["Pakistan", "United States", "Saudi Arabia", "United Kingdom", "Spain"])
    timezone_setting = st.selectbox("Time Zone", ["PKT (UTC+5)", "EST (UTC-5)", "AST (UTC+3)", "GMT (UTC+0)", "CET (UTC+1)"])

    st.markdown("<hr style='border-color: #1E293B; margin: 12px 0;'>", unsafe_allow_html=True)
    portal_role = st.selectbox("Portal Access Role", ["Patient", "Rehabilitator / Doctor"])

    if portal_role == "Patient":
        logged_patient_id = "TRP-1001"
        st.success(f"Active Account: **{logged_patient_id}**")
    else:
        logged_patient_id = st.selectbox("Select Patient Record", ["TRP-1001"])

p = fetch_patient_record(logged_patient_id)
assessment = fetch_latest_assessment(logged_patient_id)
plan = fetch_rehab_plan(logged_patient_id)
tele = fetch_teleconsultation(logged_patient_id)

# ==============================================================================
# 5. PROFILE COMPLETION CALCULATOR
# ==============================================================================
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

# ==============================================================================
# 6. HEADER & PROFILE OVERVIEW (Pure HTML Component - Zero Text Invisibility)
# ==============================================================================

# Dashboard Title Header Card
st.markdown(f"""
<div style="background-color: #FFFFFF; padding: 20px 24px; border-radius: 12px; border: 1px solid #CBD5E1; margin-bottom: 20px;">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
        <div>
            <h1 style="font-size: 1.6rem; font-weight: 800; color: #0F172A !important; margin: 0;">{t['portal_title']}</h1>
            <p style="color: #475569 !important; font-size: 0.88rem; margin: 4px 0 0 0; font-weight: 500;">{t['subtitle']}</p>
        </div>
        <div style="text-align: right;">
            <span style="font-size: 0.75rem; font-weight: 700; color: #64748B !important; letter-spacing: 0.5px; text-transform: uppercase;">PATIENT RECORD</span><br>
            <span style="font-size: 1.1rem; font-weight: 800; color: #0284C7 !important; background-color: #F0F9FF; padding: 3px 12px; border-radius: 6px; border: 1px solid #BAE6FD;">{logged_patient_id}</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Profile Overview Panel Card
status_info_bg = "#D1FAE5" if completion_status.get('patient_info') else "#FEF3C7"
status_info_text = "#065F46" if completion_status.get('patient_info') else "#92400E"
status_info_label = t['complete'] if completion_status.get('patient_info') else t['incomplete']

status_diag_bg = "#D1FAE5" if completion_status.get('clinical_diagnosis') else "#FEF3C7"
status_diag_text = "#065F46" if completion_status.get('clinical_diagnosis') else "#92400E"
status_diag_label = t['complete'] if completion_status.get('clinical_diagnosis') else t['incomplete']

status_aff_bg = "#D1FAE5" if completion_status.get('affected_region') else "#FEF3C7"
status_aff_text = "#065F46" if completion_status.get('affected_region') else "#92400E"
status_aff_label = t['complete'] if completion_status.get('affected_region') else t['incomplete']

status_rec_bg = "#D1FAE5" if completion_status.get('medical_records') else "#FEF3C7"
status_rec_text = "#065F46" if completion_status.get('medical_records') else "#92400E"
status_rec_label = t['complete'] if completion_status.get('medical_records') else t['incomplete']

status_ass_bg = "#D1FAE5" if completion_status.get('rehab_assessment') else "#F1F5F9"
status_ass_text = "#065F46" if completion_status.get('rehab_assessment') else "#334155"
status_ass_label = t['complete'] if completion_status.get('rehab_assessment') else t['not_assessed']

status_tele_bg = "#E0F2FE" if completion_status.get('teleconsultation') else "#F1F5F9"
status_tele_text = "#075985" if completion_status.get('teleconsultation') else "#334155"
status_tele_label = t['scheduled'] if completion_status.get('teleconsultation') else t['not_scheduled']

st.markdown(f"""
<div style="background-color: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 12px; padding: 20px; border-left: 6px solid #0284C7; margin-bottom: 24px; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
        <h3 style="margin:0; font-size: 1.15rem; font-weight: 800; color: #0F172A !important;">Clinical Profile Overview</h3>
        <span style="font-size: 1.05rem; font-weight: 800; color: #0284C7 !important; background-color: #F0F9FF; padding: 4px 12px; border-radius: 8px; border: 1px solid #BAE6FD;">
            {t['profile_completion']}: {completion_pct}%
        </span>
    </div>
    <div style="width: 100%; background-color: #E2E8F0; height: 10px; border-radius: 5px; overflow: hidden; margin-bottom: 20px;">
        <div style="width: {completion_pct}%; background-color: #0284C7; height: 100%; transition: width 0.5s ease;"></div>
    </div>
    
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px;">
        <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 12px; border-radius: 8px; text-align: center;">
            <div style="font-size: 0.75rem; font-weight: 700; color: #475569 !important; text-transform: uppercase; margin-bottom: 6px;">{t['patient_info']}</div>
            <span style="background-color: {status_info_bg}; color: {status_info_text} !important; padding: 4px 10px; border-radius: 6px; font-size: 0.8rem; font-weight: 700; display: inline-block;">{status_info_label}</span>
        </div>
        <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 12px; border-radius: 8px; text-align: center;">
            <div style="font-size: 0.75rem; font-weight: 700; color: #475569 !important; text-transform: uppercase; margin-bottom: 6px;">{t['clinical_diagnosis']}</div>
            <span style="background-color: {status_diag_bg}; color: {status_diag_text} !important; padding: 4px 10px; border-radius: 6px; font-size: 0.8rem; font-weight: 700; display: inline-block;">{status_diag_label}</span>
        </div>
        <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 12px; border-radius: 8px; text-align: center;">
            <div style="font-size: 0.75rem; font-weight: 700; color: #475569 !important; text-transform: uppercase; margin-bottom: 6px;">{t['affected_region']}</div>
            <span style="background-color: {status_aff_bg}; color: {status_aff_text} !important; padding: 4px 10px; border-radius: 6px; font-size: 0.8rem; font-weight: 700; display: inline-block;">{status_aff_label}</span>
        </div>
        <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 12px; border-radius: 8px; text-align: center;">
            <div style="font-size: 0.75rem; font-weight: 700; color: #475569 !important; text-transform: uppercase; margin-bottom: 6px;">{t['medical_records']}</div>
            <span style="background-color: {status_rec_bg}; color: {status_rec_text} !important; padding: 4px 10px; border-radius: 6px; font-size: 0.8rem; font-weight: 700; display: inline-block;">{status_rec_label}</span>
        </div>
        <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 12px; border-radius: 8px; text-align: center;">
            <div style="font-size: 0.75rem; font-weight: 700; color: #475569 !important; text-transform: uppercase; margin-bottom: 6px;">{t['rehab_assessment']}</div>
            <span style="background-color: {status_ass_bg}; color: {status_ass_text} !important; padding: 4px 10px; border-radius: 6px; font-size: 0.8rem; font-weight: 700; display: inline-block;">{status_ass_label}</span>
        </div>
        <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 12px; border-radius: 8px; text-align: center;">
            <div style="font-size: 0.75rem; font-weight: 700; color: #475569 !important; text-transform: uppercase; margin-bottom: 6px;">{t['teleconsultation']}</div>
            <span style="background-color: {status_tele_bg}; color: {status_tele_text} !important; padding: 4px 10px; border-radius: 6px; font-size: 0.8rem; font-weight: 700; display: inline-block;">{status_tele_label}</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 7. CLEAN WORKSPACE TABS (Streamlit Native Tabs — Ultra Stable Layout)
# ==============================================================================

tab_list = [t['tab_profile'], t['tab_assessment'], t['tab_plan'], t['tab_teleconsult']]
if portal_role == "Rehabilitator / Doctor":
    tab_list.append(t['tab_editor'])

tabs = st.tabs(tab_list)

# TAB 1: CLINICAL PROFILE
with tabs[0]:
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

        st.markdown("<hr style='border-color: #CBD5E1;'>", unsafe_allow_html=True)
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

        st.markdown("<hr style='border-color: #CBD5E1;'>", unsafe_allow_html=True)
        st.markdown("#### Uploaded Medical Reports & Consent")
        st.markdown(f"**Uploaded Documents:** {p['medical_reports_uploaded']}")
        st.markdown(f"**Document Repository:** [{p['document_links']}]({p['document_links']})")
        st.markdown(f"**Authorization Consent Status:** {'Granted' if p['consent_authorization'] else 'Pending'}")

# TAB 2: REHABILITATION ASSESSMENT
with tabs[1]:
    st.markdown("### Clinical Assessment & Measurement Metrics")
    
    st.markdown(f"#### {t['rehab_pathway']}")
    current_phase_name = plan['phase_name'] if plan else "Initial Assessment"
    
    steps = ["Initial Assessment", "Mobility & Strength", "Functional Training", "Return to Activity"]
    
    pathway_items = ""
    for step in steps:
        if step in current_phase_name:
            pathway_items += f"<div style='flex:1; text-align:center; padding:10px; font-weight:800; font-size:0.85rem; color:#0284C7 !important; border-bottom:4px solid #0284C7; background:#F0F9FF;'>{step} (Active)</div>"
        else:
            pathway_items += f"<div style='flex:1; text-align:center; padding:10px; font-weight:600; font-size:0.85rem; color:#64748B !important; border-bottom:4px solid #E2E8F0;'>{step}</div>"
            
    st.markdown(f"""
    <div style="display: flex; background: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 10px; overflow: hidden; margin-bottom: 24px;">
        {pathway_items}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### Active Clinical Measurements")
    rom_val = assessment['rom_degrees'] if (assessment and assessment.get('rom_degrees')) else "Not assessed yet"
    pain_val = assessment['pain_score'] if (assessment and assessment.get('pain_score')) else "Not assessed yet"
    str_val = assessment['strength_grade'] if (assessment and assessment.get('strength_grade')) else "Not assessed yet"
    fn_val = assessment['functional_score'] if (assessment and assessment.get('functional_score')) else "Not assessed yet"

    st.markdown(f"""
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin-bottom: 24px;">
        <div style="background-color: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 12px; padding: 18px; box-shadow: 0 1px 3px rgba(0,0,0,0.02);">
            <div style="font-size: 0.8rem; font-weight: 700; color: #475569 !important; text-transform: uppercase;">Range of Motion (ROM)</div>
            <div style="font-size: 1.35rem; font-weight: 800; color: #0F172A !important; margin-top: 6px;">{rom_val}</div>
        </div>
        <div style="background-color: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 12px; padding: 18px; box-shadow: 0 1px 3px rgba(0,0,0,0.02);">
            <div style="font-size: 0.8rem; font-weight: 700; color: #475569 !important; text-transform: uppercase;">Pain Score (VAS)</div>
            <div style="font-size: 1.35rem; font-weight: 800; color: #0F172A !important; margin-top: 6px;">{pain_val}</div>
        </div>
        <div style="background-color: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 12px; padding: 18px; box-shadow: 0 1px 3px rgba(0,0,0,0.02);">
            <div style="font-size: 0.8rem; font-weight: 700; color: #475569 !important; text-transform: uppercase;">Muscle Strength</div>
            <div style="font-size: 1.35rem; font-weight: 800; color: #0F172A !important; margin-top: 6px;">{str_val}</div>
        </div>
        <div style="background-color: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 12px; padding: 18px; box-shadow: 0 1px 3px rgba(0,0,0,0.02);">
            <div style="font-size: 0.8rem; font-weight: 700; color: #475569 !important; text-transform: uppercase;">Functional Score</div>
            <div style="font-size: 1.35rem; font-weight: 800; color: #0F172A !important; margin-top: 6px;">{fn_val}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### Additional Clinical Indicators")
    c5, c6, c7 = st.columns(3)
    with c5:
        st.markdown(f"**Gait Assessment:** {assessment['gait_status'] if (assessment and assessment.get('gait_status')) else 'Not assessed yet'}")
    with c6:
        st.markdown(f"**Swelling / Edema:** {assessment['swelling_status'] if (assessment and assessment.get('swelling_status')) else 'Not assessed yet'}")
    with c7:
        st.markdown(f"**Balance Grade:** {assessment['balance_score'] if (assessment and assessment.get('balance_score')) else 'Not assessed yet'}")

# TAB 3: CARE PLAN
with tabs[2]:
    st.markdown("### Clinical Rehabilitation Care Plan")
    if plan:
        st.markdown(f"""
        <div style="background-color: #FFFFFF; border: 1px solid #CBD5E1; border-left: 6px solid #0284C7; border-radius: 12px; padding: 20px; margin-bottom: 20px;">
            <p style="margin: 0; font-size: 0.85rem; font-weight: 700; color: #475569 !important; text-transform: uppercase;">{t['assigned_by']}: <span style="color:#0F172A !important;">{plan['assigned_by']}</span></p>
            <p style="margin: 4px 0; font-size: 1rem; font-weight: 700; color: #0F172A !important;">Condition: {p['diagnosis']}</p>
            <p style="margin: 4px 0; font-size: 0.95rem; font-weight: 700; color: #0284C7 !important;">{t['phase']}: {plan['phase_name']}</p>
            <p style="margin: 4px 0 0 0; font-size: 0.85rem; color: #475569 !important;">{t['effective_from']}: {plan['effective_date']}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### Prescribed Clinical Activities")
        if plan.get('activities'):
            for idx, act in enumerate(plan['activities'], start=1):
                st.markdown(f"""
                <div style="background-color: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 10px; padding: 14px 18px; margin-bottom: 10px;">
                    <strong style="font-size: 1rem; color: #0F172A !important;">{idx}. {act['task']}</strong><br>
                    <span style="font-size: 0.88rem; color: #334155 !important;">Prescribed Dosage: {act['reps']} | Frequency: {act['frequency']}</span>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No rehabilitation plan assigned yet by your rehabilitator.")

# TAB 4: TELECONSULTATION
with tabs[3]:
    st.markdown("### Teleconsultation Session")
    if tele and tele.get('meeting_url'):
        st.markdown(f"""
        <div style="background-color: #FFFFFF; border: 1px solid #CBD5E1; border-top: 5px solid #0284C7; border-radius: 12px; padding: 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                <div>
                    <h3 style="margin:0; font-size: 1.15rem; font-weight: 800; color: #0F172A !important;">Scheduled Clinical Teleconsultation</h3>
                    <p style="margin: 4px 0 0 0; font-size: 0.88rem; color: #475569 !important;">Host / Rehabilitator: {tele['host_rehabilitator']}</p>
                </div>
                <span style="background-color: #E0F2FE; color: #075985 !important; padding: 4px 12px; border-radius: 6px; font-weight: 700; font-size: 0.85rem;">Scheduled</span>
            </div>
            <hr style="border-color: #CBD5E1; margin: 16px 0;">
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 16px;">
                <div><strong style="color: #475569 !important; font-size: 0.8rem; text-transform: uppercase;">Provider</strong><br><span style="color: #0F172A !important; font-weight: 700;">{tele['provider']}</span></div>
                <div><strong style="color: #475569 !important; font-size: 0.8rem; text-transform: uppercase;">Date & Time</strong><br><span style="color: #0F172A !important; font-weight: 700;">{tele['scheduled_date']} at {tele['scheduled_time']} ({tele['timezone']})</span></div>
                <div><strong style="color: #475569 !important; font-size: 0.8rem; text-transform: uppercase;">Meeting ID</strong><br><span style="color: #0F172A !important; font-weight: 700;">{tele['meeting_id']}</span></div>
            </div>
            <p style="color: #334155 !important;"><strong>Clinical Notes:</strong> {tele['notes']}</p>
            <div style="margin-top: 20px;">
                <a href="{tele['meeting_url']}" target="_blank" style="background-color: #0284C7; color: white !important; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: 700; display: inline-block;">
                    {t['join_meeting']}
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("No active teleconsultation session scheduled.")

# TAB 5: DOCTOR CONSOLE (Conditional)
if portal_role == "Rehabilitator / Doctor":
    with tabs[4]:
        st.markdown("### Clinical Record & Teleconsultation Management")
        st.caption("Authorized Rehabilitator Console for entering actual clinical measurements and scheduling sessions.")

        with st.expander("1. Record Actual Clinical Assessment (No Defaults)", expanded=True):
            with st.form("assessment_form"):
                rom_input = st.text_input("Range of Motion (e.g., 95 degrees Flexion)", value=assessment['rom_degrees'] if assessment else "")
                pain_input = st.text_input("Pain Score (e.g., 3/10 VAS)", value=assessment['pain_score'] if assessment else "")
                strength_input = st.text_input("Muscle Strength (e.g., 4/5 MRC Grade)", value=assessment['strength_grade'] if assessment else "")
                functional_input = st.text_input("Functional Score (e.g., LEFS 45/80)", value=assessment['functional_score'] if assessment else "")
                
                submit_assess = st.form_submit_button("Save Assessment Record")
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

        with st.expander("2. Schedule / Update Teleconsultation Session"):
            with st.form("teleconsult_form"):
                t_provider = st.text_input("Provider Name", value="Enterprise Video Portal")
                t_url = st.text_input("Meeting Link URL", value=tele['meeting_url'] if tele else "https://meet.jit.si/")
                t_id = st.text_input("Meeting ID", value=tele['meeting_id'] if tele else "CONF-1001")
                t_date = st.date_input("Scheduled Date", value=date.today())
                t_time = st.time_input("Scheduled Time")
                t_tz = st.text_input("Timezone", value="PKT (UTC+5)")
                t_host = st.text_input("Host Rehabilitator Name", value="Dr. Ahmed Khan")
                t_notes = st.text_area("Clinical Session Notes", value="Review range of motion progress and strength loading.")

                submit_tele = st.form_submit_button("Update Teleconsultation Schedule")
                if submit_tele:
                    conn = get_db_connection()
                    cur = conn.cursor()
                    cur.execute("""
                    INSERT INTO teleconsultations (patient_id, provider, meeting_url, meeting_id, scheduled_date, scheduled_time, timezone, host_rehabilitator, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (logged_patient_id, t_provider, t_url, t_id, str(t_date), str(t_time), t_tz, t_host, t_notes))
                    conn.commit()
                    st.success("Teleconsultation session details updated.")
                    st.rerun()
