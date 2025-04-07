import sqlalchemy as sa
import sqlalchemy.orm as so
import sqlalchemy.ext.asyncio as AsyncSA

from core.extensions import hashManager
from users.model import User as UserModel
from starlette import status as http_status


async def create_user(
    user_data: dict, db_session: AsyncSA.AsyncSession
) -> tuple:
    """
    Attempts to create a new user in the database.

    This function checks for existing users with the same username, phone number, or email address.
    If any of these fields already exist in the database, it returns a corresponding HTTP 409 conflict
    with an appropriate error message. If no conflicts are found, it creates and saves the user.

    :param user_data: A dictionary or Pydantic model containing user attributes.
    :param db_session: SQLAlchemy session object used for database operations.
    :return:
        - On success: a tuple containing the created UserModel instance, e.g. `(new_user,)`
        - On failure: a tuple with HTTP status code and error message, e.g. `(409, "Username already exists.")`
    """
    query = sa.select(UserModel).filter(
        sa.or_(
            UserModel.username == user_data.username,
            UserModel.phone_number == user_data.phone_number,
            UserModel.email_address == user_data.email_address,
        )
    )
    result = (await db_session.execute(query)).scalar_one_or_none()
    if result:
        if result.username == user_data.username:
            return (
                http_status.HTTP_409_CONFLICT,
                "Username already exists.",
            )
        elif result.phone_number == user_data.phone_number:
            return (
                http_status.HTTP_409_CONFLICT,
                "Phone number already exists.",
            )
        elif result.email_address == user_data.email_address:
            return (
                http_status.HTTP_409_CONFLICT,
                "Email address already exists.",
            )

    new_user = UserModel(**user_data.model_dump())
    new_user.set_password(new_user.password)
    new_user.set_public_key()
    db_session.add(new_user)

    try:
        await db_session.commit()
    except Exception as e:
        print(e)
        await db_session.rollback()
        return (
            http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            f"there was an error in the saving the user in db. check logs for more info. + {e.args}",
        )
    await db_session.refresh(new_user)
    return (new_user,)


async def delete_user(user_id: int, db_session: AsyncSA.AsyncSession) -> tuple:
    """
    Attempts to delete a user by their ID.

    Executes a delete query on the UserModel table for the given user ID. If the user is successfully deleted,
    it returns a tuple with a single `True` value. Otherwise, returns an appropriate HTTP status code and error message.

    :param user_id: The ID of the user to be deleted.
    :param db_session: SQLAlchemy session object used for database operations.
    :return:
        - On success: a tuple containing True, e.g. `(True,)`
        - If user not found: `(400, "User not found or no changes made")`
        - On error: `(500, "An error occurred")`
    """

    query = sa.delete(UserModel).filter_by(id=user_id)
    try:
        result = await db_session.execute(query)
        await db_session.commit()
        if result.rowcount > 0:
            return (True,)
        else:
            return (
                http_status.HTTP_400_BAD_REQUEST,
                "User not found or no changes made",
            )
    except Exception as e:
        await db_session.rollback()
        return (
            http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            "An error occurred",
        )


async def update_user(
    user_data: dict, user_id: int, db_session: AsyncSA.AsyncSession
) -> tuple:
    """
    Updates the information of an existing user.

    This function takes updated user data and applies it to the user with the specified ID.
    It hashes the password before updating and commits the changes to the database.

    :param user_data: Dictionary or Pydantic model containing the updated user fields.
    :param user_id: The ID of the user to update.
    :param db_session: SQLAlchemy session object used for database operations.
    :return:
        - On success: a tuple containing True, e.g. `(True,)`
        - If user not found or no changes made: `(400, "User not found or no changes made")`
        - On error: `(500, "An error occurred")`
    """

    user_data = user_data.model_dump()
    user_data["password"] = hashManager.hash(user_data["password"])
    query = (
        sa.update(UserModel).where(UserModel.id == user_id).values(**user_data)
    )
    try:
        result = await db_session.execute(query)
        await db_session.commit()
        if result.rowcount > 0:
            return (True,)
        else:
            return (
                http_status.HTTP_400_BAD_REQUEST,
                "User not found or no changes made",
            )
    except Exception as e:
        await db_session.rollback()
        return (
            http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            "An error occurred",
        )


async def get_user_by_id(
    user_id: int, db_session: AsyncSA.AsyncSession
) -> tuple:
    """
    Retrieves a user by their unique ID.

    :param user_id: The ID of the user.
    :param db_session: SQLAlchemy session for DB operations.
    :return:
        - On success: a tuple with the user instance, e.g. `(user,)`
        - On failure: a tuple with HTTP status code and error message.
    """
    query = sa.select(UserModel).filter_by(id=user_id)
    result = (await db_session.execute(query)).scalar_one_or_none()
    if not result:
        return (
            http_status.HTTP_404_NOT_FOUND,
            "No user found with the given ID.",
        )
    return (result,)


async def get_user_by_username(
    username: str, db_session: AsyncSA.AsyncSession
) -> tuple:
    """
    Retrieves a user by their username.

    :param username: The username to search for.
    :param db_session: SQLAlchemy session for DB operations.
    :return:
        - On success: a tuple with the user instance, e.g. `(user,)`
        - On failure: a tuple with HTTP status code and error message.
    """
    query = sa.select(UserModel).filter_by(username=username)
    result = (await db_session.execute(query)).scalar_one_or_none()
    if not result:
        return (
            http_status.HTTP_404_NOT_FOUND,
            "No user found with the given username.",
        )
    return (result,)


async def get_user_by_public_key(
    public_key: str, db_session: AsyncSA.AsyncSession
) -> tuple:
    """
    Retrieves a user by their public key.

    :param public_key: The public key to search for.
    :param db_session: SQLAlchemy session for DB operations.
    :return:
        - On success: a tuple with the user instance, e.g. `(user,)`
        - On failure: a tuple with HTTP status code and error message.
    """
    query = sa.select(UserModel).filter_by(public_key=public_key)
    result = (await db_session.execute(query)).scalar_one_or_none()
    if not result:
        return (
            http_status.HTTP_404_NOT_FOUND,
            "No user found with the given public key.",
        )
    return (result,)


def get_all_users(): ...


# TODO: instead of get_user_by a field create a function get_user_by_field
