import os
import sqlite3
from datetime import datetime, date
from pathlib import Path
from urllib.parse import urlparse

import streamlit as st


# ============================================================
# TELE REHABILITATION PORTAL
# Clinical care coordination and secure tele-rehabilitation
#
# IMPORTANT:
# - This is a functional prototype/demo.
# - The role selector is NOT authentication.
# - Production deployment should use SSO/OAuth/enterprise IAM,
#   server-side authorization, encrypted external database,
#   audit logging, proper secrets management, and HTTPS.
# ============================================================


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="TeleRehabilitation Portal",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PROFESSIONAL CLINICAL UI
# ============================================================

st.markdown(
    """
<style>

:root {
    --navy: #17324D;
    --navy-2: #244B6B;
    --blue: #2F6FED;
    --blue-soft: #EAF2FF;
    --teal: #147D83;
    --teal-soft: #E8F7F7;
    --green: #247A52;
    --green-soft: #EAF7F0;
    --orange: #A75D00;
    --orange-soft: #FFF4E5;
    --red: #B42318;
    --red-soft: #FDECEC;
    --ink: #17212B;
    --muted: #667085;
    --border: #D9E1EA;
    --surface: #FFFFFF;
    --background: #F5F7FA;
}

html, body, [class*="css"] {
    font-family:
        Inter,
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        Roboto,
        Helvetica,
        Arial,
        sans-serif;
}

.stApp {
    background: var(--background);
    color: var(--ink);
}

.block-container {
    max-width: 1500px;
    padding-top: 1.2rem;
    padding-bottom: 3rem;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background: #FFFFFF;
    border-right: 1px solid var(--border);
}

section[data-testid="stSidebar"] * {
    color: var(--ink);
}

/* Hide Streamlit decoration */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* Typography */

h1, h2, h3, h4 {
    color: var(--navy) !important;
    letter-spacing: -0.02em;
}

p, label, .stMarkdown {
    color: var(--ink);
}

/* Cards */

.clinical-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 18px;
    box-shadow: 0 2px 8px rgba(23, 50, 77, 0.04);
}

.hero-card {
    background: linear-gradient(135deg, #17324D 0%, #245477 100%);
    color: white;
    border-radius: 18px;
    padding: 28px;
    margin-bottom: 20px;
    box-shadow: 0 8px 24px rgba(23, 50, 77, 0.14);
}

.hero-card h1,
.hero-card h2,
.hero-card h3,
.hero-card p {
    color: white !important;
}

.section-title {
    color: var(--navy);
    font-size: 1.25rem;
    font-weight: 700;
    margin: 6px 0 14px 0;
}

.section-subtitle {
    color: var(--muted);
    font-size: 0.94rem;
    margin-bottom: 16px;
}

.metric-card {
    background: white;
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 18px;
    min-height: 110px;
}

.metric-label {
    color: var(--muted);
    font-size: 0.86rem;
    font-weight: 600;
    margin-bottom: 7px;
}

.metric-value {
    color: var(--navy);
    font-size: 1.45rem;
    font-weight: 750;
}

.metric-muted {
    color: var(--muted);
    font-size: 1rem;
    font-weight: 600;
}

.status-complete {
    display: inline-block;
    background: var(--green-soft);
    color: var(--green);
    border-radius: 999px;
    padding: 6px 11px;
    font-size: 0.82rem;
    font-weight: 700;
}

.status-pending {
    display: inline-block;
    background: var(--orange-soft);
    color: var(--orange);
    border-radius: 999px;
    padding: 6px 11px;
    font-size: 0.82rem;
    font-weight: 700;
}

.status-info {
    display: inline-block;
    background: var(--blue-soft);
    color: var(--blue);
    border-radius: 999px;
    padding: 6px 11px;
    font-size: 0.82rem;
    font-weight: 700;
}

.notice {
    border-left: 4px solid var(--blue);
    background: var(--blue-soft);
    padding: 14px 16px;
    border-radius: 8px;
    margin: 12px 0;
    color: var(--ink);
}

.notice-warning {
    border-left: 4px solid var(--orange);
    background: var(--orange-soft);
}

.notice-danger {
    border-left: 4px solid var(--red);
    background: var(--red-soft);
}

.patient-banner {
    background: #F8FAFC;
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 18px 20px;
    margin-bottom: 18px;
}

.small-text {
    color: var(--muted);
    font-size: 0.88rem;
}

.data-label {
    color: var(--muted);
    font-size: 0.82rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

.data-value {
    color: var(--ink);
    font-size: 1rem;
    margin-top: 3px;
    margin-bottom: 12px;
}

/* Buttons */

.stButton > button,
.stFormSubmitButton > button {
    border-radius: 9px;
    font-weight: 650;
    min-height: 42px;
}

.stButton > button[kind="primary"],
.stFormSubmitButton > button[kind="primary"] {
    background: var(--blue);
    border-color: var(--blue);
    color: white;
}

.stButton > button[kind="secondary"] {
    background: white;
    border-color: var(--border);
    color: var(--navy);
}

/* Inputs */

.stTextInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] > div,
.stNumberInput input,
.stDateInput input,
.stTimeInput input {
    border-radius: 9px !important;
    border-color: #C8D2DE !important;
    background: #FFFFFF !important;
    color: var(--ink) !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus,
.stNumberInput input:focus {
    border-color: var(--blue) !important;
    box-shadow: 0 0 0 1px var(--blue) !important;
}

/* Tabs */

button[data-baseweb="tab"] {
    color: var(--muted) !important;
    font-weight: 650 !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: var(--blue) !important;
}

/* Expander */

details {
    background: white;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
}

/* Divider */

hr {
    border-color: var(--border);
}

/* Links */

a {
    color: var(--blue) !important;
    font-weight: 600;
}

/* Mobile */

@media (max-width: 800px) {
    .block-container {
        padding: 0.8rem;
    }

    .clinical-card {
        padding: 17px;
    }

    .hero-card {
        padding: 20px;
    }
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# DATABASE
# ============================================================

DB_PATH = Path(
    os.environ.get(
        "TELE_REHAB_DB",
        str(Path(__file__).resolve().parent / "tele_rehabilitation.db"),
    )
)


def get_connection():
    """
    IMPORTANT:
    Do not cache a sqlite3 connection with st.cache_resource.

    Streamlit reruns the script frequently and SQLite connections can
    become invalid/stale or be used incorrectly across execution contexts.

    Instead, create a short-lived connection for each operation.
    """
    conn = sqlite3.connect(
        str(DB_PATH),
        timeout=20,
        check_same_thread=False,
    )
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    return conn


def database_initialized():
    try:
        with get_connection() as conn:
            row = conn.execute(
                """
                SELECT name
                FROM sqlite_master
                WHERE type='table'
                  AND name='patients'
                """
            ).fetchone()
            return row is not None
    except sqlite3.Error:
        return False


def database_initialize():
    """
    Safe idempotent database initialization.

    This can be called on every Streamlit rerun.
    It does not depend on a cached connection.
    """

    with get_connection() as conn:

        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_code TEXT UNIQUE NOT NULL,
                full_name TEXT NOT NULL,
                date_of_birth TEXT,
                sex TEXT,
                country TEXT,
                city TEXT,
                timezone TEXT,
                preferred_language TEXT,
                phone TEXT,
                email TEXT,
                emergency_contact TEXT,
                emergency_phone TEXT,

                diagnosis TEXT,
                diagnosis_status TEXT DEFAULT 'Pending',
                affected_region TEXT,
                laterality TEXT,
                condition_type TEXT,
                onset_date TEXT,
                surgery_date TEXT,
                surgery_details TEXT,
                precautions TEXT,
                allergies TEXT,
                medications TEXT,
                comorbidities TEXT,

                functional_limitations TEXT,
                functional_goals TEXT,
                patient_priorities TEXT,

                baseline_pain TEXT,
                baseline_function TEXT,

                rom_status TEXT DEFAULT 'Not assessed',
                rom_notes TEXT,

                treating_clinician TEXT,
                clinician_role TEXT,
                clinician_license TEXT,

                meeting_platform TEXT,
                meeting_url TEXT,
                meeting_notes TEXT,

                mr_document_url TEXT,
                imaging_url TEXT,
                external_record_url TEXT,

                clinical_notes TEXT,
                plan_summary TEXT,

                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                clinician_name TEXT,
                session_type TEXT,
                session_date TEXT,
                session_time TEXT,
                duration_minutes INTEGER,
                platform TEXT,
                meeting_url TEXT,
                host_notes TEXT,
                status TEXT DEFAULT 'Scheduled',
                created_at TEXT NOT NULL,
                FOREIGN KEY(patient_id) REFERENCES patients(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER,
                actor_role TEXT,
                actor_name TEXT,
                action TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY(patient_id) REFERENCES patients(id)
            );
            """
        )

        # Seed only when there are no patients.
        count = conn.execute(
            "SELECT COUNT(*) AS count FROM patients"
        ).fetchone()["count"]

        if count == 0:
            now = datetime.utcnow().isoformat(timespec="seconds")

            conn.execute(
                """
                INSERT INTO patients (
                    patient_code,
                    full_name,
                    date_of_birth,
                    sex,
                    country,
                    city,
                    timezone,
                    preferred_language,
                    phone,
                    email,
                    diagnosis_status,
                    diagnosis,
                    affected_region,
                    laterality,
                    condition_type,
                    functional_limitations,
                    functional_goals,
                    patient_priorities,
                    rom_status,
                    rom_notes,
                    treating_clinician,
                    clinician_role,
                    clinician_license,
                    meeting_platform,
                    meeting_url,
                    clinical_notes,
                    plan_summary,
                    created_at,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    "TRP-1001",
                    "Demo Patient",
                    "1990-01-01",
                    "Prefer not to say",
                    "Pakistan",
                    "Islamabad",
                    "Asia/Karachi",
                    "English",
                    "",
                    "",
                    "Pending",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "Not assessed",
                    "Range of motion has not been clinically assessed.",
                    "Dr. Ahmed Khan",
                    "Physical Medicine & Rehabilitation",
                    "",
                    "Zoom",
                    "",
                    "Complete the clinical assessment before entering objective measurements.",
                    "Individualized rehabilitation plan will be documented after assessment.",
                    now,
                    now,
                ),
            )

            patient_id = conn.execute(
                "SELECT id FROM patients WHERE patient_code = ?",
                ("TRP-1001",),
            ).fetchone()["id"]

            conn.execute(
                """
                INSERT INTO sessions (
                    patient_id,
                    clinician_name,
                    session_type,
                    session_date,
                    session_time,
                    duration_minutes,
                    platform,
                    meeting_url,
                    host_notes,
                    status,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    patient_id,
                    "Dr. Ahmed Khan",
                    "Initial Tele-Rehabilitation Consultation",
                    "2026-09-15",
                    "16:30",
                    45,
                    "Zoom",
                    "",
                    "Meeting host/clinician should paste the secure meeting link here.",
                    "Scheduled",
                    now,
                ),
            )

        conn.commit()


