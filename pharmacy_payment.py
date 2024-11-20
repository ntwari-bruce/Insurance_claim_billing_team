class PharmacyPaymentProcessor:
    def __init__(self, drugs_data, patient_validator):
        """
        Initialize the PharmacyPaymentProcessor with drug data and a patient validator.

        :param drugs_data: List of dictionaries representing the drug dataset.
        :param patient_validator: Instance of PatientValidator to validate patient details.
        """
        self.drugs_data = drugs_data
        self.patient_validator = patient_validator

    def process_payment(self, patient_entry, prescribed_drugs):
        """
        Validates the patient and calculates the payment for the prescribed drugs.

        :param patient_entry: Dictionary containing patient details, e.g.,
                              {
                                  "Patient_ID": "P001",
                                  "Name": "Shadrack Peter",
                                  "Insurance_ID": "H123456789"
                              }
        :param prescribed_drugs: List of drug names prescribed to the patient, e.g.,
                                 ["Paracetamol", "Ibuprofen"]
        :return: Tuple (is_valid, result)
                 - is_valid: Boolean indicating if the payment process is valid.
                 - result: Dictionary with patient name, ID, and total amount paid, 
                           or a string explaining why the payment failed.
        """
        # Validate the patient using the PatientValidator
        is_valid_patient, coverage_percentage, reason = self.patient_validator.validate_patient(patient_entry)

        if not is_valid_patient:
            return False, reason

        total_payment = 0.0
        for drug in prescribed_drugs:
            # Find the drug in the drug database
            drug_record = next((record for record in self.drugs_data if record["Drug_Name"].lower() == drug.lower()), None)

            if not drug_record:
                return False, f"The drug '{drug}' is not available in our database."

            # Calculate the amount covered by insurance
            drug_price = float(drug_record["Drug_Price"])
            drug_coverage_percentage = float(coverage_percentage.strip('%')) / 100
            total_payment += drug_price * drug_coverage_percentage

        return True, {
            "Patient_ID": patient_entry["Patient_ID"],
            "Patient_Name": patient_entry["Name"],
            "Total_Payment": round(total_payment, 2)  # Rounded to 2 decimal places
        }

'''
# Example usage
import csv

# Load the CSV files into lists of dictionaries
def load_csv(file_path):
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        return list(reader)

# Load drug data and coverage data
drug_data = load_csv("drug_data.csv")
patient_coverage_data = load_csv("patient_coverage_data.csv")

# Initialize the patient validator
from patient_validator import PatientValidator
patient_validator = PatientValidator(patient_coverage_data)

# Initialize the pharmacy payment processor
processor = PharmacyPaymentProcessor(drug_data, patient_validator)

# Test a valid patient with valid drugs
patient_entry = {
    "Patient_ID": "P001",
    "Name": "Shadrack Peter",
    "Insurance_ID": "H123456789"
}
prescribed_drugs = ["Paracetamol", "Ibuprofen"]

is_valid, result = processor.process_payment(patient_entry, prescribed_drugs)
print(is_valid, result)
# Output: True, {'Patient_ID': 'P001', 'Patient_Name': 'Shadrack Peter', 'Total_Payment': 11.375}

# Test a patient with a drug not in the database
prescribed_drugs = ["Paracetamol", "Nonexistent Drug"]
is_valid, result = processor.process_payment(patient_entry, prescribed_drugs)
print(is_valid, result)
# Output: False, "The drug 'Nonexistent Drug' is not available in our database."

# Test a non-existent patient
invalid_patient_entry = {
    "Patient_ID": "P999",
    "Name": "Jane Doe",
    "Insurance_ID": "H111111111"
}
is_valid, result = processor.process_payment(invalid_patient_entry, prescribed_drugs)
print(is_valid, result)
# Output: False, "Patient Jane Doe is not found in the BlueCross database."
'''