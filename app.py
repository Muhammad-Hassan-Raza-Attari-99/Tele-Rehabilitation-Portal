import streamlit as st
import sqlite3
import hashlib
import html
from datetime import datetime, date, time as dt_time
from urllib.parse import urlparse

# ============================================================
# TELE REHABILITATION PORTAL
# Production-oriented Streamlit reference implementation
# ============================================================

APP_TITLE = "TeleRehabilitation Portal"
DB_PATH = "telerehabilitation.db"

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# PROFESSIONAL UI
# ============================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: Inter, sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 8% 5%, rgba(33, 150, 243, .08), transparent 28%),
        radial-gradient(circle at 92% 8%, rgba(20, 184, 166, .07), transparent 28%),
        #07111f;
    color: #edf3fb;
}

.block-container {
    max-width: 1450px;
    padding-top: 1.25rem;
    padding-bottom: 4rem;
}

section[data-testid="stSidebar"] {
    background: #091625;
    border-right: 1px solid rgba(255,255,255,.08);
}

section[data-testid="stSidebar"] * {
    color: #e8eef7 !important;
}

h1, h2, h3, h4 {
    letter-spacing: -0.025em;
}

.portal-header {
    padding: 1.1rem 1.35rem;
    border: 1px solid rgba(255,255,255,.09);
    border-radius: 18px;
    background: linear-gradient(135deg, rgba(19,48,77,.96), rgba(10,30,49,.96));
    margin-bottom: 1.2rem;
}

.portal-brand {
    font-size: 1.65rem;
    font-weight: 800;
    color: #ffffff;
}

.portal-subtitle {
    color: #9fb0c5;
    margin-top: .25rem;
    font-size: .94rem;
}

.section-card {
    padding: 1.15rem 1.25rem;
    border: 1px solid rgba(255,255,255,.08);
    border-radius: 16px;
    background: rgba(15,32,51,.88);
    margin-bottom: 1rem;
}

.metric-card {
    padding: 1rem 1.1rem;
    border: 1px solid rgba(255,255,255,.08);
    border-radius: 15px;
    background: #102238;
    min-height: 105px;
}

.metric-label {
    color: #9fb0c5;
    font-size: .82rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: .045em;
}

.metric-value {
    color: #ffffff;
    font-size: 1.65rem;
    font-weight: 800;
    margin-top: .25rem;
}

.status-complete {
    color: #69d7bd;
    font-weight: 700;
}

.status-pending {
    color: #f0c76b;
    font-weight: 700;
}

.status-info {
    color: #77b7ff;
    font-weight: 700;
}

.notice {
    padding: .85rem 1rem;
    border-radius: 12px;
    background: rgba(34, 61, 88, .72);
    border: 1px solid rgba(119,183,255,.18);
    color: #dbe9f8;
    margin: .5rem 0 1rem;
}

.clinical-warning {
    padding: .9rem 1rem;
    border-radius: 12px;
    background: rgba(102, 76, 21, .22);
    border: 1px solid rgba(240,199,107,.25);
    color: #f4ddb0;
    margin: .5rem 0 1rem;
}

