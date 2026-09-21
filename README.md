# Healthcare-Management-System

# 🏥 Healthcare Management System & Analytics

An end-to-end **Healthcare Analytics and Predictive Modeling** project designed to transform healthcare operational data into actionable business insights. The project integrates **Snowflake, Databricks, PySpark, SQL, Power BI, Python, and Streamlit** to perform data ingestion, data quality assessment, descriptive analysis, diagnostic analysis, predictive modeling, and interactive reporting.

---

## 📌 Project Overview

Healthcare organizations generate large volumes of operational data related to patients, appointments, doctors, treatments, and billing. However, raw transactional data alone does not provide sufficient visibility into operational efficiency, patient behavior, doctor workload, treatment activity, and financial performance.

This project develops an analytics solution that converts healthcare transactional data into meaningful insights through:

* Data ingestion and storage
* Data quality auditing
* Data cleaning and validation
* Descriptive analytics
* Diagnostic analytics
* Predictive analytics
* Interactive Power BI dashboards
* Appointment no-show prediction
* Business recommendations

The solution helps healthcare stakeholders understand **what happened, why it happened, what may happen next, and what actions can be taken.**

---

# 🎯 Business Context

Healthcare organizations need to efficiently manage:

* Patient appointments
* Doctor workload
* Treatment activity
* Billing and collections
* Patient attendance
* Operational performance

Missed appointments can reduce operational efficiency and create unused appointment capacity. At the same time, delayed collections, uneven doctor workloads, and differences in treatment volumes can affect overall healthcare operations.

The organization therefore requires a centralized analytics solution that can provide visibility into:

> **Patient → Appointment → Doctor → Treatment → Billing**

The project addresses this requirement by building an integrated healthcare analytics platform.

---

# ❗ Problem Statement

The healthcare organization currently has transactional data distributed across multiple datasets covering patients, appointments, doctors, treatments, and billing.

The key business challenges are:

1. Limited visibility into overall healthcare operations.
2. Difficulty monitoring appointment completion and no-show rates.
3. Difficulty identifying doctor workload patterns.
4. Limited visibility into treatment activity and treatment trends.
5. Difficulty monitoring billing, collections, and outstanding amounts.
6. Data quality issues across healthcare transactions.
7. Lack of predictive capability for identifying patients who may miss appointments.
8. Lack of a centralized dashboard for management decision-making.

### Project Objective

Build an end-to-end analytics solution that:

* Integrates healthcare datasets.
* Validates data quality.
* Provides operational and financial insights.
* Identifies important business patterns.
* Predicts potential appointment no-shows.
* Provides interactive dashboards for stakeholders.
* Supports data-driven decision-making.

---

# 👥 Stakeholders

## 1. Hospital Management / Executives

Interested in:

* Overall patient volume
* Appointment performance
* Revenue
* Collections
* Treatment activity
* Operational trends

### Key Questions

* How is the healthcare organization performing?
* How many patients and appointments are being handled?
* What is the completion rate?
* How much revenue is generated?
* What are the major operational trends?

---

## 2. Appointment / Operations Team

Interested in:

* Appointment volume
* Completed appointments
* Cancellations
* No-shows
* Doctor workload
* Appointment trends

### Key Questions

* Which doctors have the highest appointment workload?
* What percentage of appointments are cancelled?
* What is the no-show rate?
* When are appointment volumes highest?

---

## 3. Doctors / Clinical Management

Interested in:

* Patient volume
* Appointment completion
* Treatment volume
* Doctor workload
* Specialization-level performance

### Key Questions

* How many patients are being handled?
* Which specializations have higher patient demand?
* What is the appointment completion pattern?
* How does treatment volume vary across doctors?

---

## 4. Finance / Billing Team

Interested in:

* Billing amount
* Collections
* Outstanding amount
* Payment status
* Payment methods
* Revenue trends

### Key Questions

* How much has been billed?
* How much has been collected?
* What amount remains outstanding?
* Which areas generate higher revenue?

---

# 📋 Business Requirements

