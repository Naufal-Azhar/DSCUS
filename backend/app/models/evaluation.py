"""Evaluation model."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin


class Evaluation(Base, UUIDMixin):
    """Deterministic evaluation result."""
    
    __tablename__ = "evaluations"
    
    decision_version_id: Mapped[UUID] = mapped_column(
        ForeignKey("decision_versions.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    scenario_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("scenarios.id", ondelete="CASCADE"),
        nullable=True,
        index=True
    )
    evaluation_kind: Mapped[str] = mapped_column(String(50), nullable=False)
    engine_version: Mapped[str] = mapped_column(String(50), nullable=False)
    result_summary: Mapped[dict] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True
    )
    
    # Relationships
    decision_version: Mapped["DecisionVersion"] = relationship(
        "DecisionVersion",
        back_populates="evaluations"
    )
    scenario: Mapped[Optional["Scenario"]] = relationship(
        "Scenario",
        back_populates="evaluations"
    )
    
    def __repr__(self) -> str:
        return f"<Evaluation(id={self.id}, kind={self.evaluation_kind}, v={self.engine_version})>"
