--Use DATABASE and SCHEMAS
USE DATABASE HEALTHCARE_DB;
USE SCHEMA HEALTHCARE_SCHEMA;
--Creating the tables
CREATE TABLE appointments (
    appointment_id VARCHAR,
    patient_id VARCHAR,
    doctor_id VARCHAR,
    appointment_date DATE,
    appointment_time TIME,
    reason_for_visit VARCHAR,
    status VARCHAR
);
CREATE TABLE billing (
    bill_id VARCHAR,
    patient_id VARCHAR,
    treatment_id VARCHAR,
    bill_date DATE,
    amount float,
    payment_method VARCHAR,
    payment_status VARCHAR
);
CREATE TABLE doctors (
    doctor_id VARCHAR,
    first_name VARCHAR,
    last_name VARCHAR,
    specialization VARCHAR,
    phone_number VARCHAR,
    years_experience INTEGER,
    hospital_branch VARCHAR,
    email VARCHAR
);
CREATE TABLE patients (
    patient_id VARCHAR,
    first_name VARCHAR,
    last_name VARCHAR,
    gender VARCHAR,	
    date_of_birth DATE,
    contact_number VARCHAR,
    address VARCHAR,
    registration_date DATE,
    insurance_provider VARCHAR,
    insurance_number VARCHAR,
    email VARCHAR
);
CREATE TABLE treatments (
    treatment_id VARCHAR,
    appointment_id VARCHAR,
    treatment_type VARCHAR,
    description VARCHAR,
    cost FLOAT,
    treatment_date DATE
);
--View all the tables
LIST @healthcare_stage;

COPY INTO appointments
FROM @healthcare_stage/appointments.csv
FILE_FORMAT = csv_format
ON_ERROR = 'CONTINUE';

COPY INTO billing
FROM @healthcare_stage/billing.csv
FILE_FORMAT = csv_format
ON_ERROR = 'CONTINUE';

COPY INTO doctors
FROM @healthcare_stage/doctors.csv
FILE_FORMAT = csv_format
ON_ERROR = 'CONTINUE';

COPY INTO patients
FROM @healthcare_stage/patients.csv
FILE_FORMAT = csv_format
ON_ERROR = 'CONTINUE';

COPY INTO treatments
FROM @healthcare_stage/treatments.csv
FILE_FORMAT = csv_format
ON_ERROR = 'CONTINUE';

SELECT COUNT(*) FROM appointments;
SELECT COUNT(*) FROM billing;
SELECT COUNT(*) FROM doctors;
SELECT COUNT(*) FROM patients;
SELECT COUNT(*) FROM treatments;

--Check null values in patients table
SELECT
    COUNT(*) AS total_records,
    COUNT_IF(patient_id IS NULL) AS null_patient_id,
    COUNT_IF(first_name IS NULL) AS null_first_name,
    COUNT_IF(last_name IS NULL) AS null_last_name,
    COUNT_IF(gender IS NULL) AS null_gender,
    COUNT_IF(date_of_birth IS NULL) AS null_dob,
    COUNT_IF(contact_number IS NULL) AS null_contact,
    COUNT_IF(address IS NULL) AS null_address,
    COUNT_IF(registration_date IS NULL) AS null_registration_id,
    COUNT_IF(insurance_provider IS NULL) AS null_insurance_provider,
    COUNT_IF(insurance_number IS NULL) AS null_insuarance_no,
    COUNT_IF(email IS NULL) AS null_email
FROM patients;
--total records 50 and no null values in any column
--check null values in doctors table
SELECT
    COUNT(*) AS total_records,
    COUNT_IF(doctor_id IS NULL) AS NULL_DOCTOR_ID,
    COUNT_IF(first_name IS NULL) AS NULL_FIRST_NAME,
    COUNT_IF(last_name IS NULL) AS NULL_LAST_NAME,
    COUNT_IF(specialization IS NULL) AS NULL_SPECIALIZATION,
    COUNT_IF(phone_number IS NULL) AS NULL_PHONE_NUMBER,
    COUNT_IF(years_experience IS NULL) AS NULL_YEARS_EXPERIENCE,
    COUNT_IF(hospital_branch IS NULL) AS NULL_HOSPITAL_BRANCH,
    COUNT_IF(email IS NULL) AS NULL_EMAIL
