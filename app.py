import streamlit as st
import sqlite3
import html
from datetime import datetime, date, time as dt_time
from urllib.parse import urlparse


# ============================================================
# TELE REHABILITATION PORTAL
# Clinical Tele-Rehabilitation Management System
# ============================================================

APP_TITLE = "TeleRehabilitation Portal"
DB_PATH = "telerehabilitation.db"


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="TR",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PROFESSIONAL CLINICAL UI
# ============================================================

st.markdown(
    """
    <style>

    @import url(
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
    );

    html, body, [class*="css"] {
        font-family: "Inter", sans-serif;
    }

    .stApp {
        background: #f5f7fa;
        color: #172033;
    }

    .block-container {
        max-width: 1500px;
        padding-top: 1.2rem;
        padding-bottom: 4rem;
    }

    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #dce2e9;
    }

    section[data-testid="stSidebar"] * {
        color: #172033 !important;
    }

    /* ========================================================
       GLOBAL TYPOGRAPHY
       ======================================================== */

    h1, h2, h3, h4 {
        color: #172033 !important;
        letter-spacing: -0.025em;
    }

    p, label {
        color: #334155;
    }

    /* ========================================================
       HEADER
       ======================================================== */

    .clinical-header {
        background: #ffffff;
        border: 1px solid #dce2e9;
        border-radius: 14px;
        padding: 22px 26px;
        margin-bottom: 18px;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
    }

    .clinical-header-title {
        color: #172033;
        font-size: 29px;
        font-weight: 800;
        line-height: 1.2;
    }

    .clinical-header-subtitle {
        color: #64748b;
        font-size: 14px;
        margin-top: 7px;
    }

    /* ========================================================
       PATIENT CONTEXT
       ======================================================== */

    .patient-context {
        background: #ffffff;
        border: 1px solid #dce2e9;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 22px;
        box-shadow: 0 1px 5px rgba(15, 23, 42, 0.03);
    }

    .patient-context-name {
        color: #172033;
        font-size: 17px;
        font-weight: 700;
    }

    .patient-context-meta {
        color: #64748b;
        font-size: 13px;
        margin-top: 5px;
    }

    /* ========================================================
       CARDS
       ======================================================== */

    .clinical-card {
        background: #ffffff;
        border: 1px solid #dce2e9;
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
    }

    .metric-card {
        background: #ffffff;
        border: 1px solid #dce2e9;
        border-radius: 14px;
        padding: 18px;
        min-height: 112px;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
    }

    .metric-label {
        color: #64748b;
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .metric-value {
        color: #172033;
        font-size: 23px;
        font-weight: 800;
        margin-top: 8px;
        line-height: 1.2;
    }

    .section-title {
        color: #172033;
        font-size: 19px;
        font-weight: 750;
        margin-bottom: 5px;
    }

    .section-description {
        color: #64748b;
        font-size: 13px;
        margin-bottom: 16px;
    }

    /* ========================================================
       STATUS
       ======================================================== */

    .status-row {
        background: #ffffff;
        border: 1px solid #e1e6ec;
        border-radius: 10px;
        padding: 12px 15px;
        margin-bottom: 8px;
    }

    .status-name {
        color: #334155;
        font-weight: 600;
    }

    .status-value {
        color: #64748b;
        font-size: 13px;
        margin-top: 3px;
    }

    .status-complete {
        color: #146c5c;
        font-weight: 700;
    }

    .status-pending {
        color: #8a6416;
        font-weight: 700;
    }

    /* ========================================================
       INFORMATION / WARNING
       ======================================================== */

    .clinical-info {
        background: #f8fafc;
        border: 1px solid #dbe3ec;
        border-radius: 11px;
        padding: 14px 16px;
        margin: 12px 0 18px;
        color: #475569;
        font-size: 13px;
        line-height: 1.6;
    }

    .clinical-warning {
        background: #fffaf0;
        border: 1px solid #ead8a7;
        border-radius: 11px;
        padding: 14px 16px;
        margin: 12px 0 18px;
        color: #6f5316;
        font-size: 13px;
        line-height: 1.6;
    }

    /* ========================================================
       TABLE-LIKE INFORMATION
       ======================================================== */

    .data-label {
        color: #64748b;
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: .04em;
    }

    .data-value {
        color: #172033;
        font-size: 15px;
        font-weight: 600;
        margin-top: 4px;
        margin-bottom: 14px;
    }

    /* ========================================================
       BUTTONS
       ======================================================== */

    div[data-testid="stButton"] > button,
    div[data-testid="stFormSubmitButton"] > button {
        border-radius: 9px;
        min-height: 2.5rem;
        font-weight: 650;
    }

    /* ========================================================
       INPUTS
       ======================================================== */

    div[data-baseweb="input"],
    div[data-baseweb="select"],
    textarea {
        border-radius: 8px !important;
    }

    /* ========================================================
       DIVIDERS
       ======================================================== */

    hr {
        border-color: #e1e6ec !important;
    }

    /* ========================================================
       SMALL TEXT
       ======================================================== */

    .muted {
        color: #64748b;
        font-size: 13px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DATABASE
# ============================================================

def get_db():
    conn = sqlite3.connect(
        DB_PATH,
        check_same_thread=False
    )
    conn.row_factory = sqlite3.Row
    return conn


def init_db():

    conn = get_db()
    cur = conn.cursor()

    # --------------------------------------------------------
    # PATIENTS
    # --------------------------------------------------------

    cur.execute(
        """
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
        """
    )

    # --------------------------------------------------------
    # CLINICAL ASSESSMENTS
    # --------------------------------------------------------

    cur.execute(
        """
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

            FOREIGN KEY(patient_id)
                REFERENCES patients(patient_id)

        )
        """
    )

    # --------------------------------------------------------
    # REHABILITATION PLANS
    # --------------------------------------------------------

    cur.execute(
        """
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

            FOREIGN KEY(patient_id)
                REFERENCES patients(patient_id)

        )
        """
    )

    # --------------------------------------------------------
    # TELECONSULTATION
    # --------------------------------------------------------

    cur.execute(
        """
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

            FOREIGN KEY(patient_id)
                REFERENCES patients(patient_id)

        )
        """
    )

    # --------------------------------------------------------
    # MEDICAL RECORD REFERENCES
    # --------------------------------------------------------

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS records (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            patient_id TEXT NOT NULL,

            record_type TEXT NOT NULL,

            title TEXT NOT NULL,

            url TEXT,

            notes TEXT,

            uploaded_by TEXT,

            created_at TEXT NOT NULL,

            FOREIGN KEY(patient_id)
                REFERENCES patients(patient_id)

        )
        """
    )

    # --------------------------------------------------------
    # DEMO PATIENT
    #
    # IMPORTANT:
    # 28 columns = 28 values.
    #
    # NO fabricated ROM or clinical measurements.
    # --------------------------------------------------------

    existing = cur.execute(
        """
        SELECT patient_id
        FROM patients
        WHERE patient_id = ?
        """,
        ("TRP-1001",)
    ).fetchone()

    if not existing:

        now = datetime.now().isoformat(
            timespec="seconds"
        )

        cur.execute(
            """
            INSERT INTO patients (

                patient_id,
                full_name,
                dob,
                sex,
                country,
                preferred_language,
                phone,
                email,
                emergency_contact,
                diagnosis,
                diagnosis_date,
                affected_region,
                laterality,
                condition_type,
                mechanism,
                medical_history,
                surgery_history,
                medications,
                allergies,
                previous_rehab,
                functional_limitations,
                pain_notes,
                referring_physician,
                assigned_rehabilitator,
                clinical_notes,
                consent_status,
                created_at,
                updated_at

            )

            VALUES (

                ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?

            )
            """,
            (

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
                "Pending",
                now,
                now,

            )
        )

    conn.commit()
    conn.close()


