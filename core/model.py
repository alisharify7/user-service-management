import uuid
import typing
import datetime

import sqlalchemy as sa
import sqlalchemy.orm as so

from core import get_config
from core.db import BaseModelClass, get_session

Setting = get_config()
class BaseModel(BaseModelClass):
    """
    Base Parent Abstract Model.
    all models inheritance from this model.
    """
    __abstract__ = True
    id: so.Mapped[int] = so.mapped_column(sa.BigInteger(), primary_key=True)
    is_active: so.Mapped[bool] = so.mapped_column(
        sa.Boolean(), nullable=False, default=False, unique=False
    )
    public_key: so.Mapped[str] = so.mapped_column(
        sa.String(36), nullable=False, unique=True, index=True
    )  # unique key for each element <usually used in frontend>
    created_at: so.Mapped[typing.Optional[datetime.datetime]] = so.mapped_column(
        sa.TIMESTAMP, default=lambda: datetime.datetime.now(datetime.UTC)
    )
    verified_at: so.Mapped[typing.Optional[datetime.datetime]] = so.mapped_column(
        sa.TIMESTAMP, default=lambda: datetime.datetime.now(datetime.UTC)
    )
    modified_at: so.Mapped[typing.Optional[datetime.datetime]] = so.mapped_column(
        sa.TIMESTAMP,
        onupdate=lambda: datetime.datetime.now(datetime.UTC),
        default=lambda: datetime.datetime.now(datetime.UTC),
    )

    @staticmethod
    def set_table_name(name: str) -> str:
        """
        this static method concat table prefix names and table names
        for all models.

        :param name: name of the table
        :type name: str
        :return: name of the table
        :rtype: str
        """
        name = name.replace("-", "_").replace(" ", "")
        return f"{Setting.DATABASE_TABLE_PREFIX_NAME}{name}".lower()

    def set_public_key(self):
        """This Method Set a Unique PublicKey of each record"""
        self.public_key = uuid.uuid4().hex
    def save(
        self,
        session: so.Session | None = None,
        show_traceback: bool = True,
        capture_tracekback: bool = True,
    ) -> bool:
        """
        Combination of two steps: add and commit session

        :param db: Optional SQLAlchemy session to use. If None, a session will be created via `get_db()`
        :param show_traceback: Flag to show traceback of the exception to stdout or not
        :param capture_trackback: Flag to capture and return the exception
        :return: True if the save operation is successful, otherwise False
        """

        db = session or get_session()

        try:
            db.add(self)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            if show_traceback:
                print(
                    "Error occurred while saving the object", e
                )

            if capture_tracekback:
                return e

            return False
        finally:
            db.close()  # Always close the session to free up resources

    def delete(
        self, capture_exception: bool = False, session: so.Session | None = None
    ):
        """delete method"""
        db = session or get_session()

        try:
            db.delete(self)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            if capture_exception:
                return e
            return False