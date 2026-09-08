import streamlit as st
import sqlite3
import json
from datetime import datetime, date
from pathlib import Path
from urllib.parse import urlparse

# ============================================================
# TELE REHABILITATION PORTAL
# Professional clinical tele-rehabilitation coordination portal
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

DB_PATH = Path("tele_rehabilitation.db")

ROLE_OPTIONS = [
    "Patient",
    "Rehabilitator",
    "Doctor",
    "Meeting Host",
    "Administrator",
]

LANGUAGES = [
    "English",
    "Urdu",
    "Arabic",
    "Punjabi",
    "Hindi",
    "Bengali",
    "Other",
]

GENDER_OPTIONS = [
    "Not specified",
    "Male",
    "Female",
    "Other",
]

LATERALITY = [
    "Not specified",
    "Left",
    "Right",
    "Bilateral",
    "Midline",
    "Not applicable",
]

# ============================================================
# PROFESSIONAL LIGHT UI
# ============================================================

st.markdown(
    """
    <style>
    /* ========================================================
       GLOBAL
       ======================================================== */

    html, body, [class*="css"] {
        font-family: "Inter", "Segoe UI", Arial, sans-serif;
    }

    .stApp {
        background: #f5f7fa;
        color: #172033;
    }

    .main .block-container {
        max-width: 1500px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    /* Remove Streamlit decorative top line */
    header[data-testid="stHeader"] {
        background: #ffffff;
    }

    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #dce2e9;
    }

    section[data-testid="stSidebar"] * {
        color: #172033;
    }

    /* ========================================================
       TYPOGRAPHY
       ======================================================== */

    h1, h2, h3, h4 {
        color: #14213d !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }

    p, label, span, div {
        color: #263247;
    }

    .portal-title {
        font-size: 32px;
        font-weight: 800;
        color: #14213d;
        margin-bottom: 4px;
    }

    .portal-subtitle {
        font-size: 15px;
        color: #667085;
        margin-bottom: 18px;
    }

    /* ========================================================
       CARDS
       ======================================================== */

    .clinical-card {
        background: #ffffff;
        border: 1px solid #dfe5ec;
        border-radius: 16px;
        padding: 22px;
        margin-bottom: 18px;
        box-shadow: 0 2px 8px rgba(20, 33, 61, 0.05);
    }

    .clinical-card-title {
        color: #14213d;
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .clinical-card-subtitle {
        color: #667085;
        font-size: 14px;
        margin-bottom: 15px;
    }

    /* ========================================================
       STATUS
       ======================================================== */

    .status-good {
        display: inline-block;
        padding: 6px 11px;
        border-radius: 999px;
        background: #e8f7ef;
        color: #147a4a !important;
        font-size: 13px;
        font-weight: 700;
        border: 1px solid #bde8cf;
    }

    .status-pending {
        display: inline-block;
        padding: 6px 11px;
        border-radius: 999px;
        background: #fff7df;
        color: #8a6500 !important;
        font-size: 13px;
        font-weight: 700;
        border: 1px solid #f0df9e;
    }

    .status-danger {
        display: inline-block;
        padding: 6px 11px;
        border-radius: 999px;
        background: #fff0f0;
        color: #b42318 !important;
        font-size: 13px;
        font-weight: 700;
        border: 1px solid #f4c7c3;
    }

    .status-info {
        display: inline-block;
        padding: 6px 11px;
        border-radius: 999px;
        background: #edf5ff;
        color: #155eef !important;
        font-size: 13px;
        font-weight: 700;
        border: 1px solid #c8ddff;
    }

    /* ========================================================
       METRICS
       ======================================================== */

    .metric-card {
        background: #ffffff;
        border: 1px solid #dfe5ec;
        border-radius: 14px;
        padding: 18px;
        min-height: 105px;
        box-shadow: 0 2px 7px rgba(20, 33, 61, 0.04);
    }

    .metric-label {
        color: #667085 !important;
        font-size: 13px;
        font-weight: 600;
        margin-bottom: 8px;
    }

    .metric-value {
        color: #14213d !important;
        font-size: 25px;
        font-weight: 800;
    }

    .metric-note {
        color: #667085 !important;
        font-size: 12px;
        margin-top: 3px;
    }

    /* ========================================================
       SECTION HEADERS
       ======================================================== */

    .section-heading {
        color: #14213d !important;
        font-size: 23px;
        font-weight: 750;
        margin-top: 15px;
        margin-bottom: 14px;
    }

    .section-description {
        color: #667085 !important;
        font-size: 14px;
        margin-top: -7px;
        margin-bottom: 15px;
    }

    /* ========================================================
       INFORMATION ROW
       ======================================================== */

    .info-label {
        color: #667085 !important;
        font-size: 12px;
        font-weight: 600;
        margin-bottom: 2px;
    }

    .info-value {
        color: #172033 !important;
        font-size: 15px;
        font-weight: 600;
    }

    /* ========================================================
       LINKS
       ======================================================== */

    .safe-link {
        background: #edf5ff;
        border: 1px solid #c8ddff;
        border-radius: 10px;
        padding: 12px 14px;
        margin-bottom: 8px;
    }

    .safe-link a {
        color: #155eef !important;
        font-weight: 650;
        text-decoration: none;
    }

    /* ========================================================
       ALERT
       ======================================================== */

    .clinical-note {
        background: #f8fafc;
        border-left: 4px solid #155eef;
        border-radius: 8px;
        padding: 12px 15px;
        color: #344054 !important;
        margin: 10px 0;
    }

    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {
        border-radius: 9px;
        min-height: 42px;
        font-weight: 650;
        border: 1px solid #cfd6df;
    }

    .stButton > button:hover {
        border-color: #155eef;
    }

    /* ========================================================
       INPUTS
       ======================================================== */

    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div,
    textarea {
        background: #ffffff !important;
        border-color: #cfd6df !important;
        color: #172033 !important;
    }

    input, textarea {
        color: #172033 !important;
    }

    /* ========================================================
       TABS
       ======================================================== */

    button[data-baseweb="tab"] {
        color: #475467 !important;
        font-weight: 650;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #155eef !important;
    }

    /* ========================================================
       REMOVE CODE-LIKE APPEARANCE
       ======================================================== */

    pre, code {
        font-family: "Inter", "Segoe UI", Arial, sans-serif !important;
    }

    /* ========================================================
       FOOTER
       ======================================================== */

    .portal-footer {
        text-align: center;
        color: #98a2b3 !important;
        font-size: 12px;
        padding: 30px 0 10px 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# DATABASE
# ============================================================

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def database_initialized():
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='patients'"
        ).fetchone()
        return row is not None
    finally:
        conn.close()


def database_init():
    conn = get_connection()

    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS patients (
                patient_id TEXT PRIMARY KEY,
                full_name TEXT NOT NULL,
                date_of_birth TEXT,
                gender TEXT,
                phone TEXT,
                email TEXT,
                preferred_language TEXT,
                address TEXT,
                emergency_contact TEXT,
                emergency_phone TEXT,

                diagnosis TEXT,
                diagnosis_status TEXT,
                affected_organ TEXT,
                affected_region TEXT,
                laterality TEXT,
                onset_date TEXT,
                clinical_history TEXT,
                precautions TEXT,
                comorbidities TEXT,

                pain_score TEXT,
                functional_limitations TEXT,

                rom_flexion TEXT,
                rom_extension TEXT,
                rom_abduction TEXT,
                rom_other TEXT,
                rom_verified INTEGER DEFAULT 0,
                rom_verified_by TEXT,
                rom_verified_at TEXT,

                meeting_url TEXT,
                meeting_platform TEXT,
                meeting_notes TEXT,

                mrr_url TEXT,
                referral_url TEXT,
                imaging_url TEXT,
                documents_notes TEXT,

                care_plan TEXT,
                rehabilitation_phase TEXT,
                clinician_notes TEXT,

                record_created TEXT,
                record_updated TEXT
            )
            """
        )

        # Create a clearly labelled demo record.
        existing = conn.execute(
            "SELECT patient_id FROM patients WHERE patient_id = ?",
            ("TRP-1001",),
        ).fetchone()

        if not existing:
            now = datetime.now().isoformat(timespec="seconds")

            conn.execute(
                """
                INSERT INTO patients (
                    patient_id,
                    full_name,
                    preferred_language,
                    diagnosis_status,
                    record_created,
                    record_updated
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    "TRP-1001",
                    "Demo Patient",
                    "English",
                    "Not completed",
                    now,
                    now,
                ),
            )

        conn.commit()

    finally:
        conn.close()


# IMPORTANT:
# No Streamlit cache is used here.
# This prevents the database_initialization() error shown
# in the screenshot.
database_init()


# ============================================================
# DATABASE HELPERS
# ============================================================

def get_patient(patient_id):
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM patients WHERE patient_id = ?",
            (patient_id,),
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def get_all_patients():
    conn = get_connection()
    try:
        rows = conn.execute(
            """
            SELECT patient_id, full_name, diagnosis,
                   diagnosis_status, affected_region,
                   preferred_language, record_updated
            FROM patients
            ORDER BY full_name
            """
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def update_patient(patient_id, data):
    allowed = {
        "full_name",
        "date_of_birth",
        "gender",
        "phone",
        "email",
        "preferred_language",
        "address",
        "emergency_contact",
        "emergency_phone",
        "diagnosis",
        "diagnosis_status",
        "affected_organ",
        "affected_region",
        "laterality",
        "onset_date",
        "clinical_history",
        "precautions",
        "comorbidities",
        "pain_score",
        "functional_limitations",
        "rom_flexion",
        "rom_extension",
        "rom_abduction",
        "rom_other",
        "rom_verified",
        "rom_verified_by",
        "rom_verified_at",
        "meeting_url",
        "meeting_platform",
        "meeting_notes",
        "mrr_url",
        "referral_url",
        "imaging_url",
        "documents_notes",
        "care_plan",
        "rehabilitation_phase",
        "clinician_notes",
    }

    clean = {k: v for k, v in data.items() if k in allowed}

    clean["record_updated"] = datetime.now().isoformat(timespec="seconds")

    fields = list(clean.keys())
    values = list(clean.values())

    assignments = ", ".join([f"{field} = ?" for field in fields])

    conn = get_connection()

    try:
        conn.execute(
            f"""
            UPDATE patients
            SET {assignments}
            WHERE patient_id = ?
            """,
            values + [patient_id],
        )
        conn.commit()
    finally:
        conn.close()


def create_patient(patient_id, full_name):
    now = datetime.now().isoformat(timespec="seconds")

    conn = get_connection()

    try:
        conn.execute(
            """
            INSERT INTO patients (
                patient_id,
                full_name,
                preferred_language,
                diagnosis_status,
                record_created,
                record_updated
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                patient_id,
                full_name,
                "English",
                "Not completed",
                now,
                now,
            ),
        )
        conn.commit()
    finally:
        conn.close()