@st.cache_resource
def database_initialized():

    init_db()

    return True


database_initialized()


# ============================================================
# DATABASE HELPERS
# ============================================================

def db_query(
    sql,
    params=(),
    fetchone=False,
    commit=False
):

    conn = get_db()

    cur = conn.cursor()

    cur.execute(
        sql,
        params
    )

    if commit:

        conn.commit()
        conn.close()

        return True

    if fetchone:

        result = cur.fetchone()

    else:

        result = cur.fetchall()

    conn.close()

    return result


def esc(value):

    return html.escape(
        str(value or "")
    )


def valid_url(value):

    if not value:

        return False

    try:

        parsed = urlparse(
            value
        )

        return (
            parsed.scheme in (
                "http",
                "https"
            )
            and bool(
                parsed.netloc
            )
        )

    except Exception:

        return False


def role_can_edit(role):

    return role in (
        "Rehabilitator",
        "Doctor",
        "Administrator"
    )


def get_patient(patient_id):

    return db_query(
        """
        SELECT *
        FROM patients
        WHERE patient_id = ?
        """,
        (patient_id,),
        fetchone=True
    )


def get_assessment(patient_id):

    return db_query(
        """
        SELECT *
        FROM assessments
        WHERE patient_id = ?
        ORDER BY assessment_date DESC, id DESC
        LIMIT 1
        """,
        (patient_id,),
        fetchone=True
    )


