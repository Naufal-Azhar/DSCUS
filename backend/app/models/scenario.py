"""Scenario and ScenarioChange models."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class Scenario(Base, UUIDMixin, TimestampMixin):
    """Stress-test scenario."""
    
    __tablename__ = "scenarios"
    
    decision_id: Mapped[UUID] = mapped_column(
        ForeignKey("decisions.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    baseline_version_id: Mapped[UUID] = mapped_column(
        ForeignKey("decision_versions.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active")
    is_stale: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    
    # Relationships
    decision: Mapped["Decision"] = relationship("Decision", back_populates="scenarios")
    baseline_version: Mapped["DecisionVersion"] = relationship(
        "DecisionVersion",
        back_populates="scenarios_as_baseline"
    )
    changes: Mapped[List["ScenarioChange"]] = relationship(
        "ScenarioChange",
        back_populates="scenario",
        cascade="all, delete-orphan"
    )
    evaluations: Mapped[List["Evaluation"]] = relationship(
        "Evaluation",
        back_populates="scenario"
    )
    
    def __repr__(self) -> str:
        return f"<Scenario(id={self.id}, name={self.name}, stale={self.is_stale})>"


class ScenarioChange(Base, UUIDMixin):
    """Change applied in a scenario."""
    
    __tablename__ = "scenario_changes"
    
    scenario_id: Mapped[UUID] = mapped_column(
        ForeignKey("scenarios.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    node_id: Mapped[UUID] = mapped_column(
        ForeignKey("nodes.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    field_name: Mapped[str] = mapped_column(String(100), nullable=False)
    old_value: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    new_value: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    
    # Relationships
    scenario: Mapped["Scenario"] = relationship("Scenario", back_populates="changes")
    node: Mapped["Node"] = relationship("Node", back_populates="scenario_changes")
    
    def __repr__(self) -> str:
        return f"<ScenarioChange(id={self.id}, scenario={self.scenario_id}, node={self.node_id})>"
