import streamlit as st
import pandas as pd
import sqlite3
import requests
import base64
from datetime import date



st.set_page_config(
    page_title="AI Health Prediction App",
    layout="wide"
)


def set_background(image_file):
    try:
        with open(image_file, "rb") as image:
            encoded = base64.b64encode(image.read()).decode()

        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/png;base64,{encoded}");
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}

            .block-container {{
                background-color: rgba(255,255,255,0.90);
                padding: 2rem;
                border-radius: 15px;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except:
        pass

set_background(r"C:\Users\shiva\Downloads\ChatGPT Image Jun 1, 2026, 11_42_17 AM.png")



st.markdown("""
<h1 style='text-align:center;color:#003366;'>
🏥 AI Health Prediction Application
</h1>

<h3 style='text-align:center;color:#0066cc;'>
Gokul Infocare
</h3>

<h5 style='text-align:center;color:#444444;'>
MIRA - Medical Intelligence Robotic Automation
</h5>
""", unsafe_allow_html=True)

st.info(
    "AI-Powered Healthcare Prediction System with CRUD Operations and External API Integration"
)



conn = sqlite3.connect(
    "patients.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS patients(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT,
    dob TEXT,
    email TEXT,
    glucose REAL,
    haemoglobin REAL,
    cholesterol REAL,
    remarks TEXT
)
""")

conn.commit()


def predict_health(glucose, haemoglobin, cholesterol):

    if glucose > 140:
        return "High Diabetes Risk"

    elif cholesterol > 240:
        return "Possible Heart Disease Risk"

    elif haemoglobin < 12:
        return "Possible Anemia Risk"

    else:
        return "Normal Health Condition"


# EXTERNAL API


def get_ai_remark(name):

    try:

        response = requests.get(
            f"https://api.agify.io/?name={name}",
            timeout=5
        )

        data = response.json()

        age = data.get("age")

        return f"AI Estimated Age: {age}"

    except:
        return "AI Prediction Unavailable"

# SIDEBAR


st.sidebar.title("🏥 Gokul Infocare")
st.sidebar.caption("Healthcare AI Platform")

menu = [
    "Add Patient",
    "View Patients",
    "Update Patient",
    "Delete Patient"
]

choice = st.sidebar.selectbox(
    "Navigation",
    menu
)


# ADD PATIENT


if choice == "Add Patient":

    st.subheader("➕ Add Patient")

    full_name = st.text_input("Full Name")

    dob = st.date_input(
        "Date of Birth",
        value=date(2000, 1, 1),
        min_value=date(1950, 1, 1),
        max_value=date.today()
    )

    email = st.text_input("Email Address")

    glucose = st.number_input(
        "Glucose",
        min_value=0.0
    )

    haemoglobin = st.number_input(
        "Haemoglobin",
        min_value=0.0
    )

    cholesterol = st.number_input(
        "Cholesterol",
        min_value=0.0
    )

    if st.button("Save Patient"):

        if full_name.strip() == "":
            st.error("Full Name is required")

        elif "@" not in email or "." not in email:
            st.error("Enter valid email address")

        else:

            health_result = predict_health(
                glucose,
                haemoglobin,
                cholesterol
            )

            ai_result = get_ai_remark(
                full_name
            )

            remarks = (
                f"{health_result} | {ai_result}"
            )

            cursor.execute("""
            INSERT INTO patients(
                full_name,
                dob,
                email,
                glucose,
                haemoglobin,
                cholesterol,
                remarks
            )
            VALUES(?,?,?,?,?,?,?)
            """,
            (
                full_name,
                str(dob),
                email,
                glucose,
                haemoglobin,
                cholesterol,
                remarks
            ))

            conn.commit()

            st.success(
                "Patient Added Successfully"
            )


# VIEW PATIENTS


elif choice == "View Patients":

    st.subheader("📋 Patient Records")

    search = st.text_input(
        "Search Patient"
    )

    if search:

        cursor.execute("""
        SELECT * FROM patients
        WHERE full_name LIKE ?
        """,
        ('%' + search + '%',))

    else:

        cursor.execute(
            "SELECT * FROM patients"
        )

    data = cursor.fetchall()

    df = pd.DataFrame(
        data,
        columns=[
            "ID",
            "Full Name",
            "DOB",
            "Email",
            "Glucose",
            "Haemoglobin",
            "Cholesterol",
            "Remarks"
        ]
    )

    total_patients = len(df)

    high_risk = len(
        df[
            df["Remarks"].str.contains(
                "Risk",
                na=False
            )
        ]
    )

    normal = total_patients - high_risk

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "👨‍⚕️ Total Patients",
        total_patients
    )

    col2.metric(
        "⚠️ High Risk",
        high_risk
    )

    col3.metric(
        "✅ Normal",
        normal
    )

    st.dataframe(
        df,
        use_container_width=True
    )


# UPDATE PATIENT


elif choice == "Update Patient":

    st.subheader("✏️ Update Patient")

    patient_id = st.number_input(
        "Enter Patient ID",
        min_value=1,
        step=1
    )

    cursor.execute(
        "SELECT * FROM patients WHERE id=?",
        (patient_id,)
    )

    patient = cursor.fetchone()

    if patient:

        full_name = st.text_input(
            "Full Name",
            patient[1]
        )

        glucose = st.number_input(
            "Glucose",
            value=float(patient[4])
        )

        haemoglobin = st.number_input(
            "Haemoglobin",
            value=float(patient[5])
        )

        cholesterol = st.number_input(
            "Cholesterol",
            value=float(patient[6])
        )

        if st.button("Update"):

            health_result = predict_health(
                glucose,
                haemoglobin,
                cholesterol
            )

            ai_result = get_ai_remark(
                full_name
            )

            remarks = (
                f"{health_result} | {ai_result}"
            )

            cursor.execute("""
            UPDATE patients
            SET
            full_name=?,
            glucose=?,
            haemoglobin=?,
            cholesterol=?,
            remarks=?
            WHERE id=?
            """,
            (
                full_name,
                glucose,
                haemoglobin,
                cholesterol,
                remarks,
                patient_id
            ))

            conn.commit()

            st.success(
                "Patient Updated Successfully"
            )


# DELETE PATIENT


elif choice == "Delete Patient":

    st.subheader("🗑️ Delete Patient")

    patient_id = st.number_input(
        "Enter Patient ID To Delete",
        min_value=1,
        step=1
    )

    if st.button("Delete"):

        cursor.execute(
            "DELETE FROM patients WHERE id=?",
            (patient_id,)
        )

        conn.commit()

        st.success(
            "Patient Deleted Successfully"
        )