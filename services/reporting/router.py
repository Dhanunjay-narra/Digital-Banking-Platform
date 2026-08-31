"""Reporting API Endpoints."""

from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session
from finx_platform.common.database import get_db
from services.reporting.service import reporting_engine

router = APIRouter(prefix="/reporting", tags=["Reporting Engine"])


@router.get("/statement")
def get_statement(
    account_number: str = Query("100019283746"),
    format_type: str = Query("json"),
    db: Session = Depends(get_db)
):
    res = reporting_engine.generate_account_statement(db, account_number, format_type)
    if format_type.lower() == "csv":
        return Response(content=res, media_type="text/csv", headers={"Content-Disposition": f"attachment; filename=statement_{account_number}.csv"})
    return res