# ============================================================
# VALIDATION
# ============================================================

def is_valid_url(value):
    if not value:
        return True

    try:
        parsed = urlparse(value)
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)
    except Exception:
        return False


def has_clinical_region(patient):
    return bool(
        patient.get("affected_organ")
        or patient.get("affected_region")
    )


def has_verified_rom(patient):
    return bool(
        patient.get("rom_verified")
        and (
            patient.get("rom_flexion")
            or patient.get("rom_extension")
            or patient.get("rom_abduction")
            or patient.get("rom_other")
        )
    )


def profile_completion(patient):
    fields = [
        patient.get("full_name"),
        patient.get("date_of_birth"),
        patient.get("gender"),
        patient.get("preferred_language"),
        patient.get("diagnosis"),
        patient.get("affected_region"),
        patient.get("affected_organ"),
        patient.get("clinical_history"),
        patient.get("precautions"),
        patient.get("functional_limitations"),
    ]

    completed = sum(bool(x) for x in fields)
    return round((completed / len(fields)) * 100)


# ============================================================
# SESSION STATE
# ============================================================

if "role" not in st.session_state:
    st.session_state.role = "Patient"

if "patient_id" not in st.session_state:
    st.session_state.patient_id = "TRP-1001"


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="portal-title" style="font-size:25px;">TeleRehabilitation</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="portal-subtitle">Clinical tele-rehabilitation coordination portal</div>',
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown("### Portal role")

    role = st.selectbox(
        "Select your portal role",
        ROLE_OPTIONS,
        index=ROLE_OPTIONS.index(st.session_state.role),
        label_visibility="collapsed",
    )

    st.session_state.role = role

    st.divider()

    patients = get_all_patients()

    if patients:
        patient_ids = [p["patient_id"] for p in patients]

        if st.session_state.patient_id not in patient_ids:
            st.session_state.patient_id = patient_ids[0]

        selected_patient = st.selectbox(
            "Patient record",
            patient_ids,
            index=patient_ids.index(st.session_state.patient_id),
        )

        st.session_state.patient_id = selected_patient

    st.divider()

    st.markdown("### Portal principles")

    st.caption("• Patient-specific clinical records")
    st.caption("• Clinician-entered findings")
    st.caption("• Verified measurements only")
    st.caption("• Secure meeting links")
    st.caption("• Patient language preference")
    st.caption("• Medical records and referrals")

    if role == "Patient":
        st.info(
            "Patient view is read-only for clinical information. "
            "Clinical findings must be entered by an authorized clinician."
        )
    else:
        st.warning(
            "Demo authorization mode. Production deployment must connect "
            "this portal to authenticated identity and server-side authorization."
        )


