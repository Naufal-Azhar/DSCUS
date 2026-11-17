"""Node model."""

from typing import List, Optional
from uuid import UUID

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class Node(Base, UUIDMixin, TimestampMixin):
    """Reasoning element node."""
    
    __tablename__ = "nodes"
    
    decision_version_id: Mapped[UUID] = mapped_column(
        ForeignKey("decision_versions.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    node_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Provenance
    origin: Mapped[str] = mapped_column(String(50), nullable=False)
    created_by: Mapped[str] = mapped_column(String(50), nullable=False)
    updated_by: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    # State fields (type-specific)
    assumption_state: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    review_state: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    grounded_label: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    evaluation_status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    impact_status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    # Extra metadata (rename to avoid SQLAlchemy conflict)
    extra_data: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    
    # Relationships
    decision_version: Mapped["DecisionVersion"] = relationship(
        "DecisionVersion",
        back_populates="nodes"
    )
    outgoing_edges: Mapped[List["Edge"]] = relationship(
        "Edge",
        foreign_keys="Edge.source_node_id",
        back_populates="source_node",
        cascade="all, delete-orphan"
    )
    incoming_edges: Mapped[List["Edge"]] = relationship(
        "Edge",
        foreign_keys="Edge.target_node_id",
        back_populates="target_node",
        cascade="all, delete-orphan"
    )
    scenario_changes: Mapped[List["ScenarioChange"]] = relationship(
        "ScenarioChange",
        back_populates="node"
    )
    
    def __repr__(self) -> str:
        return f"<Node(id={self.id}, type={self.node_type}, title={self.title[:30]})>"