# ============================================================
# DATABASE HELPERS
# ============================================================

def get_all_patients():
    """
    Returns all patient records.

    No Streamlit cache is used.
    """
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT *
            FROM patients
            ORDER BY full_name COLLATE NOCASE
            """
        ).fetchall()
        return [dict(row) for row in rows]


def get_patient(patient_code):
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT *
            FROM patients
            WHERE patient_code = ?
            """,
            (patient_code,),
        ).fetchone()

        return dict(row) if row else None


def get_patient_by_id(patient_id):
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT *
            FROM patients
            WHERE id = ?
            """,
            (patient_id,),
        ).fetchone()

        return dict(row) if row else None


def get_sessions(patient_id):
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT *
            FROM sessions
            WHERE patient_id = ?
            ORDER BY session_date DESC, session_time DESC
            """,
            (patient_id,),
        ).fetchall()

        return [dict(row) for row in rows]


def log_action(patient_id, role, actor, action):
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO audit_log (
                patient_id,
                actor_role,
                actor_name,
                action,
                created_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                patient_id,
                role,
                actor,
                action,
                datetime.utcnow().isoformat(timespec="seconds"),
            ),
        )
        conn.commit()


def update_patient(patient_id, values):
    now = datetime.utcnow().isoformat(timespec="seconds")

    allowed = {
        "full_name",
        "date_of_birth",
        "sex",
        "country",
        "city",
        "timezone",
        "preferred_language",
        "phone",
        "email",
        "emergency_contact",
        "emergency_phone",
        "diagnosis",
        "diagnosis_status",
        "affected_region",
        "laterality",
        "condition_type",
        "onset_date",
        "surgery_date",
        "surgery_details",
        "precautions",
        "allergies",
        "medications",
        "comorbidities",
        "functional_limitations",
        "functional_goals",
        "patient_priorities",
        "baseline_pain",
        "baseline_function",
        "rom_status",
        "rom_notes",
        "treating_clinician",
        "clinician_role",
        "clinician_license",
        "meeting_platform",
        "meeting_url",
        "meeting_notes",
        "mr_document_url",
        "imaging_url",
        "external_record_url",
        "clinical_notes",
        "plan_summary",
    }

    clean = {
        key: value
        for key, value in values.items()
        if key in allowed
    }

    clean["updated_at"] = now

    assignments = ", ".join(
        f"{key} = ?" for key in clean.keys()
    )

    params = list(clean.values())
    params.append(patient_id)

    with get_connection() as conn:
        conn.execute(
            f"""
            UPDATE patients
            SET {assignments}
            WHERE id = ?
            """,
            params,
        )
        conn.commit()


