# backend/app/routers/employees.py
from fastapi import APIRouter, Query
from typing import Optional
from ..services.data_service import DataService
from ..models.employee import Employee

router = APIRouter()

@router.get("/search", response_model=list[Employee])
def search_employees(
    skill: Optional[str] = Query(None, description="Skill substring to match"),
    min_experience: Optional[int] = Query(None, ge=0, description="Minimum years of experience"),
    project: Optional[str] = Query(None, description="Project keyword"),
    availability: Optional[str] = Query(None, description="availability (available|busy|on_notice)")
):
    svc = DataService.instance()
    results = svc.filter(skill=skill, min_experience=min_experience, project=project, availability=availability)
    return results