FROM doctors;
--total records 10 and no null values in any column
--check null values in appointments table
SELECT
    COUNT(*) AS total_records,
    COUNT_IF(appointment_id IS NULL) AS NULL_APPOINTMENT_ID,
    COUNT_IF(patient_id IS NULL) AS NULL_PATIENT_ID,
    COUNT_IF(doctor_id IS NULL) AS NULL_DOCTOR_ID,
    COUNT_IF(appointment_date IS NULL) AS NULL_APPOINTMENT_DATE,
    COUNT_IF(appointment_time IS NULL) AS NULL_APPOINTMENT_TIME,
    COUNT_IF(reason_for_visit IS NULL) AS NULL_REASON,
    COUNT_IF(status IS NULL) AS NULL_STATUS
FROM appointments;
--total records 200 and no null values in any column
--check null values in billing table
SELECT
    COUNT(*) AS total_records,
    COUNT_IF(bill_id IS NULL) AS NULL_BILL_ID,
    COUNT_IF(patient_id IS NULL) AS NULL_PATIENT_ID,
    COUNT_IF(treatment_id IS NULL) AS NULL_TREATMENT_ID,
    COUNT_IF(bill_date IS NULL) AS NULL_BILL_DATE,
    COUNT_IF(amount IS NULL) AS NULL_AMOUNT,
    COUNT_IF(payment_method IS NULL) AS NULL_PAYMENT_METHOD,
    COUNT_IF(payment_status IS NULL) AS NULL_PAYMENT_STATUS
FROM billing;
--total records 200 and no null values in any column
--check null values in treatments table
SELECT
    COUNT(*) AS total_records,
    COUNT_IF(treatment_id IS NULL) AS NULL_TREATMENT_ID,
    COUNT_IF(appointment_id IS NULL) AS NULL_APPOINTMENT_ID,
    COUNT_IF(treatment_type IS NULL) AS NULL_TREATMENT_TYPE,
    COUNT_IF(description IS NULL) AS NULL_DESCRIPTION,
    COUNT_IF(cost IS NULL) AS NULL_COST,
    COUNT_IF(treatment_date IS NULL) AS NULL_TREATMENT_DATE
FROM treatments;
--total records 200 and no null values in any column

--Primary key shouldn't contains duplicates
SELECT patient_id, COUNT(*) AS duplicate_count
FROM patients
GROUP BY patient_id
HAVING COUNT(*) > 1;
--no duplicacy in patients table in patient_id column

SELECT doctor_id, COUNT(*) AS duplicate_count
FROM doctors
GROUP BY doctor_id
HAVING COUNT(*) > 1;
--no duplicacy in doctors table in doctor_id column

SELECT appointment_id, COUNT(*) AS duplicate_count
FROM appointments
GROUP BY appointment_id
HAVING COUNT(*) > 1;
--no duplicacy in apponitments table in appointment_id column

SELECT treatment_id, COUNT(*) AS duplicate_count
FROM treatments
GROUP BY treatment_id
HAVING COUNT(*) > 1;
--no duplicacy in treatments table in treatments_id column

SELECT bill_id, COUNT(*) AS duplicate_count
FROM billing
GROUP BY bill_id
HAVING COUNT(*) > 1;
--no duplicacy in billing table in bill_id column

