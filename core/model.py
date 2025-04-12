"""
* users management
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/user-service-management
"""

import uuid
import typing
import datetime

import sqlalchemy as sa
import sqlalchemy.orm as so
import sqlalchemy.ext.asyncio as AsyncSA

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
    created_at: so.Mapped[typing.Optional[datetime.datetime]] = (
        so.mapped_column(
            sa.TIMESTAMP(timezone=True),  # Add timezone support
            default=lambda: datetime.datetime.now(datetime.UTC),
        )
    )
    verified_at: so.Mapped[typing.Optional[datetime.datetime]] = (
        so.mapped_column(
            sa.TIMESTAMP(timezone=True),
            default=lambda: datetime.datetime.now(datetime.UTC),
        )
    )
    modified_at: so.Mapped[typing.Optional[datetime.datetime]] = (
        so.mapped_column(
            sa.TIMESTAMP(timezone=True),
            onupdate=lambda: datetime.datetime.now(datetime.UTC),
            default=lambda: datetime.datetime.now(datetime.UTC),
        )
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

    async def save(
        self,
        db_session: AsyncSA.AsyncSession | None = None,
        show_traceback: bool = True,
        capture_traceback: bool = True,
    ) -> bool:
        """
        Combination of two steps: add and commit session

        :param db: Optional SQLAlchemy session to use. If None, a session will be created via `get_db()`
        :param show_traceback: Flag to show traceback of the exception to stdout or not
        :param capture_trackback: Flag to capture and return the exception
        :return: True if the save operation is successful, otherwise False
        """

        session: AsyncSA.AsyncSession = db_session or get_session()
        try:
            session.add(self)
            await session.commit()
            return True
        except Exception as e:
            await session.rollback()
            if show_traceback:
                print("Error occurred while saving the object", e)

            if capture_traceback:
                return e

            return False

    async def delete(
        self,
        capture_exception: bool = False,
        session: AsyncSA.AsyncSession | None = None,
    ):
        """delete method"""
        db: AsyncSA.AsyncSession = session or get_session()

        try:
            await db.delete(self)
            await db.commit()
            return True
        except Exception as e:
            await db.rollback()
            if capture_exception:
                return e
            return False