The analytics solution should provide:

### Patient Analytics

* Total patients
* Patient demographics
* Gender distribution
* Registration trends
* Patient volume

### Appointment Analytics

* Total appointments
* Completed appointments
* Scheduled appointments
* Cancelled appointments
* No-show appointments
* Completion rate
* Cancellation rate
* No-show rate
* Appointment trends

### Doctor Analytics

* Total doctors
* Doctor workload
* Patient volume by doctor
* Appointments by doctor
* Specialization analysis
* Doctor experience analysis

### Treatment Analytics

* Total treatments
* Treatment volume
* Treatment trends
* Treatment type analysis
* Treatment cost analysis

### Financial Analytics

* Total billing amount
* Amount collected
* Outstanding amount
* Collection rate
* Average bill amount
* Payment status analysis
* Payment method analysis

### Predictive Analytics

Develop a machine learning model to predict whether a patient is likely to miss a scheduled appointment.

---

# 🗂️ Data Availability

The project contains **five relational datasets/tables**.

| Table        | Purpose                                          |
| ------------ | ------------------------------------------------ |
| APPOINTMENTS | Patient appointment information                  |
| PATIENTS     | Patient demographic and registration information |
| DOCTORS      | Doctor information and specialization            |
| TREATMENTS   | Treatment information                            |
| BILLING      | Billing and payment information                  |

---

# 📊 Data Dictionary

## APPOINTMENTS

| Column           | Description                   |
| ---------------- | ----------------------------- |
| appointment_id   | Unique appointment identifier |
| patient_id       | Patient identifier            |
| doctor_id        | Doctor identifier             |
| appointment_date | Date of appointment           |
| appointment_time | Appointment time              |
| reason_for_visit | Reason for appointment        |
| status           | Appointment status            |

### Appointment Status

* Scheduled
* Completed
* Cancelled
* No-show

---

## PATIENTS

| Column             | Description               |
| ------------------ | ------------------------- |
| patient_id         | Unique patient identifier |
| first_name         | Patient first name        |
| last_name          | Patient last name         |
| gender             | Patient gender            |
| date_of_birth      | Patient date of birth     |
| contact_number     | Patient contact           |
| address            | Patient address           |
| registration_date  | Patient registration date |
| insurance_provider | Insurance provider        |
| insurance_number   | Insurance identifier      |
| email              | Patient email             |

---

## DOCTORS

| Column           | Description              |
| ---------------- | ------------------------ |
| doctor_id        | Unique doctor identifier |
| first_name       | Doctor first name        |
| last_name        | Doctor last name         |
| specialization   | Medical specialization   |
| phone_number     | Doctor phone number      |
| years_experience | Doctor experience        |
| hospital_branch  | Hospital branch          |
| email            | Doctor email             |

---

## TREATMENTS

| Column         | Description                 |
| -------------- | --------------------------- |
| treatment_id   | Unique treatment identifier |
| appointment_id | Related appointment         |
| treatment_type | Type of treatment           |
| description    | Treatment description       |
| cost           | Treatment cost              |
| treatment_date | Treatment date              |

---

## BILLING

| Column         | Description            |
| -------------- | ---------------------- |
| bill_id        | Unique bill identifier |
| patient_id     | Patient identifier     |
| treatment_id   | Related treatment      |
| bill_date      | Billing date           |
| amount         | Billing amount         |
| payment_method | Payment method         |
| payment_status | Payment status         |

---

# 🔗 Data Relationships

The project uses a relational data model.

