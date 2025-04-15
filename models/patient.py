from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    procedures = relationship("Procedure", back_populates="patient")
