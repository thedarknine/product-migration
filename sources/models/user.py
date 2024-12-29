"""User model."""

import enum
import uuid
from sqlalchemy import Column
from sqlalchemy.types import Uuid, Integer, String, DateTime, Boolean, Enum
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class UserStatus(enum.Enum):
    """User status."""

    ACTIVE = "active"
    INACTIVE = "inactive"


class User(Base):
    """Data User model."""

    __tablename__ = "users"
    uuid = Column(Uuid, primary_key=True)
    external_id = Column(Integer, unique=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    full_name = Column(String(255))
    email = Column(String(255), nullable=False)
    login = Column(String(255))
    is_admin = Column(Boolean, default=False)
    status = Column(Enum(UserStatus), default=UserStatus.ACTIVE)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    def __repr__(self) -> str:
        """User representation.

        Returns:
            str: User representation.
        """
        return (
            f"<User(uuid={self.uuid}, external_id={self.external_id}, "
            f"first_name={self.first_name}, last_name={self.last_name}, "
            f"full_name={self.full_name}, email={self.email}, "
            f"login={self.login}, is_admin={self.is_admin}, "
            f"status={self.status}, created_at={self.created_at}, "
            f"updated_at={self.updated_at})>"
        )

    def from_raw(self, data: object) -> object:
        """Convert raw data to model.

        Args:
            data (object): Raw data.

        Returns:
            object: User model.
        """
        return User(
            uuid=str(uuid.uuid4()),
            external_id=data.id,
            first_name=data.firstName,
            last_name=data.lastName,
            full_name=data.name,
            email=data.email,
            login=data.login,
            is_admin=data.admin,
            created_at=data.createdAt,
            updated_at=data.updatedAt,
        )

    def to_dict(self) -> dict:
        """Convert model to dictionary.

        Returns:
            dict: User dictionary.
        """
        return {
            "uuid": self.uuid,
            "external_id": self.external_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "email": self.email,
            "login": self.login,
            "is_admin": self.is_admin,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
