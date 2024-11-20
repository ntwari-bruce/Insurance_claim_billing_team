class PatientValidator:
    def __init__(self, coverage_data):
        """
        Initialize the PatientValidator with BlueCross coverage data.

        :param coverage_data: List of dictionaries representing the BlueCross coverage dataset.
        """
        self.coverage_data = coverage_data

    def validate_patient(self, patient_entry):
        """
        Validates if the patient is covered under BlueCross and returns their coverage percentage.

        :param patient_entry: Dictionary containing patient details to validate, e.g.,
                              {
                                  "Patient_ID": "P001",
                                  "Name": "Shadrack Peter",
                                  "Insurance_ID": "H123456789"
                              }
        :return: Tuple (is_valid, coverage_percentage, invalid_reason)
                 - is_valid: Boolean indicating if the patient is valid.
                 - coverage_percentage: The coverage percentage if valid, or None.
                 - invalid_reason: None if valid, otherwise a string explaining the validation error.
        """
        for record in self.coverage_data:
            if (
                record["Patient_ID"] == patient_entry["Patient_ID"]
                and record["Name"] == patient_entry["Name"]
                and record["Insurance_ID"] == patient_entry["Insurance_ID"]
            ):
                return True, record["Coverage_Percentage"], None

        return False, None, f"Patient {patient_entry['Name']} is not found in the BlueCross database."

