
import streamlit as st
import pandas as pd
import plotly.express as px
import snowflake.connector



from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Healthcare Management System",
    page_icon="🏥",
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title("🏥 Healthcare Management System")
st.caption("Databricks + Streamlit Healthcare Analytics")


@st.cache_resource
def get_connection():

    return snowflake.connector.connect(
        account=st.secrets["account"],
        user=st.secrets["user"],
        password=st.secrets["password"],
        warehouse=st.secrets["warehouse"],
        database=st.secrets["database"],
        schema=st.secrets["schema"]
    )

@st.cache_data(ttl=600)
def load_table(table_name):

    conn = get_connection()

    query = f"""
    SELECT *
    FROM {table_name}
    """

    return pd.read_sql(query, conn)

# ============================================================
# LOAD HEALTHCARE TABLES
# ============================================================

try:

    patients = load_table("patients")

    doctors = load_table("doctors")

    appointments = load_table("appointments")

    treatments = load_table("treatments")

    billing = load_table("billing")

except Exception as e:

    st.error("Unable to load healthcare tables.")

    st.exception(e)

    st.stop()

    raise


# ============================================================
# STANDARDIZE COLUMN NAMES
# ============================================================

patients.columns = [
    c.upper() for c in patients.columns
]

doctors.columns = [
    c.upper() for c in doctors.columns
]

appointments.columns = [
    c.upper() for c in appointments.columns
]

treatments.columns = [
    c.upper() for c in treatments.columns
]

billing.columns = [
    c.upper() for c in billing.columns
]


# ============================================================
# DATE CONVERSION
# ============================================================

date_columns = {
    "patients": [
        "REGISTRATION_DATE",
        "DATE_OF_BIRTH"
    ],
    "appointments": [
        "APPOINTMENT_DATE"
    ],
    "treatments": [
        "TREATMENT_DATE"
    ],
    "billing": [
        "BILL_DATE"
    ]
}


for column in date_columns["patients"]:

    if column in patients.columns:

        patients[column] = pd.to_datetime(
            patients[column],
            errors="coerce"
        )


for column in date_columns["appointments"]:

    if column in appointments.columns:

        appointments[column] = pd.to_datetime(
            appointments[column],
            errors="coerce"
        )


for column in date_columns["treatments"]:

    if column in treatments.columns:

        treatments[column] = pd.to_datetime(
            treatments[column],
            errors="coerce"
        )


for column in date_columns["billing"]:

    if column in billing.columns:

        billing[column] = pd.to_datetime(
            billing[column],
            errors="coerce"
        )

# ============================================================
# NO-SHOW PREDICTION MODEL
# ============================================================

