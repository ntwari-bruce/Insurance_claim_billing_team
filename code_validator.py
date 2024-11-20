class CodeValidator:
    def __init__(self, cms_data):
        """
        Initialize the CodeValidator with CMS data.

        :param cms_data: List of dictionaries representing the CMS dataset.
        """
        self.cms_data = cms_data

    def validate_entries(self, entries):
        """
        Validates a list of diagnosis dictionaries against the CMS dataset.

        :param entries: List of dictionaries, each representing a diagnosis, e.g.,
                        [
                            {
                                "CPT_Code": "92012",
                                "CPT_Description": "Eye exam established patient",
                                "Condition_Name": "Dry Eyes",
                                "ICD10_Code": "H04.123",
                                "ICD10_Description": "Dry eye syndrome of bilateral lacrimal glands",
                                "Price": 22.59
                            }
                        ]
        :return: A tuple containing two lists:
                 - A list of dictionaries for valid entries that match the CMS dataset.
                 - A list of dictionaries for invalid entries that do not match.
        """
        valid_entries = []
        invalid_entries = []

        for entry in entries:
            # Check if any CMS row matches all fields (except Price)
            match_found = any(
                row["CPT_Code"] == entry["CPT_Code"] and
                row["CPT_Description"] == entry["CPT_Description"] and
                row["Condition_Name"] == entry["Condition_Name"] and
                row["ICD10_Code"] == entry["ICD10_Code"] and
                row["ICD10_Description"] == entry["ICD10_Description"]
                for row in self.cms_data
            )

            # Add to valid or invalid list based on match result
            if match_found:
                valid_entries.append(entry)
            else:
                invalid_entries.append(entry)

        return valid_entries, invalid_entries