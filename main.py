import json
from file_handler import load_csv
from patient_validator import PatientValidator
from doctor_validator import DoctorValidator
from code_validator import CodeValidator
from pharmacy_payment import PharmacyPaymentProcessor

def calculate_insurance_payment(patient_entry, doctor_entry, diagnosis_entries, prescribed_drugs):
    """
    Calculates the total amount paid by the insurance for the healthcare provider and pharmacy.

    :param patient_entry: Dictionary containing patient details.
    :param doctor_entry: Dictionary containing doctor details.
    :param diagnosis_entries: List of diagnosis entries to validate against CMS data.
    :param prescribed_drugs: List of drug names prescribed to the patient.
    :return: Dictionary containing the insurance payment details and rejection reasons, if any.
    """
    # Load all required datasets
    cms_data = load_csv("CMS_CPT_ICD.csv")
    doctor_data = load_csv("doctor_data.csv")
    patient_coverage_data = load_csv("patient_coverage.csv")
    drug_data = load_csv("drugs_data.csv")

    # Initialize validators and processors
    patient_validator = PatientValidator(patient_coverage_data)
    doctor_validator = DoctorValidator(doctor_data)
    code_validator = CodeValidator(cms_data)
    pharmacy_processor = PharmacyPaymentProcessor(drug_data, patient_validator)

    result = {
        "Patient_ID": patient_entry["Patient_ID"],
        "Patient_Name": patient_entry["Name"],
        "Doctor_ID": doctor_entry["Doctor_ID"],
        "Doctor_Name": doctor_entry["Name"],
        "Diagnosis": diagnosis_entries,
        "Prescribed_Drugs": prescribed_drugs,
        "Payment_Details": {
            "Payment to Healthcare_Provider": 0.0,
            "Payment to Pharmacy": 0.0,
        },
        "Rejections": []
    }

    # Step 1: Validate the patient
    is_valid_patient, coverage_percentage, reason = patient_validator.validate_patient(patient_entry)
    if not is_valid_patient:
        result["Rejections"].append(reason)
        return result

    # Step 2: Validate the doctor
    is_valid_doctor, reason = doctor_validator.validate_doctor(doctor_entry)
    if not is_valid_doctor:
        result["Rejections"].append(reason)
        return result

    # Step 3: Validate the diagnosis (CPT and ICD codes)
    valid_diagnoses, invalid_diagnoses = code_validator.validate_entries(diagnosis_entries)
    if invalid_diagnoses:
        result["Rejections"].append(f"Invalid diagnoses: {invalid_diagnoses}")
        return result

    # Step 4: Calculate payment for the healthcare provider
    total_diagnosis_cost = sum(float(entry["Price"]) for entry in valid_diagnoses)
    patient_coverage_rate = float(coverage_percentage.strip('%')) / 100
    provider_payment = total_diagnosis_cost * patient_coverage_rate
    result["Payment_Details"]["Payment to Healthcare_Provider"] = round(provider_payment, 2)

    # Step 5: Process pharmacy payments
    is_valid_pharmacy, pharmacy_result = pharmacy_processor.process_payment(patient_entry, prescribed_drugs)
    if not is_valid_pharmacy:
        result["Rejections"].append(pharmacy_result)
    else:
        result["Payment_Details"]["Payment to Pharmacy"] = pharmacy_result["Total_Payment"]

    return result


def main():
    # Example data
    patient_entry = {
        "Patient_ID": "P001",
        "Name": "Shadrack Peter",
        "Insurance_ID": "H123456789"
    }

    doctor_entry = {
        "Doctor_ID": "D001",
        "Name": "Dr. Martin",
        "Specialization": "Optometrist",
        "License_Number": "L12345",
        "Active_Status": "Active"
    }

    diagnosis_entries = [
        {
            "CPT_Code": "92012",
            "CPT_Description": "Eye exam established patient",
            "Condition_Name": "Dry Eyes",
            "ICD10_Code": "H04.123",
            "ICD10_Description": "Dry eye syndrome of bilateral lacrimal glands",
            "Price": 22.59
        },
        {
            "CPT_Code": "92015",
            "CPT_Description": "Determination of refractive state",
            "Condition_Name": "Myopia",
            "ICD10_Code": "H52.13",
            "ICD10_Description": "Myopia bilateral",
            "Price": 35.38
        }
    ]

    prescribed_drugs = ["Paracetamol", "Ibuprofen"]

    # Calculate the insurance payment
    result = calculate_insurance_payment(patient_entry, doctor_entry, diagnosis_entries, prescribed_drugs)

    # Save the result as a JSON file
    with open("insurance_payment_report.json", "w") as json_file:
        json.dump(result, json_file, indent=4)

    # Print the result
    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()