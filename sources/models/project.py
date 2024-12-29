"""Project model."""

import uuid
from sqlalchemy import Column
from sqlalchemy.types import Uuid, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Project(Base):
    """Data Project model."""

    __tablename__ = "projects"
    uuid = Column(Uuid, primary_key=True)
    external_id = Column(Integer, unique=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, default="")
    identifier = Column(String(255))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    def __repr__(self) -> str:
        """Project representation.

        Returns:
            str: Project representation.
        """
        return (
            f"<Project(uuid={self.uuid}, external_id={self.external_id}, "
            f"name={self.name}, description={self.description}, "
            f"identifier={self.identifier}, "
            f"created_at={self.created_at}, updated_at={self.updated_at})>"
        )

    def from_raw(self, data: object) -> object:
        """Convert raw data to model.

        Args:
            data (object): Raw data.

        Returns:
            object: Project model.
        """
        return Project(
            uuid=str(uuid.uuid4()),
            external_id=data.id,
            name=data.name,
            identifier=data.identifier,
            created_at=data.createdAt,
            updated_at=data.updatedAt,
        )

    def to_dict(self) -> dict:
        """Convert model to dictionary.

        Returns:
            dict: Project dictionary.
        """
        return {
            "uuid": self.uuid,
            "external_id": self.external_id,
            "name": self.name,
            "description": self.description,
            "identifier": self.identifier,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
