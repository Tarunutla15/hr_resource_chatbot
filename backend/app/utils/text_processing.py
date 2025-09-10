# backend/app/utils/text_processing.py
# Small helpers — keep modular in case we want to add keyword extraction later

import re
from typing import List

# In text_processing.py, ensure robust normalization:
def normalize_text(text: str) -> str:
    if not text:
        return ""
    # Convert to lowercase, remove punctuation, extra spaces
    text = text.lower().strip()
    text = re.sub(r'[^\w\s]', ' ', text)  # Remove punctuation
    text = re.sub(r'\s+', ' ', text)      # Collapse multiple spaces
    return text

def split_skills(skills_str: str) -> List[str]:
    # simple splitter for CSV/pipe formats
    for sep in [',', '|', ';']:
        if sep in skills_str:
            return [x.strip() for x in skills_str.split(sep) if x.strip()]
    return [skills_str.strip()] if skills_str.strip() else []
