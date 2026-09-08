import streamlit as st
import sqlite3
import json
from datetime import datetime, date
from pathlib import Path

# ============================================================
# TELE REHABILITATION PORTAL
# Professional Clinical Tele-Rehabilitation Management System
# ============================================================

st.set_page_config(
    page_title="TeleRehabilitation Portal",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

DB_FILE = "tele_rehabilitation.db"


# ============================================================
# DATABASE
# ============================================================

def get_connection():
    return sqlite3.connect(DB_FILE, check_same_thread=False)


def database_initialized():
    conn = get_connection()
    cur = conn.cursor()

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

            medical_history TEXT,
            medications TEXT,
            allergies TEXT,
            previous_surgery TEXT,
            previous_rehabilitation TEXT,

            functional_limitations TEXT,
            pain_score TEXT,
            pain_location TEXT,

            rom_available INTEGER DEFAULT 0,
            rom_value TEXT,
            rom_joint TEXT,
            rom_measurement_date TEXT,
            rom_source TEXT,

            mr_link TEXT,
            clinical_documents TEXT,

            meeting_platform TEXT,
            meeting_link TEXT,
            meeting_notes TEXT,

            assigned_rehabilitator TEXT,
            care_plan_status TEXT,

            created_at TEXT,
            updated_at TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT,
            professional_name TEXT,
            professional_role TEXT,
            specialty TEXT,
            appointment_date TEXT,
            appointment_time TEXT,
            platform TEXT,
            meeting_link TEXT,
            notes TEXT,
            status TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


database_initialized()


# ============================================================
# DATABASE HELPERS
# ============================================================

def get_patient(patient_id):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM patients WHERE patient_id = ?",
        (patient_id,)
    )

    row = cur.fetchone()
    conn.close()

    return dict(row) if row else None


def get_all_patients():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM patients ORDER BY updated_at DESC"
    )

    rows = cur.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def save_patient(data):
    conn = get_connection()
    cur = conn.cursor()

    now = datetime.now().isoformat(timespec="seconds")

    existing = get_patient(data["patient_id"])

    if existing:
        cur.execute("""
            UPDATE patients SET
                full_name = ?,
                date_of_birth = ?,
                sex = ?,
                phone = ?,
                email = ?,
                country = ?,
                city = ?,
                preferred_language = ?,
                emergency_contact = ?,
                emergency_phone = ?,

                diagnosis = ?,
                diagnosis_date = ?,
                affected_organ = ?,
                affected_side = ?,
                diagnosis_notes = ?,

                medical_history = ?,
                medications = ?,
                allergies = ?,
                previous_surgery = ?,
                previous_rehabilitation = ?,

                functional_limitations = ?,
                pain_score = ?,
                pain_location = ?,

                rom_available = ?,
                rom_value = ?,
                rom_joint = ?,
                rom_measurement_date = ?,
                rom_source = ?,

                mr_link = ?,
                clinical_documents = ?,

                meeting_platform = ?,
                meeting_link = ?,
                meeting_notes = ?,

                assigned_rehabilitator = ?,
                care_plan_status = ?,
                updated_at = ?

            WHERE patient_id = ?
        """, (
            data["full_name"],
            data["date_of_birth"],
            data["sex"],
            data["phone"],
            data["email"],
            data["country"],
            data["city"],
            data["preferred_language"],
            data["emergency_contact"],
            data["emergency_phone"],

            data["diagnosis"],
            data["diagnosis_date"],
            data["affected_organ"],
            data["affected_side"],
            data["diagnosis_notes"],

            data["medical_history"],
            data["medications"],
            data["allergies"],
            data["previous_surgery"],
            data["previous_rehabilitation"],

            data["functional_limitations"],
            data["pain_score"],
            data["pain_location"],

            data["rom_available"],
            data["rom_value"],
            data["rom_joint"],
            data["rom_measurement_date"],
            data["rom_source"],

            data["mr_link"],
            data["clinical_documents"],

            data["meeting_platform"],
            data["meeting_link"],
            data["meeting_notes"],

            data["assigned_rehabilitator"],
            data["care_plan_status"],
            now,

            data["patient_id"],
        ))

    else:
        cur.execute("""
            INSERT INTO patients (
                patient_id,
                full_name,
                date_of_birth,
                sex,
                phone,
                email,
                country,
                city,
                preferred_language,
                emergency_contact,
                emergency_phone,

                diagnosis,
                diagnosis_date,
                affected_organ,
                affected_side,
                diagnosis_notes,

                medical_history,
                medications,
                allergies,
                previous_surgery,
                previous_rehabilitation,

                functional_limitations,
                pain_score,
                pain_location,

                rom_available,
                rom_value,
                rom_joint,
                rom_measurement_date,
                rom_source,

                mr_link,
                clinical_documents,

                meeting_platform,
                meeting_link,
                meeting_notes,

                assigned_rehabilitator,
                care_plan_status,

                created_at,
                updated_at
            )
            VALUES (
                ?,?,?,?,?,?,?,?,?,?,
                ?,?,?,?,?,?,?,?,?,?,
                ?,?,
                ?,?,?,?,?,?,
                ?,?,
                ?,?,
                ?,?,
                ?,?,
                ?,?
            )
        """, (
            data["patient_id"],
            data["full_name"],
            data["date_of_birth"],
            data["sex"],
            data["phone"],
            data["email"],
            data["country"],
            data["city"],
            data["preferred_language"],
            data["emergency_contact"],
            data["emergency_phone"],

            data["diagnosis"],
            data["diagnosis_date"],
            data["affected_organ"],
            data["affected_side"],
            data["diagnosis_notes"],

            data["medical_history"],
            data["medications"],
            data["allergies"],
            data["previous_surgery"],
            data["previous_rehabilitation"],

            data["functional_limitations"],
            data["pain_score"],
            data["pain_location"],

            data["rom_available"],
            data["rom_value"],
            data["rom_joint"],
            data["rom_measurement_date"],
            data["rom_source"],

            data["mr_link"],
            data["clinical_documents"],

            data["meeting_platform"],
            data["meeting_link"],
            data["meeting_notes"],

            data["assigned_rehabilitator"],
            data["care_plan_status"],

            now,
            now,
        ))

    conn.commit()
    conn.close()