# ============================================================
# CURRENT PATIENT
# ============================================================

patient = get_patient(st.session_state.patient_id)

if not patient:
    st.error("Patient record could not be loaded.")
    st.stop()


# ============================================================
# HEADER
# ============================================================

header_col1, header_col2 = st.columns([4, 1])

with header_col1:
    st.markdown(
        '<div class="portal-title">TeleRehabilitation Portal</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="portal-subtitle">'
        "Clinical care coordination, patient records and secure tele-rehabilitation management"
        "</div>",
        unsafe_allow_html=True,
    )

with header_col2:
    st.markdown(
        f'<span class="status-info">{role}</span>',
        unsafe_allow_html=True,
    )


# ============================================================
# PATIENT HEADER
# ============================================================

st.markdown(
    f"""
    <div class="clinical-card">
        <div class="clinical-card-title">{patient.get("full_name") or "Patient"}</div>
        <div class="clinical-card-subtitle">
            Patient ID: {patient.get("patient_id")}
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# TOP METRICS
# ============================================================

completion = profile_completion(patient)

if patient.get("diagnosis"):
    diagnosis_display = patient["diagnosis"]
else:
    diagnosis_display = "Not documented"

if has_clinical_region(patient):
    region_display = patient.get("affected_region") or patient.get("affected_organ")
else:
    region_display = "Not documented"

language_display = patient.get("preferred_language") or "Not selected"

if has_verified_rom(patient):
    rom_display = "Verified"
else:
    rom_display = "Not recorded"


m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Patient profile</div>
            <div class="metric-value">{completion}%</div>
            <div class="metric-note">Completion</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Diagnosis</div>
            <div class="metric-value" style="font-size:18px;">{diagnosis_display}</div>
            <div class="metric-note">Clinical documentation</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m3:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Affected region</div>
            <div class="metric-value" style="font-size:18px;">{region_display}</div>
            <div class="metric-note">Clinician documented</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m4:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Language</div>
            <div class="metric-value" style="font-size:18px;">{language_display}</div>
            <div class="metric-note">Patient preference</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# NAVIGATION
# ============================================================

st.write("")

tab_overview, tab_record, tab_consult, tab_care = st.tabs(
    [
        "Overview",
        "Clinical Record",
        "Teleconsultation",
        "Care Plan",
    ]
)


# ============================================================
# OVERVIEW
# ============================================================

with tab_overview:

    st.markdown(
        '<div class="section-heading">Patient overview</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-description">'
        "A concise clinical snapshot. Information is displayed only when it has been documented."
        "</div>",
        unsafe_allow_html=True,
    )

    left, right = st.columns(2)

    with left:

        st.markdown(
            """
            <div class="clinical-card">
                <div class="clinical-card-title">Patient information</div>
            """,
            unsafe_allow_html=True,
        )

        info = [
            ("Patient ID", patient.get("patient_id")),
            ("Full name", patient.get("full_name")),
            ("Date of birth", patient.get("date_of_birth")),
            ("Gender", patient.get("gender")),
            ("Preferred language", patient.get("preferred_language")),
            ("Phone", patient.get("phone")),
            ("Email", patient.get("email")),
        ]

        for label, value in info:
            value = value if value else "Not documented"

            st.markdown(
                f"""
                <div style="margin-bottom:13px;">
                    <div class="info-label">{label}</div>
                    <div class="info-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

    with right:

        st.markdown(
            """
            <div class="clinical-card">
                <div class="clinical-card-title">Clinical status</div>
            """,
            unsafe_allow_html=True,
        )

        diagnosis = patient.get("diagnosis")
        region = patient.get("affected_region")
        organ = patient.get("affected_organ")
        laterality = patient.get("laterality")
        diagnosis_status = patient.get("diagnosis_status")

        clinical_items = [
            ("Diagnosis", diagnosis or "Not documented"),
            ("Diagnosis status", diagnosis_status or "Not completed"),
            ("Affected organ", organ or "Not documented"),
            ("Affected region", region or "Not documented"),
            ("Laterality", laterality or "Not specified"),
            ("Pain score", patient.get("pain_score") or "Not recorded"),
        ]

        for label, value in clinical_items:
            st.markdown(
                f"""
                <div style="margin-bottom:13px;">
                    <div class="info-label">{label}</div>
                    <div class="info-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------------------------
    # ROM
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-heading">Range of motion</div>',
        unsafe_allow_html=True,
    )

    if has_verified_rom(patient):

        st.success(
            "Range-of-motion values are displayed because a clinician has "
            "entered and marked them as verified."
        )

        r1, r2, r3, r4 = st.columns(4)

        rom_values = [
            ("Flexion", patient.get("rom_flexion")),
            ("Extension", patient.get("rom_extension")),
            ("Abduction", patient.get("rom_abduction")),
            ("Other", patient.get("rom_other")),
        ]

        for column, (label, value) in zip([r1, r2, r3, r4], rom_values):
            with column:
                st.metric(
                    label,
                    value if value else "—",
                )

        verifier = patient.get("rom_verified_by") or "Clinician"
        verified_at = patient.get("rom_verified_at") or "Date not recorded"

        st.caption(
            f"Verified by: {verifier} • Verification time: {verified_at}"
        )

    else:

        st.info(
            "Range of motion has not been clinically documented and verified. "
            "The portal intentionally does not estimate or invent a ROM value."
        )

    # --------------------------------------------------------
    # PROFILE COMPLETION
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-heading">Profile completion</div>',
        unsafe_allow_html=True,
    )

    st.progress(completion / 100)

    if completion < 100:
        st.warning(
            "The patient record is incomplete. Complete the clinical record "
            "before relying on missing fields for treatment decisions."
        )
    else:
        st.success("The patient profile is substantially complete.")


# ============================================================
# CLINICAL RECORD
# ============================================================

with tab_record:

    st.markdown(
        '<div class="section-heading">Clinical record</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-description">'
        "This section is the source of truth for patient-specific clinical information."
        "</div>",
        unsafe_allow_html=True,
    )

    if role == "Patient":

        st.info(
            "Your clinical record is presented for review. Diagnosis, affected "
            "region, examination findings and ROM must be entered by the "
            "authorized rehabilitator or doctor."
        )

        sections = [
            (
                "Demographics",
                [
                    ("Full name", patient.get("full_name")),
                    ("Date of birth", patient.get("date_of_birth")),
                    ("Gender", patient.get("gender")),
                    ("Preferred language", patient.get("preferred_language")),
                    ("Phone", patient.get("phone")),
                    ("Email", patient.get("email")),
                    ("Address", patient.get("address")),
                ],
            ),
            (
                "Clinical information",
                [
                    ("Diagnosis", patient.get("diagnosis")),
                    ("Diagnosis status", patient.get("diagnosis_status")),
                    ("Affected organ", patient.get("affected_organ")),
                    ("Affected region", patient.get("affected_region")),
                    ("Laterality", patient.get("laterality")),
                    ("Onset date", patient.get("onset_date")),
                    ("Pain score", patient.get("pain_score")),
                    ("Clinical history", patient.get("clinical_history")),
                    ("Functional limitations", patient.get("functional_limitations")),
                    ("Precautions", patient.get("precautions")),
                    ("Comorbidities", patient.get("comorbidities")),
                ],
            ),
        ]

        for title, items in sections:

            with st.container(border=True):
                st.subheader(title)

                for label, value in items:
                    st.write(
                        f"**{label}:** {value if value else 'Not documented'}"
                    )

    else:

        with st.form("clinical_record_form"):

            st.subheader("Patient demographics")

            c1, c2 = st.columns(2)

            with c1:
                full_name = st.text_input(
                    "Full name",
                    value=patient.get("full_name") or "",
                )

                date_of_birth = st.text_input(
                    "Date of birth",
                    value=patient.get("date_of_birth") or "",
                    placeholder="YYYY-MM-DD",
                )

                gender = st.selectbox(
                    "Gender",
                    GENDER_OPTIONS,
                    index=(
                        GENDER_OPTIONS.index(patient["gender"])
                        if patient.get("gender") in GENDER_OPTIONS
                        else 0
                    ),
                )

                preferred_language = st.selectbox(
                    "Preferred language",
                    LANGUAGES,
                    index=(
                        LANGUAGES.index(patient["preferred_language"])
                        if patient.get("preferred_language") in LANGUAGES
                        else 0
                    ),
                )

            with c2:

                phone = st.text_input(
                    "Phone",
                    value=patient.get("phone") or "",
                )

                email = st.text_input(
                    "Email",
                    value=patient.get("email") or "",
                )

                address = st.text_area(
                    "Address",
                    value=patient.get("address") or "",
                    height=80,
                )

            st.divider()

            st.subheader("Emergency contact")

            e1, e2 = st.columns(2)

            with e1:
                emergency_contact = st.text_input(
                    "Emergency contact name",
                    value=patient.get("emergency_contact") or "",
                )

            with e2:
                emergency_phone = st.text_input(
                    "Emergency contact phone",
                    value=patient.get("emergency_phone") or "",
                )

            st.divider()

            st.subheader("Diagnosis and affected region")

            d1, d2 = st.columns(2)

            with d1:

                diagnosis = st.text_input(
                    "Diagnosis",
                    value=patient.get("diagnosis") or "",
                    placeholder="Enter clinician-confirmed diagnosis",
                )

                diagnosis_status_options = [
                    "Not completed",
                    "Provisional",
                    "Clinician confirmed",
                    "Doctor confirmed",
                ]

                diagnosis_status = st.selectbox(
                    "Diagnosis status",
                    diagnosis_status_options,
                    index=(
                        diagnosis_status_options.index(
                            patient["diagnosis_status"]
                        )
                        if patient.get("diagnosis_status")
                        in diagnosis_status_options
                        else 0
                    ),
                )

                affected_organ = st.text_input(
                    "Affected organ / structure",
                    value=patient.get("affected_organ") or "",
                    placeholder="e.g. knee joint",
                )

                affected_region = st.text_input(
                    "Affected region / body area",
                    value=patient.get("affected_region") or "",
                    placeholder="e.g. right lower limb",
                )

            with d2:

                laterality = st.selectbox(
                    "Laterality",
                    LATERALITY,
                    index=(
                        LATERALITY.index(patient["laterality"])
                        if patient.get("laterality") in LATERALITY
                        else 0
                    ),
                )

                onset_date = st.text_input(
                    "Condition / injury onset date",
                    value=patient.get("onset_date") or "",
                    placeholder="YYYY-MM-DD",
                )

                pain_score = st.selectbox(
                    "Pain score",
                    ["Not recorded", "0", "1", "2", "3", "4", "5",
                     "6", "7", "8", "9", "10"],
                    index=(
                        ["Not recorded", "0", "1", "2", "3", "4", "5",
                         "6", "7", "8", "9", "10"].index(
                            patient.get("pain_score")
                        )
                        if patient.get("pain_score")
                        in ["Not recorded", "0", "1", "2", "3", "4", "5",
                            "6", "7", "8", "9", "10"]
                        else 0
                    ),
                )

            clinical_history = st.text_area(
                "Clinical history",
                value=patient.get("clinical_history") or "",
                height=120,
                placeholder=(
                    "Relevant history, previous treatment, surgery, injury, "
                    "symptoms and clinical context."
                ),
            )

            functional_limitations = st.text_area(
                "Functional limitations",
                value=patient.get("functional_limitations") or "",
                height=100,
                placeholder=(
                    "Document activities, movements or participation affected."
                ),
            )

            precautions = st.text_area(
                "Precautions / contraindications",
                value=patient.get("precautions") or "",
                height=100,
            )

            comorbidities = st.text_area(
                "Relevant comorbidities",
                value=patient.get("comorbidities") or "",
                height=100,
            )

            st.divider()

            st.subheader("Clinically measured range of motion")

            st.caption(
                "Do not enter estimated values. ROM should be based on an actual "
                "clinical assessment."
            )

            rom1, rom2, rom3, rom4 = st.columns(4)

            with rom1:
                rom_flexion = st.text_input(
                    "Flexion",
                    value=patient.get("rom_flexion") or "",
                    placeholder="e.g. 112°",
                )

            with rom2:
                rom_extension = st.text_input(
                    "Extension",
                    value=patient.get("rom_extension") or "",
                    placeholder="e.g. 0°",
                )

            with rom3:
                rom_abduction = st.text_input(
                    "Abduction",
                    value=patient.get("rom_abduction") or "",
                    placeholder="e.g. 45°",
                )

            with rom4:
                rom_other = st.text_input(
                    "Other ROM",
                    value=patient.get("rom_other") or "",
                    placeholder="Joint/movement + value",
                )

            existing_verified = bool(patient.get("rom_verified"))

            rom_verified = st.checkbox(
                "I confirm these ROM values were clinically assessed and verified.",
                value=existing_verified,
            )

            rom_verified_by = st.text_input(
                "Verified by",
                value=patient.get("rom_verified_by") or "",
                placeholder="Clinician name / professional identifier",
            )

            if rom_verified:
                rom_verified_at = datetime.now().isoformat(
                    timespec="seconds"
                )
            else:
                rom_verified_at = ""

            st.divider()

            clinician_notes = st.text_area(
                "Clinician notes",
                value=patient.get("clinician_notes") or "",
                height=120,
            )

            submitted = st.form_submit_button(
                "Save clinical record",
                type="primary",
                use_container_width=True,
            )

            if submitted:

                if not full_name.strip():
                    st.error("Full name is required.")
                    st.stop()

                if rom_verified and not (
                    rom_flexion
                    or rom_extension
                    or rom_abduction
                    or rom_other
                ):
                    st.error(
                        "ROM cannot be marked verified without at least one "
                        "clinically assessed ROM value."
                    )
                    st.stop()

                data = {
                    "full_name": full_name,
                    "date_of_birth": date_of_birth,
                    "gender": gender,
                    "phone": phone,
                    "email": email,
                    "preferred_language": preferred_language,
                    "address": address,
                    "emergency_contact": emergency_contact,
                    "emergency_phone": emergency_phone,
                    "diagnosis": diagnosis,
                    "diagnosis_status": diagnosis_status,
                    "affected_organ": affected_organ,
                    "affected_region": affected_region,
                    "laterality": laterality,
                    "onset_date": onset_date,
                    "clinical_history": clinical_history,
                    "precautions": precautions,
                    "comorbidities": comorbidities,
                    "pain_score": pain_score,
                    "functional_limitations": functional_limitations,
                    "rom_flexion": rom_flexion,
                    "rom_extension": rom_extension,
                    "rom_abduction": rom_abduction,
                    "rom_other": rom_other,
                    "rom_verified": 1 if rom_verified else 0,
                    "rom_verified_by": rom_verified_by if rom_verified else "",
                    "rom_verified_at": rom_verified_at,
                    "clinician_notes": clinician_notes,
                }

                update_patient(patient["patient_id"], data)

                st.success(
                    "Clinical record saved successfully."
                )

                st.rerun()


# ============================================================
# TELECONSULTATION
# ============================================================

with tab_consult:

    st.markdown(
        '<div class="section-heading">Teleconsultation</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-description">'
        "Meeting information is stored against this patient record. "
        "The actual meeting URL must be supplied by the authorized doctor, "
        "rehabilitator or meeting host."
        "</div>",
        unsafe_allow_html=True,
    )

    meeting_url = patient.get("meeting_url")

    if meeting_url and is_valid_url(meeting_url):

        st.success("A teleconsultation link is available for this patient.")

        st.link_button(
            "Join teleconsultation",
            meeting_url,
            use_container_width=True,
        )

        st.caption(
            f"Platform: {patient.get('meeting_platform') or 'Not specified'}"
        )

        if patient.get("meeting_notes"):
            st.info(patient["meeting_notes"])

    else:

        st.warning(
            "No valid teleconsultation link has been added yet."
        )

    if role in ["Doctor", "Rehabilitator", "Meeting Host", "Administrator"]:

        with st.container(border=True):

            st.subheader("Meeting details")

            with st.form("meeting_form"):

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
                        ].index(patient.get("meeting_platform"))
                        if patient.get("meeting_platform")
                        in [
                            "Zoom",
                            "Microsoft Teams",
                            "Google Meet",
                            "Other",
                        ]
                        else 0
                    ),
                )

                new_meeting_url = st.text_input(
                    "Meeting URL",
                    value=patient.get("meeting_url") or "",
                    placeholder="Paste the official meeting link here",
                )

                meeting_notes = st.text_area(
                    "Meeting notes / instructions",
                    value=patient.get("meeting_notes") or "",
                    height=100,
                )

                meeting_submit = st.form_submit_button(
                    "Save meeting information",
                    type="primary",
                    use_container_width=True,
                )

                if meeting_submit:

                    if new_meeting_url and not is_valid_url(
                        new_meeting_url
                    ):
                        st.error(
                            "Please enter a valid HTTPS/HTTP meeting URL."
                        )
                        st.stop()

                    update_patient(
                        patient["patient_id"],
                        {
                            "meeting_platform": meeting_platform,
                            "meeting_url": new_meeting_url,
                            "meeting_notes": meeting_notes,
                        },
                    )

                    st.success("Meeting information saved.")
                    st.rerun()

    else:

        st.info(
            "Only the authorized clinical/meeting roles can add or change "
            "the teleconsultation URL."
        )


# ============================================================
# CARE PLAN
# ============================================================

with tab_care:

    st.markdown(
        '<div class="section-heading">Rehabilitation care plan</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-description">'
        "The care plan should be based on the documented clinical assessment."
        "</div>",
        unsafe_allow_html=True,
    )

    phase = patient.get("rehabilitation_phase") or "Not assigned"

    phase_options = [
        "Not assigned",
        "Phase 1 — Protection / Initial recovery",
        "Phase 2 — Mobility + Strength",
        "Phase 3 — Functional training",
        "Phase 4 — Return to activity",
    ]

    if phase not in phase_options:
        phase = "Not assigned"

    with st.container(border=True):

        st.subheader("Current rehabilitation phase")

        st.markdown(
            f'<span class="status-info">{phase}</span>',
            unsafe_allow_html=True,
        )

        if patient.get("care_plan"):
            st.write("")
            st.write(patient["care_plan"])
        else:
            st.info(
                "No care plan has been documented yet."
            )

    if role in ["Doctor", "Rehabilitator", "Administrator"]:

        with st.container(border=True):

            st.subheader("Manage care plan")

            with st.form("care_plan_form"):

                new_phase = st.selectbox(
                    "Rehabilitation phase",
                    phase_options,
                    index=phase_options.index(phase),
                )

                new_care_plan = st.text_area(
                    "Care plan",
                    value=patient.get("care_plan") or "",
                    height=180,
                    placeholder=(
                        "Document goals, frequency, progression criteria, "
                        "precautions and clinician-directed rehabilitation plan."
                    ),
                )

                save_care = st.form_submit_button(
                    "Save care plan",
                    type="primary",
                    use_container_width=True,
                )

                if save_care:

                    update_patient(
                        patient["patient_id"],
                        {
                            "rehabilitation_phase": new_phase,
                            "care_plan": new_care_plan,
                        },
                    )

                    st.success("Care plan updated.")
                    st.rerun()

    else:

        st.info(
            "Care-plan changes are restricted to authorized clinical roles."
        )


# ============================================================
# MEDICAL RECORDS / MRR
# ============================================================

st.markdown(
    '<div class="section-heading">Medical records and referral documents</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-description">'
    "Links are provided by the authorized doctor, rehabilitator or meeting host. "
    "The portal does not invent or generate medical-document URLs."
    "</div>",
    unsafe_allow_html=True,
)

documents = [
    ("Medical record / MRR", patient.get("mrr_url")),
    ("Referral document", patient.get("referral_url")),
    ("Imaging / investigation", patient.get("imaging_url")),
]

available_documents = [
    (name, url)
    for name, url in documents
    if url and is_valid_url(url)
]

if available_documents:

    for name, url in available_documents:

        st.link_button(
            f"Open {name}",
            url,
            use_container_width=False,
        )

else:

    st.info(
        "No medical-record, referral or imaging links have been added."
    )


if role in ["Doctor", "Rehabilitator", "Meeting Host", "Administrator"]:

    with st.expander("Manage medical record links"):

        with st.form("documents_form"):

            mrr_url = st.text_input(
                "Medical record / MRR URL",
                value=patient.get("mrr_url") or "",
                placeholder="Paste document URL",
            )

            referral_url = st.text_input(
                "Referral URL",
                value=patient.get("referral_url") or "",
                placeholder="Paste referral document URL",
            )

            imaging_url = st.text_input(
                "Imaging / investigation URL",
                value=patient.get("imaging_url") or "",
                placeholder="Paste imaging document URL",
            )

            documents_notes = st.text_area(
                "Document notes",
                value=patient.get("documents_notes") or "",
                height=100,
            )

            save_documents = st.form_submit_button(
                "Save document links",
                type="primary",
                use_container_width=True,
            )

            if save_documents:

                urls = [
                    ("Medical record / MRR", mrr_url),
                    ("Referral", referral_url),
                    ("Imaging", imaging_url),
                ]

                invalid = [
                    name
                    for name, url in urls
                    if url and not is_valid_url(url)
                ]

                if invalid:

                    st.error(
                        "Invalid URL for: " + ", ".join(invalid)
                    )

                else:

                    update_patient(
                        patient["patient_id"],
                        {
                            "mrr_url": mrr_url,
                            "referral_url": referral_url,
                            "imaging_url": imaging_url,
                            "documents_notes": documents_notes,
                        },
                    )

                    st.success("Document links saved.")
                    st.rerun()


# ============================================================
# ADMIN / PATIENT CREATION
# ============================================================

if role == "Administrator":

    st.markdown(
        '<div class="section-heading">Patient administration</div>',
        unsafe_allow_html=True,
    )

    with st.container(border=True):

        st.subheader("Create patient record")

        with st.form("create_patient_form"):

            new_patient_id = st.text_input(
                "Patient ID",
                placeholder="Example: TRP-1002",
            )

            new_patient_name = st.text_input(
                "Patient name",
                placeholder="Full patient name",
            )

            create_submit = st.form_submit_button(
                "Create patient",
                type="primary",
            )

            if create_submit:

                new_patient_id = new_patient_id.strip().upper()
                new_patient_name = new_patient_name.strip()

                if not new_patient_id or not new_patient_name:
                    st.error(
                        "Patient ID and patient name are required."
                    )

                elif get_patient(new_patient_id):
                    st.error(
                        "A patient with this ID already exists."
                    )

                else:

                    create_patient(
                        new_patient_id,
                        new_patient_name,
                    )

                    st.success(
                        f"Patient {new_patient_id} created successfully."
                    )

                    st.session_state.patient_id = new_patient_id

                    st.rerun()


# ============================================================
# SECURITY NOTICE
# ============================================================

st.divider()

st.markdown(
    """
    <div class="clinical-note">
        <strong>Production security requirement:</strong>
        This demonstration uses a local SQLite database and a role selector.
        A production clinical deployment must replace the demo role selector
        with authenticated identity, server-side authorization, encrypted
        transport, audit logging, appropriate access controls, secure document
        storage and applicable healthcare/privacy compliance controls.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="portal-footer">
        TeleRehabilitation Portal • Clinical coordination interface
    </div>
    """,
    unsafe_allow_html=True,
)