@st.cache_resource
def train_no_show_model(
    appointments,
    patients,
    doctors
):

    # --------------------------------------------------------
    # Select required columns
    # --------------------------------------------------------

    appointment_cols = [
        "APPOINTMENT_ID",
        "PATIENT_ID",
        "DOCTOR_ID",
        "APPOINTMENT_DATE",
        "APPOINTMENT_TIME",
        "REASON_FOR_VISIT",
        "STATUS"
    ]

    patient_cols = [
        "PATIENT_ID",
        "GENDER",
        "DATE_OF_BIRTH",
        "REGISTRATION_DATE",
        "INSURANCE_PROVIDER"
    ]

    doctor_cols = [
        "DOCTOR_ID",
        "SPECIALIZATION",
        "YEARS_EXPERIENCE",
        "HOSPITAL_BRANCH"
    ]

    ml_data = appointments[appointment_cols].merge(
        patients[patient_cols],
        on="PATIENT_ID",
        how="left"
    )

    ml_data = ml_data.merge(
        doctors[doctor_cols],
        on="DOCTOR_ID",
        how="left"
    )

    # --------------------------------------------------------
    # Convert dates
    # --------------------------------------------------------

    ml_data["APPOINTMENT_DATE"] = pd.to_datetime(
        ml_data["APPOINTMENT_DATE"],
        errors="coerce"
    )

    ml_data["DATE_OF_BIRTH"] = pd.to_datetime(
        ml_data["DATE_OF_BIRTH"],
        errors="coerce"
    )

    ml_data["REGISTRATION_DATE"] = pd.to_datetime(
        ml_data["REGISTRATION_DATE"],
        errors="coerce"
    )

    # --------------------------------------------------------
    # Feature Engineering
    # --------------------------------------------------------

    ml_data["Age"] = (
        (
            ml_data["APPOINTMENT_DATE"]
            - ml_data["DATE_OF_BIRTH"]
        ).dt.days / 365.25
    )

    ml_data["Registration_to_Appointment_Days"] = (
        ml_data["APPOINTMENT_DATE"]
        - ml_data["REGISTRATION_DATE"]
    ).dt.days

    ml_data["Appointment_Day"] = (
        ml_data["APPOINTMENT_DATE"]
        .dt.day_name()
    )

    ml_data["Appointment_Month"] = (
        ml_data["APPOINTMENT_DATE"]
        .dt.month
    )

    # Appointment time
    ml_data["Appointment_Hour"] = pd.to_datetime(
        ml_data["APPOINTMENT_TIME"],
        errors="coerce"
    ).dt.hour

    # --------------------------------------------------------
    # Target
    # --------------------------------------------------------

    ml_data["No_Show"] = (
        ml_data["STATUS"]
        .eq("No-show")
        .astype(int)
    )

    # Remove rows with invalid target/date
    ml_data = ml_data.dropna(
        subset=[
            "APPOINTMENT_DATE",
            "No_Show"
        ]
    )

    # Remove invalid negative lead times
    ml_data = ml_data[
        ml_data["Registration_to_Appointment_Days"] >= 0
    ]

    # --------------------------------------------------------
    # Features
    # --------------------------------------------------------

    feature_columns = [
        "GENDER",
        "INSURANCE_PROVIDER",
        "REASON_FOR_VISIT",
        "SPECIALIZATION",
        "HOSPITAL_BRANCH",
        "Appointment_Day",
        "Age",
        "YEARS_EXPERIENCE",
        "Registration_to_Appointment_Days",
        "Appointment_Hour",
        "Appointment_Month"
    ]

    X = ml_data[feature_columns]

    y = ml_data["No_Show"]

    # --------------------------------------------------------
    # Train/Test Split
    # --------------------------------------------------------

    # Chronological split to avoid using future appointments
    ml_data = ml_data.sort_values(
        "APPOINTMENT_DATE"
    )

    split_index = int(
        len(ml_data) * 0.80
    )

    train_data = ml_data.iloc[:split_index]
    test_data = ml_data.iloc[split_index:]

    X_train = train_data[feature_columns]
    y_train = train_data["No_Show"]

    X_test = test_data[feature_columns]
    y_test = test_data["No_Show"]

    # --------------------------------------------------------
    # Feature Types
    # --------------------------------------------------------

    categorical_features = [
        "GENDER",
        "INSURANCE_PROVIDER",
        "REASON_FOR_VISIT",
        "SPECIALIZATION",
        "HOSPITAL_BRANCH",
        "Appointment_Day"
    ]

    numeric_features = [
        "Age",
        "YEARS_EXPERIENCE",
        "Registration_to_Appointment_Days",
        "Appointment_Hour",
        "Appointment_Month"
    ]

    # --------------------------------------------------------
    # Preprocessing
    # --------------------------------------------------------

    numeric_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(
                    strategy="median"
                )
            )
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(
                    strategy="most_frequent"
                )
            ),
            (
                "encoder",
                OneHotEncoder(
                    handle_unknown="ignore"
                )
            )
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "numeric",
                numeric_pipeline,
                numeric_features
            ),
            (
                "categorical",
                categorical_pipeline,
                categorical_features
            )
        ]
    )

    # --------------------------------------------------------
    # Random Forest
    # --------------------------------------------------------

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=5,
        class_weight="balanced",
        random_state=42
    )

    pipeline = Pipeline(
        steps=[
            (
                "preprocessor",
                preprocessor
            ),
            (
                "model",
                model
            )
        ]
    )

    # --------------------------------------------------------
    # Train
    # --------------------------------------------------------

    pipeline.fit(
        X_train,
        y_train
    )

    # --------------------------------------------------------
    # Test
    # --------------------------------------------------------

    predictions = pipeline.predict(
        X_test
    )

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    precision = precision_score(
        y_test,
        predictions,
        zero_division=0
    )

    recall = recall_score(
        y_test,
        predictions,
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        predictions,
        zero_division=0
    )

    cm = confusion_matrix(
        y_test,
        predictions
    )

    metrics = {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "confusion_matrix": cm,
        "test_size": len(y_test),
        "no_show_test": int(y_test.sum())
    }

    return pipeline, metrics

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🏥 Healthcare Analytics")

