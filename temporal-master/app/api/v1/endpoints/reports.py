"""
app/api/v1/endpoints/reports.py — D026 Reporte de Inteligencia

POST /reports         — Crear un reporte (requiere JWT)
GET  /reports         — Listar reportes (solo admin)
PATCH /reports/{id}   — Actualizar estado (solo admin)
"""

from __future__ import annotations

import uuid
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.intelligence_report import IntelligenceReport
from app.models.user import User

router = APIRouter(prefix="/reports", tags=["reports"])

# ─── Schemas ──────────────────────────────────────────────────────────────────

ReportType     = Literal["BUG", "UX_UI", "TACTICAL_IDEA"]
ReportSeverity = Literal["LOW", "HIGH", "CRITICAL"]
ReportStatus   = Literal["OPEN", "IN_PROGRESS", "RESOLVED"]


class ReportCreate(BaseModel):
    type:                ReportType
    severity:            ReportSeverity
    description:         str = Field(..., min_length=10, max_length=2000)
    steps_to_reproduce:  str | None = Field(None, max_length=2000)


class ReportOut(BaseModel):
    id:                  uuid.UUID
    user_id:             uuid.UUID
    type:                str
    severity:            str
    description:         str
    steps_to_reproduce:  str | None
    status:              str
    created_at:          str

    model_config = {"from_attributes": True}


class ReportStatusUpdate(BaseModel):
    status: ReportStatus


# ─── Endpoints ────────────────────────────────────────────────────────────────

@router.post("", status_code=status.HTTP_201_CREATED, response_model=ReportOut)
async def create_report(
    payload:      ReportCreate,
    current_user: User = Depends(get_current_user),
    db:           AsyncSession = Depends(get_db),
) -> ReportOut:
    """Crea un reporte de inteligencia para el operador autenticado."""
    report = IntelligenceReport(
        user_id             = current_user.id,
        type                = payload.type,
        severity            = payload.severity,
        description         = payload.description,
        steps_to_reproduce  = payload.steps_to_reproduce,
        status              = "OPEN",
    )
    db.add(report)
    await db.commit()
    await db.refresh(report)

    return ReportOut(
        id                 = report.id,
        user_id            = report.user_id,
        type               = report.type,
        severity           = report.severity,
        description        = report.description,
        steps_to_reproduce = report.steps_to_reproduce,
        status             = report.status,
        created_at         = report.created_at.isoformat(),
    )


@router.get("", response_model=list[ReportOut])
async def list_reports(
    current_user: User = Depends(get_current_user),
    db:           AsyncSession = Depends(get_db),
) -> list[ReportOut]:
    """Lista reportes. Admin ve todos; el operador ve solo los suyos."""
    if getattr(current_user, "is_admin", False) or getattr(current_user, "role", "") == "FOUNDER":
        result = await db.execute(
            select(IntelligenceReport).order_by(IntelligenceReport.created_at.desc())
        )
    else:
        result = await db.execute(
            select(IntelligenceReport)
            .where(IntelligenceReport.user_id == current_user.id)
            .order_by(IntelligenceReport.created_at.desc())
        )
    reports = result.scalars().all()
    return [
        ReportOut(
            id                 = r.id,
            user_id            = r.user_id,
            type               = r.type,
            severity           = r.severity,
            description        = r.description,
            steps_to_reproduce = r.steps_to_reproduce,
            status             = r.status,
            created_at         = r.created_at.isoformat(),
        )
        for r in reports
    ]


@router.patch("/{report_id}", response_model=ReportOut)
async def update_report_status(
    report_id:    uuid.UUID,
    payload:      ReportStatusUpdate,
    current_user: User = Depends(get_current_user),
    db:           AsyncSession = Depends(get_db),
) -> ReportOut:
    """Actualiza el estado de un reporte. Solo admin/FOUNDER."""
    if not (getattr(current_user, "is_admin", False) or getattr(current_user, "role", "") == "FOUNDER"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso denegado")

    result = await db.execute(
        select(IntelligenceReport).where(IntelligenceReport.id == report_id)
    )
    report = result.scalar_one_or_none()
    if not report:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")

    report.status = payload.status
    await db.commit()
    await db.refresh(report)

    return ReportOut(
        id                 = report.id,
        user_id            = report.user_id,
        type               = report.type,
        severity           = report.severity,
        description        = report.description,
        steps_to_reproduce = report.steps_to_reproduce,
        status             = report.status,
        created_at         = report.created_at.isoformat(),
    )
