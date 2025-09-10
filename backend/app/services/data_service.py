# backend/app/services/data_service.py
import json
from typing import List, Dict, Any, Optional
from pathlib import Path

from ..models.employee import Employee

class DataService:
    _instance = None
    _employees: List[Dict[str, Any]] = []

    @classmethod
    def load_data(cls, path: str):
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"employees.json not found at {path}")
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
        cls._employees = data.get("employees", [])
        cls._instance = cls()
        return cls._instance

    @classmethod
    def instance(cls):
        if cls._instance is None:
            raise RuntimeError("DataService not initialized. Call load_data() first.")
        return cls._instance

    def list_all(self) -> List[Dict[str, Any]]:
        return self._employees

    def filter(self, skill: Optional[str]=None, min_experience: Optional[int]=None,
               project: Optional[str]=None, availability: Optional[str]=None) -> List[Dict[str, Any]]:
        results = self._employees
        if skill:
            results = [e for e in results if any(skill.lower() in s.lower() for s in e.get("skills", []))]
        if min_experience:
            results = [e for e in results if e.get("experience_years", 0) >= min_experience]
        if project:
            results = [e for e in results if any(project.lower() in p.lower() for p in e.get("projects", []))]
        if availability:
            results = [e for e in results if availability.lower() == e.get("availability", "").lower()]
        return results
