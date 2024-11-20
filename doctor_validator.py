# we are checking if the doctor is among the list of licensed doctors that we work with
class DoctorValidator:
    def __init__(self, doctor_data):
        """
        Initialize the DoctorValidator with doctor data.

        :param doctor_data: List of dictionaries representing the doctor dataset.
        """
        self.doctor_data = doctor_data

    def validate_doctor(self, doctor_entry):
        """
        Validates if the provided doctor information matches the database.

        :param doctor_entry: Dictionary containing doctor details to validate, e.g.,
                             {
                                "Doctor_ID": "D001",
                                "Name": "Dr. Martin",
                                "Specialization": "Optometrist",
                                "License_Number": "L12345",
                                "Active_Status": "Active"
                             }
        :return: Tuple (is_valid, invalid_reason)
                 - is_valid: Boolean indicating if the doctor is valid.
                 - invalid_reason: None if valid, otherwise a string explaining the validation error.
        """
        for doctor in self.doctor_data:
            if (
                doctor["Doctor_ID"] == doctor_entry["Doctor_ID"]
                and doctor["Name"] == doctor_entry["Name"]
                and doctor["Specialization"] == doctor_entry["Specialization"]
                and doctor["License_Number"] == doctor_entry["License_Number"]
            ):
                if doctor["Active_Status"] != "Active":
                    return False, f"Doctor {doctor['Name']} is not active."
                return True, None
        
        return False, "Doctor information does not match any record."

