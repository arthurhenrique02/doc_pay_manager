from sqlalchemy.orm import DeclarativeBase

from .engine import get_db


class Base(DeclarativeBase):
    __database = next(get_db())

    def create(self):
        self.__database.add(self)
        self.save()

    def update(self, id: int) -> None:
        instance = (
            self.__database.query(self.__class__)
            .filter(self.__class__.id == id)
            .first()
        )
        self.save()
        return instance

    def delete(self, id: int) -> bool:
        instance = (
            self.__database.query(self.__class__)
            .filter(self.__class__.id == id)
            .first()
        )
        if instance:
            self.__database.delete(instance)
            self.save()
            return True
        return False

    def save(self):
        self.__database.commit()
        self.__database.refresh(self)