```text
                         ┌─────────────────┐
                         │    PATIENTS     │
                         │─────────────────│
                         │ PK patient_id   │
                         └────────┬────────┘
                                  │
                                  │ 1:M
                                  ▼
                       ┌────────────────────┐
                       │   APPOINTMENTS     │
                       │────────────────────│
                       │ PK appointment_id │
                       │ FK patient_id     │
                       │ FK doctor_id      │
                       └──────┬───────┬─────┘
                              │       │
                         M:1  │       │ 1:M
                              ▼       ▼
                    ┌─────────────┐ ┌─────────────────┐
                    │   DOCTORS   │ │   TREATMENTS    │
                    │─────────────│ │─────────────────│
                    │ PK doctor_id│ │ PK treatment_id │
                    └─────────────┘ │ FK appointment  │
                                    └────────┬────────┘
                                             │
                                             │ 1:M
                                             ▼
                                    ┌────────────────┐
                                    │    BILLING     │
                                    │────────────────│
                                    │ PK bill_id     │
                                    │ FK patient_id  │
                                    │ FK treatment_id│
                                    └────────────────┘
```

### Key Relationships

```text
PATIENTS
   │
   └── PATIENT_ID → APPOINTMENTS.PATIENT_ID

DOCTORS
   │
   └── DOCTOR_ID → APPOINTMENTS.DOCTOR_ID

APPOINTMENTS
   │
   └── APPOINTMENT_ID → TREATMENTS.APPOINTMENT_ID

TREATMENTS
   │
   └── TREATMENT_ID → BILLING.TREATMENT_ID

PATIENTS
   │
   └── PATIENT_ID → BILLING.PATIENT_ID
```

---

# 🏗️ Technology Stack

## Data Storage & Warehousing

* **Snowflake**
* SQL
* Snowflake schemas and tables
* Data staging
* Data quality auditing

## Data Engineering & Processing

* **Databricks**
* **PySpark**
* Spark SQL
* Data transformation
* Data validation

## Programming & Analytics

* **Python**
* Pandas
* NumPy
* Scikit-learn
* Matplotlib / visualization libraries

## Business Intelligence

* **Microsoft Power BI**
* DAX
* Power Query
* Interactive dashboards
* KPI reporting

## Application

* **Streamlit**
* Python
* Interactive predictive analytics application

## Version Control

* Git
* GitHub

---

# 🔄 End-to-End Project Architecture

```text
                 RAW HEALTHCARE DATA
                         │
                         ▼
                  ┌──────────────┐
                  │   Snowflake  │
                  └──────┬───────┘
                         │
                         ▼
                  ┌──────────────┐
                  │  Databricks  │
                  │   PySpark    │
                  └──────┬───────┘
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
      Data Quality             Data Analysis
             │                       │
             └───────────┬───────────┘
                         ▼
               Descriptive Analysis
                         │
                         ▼
                Diagnostic Analysis
                         │
                         ▼
                Predictive Analysis
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
          Power BI              Streamlit
         Dashboards          ML Prediction App
              │                     │
              └──────────┬──────────┘
                         ▼
                Business Insights
                         │
                         ▼
              Recommendations
                         │
                         ▼
                Business Impact
```

---

# 🧹 Data Quality Analysis

Before analysis, the datasets were evaluated for common data quality problems.

## 1. Completeness

Checked:

* Missing patient IDs
* Missing doctor IDs
* Missing appointment dates
* Missing treatment IDs
* Missing billing values
* Missing important demographic fields

---

## 2. Uniqueness

Checked whether primary keys contain duplicates:

```sql
SELECT appointment_id, COUNT(*)
FROM appointments
GROUP BY appointment_id
HAVING COUNT(*) > 1;
```

Similar checks were performed for:

* patient_id
* doctor_id
* treatment_id
* bill_id

---

## 3. Referential Integrity

Verified relationships such as:

```text
Appointment → Patient
Appointment → Doctor
Treatment → Appointment
Billing → Treatment
Billing → Patient
```

This ensures that foreign-key values correspond to valid records.

---

## 4. Date Consistency

A specific quality issue was identified where some appointment dates occurred before patient registration dates.

Example validation:

```sql
SELECT
    a.appointment_id,
    a.patient_id,
    p.registration_date,
    a.appointment_date
FROM appointments a
JOIN patients p
    ON a.patient_id = p.patient_id
WHERE a.appointment_date < p.registration_date;
```

This identified **28 records** requiring investigation.

The issue should not be silently overwritten. The appropriate approach is to:

1. Investigate the source records.
2. Determine whether registration or appointment dates are incorrect.
3. Correct the source data when the true value is known.
4. Otherwise flag or exclude invalid records from lead-time analysis.
5. Document the data-quality decision.

---

# 📈 Types of Analysis

The project performs four major levels of analytics.

---

# 1️⃣ Descriptive Analysis

### Objective

Understand **what happened** in the healthcare organization.

### Patient Analysis

* Total patients
* Gender distribution
* Registration trends
* Patient demographics
* Insurance provider distribution

### Appointment Analysis

* Total appointments
* Completed appointments
* Scheduled appointments
* Cancelled appointments
* No-show appointments
* Appointment trends
* Appointment status distribution

### Doctor Analysis

* Number of doctors
* Patients handled by doctors
* Appointment volume
* Specialization distribution
* Doctor workload

### Treatment Analysis

* Total treatments
* Treatment types
* Treatment trends
* Treatment costs
* Treatment volume by specialization

### Financial Analysis

* Total billing
* Collection amount
* Outstanding amount
* Average bill amount
* Payment method distribution
* Payment status distribution

---

# 2️⃣ Diagnostic Analysis

### Objective

Understand **why certain patterns occurred**.

Examples:

* Why are no-show rates high?
* Which patient groups have higher appointment absence?
* Which doctors have higher appointment workloads?
* Which specializations generate greater treatment activity?
* Which areas contribute more revenue?
* Which payment statuses contribute to outstanding amounts?
* Are appointment volumes concentrated on specific days?
* Is treatment activity associated with particular specializations?

Diagnostic analysis uses:

* Drill-down analysis
* Segmentation
* Correlation analysis
* Comparative analysis
* Trend analysis
* Cross-filtering
* Root-cause investigation

---

# 3️⃣ Predictive Analysis

## Appointment No-Show Prediction

The predictive component estimates whether a patient may miss a scheduled appointment.

### Target Variable

```text
No-show = 1
Other appointment outcomes = 0
```

The appointment `STATUS` itself is **not used as a predictive feature**, because it represents the outcome and would cause target leakage.

### Potential Features

* Gender
* Patient age
* Insurance provider
* Registration-to-appointment days
* Appointment day
* Appointment month
* Appointment hour
* Reason for visit
* Doctor specialization
* Doctor experience
* Hospital branch
* Historical appointment count
* Historical completed appointments
* Historical no-show behavior

Only information available **before the appointment** should be used for prediction.

---

# 🤖 Machine Learning Models

The project evaluates classification models such as:

### Logistic Regression

Used as a baseline classification model.

### Random Forest Classifier

Used to capture nonlinear relationships between patient, appointment, doctor, and scheduling characteristics.

### Evaluation Metrics

Because no-shows can represent a minority class, accuracy alone is not sufficient.

The model is evaluated using:

* Accuracy
* Precision
* Recall
* F1 Score
* ROC-AUC
* Confusion Matrix

Special attention is given to **No-show recall**, because identifying potential missed appointments can help operations teams take preventive action.

---

# 📊 Predictive Model Results

The available dataset contains approximately:

```text
Total records: 200
No-show = 52
Other outcomes = 148
```

A chronological train/test split was used to avoid using future records to predict earlier records.

### Random Forest

```text
Accuracy: 71.79%
Overall F1: 63.98%

No-show Precision: 50.00%
No-show Recall: 9.09%
No-show F1: 15.38%
```

### Logistic Regression

```text
Accuracy: 43.59%
Overall F1: 46.25%

No-show Precision: 17.65%
No-show Recall: 27.27%
No-show F1: 21.43%
```

### Interpretation

The results demonstrate that overall accuracy does not necessarily indicate good performance on the minority no-show class.

The current dataset is relatively small, and the test set contains only a limited number of no-show observations. Therefore, the model should be considered a **proof of concept rather than a production-ready prediction system**.

Further improvement should focus on:

* More historical data
* Better patient behavioral features
* More balanced training data
* Feature engineering
* Hyperparameter tuning
* Threshold optimization
* Cross-validation