--checks whether foreign key values actually exist in the parent tables
--appointments and patients table
SELECT a.* FROM appointments a
LEFT JOIN patients p ON a.patient_id = p.patient_id
WHERE p.patient_id IS NULL;
--appointments and doctors table
SELECT a.* FROM appointments a
LEFT JOIN doctors d ON a.doctor_id = d.doctor_id
WHERE d.doctor_id IS NULL;
--treatments and appointments
SELECT t.* FROM treatments t
LEFT JOIN appointments a ON t.appointment_id = a.appointment_id
WHERE a.appointment_id IS NULL;
--billing and treatments
SELECT b.* FROM billing b
LEFT JOIN treatments t ON b.treatment_id = t.treatment_id
WHERE t.treatment_id IS NULL;
--billing and patients table
SELECT b.* FROM billing b
LEFT JOIN patients p ON b.patient_id = p.patient_id
WHERE p.patient_id IS NULL;

--check negative treatments costs
SELECT * FROM treatments
WHERE cost < 0;
--check negative billing amounts
SELECT * FROM billing
WHERE amount < 0;
--check invalid gender values
SELECT gender, COUNT(*) AS record_count
FROM patients
GROUP BY gender
ORDER BY record_count DESC;
--check appointment status
SELECT status, COUNT(*) AS record_count
FROM appointments
GROUP BY status
ORDER BY record_count DESC;
--check payment status
SELECT payment_status, COUNT(*) AS record_count
FROM billing
GROUP BY payment_status
ORDER BY record_count DESC;
--check year_of_exp
SELECT * FROM doctors
WHERE years_experience < 0 OR years_experience > 60;
--check invalid treatment cost
SELECT * FROM treatments
WHERE cost IS NULL OR cost < 0;
--registration and appointments
--A patient should normally be registered before their appointment.
SELECT a.appointment_id, a.patient_id, p.registration_date, a.appointment_date
FROM appointments a
JOIN patients p ON a.patient_id = p.patient_id
WHERE a.appointment_date < p.registration_date;

--So 28 rows are potentially inconsistent records.

SELECT a.patient_id, COUNT(*) AS invalid_appointments FROM appointments a
JOIN patients p ON a.patient_id = p.patient_id
WHERE a.appointment_date < p.registration_date
GROUP BY a.patient_id
ORDER BY invalid_appointments DESC;

SELECT a.appointment_id, a.patient_id, p.registration_date, a.appointment_date,
    DATEDIFF(
        'DAY',
        a.appointment_date,
        p.registration_date
    ) AS DAYS_BEFORE_REGISTRATION
FROM appointments a
JOIN patients p ON a.patient_id = p.patient_id
WHERE a.appointment_date < p.registration_date
ORDER BY DAYS_BEFORE_REGISTRATION DESC;

CREATE OR REPLACE TABLE appointments_clean AS
SELECT a.*,CASE WHEN a.appointment_date < p.registration_date THEN 'INVALID_DATE_SEQUENCE'ELSE'VALID' END AS DATA_QUALITY_STATUS
FROM appointments a
JOIN patients p ON a.patient_id = p.patient_id
;
select * from appointments_clean
SELECT * FROM appointments_clean
WHERE DATA_QUALITY_STATUS = 'VALID';
--there are 172 rows in new appointmnets table where data is cleaned
--I used this data...
SELECT t.treatment_id,t.appointment_id,a.appointment_date,t.treatment_date
FROM treatments t
JOIN appointments a ON t.appointment_id = a.appointment_id
WHERE t.treatment_date < a.appointment_date
;
--Treatment should normally occur on or after the appointment date.
--treatment and billing
SELECT b.bill_id, b.treatment_id, t.treatment_date,b.bill_date
FROM billing b
JOIN treatments t ON b.treatment_id = t.treatment_id
WHERE b.bill_date < t.treatment_date;
--Billing should normally occur on or after the treatment date.

--we can check whether the patient in billing is actually the patient associated with the treatment's appointment.
SELECT b.bill_id, b.patient_id AS BILLING_PATIENT, a.patient_id AS APPOINTMENT_PATIENT,b.treatment_id
FROM billing b
JOIN treatments t ON b.treatment_id = t.treatment_id
JOIN appointments a ON t.appointment_id = a.appointment_id
WHERE b.patient_id <> a.patient_id;
