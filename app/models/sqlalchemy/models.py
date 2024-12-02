import uuid
from datetime import datetime, timezone

from sqlalchemy import VARCHAR, Boolean, DateTime
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from aiwrappifymodels.rehearse_curate import Status, Curator

from app.models.sqlalchemy.base import Base




class TopicRecord(Base):
    __tablename__ = "topic"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    display_name: Mapped[str] = mapped_column(VARCHAR(1000), nullable=False)
    description: Mapped[str] = mapped_column(VARCHAR(1000), nullable=False)
    message_event_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False) # the event that triggered the topic
    agent_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    machine_curation_status: Mapped[Status] = mapped_column(VARCHAR(20), nullable=True)
    human_curation_status: Mapped[Status] = mapped_column(VARCHAR(20), nullable=True)
    create_time: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    digest_time: Mapped[datetime] = mapped_column(DateTime, nullable=True)


class HumanRawResponseRecord(Base):
    __tablename__ = "human_raw_response"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    response: Mapped[str] = mapped_column(VARCHAR(1000), nullable=False)
    topic_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    create_time: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )


class CuratedFileRecord(Base):
    __tablename__ = "curated_file"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    storage_uri: Mapped[str] = mapped_column(VARCHAR(1000), nullable=False) # to some minio/azure storage 
    topic_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    digest_status: Mapped[Status] = mapped_column(VARCHAR(20),nullable=True)
    source: Mapped[Curator] = mapped_column(VARCHAR(20), nullable=False)
    human_raw_response_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )
    create_time: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    