---

# 📊 Power BI Dashboards

The project contains four major Power BI dashboards.

---

# Dashboard 1 — Executive Dashboard

### KPIs

* Total Patients
* Total Appointments
* Completed Appointments
* Revenue
* Collection Rate
* Total Treatments
* Outstanding Amount

### Visualizations

* Monthly Patient & Appointment Trend
* Revenue & Collection Trend
* Patient Volume by Specialization
* Appointment Status Distribution
* Revenue by Specialization
* Treatment Trend

### Slicers

* Date
* Specialization
* Hospital Branch
* Doctor
* Appointment Status
* Gender
* Payment Status

### Purpose

Provides management with a high-level view of overall healthcare performance.

---

# Dashboard 2 — Appointment Operations

### KPIs

* Total Appointments
* Completed Appointments
* Scheduled Appointments
* Cancelled Appointments
* Cancellation Rate
* No-show Rate

### Visualizations

* Appointment Trend by Month
* Appointment Status Analysis
* Appointments by Specialization
* Appointments by Hospital Branch
* Appointments by Day of Week
* Doctor-wise Appointment Load
* Registration-to-Appointment Lead Time

### Slicers

* Date
* Specialization
* Hospital Branch
* Doctor
* Appointment Status
* Patient

### Purpose

Helps the operations team monitor appointment efficiency and identify attendance patterns.

---

# Dashboard 3 — Doctor & Treatment Analytics

### KPIs

* Total Doctors
* Active Doctors
* Total Patients Treated
* Completed Treatments
* Average Patients per Doctor
* Average Appointment-to-Treatment Days

### Visualizations

* Doctor-wise Patient Volume
* Doctor-wise Appointment Completion
* Specialization-wise Treatment Volume
* Top Treatment Types
* Treatment Trend
* Doctor Workload Distribution
* Doctor Performance Scatter Plot

### Slicers

* Date
* Specialization
* Doctor
* Treatment Type
* Gender
* Age Group
* Appointment Status

### Purpose

Provides visibility into doctor workload, patient demand, and treatment activity.

---

# Dashboard 4 — Billing & Collections

### KPIs

* Total Billing Amount
* Total Amount Collected
* Outstanding Amount
* Collection Rate
* Average Bill Amount
* Total Transactions

### Visualizations

* Monthly Billing & Collection Trend
* Payment Status Distribution
* Revenue by Specialization
* Revenue by Payment Method
* Outstanding Amount by Specialization
* Top High-Value Patients/Bills

### Slicers

* Date
* Specialization
* Doctor
* Payment Status
* Payment Method
* Patient

### Purpose

Helps finance teams monitor billing performance, collections, and outstanding amounts.

---

# 💡 Key Business Insights

The project enables stakeholders to identify insights such as:

### Patient Insights

* Patient volume can be segmented by demographic characteristics.
* Registration patterns help identify periods of higher patient acquisition.
* Insurance-provider distributions provide visibility into patient coverage patterns.

### Appointment Insights

* Appointment status analysis identifies completed, cancelled, scheduled, and no-show volumes.
* No-show analysis can identify opportunities for appointment reminders.
* Appointment trends can highlight periods of higher operational demand.

### Doctor Insights

* Doctor-wise appointment volumes reveal workload distribution.
* Specialization-level analysis helps identify areas with higher patient demand.
* Doctor experience can be compared with workload and treatment activity.

### Treatment Insights

* Treatment trends identify frequently performed treatments.
* Treatment costs provide visibility into treatment-level financial activity.
* Specialization-level treatment analysis supports resource planning.

### Financial Insights

* Billing and collection trends provide visibility into financial performance.
* Outstanding amounts can highlight collection opportunities.
* Payment method analysis helps understand transaction patterns.

---

# 🎯 Business Recommendations

## 1. Reduce Appointment No-Shows

Use predictive no-show scores to identify appointments that may require additional reminders.

Possible actions:

* Automated SMS reminders
* Email reminders
* Confirmation calls for high-risk appointments
* Easy appointment rescheduling

---

## 2. Improve Doctor Workload Management

Monitor doctor-wise appointment volumes and workload distribution.

Potential actions:

* Optimize appointment scheduling
* Redistribute workload where appropriate
* Identify high-demand specializations
* Adjust appointment slots according to demand

---

## 3. Improve Appointment Planning

Analyze appointment trends by:

* Month
* Day
* Specialization
* Doctor
* Hospital branch

This can help operations teams plan resources according to demand patterns.

---

## 4. Improve Revenue Collection

Monitor:

* Outstanding amount
* Payment status
* Collection rate
* Billing trends

Potential actions include:

* Automated payment reminders
* Follow-up on overdue payments
* Digital payment options
* Collection monitoring dashboards

---

## 5. Improve Data Quality

Establish automated data-quality checks for:

* Duplicate IDs
* Missing values
* Invalid dates
* Referential integrity
* Invalid status values
* Negative financial values
* Date sequence violations

---

# 📈 Business Impact

The analytics solution can support healthcare organizations by improving:

### Operational Visibility

Centralized dashboards provide a single view of patient, appointment, doctor, treatment, and billing activity.

### Appointment Efficiency

No-show and cancellation analysis helps operations teams identify opportunities to improve appointment utilization.

### Resource Planning

Doctor and specialization analysis supports better workload and resource planning.

### Financial Monitoring

Billing and collection dashboards provide visibility into revenue and outstanding amounts.

### Data-Driven Decision Making

Stakeholders can use interactive dashboards instead of relying only on manual reports.

### Predictive Decision Support

The no-show prediction model provides a foundation for proactive appointment management.

---

# 🔮 Future Recommendations

## 1. Increase Dataset Size

The current predictive dataset is relatively small. A larger historical dataset would improve model reliability.

---

## 2. Add Patient Behavioral Features

Future versions can include:

* Previous no-show count
* Previous cancellation count
* Previous completed appointment count
* Historical attendance rate
* Time since previous appointment

These features should be calculated using only historical information available before each appointment.

---

## 3. Improve Machine Learning

Future modeling can include:

* XGBoost
* Gradient Boosting
* Hyperparameter optimization
* Cross-validation
* Feature selection
* Probability threshold optimization
* Model explainability using SHAP

---

## 4. Real-Time Appointment Monitoring

Future architecture could support near-real-time data ingestion and monitoring.

```text
Hospital System
      ↓
Real-Time Data
      ↓
Databricks
      ↓
ML Prediction
      ↓
Streamlit / Power BI
      ↓
Operational Action
```

---

## 5. Automated Alerts

Create automated alerts for:

* High no-show risk
* Increasing cancellation rate
* High outstanding billing
* Unusual appointment volume
* Data-quality failures

---

## 6. Advanced Patient Analytics

Future versions could analyze:

* Patient retention
* Patient segmentation
* Repeat visits
* Treatment patterns
* Insurance utilization
* Patient lifetime value

---

# 🔐 Data Governance & Security

Healthcare data can contain sensitive information. A production implementation should include:

* Role-based access control
* Data encryption
* Secure credentials
* Restricted access to personally identifiable information
* Audit logging
* Data masking where appropriate
* Secure API/database connections
* Appropriate healthcare privacy and regulatory controls

The project uses healthcare-style data for analytics and demonstration purposes and should not be treated as a production clinical system without appropriate governance and validation.

---

# 📌 Key Metrics / KPIs

| KPI                           | Purpose                            |
| ----------------------------- | ---------------------------------- |
| Total Patients                | Measures patient population        |
| Total Appointments            | Measures appointment volume        |
| Completed Appointments        | Measures completed visits          |
| Completion Rate               | Measures appointment completion    |
| Cancellation Rate             | Measures cancellations             |
| No-Show Rate                  | Measures missed appointments       |
| Total Treatments              | Measures treatment activity        |
| Total Revenue                 | Measures billing activity          |
| Collection Rate               | Measures collection efficiency     |
| Outstanding Amount            | Measures unpaid billing            |
| Average Bill Amount           | Measures average transaction value |
| Patients per Doctor           | Indicates workload                 |
| Appointment-to-Treatment Days | Measures treatment timing          |

