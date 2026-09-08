import streamlit as st
import sqlite3
import hashlib
from datetime import datetime, date, time as dt_time
from urllib.parse import urlparse

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

# ============================================================
# CONFIGURATION
# ============================================================

DB_FILE = "tele_rehabilitation.db"

ROLE_PATIENT = "Patient"
ROLE_REHAB = "Rehabilitation Professional"
ROLE_HOST = "Meeting Host"
ROLE_ADMIN = "Clinical Administrator"

ROLES = [
    ROLE_PATIENT,
    ROLE_REHAB,
    ROLE_HOST,
    ROLE_ADMIN,
]

LANGUAGES = [
    "English",
    "Urdu",
    "Arabic",
    "Hindi",
    "Punjabi",
    "Sindhi",
    "Pashto",
    "Bengali",
    "French",
    "Spanish",
    "Other",
]

BODY_REGIONS = [
    "Not specified",
    "Head / Neck",
    "Shoulder",
    "Elbow",
    "Wrist / Hand",
    "Chest / Thorax",
    "Upper Back",
    "Lower Back",
    "Hip",
    "Knee",
    "Ankle / Foot",
    "Multiple regions",
    "Other",
]

DIAGNOSIS_STATUS = [
    "Not yet documented",
    "Under assessment",
    "Clinically documented",
    "Referred for further assessment",
]

# ============================================================
# DATABASE
# ============================================================

def get_connection():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def database_initialized():
    try:
        conn = get_connection()
        row = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='patients'"
        ).fetchone()
        conn.close()
        return row is not None
    except Exception:
        return False


def database_init():
    conn = get_connection()

    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT UNIQUE NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            date_of_birth TEXT,
            sex TEXT,
            country TEXT,
            preferred_language TEXT,
            timezone TEXT,
            email TEXT,
            phone TEXT,
            emergency_contact TEXT,
            emergency_phone TEXT,
            diagnosis TEXT,
            diagnosis_status TEXT,
            affected_region TEXT,
            diagnosis_details TEXT,
            medical_record_reference TEXT,
            clinical_notes TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS clinical_measurements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT NOT NULL,
            measurement_name TEXT NOT NULL,
            value TEXT,
            unit TEXT,
            recorded_by TEXT,
            recorded_at TEXT NOT NULL,
            notes TEXT
        );

        CREATE TABLE IF NOT EXISTS rehabilitation_plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT NOT NULL,
            plan_title TEXT NOT NULL,
            goals TEXT,
            precautions TEXT,
            frequency TEXT,
            duration TEXT,
            clinical_instructions TEXT,
            created_by TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS meetings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT NOT NULL,
            meeting_title TEXT,
            provider TEXT,
            meeting_url TEXT,
            meeting_date TEXT,
            meeting_time TEXT,
            host_name TEXT,
            notes TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS activity_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT,
            actor_role TEXT,
            actor_name TEXT,
            action TEXT,
            created_at TEXT NOT NULL
        );
        """
    )

    # --------------------------------------------------------
    # DEMO DATA
    # --------------------------------------------------------

    patient = conn.execute(
        "SELECT patient_id FROM patients WHERE patient_id=?",
        ("TRP-1001",),
    ).fetchone()

    if not patient:
        now = datetime.now().isoformat(timespec="seconds")

        conn.execute(
            """
            INSERT INTO patients (
                patient_id,
                first_name,
                last_name,
                date_of_birth,
                sex,
                country,
                preferred_language,
                timezone,
                email,
                phone,
                emergency_contact,
                emergency_phone,
                diagnosis,
                diagnosis_status,
                affected_region,
                diagnosis_details,
                medical_record_reference,
                clinical_notes,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "TRP-1001",
                "Demo",
                "Patient",
                "1990-01-15",
                "Prefer not to say",
                "Pakistan",
                "English",
                "Asia/Karachi",
                "patient@example.com",
                "",
                "",
                "",
                "",
                "Not yet documented",
                "Not specified",
                "",
                "",
                "",
                now,
                now,
            ),
        )

    plan = conn.execute(
        "SELECT id FROM rehabilitation_plans WHERE patient_id=?",
        ("TRP-1001",),
    ).fetchone()

    if not plan:
        now = datetime.now().isoformat(timespec="seconds")

        conn.execute(
            """
            INSERT INTO rehabilitation_plans (
                patient_id,
                plan_title,
                goals,
                precautions,
                frequency,
                duration,
                clinical_instructions,
                created_by,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "TRP-1001",
                "Initial rehabilitation plan",
                "Clinical assessment and individualized rehabilitation planning.",
                "Follow the rehabilitation professional's instructions.",
                "As clinically prescribed",
                "To be determined",
                "No exercise prescription has been entered yet.",
                "Clinical Team",
                now,
                now,
            ),
        )

    conn.commit()
    conn.close()


# Do NOT use @st.cache_resource for database initialization.
# This prevents the database initialization problem shown in the screenshot.
database_init()

# ============================================================
# DATABASE HELPERS
# ============================================================

def query_one(sql, params=()):
    conn = get_connection()
    row = conn.execute(sql, params).fetchone()
    conn.close()
    return row


def query_all(sql, params=()):
    conn = get_connection()
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return rows


def execute_sql(sql, params=()):
    conn = get_connection()
    cur = conn.execute(sql, params)
    conn.commit()
    last_id = cur.lastrowid
    conn.close()
    return last_id


def now_string():
    return datetime.now().isoformat(timespec="seconds")


def log_activity(patient_id, role, actor_name, action):
    execute_sql(
        """
        INSERT INTO activity_log
        (patient_id, actor_role, actor_name, action, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            patient_id,
            role,
            actor_name,
            action,
            now_string(),
        ),
    )