page = st.sidebar.radio(
    "Select Dashboard",
    [
        "Executive Dashboard",
        "Patient Analysis",
        "Appointment Operations",
        "Doctor & Treatment",
        "Billing & Collections",
        "🤖 No-Show Prediction"
    ]
)


# ============================================================
# EXECUTIVE DASHBOARD
# ============================================================

if page == "Executive Dashboard":

    st.header("📊 Executive Dashboard")

    total_patients = patients["PATIENT_ID"].nunique()

    total_appointments = (
        appointments["APPOINTMENT_ID"].nunique()
    )

    completed_appointments = (
        appointments[
            appointments["STATUS"] == "Completed"
        ]["APPOINTMENT_ID"].nunique()
    )

    total_treatments = (
        treatments["TREATMENT_ID"].nunique()
    )

    total_revenue = billing["AMOUNT"].sum()

    completion_rate = (
        completed_appointments /
        total_appointments * 100
        if total_appointments > 0
        else 0
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Patients",
        f"{total_patients:,}"
    )

    col2.metric(
        "Total Appointments",
        f"{total_appointments:,}"
    )

    col3.metric(
        "Completed Appointments",
        f"{completed_appointments:,}"
    )

    col4, col5, col6 = st.columns(3)

    col4.metric(
        "Total Treatments",
        f"{total_treatments:,}"
    )

    col5.metric(
        "Total Revenue",
        f"₹{total_revenue:,.2f}"
    )

    col6.metric(
        "Completion Rate",
        f"{completion_rate:.2f}%"
    )

    st.divider()

    # Appointment status

    status_df = (
        appointments
        .groupby("STATUS")
        .size()
        .reset_index(name="COUNT")
    )

    fig = px.pie(
        status_df,
        names="STATUS",
        values="COUNT",
        title="Appointment Status Distribution",
        hole=0.45
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # Monthly appointments

    monthly = (
        appointments
        .dropna(subset=["APPOINTMENT_DATE"])
        .assign(
            MONTH=lambda x:
            x["APPOINTMENT_DATE"].dt.to_period("M").astype(str)
        )
        .groupby("MONTH")
        .size()
        .reset_index(name="APPOINTMENTS")
    )

    fig = px.line(
        monthly,
        x="MONTH",
        y="APPOINTMENTS",
        markers=True,
        title="Monthly Appointment Trend"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# PATIENT ANALYSIS
# ============================================================

elif page == "Patient Analysis":

    st.header("👥 Patient Analysis")

    total_patients = patients["PATIENT_ID"].nunique()

    st.metric(
        "Total Patients",
        f"{total_patients:,}"
    )

    col1, col2 = st.columns(2)

    with col1:

        gender_df = (
            patients
            .groupby("GENDER")
            .size()
            .reset_index(name="PATIENTS")
        )

        fig = px.bar(
            gender_df,
            x="GENDER",
            y="PATIENTS",
            title="Patients by Gender"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        if "INSURANCE_PROVIDER" in patients.columns:

            insurance_df = (
                patients
                .groupby("INSURANCE_PROVIDER")
                .size()
                .reset_index(name="PATIENTS")
                .sort_values(
                    "PATIENTS",
                    ascending=False
                )
            )

            fig = px.bar(
                insurance_df,
                x="INSURANCE_PROVIDER",
                y="PATIENTS",
                title="Patients by Insurance Provider"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    st.subheader("Patient Data")

    st.dataframe(
        patients,
        use_container_width=True
    )


# ============================================================
# APPOINTMENT OPERATIONS
# ============================================================

elif page == "Appointment Operations":

    st.header("📅 Appointment Operations")

    total = appointments["APPOINTMENT_ID"].nunique()

    completed = (
        appointments[
            appointments["STATUS"] == "Completed"
        ]["APPOINTMENT_ID"].nunique()
    )

    cancelled = (
        appointments[
            appointments["STATUS"] == "Cancelled"
        ]["APPOINTMENT_ID"].nunique()
    )

    no_show = (
        appointments[
            appointments["STATUS"] == "No-show"
        ]["APPOINTMENT_ID"].nunique()
    )

    cancellation_rate = (
        cancelled / total * 100
        if total > 0 else 0
    )

    no_show_rate = (
        no_show / total * 100
        if total > 0 else 0
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Total Appointments",
        f"{total:,}"
    )

    c2.metric(
        "Completed",
        f"{completed:,}"
    )

    c3.metric(
        "Cancelled",
        f"{cancelled:,}"
    )

    c4, c5, c6 = st.columns(3)

    c4.metric(
        "No-Show",
        f"{no_show:,}"
    )

    c5.metric(
        "Cancellation Rate",
        f"{cancellation_rate:.2f}%"
    )

    c6.metric(
        "No-Show Rate",
        f"{no_show_rate:.2f}%"
    )

    st.divider()

    status_df = (
        appointments
        .groupby("STATUS")
        .size()
        .reset_index(name="APPOINTMENTS")
    )

    fig = px.bar(
        status_df,
        x="STATUS",
        y="APPOINTMENTS",
        title="Appointment Status Analysis",
        text_auto=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # Doctor workload

    if "DOCTOR_ID" in appointments.columns:

        doctor_load = (
            appointments
            .groupby("DOCTOR_ID")
            .size()
            .reset_index(
                name="APPOINTMENTS"
            )
            .sort_values(
                "APPOINTMENTS",
                ascending=False
            )
            .head(10)
        )

        fig = px.bar(
            doctor_load,
            x="DOCTOR_ID",
            y="APPOINTMENTS",
            title="Top 10 Doctors by Appointment Load"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# DOCTOR & TREATMENT
# ============================================================

elif page == "Doctor & Treatment":

    st.header("👨‍⚕️ Doctor & Treatment Dashboard")

    total_doctors = doctors["DOCTOR_ID"].nunique()

    total_treatments = (
        treatments["TREATMENT_ID"].nunique()
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Total Doctors",
        f"{total_doctors:,}"
    )

    c2.metric(
        "Total Treatments",
        f"{total_treatments:,}"
    )

    c3.metric(
        "Total Patients",
        f"{patients['PATIENT_ID'].nunique():,}"
    )

    st.divider()

    # Specialization

    if "SPECIALIZATION" in doctors.columns:

        specialization_df = (
            doctors
            .groupby("SPECIALIZATION")
            .size()
            .reset_index(
                name="DOCTORS"
            )
            .sort_values(
                "DOCTORS",
                ascending=False
            )
        )

        fig = px.bar(
            specialization_df,
            x="SPECIALIZATION",
            y="DOCTORS",
            title="Doctors by Specialization"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # Treatment type

    if "TREATMENT_TYPE" in treatments.columns:

        treatment_df = (
            treatments
            .groupby("TREATMENT_TYPE")
            .size()
            .reset_index(
                name="TREATMENTS"
            )
            .sort_values(
                "TREATMENTS",
                ascending=False
            )
            .head(10)
        )

        fig = px.bar(
            treatment_df,
            x="TREATMENT_TYPE",
            y="TREATMENTS",
            title="Top Treatment Types"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# BILLING & COLLECTIONS
# ============================================================

elif page == "Billing & Collections":

    st.header("💰 Billing & Collections")

    total_billing = billing["AMOUNT"].sum()

    if "PAYMENT_STATUS" in billing.columns:

        # Show actual statuses first

        payment_status_df = (
            billing
            .groupby("PAYMENT_STATUS")["AMOUNT"]
            .sum()
            .reset_index()
        )

        fig = px.bar(
            payment_status_df,
            x="PAYMENT_STATUS",
            y="AMOUNT",
            title="Billing Amount by Payment Status",
            text_auto=".2s"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # Display statuses

        st.subheader("Payment Status")

        st.dataframe(
            payment_status_df,
            use_container_width=True
        )

    c1, c2 = st.columns(2)

    c1.metric(
        "Total Billing",
        f"₹{total_billing:,.2f}"
    )

    c2.metric(
        "Average Bill",
        f"₹{billing['AMOUNT'].mean():,.2f}"
    )

    # Payment method

    if "PAYMENT_METHOD" in billing.columns:

        method_df = (
            billing
            .groupby("PAYMENT_METHOD")
            .size()
            .reset_index(
                name="TRANSACTIONS"
            )
        )

        fig = px.pie(
            method_df,
            names="PAYMENT_METHOD",
            values="TRANSACTIONS",
            title="Payment Method Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.subheader("Billing Data")

    st.dataframe(
        billing,
        use_container_width=True
    )
    # ============================================================
# NO-SHOW PREDICTION
# ============================================================

elif page == "🤖 No-Show Prediction":

    st.header("🤖 Patient No-Show Prediction")

    st.write(
        """
        This model predicts whether a scheduled appointment
        is likely to become a **No-show** based on historical
        patient, appointment, doctor and scheduling information.
        """
    )

    st.info(
        "The prediction is a decision-support output, "
        "not a medical diagnosis."
    )

    # --------------------------------------------------------
    # Train model
    # --------------------------------------------------------

    with st.spinner(
        "Training No-show prediction model..."
    ):

        model, metrics = train_no_show_model(
            appointments,
            patients,
            doctors
        )

    st.success(
        "Random Forest model trained successfully."
    )

    # --------------------------------------------------------
    # Model Metrics
    # --------------------------------------------------------

    st.subheader("📊 Model Performance")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Accuracy",
        f"{metrics['accuracy']:.2%}"
    )

    c2.metric(
        "Precision",
        f"{metrics['precision']:.2%}"
    )

    c3.metric(
        "Recall",
        f"{metrics['recall']:.2%}"
    )

    c4.metric(
        "F1 Score",
        f"{metrics['f1']:.2%}"
    )

    st.caption(
        f"Test records: {metrics['test_size']} | "
        f"Actual no-shows in test set: "
        f"{metrics['no_show_test']}"
    )

    # --------------------------------------------------------
    # Confusion Matrix
    # --------------------------------------------------------

    st.subheader("Confusion Matrix")

    cm = metrics["confusion_matrix"]

    cm_df = pd.DataFrame(
        cm,
        index=[
            "Actual: Not No-show",
            "Actual: No-show"
        ],
        columns=[
            "Predicted: Not No-show",
            "Predicted: No-show"
        ]
    )

    st.dataframe(
        cm_df,
        use_container_width=True
    )

    # --------------------------------------------------------
    # Prediction Form
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "🔮 Predict an Upcoming Appointment"
    )

    col1, col2 = st.columns(2)

    with col1:

        gender_options = sorted(
            patients["GENDER"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        gender = st.selectbox(
            "Gender",
            gender_options
        )

        insurance_options = sorted(
            patients["INSURANCE_PROVIDER"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        insurance = st.selectbox(
            "Insurance Provider",
            insurance_options
        )

        reason_options = sorted(
            appointments["REASON_FOR_VISIT"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        reason = st.selectbox(
            "Reason for Visit",
            reason_options
        )

        specialization_options = sorted(
            doctors["SPECIALIZATION"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        specialization = st.selectbox(
            "Specialization",
            specialization_options
        )

    with col2:

        branch_options = sorted(
            doctors["HOSPITAL_BRANCH"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        branch = st.selectbox(
            "Hospital Branch",
            branch_options
        )

        age = st.number_input(
            "Patient Age",
            min_value=0,
            max_value=120,
            value=30
        )

        experience = st.number_input(
            "Doctor Experience (Years)",
            min_value=0,
            max_value=70,
            value=5
        )

        lead_time = st.number_input(
            "Registration to Appointment Days",
            min_value=0,
            max_value=1000,
            value=7
        )

    appointment_date = st.date_input(
        "Appointment Date"
    )

    appointment_hour = st.slider(
        "Appointment Hour",
        min_value=0,
        max_value=23,
        value=10
    )

    if st.button(
        "🔮 Predict No-show",
        type="primary"
    ):

        prediction_input = pd.DataFrame(
            {
                "GENDER": [gender],
                "INSURANCE_PROVIDER": [insurance],
                "REASON_FOR_VISIT": [reason],
                "SPECIALIZATION": [specialization],
                "HOSPITAL_BRANCH": [branch],
                "Appointment_Day": [
                    pd.Timestamp(
                        appointment_date
                    ).day_name()
                ],
                "Age": [age],
                "YEARS_EXPERIENCE": [
                    experience
                ],
                "Registration_to_Appointment_Days": [
                    lead_time
                ],
                "Appointment_Hour": [
                    appointment_hour
                ],
                "Appointment_Month": [
                    pd.Timestamp(
                        appointment_date
                    ).month
                ]
            }
        )

        prediction = model.predict(
            prediction_input
        )[0]

        probability = model.predict_proba(
            prediction_input
        )[0][1]

        st.divider()

        st.subheader(
            "Prediction Result"
        )

        if prediction == 1:

            st.error(
                "⚠️ Predicted: No-show"
            )

            st.write(
                f"Estimated no-show probability: "
                f"**{probability:.2%}**"
            )

            st.warning(
                "This appointment may warrant "
                "additional reminder or follow-up."
            )

        else:

            st.success(
                "✅ Predicted: Appointment likely to be attended"
            )

            st.write(
                f"Estimated no-show probability: "
                f"**{probability:.2%}**"
            )