---

# 🧮 Important DAX Measures

### Total Patients

```DAX
Total Patients =
DISTINCTCOUNT(PATIENTS[PATIENT_ID])
```

### Total Appointments

```DAX
Total Appointments =
DISTINCTCOUNT(APPOINTMENTS[APPOINTMENT_ID])
```

### Completed Appointments

```DAX
Completed Appointments =
CALCULATE(
    DISTINCTCOUNT(APPOINTMENTS[APPOINTMENT_ID]),
    APPOINTMENTS[STATUS] = "Completed"
)
```

### No-Show Appointments

```DAX
No-Show Appointments =
CALCULATE(
    DISTINCTCOUNT(APPOINTMENTS[APPOINTMENT_ID]),
    APPOINTMENTS[STATUS] = "No-show"
)
```

### No-Show Rate

```DAX
No-Show Rate % =
DIVIDE(
    [No-Show Appointments],
    [Total Appointments],
    0
)
```

### Cancellation Rate

```DAX
Cancellation Rate % =
DIVIDE(
    [Cancelled Appointments],
    [Total Appointments],
    0
)
```

### Total Revenue

```DAX
Total Revenue =
SUM(BILLING[AMOUNT])
```

---

# 📁 Suggested GitHub Repository Structure

```text
Healthcare-Management-System/
│
├── README.md
│
├── data/
│   ├── appointments.csv
│   ├── patients.csv
│   ├── doctors.csv
│   ├── treatments.csv
│   └── billing.csv
│
├── sql/
│   ├── database_creation.sql
│   ├── data_loading.sql
│   └── data_quality.sql
│
├── databricks/
│   ├── Healthcare_Management_Analysis.py
│   ├── descriptive_analysis.py
│   ├── diagnostic_analysis.py
│   └── predictive_analysis.py
│
├── powerbi/
│   └── Healthcare_Analytics.pbix
│
├── streamlit/
│   ├── app.py
│   └── requirements.txt
│
├── models/
│   └── no_show_model.pkl
│
├── documentation/
│   ├── ER_Diagram.png
│   └── Project_Presentation.pptx
│
└── screenshots/
    ├── executive_dashboard.png
    ├── appointment_dashboard.png
    ├── doctor_treatment_dashboard.png
    └── billing_dashboard.png
```

---

# 🚀 End-to-End Workflow

```text
1. Collect Healthcare Data
          ↓
2. Load Data into Snowflake
          ↓
3. Perform Data Quality Auditing
          ↓
4. Load Data into Databricks
          ↓
5. Transform & Clean Data using PySpark
          ↓
6. Descriptive Analysis
          ↓
7. Diagnostic Analysis
          ↓
8. Predictive Analysis
          ↓
9. Build Power BI Dashboards
          ↓
10. Build Streamlit ML Application
          ↓
11. Generate Business Insights
          ↓
12. Provide Recommendations
          ↓
13. Deploy & Monitor
```

---

# 🏁 Conclusion

The **Healthcare Management System & Analytics** project demonstrates an end-to-end approach to solving real-world healthcare analytics problems.

The solution combines:

**Snowflake + Databricks + PySpark + SQL + Python + Machine Learning + Power BI + Streamlit**

to transform raw healthcare data into meaningful business intelligence.

The project provides stakeholders with visibility into:

* Patient activity
* Appointment performance
* Doctor workload
* Treatment trends
* Billing and collections
* Data quality
* Appointment no-show risk

The predictive component further demonstrates how historical healthcare data can be used to move from **reactive reporting toward proactive decision support**.

Overall, the project establishes a foundation for a scalable healthcare analytics platform that can be enhanced with larger datasets, advanced machine learning, real-time monitoring, automated alerts, and stronger data governance.