# ============================================================
# VALIDATION
# ============================================================

def valid_url(url):
    if not url:
        return False

    try:
        parsed = urlparse(url)
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)
    except Exception:
        return False


def make_patient_id(first_name, last_name):
    base = (
        first_name.strip().upper()[:3]
        + last_name.strip().upper()[:3]
    )

    digest = hashlib.sha1(
        f"{first_name}{last_name}{datetime.now().isoformat()}".encode()
    ).hexdigest()[:4].upper()

    return f"TRP-{base}-{digest}"


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    /* --------------------------------------------------------
       GLOBAL
    -------------------------------------------------------- */

    html, body, [class*="css"] {
        font-family:
            Inter,
            -apple-system,
            BlinkMacSystemFont,
            "Segoe UI",
            sans-serif;
    }

    .stApp {
        background: #f5f7fa;
        color: #172033;
    }

    .block-container {
        max-width: 1500px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    /* --------------------------------------------------------
       SIDEBAR
    -------------------------------------------------------- */

    section[data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e2e7ef;
    }

    section[data-testid="stSidebar"] * {
        color: #172033;
    }

    /* --------------------------------------------------------
       HEADER
    -------------------------------------------------------- */

    .portal-header {
        background: #ffffff;
        border: 1px solid #e0e6ee;
        border-radius: 14px;
        padding: 24px 28px;
        margin-bottom: 20px;
    }

    .portal-title {
        font-size: 30px;
        font-weight: 750;
        letter-spacing: -0.6px;
        color: #13233a;
        margin-bottom: 5px;
    }

    .portal-subtitle {
        font-size: 15px;
        color: #637083;
    }

    /* --------------------------------------------------------
       CARDS
    -------------------------------------------------------- */

    .clinical-card {
        background: #ffffff;
        border: 1px solid #e0e6ee;
        border-radius: 14px;
        padding: 22px;
        margin-bottom: 18px;
        box-shadow: 0 2px 8px rgba(20, 35, 55, 0.035);
    }

    .clinical-card h3 {
        color: #13233a;
        margin-top: 0;
        margin-bottom: 12px;
    }

    .section-title {
        color: #13233a;
        font-size: 22px;
        font-weight: 720;
        margin-top: 8px;
        margin-bottom: 15px;
    }

    .field-label {
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: .55px;
        color: #718096;
        font-weight: 650;
        margin-bottom: 4px;
    }

    .field-value {
        font-size: 16px;
        color: #182338;
        font-weight: 550;
        margin-bottom: 15px;
    }

    .muted {
        color: #68768a;
        font-size: 14px;
    }

    .not-recorded {
        color: #7a8492;
        font-style: italic;
    }

    /* --------------------------------------------------------
       PATIENT HEADER
    -------------------------------------------------------- */

    .patient-banner {
        background: #ffffff;
        border: 1px solid #dfe5ed;
        border-radius: 14px;
        padding: 24px;
        margin-bottom: 22px;
    }

    .patient-name {
        font-size: 27px;
        font-weight: 750;
        color: #13233a;
    }

    .patient-id {
        color: #64748b;
        font-size: 14px;
        margin-top: 3px;
    }

    /* --------------------------------------------------------
       MEETING
    -------------------------------------------------------- */

    .meeting-card {
        background: #f8fbff;
        border: 1px solid #cfddec;
        border-radius: 14px;
        padding: 22px;
        margin-bottom: 18px;
    }

    .meeting-title {
        color: #13233a;
        font-size: 21px;
        font-weight: 720;
    }

    /* --------------------------------------------------------
       STATUS
    -------------------------------------------------------- */

    .status-ok {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 6px;
        background: #edf8f1;
        color: #237344;
        font-size: 13px;
        font-weight: 650;
    }

    .status-warning {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 6px;
        background: #fff7e8;
        color: #8a5b12;
        font-size: 13px;
        font-weight: 650;
    }

    .status-info {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 6px;
        background: #eef5ff;
        color: #315f9d;
        font-size: 13px;
        font-weight: 650;
    }

    /* --------------------------------------------------------
       NOTICE
    -------------------------------------------------------- */

    .clinical-notice {
        background: #f8fafc;
        border-left: 4px solid #607d9f;
        padding: 13px 16px;
        border-radius: 6px;
        color: #445268;
        margin-bottom: 16px;
        font-size: 14px;
    }

    /* --------------------------------------------------------
       BUTTONS
    -------------------------------------------------------- */

    .stButton > button {
        border-radius: 8px;
        font-weight: 650;
        min-height: 42px;
    }

    /* --------------------------------------------------------
       MOBILE
    -------------------------------------------------------- */

    @media (max-width: 800px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .portal-title {
            font-size: 24px;
        }

        .patient-name {
            font-size: 23px;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# SESSION STATE
# ============================================================

if "role" not in st.session_state:
    st.session_state.role = ROLE_PATIENT

if "patient_id" not in st.session_state:
    st.session_state.patient_id = "TRP-1001"

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="padding: 8px 0 20px 0;">
            <div style="
                font-size:22px;
                font-weight:750;
                color:#13233a;
            ">
                TeleRehabilitation
            </div>

            <div style="
                margin-top:6px;
                color:#6b7788;
                font-size:14px;
                line-height:1.5;
            ">
                Clinical tele-rehabilitation portal
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    role = st.selectbox(
        "Portal role",
        ROLES,
        index=ROLES.index(st.session_state.role),
    )

    st.session_state.role = role

    patients = query_all(
        """
        SELECT patient_id, first_name, last_name
        FROM patients
        ORDER BY first_name, last_name
        """
    )

    patient_options = [
        f"{p['patient_id']} — {p['first_name']} {p['last_name']}"
        for p in patients
    ]

    patient_ids = [p["patient_id"] for p in patients]

    if patient_ids:
        current_index = (
            patient_ids.index(st.session_state.patient_id)
            if st.session_state.patient_id in patient_ids
            else 0
        )

        selected_patient = st.selectbox(
            "Patient record",
            patient_options,
            index=current_index,
        )

        selected_patient_id = selected_patient.split(" — ")[0]
        st.session_state.patient_id = selected_patient_id

    st.divider()

    # Navigation differs according to role.
    if role == ROLE_PATIENT:
        navigation = [
            "Dashboard",
            "My Clinical Record",
            "Rehabilitation Plan",
            "Teleconsultation",
        ]

    elif role == ROLE_REHAB:
        navigation = [
            "Dashboard",
            "Patient Record",
            "Diagnosis & Assessment",
            "Clinical Measurements",
            "Rehabilitation Plan",
            "Teleconsultation",
        ]

    elif role == ROLE_HOST:
        navigation = [
            "Dashboard",
            "Patient Record",
            "Teleconsultation",
        ]

    else:
        navigation = [
            "Dashboard",
            "Patient Record",
            "Diagnosis & Assessment",
            "Clinical Measurements",
            "Rehabilitation Plan",
            "Teleconsultation",
            "System Overview",
        ]

    page = st.radio(
        "Portal navigation",
        navigation,
        index=(
            navigation.index(st.session_state.page)
            if st.session_state.page in navigation
            else 0
        ),
    )

    st.session_state.page = page

    st.divider()

    st.caption(
        "Production deployment should connect authenticated users "
        "to server-side authorization and a secure clinical database."
    )


# ============================================================
# LOAD PATIENT
# ============================================================

patient = query_one(
    """
    SELECT *
    FROM patients
    WHERE patient_id=?
    """,
    (st.session_state.patient_id,),
)

if not patient:
    st.error("The selected patient record could not be loaded.")
    st.stop()


patient_full_name = f"{patient['first_name']} {patient['last_name']}"


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="portal-header">
        <div class="portal-title">
            TeleRehabilitation Portal
        </div>

        <div class="portal-subtitle">
            Clinical care coordination, patient records and
            secure tele-rehabilitation management
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# COMMON PATIENT BANNER
# ============================================================

def render_patient_banner():

    st.markdown(
        f"""
        <div class="patient-banner">
            <div class="patient-name">
                {patient_full_name}
            </div>

            <div class="patient-id">
                Patient ID: {patient['patient_id']}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# DASHBOARD
# ============================================================

def dashboard():

    render_patient_banner()

    st.markdown(
        '<div class="section-title">Patient Overview</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            '<div class="clinical-card">'
            '<div class="field-label">Country</div>',
            unsafe_allow_html=True,
        )
        st.write(patient["country"] or "Not recorded")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown(
            '<div class="clinical-card">'
            '<div class="field-label">Preferred language</div>',
            unsafe_allow_html=True,
        )
        st.write(patient["preferred_language"] or "Not recorded")
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        st.markdown(
            '<div class="clinical-card">'
            '<div class="field-label">Affected region</div>',
            unsafe_allow_html=True,
        )
        st.write(patient["affected_region"] or "Not specified")
        st.markdown("</div>", unsafe_allow_html=True)

    with col4:
        st.markdown(
            '<div class="clinical-card">'
            '<div class="field-label">Diagnosis status</div>',
            unsafe_allow_html=True,
        )
        st.write(patient["diagnosis_status"] or "Not documented")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">Clinical Information</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            '<div class="clinical-card"><h3>Diagnosis</h3>',
            unsafe_allow_html=True,
        )

        diagnosis = patient["diagnosis"]

        if diagnosis:
            st.write(diagnosis)
        else:
            st.markdown(
                '<span class="not-recorded">Not recorded by the rehabilitation professional.</span>',
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown(
            '<div class="clinical-card"><h3>Diagnosis Details</h3>',
            unsafe_allow_html=True,
        )

        details = patient["diagnosis_details"]

        if details:
            st.write(details)
        else:
            st.markdown(
                '<span class="not-recorded">No clinical diagnosis details have been entered.</span>',
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------------------------
    # ROM
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Clinical Measurements</div>',
        unsafe_allow_html=True,
    )

    rom = query_one(
        """
        SELECT *
        FROM clinical_measurements
        WHERE patient_id=?
        AND measurement_name='Range of Motion'
        ORDER BY id DESC
        LIMIT 1
        """,
        (patient["patient_id"],),
    )

    st.markdown(
        '<div class="clinical-card">',
        unsafe_allow_html=True,
    )

    if rom and rom["value"]:
        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown(
                '<div class="field-label">Range of Motion</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="field-value">{rom["value"]} {rom["unit"] or ""}</div>',
                unsafe_allow_html=True,
            )

        with c2:
            st.markdown(
                '<div class="field-label">Recorded by</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="field-value">{rom["recorded_by"] or "Clinical Team"}</div>',
                unsafe_allow_html=True,
            )

        with c3:
            st.markdown(
                '<div class="field-label">Recorded</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="field-value">{rom["recorded_at"]}</div>',
                unsafe_allow_html=True,
            )

        if rom["notes"]:
            st.caption(rom["notes"])

    else:
        st.markdown(
            """
            <div class="clinical-notice">
                Range of motion has not been recorded in this patient
                record. No ROM value is being estimated or generated
                automatically.
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------------------------
    # PLAN
    # --------------------------------------------------------

    plan = query_one(
        """
        SELECT *
        FROM rehabilitation_plans
        WHERE patient_id=?
        ORDER BY id DESC
        LIMIT 1
        """,
        (patient["patient_id"],),
    )

    st.markdown(
        '<div class="section-title">Rehabilitation Plan</div>',
        unsafe_allow_html=True,
    )

    if plan:

        st.markdown(
            '<div class="clinical-card">',
            unsafe_allow_html=True,
        )

        st.subheader(plan["plan_title"])

        c1, c2 = st.columns(2)

        with c1:
            st.markdown("**Clinical goals**")
            st.write(
                plan["goals"]
                or "No goals have been entered."
            )

            st.markdown("**Frequency**")
            st.write(
                plan["frequency"]
                or "Not specified."
            )

        with c2:
            st.markdown("**Precautions**")
            st.write(
                plan["precautions"]
                or "No precautions recorded."
            )

            st.markdown("**Duration**")
            st.write(
                plan["duration"]
                or "Not specified."
            )

        st.markdown("**Clinical instructions**")
        st.write(
            plan["clinical_instructions"]
            or "No instructions have been entered."
        )

        st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.info("No rehabilitation plan has been entered yet.")

    # --------------------------------------------------------
    # MEETING
    # --------------------------------------------------------

    latest_meeting = query_one(
        """
        SELECT *
        FROM meetings
        WHERE patient_id=?
        ORDER BY meeting_date DESC, meeting_time DESC
        LIMIT 1
        """,
        (patient["patient_id"],),
    )

    st.markdown(
        '<div class="section-title">Teleconsultation</div>',
        unsafe_allow_html=True,
    )

    if latest_meeting:

        st.markdown(
            '<div class="meeting-card">',
            unsafe_allow_html=True,
        )

        st.markdown(
            f'<div class="meeting-title">'
            f'{latest_meeting["meeting_title"] or "Scheduled teleconsultation"}'
            f'</div>',
            unsafe_allow_html=True,
        )

        st.write(
            f"Date: {latest_meeting['meeting_date'] or 'Not specified'}"
        )

        st.write(
            f"Time: {latest_meeting['meeting_time'] or 'Not specified'}"
        )

        st.write(
            f"Provider: {latest_meeting['provider'] or 'Not specified'}"
        )

        if latest_meeting["meeting_url"]:
            if valid_url(latest_meeting["meeting_url"]):
                st.link_button(
                    "Join teleconsultation",
                    latest_meeting["meeting_url"],
                    use_container_width=False,
                )
            else:
                st.warning(
                    "The meeting link is present but is not a valid web URL."
                )
        else:
            st.info(
                "No meeting link has been entered by the authorized "
                "meeting host or rehabilitation professional."
            )

        st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.info(
            "No teleconsultation has been scheduled for this patient."
        )


# ============================================================
# PATIENT CLINICAL RECORD
# ============================================================

def clinical_record():

    render_patient_banner()

    st.markdown(
        '<div class="section-title">Patient Clinical Record</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="clinical-notice">
            This record contains patient information entered by the
            clinical team. Patients should not be shown information
            belonging to another patient record.
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            '<div class="clinical-card"><h3>Personal Information</h3>',
            unsafe_allow_html=True,
        )

        fields = [
            ("Patient ID", patient["patient_id"]),
            ("First name", patient["first_name"]),
            ("Last name", patient["last_name"]),
            ("Date of birth", patient["date_of_birth"]),
            ("Sex", patient["sex"]),
            ("Country", patient["country"]),
            ("Preferred language", patient["preferred_language"]),
            ("Timezone", patient["timezone"]),
        ]

        for label, value in fields:
            st.markdown(
                f'<div class="field-label">{label}</div>'
                f'<div class="field-value">'
                f'{value or "Not recorded"}'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown(
            '<div class="clinical-card"><h3>Contact Information</h3>',
            unsafe_allow_html=True,
        )

        fields = [
            ("Email", patient["email"]),
            ("Phone", patient["phone"]),
            ("Emergency contact", patient["emergency_contact"]),
            ("Emergency phone", patient["emergency_phone"]),
            (
                "Medical record reference",
                patient["medical_record_reference"],
            ),
        ]

        for label, value in fields:
            st.markdown(
                f'<div class="field-label">{label}</div>'
                f'<div class="field-value">'
                f'{value or "Not recorded"}'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        '<div class="clinical-card"><h3>Clinical Record</h3>',
        unsafe_allow_html=True,
    )

    clinical_fields = [
        ("Diagnosis", patient["diagnosis"]),
        ("Diagnosis status", patient["diagnosis_status"]),
        ("Affected region", patient["affected_region"]),
        ("Diagnosis details", patient["diagnosis_details"]),
        ("Clinical notes", patient["clinical_notes"]),
    ]

    for label, value in clinical_fields:
        st.markdown(
            f'<div class="field-label">{label}</div>',
            unsafe_allow_html=True,
        )

        if value:
            st.write(value)
        else:
            st.markdown(
                '<span class="not-recorded">Not recorded.</span>',
                unsafe_allow_html=True,
            )

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# DIAGNOSIS & ASSESSMENT
# ============================================================

def diagnosis_assessment():

    render_patient_banner()

    st.markdown(
        '<div class="section-title">Diagnosis & Clinical Assessment</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="clinical-notice">
            Clinical values must be entered from the professional
            assessment. The portal does not fabricate range-of-motion
            values or infer a diagnosis from incomplete information.
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.role not in [
        ROLE_REHAB,
        ROLE_ADMIN,
    ]:
        st.warning(
            "Only a rehabilitation professional or clinical administrator "
            "can update this section."
        )
        clinical_record()
        return

    with st.form("diagnosis_form"):

        col1, col2 = st.columns(2)

        with col1:
            diagnosis = st.text_input(
                "Diagnosis",
                value=patient["diagnosis"] or "",
                placeholder="Enter the clinically documented diagnosis",
            )

            diagnosis_status = st.selectbox(
                "Diagnosis status",
                DIAGNOSIS_STATUS,
                index=(
                    DIAGNOSIS_STATUS.index(
                        patient["diagnosis_status"]
                    )
                    if patient["diagnosis_status"]
                    in DIAGNOSIS_STATUS
                    else 0
                ),
            )

            affected_region = st.selectbox(
                "Affected body region / organ",
                BODY_REGIONS,
                index=(
                    BODY_REGIONS.index(
                        patient["affected_region"]
                    )
                    if patient["affected_region"]
                    in BODY_REGIONS
                    else 0
                ),
            )

        with col2:

            diagnosis_details = st.text_area(
                "Diagnosis details",
                value=patient["diagnosis_details"] or "",
                height=150,
                placeholder=(
                    "Clinical findings, relevant history, "
                    "assessment details and other information"
                ),
            )

            clinical_notes = st.text_area(
                "Clinical notes",
                value=patient["clinical_notes"] or "",
                height=150,
                placeholder="Professional clinical notes",
            )

        submitted = st.form_submit_button(
            "Save clinical assessment",
            use_container_width=True,
        )

        if submitted:

            execute_sql(
                """
                UPDATE patients
                SET diagnosis=?,
                    diagnosis_status=?,
                    affected_region=?,
                    diagnosis_details=?,
                    clinical_notes=?,
                    updated_at=?
                WHERE patient_id=?
                """,
                (
                    diagnosis.strip(),
                    diagnosis_status,
                    affected_region,
                    diagnosis_details.strip(),
                    clinical_notes.strip(),
                    now_string(),
                    patient["patient_id"],
                ),
            )

            log_activity(
                patient["patient_id"],
                st.session_state.role,
                "Clinical User",
                "Updated diagnosis and clinical assessment",
            )

            st.success(
                "Clinical assessment saved successfully."
            )

            st.rerun()


# ============================================================
# CLINICAL MEASUREMENTS
# ============================================================

def clinical_measurements():

    render_patient_banner()

    st.markdown(
        '<div class="section-title">Clinical Measurements</div>',
        unsafe_allow_html=True,
    )

    if st.session_state.role not in [
        ROLE_REHAB,
        ROLE_ADMIN,
    ]:
        st.warning(
            "Clinical measurements can only be entered by "
            "an authorized rehabilitation professional."
        )
        return

    existing_measurements = query_all(
        """
        SELECT *
        FROM clinical_measurements
        WHERE patient_id=?
        ORDER BY id DESC
        """,
        (patient["patient_id"],),
    )

    st.markdown(
        '<div class="clinical-card">',
        unsafe_allow_html=True,
    )

    st.subheader("Record range of motion")

    st.caption(
        "Only enter a value that has actually been measured and documented."
    )

    with st.form("rom_form"):

        col1, col2 = st.columns(2)

        with col1:
            rom_value = st.text_input(
                "Measured ROM",
                placeholder="Example: 112",
            )

        with col2:
            rom_unit = st.text_input(
                "Unit",
                value="degrees",
                placeholder="degrees",
            )

        rom_notes = st.text_area(
            "Measurement notes",
            placeholder=(
                "Specify movement, side, position, "
                "or other clinically relevant context."
            ),
        )

        save_rom = st.form_submit_button(
            "Save measurement",
            use_container_width=True,
        )

        if save_rom:

            if not rom_value.strip():
                st.error(
                    "Enter the measured ROM value before saving."
                )
            else:

                execute_sql(
                    """
                    INSERT INTO clinical_measurements (
                        patient_id,
                        measurement_name,
                        value,
                        unit,
                        recorded_by,
                        recorded_at,
                        notes
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        patient["patient_id"],
                        "Range of Motion",
                        rom_value.strip(),
                        rom_unit.strip(),
                        "Rehabilitation Professional",
                        now_string(),
                        rom_notes.strip(),
                    ),
                )

                log_activity(
                    patient["patient_id"],
                    st.session_state.role,
                    "Clinical User",
                    "Recorded range of motion",
                )

                st.success(
                    "Clinical measurement recorded."
                )

                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        '<div class="clinical-card"><h3>Measurement history</h3>',
        unsafe_allow_html=True,
    )

    if not existing_measurements:
        st.info(
            "No clinical measurements have been recorded."
        )

    else:
        for measurement in existing_measurements:

            with st.container(border=True):

                c1, c2, c3 = st.columns(3)

                with c1:
                    st.markdown(
                        f"**{measurement['measurement_name']}**"
                    )
                    st.write(
                        f"{measurement['value']} "
                        f"{measurement['unit'] or ''}"
                    )

                with c2:
                    st.write(
                        f"Recorded by: "
                        f"{measurement['recorded_by'] or 'Clinical Team'}"
                    )

                with c3:
                    st.write(
                        f"Recorded: {measurement['recorded_at']}"
                    )

                if measurement["notes"]:
                    st.caption(
                        measurement["notes"]
                    )

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# REHABILITATION PLAN
# ============================================================

def rehabilitation_plan():

    render_patient_banner()

    st.markdown(
        '<div class="section-title">Rehabilitation Plan</div>',
        unsafe_allow_html=True,
    )

    plan = query_one(
        """
        SELECT *
        FROM rehabilitation_plans
        WHERE patient_id=?
        ORDER BY id DESC
        LIMIT 1
        """,
        (patient["patient_id"],),
    )

    if st.session_state.role == ROLE_PATIENT:

        if not plan:
            st.info(
                "No rehabilitation plan has been entered yet."
            )
            return

        st.markdown(
            '<div class="clinical-card">',
            unsafe_allow_html=True,
        )

        st.subheader(plan["plan_title"])

        st.markdown("**Goals**")
        st.write(
            plan["goals"]
            or "No goals have been documented."
        )

        st.markdown("**Frequency**")
        st.write(
            plan["frequency"]
            or "Not specified."
        )

        st.markdown("**Duration**")
        st.write(
            plan["duration"]
            or "Not specified."
        )

        st.markdown("**Precautions**")
        st.write(
            plan["precautions"]
            or "No precautions recorded."
        )

        st.markdown("**Clinical instructions**")
        st.write(
            plan["clinical_instructions"]
            or "No instructions have been entered."
        )

        st.markdown("</div>", unsafe_allow_html=True)

        return

    # --------------------------------------------------------
    # PROFESSIONAL EDIT MODE
    # --------------------------------------------------------

    if st.session_state.role not in [
        ROLE_REHAB,
        ROLE_ADMIN,
    ]:
        st.warning(
            "Only a rehabilitation professional or clinical "
            "administrator can edit the rehabilitation plan."
        )
        return

    current = plan

    with st.form("rehabilitation_plan_form"):

        title = st.text_input(
            "Plan title",
            value=(
                current["plan_title"]
                if current
                else "Individualized rehabilitation plan"
            ),
        )

        goals = st.text_area(
            "Clinical goals",
            value=current["goals"] if current else "",
            height=130,
        )

        precautions = st.text_area(
            "Precautions / contraindications",
            value=current["precautions"] if current else "",
            height=130,
        )

        frequency = st.text_input(
            "Frequency",
            value=current["frequency"] if current else "",
            placeholder="Example: 3 sessions per week",
        )

        duration = st.text_input(
            "Plan duration",
            value=current["duration"] if current else "",
            placeholder="Example: 6 weeks",
        )

        instructions = st.text_area(
            "Clinical instructions",
            value=(
                current["clinical_instructions"]
                if current
                else ""
            ),
            height=160,
        )

        save_plan = st.form_submit_button(
            "Save rehabilitation plan",
            use_container_width=True,
        )

        if save_plan:

            if current:

                execute_sql(
                    """
                    UPDATE rehabilitation_plans
                    SET plan_title=?,
                        goals=?,
                        precautions=?,
                        frequency=?,
                        duration=?,
                        clinical_instructions=?,
                        updated_at=?
                    WHERE id=?
                    """,
                    (
                        title.strip(),
                        goals.strip(),
                        precautions.strip(),
                        frequency.strip(),
                        duration.strip(),
                        instructions.strip(),
                        now_string(),
                        current["id"],
                    ),
                )

            else:

                execute_sql(
                    """
                    INSERT INTO rehabilitation_plans (
                        patient_id,
                        plan_title,
                        goals,
                        precautions,
                        frequency,
                        duration,
                        clinical_instructions,
                        created_by,
                        created_at,
                        updated_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        patient["patient_id"],
                        title.strip(),
                        goals.strip(),
                        precautions.strip(),
                        frequency.strip(),
                        duration.strip(),
                        instructions.strip(),
                        "Rehabilitation Professional",
                        now_string(),
                        now_string(),
                    ),
                )

            log_activity(
                patient["patient_id"],
                st.session_state.role,
                "Clinical User",
                "Updated rehabilitation plan",
            )

            st.success(
                "Rehabilitation plan saved."
            )

            st.rerun()


# ============================================================
# TELECONSULTATION
# ============================================================

def teleconsultation():

    render_patient_banner()

    st.markdown(
        '<div class="section-title">Teleconsultation</div>',
        unsafe_allow_html=True,
    )

    meeting = query_one(
        """
        SELECT *
        FROM meetings
        WHERE patient_id=?
        ORDER BY meeting_date DESC, meeting_time DESC
        LIMIT 1
        """,
        (patient["patient_id"],),
    )

    if meeting:

        st.markdown(
            '<div class="meeting-card">',
            unsafe_allow_html=True,
        )

        st.markdown(
            f'<div class="meeting-title">'
            f'{meeting["meeting_title"] or "Teleconsultation"}'
            f'</div>',
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Date**")
            st.write(
                meeting["meeting_date"]
                or "Not specified"
            )

            st.markdown("**Time**")
            st.write(
                meeting["meeting_time"]
                or "Not specified"
            )

        with col2:
            st.markdown("**Provider**")
            st.write(
                meeting["provider"]
                or "Not specified"
            )

            st.markdown("**Meeting host**")
            st.write(
                meeting["host_name"]
                or "Not specified"
            )

        if meeting["notes"]:
            st.markdown("**Meeting notes**")
            st.write(meeting["notes"])

        if meeting["meeting_url"]:

            if valid_url(meeting["meeting_url"]):

                st.link_button(
                    "Join teleconsultation",
                    meeting["meeting_url"],
                )

            else:

                st.warning(
                    "The saved meeting URL is not valid."
                )

        else:

            st.info(
                "The meeting host or authorized rehabilitation "
                "professional has not added the meeting link yet."
            )

        st.markdown("</div>", unsafe_allow_html=True)

    else:

        st.info(
            "There is currently no teleconsultation linked "
            "to this patient record."
        )

    # --------------------------------------------------------
    # HOST / REHAB / ADMIN
    # --------------------------------------------------------

    if st.session_state.role not in [
        ROLE_HOST,
        ROLE_REHAB,
        ROLE_ADMIN,
    ]:
        return

    st.markdown(
        '<div class="section-title">Meeting management</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="clinical-notice">
            The authorized meeting host, rehabilitation professional,
            or administrator can paste the external teleconsultation
            link here. The patient will see the link only when viewing
            this patient record.
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("meeting_form"):

        col1, col2 = st.columns(2)

        with col1:

            meeting_title = st.text_input(
                "Meeting title",
                value=(
                    meeting["meeting_title"]
                    if meeting
                    else "Tele-rehabilitation consultation"
                ),
            )

            provider = st.text_input(
                "Provider / clinician",
                value=(
                    meeting["provider"]
                    if meeting
                    else ""
                ),
            )

            host_name = st.text_input(
                "Meeting host",
                value=(
                    meeting["host_name"]
                    if meeting
                    else ""
                ),
            )

        with col2:

            meeting_date = st.text_input(
                "Meeting date",
                value=(
                    meeting["meeting_date"]
                    if meeting
                    else ""
                ),
                placeholder="YYYY-MM-DD",
            )

            meeting_time = st.text_input(
                "Meeting time",
                value=(
                    meeting["meeting_time"]
                    if meeting
                    else ""
                ),
                placeholder="Example: 4:30 PM",
            )

            meeting_url = st.text_input(
                "Teleconsultation / Zoom link",
                value=(
                    meeting["meeting_url"]
                    if meeting
                    else ""
                ),
                placeholder="Paste the complete https:// link",
            )

        meeting_notes = st.text_area(
            "Meeting notes",
            value=(
                meeting["notes"]
                if meeting
                else ""
            ),
            placeholder="Optional meeting information",
        )

        save_meeting = st.form_submit_button(
            "Save meeting information",
            use_container_width=True,
        )

        if save_meeting:

            if meeting_url and not valid_url(meeting_url):

                st.error(
                    "Please enter a valid web link beginning with "
                    "http:// or https://."
                )

            elif meeting:

                execute_sql(
                    """
                    UPDATE meetings
                    SET meeting_title=?,
                        provider=?,
                        meeting_url=?,
                        meeting_date=?,
                        meeting_time=?,
                        host_name=?,
                        notes=?,
                        updated_at=?
                    WHERE id=?
                    """,
                    (
                        meeting_title.strip(),
                        provider.strip(),
                        meeting_url.strip(),
                        meeting_date.strip(),
                        meeting_time.strip(),
                        host_name.strip(),
                        meeting_notes.strip(),
                        now_string(),
                        meeting["id"],
                    ),
                )

                log_activity(
                    patient["patient_id"],
                    st.session_state.role,
                    host_name or "Authorized User",
                    "Updated teleconsultation information",
                )

                st.success(
                    "Teleconsultation information saved."
                )

                st.rerun()

            else:

                execute_sql(
                    """
                    INSERT INTO meetings (
                        patient_id,
                        meeting_title,
                        provider,
                        meeting_url,
                        meeting_date,
                        meeting_time,
                        host_name,
                        notes,
                        created_at,
                        updated_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        patient["patient_id"],
                        meeting_title.strip(),
                        provider.strip(),
                        meeting_url.strip(),
                        meeting_date.strip(),
                        meeting_time.strip(),
                        host_name.strip(),
                        meeting_notes.strip(),
                        now_string(),
                        now_string(),
                    ),
                )

                log_activity(
                    patient["patient_id"],
                    st.session_state.role,
                    host_name or "Authorized User",
                    "Created teleconsultation",
                )

                st.success(
                    "Teleconsultation created."
                )

                st.rerun()


# ============================================================
# SYSTEM OVERVIEW
# ============================================================

def system_overview():

    if st.session_state.role != ROLE_ADMIN:
        st.error(
            "This section is restricted to clinical administrators."
        )
        return

    st.markdown(
        '<div class="section-title">System Overview</div>',
        unsafe_allow_html=True,
    )

    patient_count = query_one(
        "SELECT COUNT(*) AS count FROM patients"
    )["count"]

    meeting_count = query_one(
        "SELECT COUNT(*) AS count FROM meetings"
    )["count"]

    measurement_count = query_one(
        "SELECT COUNT(*) AS count FROM clinical_measurements"
    )["count"]

    plan_count = query_one(
        "SELECT COUNT(*) AS count FROM rehabilitation_plans"
    )["count"]

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Patient records",
            patient_count,
        )

    with c2:
        st.metric(
            "Teleconsultations",
            meeting_count,
        )

    with c3:
        st.metric(
            "Clinical measurements",
            measurement_count,
        )

    with c4:
        st.metric(
            "Rehabilitation plans",
            plan_count,
        )

    st.markdown(
        '<div class="section-title">Recent activity</div>',
        unsafe_allow_html=True,
    )

    logs = query_all(
        """
        SELECT *
        FROM activity_log
        ORDER BY id DESC
        LIMIT 20
        """
    )

    if not logs:
        st.info("No activity has been recorded yet.")
        return

    for log in logs:

        with st.container(border=True):

            c1, c2, c3 = st.columns([2, 2, 4])

            with c1:
                st.write(log["created_at"])

            with c2:
                st.write(log["actor_role"])

            with c3:
                st.write(log["action"])


# ============================================================
# PAGE ROUTING
# ============================================================

if page == "Dashboard":
    dashboard()

elif page == "My Clinical Record":
    clinical_record()

elif page == "Patient Record":
    clinical_record()

elif page == "Diagnosis & Assessment":
    diagnosis_assessment()

elif page == "Clinical Measurements":
    clinical_measurements()

elif page == "Rehabilitation Plan":
    rehabilitation_plan()

elif page == "Teleconsultation":
    teleconsultation()

elif page == "System Overview":
    system_overview()

else:
    dashboard()


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "TeleRehabilitation Portal • Clinical care coordination interface"
)