def add_session(
    patient_id,
    clinician_name,
    session_type,
    session_date,
    session_time,
    duration_minutes,
    platform,
    meeting_url,
    host_notes,
):
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO sessions (
                patient_id,
                clinician_name,
                session_type,
                session_date,
                session_time,
                duration_minutes,
                platform,
                meeting_url,
                host_notes,
                status,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                patient_id,
                clinician_name,
                session_type,
                session_date,
                session_time,
                duration_minutes,
                platform,
                meeting_url,
                host_notes,
                "Scheduled",
                datetime.utcnow().isoformat(timespec="seconds"),
            ),
        )
        conn.commit()


# ============================================================
# SAFE URL VALIDATION
# ============================================================

def valid_http_url(value):
    if not value:
        return True

    try:
        parsed = urlparse(value.strip())
        return parsed.scheme in {"http", "https"} and bool(parsed.netloc)
    except Exception:
        return False


# ============================================================
# DATABASE STARTUP
# ============================================================

try:
    database_initialize()
except Exception as exc:
    st.error(
        "The clinical database could not be initialized. "
        "Check the application's writable storage and database configuration."
    )
    st.exception(exc)
    st.stop()


# ============================================================
# SESSION STATE
# ============================================================

if "portal_role" not in st.session_state:
    st.session_state.portal_role = "Patient"

if "patient_code" not in st.session_state:
    st.session_state.patient_code = "TRP-1001"

if "page" not in st.session_state:
    st.session_state.page = "Overview"


# ============================================================
# CONSTANTS
# ============================================================

ROLES = [
    "Patient",
    "Rehabilitation Clinician",
    "Doctor",
    "Meeting Host",
    "Portal Administrator",
]

