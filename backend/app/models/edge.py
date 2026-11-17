"""Edge model."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin


class Edge(Base, UUIDMixin):
    """Relationship between nodes."""
    
    __tablename__ = "edges"
    
    decision_version_id: Mapped[UUID] = mapped_column(
        ForeignKey("decision_versions.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    source_node_id: Mapped[UUID] = mapped_column(
        ForeignKey("nodes.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    target_node_id: Mapped[UUID] = mapped_column(
        ForeignKey("nodes.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    edge_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    
    # Relationships
    decision_version: Mapped["DecisionVersion"] = relationship(
        "DecisionVersion",
        back_populates="edges"
    )
    source_node: Mapped["Node"] = relationship(
        "Node",
        foreign_keys=[source_node_id],
        back_populates="outgoing_edges"
    )
    target_node: Mapped["Node"] = relationship(
        "Node",
        foreign_keys=[target_node_id],
        back_populates="incoming_edges"
    )
    
    def __repr__(self) -> str:
        return f"<Edge(id={self.id}, type={self.edge_type}, {self.source_node_id}->{self.target_node_id})>"
