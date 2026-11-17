"""Session model."""

from datetime import datetime
from typing import List
from uuid import UUID

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class Session(Base, UUIDMixin, TimestampMixin):
    """Anonymous session model."""
    
    __tablename__ = "sessions"
    
    session_token_hash: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    
    # Relationships
    decisions: Mapped[List["Decision"]] = relationship(
        "Decision",
        back_populates="session",
        cascade="all, delete-orphan"
    )
    audit_events: Mapped[List["AuditEvent"]] = relationship(
        "AuditEvent",
        back_populates="session"
    )
    
    def __repr__(self) -> str:
        return f"<Session(id={self.id}, expires_at={self.expires_at})>"