def save_appointment(
    patient_id,
    professional_name,
    professional_role,
    specialty,
    appointment_date,
    appointment_time,
    platform,
    meeting_link,
    notes,
):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO appointments (
            patient_id,
            professional_name,
            professional_role,
            specialty,
            appointment_date,
            appointment_time,
            platform,
            meeting_link,
            notes,
            status,
            created_at
        )
        VALUES (?,?,?,?,?,?,?,?,?,?,?)
    """, (
        patient_id,
        professional_name,
        professional_role,
        specialty,
        appointment_date,
        appointment_time,
        platform,
        meeting_link,
        notes,
        "Scheduled",
        datetime.now().isoformat(timespec="seconds"),
    ))

    conn.commit()
    conn.close()


def get_appointments(patient_id):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM appointments
        WHERE patient_id = ?
        ORDER BY appointment_date ASC, appointment_time ASC
    """, (patient_id,))

    rows = cur.fetchall()
    conn.close()

    return [dict(row) for row in rows]


# ============================================================
# PROFESSIONAL UI
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: "Inter", sans-serif;
}

.stApp {
    background: #f5f7fa;
    color: #162033;
}

.block-container {
    max-width: 1500px;
    padding-top: 1.2rem;
    padding-bottom: 4rem;
}

/* ---------------------------------------------------------
   SIDEBAR
--------------------------------------------------------- */

section[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid #dfe5ec;
}

section[data-testid="stSidebar"] > div {
    padding-top: 1.5rem;
}

.sidebar-brand {
    font-size: 23px;
    font-weight: 800;
    color: #14213d;
    margin-bottom: 4px;
}

.sidebar-subtitle {
    color: #697586;
    font-size: 13px;
    line-height: 1.5;
    margin-bottom: 28px;
}

/* ---------------------------------------------------------
   HEADER
--------------------------------------------------------- */

.portal-header {
    background: #ffffff;
    border: 1px solid #dfe5ec;
    border-radius: 18px;
    padding: 28px 32px;
    margin-bottom: 22px;
    box-shadow: 0 5px 18px rgba(30, 50, 80, 0.05);
}

.portal-title {
    font-size: 34px;
    font-weight: 800;
    color: #12213a;
    margin: 0;
}

.portal-subtitle {
    color: #687588;
    font-size: 15px;
    margin-top: 7px;
}

/* ---------------------------------------------------------
   CARDS
--------------------------------------------------------- */

.clinical-card {
    background: #ffffff;
    border: 1px solid #dfe5ec;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 18px;
    box-shadow: 0 4px 15px rgba(30, 50, 80, 0.04);
}

.card-title {
    font-size: 20px;
    font-weight: 750;
    color: #14213d;
    margin-bottom: 7px;
}

.card-description {
    color: #697586;
    font-size: 14px;
    margin-bottom: 20px;
}

/* ---------------------------------------------------------
   PATIENT SUMMARY
--------------------------------------------------------- */

.patient-name {
    font-size: 28px;
    font-weight: 800;
    color: #10213b;
}

.patient-id {
    font-size: 14px;
    color: #6b7788;
    margin-top: 4px;
}

.info-label {
    color: #718096;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: .04em;
}