.patient-banner {
    padding: 1rem 1.2rem;
    border-radius: 14px;
    background: linear-gradient(135deg, #112e49, #0e2034);
    border: 1px solid rgba(119,183,255,.14);
    margin-bottom: 1rem;
}

.small-muted {
    color: #91a4b9;
    font-size: .86rem;
}

hr {
    border-color: rgba(255,255,255,.08);
}

div[data-testid="stButton"] > button {
    border-radius: 10px;
    min-height: 2.55rem;
    font-weight: 650;
}

a {
    color: #77b7ff !important;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# DATABASE
# ============================================================

def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            patient_id TEXT PRIMARY KEY,
            full_name TEXT NOT NULL,
            dob TEXT,
            sex TEXT,
            country TEXT,
            preferred_language TEXT,
            phone TEXT,
            email TEXT,
            emergency_contact TEXT,
            diagnosis TEXT,
            diagnosis_date TEXT,
            affected_region TEXT,
            laterality TEXT,
            condition_type TEXT,
            mechanism TEXT,
            medical_history TEXT,
            surgery_history TEXT,
            medications TEXT,
            allergies TEXT,
            previous_rehab TEXT,
            functional_limitations TEXT,
            pain_notes TEXT,
            referring_physician TEXT,
            assigned_rehabilitator TEXT,
            clinical_notes TEXT,
            consent_status TEXT DEFAULT 'Pending',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT NOT NULL,
            assessment_date TEXT NOT NULL,
            rom_value REAL,
            rom_unit TEXT,
            pain_score REAL,
            strength_grade TEXT,
            gait_status TEXT,
            functional_score REAL,
            notes TEXT,
            assessed_by TEXT,
            FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS rehabilitation_plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT NOT NULL,
            phase TEXT NOT NULL,
            phase_name TEXT NOT NULL,
            plan_title TEXT NOT NULL,
            instructions TEXT,
            start_date TEXT,
            end_date TEXT,
            assigned_by TEXT NOT NULL,
            status TEXT DEFAULT 'Assigned',
            FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS meetings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT NOT NULL,
            provider_name TEXT NOT NULL,
            provider_role TEXT NOT NULL,
            meeting_provider TEXT,
            meeting_url TEXT,
            meeting_id TEXT,
            scheduled_date TEXT,
            scheduled_time TEXT,
            timezone TEXT,
            notes TEXT,
            FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT NOT NULL,
            record_type TEXT NOT NULL,
            title TEXT NOT NULL,
            url TEXT,
            notes TEXT,
            uploaded_by TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
        )
    """)

    # Safe demo seed. Clinical measurements intentionally remain empty.
    existing = cur.execute(
        "SELECT patient_id FROM patients WHERE patient_id = ?",
        ("TRP-1001",)
    ).fetchone()

    if not existing:
        now = datetime.now().isoformat(timespec="seconds")
        cur.execute("""
            INSERT INTO patients (
                patient_id, full_name, dob, sex, country, preferred_language,
                phone, email, emergency_contact, diagnosis, diagnosis_date,
                affected_region, laterality, condition_type, mechanism,
                medical_history, surgery_history, medications, allergies,
                previous_rehab, functional_limitations, pain_notes,
                referring_physician, assigned_rehabilitator, clinical_notes,
                consent_status, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "TRP-1001",
            "Demo Patient",
            "",
            "",
            "Pakistan",
            "English",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "Rehabilitation Team",
            "",
            "",
            "Pending",
            now,
            now,
        ))

    conn.commit()
    conn.close()

@st.cache_resource
def database_initialized():
    init_db()
    return True

database_initialized()

# ============================================================
# HELPERS
# ============================================================

def q(sql, params=(), fetchone=False, commit=False):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(sql, params)
    if commit:
        conn.commit()
        conn.close()
        return True
    result = cur.fetchone() if fetchone else cur.fetchall()
    conn.close()
    return result

def esc(value):
    return html.escape(str(value or ""))

def is_valid_url(value):
    if not value:
        return False
    try:
        p = urlparse(value)
        return p.scheme in ("http", "https") and bool(p.netloc)
    except Exception:
        return False

def pct_complete(patient):
    fields = [
        "full_name", "dob", "sex", "country", "preferred_language",
        "diagnosis", "affected_region", "laterality",
        "assigned_rehabilitator", "consent_status"
    ]
    completed = sum(bool(patient[f]) and patient[f] != "Pending" for f in fields)
    return round((completed / len(fields)) * 100)

