"""
A module just to insert some doctor data into the database.
And used to test the Procedure API.
"""

from fastapi import APIRouter

# from fastapi.responses import JSONResponse
from models.doctor import Doctor, DoctorDetail, NewDoctor

blueprint_name = "doctor"

router = APIRouter(
    prefix=f"/{blueprint_name}",
    tags=[blueprint_name],
    responses={404: {"description": "Not found"}},
)


@router.post("/registry", response_model=DoctorDetail)
async def create_doctor(doctor: NewDoctor) -> DoctorDetail:
    doctor_instc = Doctor(**doctor.model_dump())
    doctor_instc.create()
    return doctor_instc
