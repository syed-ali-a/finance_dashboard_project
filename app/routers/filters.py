from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import extract
from typing import List, Dict

from app.database import get_db
from app.models import DailyRevenue

router = APIRouter(prefix="/api/filters", tags=["Filters"])

@router.get("/dates")
def get_available_dates(db: Session = Depends(get_db)):
    # Get distinct years
    years_query = db.query(extract('year', DailyRevenue.date)).distinct().order_by(extract('year', DailyRevenue.date).desc()).all()
    years = [int(y[0]) for y in years_query if y[0]]
    
    # Get distinct months
    months_query = db.query(extract('month', DailyRevenue.date)).distinct().order_by(extract('month', DailyRevenue.date)).all()
    months = [int(m[0]) for m in months_query if m[0]]
    
    return {
        "years": years,
        "months": months
    }
