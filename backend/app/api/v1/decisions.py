"""Decision API endpoints."""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models import Decision, DecisionVersion
from app.schemas.decision import (
    DecisionCreate,
    DecisionResponse,
    DecisionListResponse,
)

router = APIRouter()


@router.post("/", response_model=DecisionResponse, status_code=status.HTTP_201_CREATED)
async def create_decision(
    decision_data: DecisionCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new decision."""
    # For MVP, we'll use a temporary session_id (in production, get from auth)
    from uuid import uuid4
    temp_session_id = uuid4()
    
    # Create decision
    decision = Decision(
        session_id=temp_session_id,
        title=decision_data.title,
        original_input=decision_data.original_input,
        locale=decision_data.locale,
        current_version_number=1
    )
    
    db.add(decision)
    await db.flush()
    
    # Create initial version
    version = DecisionVersion(
        decision_id=decision.id,
        version_number=1,
        snapshot_status="active"
    )
    
    db.add(version)
    await db.commit()
    await db.refresh(decision)
    
    return DecisionResponse(
        id=decision.id,
        title=decision.title,
        original_input=decision.original_input,
        locale=decision.locale,
        current_version_number=decision.current_version_number,
        created_at=decision.created_at,
        updated_at=decision.updated_at
    )


@router.get("/{decision_id}", response_model=DecisionResponse)
async def get_decision(
    decision_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Get decision by ID."""
    result = await db.execute(
        select(Decision)
        .where(Decision.id == decision_id)
        .where(Decision.deleted_at.is_(None))
        .options(selectinload(Decision.versions))
    )
    decision = result.scalar_one_or_none()
    
    if not decision:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Decision not found"
        )
    
    return DecisionResponse(
        id=decision.id,
        title=decision.title,
        original_input=decision.original_input,
        locale=decision.locale,
        current_version_number=decision.current_version_number,
        created_at=decision.created_at,
        updated_at=decision.updated_at
    )


@router.delete("/{decision_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_decision(
    decision_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Soft delete a decision."""
    from datetime import datetime
    
    result = await db.execute(
        select(Decision)
        .where(Decision.id == decision_id)
        .where(Decision.deleted_at.is_(None))
    )
    decision = result.scalar_one_or_none()
    
    if not decision:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Decision not found"
        )
    
    decision.deleted_at = datetime.now()
    await db.commit()
    
    return None
