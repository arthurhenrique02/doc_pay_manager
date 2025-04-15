def doctor_exists(doctor_id: int) -> int:
    """
    Check if a doctor exists in the database.

    @Params:
        - doctor_id: ID of the doctor

    @Return:
        - True if the doctor exists, False otherwise
    """
    from models.doctor import Doctor

    if not isinstance(doctor_id, int) or doctor_id <= 0:
        raise ValueError("Doctor id must be an integer greater than 0.")

    if not Doctor.exists(id=doctor_id):
        raise ValueError(f"Doctor with id {doctor_id} does not exist.")

    return doctor_id


def patient_exists(patient_id: int) -> int:
    """
    Check if a patient exists in the database.

    @Params:
        - patient_id: ID of the patient

    @Return:
        - True if the patient exists, False otherwise
    """
    from models.patient import Patient

    if not isinstance(patient_id, int) or patient_id <= 0:
        raise ValueError("Patient id must be an integer greater than 0.")

    if not Patient.exists(id=patient_id):
        raise ValueError(f"Patient with id {patient_id} does not exist.")

    return patient_id