PAGES = [
    "Overview",
    "Patient Record",
    "Teleconsultation",
    "Care Plan",
]


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            padding: 8px 0 22px 0;
            border-bottom: 1px solid #D9E1EA;
            margin-bottom: 22px;
        ">
            <div style="
                font-size: 1.35rem;
                font-weight: 800;
                color: #17324D;
            ">
                TeleRehabilitation
            </div>
            <div style="
                margin-top: 6px;
                color: #667085;
                font-size: 0.88rem;
                line-height: 1.45;
            ">
                Clinical care coordination and secure
                tele-rehabilitation management
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Portal access")

    selected_role = st.selectbox(
        "Portal role",
        ROLES,
        index=ROLES.index(st.session_state.portal_role),
        help=(
            "Prototype role selector. Production systems must "
            "derive the role from authenticated identity."
        ),
    )

    if selected_role != st.session_state.portal_role:
        st.session_state.portal_role = selected_role
        st.rerun()

    patients = get_all_patients()

    patient_options = [
        f"{p['patient_code']} — {p['full_name']}"
        for p in patients
    ]

    selected_patient_display = st.selectbox(
        "Patient record",
        patient_options,
        index=next(
            (
                i
                for i, p in enumerate(patients)
                if p["patient_code"] == st.session_state.patient_code
            ),
            0,
        ),
    )

    selected_patient_code = selected_patient_display.split(" — ")[0]

    if selected_patient_code != st.session_state.patient_code:
        st.session_state.patient_code = selected_patient_code
        st.rerun()

    st.divider()

    st.markdown("### Portal")

    for page_name in PAGES:
        if st.button(
            page_name,
            use_container_width=True,
            type=(
                "primary"
                if st.session_state.page == page_name
                else "secondary"
            ),
        ):
            st.session_state.page = page_name
            st.rerun()

    st.divider()

    st.markdown(
        """
        <div class="small-text">
        <strong>Clinical safety</strong><br>
        This portal records clinical information and coordinates
        tele-rehabilitation. It does not independently diagnose
        patients or invent clinical measurements.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# CURRENT PATIENT
# ============================================================

patient = get_patient(st.session_state.patient_code)

if not patient:
    st.error("The selected patient record could not be found.")
    st.stop()


role = st.session_state.portal_role

# Patient access restriction:
#
# In this prototype, the patient can only see the selected patient.
# In production, the patient_code must come from authenticated
# identity/session claims and MUST NOT be selectable by the patient.


# ============================================================
# HEADER
# ============================================================

st.markdown(
    f"""
    <div class="hero-card">
        <h1 style="margin:0;">
            TeleRehabilitation Portal
        </h1>
        <p style="
            margin:8px 0 0 0;
            opacity:0.92;
            font-size:1rem;
        ">
            Clinical care coordination, patient records and
            secure tele-rehabilitation management
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# PATIENT CONTEXT
# ============================================================

st.markdown(
    f"""
    <div class="patient-banner">
        <div style="
            font-size:1.2rem;
            font-weight:750;
            color:#17324D;
        ">
            {patient["full_name"]}
        </div>
        <div class="small-text">
            Patient ID: {patient["patient_code"]}
            &nbsp;&nbsp;•&nbsp;&nbsp;
            Portal role: {role}
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# CLINICAL COMPLETENESS
# ============================================================

def diagnosis_complete(p):
    return bool(
        p.get("diagnosis")
        and p.get("affected_region")
        and p.get("diagnosis_status") == "Complete"
    )


def record_completion_items(p):
    return {
        "Identity & demographics": bool(
            p.get("full_name")
            and p.get("country")
            and p.get("preferred_language")
        ),
        "Diagnosis": diagnosis_complete(p),
        "Affected region": bool(p.get("affected_region")),
        "Clinical precautions": bool(p.get("precautions")),
        "Functional goals": bool(p.get("functional_goals")),
        "Clinician": bool(p.get("treating_clinician")),
        "Teleconsultation link": bool(p.get("meeting_url")),
    }


completion = record_completion_items(patient)
completed_count = sum(completion.values())
total_count = len(completion)


# ============================================================
# OVERVIEW
# ============================================================

def render_overview():
    st.markdown("## Overview")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Patient</div>
                <div class="metric-value">
                    {patient["full_name"]}
                </div>
                <div class="small-text">
                    {patient["patient_code"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        diagnosis_value = (
            patient["diagnosis"]
            if patient["diagnosis"]
            else "Not documented"
        )

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Diagnosis</div>
                <div class="metric-value">
                    {diagnosis_value}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        region_value = (
            patient["affected_region"]
            if patient["affected_region"]
            else "Not documented"
        )

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Affected region</div>
                <div class="metric-value">
                    {region_value}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c4:
        language_value = (
            patient["preferred_language"]
            if patient["preferred_language"]
            else "Not selected"
        )

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Preferred language</div>
                <div class="metric-value">
                    {language_value}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")

    st.markdown(
        """
        <div class="clinical-card">
            <div class="section-title">
                Patient record completion
            </div>
            <div class="section-subtitle">
                Clinical measurements should only be entered after
                the relevant assessment information is documented.
            </div>
        """,
        unsafe_allow_html=True,
    )

    progress = completed_count / total_count if total_count else 0

    st.progress(progress)

    st.markdown(
        f"""
        <div class="small-text">
            {completed_count} of {total_count} core record areas completed
        </div>
        """,
        unsafe_allow_html=True,
    )

    for item, done in completion.items():
        if done:
            st.markdown(
                f"""
                <div style="
                    display:inline-block;
                    margin:6px 6px 0 0;
                    padding:7px 10px;
                    border-radius:8px;
                    background:#EAF7F0;
                    color:#247A52;
                    font-weight:650;
                    font-size:0.84rem;
                ">
                    ✓ {item}
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div style="
                    display:inline-block;
                    margin:6px 6px 0 0;
                    padding:7px 10px;
                    border-radius:8px;
                    background:#FFF4E5;
                    color:#A75D00;
                    font-weight:650;
                    font-size:0.84rem;
                ">
                    Pending · {item}
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------------------------
    # ROM SAFETY
    # --------------------------------------------------------

    st.markdown("### Objective assessment")

    if not diagnosis_complete(patient):
        st.markdown(
            """
            <div class="notice notice-warning">
                <strong>Range of motion: Not assessed</strong><br>
                Diagnosis and affected region have not been completed.
                No numerical ROM value is displayed because the portal
                must not fabricate a clinical measurement.
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        rom_status = patient.get("rom_status") or "Not assessed"

        if rom_status == "Assessed":
            st.markdown(
                f"""
                <div class="clinical-card">
                    <div class="section-title">
                        Range of motion assessment
                    </div>
                    <div class="metric-value">
                        Clinically assessed
                    </div>
                    <div class="small-text">
                        {patient.get("rom_notes") or "Assessment notes recorded by clinician."}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div class="notice">
                    <strong>Range of motion: Not assessed</strong><br>
                    A clinician must perform and document the assessment
                    before an objective value is recorded.
                </div>
                """,
                unsafe_allow_html=True,
            )

    # --------------------------------------------------------
    # UPCOMING SESSION
    # --------------------------------------------------------

    st.markdown("### Upcoming teleconsultation")

    sessions = get_sessions(patient["id"])

    upcoming = [
        s for s in sessions
        if s["status"] in {"Scheduled", "Confirmed"}
    ]

    if upcoming:
        session = upcoming[0]

        st.markdown(
            f"""
            <div class="clinical-card">
                <div class="section-title">
                    {session["session_type"]}
                </div>

                <div class="data-label">Clinician</div>
                <div class="data-value">
                    {session["clinician_name"] or "Not assigned"}
                </div>

                <div class="data-label">Date</div>
                <div class="data-value">
                    {session["session_date"] or "Not scheduled"}
                </div>

                <div class="data-label">Time</div>
                <div class="data-value">
                    {session["session_time"] or "Not scheduled"}
                </div>

                <div class="data-label">Platform</div>
                <div class="data-value">
                    {session["platform"] or "Not specified"}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if session.get("meeting_url") and valid_http_url(
            session["meeting_url"]
        ):
            st.link_button(
                "Join teleconsultation",
                session["meeting_url"],
                type="primary",
            )
        else:
            st.info(
                "The secure meeting link has not yet been added by "
                "the meeting host or clinician."
            )
    else:
        st.info("No scheduled teleconsultation is currently recorded.")


# ============================================================
# PATIENT RECORD
# ============================================================

def render_patient_record():

    st.markdown("## Patient Record")

    can_edit = role in {
        "Rehabilitation Clinician",
        "Doctor",
        "Portal Administrator",
    }

    if not can_edit:
        st.info(
            "This record is read-only for the current portal role."
        )

    # --------------------------------------------------------
    # RECORD VIEW
    # --------------------------------------------------------

    with st.expander(
        "Identity, demographics and communication",
        expanded=True,
    ):
        cols = st.columns(3)

        with cols[0]:
            st.markdown("**Patient name**")
            st.write(patient["full_name"] or "Not documented")

            st.markdown("**Date of birth**")
            st.write(patient["date_of_birth"] or "Not documented")

            st.markdown("**Sex**")
            st.write(patient["sex"] or "Not documented")

        with cols[1]:
            st.markdown("**Country**")
            st.write(patient["country"] or "Not documented")

            st.markdown("**City**")
            st.write(patient["city"] or "Not documented")

            st.markdown("**Timezone**")
            st.write(patient["timezone"] or "Not documented")

        with cols[2]:
            st.markdown("**Preferred language**")
            st.write(
                patient["preferred_language"]
                or "Not documented"
            )

            st.markdown("**Email**")
            st.write(patient["email"] or "Not documented")

            st.markdown("**Phone**")
            st.write(patient["phone"] or "Not documented")

    # --------------------------------------------------------
    # CLINICAL INFORMATION
    # --------------------------------------------------------

    with st.expander(
        "Diagnosis and affected region",
        expanded=True,
    ):

        cols = st.columns(3)

        with cols[0]:
            st.markdown("**Diagnosis status**")
            st.write(
                patient["diagnosis_status"]
                or "Pending"
            )

            st.markdown("**Diagnosis**")
            st.write(
                patient["diagnosis"]
                or "Not documented"
            )

        with cols[1]:
            st.markdown("**Condition type**")
            st.write(
                patient["condition_type"]
                or "Not documented"
            )

            st.markdown("**Affected region**")
            st.write(
                patient["affected_region"]
                or "Not documented"
            )

        with cols[2]:
            st.markdown("**Laterality**")
            st.write(
                patient["laterality"]
                or "Not documented"
            )

            st.markdown("**Onset date**")
            st.write(
                patient["onset_date"]
                or "Not documented"
            )

        if not diagnosis_complete(patient):
            st.warning(
                "Clinical assessment is incomplete. Objective "
                "measurements must not be inferred from missing data."
            )

    # --------------------------------------------------------
    # HISTORY AND SAFETY
    # --------------------------------------------------------

    with st.expander("Clinical history and safety"):

        fields = [
            ("Surgery date", patient["surgery_date"]),
            ("Surgery details", patient["surgery_details"]),
            ("Precautions", patient["precautions"]),
            ("Allergies", patient["allergies"]),
            ("Medications", patient["medications"]),
            ("Comorbidities", patient["comorbidities"]),
        ]

        for label, value in fields:
            st.markdown(f"**{label}**")
            st.write(value or "Not documented")

    # --------------------------------------------------------
    # FUNCTIONAL INFORMATION
    # --------------------------------------------------------

    with st.expander("Functional status and patient goals"):

        st.markdown("**Functional limitations**")
        st.write(
            patient["functional_limitations"]
            or "Not documented"
        )

        st.markdown("**Functional goals**")
        st.write(
            patient["functional_goals"]
            or "Not documented"
        )

        st.markdown("**Patient priorities**")
        st.write(
            patient["patient_priorities"]
            or "Not documented"
        )

        st.markdown("**Baseline pain**")
        st.write(
            patient["baseline_pain"]
            or "Not documented"
        )

        st.markdown("**Baseline function**")
        st.write(
            patient["baseline_function"]
            or "Not documented"
        )

    # --------------------------------------------------------
    # CLINICIAN
    # --------------------------------------------------------

    with st.expander("Treating clinician"):

        cols = st.columns(3)

        with cols[0]:
            st.markdown("**Clinician**")
            st.write(
                patient["treating_clinician"]
                or "Not assigned"
            )

        with cols[1]:
            st.markdown("**Professional role**")
            st.write(
                patient["clinician_role"]
                or "Not documented"
            )

        with cols[2]:
            st.markdown("**Professional license / registration**")
            st.write(
                patient["clinician_license"]
                or "Not documented"
            )

    # --------------------------------------------------------
    # DOCUMENT LINKS
    # --------------------------------------------------------

    with st.expander("Clinical documents and medical-record links"):

        st.markdown(
            """
            <div class="notice">
                Documents and links should be supplied by the authorized
                clinician, doctor or meeting host. The application should
                not expose another patient's records.
            </div>
            """,
            unsafe_allow_html=True,
        )

        links = [
            ("Medical record / MR", patient["mr_document_url"]),
            ("Imaging", patient["imaging_url"]),
            ("External clinical record", patient["external_record_url"]),
        ]

        for label, url in links:
            st.markdown(f"**{label}**")

            if url and valid_http_url(url):
                st.link_button(
                    f"Open {label}",
                    url,
                )
            else:
                st.caption("No link has been added.")

    # --------------------------------------------------------
    # EDIT FORM
    # --------------------------------------------------------

    if not can_edit:
        return

    st.markdown("### Clinical record management")

    with st.form("patient_record_form"):

        st.markdown("#### Identity and demographics")

        c1, c2, c3 = st.columns(3)

        with c1:
            full_name = st.text_input(
                "Full name",
                value=patient["full_name"] or "",
            )

            date_of_birth = st.text_input(
                "Date of birth",
                value=patient["date_of_birth"] or "",
                placeholder="YYYY-MM-DD",
            )

            sex = st.selectbox(
                "Sex",
                [
                    "",
                    "Female",
                    "Male",
                    "Intersex",
                    "Prefer not to say",
                ],
                index=(
                    [
                        "",
                        "Female",
                        "Male",
                        "Intersex",
                        "Prefer not to say",
                    ].index(patient["sex"])
                    if patient["sex"] in [
                        "",
                        "Female",
                        "Male",
                        "Intersex",
                        "Prefer not to say",
                    ]
                    else 0
                ),
            )

        with c2:
            country = st.text_input(
                "Country",
                value=patient["country"] or "",
            )

            city = st.text_input(
                "City",
                value=patient["city"] or "",
            )

            timezone = st.text_input(
                "Timezone",
                value=patient["timezone"] or "",
                placeholder="e.g. Asia/Karachi",
            )

        with c3:
            language_options = [
                "English",
                "Urdu",
                "Arabic",
                "French",
                "Spanish",
                "German",
                "Chinese",
                "Other",
            ]

            preferred_language = st.selectbox(
                "Preferred language",
                language_options,
                index=(
                    language_options.index(
                        patient["preferred_language"]
                    )
                    if patient["preferred_language"]
                    in language_options
                    else 0
                ),
            )

            phone = st.text_input(
                "Phone",
                value=patient["phone"] or "",
            )

            email = st.text_input(
                "Email",
                value=patient["email"] or "",
            )

        st.markdown("#### Diagnosis and clinical assessment")

        c1, c2 = st.columns(2)

        with c1:

            diagnosis_status = st.selectbox(
                "Diagnosis status",
                ["Pending", "Complete"],
                index=(
                    1
                    if patient["diagnosis_status"] == "Complete"
                    else 0
                ),
            )

            diagnosis = st.text_input(
                "Clinical diagnosis",
                value=patient["diagnosis"] or "",
            )

            condition_type = st.selectbox(
                "Condition type",
                [
                    "",
                    "Musculoskeletal",
                    "Neurological",
                    "Orthopaedic",
                    "Post-operative",
                    "Sports / activity-related",
                    "Cardiopulmonary",
                    "Other",
                ],
                index=(
                    [
                        "",
                        "Musculoskeletal",
                        "Neurological",
                        "Orthopaedic",
                        "Post-operative",
                        "Sports / activity-related",
                        "Cardiopulmonary",
                        "Other",
                    ].index(patient["condition_type"])
                    if patient["condition_type"] in [
                        "",
                        "Musculoskeletal",
                        "Neurological",
                        "Orthopaedic",
                        "Post-operative",
                        "Sports / activity-related",
                        "Cardiopulmonary",
                        "Other",
                    ]
                    else 0
                ),
            )

        with c2:

            affected_region = st.text_input(
                "Affected body region",
                value=patient["affected_region"] or "",
                placeholder="e.g. right knee",
            )

            laterality = st.selectbox(
                "Laterality",
                [
                    "",
                    "Left",
                    "Right",
                    "Bilateral",
                    "Midline",
                    "Not applicable",
                ],
                index=(
                    [
                        "",
                        "Left",
                        "Right",
                        "Bilateral",
                        "Midline",
                        "Not applicable",
                    ].index(patient["laterality"])
                    if patient["laterality"] in [
                        "",
                        "Left",
                        "Right",
                        "Bilateral",
                        "Midline",
                        "Not applicable",
                    ]
                    else 0
                ),
            )

            onset_date = st.text_input(
                "Onset date",
                value=patient["onset_date"] or "",
                placeholder="YYYY-MM-DD",
            )

        st.markdown("#### History and safety")

        surgery_date = st.text_input(
            "Surgery date",
            value=patient["surgery_date"] or "",
            placeholder="YYYY-MM-DD or not applicable",
        )

        surgery_details = st.text_area(
            "Surgery / procedure details",
            value=patient["surgery_details"] or "",
        )

        precautions = st.text_area(
            "Precautions / contraindications",
            value=patient["precautions"] or "",
        )

        allergies = st.text_area(
            "Allergies",
            value=patient["allergies"] or "",
        )

        medications = st.text_area(
            "Current medications",
            value=patient["medications"] or "",
        )

        comorbidities = st.text_area(
            "Relevant comorbidities",
            value=patient["comorbidities"] or "",
        )

        st.markdown("#### Functional assessment")

        functional_limitations = st.text_area(
            "Functional limitations",
            value=patient["functional_limitations"] or "",
        )

        functional_goals = st.text_area(
            "Functional goals",
            value=patient["functional_goals"] or "",
        )

        patient_priorities = st.text_area(
            "Patient priorities",
            value=patient["patient_priorities"] or "",
        )

        baseline_pain = st.text_input(
            "Baseline pain / symptom description",
            value=patient["baseline_pain"] or "",
        )

        baseline_function = st.text_area(
            "Baseline functional status",
            value=patient["baseline_function"] or "",
        )

        st.markdown("#### Objective assessment")

        rom_status_options = [
            "Not assessed",
            "Assessed",
        ]

        rom_status = st.selectbox(
            "Range-of-motion assessment status",
            rom_status_options,
            index=(
                1
                if patient["rom_status"] == "Assessed"
                else 0
            ),
        )

        rom_notes = st.text_area(
            "ROM assessment notes",
            value=patient["rom_notes"] or "",
            help=(
                "Record the actual clinician assessment. "
                "Do not enter an estimated or automatically invented value."
            ),
        )

        st.markdown("#### Treating clinician")

        c1, c2, c3 = st.columns(3)

        with c1:
            treating_clinician = st.text_input(
                "Clinician name",
                value=patient["treating_clinician"] or "",
            )

        with c2:
            clinician_role = st.text_input(
                "Professional role",
                value=patient["clinician_role"] or "",
            )

        with c3:
            clinician_license = st.text_input(
                "License / registration",
                value=patient["clinician_license"] or "",
            )

        st.markdown("#### Secure teleconsultation")

        c1, c2 = st.columns(2)

        with c1:
            meeting_platform = st.selectbox(
                "Meeting platform",
                [
                    "Zoom",
                    "Microsoft Teams",
                    "Google Meet",
                    "Other",
                ],
                index=(
                    [
                        "Zoom",
                        "Microsoft Teams",
                        "Google Meet",
                        "Other",
                    ].index(patient["meeting_platform"])
                    if patient["meeting_platform"] in [
                        "Zoom",
                        "Microsoft Teams",
                        "Google Meet",
                        "Other",
                    ]
                    else 0
                ),
            )

        with c2:
            meeting_url = st.text_input(
                "Secure meeting link",
                value=patient["meeting_url"] or "",
                placeholder="Paste the secure meeting URL",
            )

        meeting_notes = st.text_area(
            "Meeting notes / host instructions",
            value=patient["meeting_notes"] or "",
        )

        st.markdown("#### Clinical document links")

        mr_document_url = st.text_input(
            "MR / medical record link",
            value=patient["mr_document_url"] or "",
            placeholder="Paste authorized document URL",
        )

        imaging_url = st.text_input(
            "Imaging / investigation link",
            value=patient["imaging_url"] or "",
            placeholder="Paste authorized document URL",
        )

        external_record_url = st.text_input(
            "External clinical record link",
            value=patient["external_record_url"] or "",
            placeholder="Paste authorized record URL",
        )

        st.markdown("#### Clinical plan")

        clinical_notes = st.text_area(
            "Clinical notes",
            value=patient["clinical_notes"] or "",
        )

        plan_summary = st.text_area(
            "Care-plan summary",
            value=patient["plan_summary"] or "",
        )

        submitted = st.form_submit_button(
            "Save clinical record",
            type="primary",
            use_container_width=True,
        )

    if submitted:

        # --------------------------------------------
        # VALIDATION
        # --------------------------------------------

        errors = []

        if not full_name.strip():
            errors.append("Full name is required.")

        if not country.strip():
            errors.append("Country is required.")

        if not preferred_language.strip():
            errors.append("Preferred language is required.")

        if meeting_url and not valid_http_url(meeting_url):
            errors.append(
                "Meeting link must be a valid HTTP/HTTPS URL."
            )

        for label, url in [
            ("MR document", mr_document_url),
            ("Imaging", imaging_url),
            ("External record", external_record_url),
        ]:
            if url and not valid_http_url(url):
                errors.append(
                    f"{label} link must be a valid HTTP/HTTPS URL."
                )

        # --------------------------------------------
        # IMPORTANT CLINICAL VALIDATION
        # --------------------------------------------

        if rom_status == "Assessed":
            if not diagnosis.strip():
                errors.append(
                    "A diagnosis is required before recording "
                    "an objective ROM assessment."
                )

            if not affected_region.strip():
                errors.append(
                    "The affected region is required before recording "
                    "an objective ROM assessment."
                )

            if not rom_notes.strip():
                errors.append(
                    "ROM assessment notes are required when "
                    "ROM status is 'Assessed'."
                )

        if diagnosis_status == "Complete":
            if not diagnosis.strip():
                errors.append(
                    "Diagnosis status cannot be Complete without "
                    "a documented diagnosis."
                )

            if not affected_region.strip():
                errors.append(
                    "Diagnosis status cannot be Complete without "
                    "an affected body region."
                )

        if errors:
            for error in errors:
                st.error(error)
        else:

            update_patient(
                patient["id"],
                {
                    "full_name": full_name.strip(),
                    "date_of_birth": date_of_birth.strip(),
                    "sex": sex,
                    "country": country.strip(),
                    "city": city.strip(),
                    "timezone": timezone.strip(),
                    "preferred_language": preferred_language,
                    "phone": phone.strip(),
                    "email": email.strip(),
                    "diagnosis": diagnosis.strip(),
                    "diagnosis_status": diagnosis_status,
                    "affected_region": affected_region.strip(),
                    "laterality": laterality,
                    "condition_type": condition_type,
                    "onset_date": onset_date.strip(),
                    "surgery_date": surgery_date.strip(),
                    "surgery_details": surgery_details.strip(),
                    "precautions": precautions.strip(),
                    "allergies": allergies.strip(),
                    "medications": medications.strip(),
                    "comorbidities": comorbidities.strip(),
                    "functional_limitations": functional_limitations.strip(),
                    "functional_goals": functional_goals.strip(),
                    "patient_priorities": patient_priorities.strip(),
                    "baseline_pain": baseline_pain.strip(),
                    "baseline_function": baseline_function.strip(),
                    "rom_status": rom_status,
                    "rom_notes": rom_notes.strip(),
                    "treating_clinician": treating_clinician.strip(),
                    "clinician_role": clinician_role.strip(),
                    "clinician_license": clinician_license.strip(),
                    "meeting_platform": meeting_platform,
                    "meeting_url": meeting_url.strip(),
                    "meeting_notes": meeting_notes.strip(),
                    "mr_document_url": mr_document_url.strip(),
                    "imaging_url": imaging_url.strip(),
                    "external_record_url": external_record_url.strip(),
                    "clinical_notes": clinical_notes.strip(),
                    "plan_summary": plan_summary.strip(),
                },
            )

            log_action(
                patient["id"],
                role,
                treating_clinician or role,
                "Updated patient clinical record",
            )

            st.success(
                "Clinical record saved successfully."
            )

            st.rerun()


# ============================================================
# TELECONSULTATION
# ============================================================

def render_teleconsultation():

    st.markdown("## Teleconsultation")

    sessions = get_sessions(patient["id"])

    if sessions:
        for session in sessions:

            with st.container(border=True):

                cols = st.columns([2.2, 1, 1, 1])

                with cols[0]:
                    st.markdown(
                        f"### {session['session_type']}"
                    )
                    st.write(
                        session["clinician_name"]
                        or "Clinician not assigned"
                    )

                with cols[1]:
                    st.markdown("**Date**")
                    st.write(
                        session["session_date"]
                        or "Not scheduled"
                    )

                with cols[2]:
                    st.markdown("**Time**")
                    st.write(
                        session["session_time"]
                        or "Not scheduled"
                    )

                with cols[3]:
                    st.markdown("**Status**")
                    st.write(
                        session["status"]
                        or "Scheduled"
                    )

                st.markdown(
                    f"**Platform:** "
                    f"{session['platform'] or 'Not specified'}"
                )

                if session.get("meeting_url") and valid_http_url(
                    session["meeting_url"]
                ):
                    st.link_button(
                        "Join secure meeting",
                        session["meeting_url"],
                        type="primary",
                    )
                else:
                    st.info(
                        "Meeting URL not yet provided. "
                        "The host or clinician can add it to the patient record."
                    )

                if session.get("host_notes"):
                    st.markdown("**Host / clinician notes**")
                    st.write(session["host_notes"])

    else:
        st.info(
            "No teleconsultation sessions have been scheduled."
        )

    # --------------------------------------------------------
    # HOST / CLINICIAN SESSION CREATION
    # --------------------------------------------------------

    can_schedule = role in {
        "Rehabilitation Clinician",
        "Doctor",
        "Meeting Host",
        "Portal Administrator",
    }

    if not can_schedule:
        return

    st.markdown("### Schedule a teleconsultation")

    with st.form("session_form"):

        c1, c2 = st.columns(2)

        with c1:

            clinician_name = st.text_input(
                "Clinician / host name",
                value=patient["treating_clinician"] or "",
            )

            session_type = st.selectbox(
                "Session type",
                [
                    "Initial Tele-Rehabilitation Consultation",
                    "Follow-up Rehabilitation Session",
                    "Clinical Review",
                    "Functional Assessment",
                    "Care-plan Review",
                    "Other",
                ],
            )

            session_date = st.date_input(
                "Session date",
                value=date.today(),
            )

        with c2:

            session_time = st.time_input(
                "Session time",
            )

            duration_minutes = st.number_input(
                "Duration (minutes)",
                min_value=10,
                max_value=240,
                value=45,
                step=5,
            )

            platform = st.selectbox(
                "Meeting platform",
                [
                    "Zoom",
                    "Microsoft Teams",
                    "Google Meet",
                    "Other",
                ],
            )

        meeting_url = st.text_input(
            "Secure meeting URL",
            placeholder="Paste the meeting link supplied by the host",
        )

        host_notes = st.text_area(
            "Host / clinician notes",
            placeholder=(
                "Information needed by the patient or clinical team."
            ),
        )

        create_session = st.form_submit_button(
            "Schedule session",
            type="primary",
            use_container_width=True,
        )

    if create_session:

        if meeting_url and not valid_http_url(meeting_url):
            st.error(
                "Please enter a valid HTTP/HTTPS meeting URL."
            )
        else:

            add_session(
                patient["id"],
                clinician_name.strip(),
                session_type,
                session_date.isoformat(),
                session_time.strftime("%H:%M"),
                int(duration_minutes),
                platform,
                meeting_url.strip(),
                host_notes.strip(),
            )

            log_action(
                patient["id"],
                role,
                clinician_name or role,
                "Created teleconsultation session",
            )

            st.success(
                "Teleconsultation scheduled."
            )

            st.rerun()


# ============================================================
# CARE PLAN
# ============================================================

def render_care_plan():

    st.markdown("## Care Plan")

    if not diagnosis_complete(patient):

        st.markdown(
            """
            <div class="notice notice-warning">
                <strong>Care plan is awaiting clinical assessment.</strong><br>
                Complete the diagnosis and affected-region information
                before assigning an individualized rehabilitation plan.
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("### Current information")

        cols = st.columns(3)

        with cols[0]:
            st.markdown("**Diagnosis**")
            st.write(
                patient["diagnosis"]
                or "Not documented"
            )

        with cols[1]:
            st.markdown("**Affected region**")
            st.write(
                patient["affected_region"]
                or "Not documented"
            )

        with cols[2]:
            st.markdown("**Functional goals**")
            st.write(
                patient["functional_goals"]
                or "Not documented"
            )

        return

    st.markdown(
        """
        <div class="clinical-card">
            <div class="section-title">
                Individualized rehabilitation plan
            </div>
            <div class="section-subtitle">
                This section is intended for the clinician's
                documented clinical plan. It is not an automatic
                exercise prescription.
            </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("**Diagnosis**")
    st.write(patient["diagnosis"])

    st.markdown("**Affected region**")
    st.write(patient["affected_region"])

    st.markdown("**Functional goals**")
    st.write(
        patient["functional_goals"]
        or "Not documented"
    )

    st.markdown("**Care-plan summary**")
    st.write(
        patient["plan_summary"]
        or "No individualized plan has been documented."
    )

    st.markdown("</div>", unsafe_allow_html=True)

    can_edit = role in {
        "Rehabilitation Clinician",
        "Doctor",
        "Portal Administrator",
    }

    if not can_edit:
        return

    st.markdown("### Update care plan")

    with st.form("care_plan_form"):

        plan_summary = st.text_area(
            "Clinical care-plan summary",
            value=patient["plan_summary"] or "",
            height=180,
        )

        save_plan = st.form_submit_button(
            "Save care plan",
            type="primary",
            use_container_width=True,
        )

    if save_plan:

        update_patient(
            patient["id"],
            {
                "plan_summary": plan_summary.strip(),
            },
        )

        log_action(
            patient["id"],
            role,
            patient["treating_clinician"] or role,
            "Updated care plan",
        )

        st.success(
            "Care plan saved."
        )

        st.rerun()


# ============================================================
# ROLE-SPECIFIC NOTICE
# ============================================================

if role == "Patient":
    st.markdown(
        """
        <div class="notice">
            <strong>Patient portal</strong><br>
            You can review your own clinical information,
            teleconsultation schedule and documented care plan.
            Clinical record changes are performed by authorized
            clinical staff.
        </div>
        """,
        unsafe_allow_html=True,
    )

elif role == "Rehabilitation Clinician":
    st.markdown(
        """
        <div class="notice">
            <strong>Rehabilitation clinician workspace</strong><br>
            Document assessment findings, functional goals,
            precautions, care-plan information and secure
            teleconsultation details.
        </div>
        """,
        unsafe_allow_html=True,
    )

elif role == "Doctor":
    st.markdown(
        """
        <div class="notice">
            <strong>Doctor workspace</strong><br>
            Review and update the patient's clinical record,
            diagnosis, medical history and teleconsultation
            coordination information.
        </div>
        """,
        unsafe_allow_html=True,
    )

elif role == "Meeting Host":
    st.markdown(
        """
        <div class="notice">
            <strong>Meeting host workspace</strong><br>
            Schedule teleconsultations and attach the authorized
            meeting URL to the correct patient session.
        </div>
        """,
        unsafe_allow_html=True,
    )

else:
    st.markdown(
        """
        <div class="notice">
            <strong>Portal administration</strong><br>
            Administrative access should be protected by
            enterprise authentication and audited permissions
            in production.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# ROUTING
# ============================================================

if st.session_state.page == "Overview":
    render_overview()

elif st.session_state.page == "Patient Record":
    render_patient_record()

elif st.session_state.page == "Teleconsultation":
    render_teleconsultation()

elif st.session_state.page == "Care Plan":
    render_care_plan()


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div style="
        text-align:center;
        color:#667085;
        font-size:0.78rem;
        padding:10px;
    ">
        TeleRehabilitation Portal · Clinical care coordination
        · Prototype interface
    </div>
    """,
    unsafe_allow_html=True,
)
