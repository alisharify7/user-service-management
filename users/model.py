import datetime
import enum
import typing

import sqlalchemy as sa
import sqlalchemy.orm as so

from core.model import BaseModel


class Gender(enum.Enum):
    female: str = "female"
    male: str = "male"
    other: str = "other"

class User(BaseModel):
    __tablename__ = BaseModel.set_table_name("users")
    first_name: so.Mapped[str] = so.mapped_column(sa.String(256), unique=False, nullable=True)
    last_name: so.Mapped[str] = so.mapped_column(sa.String(256), unique=False, nullable=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(256), unique=True, nullable=False)
    password: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=False)
    email_address: so.Mapped[str] = so.mapped_column(sa.String(320), unique=True, nullable=True) #https://stackoverflow.com/questions/386294/what-is-the-maximum-length-of-a-valid-email-address
    phone_number: so.Mapped[str] = so.mapped_column(sa.String(16), unique=True, nullable=True)
    last_login: so.Mapped[typing.Optional[datetime.datetime]] = so.mapped_column(sa.TIMESTAMP(), nullable=True)
    login_attempts: so.Mapped[int] = so.mapped_column(sa.BigInteger(), default=0, nullable=False)
    gender: so.Mapped[Gender] = so.mapped_column(sa.Enum(Gender), nullable=True)


    def set_password(self):
        pass
    def set_username(self):
        pass
    def set_phone_number(self):
        pass
    def set_email_address(self):
        pass