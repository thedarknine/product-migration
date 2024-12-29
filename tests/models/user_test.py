"""Test user model."""

from datetime import datetime, timedelta
from sources.models.user import User


past_datetime = datetime.now() - timedelta(days=1)
user_test = User(
    uuid="62492acb-203d-4bdb-82e3-85fbd5cf2cc9",
    external_id=9,
    full_name="FirstName LastName",
    first_name="FirstName",
    last_name="LastName",
    email="test@mail.com",
    login="first.last",
    is_admin=False,
    status="active",
    created_at=past_datetime,
    updated_at=past_datetime,
)


def test_repr():
    """Test the user model."""
    assert (
        repr(user_test)
        == "<User(uuid=62492acb-203d-4bdb-82e3-85fbd5cf2cc9, external_id=9, "
        + "first_name=FirstName, last_name=LastName, full_name=FirstName LastName, "
        + "email=test@mail.com, login=first.last, is_admin=False, status=active, created_at="
        + str(past_datetime)
        + ", updated_at="
        + str(past_datetime)
        + ")>"
    )


def test_from_raw():
    """Test the user model."""
    raw_data = {
        "id": 9,
        "name": "FirstName LastName",
        "firstName": "FirstName",
        "lastName": "LastName",
        "email": "test@mail.com",
        "login": "first.last",
        "admin": False,
        "status": "active",
        "createdAt": "2024-12-27T12:00:00.000Z",
        "updatedAt": "2024-12-27T12:00:00.000Z",
    }
    raw_obj = type("Obj", (object,), dict(raw_data))()
    assert isinstance(User().from_raw(raw_obj), User)


def test_to_dict():
    """Test the user model."""
    assert isinstance(user_test.to_dict(), dict)
    assert user_test.to_dict()["uuid"] == "62492acb-203d-4bdb-82e3-85fbd5cf2cc9"
    assert user_test.to_dict()["external_id"] == 9
    assert user_test.to_dict()["full_name"] == "FirstName LastName"
    assert user_test.to_dict()["first_name"] == "FirstName"
    assert user_test.to_dict()["last_name"] == "LastName"
    assert user_test.to_dict()["email"] == "test@mail.com"
    assert user_test.to_dict()["login"] == "first.last"
    assert user_test.to_dict()["is_admin"] is False
    assert user_test.to_dict()["status"] == "active"
    assert user_test.to_dict()["created_at"] == past_datetime
    assert user_test.to_dict()["updated_at"] == past_datetime

    assert user_test.to_dict() == {
        "uuid": "62492acb-203d-4bdb-82e3-85fbd5cf2cc9",
        "external_id": 9,
        "full_name": "FirstName LastName",
        "first_name": "FirstName",
        "last_name": "LastName",
        "email": "test@mail.com",
        "login": "first.last",
        "is_admin": False,
        "status": "active",
        "created_at": past_datetime,
        "updated_at": past_datetime,
    }
