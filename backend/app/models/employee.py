# backend/app/models/employee.py
from pydantic import BaseModel
from typing import List, Optional

class Employee(BaseModel):
    id: int
    name: str
    role: Optional[str] = None
    skills: List[str]
    experience_years: int
    projects: List[str]
    availability: str
    notes: Optional[str] = None

class EmployeeSearchResult(BaseModel):
    employee: Employee
    score: float

class EmployeeSearchQuery(BaseModel):
    skill: Optional[str] = None
    min_experience: Optional[int] = None
    project: Optional[str] = None
    availability: Optional[str] = None

class ChatRequest(BaseModel):
    query: str
    top_k: Optional[int] = 3

class ChatResponse(BaseModel):
    answer: str
    candidates: List[EmployeeSearchResult]