.info-value {
    color: #17243b;
    font-size: 15px;
    font-weight: 600;
    margin-top: 3px;
}

/* ---------------------------------------------------------
   STATUS
--------------------------------------------------------- */

.status-complete {
    background: #e9f7ef;
    color: #18794e;
    border: 1px solid #b9e4cc;
    padding: 8px 13px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 700;
    display: inline-block;
}

.status-pending {
    background: #fff6df;
    color: #8a6200;
    border: 1px solid #eed58d;
    padding: 8px 13px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 700;
    display: inline-block;
}

.status-neutral {
    background: #eef2f6;
    color: #556273;
    border: 1px solid #d9e0e7;
    padding: 8px 13px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 700;
    display: inline-block;
}

/* ---------------------------------------------------------
   PHASES
--------------------------------------------------------- */

.phase-card {
    background: #ffffff;
    border: 1px solid #dfe5ec;
    border-radius: 14px;
    padding: 20px;
    min-height: 135px;
}

.phase-number {
    color: #526173;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .06em;
}

.phase-title {
    color: #14213d;
    font-size: 18px;
    font-weight: 750;
    margin-top: 9px;
}

.phase-state {
    color: #687588;
    font-size: 13px;
    margin-top: 8px;
}

/* ---------------------------------------------------------
   MEETING
--------------------------------------------------------- */

.meeting-card {
    background: #f8fbff;
    border: 1px solid #cfddeb;
    border-radius: 15px;
    padding: 22px;
}

.meeting-title {
    font-size: 19px;
    font-weight: 750;
    color: #14213d;
}

.meeting-meta {
    color: #66758a;
    font-size: 14px;
    margin-top: 7px;
}

/* ---------------------------------------------------------
   REMOVE STREAMLIT CODE-LIKE LOOK
--------------------------------------------------------- */

pre {
    display: none !important;
}

code {
    font-family: inherit !important;
}

[data-testid="stMarkdownContainer"] pre {
    display: none !important;
}

/* ---------------------------------------------------------
   BUTTONS
--------------------------------------------------------- */

.stButton > button {
    border-radius: 9px;
    min-height: 42px;
    font-weight: 650;
    border: 1px solid #cfd7e2;
}

.stButton > button:hover {
    border-color: #8391a5;
}

/* ---------------------------------------------------------
   INPUTS
--------------------------------------------------------- */

