from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, Numeric
from sqlalchemy.orm import relationship

from .base import Base


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
