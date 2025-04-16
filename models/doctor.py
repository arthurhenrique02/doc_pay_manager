import typing

from pydantic import AfterValidator, BaseModel, ConfigDict
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from validators.validators import user_exists

from .base import Base


class NewDoctor(BaseModel):
    name: str
    user_id: typing.Annotated[int, AfterValidator(user_exists)]


class DoctorDetail(NewDoctor):
    model_config = ConfigDict(from_attributes=True)

    id: int


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    procedures = relationship("Procedure", back_populates="doctor")
    user = relationship("User", back_populates="doctor")

    @classmethod
    def get_by_user_id(cls, user_id: int) -> DoctorDetail | bool:
        """
        Get doctor by user ID.
        """
        return cls.filter(user_id=user_id).first()
