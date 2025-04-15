"""
A module just to insert some patient data into the database.
And used to test the Procedure API.
"""

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict

# from fastapi.responses import JSONResponse
from models.patient import Patient

blueprint_name = "patient"

router = APIRouter(
    prefix=f"/{blueprint_name}",
    tags=[blueprint_name],
    responses={404: {"description": "Not found"}},
)


class NewPatient(BaseModel):
    name: str


class PatientDetail(NewPatient):
    model_config = ConfigDict(from_attributes=True)

    id: int


@router.post("/registry", response_model=PatientDetail)
async def create_patient(patient: NewPatient) -> PatientDetail:
    patient_instc = Patient(**patient.model_dump())
    patient_instc.create()
    return patient_instc