def get_plan(patient_id):

    return db_query(
        """
        SELECT *
        FROM rehabilitation_plans
        WHERE patient_id = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (patient_id,),
        fetchone=True
    )


def get_meeting(patient_id):

    return db_query(
        """
        SELECT *
        FROM meetings
        WHERE patient_id = ?
        ORDER BY scheduled_date DESC, id DESC
        LIMIT 1
        """,
        (patient_id,),
        fetchone=True
    )


def get_records(patient_id):

    return db_query(
        """
        SELECT *
        FROM records
        WHERE patient_id = ?
        ORDER BY created_at DESC, id DESC
        """,
        (patient_id,)
    )


def profile_completion(patient):

    fields = [

        "full_name",
        "dob",
        "sex",
        "country",
        "preferred_language",
        "diagnosis",
        "affected_region",
        "laterality",
        "assigned_rehabilitator"

    ]

    completed = sum(
        bool(
            patient[field]
        )
        for field in fields
    )

    return round(
        completed /
        len(fields) *
        100
    )


def save_patient(data):

    now = datetime.now().isoformat(
        timespec="seconds"
    )

    db_query(
        """
        UPDATE patients SET

            full_name = ?,
            dob = ?,
            sex = ?,
            country = ?,
            preferred_language = ?,
            phone = ?,
            email = ?,
            emergency_contact = ?,
            diagnosis = ?,
            diagnosis_date = ?,
            affected_region = ?,
            laterality = ?,
            condition_type = ?,
            mechanism = ?,
            medical_history = ?,
            surgery_history = ?,
            medications = ?,
            allergies = ?,
            previous_rehab = ?,
            functional_limitations = ?,
            pain_notes = ?,
            referring_physician = ?,
            assigned_rehabilitator = ?,
            clinical_notes = ?,
            consent_status = ?,
            updated_at = ?

        WHERE patient_id = ?

        """,
        (

            data["full_name"],
            data["dob"],
            data["sex"],
            data["country"],
            data["preferred_language"],
            data["phone"],
            data["email"],
            data["emergency_contact"],
            data["diagnosis"],
            data["diagnosis_date"],
            data["affected_region"],
            data["laterality"],
            data["condition_type"],
            data["mechanism"],
            data["medical_history"],
            data["surgery_history"],
            data["medications"],
            data["allergies"],
            data["previous_rehab"],
            data["functional_limitations"],
            data["pain_notes"],
            data["referring_physician"],
            data["assigned_rehabilitator"],
            data["clinical_notes"],
            data["consent_status"],
            now,
            data["patient_id"]

        ),
        commit=True
    )


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
        "## TeleRehabilitation"
    )

    st.caption(
        "Clinical care coordination portal"
    )

    st.divider()

    # --------------------------------------------------------
    # Role
    # --------------------------------------------------------

    selected_role = st.selectbox(
        "Portal role",
        [
            "Patient",
            "Rehabilitator",
            "Doctor",
            "Administrator"
        ],
        index=[
            "Patient",
            "Rehabilitator",
            "Doctor",
            "Administrator"
        ].index(
            st.session_state.role
        )
    )

    st.session_state.role = selected_role

    # --------------------------------------------------------
    # Patient
    # --------------------------------------------------------

    if selected_role == "Patient":

        patient_choices = [
            "TRP-1001"
        ]

    else:

        patient_rows = db_query(
            """
            SELECT patient_id
            FROM patients
            ORDER BY patient_id
            """
        )

        patient_choices = [
            row["patient_id"]
            for row in patient_rows
        ]

    if not patient_choices:

        st.error(
            "No patient records available."
        )

        st.stop()

    selected_patient = st.selectbox(
        "Patient record",
        patient_choices,
        index=(
            patient_choices.index(
                st.session_state.patient_id
            )
            if st.session_state.patient_id
            in patient_choices
            else 0
        )
    )

    st.session_state.patient_id = (
        selected_patient
    )

    st.divider()

    st.caption(
        "Clinical roles should be connected to "
        "authenticated identity and server-side "
        "authorization in production."
    )


# ============================================================
# LOAD PATIENT
# ============================================================

patient = get_patient(
    st.session_state.patient_id
)

if not patient:

    st.error(
        "Patient record could not be found."
    )

    st.stop()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="clinical-header">

        <div class="clinical-header-title">
            TeleRehabilitation Portal
        </div>

        <div class="clinical-header-subtitle">
            Clinical care coordination and
            tele-rehabilitation management
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# PATIENT CONTEXT
# ============================================================

st.markdown(
    f"""
    <div class="patient-context">

        <div class="patient-context-name">
            {esc(patient["full_name"])}
        </div>

        <div class="patient-context-meta">
            Patient ID: {esc(patient["patient_id"])}
            &nbsp;&nbsp;•&nbsp;&nbsp;
            Current portal role:
            {esc(st.session_state.role)}
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# MAIN NAVIGATION
# ============================================================

tabs = st.tabs(
    [
        "Overview",
        "Clinical Profile",
        "Clinical Assessment",
        "Rehabilitation Plan",
        "Teleconsultation",
        "Medical Records",
    ]
)


# ============================================================
# TAB 1 — OVERVIEW
# ============================================================

with tabs[0]:

    st.title(
        "Clinical Overview"
    )

    st.caption(
        "Current status of the patient's "
        "tele-rehabilitation care record."
    )

    completion = profile_completion(
        patient
    )

    assessment = get_assessment(
        patient["patient_id"]
    )

    plan = get_plan(
        patient["patient_id"]
    )

    meeting = get_meeting(
        patient["patient_id"]
    )

    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    Profile completion
                </div>

                <div class="metric-value">
                    {completion}%
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:

        affected = (
            patient["affected_region"]
            or "Not recorded"
        )

        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    Affected region
                </div>

                <div class="metric-value">
                    {esc(affected)}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:

        assessment_status = (
            "Recorded"
            if assessment
            else "Not assessed"
        )

        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    Clinical assessment
                </div>

                <div class="metric-value">
                    {assessment_status}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:

        consultation_status = (
            "Scheduled"
            if meeting
            else "Not scheduled"
        )

        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    Teleconsultation
                </div>

                <div class="metric-value">
                    {consultation_status}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    st.markdown(
        "<br>",
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # PROFILE COMPLETION
    # --------------------------------------------------------

    st.subheader(
        "Patient record completion"
    )

    status_items = [

        (
            "Patient information",
            bool(patient["full_name"])
        ),

        (
            "Date of birth",
            bool(patient["dob"])
        ),

        (
            "Country",
            bool(patient["country"])
        ),

        (
            "Preferred language",
            bool(
                patient[
                    "preferred_language"
                ]
            )
        ),

        (
            "Diagnosis",
            bool(patient["diagnosis"])
        ),

        (
            "Affected organ / body region",
            bool(
                patient[
                    "affected_region"
                ]
            )
        ),

        (
            "Assigned rehabilitator",
            bool(
                patient[
                    "assigned_rehabilitator"
                ]
            )
        ),

        (
            "Clinical assessment",
            bool(assessment)
        ),

        (
            "Rehabilitation plan",
            bool(plan)
        ),

        (
            "Teleconsultation",
            bool(meeting)
        ),

    ]


    cols = st.columns(2)

    for index, (
        label,
        complete
    ) in enumerate(status_items):

        with cols[index % 2]:

            status_text = (
                "Complete"
                if complete
                else "Pending"
            )

            status_class = (
                "status-complete"
                if complete
                else "status-pending"
            )

            st.markdown(
                f"""
                <div class="status-row">

                    <div class="status-name">
                        {esc(label)}
                    </div>

                    <div class="status-value">
                        <span class="{status_class}">
                            {status_text}
                        </span>
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


    # --------------------------------------------------------
    # NO FABRICATED CLINICAL VALUES
    # --------------------------------------------------------

    if (
        not patient["diagnosis"]
        or not patient["affected_region"]
    ):

        st.markdown(
            """
            <div class="clinical-warning">

                <strong>
                    Clinical assessment not yet established
                </strong>

                <br><br>

                Diagnosis and the affected organ/body
                region must be documented before clinical
                measurements are interpreted.

                The portal does not generate or invent
                range-of-motion, pain, strength or
                functional values.

            </div>
            """,
            unsafe_allow_html=True
        )


    # --------------------------------------------------------
    # CURRENT CARE
    # --------------------------------------------------------

    st.subheader(
        "Current care"
    )

    care_col1, care_col2 = st.columns(2)

    with care_col1:

        st.markdown(
            '<div class="clinical-card">',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-title">Diagnosis</div>',
            unsafe_allow_html=True
        )

        st.write(
            patient["diagnosis"]
            or "Not documented"
        )

        st.markdown(
            '<div class="section-title">Affected region</div>',
            unsafe_allow_html=True
        )

        region_text = (
            patient["affected_region"]
            or "Not documented"
        )

        if patient["laterality"]:

            region_text += (
                " · "
                + patient["laterality"]
            )

        st.write(
            region_text
        )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )


    with care_col2:

        st.markdown(
            '<div class="clinical-card">',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-title">Assigned rehabilitator</div>',
            unsafe_allow_html=True
        )

        st.write(
            patient[
                "assigned_rehabilitator"
            ]
            or "Not assigned"
        )

        st.markdown(
            '<div class="section-title">Preferred language</div>',
            unsafe_allow_html=True
        )

        st.write(
            patient[
                "preferred_language"
            ]
            or "Not recorded"
        )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )


# ============================================================
# TAB 2 — CLINICAL PROFILE
# ============================================================

with tabs[1]:

    st.title(
        "Clinical Profile"
    )

    st.caption(
        "Complete patient information and clinical "
        "history for coordinated rehabilitation care."
    )

    editable = role_can_edit(
        st.session_state.role
    )


    if not editable:

        st.info(
            "Patient access is read-only. Clinical "
            "information is managed by the authorized "
            "care team."
        )


    with st.form(
        "clinical_profile_form"
    ):

        # ----------------------------------------------------
        # DEMOGRAPHICS
        # ----------------------------------------------------

        st.subheader(
            "Patient information"
        )

        c1, c2, c3 = st.columns(3)

        with c1:

            full_name = st.text_input(
                "Full name",
                value=patient[
                    "full_name"
                ] or ""
            )

            dob = st.text_input(
                "Date of birth",
                value=patient[
                    "dob"
                ] or "",
                placeholder="YYYY-MM-DD"
            )

            sex_options = [
                "",
                "Female",
                "Male",
                "Intersex",
                "Prefer not to say"
            ]

            current_sex = (
                patient["sex"]
                if patient["sex"]
                in sex_options
                else ""
            )

            sex = st.selectbox(
                "Sex",
                sex_options,
                index=sex_options.index(
                    current_sex
                )
            )


        with c2:

            country = st.text_input(
                "Country",
                value=patient[
                    "country"
                ] or ""
            )

            language_options = [
                "English",
                "Urdu",
                "Arabic",
                "French",
                "Spanish",
                "German",
                "Chinese",
                "Other"
            ]

            current_language = (
                patient[
                    "preferred_language"
                ]
                if patient[
                    "preferred_language"
                ] in language_options
                else "English"
            )

            preferred_language = st.selectbox(
                "Preferred language",
                language_options,
                index=language_options.index(
                    current_language
                )
            )

            phone = st.text_input(
                "Phone",
                value=patient[
                    "phone"
                ] or ""
            )


        with c3:

            email = st.text_input(
                "Email",
                value=patient[
                    "email"
                ] or ""
            )

            emergency_contact = st.text_input(
                "Emergency contact",
                value=patient[
                    "emergency_contact"
                ] or ""
            )

            consent_options = [
                "Pending",
                "Approved",
                "Declined",
                "Expired"
            ]

            current_consent = (
                patient[
                    "consent_status"
                ]
                if patient[
                    "consent_status"
                ] in consent_options
                else "Pending"
            )

            consent_status = st.selectbox(
                "Consent / authorization",
                consent_options,
                index=consent_options.index(
                    current_consent
                )
            )


        st.divider()


        # ----------------------------------------------------
        # DIAGNOSIS
        # ----------------------------------------------------

        st.subheader(
            "Diagnosis and affected body region"
        )

        st.markdown(
            """
            <div class="clinical-info">

                This section establishes the clinical
                context required for assessment.

                Range-of-motion and other measurements
                must not be displayed as if they were
                known when diagnosis or affected anatomy
                has not been documented.

            </div>
            """,
            unsafe_allow_html=True
        )


        c1, c2 = st.columns(2)

        with c1:

            diagnosis = st.text_area(
                "Diagnosis",
                value=patient[
                    "diagnosis"
                ] or "",
                height=110,
                placeholder=(
                    "Document the diagnosis provided "
                    "by the authorized clinician."
                )
            )

            diagnosis_date = st.text_input(
                "Diagnosis date",
                value=patient[
                    "diagnosis_date"
                ] or "",
                placeholder="YYYY-MM-DD"
            )


        with c2:

            affected_region = st.text_input(
                "Affected organ / body region",
                value=patient[
                    "affected_region"
                ] or "",
                placeholder=(
                    "e.g. right knee, lumbar spine, "
                    "left shoulder"
                )
            )

            laterality_options = [
                "",
                "Left",
                "Right",
                "Bilateral",
                "Not applicable"
            ]

            current_laterality = (
                patient[
                    "laterality"
                ]
                if patient[
                    "laterality"
                ] in laterality_options
                else ""
            )

            laterality = st.selectbox(
                "Laterality",
                laterality_options,
                index=laterality_options.index(
                    current_laterality
                )
            )


        c1, c2 = st.columns(2)

        with c1:

            condition_type = st.text_input(
                "Condition / injury type",
                value=patient[
                    "condition_type"
                ] or ""
            )

        with c2:

            mechanism = st.text_input(
                "Cause / mechanism",
                value=patient[
                    "mechanism"
                ] or ""
            )


        st.divider()


        # ----------------------------------------------------
        # MEDICAL HISTORY
        # ----------------------------------------------------

        st.subheader(
            "Medical history"
        )

        c1, c2 = st.columns(2)

        with c1:

            medical_history = st.text_area(
                "Relevant medical history",
                value=patient[
                    "medical_history"
                ] or "",
                height=120
            )

            surgery_history = st.text_area(
                "Surgery / procedure history",
                value=patient[
                    "surgery_history"
                ] or "",
                height=120
            )

            medications = st.text_area(
                "Current medications",
                value=patient[
                    "medications"
                ] or "",
                height=120
            )


        with c2:

            allergies = st.text_area(
                "Allergies",
                value=patient[
                    "allergies"
                ] or "",
                height=120
            )

            previous_rehab = st.text_area(
                "Previous rehabilitation",
                value=patient[
                    "previous_rehab"
                ] or "",
                height=120
            )

            functional_limitations = st.text_area(
                "Functional limitations",
                value=patient[
                    "functional_limitations"
                ] or "",
                height=120
            )


        pain_notes = st.text_area(
            "Patient-reported pain and symptoms",
            value=patient[
                "pain_notes"
            ] or "",
            height=100
        )


        st.divider()


        # ----------------------------------------------------
        # CARE TEAM
        # ----------------------------------------------------

        st.subheader(
            "Care team"
        )

        c1, c2 = st.columns(2)

        with c1:

            referring_physician = st.text_input(
                "Referring physician",
                value=patient[
                    "referring_physician"
                ] or ""
            )

        with c2:

            assigned_rehabilitator = st.text_input(
                "Assigned rehabilitator",
                value=patient[
                    "assigned_rehabilitator"
                ] or ""
            )


        clinical_notes = st.text_area(
            "Clinical notes",
            value=patient[
                "clinical_notes"
            ] or "",
            height=120
        )


        submitted = st.form_submit_button(
            "Save clinical profile",
            type="primary",
            disabled=not editable
        )


        if submitted and editable:

            if not full_name.strip():

                st.error(
                    "Full name is required."
                )

            else:

                save_patient(
                    {

                        "patient_id":
                            patient[
                                "patient_id"
                            ],

                        "full_name":
                            full_name.strip(),

                        "dob":
                            dob.strip(),

                        "sex":
                            sex,

                        "country":
                            country.strip(),

                        "preferred_language":
                            preferred_language,

                        "phone":
                            phone.strip(),

                        "email":
                            email.strip(),

                        "emergency_contact":
                            emergency_contact.strip(),

                        "diagnosis":
                            diagnosis.strip(),

                        "diagnosis_date":
                            diagnosis_date.strip(),

                        "affected_region":
                            affected_region.strip(),

                        "laterality":
                            laterality,

                        "condition_type":
                            condition_type.strip(),

                        "mechanism":
                            mechanism.strip(),

                        "medical_history":
                            medical_history.strip(),

                        "surgery_history":
                            surgery_history.strip(),

                        "medications":
                            medications.strip(),

                        "allergies":
                            allergies.strip(),

                        "previous_rehab":
                            previous_rehab.strip(),

                        "functional_limitations":
                            functional_limitations.strip(),

                        "pain_notes":
                            pain_notes.strip(),

                        "referring_physician":
                            referring_physician.strip(),

                        "assigned_rehabilitator":
                            assigned_rehabilitator.strip(),

                        "clinical_notes":
                            clinical_notes.strip(),

                        "consent_status":
                            consent_status,

                    }
                )

                st.success(
                    "Clinical profile saved successfully."
                )

                st.rerun()


# ============================================================
# TAB 3 — CLINICAL ASSESSMENT
# ============================================================

with tabs[2]:

    st.title(
        "Clinical Assessment"
    )

    st.caption(
        "Clinical measurements are recorded by the "
        "authorized clinician after assessment."
    )


    assessment = get_assessment(
        patient["patient_id"]
    )


    # --------------------------------------------------------
    # REQUIRE CLINICAL CONTEXT
    # --------------------------------------------------------

    if (
        not patient["diagnosis"]
        or not patient["affected_region"]
    ):

        st.markdown(
            """
            <div class="clinical-warning">

                <strong>
                    Assessment cannot be interpreted yet.
                </strong>

                <br><br>

                The patient's diagnosis and affected
                organ/body region have not been fully
                documented.

                <br><br>

                The system will not invent or estimate
                range of motion, pain, strength or
                functional measurements.

            </div>
            """,
            unsafe_allow_html=True
        )


    # --------------------------------------------------------
    # LATEST ASSESSMENT
    # --------------------------------------------------------

    if assessment:

        st.subheader(
            "Latest recorded assessment"
        )

        c1, c2, c3, c4 = st.columns(4)


        with c1:

            if (
                assessment["rom_value"]
                is not None
            ):

                rom_display = (
                    f'{assessment["rom_value"]} '
                    f'{assessment["rom_unit"]}'
                )

            else:

                rom_display = (
                    "Not recorded"
                )

            st.markdown(
                f"""
                <div class="metric-card">

                    <div class="metric-label">
                        Range of motion
                    </div>

                    <div class="metric-value">
                        {esc(rom_display)}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


        with c2:

            if (
                assessment["pain_score"]
                is not None
            ):

                pain_display = (
                    f'{assessment["pain_score"]}/10'
                )

            else:

                pain_display = (
                    "Not recorded"
                )

            st.markdown(
                f"""
                <div class="metric-card">

                    <div class="metric-label">
                        Pain score
                    </div>

                    <div class="metric-value">
                        {esc(pain_display)}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


        with c3:

            strength = (
                assessment[
                    "strength_grade"
                ]
                or "Not recorded"
            )

            st.markdown(
                f"""
                <div class="metric-card">

                    <div class="metric-label">
                        Strength
                    </div>

                    <div class="metric-value">
                        {esc(strength)}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


        with c4:

            gait = (
                assessment[
                    "gait_status"
                ]
                or "Not recorded"
            )

            st.markdown(
                f"""
                <div class="metric-card">

                    <div class="metric-label">
                        Gait
                    </div>

                    <div class="metric-value">
                        {esc(gait)}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


        st.caption(
            f'Assessment date: '
            f'{assessment["assessment_date"]} · '
            f'Assessed by: '
            f'{assessment["assessed_by"] or "Not specified"}'
        )


        if assessment["notes"]:

            st.markdown(
                '<div class="clinical-card">',
                unsafe_allow_html=True
            )

            st.markdown(
                "#### Assessment notes"
            )

            st.write(
                assessment["notes"]
            )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )


    else:

        st.info(
            "No clinical assessment has been recorded "
            "for this patient."
        )


    # --------------------------------------------------------
    # RECORD ASSESSMENT
    # --------------------------------------------------------

    if role_can_edit(
        st.session_state.role
    ):

        st.divider()

        st.subheader(
            "Record clinical assessment"
        )

        with st.form(
            "assessment_form"
        ):

            assessment_date = st.date_input(
                "Assessment date",
                value=date.today()
            )


            c1, c2, c3 = st.columns(3)


            with c1:

                rom_value = st.number_input(
                    "Measured range of motion",
                    min_value=0.0,
                    max_value=360.0,
                    value=0.0,
                    step=0.5,
                    help=(
                        "Enter the actual measurement "
                        "obtained by the clinician. "
                        "Leave at zero when not assessed."
                    )
                )

                rom_unit = st.selectbox(
                    "ROM unit",
                    [
                        "degrees"
                    ]
                )


            with c2:

                pain_score = st.number_input(
                    "Pain score",
                    min_value=0.0,
                    max_value=10.0,
                    value=0.0,
                    step=0.5,
                    help=(
                        "Enter a documented patient-reported "
                        "or clinical pain score."
                    )
                )

                strength_grade = st.text_input(
                    "Strength grade",
                    placeholder="Example: 4/5"
                )


            with c3:

                gait_status = st.selectbox(
                    "Gait status",
                    [
                        "",
                        "Independent",
                        "Assisted",
                        "Limited",
                        "Non-ambulatory",
                        "Not assessed"
                    ]
                )

                functional_score = st.number_input(
                    "Functional score",
                    min_value=0.0,
                    value=0.0,
                    step=0.5,
                    help=(
                        "Enter a score only when a "
                        "documented functional scale "
                        "is being used."
                    )
                )


            assessment_notes = st.text_area(
                "Assessment notes",
                height=120
            )


            assessed_by = st.text_input(
                "Assessed by",
                value=patient[
                    "assigned_rehabilitator"
                ] or ""
            )


            save_assessment = st.form_submit_button(
                "Save clinical assessment",
                type="primary"
            )


            if save_assessment:

                if (
                    not patient["diagnosis"]
                    or not patient[
                        "affected_region"
                    ]
                ):

                    st.error(
                        "Document diagnosis and affected "
                        "body region before recording "
                        "clinical measurements."
                    )

                elif not assessed_by.strip():

                    st.error(
                        "Assessed by is required."
                    )

                else:

                    db_query(
                        """
                        INSERT INTO assessments (

                            patient_id,
                            assessment_date,
                            rom_value,
                            rom_unit,
                            pain_score,
                            strength_grade,
                            gait_status,
                            functional_score,
                            notes,
                            assessed_by

                        )

                        VALUES (
                            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                        )
                        """,
                        (

                            patient[
                                "patient_id"
                            ],

                            assessment_date.isoformat(),

                            (
                                rom_value
                                if rom_value > 0
                                else None
                            ),

                            (
                                rom_unit
                                if rom_value > 0
                                else None
                            ),

                            (
                                pain_score
                                if pain_score > 0
                                else None
                            ),

                            (
                                strength_grade.strip()
                                or None
                            ),

                            (
                                gait_status
                                or None
                            ),

                            (
                                functional_score
                                if functional_score > 0
                                else None
                            ),

                            assessment_notes.strip(),

                            assessed_by.strip(),

                        ),
                        commit=True
                    )

                    st.success(
                        "Clinical assessment saved."
                    )

                    st.rerun()


    else:

        st.info(
            "Only authorized clinical roles can "
            "record assessment measurements."
        )


# ============================================================
# TAB 4 — REHABILITATION PLAN
# ============================================================

with tabs[3]:

    st.title(
        "Rehabilitation Plan"
    )

    st.caption(
        "The rehabilitation plan is assigned by the "
        "clinical team and presented to the patient "
        "through the portal."
    )


    plan = get_plan(
        patient["patient_id"]
    )


    # --------------------------------------------------------
    # CURRENT PLAN
    # --------------------------------------------------------

    if plan:

        st.markdown(
            f"""
            <div class="clinical-card">

                <div class="data-label">
                    Current phase
                </div>

                <div class="data-value">
                    {esc(plan["phase"])}
                    ·
                    {esc(plan["phase_name"])}
                </div>

                <div class="data-label">
                    Rehabilitation plan
                </div>

                <div class="data-value">
                    {esc(plan["plan_title"])}
                </div>

                <div class="data-label">
                    Status
                </div>

                <div class="data-value">
                    {esc(plan["status"])}
                </div>

                <div class="data-label">
                    Assigned by
                </div>

                <div class="data-value">
                    {esc(plan["assigned_by"])}
                </div>

                <div class="data-label">
                    Start date
                </div>

                <div class="data-value">
                    {esc(plan["start_date"])}
                </div>

                <div class="data-label">
                    End date
                </div>

                <div class="data-value">
                    {esc(plan["end_date"])}
                </div>

                <div class="data-label">
                    Clinical plan
                </div>

                <div class="data-value">
                    {esc(plan["instructions"])}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.info(
            "No rehabilitation plan has been assigned."
        )


    # --------------------------------------------------------
    # PHASE OVERVIEW
    # --------------------------------------------------------

    st.subheader(
        "Rehabilitation pathway"
    )

    phases = [

        (
            "Phase 1",
            "Initial Assessment",
            "Clinical assessment and care planning"
        ),

        (
            "Phase 2",
            "Mobility and Strength",
            "Clinician-directed mobility and strengthening"
        ),

        (
            "Phase 3",
            "Functional Training",
            "Progressive functional rehabilitation"
        ),

        (
            "Phase 4",
            "Return to Activity",
            "Clinician-approved return to activity"
        ),

    ]


    for phase, name, description in phases:

        is_current = (
            plan
            and plan["phase"] == phase
        )

        border_text = (
            "Current phase"
            if is_current
            else "Planned phase"
        )

        st.markdown(
            f"""
            <div class="clinical-card">

                <div class="section-title">
                    {esc(phase)}
                    ·
                    {esc(name)}
                </div>

                <div class="muted">
                    {esc(description)}
                </div>

                <div class="muted"
                     style="margin-top:8px;">
                    {border_text}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # --------------------------------------------------------
    # ASSIGN PLAN
    # --------------------------------------------------------

    if role_can_edit(
        st.session_state.role
    ):

        st.divider()

        st.subheader(
            "Assign rehabilitation plan"
        )

        with st.form(
            "plan_form"
        ):

            c1, c2 = st.columns(2)

            with c1:

                phase = st.selectbox(
                    "Phase",
                    [
                        "Phase 1",
                        "Phase 2",
                        "Phase 3",
                        "Phase 4"
                    ]
                )

                phase_names = {

                    "Phase 1":
                        "Initial Assessment",

                    "Phase 2":
                        "Mobility and Strength",

                    "Phase 3":
                        "Functional Training",

                    "Phase 4":
                        "Return to Activity",

                }

                phase_name = st.text_input(
                    "Phase name",
                    value=phase_names[
                        phase
                    ]
                )

                plan_title = st.text_input(
                    "Plan title"
                )


            with c2:

                start_date = st.date_input(
                    "Start date",
                    value=date.today()
                )

                end_date = st.date_input(
                    "End date",
                    value=date.today()
                )

                assigned_by = st.text_input(
                    "Assigned by",
                    value=patient[
                        "assigned_rehabilitator"
                    ] or ""
                )


            instructions = st.text_area(
                "Clinical rehabilitation plan",
                height=150,
                placeholder=(
                    "Enter the clinician-approved "
                    "rehabilitation plan."
                )
            )


            save_plan = st.form_submit_button(
                "Assign rehabilitation plan",
                type="primary"
            )


            if save_plan:

                if not plan_title.strip():

                    st.error(
                        "Plan title is required."
                    )

                elif not assigned_by.strip():

                    st.error(
                        "Assigned clinician is required."
                    )

                elif end_date < start_date:

                    st.error(
                        "End date cannot be earlier "
                        "than start date."
                    )

                else:

                    db_query(
                        """
                        INSERT INTO rehabilitation_plans (

                            patient_id,
                            phase,
                            phase_name,
                            plan_title,
                            instructions,
                            start_date,
                            end_date,
                            assigned_by,
                            status

                        )

                        VALUES (
                            ?, ?, ?, ?, ?, ?, ?, ?, ?
                        )
                        """,
                        (

                            patient[
                                "patient_id"
                            ],

                            phase,

                            phase_name.strip(),

                            plan_title.strip(),

                            instructions.strip(),

                            start_date.isoformat(),

                            end_date.isoformat(),

                            assigned_by.strip(),

                            "Assigned",

                        ),
                        commit=True
                    )

                    st.success(
                        "Rehabilitation plan assigned."
                    )

                    st.rerun()


# ============================================================
# TAB 5 — TELECONSULTATION
# ============================================================

with tabs[4]:

    st.title(
        "Teleconsultation"
    )

    st.caption(
        "Teleconsultation links are supplied by the "
        "authorized doctor, rehabilitator or meeting host."
    )


    meeting = get_meeting(
        patient["patient_id"]
    )


    # --------------------------------------------------------
    # SCHEDULED MEETING
    # --------------------------------------------------------

    if meeting:

        c1, c2 = st.columns(
            [1.4, 1]
        )


        with c1:

            st.markdown(
                f"""
                <div class="clinical-card">

                    <div class="section-title">
                        Scheduled teleconsultation
                    </div>

                    <div class="data-label">
                        Provider
                    </div>

                    <div class="data-value">
                        {esc(
                            meeting["provider_name"]
                        )}
                    </div>

                    <div class="data-label">
                        Provider role
                    </div>

                    <div class="data-value">
                        {esc(
                            meeting["provider_role"]
                        )}
                    </div>

                    <div class="data-label">
                        Platform
                    </div>

                    <div class="data-value">
                        {esc(
                            meeting["meeting_provider"]
                            or "Not specified"
                        )}
                    </div>

                    <div class="data-label">
                        Date
                    </div>

                    <div class="data-value">
                        {esc(
                            meeting["scheduled_date"]
                        )}
                    </div>

                    <div class="data-label">
                        Time
                    </div>

                    <div class="data-value">
                        {esc(
                            meeting["scheduled_time"]
                        )}
                    </div>

                    <div class="data-label">
                        Time zone
                    </div>

                    <div class="data-value">
                        {esc(
                            meeting["timezone"]
                        )}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


        with c2:

            st.markdown(
                '<div class="clinical-card">',
                unsafe_allow_html=True
            )

            st.subheader(
                "Join consultation"
            )

            if (
                meeting["meeting_url"]
                and valid_url(
                    meeting["meeting_url"]
                )
            ):

                st.link_button(
                    "Join Teleconsultation",
                    meeting[
                        "meeting_url"
                    ],
                    type="primary",
                    use_container_width=True
                )

            else:

                st.warning(
                    "The meeting host has not supplied "
                    "a valid meeting link."
                )


            if meeting["meeting_id"]:

                st.write(
                    f'**Meeting ID:** '
                    f'{meeting["meeting_id"]}'
                )


            if meeting["notes"]:

                st.markdown(
                    "#### Meeting notes"
                )

                st.write(
                    meeting["notes"]
                )


            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )


    else:

        st.info(
            "No teleconsultation is currently scheduled."
        )


    # --------------------------------------------------------
    # MEETING MANAGEMENT
    # --------------------------------------------------------

    if role_can_edit(
        st.session_state.role
    ):

        st.divider()

        st.subheader(
            "Schedule teleconsultation"
        )

        with st.form(
            "meeting_form"
        ):

            c1, c2 = st.columns(2)

            with c1:

                provider_name = st.text_input(
                    "Doctor / rehabilitator / meeting host",
                    value=patient[
                        "assigned_rehabilitator"
                    ] or ""
                )

                provider_role = st.selectbox(
                    "Provider role",
                    [
                        "Rehabilitator",
                        "Doctor",
                        "Meeting Host"
                    ]
                )

                meeting_provider = st.text_input(
                    "Meeting platform",
                    placeholder=(
                        "Example: Zoom, Microsoft Teams, "
                        "Google Meet"
                    )
                )

                meeting_url = st.text_input(
                    "Meeting URL",
                    placeholder=(
                        "Paste the meeting link supplied "
                        "by the host"
                    )
                )


            with c2:

                scheduled_date = st.date_input(
                    "Scheduled date",
                    value=date.today()
                )

                scheduled_time = st.time_input(
                    "Scheduled time",
                    value=dt_time(
                        16,
                        30
                    )
                )

                timezone = st.text_input(
                    "Time zone",
                    value="Asia/Karachi"
                )

                meeting_id = st.text_input(
                    "Meeting ID / reference"
                )


            meeting_notes = st.text_area(
                "Meeting notes",
                height=110
            )


            save_meeting = st.form_submit_button(
                "Save teleconsultation",
                type="primary"
            )


            if save_meeting:

                if not provider_name.strip():

                    st.error(
                        "Provider / host name is required."
                    )

                elif not meeting_url.strip():

                    st.error(
                        "Meeting URL is required."
                    )

                elif not valid_url(
                    meeting_url.strip()
                ):

                    st.error(
                        "Enter a valid HTTP or HTTPS "
                        "meeting URL."
                    )

                else:

                    db_query(
                        """
                        INSERT INTO meetings (

                            patient_id,
                            provider_name,
                            provider_role,
                            meeting_provider,
                            meeting_url,
                            meeting_id,
                            scheduled_date,
                            scheduled_time,
                            timezone,
                            notes

                        )

                        VALUES (
                            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                        )
                        """,
                        (

                            patient[
                                "patient_id"
                            ],

                            provider_name.strip(),

                            provider_role,

                            meeting_provider.strip(),

                            meeting_url.strip(),

                            meeting_id.strip(),

                            scheduled_date.isoformat(),

                            scheduled_time.strftime(
                                "%H:%M"
                            ),

                            timezone.strip(),

                            meeting_notes.strip(),

                        ),
                        commit=True
                    )

                    st.success(
                        "Teleconsultation scheduled."
                    )

                    st.rerun()


# ============================================================
# TAB 6 — MEDICAL RECORDS
# ============================================================

with tabs[5]:

    st.title(
        "Medical Records"
    )

    st.caption(
        "Clinical documents and imaging references "
        "associated with this patient."
    )


    records = get_records(
        patient["patient_id"]
    )


    # --------------------------------------------------------
    # EXISTING RECORDS
    # --------------------------------------------------------

    if records:

        for record in records:

            with st.container(
                border=True
            ):

                c1, c2 = st.columns(
                    [3, 1]
                )


                with c1:

                    st.markdown(
                        f"""
                        <div class="section-title">
                            {esc(record["title"])}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.caption(
                        f'{record["record_type"]} · '
                        f'Added '
                        f'{record["created_at"]}'
                        ' · '
                        f'By '
                        f'{record["uploaded_by"] or "Care team"}'
                    )

                    if record["notes"]:

                        st.write(
                            record["notes"]
                        )


                with c2:

                    if (
                        record["url"]
                        and valid_url(
                            record["url"]
                        )
                    ):

                        st.link_button(
                            "Open medical record",
                            record["url"],
                            use_container_width=True
                        )

                    else:

                        st.caption(
                            "No external document link"
                        )


    else:

        st.info(
            "No medical records have been added."
        )


    # --------------------------------------------------------
    # ADD RECORD
    # --------------------------------------------------------

    if role_can_edit(
        st.session_state.role
    ):

        st.divider()

        st.subheader(
            "Add medical record"
        )

        st.markdown(
            """
            <div class="clinical-info">

                The portal stores a reference to the
                authorized medical document.

                Examples include MRI, X-ray, CT,
                ultrasound, referral letters, discharge
                summaries and clinical reports.

                Paste the secure document link supplied
                by the authorized provider.

            </div>
            """,
            unsafe_allow_html=True
        )


        with st.form(
            "record_form"
        ):

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
                        "Clinical report",
                        "Other"
                    ]
                )

                title = st.text_input(
                    "Record title"
                )


            with c2:

                url = st.text_input(
                    "Secure document URL",
                    placeholder=(
                        "Paste authorized document link"
                    )
                )

                uploaded_by = st.text_input(
                    "Added by",
                    value=patient[
                        "assigned_rehabilitator"
                    ] or ""
                )


            notes = st.text_area(
                "Record notes",
                height=110
            )


            save_record = st.form_submit_button(
                "Add medical record",
                type="primary"
            )


            if save_record:

                if not title.strip():

                    st.error(
                        "Record title is required."
                    )

                elif (
                    url.strip()
                    and not valid_url(
                        url.strip()
                    )
                ):

                    st.error(
                        "Enter a valid HTTP or HTTPS "
                        "document URL."
                    )

                else:

                    db_query(
                        """
                        INSERT INTO records (

                            patient_id,
                            record_type,
                            title,
                            url,
                            notes,
                            uploaded_by,
                            created_at

                        )

                        VALUES (
                            ?, ?, ?, ?, ?, ?, ?
                        )
                        """,
                        (

                            patient[
                                "patient_id"
                            ],

                            record_type,

                            title.strip(),

                            url.strip(),

                            notes.strip(),

                            uploaded_by.strip(),

                            datetime.now().isoformat(
                                timespec="seconds"
                            ),

                        ),
                        commit=True
                    )

                    st.success(
                        "Medical record added."
                    )

                    st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "TeleRehabilitation Portal · "
    "Clinical workflow interface"
)

st.caption(
    "Production deployment requires authenticated "
    "identity, server-side authorization, encrypted "
    "storage, audit logging, secure document handling "
    "and applicable healthcare/privacy compliance."
)
