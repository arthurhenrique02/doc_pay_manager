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


def value_is_number(value: float) -> float:
    """
    Check if a value is a number.

    @Params:
        - value: Value to be checked

    @Return:
        - True if the value is a number, False otherwise
    """
    if not isinstance(value, (int, float)):
        raise ValueError("Value must be a number.")

    return value


def user_exists(user_id: int) -> int:
    """
    Check if a user exists in the database.

    @Params:
        - user_id: ID of the user

    @Return:
        - True if the user exists, False otherwise
    """
    from models.user import User

    if not isinstance(user_id, int) or user_id <= 0:
        raise ValueError("User id must be an integer greater than 0.")

    if not User.exists(id=user_id):
        raise ValueError(f"User with id {user_id} does not exist.")

    return user_id
