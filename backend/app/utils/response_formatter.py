# backend/app/utils/response_formatter.py
from typing import List, Dict

def format_candidates_text(employees: List[Dict]) -> str:
    parts = []
    for i, e in enumerate(employees, start=1):
        parts.append(
            f"{i}. {e.get('name')} — {e.get('experience_years', 'N/A')} years. "
            f"Projects: {', '.join(e.get('projects', []))}. "
            f"Skills: {', '.join(e.get('skills', []))}. Availability: {e.get('availability','unknown')}."
        )
    return "\n".join(parts)

def template_generate_response(query: str, employees: List[Dict]) -> str:
    if not employees:
        return f"Sorry — I couldn't find anyone matching: \"{query}\". Could you provide more details or relax some constraints?"
    lines = [f"Based on your requirements for \"{query}\", I found {len(employees)} candidate(s):\n"]
    for e in employees:
        lines.append(
            f"**{e.get('name')}** ({e.get('role','')}) has {e.get('experience_years')} years of experience and worked on projects like {', '.join(e.get('projects',[]))}. "
            f"Key skills: {', '.join(e.get('skills',[]))}. Availability: {e.get('availability','unknown')}.\n"
        )
    lines.append("Would you like more details about any candidate or shall I check their availability for meetings?")
    return "\n".join(lines)
