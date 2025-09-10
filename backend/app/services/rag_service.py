# backend/app/services/rag_service.py
from typing import List, Dict, Any
from .embedding_service import EmbeddingService
from .data_service import DataService
from ..utils.response_formatter import format_candidates_text, template_generate_response
from ..config import SETTINGS
from ..utils.text_processing import normalize_text
from sentence_transformers import util
# try to import ollama but keep fallback
try:
    import ollama
    OLLAMA_AVAILABLE = True
except Exception:
    OLLAMA_AVAILABLE = False

class RAGService:
    _instance = None

    def __init__(self, embedding_service: EmbeddingService, data_service: DataService, top_k: int = 3):
        self.embedding_service = embedding_service
        self.data_service = data_service
        self.top_k = top_k
        # Precompute index from data_service
        self._build_index()

    @classmethod
    def initialize(cls, embedding_service: EmbeddingService, data_service: DataService, top_k: int = 3):
        if cls._instance is None:
            cls._instance = RAGService(embedding_service, data_service, top_k)
        return cls._instance

    @classmethod
    def instance(cls):
        if cls._instance is None:
            raise RuntimeError("RAGService not initialized. Call initialize() first.")
        return cls._instance
    
    def _build_index(self):
        employees = self.data_service.list_all()
        texts = []
        self.employee_embeddings = {}  # Store embedding index by employee ID
        
        for idx, e in enumerate(employees):
            text = f"{e.get('name')} - {e.get('role','')} - Skills: {', '.join(e.get('skills',[]))}. Projects: {', '.join(e.get('projects',[]))}. Notes: {e.get('notes','')}"
            texts.append(text)
            self.employee_embeddings[e['id']] = idx  # Map ID to embedding index
        
        self.embedding_service.index(texts, employees)


    def retrieve(self, query: str, top_k: int = None):
        top_k = top_k or self.top_k
        employees = self.data_service.list_all()

        q = query.lower()

        # Step 1: Dynamically collect all unique skills and projects from DB
        all_skills = set(skill.lower() for e in employees for skill in e.get("skills", []))
        all_projects = set(
            proj.lower() for e in employees for proj in e.get("projects", []) + [e.get("notes","")]
        )

        # Step 2: Extract required skills/projects from query
        required_skills = [s for s in all_skills if s in q]
        required_projects = [p for p in all_projects if p in q]
        # Step 2.5: Check availability if mentioned in query
        all_status = set(e.get("availability","").lower() for e in employees)
        required_status = [s for s in all_status if s in q]

        
        # Step 3: Filter employees dynamically
        filtered = []
        for e in employees:
            
            skills = [normalize_text(s) for s in e.get("skills", [])]
            projects_notes_text = " ".join(e.get("projects", []) + [e.get("notes","")])
            projects_notes = normalize_text(projects_notes_text)

            # Check skills
            if required_skills and not any(rs in skills for rs in required_skills):
                continue

            # Check projects / notes using token-level intersection
            if required_projects:
                query_tokens = set(normalize_text(query).split())
                projects_notes_tokens = set(projects_notes.split())
                if not query_tokens.intersection(projects_notes_tokens):
                    continue

            # Check availability
            if required_status and e.get("availability","").lower() not in required_status:
                continue


            filtered.append(e)

        # Step 4: Rank filtered employees with embeddings
        # if filtered:
        #     texts = [
        #         f"{e['name']} - {e['role']} - Skills: {', '.join(e['skills'])}. "
        #         f"Projects: {', '.join(e['projects'])}. Notes: {e.get('notes','')}"
        #         for e in filtered
        #     ]
        #     temp_embeddings = self.embedding_service.encode_texts(texts)
        #     q_emb = self.embedding_service.encode_texts([query])[0]
        #     from sentence_transformers import util
        #     scores = util.cos_sim(q_emb, temp_embeddings)[0].cpu().numpy()
        #     idxs = scores.argsort()[::-1][:top_k]
        #     return [{"employee": filtered[i], "score": float(scores[i])} for i in idxs]
        
        if filtered:
            # Use precomputed embeddings instead of recomputing
            emb_indices = [self.employee_embeddings[e['id']] for e in filtered]
            filtered_embeddings = self.embedding_service.embeddings[emb_indices]
            
            q_emb = self.embedding_service.encode_texts([query])[0]
            scores = util.cos_sim(q_emb, filtered_embeddings)[0].cpu().numpy()
            idxs = scores.argsort()[::-1][:top_k]
            return [{"employee": filtered[i], "score": float(scores[i])} for i in idxs]
        # Step 5: Fallback to full semantic search
        idxs_scores = self.embedding_service.query(query, top_k=top_k)
        return [{"employee": self.embedding_service.meta[i], "score": s} for i, s in idxs_scores]


    def generate(self, query: str, top_k: int = None) -> Dict[str, Any]:
        top_k = top_k or self.top_k

        # 1️⃣ Retrieve candidates using dynamic filter + embeddings
        candidates = self.retrieve(query, top_k=top_k)

        # 2️⃣ Format candidates for response
        candidates_text = format_candidates_text([c["employee"] for c in candidates])
        prompt = f"""
    You are a helpful HR assistant. User query: "{query}"

    Top candidates:
    {candidates_text}

    Write a professional response recommending these candidates. Mention years of experience, relevant projects and skills, and availability. End with a follow-up question asking if the user wants more details or to schedule meetings.
    """

        # 3️⃣ Attempt Ollama (Mistral) generation
        # In rag_service.py, improve error handling:
        if OLLAMA_AVAILABLE and SETTINGS.USE_OLLAMA:
            try:
                # Add timeout and better error handling
                resp = ollama.chat(
                    model=SETTINGS.OLLAMA_MODEL,
                    messages=[{"role": "user", "content": prompt}],
                    options={'timeout': 30}  # Add timeout
                )
                text = resp.get("message", {}).get("content", "").strip()
                if text:
                    return {"answer": text, "candidates": candidates}
            except Exception as exc:
                print(f"Ollama call failed: {exc}, falling back to template")
        # 4️⃣ Fallback template response
        answer = template_generate_response(query, [c["employee"] for c in candidates])
        return {"answer": answer, "candidates": candidates}

        