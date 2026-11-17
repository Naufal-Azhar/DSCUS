"""Decision and DecisionVersion models."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

import sqlalchemy.dialects.postgresql
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class Decision(Base, UUIDMixin, TimestampMixin):
    """Decision model."""
    
    __tablename__ = "decisions"
    
    session_id: Mapped[UUID] = mapped_column(
        ForeignKey("sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    original_input: Mapped[str] = mapped_column(Text, nullable=False)
    locale: Mapped[str] = mapped_column(String(10), nullable=False, default="en")
    current_version_number: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    session: Mapped["Session"] = relationship("Session", back_populates="decisions")
    versions: Mapped[List["DecisionVersion"]] = relationship(
        "DecisionVersion",
        back_populates="decision",
        cascade="all, delete-orphan",
        order_by="DecisionVersion.version_number"
    )
    scenarios: Mapped[List["Scenario"]] = relationship(
        "Scenario",
        back_populates="decision",
        cascade="all, delete-orphan"
    )
    audit_events: Mapped[List["AuditEvent"]] = relationship(
        "AuditEvent",
        back_populates="decision"
    )
    
    def __repr__(self) -> str:
        return f"<Decision(id={self.id}, title={self.title[:50]})>"


class DecisionVersion(Base, UUIDMixin):
    """Immutable decision version snapshot."""
    
    __tablename__ = "decision_versions"
    
    decision_id: Mapped[UUID] = mapped_column(
        ForeignKey("decisions.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    snapshot_status: Mapped[str] = mapped_column(String(50), nullable=False, default="active")
    snapshot_metadata: Mapped[Optional[dict]] = mapped_column(
        type_=sqlalchemy.dialects.postgresql.JSONB,
        nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    
    # Relationships
    decision: Mapped["Decision"] = relationship("Decision", back_populates="versions")
    nodes: Mapped[List["Node"]] = relationship(
        "Node",
        back_populates="decision_version",
        cascade="all, delete-orphan"
    )
    edges: Mapped[List["Edge"]] = relationship(
        "Edge",
        back_populates="decision_version",
        cascade="all, delete-orphan"
    )
    scenarios_as_baseline: Mapped[List["Scenario"]] = relationship(
        "Scenario",
        back_populates="baseline_version"
    )
    evaluations: Mapped[List["Evaluation"]] = relationship(
        "Evaluation",
        back_populates="decision_version"
    )
    
    __table_args__ = (
        sqlalchemy.UniqueConstraint("decision_id", "version_number", name="uq_decision_version"),
    )
    
    def __repr__(self) -> str:
        return f"<DecisionVersion(id={self.id}, decision_id={self.decision_id}, v={self.version_number})>"