div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div,
textarea {
    border-radius: 8px !important;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "portal_role" not in st.session_state:
    st.session_state.portal_role = "Patient"

if "patient_id" not in st.session_state:
    st.session_state.patient_id = "TRP-1001"


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-brand">TeleRehabilitation</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-subtitle">'
        'Clinical care coordination and secure tele-rehabilitation management'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    role = st.selectbox(
        "Portal role",
        [
            "Patient",
            "Rehabilitator",
            "Doctor",
            "Meeting Host",
            "Clinical Administrator",
        ],
        index=[
            "Patient",
            "Rehabilitator",
            "Doctor",
            "Meeting Host",
            "Clinical Administrator",
        ].index(st.session_state.portal_role),
    )

    st.session_state.portal_role = role

    patients = get_all_patients()

    if not patients:
        st.session_state.patient_id = "TRP-1001"

    patient_ids = [p["patient_id"] for p in patients]

    if not patient_ids:
        patient_ids = ["TRP-1001"]

    selected_patient = st.selectbox(
        "Patient record",
        patient_ids,
        index=(
            patient_ids.index(st.session_state.patient_id)
            if st.session_state.patient_id in patient_ids
            else 0
        )
    )

    st.session_state.patient_id = selected_patient

    st.divider()

    st.caption(
        "Production deployment should connect portal roles "
        "to authenticated identity and server-side authorization."
    )


# ============================================================
# CURRENT PATIENT
# ============================================================

patient = get_patient(st.session_state.patient_id)


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="portal-header">

    <div class="portal-title">
        TeleRehabilitation Portal
    </div>

    <div class="portal-subtitle">
        Secure clinical coordination, patient records, rehabilitation
        management and teleconsultation access
    </div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# FIRST-TIME PATIENT RECORD
# ============================================================

if patient is None:

    st.markdown("""
    <div class="clinical-card">
        <div class="card-title">Patient record not yet completed</div>
        <div class="card-description">
            Clinical information must be entered before rehabilitation
            measurements or treatment decisions can be displayed.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.warning(
        "No patient record exists for this patient ID. "
        "Complete the patient profile below."
    )

    with st.form("new_patient_form"):

        st.subheader("Patient profile")

        c1, c2 = st.columns(2)

        with c1:
            full_name = st.text_input("Full name")
            dob = st.date_input(
                "Date of birth",
                value=date(2000, 1, 1),
                min_value=date(1900, 1, 1),
                max_value=date.today(),
            )
            sex = st.selectbox(
                "Sex",
                ["Not specified", "Female", "Male", "Other"]
            )
            phone = st.text_input("Phone")
            email = st.text_input("Email")

        with c2:
            country = st.text_input("Country")
            city = st.text_input("City")
            language = st.selectbox(
                "Preferred language",
                [
                    "English",
                    "Urdu",
                    "Arabic",
                    "Spanish",
                    "French",
                    "German",
                    "Other",
                ],
            )
            emergency_contact = st.text_input("Emergency contact")
            emergency_phone = st.text_input("Emergency contact phone")

        st.subheader("Clinical diagnosis")

        diagnosis = st.text_area(
            "Diagnosis / clinical condition",
            placeholder="Enter the documented diagnosis..."
        )

        diagnosis_date = st.date_input(
            "Diagnosis date",
            value=date.today()
        )

        affected_organ = st.text_input(
            "Affected organ / body region",
            placeholder="Example: Left knee, shoulder, lumbar spine..."
        )

        affected_side = st.selectbox(
            "Affected side",
            [
                "Not specified",
                "Left",
                "Right",
                "Bilateral",
                "Midline",
                "Multiple regions",
            ]
        )

        diagnosis_notes = st.text_area(
            "Clinical diagnosis notes"
        )

        st.subheader("Clinical history")

        medical_history = st.text_area("Relevant medical history")
        medications = st.text_area("Current medications")
        allergies = st.text_area("Allergies")
        previous_surgery = st.text_area("Previous surgery / procedures")
        previous_rehabilitation = st.text_area(
            "Previous rehabilitation history"
        )

        functional_limitations = st.text_area(
            "Functional limitations"
        )

        pain_score = st.selectbox(
            "Pain score",
            ["Not assessed", "0", "1", "2", "3", "4", "5",
             "6", "7", "8", "9", "10"]
        )

        pain_location = st.text_input("Pain location")

        st.subheader("Existing clinical measurements")

        rom_available = st.checkbox(
            "A verified range-of-motion measurement is available"
        )

        rom_value = ""
        rom_joint = ""
        rom_date = ""
        rom_source = ""

        if rom_available:

            rom_value = st.text_input(
                "Range of motion",
                placeholder="Example: 112°"
            )

            rom_joint = st.text_input(
                "Joint / movement measured"
            )

            rom_date = st.date_input(
                "Measurement date",
                value=date.today()
            ).isoformat()

            rom_source = st.text_input(
                "Measurement source",
                placeholder="Example: Clinical assessment by Dr. Ahmed Khan"
            )

        st.subheader("Medical records and secure meeting")

        mr_link = st.text_input(
            "Medical record / document link",
            placeholder="Paste secure clinical record link"
        )

        clinical_documents = st.text_area(
            "Clinical document references"
        )

        meeting_platform = st.selectbox(
            "Teleconsultation platform",
            [
                "Not scheduled",
                "Zoom",
                "Microsoft Teams",
                "Google Meet",
                "Other secure platform",
            ]
        )

        meeting_link = st.text_input(
            "Meeting link",
            placeholder="Meeting host / doctor / rehabilitator pastes the secure meeting URL here"
        )

        meeting_notes = st.text_area(
            "Meeting instructions"
        )

        assigned_rehabilitator = st.text_input(
            "Assigned rehabilitator"
        )

        care_plan_status = "Profile completed"

        submitted = st.form_submit_button(
            "Save patient record",
            use_container_width=True
        )

        if submitted:

            if not full_name.strip():
                st.error("Full name is required.")

            elif not diagnosis.strip():
                st.error(
                    "Diagnosis is required before the clinical record "
                    "can be considered complete."
                )

            elif not affected_organ.strip():
                st.error(
                    "Affected organ / body region is required. "
                    "The system will not invent range-of-motion data."
                )

            else:

                save_patient({
                    "patient_id": st.session_state.patient_id,
                    "full_name": full_name,
                    "date_of_birth": dob.isoformat(),
                    "sex": sex,
                    "phone": phone,
                    "email": email,
                    "country": country,
                    "city": city,
                    "preferred_language": language,
                    "emergency_contact": emergency_contact,
                    "emergency_phone": emergency_phone,

                    "diagnosis": diagnosis,
                    "diagnosis_date": diagnosis_date.isoformat(),
                    "affected_organ": affected_organ,
                    "affected_side": affected_side,
                    "diagnosis_notes": diagnosis_notes,

                    "medical_history": medical_history,
                    "medications": medications,
                    "allergies": allergies,
                    "previous_surgery": previous_surgery,
                    "previous_rehabilitation": previous_rehabilitation,

                    "functional_limitations": functional_limitations,
                    "pain_score": pain_score,
                    "pain_location": pain_location,

                    "rom_available": int(rom_available),
                    "rom_value": rom_value,
                    "rom_joint": rom_joint,
                    "rom_measurement_date": rom_date,
                    "rom_source": rom_source,

                    "mr_link": mr_link,
                    "clinical_documents": clinical_documents,

                    "meeting_platform": meeting_platform,
                    "meeting_link": meeting_link,
                    "meeting_notes": meeting_notes,

                    "assigned_rehabilitator": assigned_rehabilitator,
                    "care_plan_status": care_plan_status,
                })

                st.success("Patient record saved successfully.")
                st.rerun()

    st.stop()


# ============================================================
# PATIENT SUMMARY
# ============================================================

profile_fields = [
    patient.get("full_name"),
    patient.get("date_of_birth"),
    patient.get("country"),
    patient.get("preferred_language"),
    patient.get("diagnosis"),
    patient.get("affected_organ"),
]

profile_complete = all(
    x is not None and str(x).strip() != ""
    for x in profile_fields
)


if profile_complete:
    profile_status = (
        '<span class="status-complete">Profile complete</span>'
    )
else:
    profile_status = (
        '<span class="status-pending">Profile incomplete</span>'
    )


st.markdown(f"""
<div class="clinical-card">

    <div style="display:flex; justify-content:space-between; gap:20px;">

        <div>
            <div class="patient-name">
                {patient.get("full_name", "Patient")}
            </div>

            <div class="patient-id">
                Patient ID: {patient.get("patient_id")}
            </div>
        </div>

        <div>
            {profile_status}
        </div>

    </div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# ROLE-SPECIFIC NAVIGATION
# ============================================================

if role == "Patient":

    pages = [
        "Overview",
        "My Clinical Record",
        "Teleconsultation",
        "Care Plan",
    ]

elif role == "Rehabilitator":

    pages = [
        "Clinical Dashboard",
        "Patient Assessment",
        "Care Plan",
        "Teleconsultation",
    ]

elif role == "Doctor":

    pages = [
        "Clinical Dashboard",
        "Patient Record",
        "Teleconsultation",
        "Care Plan",
    ]

elif role == "Meeting Host":

    pages = [
        "Meeting Dashboard",
        "Patient Record",
        "Teleconsultation",
    ]

else:

    pages = [
        "Clinical Dashboard",
        "Patient Record",
        "Teleconsultation",
        "Care Plan",
    ]


page = st.radio(
    "Portal section",
    pages,
    horizontal=True,
    label_visibility="collapsed"
)


# ============================================================
# OVERVIEW / CLINICAL DASHBOARD
# ============================================================

if page in ["Overview", "Clinical Dashboard"]:

    st.markdown("""
    <div class="clinical-card">

        <div class="card-title">
            Clinical Overview
        </div>

        <div class="card-description">
            The dashboard presents documented clinical information only.
            It does not generate measurements or diagnoses that have not
            been recorded by an authorized clinician.
        </div>

    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Patient",
            patient.get("full_name") or "Not recorded"
        )

    with c2:
        st.metric(
            "Diagnosis",
            "Documented" if patient.get("diagnosis") else "Pending"
        )

    with c3:
        st.metric(
            "Affected region",
            patient.get("affected_organ") or "Not documented"
        )

    with c4:
        st.metric(
            "Language",
            patient.get("preferred_language") or "Not specified"
        )

    st.markdown("---")

    c1, c2 = st.columns(2)

    with c1:

        st.markdown("""
        <div class="clinical-card">

            <div class="card-title">
                Diagnosis
            </div>

        """, unsafe_allow_html=True)

        st.write(
            patient.get("diagnosis")
            or "No diagnosis has been documented."
        )

        if patient.get("diagnosis_date"):
            st.caption(
                f"Diagnosis date: {patient['diagnosis_date']}"
            )

        st.markdown("</div>", unsafe_allow_html=True)

    with c2:

        st.markdown("""
        <div class="clinical-card">

            <div class="card-title">
                Affected body region
            </div>

        """, unsafe_allow_html=True)

        if patient.get("affected_organ"):
            st.write(
                patient.get("affected_organ")
            )

            st.caption(
                f"Side: {patient.get('affected_side') or 'Not specified'}"
            )

        else:
            st.warning(
                "Affected body region has not been documented."
            )

        st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# PATIENT RECORD
# ============================================================

if page in ["My Clinical Record", "Patient Record", "Patient Assessment"]:

    st.markdown("""
    <div class="clinical-card">

        <div class="card-title">
            Complete Clinical Patient Record
        </div>

        <div class="card-description">
            This section contains the patient information documented by
            the clinical team. Sensitive clinical information should be
            protected by authenticated access in production.
        </div>

    </div>
    """, unsafe_allow_html=True)

    tabs = st.tabs([
        "Demographics",
        "Diagnosis",
        "Medical history",
        "Functional status",
        "Measurements",
        "Documents",
    ])

    # --------------------------------------------------------
    # DEMOGRAPHICS
    # --------------------------------------------------------

    with tabs[0]:

        c1, c2 = st.columns(2)

        with c1:
            st.write("**Full name**")
            st.write(patient.get("full_name") or "Not documented")

            st.write("**Date of birth**")
            st.write(patient.get("date_of_birth") or "Not documented")

            st.write("**Sex**")
            st.write(patient.get("sex") or "Not documented")

            st.write("**Phone**")
            st.write(patient.get("phone") or "Not documented")

            st.write("**Email**")
            st.write(patient.get("email") or "Not documented")

        with c2:
            st.write("**Country**")
            st.write(patient.get("country") or "Not documented")

            st.write("**City**")
            st.write(patient.get("city") or "Not documented")

            st.write("**Preferred language**")
            st.write(
                patient.get("preferred_language")
                or "Not documented"
            )

            st.write("**Emergency contact**")
            st.write(
                patient.get("emergency_contact")
                or "Not documented"
            )

            st.write("**Emergency phone**")
            st.write(
                patient.get("emergency_phone")
                or "Not documented"
            )

    # --------------------------------------------------------
    # DIAGNOSIS
    # --------------------------------------------------------

    with tabs[1]:

        if not patient.get("diagnosis"):
            st.error(
                "Diagnosis has not been documented."
            )
        else:

            st.markdown(
                f"""
                <div class="clinical-card">

                    <div class="card-title">
                        Documented diagnosis
                    </div>

                    <div style="font-size:16px; color:#17243b;">
                        {patient.get("diagnosis")}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        c1, c2 = st.columns(2)

        with c1:
            st.write("**Affected organ / body region**")
            st.write(
                patient.get("affected_organ")
                or "Not documented"
            )

        with c2:
            st.write("**Affected side**")
            st.write(
                patient.get("affected_side")
                or "Not documented"
            )

        st.write("**Clinical notes**")
        st.write(
            patient.get("diagnosis_notes")
            or "No clinical diagnosis notes recorded."
        )

    # --------------------------------------------------------
    # HISTORY
    # --------------------------------------------------------

    with tabs[2]:

        history_items = {
            "Medical history": patient.get("medical_history"),
            "Medications": patient.get("medications"),
            "Allergies": patient.get("allergies"),
            "Previous surgery": patient.get("previous_surgery"),
            "Previous rehabilitation": patient.get(
                "previous_rehabilitation"
            ),
        }

        for title, value in history_items.items():

            st.markdown(
                f"### {title}"
            )

            st.write(
                value
                if value and str(value).strip()
                else "Not documented."
            )

    # --------------------------------------------------------
    # FUNCTIONAL STATUS
    # --------------------------------------------------------

    with tabs[3]:

        st.write("### Functional limitations")

        st.write(
            patient.get("functional_limitations")
            or "Functional limitations have not been documented."
        )

        c1, c2 = st.columns(2)

        with c1:
            st.write("**Pain score**")
            st.write(
                patient.get("pain_score")
                or "Not assessed"
            )

        with c2:
            st.write("**Pain location**")
            st.write(
                patient.get("pain_location")
                or "Not documented"
            )

    # --------------------------------------------------------
    # MEASUREMENTS
    # --------------------------------------------------------

    with tabs[4]:

        st.write("### Range of motion")

        if patient.get("rom_available") and patient.get("rom_value"):

            st.success(
                "Verified/documented measurement available."
            )

            c1, c2, c3 = st.columns(3)

            with c1:
                st.metric(
                    "Recorded ROM",
                    patient.get("rom_value")
                )

            with c2:
                st.write("**Joint / movement**")
                st.write(
                    patient.get("rom_joint")
                    or "Not documented"
                )

            with c3:
                st.write("**Measurement date**")
                st.write(
                    patient.get("rom_measurement_date")
                    or "Not documented"
                )

            st.caption(
                "Measurement source: "
                + (
                    patient.get("rom_source")
                    or "Not documented"
                )
            )

        else:

            st.warning(
                "Range of motion has not been documented. "
                "The portal does NOT invent a ROM value from an incomplete diagnosis."
            )

            st.info(
                "A clinician must perform or enter the appropriate "
                "measurement before ROM can be displayed."
            )

    # --------------------------------------------------------
    # DOCUMENTS
    # --------------------------------------------------------

    with tabs[5]:

        st.write("### Medical record")

        if patient.get("mr_link"):

            st.link_button(
                "Open secure medical record",
                patient.get("mr_link")
            )

        else:

            st.info(
                "No medical-record link has been added yet."
            )

        st.write("### Clinical document references")

        st.write(
            patient.get("clinical_documents")
            or "No document references have been added."
        )


# ============================================================
# TELECONSULTATION
# ============================================================

if page in ["Teleconsultation"]:

    st.markdown("""
    <div class="clinical-card">

        <div class="card-title">
            Teleconsultation
        </div>

        <div class="card-description">
            The patient joins the scheduled clinical consultation from
            the portal. The meeting link is entered by the authorized
            doctor, rehabilitator or meeting host.
        </div>

    </div>
    """, unsafe_allow_html=True)

    platform = patient.get("meeting_platform")
    meeting_link = patient.get("meeting_link")

    if meeting_link:

        st.markdown(f"""
        <div class="meeting-card">

            <div class="meeting-title">
                Scheduled teleconsultation
            </div>

            <div class="meeting-meta">
                Platform: {platform or "Secure teleconsultation platform"}
            </div>

            <div class="meeting-meta">
                Patient: {patient.get("full_name")}
            </div>

        </div>
        """, unsafe_allow_html=True)

        st.link_button(
            "Join teleconsultation",
            meeting_link,
            use_container_width=False
        )

        if patient.get("meeting_notes"):
            st.info(
                patient.get("meeting_notes")
            )

    else:

        st.warning(
            "No meeting link has been added yet."
        )

        st.info(
            "The doctor, rehabilitator or meeting host must add "
            "the secure meeting link before the patient can join."
        )

    appointments = get_appointments(
        st.session_state.patient_id
    )

    if appointments:

        st.markdown("### Scheduled sessions")

        for appointment in appointments:

            st.markdown(
                f"""
                <div class="clinical-card">

                    <div class="card-title">
                        {appointment.get("specialty") or "Teleconsultation"}
                    </div>

                    <div>
                        Professional:
                        <strong>
                            {appointment.get("professional_name") or "Not specified"}
                        </strong>
                    </div>

                    <div>
                        Date:
                        <strong>
                            {appointment.get("appointment_date") or "Not specified"}
                        </strong>
                    </div>

                    <div>
                        Time:
                        <strong>
                            {appointment.get("appointment_time") or "Not specified"}
                        </strong>
                    </div>

                    <div>
                        Platform:
                        <strong>
                            {appointment.get("platform") or "Not specified"}
                        </strong>
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# MEETING HOST DASHBOARD
# ============================================================

if page == "Meeting Dashboard":

    st.markdown("""
    <div class="clinical-card">

        <div class="card-title">
            Meeting Host Dashboard
        </div>

        <div class="card-description">
            Meeting hosts can attach the secure meeting information
            to the correct patient record.
        </div>

    </div>
    """, unsafe_allow_html=True)

    with st.form("meeting_form"):

        meeting_platform = st.selectbox(
            "Meeting platform",
            [
                "Zoom",
                "Microsoft Teams",
                "Google Meet",
                "Other secure platform",
            ]
        )

        meeting_link = st.text_input(
            "Meeting URL",
            value=patient.get("meeting_link") or ""
        )

        meeting_notes = st.text_area(
            "Instructions for patient",
            value=patient.get("meeting_notes") or ""
        )

        if st.form_submit_button(
            "Save meeting details"
        ):

            save_patient({
                **patient,
                "meeting_platform": meeting_platform,
                "meeting_link": meeting_link,
                "meeting_notes": meeting_notes,
            })

            st.success(
                "Meeting information saved to the patient record."
            )

            st.rerun()


# ============================================================
# CARE PLAN
# ============================================================

if page == "Care Plan":

    st.markdown("""
    <div class="clinical-card">

        <div class="card-title">
            Rehabilitation Care Pathway
        </div>

        <div class="card-description">
            The rehabilitation pathway is presented as a clinical
            progression rather than as a generic exercise checklist.
            Specific interventions are determined by the treating
            professional.
        </div>

    </div>
    """, unsafe_allow_html=True)

    phases = [
        (
            "Phase 1",
            "Assessment & Clinical Preparation",
            "Current" if profile_complete else "Requires patient information"
        ),
        (
            "Phase 2",
            "Mobility & Strength",
            "Upcoming"
        ),
        (
            "Phase 3",
            "Functional Rehabilitation",
            "Upcoming"
        ),
        (
            "Phase 4",
            "Return to Activity",
            "Upcoming"
        ),
    ]

    cols = st.columns(4)

    for col, phase in zip(cols, phases):

        with col:

            st.markdown(
                f"""
                <div class="phase-card">

                    <div class="phase-number">
                        {phase[0]}
                    </div>

                    <div class="phase-title">
                        {phase[1]}
                    </div>

                    <div class="phase-state">
                        {phase[2]}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("---")

    st.info(
        "No exercise is automatically prescribed by this demo portal. "
        "The treating rehabilitation professional is responsible for "
        "the clinical program."
    )


# ============================================================
# CLINICAL DASHBOARD ADMINISTRATION
# ============================================================

if page == "Clinical Dashboard":

    st.markdown("""
    <div class="clinical-card">

        <div class="card-title">
            Clinical Dashboard
        </div>

        <div class="card-description">
            Review patient records, completeness and teleconsultation
            readiness.
        </div>

    </div>
    """, unsafe_allow_html=True)

    patients = get_all_patients()

    if not patients:

        st.info("No patient records available.")

    else:

        for p in patients:

            complete = all([
                p.get("full_name"),
                p.get("diagnosis"),
                p.get("affected_organ"),
                p.get("preferred_language"),
            ])

            status = (
                '<span class="status-complete">Ready</span>'
                if complete
                else
                '<span class="status-pending">Incomplete</span>'
            )

            meeting_status = (
                "Meeting link available"
                if p.get("meeting_link")
                else "Meeting link not added"
            )

            st.markdown(
                f"""
                <div class="clinical-card">

                    <div style="display:flex;
                                justify-content:space-between;
                                gap:20px;">

                        <div>

                            <div class="card-title">
                                {p.get("full_name") or "Unnamed patient"}
                            </div>

                            <div style="color:#697586;">
                                Patient ID: {p.get("patient_id")}
                            </div>

                            <div style="margin-top:12px;">
                                Diagnosis:
                                <strong>
                                    {p.get("diagnosis") or "Not documented"}
                                </strong>
                            </div>

                            <div>
                                Affected region:
                                <strong>
                                    {p.get("affected_organ") or "Not documented"}
                                </strong>
                            </div>

                            <div>
                                Language:
                                <strong>
                                    {p.get("preferred_language") or "Not documented"}
                                </strong>
                            </div>

                            <div style="margin-top:8px;color:#687588;">
                                {meeting_status}
                            </div>

                        </div>

                        <div>
                            {status}
                        </div>

                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# PROFESSIONAL APPOINTMENT CREATION
# ============================================================

if role in [
    "Doctor",
    "Rehabilitator",
    "Clinical Administrator"
] and page == "Teleconsultation":

    st.markdown("""
    <div class="clinical-card">

        <div class="card-title">
            Schedule clinical session
        </div>

        <div class="card-description">
            Create the scheduled consultation and attach the meeting
            information to the patient workflow.
        </div>

    </div>
    """, unsafe_allow_html=True)

    with st.form("appointment_form"):

        c1, c2 = st.columns(2)

        with c1:

            professional_name = st.text_input(
                "Professional name"
            )

            professional_role = st.selectbox(
                "Professional role",
                [
                    "Doctor",
                    "Rehabilitator",
                    "Physiotherapist",
                    "Occupational Therapist",
                    "Other clinical professional",
                ]
            )

            specialty = st.text_input(
                "Specialty",
                value="Physical Medicine & Rehabilitation"
            )

            appointment_date = st.date_input(
                "Appointment date",
                value=date.today()
            )

        with c2:

            appointment_time = st.text_input(
                "Appointment time",
                placeholder="Example: 4:30 PM"
            )

            platform = st.selectbox(
                "Platform",
                [
                    "Zoom",
                    "Microsoft Teams",
                    "Google Meet",
                    "Other secure platform",
                ]
            )

            appointment_link = st.text_input(
                "Meeting link",
                placeholder="Paste the meeting URL"
            )

            notes = st.text_area(
                "Session notes"
            )

        if st.form_submit_button(
            "Schedule session"
        ):

            if not professional_name.strip():
                st.error("Professional name is required.")

            elif not appointment_link.strip():
                st.error(
                    "A secure meeting link is required."
                )

            else:

                save_appointment(
                    st.session_state.patient_id,
                    professional_name,
                    professional_role,
                    specialty,
                    appointment_date.isoformat(),
                    appointment_time,
                    platform,
                    appointment_link,
                    notes,
                )

                save_patient({
                    **patient,
                    "meeting_platform": platform,
                    "meeting_link": appointment_link,
                    "meeting_notes": notes,
                })

                st.success(
                    "Clinical session scheduled successfully."
                )

                st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div style="
    margin-top:50px;
    padding-top:20px;
    border-top:1px solid #dfe5ec;
    color:#7a8697;
    font-size:12px;
">
    TeleRehabilitation Portal · Clinical care coordination interface
    <br>
    Production systems require authenticated access control,
    encrypted clinical data storage, audit logging and appropriate
    healthcare privacy/security controls.
</div>
""", unsafe_allow_html=True)