def hash_value(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()

def get_patient(patient_id):
    return q(
        "SELECT * FROM patients WHERE patient_id = ?",
        (patient_id,),
        fetchone=True
    )

def get_assessment(patient_id):
    return q("""
        SELECT * FROM assessments
        WHERE patient_id = ?
        ORDER BY assessment_date DESC, id DESC
        LIMIT 1
    """, (patient_id,), fetchone=True)

def get_meeting(patient_id):
    return q("""
        SELECT * FROM meetings
        WHERE patient_id = ?
        ORDER BY scheduled_date DESC, id DESC
        LIMIT 1
    """, (patient_id,), fetchone=True)

def get_plan(patient_id):
    return q("""
        SELECT * FROM rehabilitation_plans
        WHERE patient_id = ?
        ORDER BY id DESC
        LIMIT 1
    """, (patient_id,), fetchone=True)

def get_records(patient_id):
    return q("""
        SELECT * FROM records
        WHERE patient_id = ?
        ORDER BY created_at DESC
    """, (patient_id,))

def save_patient(data):
    now = datetime.now().isoformat(timespec="seconds")
    q("""
        UPDATE patients SET
            full_name=?, dob=?, sex=?, country=?, preferred_language=?,
            phone=?, email=?, emergency_contact=?, diagnosis=?,
            diagnosis_date=?, affected_region=?, laterality=?,
            condition_type=?, mechanism=?, medical_history=?,
            surgery_history=?, medications=?, allergies=?,
            previous_rehab=?, functional_limitations=?, pain_notes=?,
            referring_physician=?, assigned_rehabilitator=?,
            clinical_notes=?, consent_status=?, updated_at=?
        WHERE patient_id=?
    """, (
        data["full_name"], data["dob"], data["sex"], data["country"],
        data["preferred_language"], data["phone"], data["email"],
        data["emergency_contact"], data["diagnosis"], data["diagnosis_date"],
        data["affected_region"], data["laterality"], data["condition_type"],
        data["mechanism"], data["medical_history"], data["surgery_history"],
        data["medications"], data["allergies"], data["previous_rehab"],
        data["functional_limitations"], data["pain_notes"],
        data["referring_physician"], data["assigned_rehabilitator"],
        data["clinical_notes"], data["consent_status"], now,
        data["patient_id"]
    ), commit=True)

def role_can_edit(role):
    return role in ("Rehabilitator", "Doctor", "Administrator")

# ============================================================
# SESSION / ACCESS MODEL
# ============================================================

if "role" not in st.session_state:
    st.session_state.role = "Patient"

if "patient_id" not in st.session_state:
    st.session_state.patient_id = "TRP-1001"

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("## TeleRehabilitation")
    st.caption("Clinical care coordination portal")

    st.markdown("---")
    role = st.selectbox(
        "Portal role",
        ["Patient", "Rehabilitator", "Doctor", "Administrator"],
        index=["Patient", "Rehabilitator", "Doctor", "Administrator"].index(
            st.session_state.role
        )
    )
    st.session_state.role = role

    # Demo role isolation: patient sees only their assigned patient ID.
    if role == "Patient":
        patient_choices = ["TRP-1001"]
    else:
        rows = q("SELECT patient_id FROM patients ORDER BY patient_id")
        patient_choices = [r["patient_id"] for r in rows]

    selected_patient = st.selectbox(
        "Patient record",
        patient_choices,
        index=patient_choices.index(st.session_state.patient_id)
        if st.session_state.patient_id in patient_choices else 0
    )
    st.session_state.patient_id = selected_patient

    st.markdown("---")
    st.caption("Access is role-based. In production, connect this layer to your organization’s SSO/OAuth/identity provider.")

patient = get_patient(st.session_state.patient_id)

if not patient:
    st.error("Patient record could not be found.")
    st.stop()

# ============================================================
# HEADER
# ============================================================

st.markdown(f"""
<div class="portal-header">
    <div class="portal-brand">{APP_TITLE}</div>
    <div class="portal-subtitle">
        Secure clinical coordination, rehabilitation planning and teleconsultation
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="patient-banner">
    <strong>{esc(patient["full_name"])}</strong>
    <span class="small-muted"> · Patient ID: {esc(patient["patient_id"])}</span>
    <span class="small-muted"> · Portal role: {esc(st.session_state.role)}</span>
</div>
""", unsafe_allow_html=True)

# ============================================================
# NAVIGATION
# ============================================================

tabs = st.tabs([
    "Overview",
    "Clinical Profile",
    "Assessment",
    "Rehabilitation Plan",
    "Teleconsultation",
    "Medical Records",
])

# ============================================================
# OVERVIEW
# ============================================================

with tabs[0]:
    completion = pct_complete(patient)
    assessment = get_assessment(patient["patient_id"])
    meeting = get_meeting(patient["patient_id"])
    plan = get_plan(patient["patient_id"])

    st.title("Clinical Overview")
    st.caption("A concise view of the patient's current care record.")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Profile completion</div>
            <div class="metric-value">{completion}%</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        value = patient["affected_region"] or "Not recorded"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Affected region</div>
            <div class="metric-value">{esc(value)}</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        value = "Recorded" if assessment else "Not assessed"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Clinical assessment</div>
            <div class="metric-value">{esc(value)}</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        value = "Scheduled" if meeting else "Not scheduled"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Teleconsultation</div>
            <div class="metric-value">{esc(value)}</div>
        </div>
        """, unsafe_allow_html=True)

    st.subheader("Care record status")

    status_items = [
        ("Patient information", bool(patient["full_name"])),
        ("Clinical diagnosis", bool(patient["diagnosis"])),
        ("Affected body region", bool(patient["affected_region"])),
        ("Assigned rehabilitator", bool(patient["assigned_rehabilitator"])),
        ("Consent / authorization", patient["consent_status"] == "Approved"),
        ("Clinical assessment", bool(assessment)),
        ("Rehabilitation plan", bool(plan)),
        ("Teleconsultation", bool(meeting)),
    ]

    cols = st.columns(2)
    for i, (label, complete) in enumerate(status_items):
        with cols[i % 2]:
            state = "Complete" if complete else "Pending"
            css = "status-complete" if complete else "status-pending"
            st.markdown(
                f"**{esc(label)}**  ·  <span class='{css}'>{state}</span>",
                unsafe_allow_html=True
            )

    if not patient["diagnosis"] or not patient["affected_region"]:
        st.markdown("""
        <div class="clinical-warning">
            Clinical measurements are intentionally withheld until the diagnosis and
            affected body region are recorded and an authorized clinician performs an assessment.
            The portal never invents ROM, pain, strength or functional values.
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# CLINICAL PROFILE
# ============================================================

with tabs[1]:
    st.title("Clinical Profile")
    st.caption("Complete the patient's record before clinical measurements are documented.")

    editable = role_can_edit(st.session_state.role)

    with st.form("patient_profile_form"):
        st.subheader("Patient identity and demographics")
        a, b, c = st.columns(3)

        with a:
            full_name = st.text_input("Full name", value=patient["full_name"] or "")
            dob = st.text_input("Date of birth", value=patient["dob"] or "", placeholder="YYYY-MM-DD")
            sex = st.selectbox(
                "Sex",
                ["", "Female", "Male", "Intersex", "Prefer not to say"],
                index=["", "Female", "Male", "Intersex", "Prefer not to say"].index(patient["sex"] or "")
            )
        with b:
            country = st.text_input("Country", value=patient["country"] or "")
            language_options = ["English", "Urdu", "Arabic", "French", "Spanish", "German", "Chinese", "Other"]
            language_index = language_options.index(patient["preferred_language"]) if patient["preferred_language"] in language_options else 0
            preferred_language = st.selectbox("Preferred language", language_options, index=language_index)
            phone = st.text_input("Phone", value=patient["phone"] or "")
        with c:
            email = st.text_input("Email", value=patient["email"] or "")
            emergency_contact = st.text_input("Emergency contact", value=patient["emergency_contact"] or "")
            consent_options = ["Pending", "Approved", "Declined", "Expired"]
            consent_index = consent_options.index(patient["consent_status"]) if patient["consent_status"] in consent_options else 0
            consent_status = st.selectbox("Consent / authorization", consent_options, index=consent_index)

        st.divider()
        st.subheader("Diagnosis and affected body region")
        a, b, c = st.columns(3)
        with a:
            diagnosis = st.text_area("Diagnosis", value=patient["diagnosis"] or "", height=100)
            diagnosis_date = st.text_input("Diagnosis date", value=patient["diagnosis_date"] or "", placeholder="YYYY-MM-DD")
        with b:
            affected_region = st.text_input("Affected organ / body region", value=patient["affected_region"] or "")
            laterality_options = ["", "Left", "Right", "Bilateral", "Not applicable"]
            laterality_index = laterality_options.index(patient["laterality"]) if patient["laterality"] in laterality_options else 0
            laterality = st.selectbox("Laterality", laterality_options, index=laterality_index)
        with c:
            condition_type = st.text_input("Condition / injury type", value=patient["condition_type"] or "")
            mechanism = st.text_input("Cause / mechanism", value=patient["mechanism"] or "")

        st.divider()
        st.subheader("Medical history")
        a, b = st.columns(2)
        with a:
            medical_history = st.text_area("Relevant medical history", value=patient["medical_history"] or "", height=120)
            surgery_history = st.text_area("Surgery / procedure history", value=patient["surgery_history"] or "", height=120)
            medications = st.text_area("Current medications", value=patient["medications"] or "", height=120)
        with b:
            allergies = st.text_area("Allergies", value=patient["allergies"] or "", height=120)
            previous_rehab = st.text_area("Previous rehabilitation", value=patient["previous_rehab"] or "", height=120)
            functional_limitations = st.text_area("Functional limitations", value=patient["functional_limitations"] or "", height=120)

        pain_notes = st.text_area("Pain information / patient-reported symptoms", value=patient["pain_notes"] or "", height=100)

        st.divider()
        st.subheader("Care team")
        a, b, c = st.columns(3)
        with a:
            referring_physician = st.text_input("Referring physician", value=patient["referring_physician"] or "")
        with b:
            assigned_rehabilitator = st.text_input("Assigned rehabilitator", value=patient["assigned_rehabilitator"] or "")
        with c:
            clinical_notes = st.text_area("Clinical notes", value=patient["clinical_notes"] or "", height=90)

        submitted = st.form_submit_button(
            "Save clinical profile",
            type="primary",
            disabled=not editable
        )

        if submitted and editable:
            save_patient({
                "patient_id": patient["patient_id"],
                "full_name": full_name.strip(),
                "dob": dob.strip(),
                "sex": sex,
                "country": country.strip(),
                "preferred_language": preferred_language,
                "phone": phone.strip(),
                "email": email.strip(),
                "emergency_contact": emergency_contact.strip(),
                "diagnosis": diagnosis.strip(),
                "diagnosis_date": diagnosis_date.strip(),
                "affected_region": affected_region.strip(),
                "laterality": laterality,
                "condition_type": condition_type.strip(),
                "mechanism": mechanism.strip(),
                "medical_history": medical_history.strip(),
                "surgery_history": surgery_history.strip(),
                "medications": medications.strip(),
                "allergies": allergies.strip(),
                "previous_rehab": previous_rehab.strip(),
                "functional_limitations": functional_limitations.strip(),
                "pain_notes": pain_notes.strip(),
                "referring_physician": referring_physician.strip(),
                "assigned_rehabilitator": assigned_rehabilitator.strip(),
                "clinical_notes": clinical_notes.strip(),
                "consent_status": consent_status,
            })
            st.success("Clinical profile saved.")
            st.rerun()

    if not editable:
        st.info("Patient role is read-only for clinical profile editing.")

# ============================================================
# ASSESSMENT
# ============================================================

with tabs[2]:
    st.title("Clinical Assessment")
    st.caption("Only authorized clinicians should record clinical measurements.")

    assessment = get_assessment(patient["patient_id"])

    if not patient["diagnosis"] or not patient["affected_region"]:
        st.markdown("""
        <div class="clinical-warning">
            Assessment is not ready. Enter the diagnosis and affected organ/body region first.
            No range-of-motion value is displayed or generated automatically.
        </div>
        """, unsafe_allow_html=True)

    if assessment:
        st.subheader("Latest recorded assessment")
        c1, c2, c3, c4 = st.columns(4)

        with c1:
            rom_display = (
                f'{assessment["rom_value"]} {assessment["rom_unit"]}'
                if assessment["rom_value"] is not None else "Not recorded"
            )
            st.metric("Range of motion", rom_display)

        with c2:
            pain_display = (
                f'{assessment["pain_score"]}/10'
                if assessment["pain_score"] is not None else "Not recorded"
            )
            st.metric("Pain score", pain_display)

        with c3:
            st.metric("Strength", assessment["strength_grade"] or "Not recorded")

        with c4:
            st.metric("Gait", assessment["gait_status"] or "Not recorded")

        st.caption(
            f'Assessment date: {assessment["assessment_date"]} · '
            f'Assessed by: {assessment["assessed_by"] or "Not specified"}'
        )
        if assessment["notes"]:
            st.write(assessment["notes"])
    else:
        st.info("No clinical assessment has been recorded yet.")

    if role_can_edit(st.session_state.role):
        st.divider()
        st.subheader("Record new assessment")

        with st.form("assessment_form"):
            assessment_date = st.date_input("Assessment date", value=date.today())
            c1, c2, c3 = st.columns(3)

            with c1:
                rom_value = st.number_input(
                    "Range of motion",
                    min_value=0.0,
                    max_value=360.0,
                    value=0.0,
                    step=0.5,
                    help="Enter the value actually measured by the clinician. Zero means no value will be stored."
                )
                rom_unit = st.selectbox("ROM unit", ["degrees"])
            with c2:
                pain_score = st.number_input(
                    "Pain score",
                    min_value=0.0,
                    max_value=10.0,
                    value=0.0,
                    step=0.5,
                    help="Enter a patient-reported or clinically documented value."
                )
                strength_grade = st.text_input("Strength grade", placeholder="e.g. 4/5")
            with c3:
                gait_status = st.selectbox(
                    "Gait status",
                    ["", "Independent", "Assisted", "Limited", "Non-ambulatory", "Not assessed"]
                )
                functional_score = st.number_input(
                    "Functional score",
                    min_value=0.0,
                    value=0.0,
                    step=0.5,
                    help="Enter only when a documented functional scale is being used."
                )

            assessment_notes = st.text_area("Assessment notes")
            assessed_by = st.text_input(
                "Assessed by",
                value=patient["assigned_rehabilitator"] or ""
            )

            save_assessment = st.form_submit_button("Save assessment", type="primary")

            if save_assessment:
                q("""
                    INSERT INTO assessments (
                        patient_id, assessment_date, rom_value, rom_unit,
                        pain_score, strength_grade, gait_status,
                        functional_score, notes, assessed_by
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    patient["patient_id"],
                    assessment_date.isoformat(),
                    rom_value if rom_value > 0 else None,
                    rom_unit if rom_value > 0 else None,
                    pain_score if pain_score > 0 else None,
                    strength_grade.strip() or None,
                    gait_status or None,
                    functional_score if functional_score > 0 else None,
                    assessment_notes.strip(),
                    assessed_by.strip(),
                ), commit=True)

                st.success("Assessment saved.")
                st.rerun()

# ============================================================
# REHABILITATION PLAN
# ============================================================

with tabs[3]:
    st.title("Rehabilitation Plan")
    st.caption("Plans are assigned by the clinical team; patients do not self-prescribe treatment.")

    plan = get_plan(patient["patient_id"])

    if plan:
        st.markdown(f"""
        <div class="section-card">
            <div class="small-muted">Current assigned phase</div>
            <h2>{esc(plan["phase"])} · {esc(plan["phase_name"])}</h2>
            <h3>{esc(plan["plan_title"])}</h3>
            <p>{esc(plan["instructions"])}</p>
            <p class="small-muted">
                Assigned by {esc(plan["assigned_by"])} · Status: {esc(plan["status"])}
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("No rehabilitation plan has been assigned yet.")

    if role_can_edit(st.session_state.role):
        st.divider()
        st.subheader("Assign rehabilitation plan")

        with st.form("plan_form"):
            c1, c2 = st.columns(2)
            with c1:
                phase = st.selectbox(
                    "Phase",
                    ["Phase 1", "Phase 2", "Phase 3", "Phase 4"]
                )
                phase_name_options = {
                    "Phase 1": "Initial Assessment",
                    "Phase 2": "Mobility and Strength",
                    "Phase 3": "Functional Training",
                    "Phase 4": "Return to Activity",
                }
                phase_name = st.text_input(
                    "Phase name",
                    value=phase_name_options[phase]
                )
                plan_title = st.text_input("Plan title")
            with c2:
                start_date = st.date_input("Start date", value=date.today())
                end_date = st.date_input("End date", value=date.today())
                assigned_by = st.text_input(
                    "Assigned by",
                    value=patient["assigned_rehabilitator"] or ""
                )

            instructions = st.text_area(
                "Clinical plan / instructions",
                height=140,
                placeholder="Enter the clinician-approved plan here."
            )

            save_plan = st.form_submit_button("Assign plan", type="primary")

            if save_plan:
                if not plan_title.strip() or not assigned_by.strip():
                    st.error("Plan title and assigned clinician are required.")
                else:
                    q("""
                        INSERT INTO rehabilitation_plans (
                            patient_id, phase, phase_name, plan_title,
                            instructions, start_date, end_date,
                            assigned_by, status
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        patient["patient_id"], phase, phase_name.strip(),
                        plan_title.strip(), instructions.strip(),
                        start_date.isoformat(), end_date.isoformat(),
                        assigned_by.strip(), "Assigned"
                    ), commit=True)
                    st.success("Rehabilitation plan assigned.")
                    st.rerun()

# ============================================================
# TELECONSULTATION
# ============================================================

with tabs[4]:
    st.title("Teleconsultation")
    st.caption("Meeting links are supplied by the authorized doctor, rehabilitator or meeting host.")

    meeting = get_meeting(patient["patient_id"])

    if meeting:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""
            <div class="section-card">
                <h3>Scheduled consultation</h3>
                <p><strong>Provider:</strong> {esc(meeting["provider_name"])}</p>
                <p><strong>Role:</strong> {esc(meeting["provider_role"])}</p>
                <p><strong>Platform:</strong> {esc(meeting["meeting_provider"])}</p>
                <p><strong>Date:</strong> {esc(meeting["scheduled_date"])}</p>
                <p><strong>Time:</strong> {esc(meeting["scheduled_time"])}</p>
                <p><strong>Time zone:</strong> {esc(meeting["timezone"])}</p>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            if meeting["meeting_url"] and is_valid_url(meeting["meeting_url"]):
                st.link_button("Join Teleconsultation", meeting["meeting_url"], type="primary")
            else:
                st.warning("No valid meeting URL has been supplied by the care team.")

            if meeting["meeting_id"]:
                st.write(f'**Meeting ID:** {meeting["meeting_id"]}')

            if meeting["notes"]:
                st.write(f'**Meeting notes:** {meeting["notes"]}')
    else:
        st.info("No teleconsultation has been scheduled.")

    if role_can_edit(st.session_state.role):
        st.divider()
        st.subheader("Schedule / update teleconsultation")

        with st.form("meeting_form"):
            c1, c2 = st.columns(2)
            with c1:
                provider_name = st.text_input(
                    "Doctor / rehabilitator / host",
                    value=patient["assigned_rehabilitator"] or ""
                )
                provider_role = st.selectbox(
                    "Provider role",
                    ["Rehabilitator", "Doctor", "Meeting Host"]
                )
                meeting_provider = st.text_input(
                    "Meeting provider",
                    placeholder="e.g. Zoom, Microsoft Teams, Google Meet"
                )
                meeting_url = st.text_input(
                    "Meeting URL",
                    placeholder="https://..."
                )
            with c2:
                scheduled_date = st.date_input("Scheduled date", value=date.today())
                scheduled_time = st.time_input("Scheduled time", value=dt_time(16, 30))
                timezone = st.text_input("Time zone", value="Asia/Karachi")
                meeting_id = st.text_input("Meeting ID / reference")

            meeting_notes = st.text_area("Host / clinical notes")

            save_meeting = st.form_submit_button(
                "Save teleconsultation",
                type="primary"
            )

            if save_meeting:
                if not provider_name.strip():
                    st.error("Provider / host name is required.")
                elif not meeting_url.strip() or not is_valid_url(meeting_url.strip()):
                    st.error("Enter a valid HTTPS/HTTP meeting URL.")
                else:
                    q("""
                        INSERT INTO meetings (
                            patient_id, provider_name, provider_role,
                            meeting_provider, meeting_url, meeting_id,
                            scheduled_date, scheduled_time, timezone, notes
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        patient["patient_id"],
                        provider_name.strip(),
                        provider_role,
                        meeting_provider.strip(),
                        meeting_url.strip(),
                        meeting_id.strip(),
                        scheduled_date.isoformat(),
                        scheduled_time.strftime("%H:%M"),
                        timezone.strip(),
                        meeting_notes.strip(),
                    ), commit=True)
                    st.success("Teleconsultation saved.")
                    st.rerun()

# ============================================================
# MEDICAL RECORDS
# ============================================================

with tabs[5]:
    st.title("Medical Records")
    st.caption("Attach or reference MRI, X-ray, CT, reports and other clinical documentation.")

    records = get_records(patient["patient_id"])

    if records:
        for record in records:
            with st.container(border=True):
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.write(f"**{record['title']}**")
                    st.caption(
                        f"{record['record_type']} · Added {record['created_at']} · "
                        f"By {record['uploaded_by'] or 'Care team'}"
                    )
                    if record["notes"]:
                        st.write(record["notes"])
                with c2:
                    if record["url"] and is_valid_url(record["url"]):
                        st.link_button("Open record", record["url"])
                    else:
                        st.caption("No external link")
    else:
        st.info("No medical records have been added.")

    if role_can_edit(st.session_state.role):
        st.divider()
        st.subheader("Add medical record reference")

        with st.form("record_form"):
            c1, c2 = st.columns(2)
            with c1:
                record_type = st.selectbox(
                    "Record type",
                    [
                        "MRI",
                        "X-ray",
                        "CT",
                        "Ultrasound",
                        "Laboratory report",
                        "Discharge summary",
                        "Referral",
                        "Other",
                    ]
                )
                title = st.text_input("Record title")
            with c2:
                url = st.text_input(
                    "Secure record URL",
                    placeholder="Paste the authorized document link"
                )
                uploaded_by = st.text_input(
                    "Added by",
                    value=patient["assigned_rehabilitator"] or ""
                )

            notes = st.text_area("Record notes")

            save_record = st.form_submit_button(
                "Add record",
                type="primary"
            )

            if save_record:
                if not title.strip():
                    st.error("Record title is required.")
                elif url.strip() and not is_valid_url(url.strip()):
                    st.error("The record URL is not valid.")
                else:
                    q("""
                        INSERT INTO records (
                            patient_id, record_type, title, url,
                            notes, uploaded_by, created_at
                        ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        patient["patient_id"],
                        record_type,
                        title.strip(),
                        url.strip(),
                        notes.strip(),
                        uploaded_by.strip(),
                        datetime.now().isoformat(timespec="seconds"),
                    ), commit=True)
                    st.success("Medical record reference added.")
                    st.rerun()

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")
st.caption(
    "TeleRehabilitation Portal · Clinical workflow interface · "
    "Production deployment requires authenticated identity, encrypted storage, "
    "audit logging, access controls and applicable healthcare/privacy compliance."
)
