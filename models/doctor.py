from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    procedures = relationship("Procedure", back_populates="doctor")
