from sqlalchemy import and_, exists
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

    def get(self, id: int):
        return self.__database.query(self.__class__).get(id)

    @classmethod
    def filter(cls, **kwargs):
        # pass kwargs by reference
        range_filters = cls.__create_range_filter(kwargs)
        remaining_filters = [
            getattr(cls, key) == value for key, value in kwargs.items()
        ]

        all_filters = range_filters + remaining_filters

        return cls.__database.query(cls).filter(and_(*all_filters))

    @classmethod
    def exists(cls, **kwargs) -> bool:
        """
        Check if a record exists in the database.
        """
        return cls.__database.query(
            exists().where(
                *[getattr(cls, key) == value for key, value in kwargs.items()]
            )
        ).scalar()

    def save(self):
        self.__database.commit()
        self.__database.refresh(self)

    @classmethod
    def __create_range_filter(cls, kwargs: dict) -> list:
        range_filters = []

        for key in list(kwargs.keys()):
            # check if is a range filter. Get the columns and create the filter
            if key.endswith("__range"):
                col_name = key[: -len("__range")]
                column = getattr(cls, col_name, None)
                start, end = kwargs.pop(key)

                # if column does not exist, raise an error
                if column is None:
                    raise ValueError(
                        f"Column {col_name} does not exist in {cls.__class__}"
                    )

                if not start or not end:
                    raise ValueError(
                        "Start and end values are required for range filter"
                    )

                range_filters.append(column.between(start, end))
        return range_filters
