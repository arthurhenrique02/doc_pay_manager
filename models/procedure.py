import typing
from datetime import date

from pydantic import AfterValidator, BaseModel, ConfigDict
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, Numeric, func
from sqlalchemy.orm import relationship

from validators.validators import doctor_exists, patient_exists, value_is_number

from .base import Base


class FinancialReport(BaseModel):
    total_value: float
    procedures: int
    status: str


class NewProcedure(BaseModel):
    doctor_id: typing.Annotated[int, AfterValidator(doctor_exists)]
    patient_id: typing.Annotated[int, AfterValidator(patient_exists)]
    date: date
    value: typing.Annotated[float, AfterValidator(value_is_number)]
    payment_status: typing.Literal["paid", "pending", "glossed"]


class ProcedureDetail(NewProcedure):
    model_config = ConfigDict(from_attributes=True)

    id: int


class GlossedReport(BaseModel):
    start: date
    end: date


class Procedure(Base):
    __tablename__ = "procedures"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    value = Column(Numeric(10, 2), nullable=False)
    payment_status = Column(
        Enum("paid", "pending", "glossed", name="payment_status"), nullable=False
    )

    doctor = relationship("Doctor", back_populates="procedures")
    patient = relationship("Patient", back_populates="procedures")

    @classmethod
    def get_financial_report(cls, doctor_id: int) -> list[FinancialReport]:
        """
        Get financial report of procedures by doctor.
        """
        return (
            cls._database.query(
                func.sum(cls.value).label("total_value"),
                func.count(cls.id).label("procedures"),
                cls.payment_status.label("status"),
            )
            .filter(cls.doctor_id == doctor_id)
            .group_by(cls.payment_status)
            .all()
        )
